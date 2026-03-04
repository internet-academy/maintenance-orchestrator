import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
import re
from datetime import datetime, timedelta

class CloudIngestor:
    def __init__(self, service_account_json_str, sheet_id):
        # Authenticate with Google
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        if not service_account_json_str:
            raise ValueError("ERROR: GOOGLE_SERVICE_ACCOUNT_JSON is empty or missing from environment.")
            
        try:
            # CHECK: Is this a file path or a raw JSON string?
            if os.path.exists(service_account_json_str):
                print(f"DEBUG: Loading Service Account from file: {service_account_json_str}")
                with open(service_account_json_str, 'r') as f:
                    creds_dict = json.load(f)
            else:
                print(f"DEBUG: Loading Service Account from string (Length: {len(service_account_json_str)})")
                creds_dict = json.loads(service_account_json_str)
            
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            self.client = gspread.authorize(creds)
            self.sheet_id = sheet_id
        except json.JSONDecodeError as e:
            print(f"CRITICAL: Failed to decode Service Account JSON. Ensure valid JSON or valid file path.")
            print(f"Error Detail: {str(e)}")
            raise

    def get_current_month_worksheet(self):
        """Finds the tab matching the YYMM pattern (e.g., エラー報告_2602), favoring recent reports."""
        workbook = self.client.open_by_key(self.sheet_id)
        
        # 1. Try current month (YYMM)
        target_pattern = datetime.now().strftime("%y%m")
        for sheet in workbook.worksheets():
            if target_pattern in sheet.title and "エラー報告" in sheet.title:
                return sheet
                
        # 2. Try last month if current month doesn't exist yet
        last_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%y%m")
        for sheet in workbook.worksheets():
            if last_month in sheet.title and "エラー報告" in sheet.title:
                return sheet
        
        # 3. Fallback to any 'エラー報告' tab
        for sheet in workbook.worksheets():
            if "エラー報告" in sheet.title:
                return sheet
                
        return workbook.get_worksheet(0)

    def get_live_tasks(self):
        """Reads the worksheet and uses our block-parsing logic."""
        worksheet = self.get_current_month_worksheet()
        gid = worksheet.id
        all_data = worksheet.get_all_values()
        
        tasks = []
        # Start from Row 18 to skip headers and the Example (記入例) block
        for i in range(18, len(all_data)):
            row = all_data[i]
            # Check if row starts with a number (Task ID)
            if row and row[0].strip().isdigit():
                task = self._parse_block_from_list(all_data, i)
                if task and self._is_valid(task):
                    task['gid'] = gid # Attach worksheet ID for linking
                    tasks.append(task)
        return tasks

    def write_backlog_id(self, anchor_map, issue_key):
        """Writes the Backlog ID using verified anchor coordinates."""
        if not anchor_map or 'backlog_id' not in anchor_map:
            print("ERROR: No anchor found for Backlog ID. Skipping write.")
            return

        row, col = anchor_map['backlog_id']
        worksheet = self.get_current_month_worksheet()
        
        # VERIFICATION: If anchor is at Column J (9), we allow writing even if label is missing
        # because it's our designated ID column. Otherwise, we verify the label.
        label_cell = str(worksheet.cell(row + 1, col + 1).value or "").strip()
        is_valid_label = "Backlog ID" in label_cell or "Ticket" in label_cell or col == 9
        
        if is_valid_label:
            # If col == 9, we write directly to the cell (it's the value cell, not the label cell)
            # In other cases, we write to col + 2 (the value cell next to the label)
            target_col = col + 1 if col == 9 else col + 2
            worksheet.update_cell(row + 1, target_col, issue_key)
        else:
            print(f"CRITICAL: Anchor mismatch at R{row+1}C{col+1}. Expected 'Backlog ID', found '{label_cell}'. Write ABORTED.")

    def write_status(self, anchor_map, status_text):
        """Writes the task status using verified anchor coordinates."""
        if not anchor_map or 'status' not in anchor_map:
            print("ERROR: No anchor found for Status. Skipping write.")
            return

        row, col = anchor_map['status']
        worksheet = self.get_current_month_worksheet()
        
        # VERIFICATION
        label_cell = worksheet.cell(row + 1, col + 1).value
        if "Status" in label_cell:
            worksheet.update_cell(row + 1, col + 2, status_text)
        else:
            print(f"CRITICAL: Anchor mismatch at R{row+1}C{col+1}. Expected 'Status', found '{label_cell}'. Write ABORTED.")

    def write_pic(self, anchor_map, pic_name):
        """Writes the PIC using verified anchor coordinates."""
        if not anchor_map or 'pic' not in anchor_map:
            print("ERROR: No anchor found for PIC. Skipping write.")
            return

        row, col = anchor_map['pic']
        worksheet = self.get_current_month_worksheet()
        
        # Verification: Label should be "PIC"
        label_cell = str(worksheet.cell(row + 1, col + 1).value or "").strip()
        if "PIC" in label_cell:
            worksheet.update_cell(row + 1, col + 2, pic_name)
        else:
            print(f"CRITICAL: Anchor mismatch at R{row+1}C{col+1}. Expected 'PIC', found '{label_cell}'. Write ABORTED.")

    def write_dates(self, anchor_map, start_date, end_date):
        """
        Writes Start and End dates. 
        Note: The sheet may not have explicit anchors for these, so we use heuristics 
        near the Status/PIC area if missing, but for now we look for 'Start Date' labels.
        """
        worksheet = self.get_current_month_worksheet()
        
        # Heuristic: Find 'Start Date' and 'End Date' labels in the same block
        # We search the block rows (roughly 15 rows)
        if not anchor_map or 'status' not in anchor_map: return
        
        row_start, _ = anchor_map['status']
        for r in range(row_start, row_start + 10):
            row_vals = worksheet.row_values(r + 1)
            for c, val in enumerate(row_vals):
                if "Start date" in str(val):
                    worksheet.update_cell(r + 1, c + 2, start_date)
                if "End date" in str(val) or "Finish date" in str(val):
                    worksheet.update_cell(r + 1, c + 2, end_date)

    def _is_valid(self, task):
        # Reject tasks with no date, no requester, OR no content.
        # Ensure we are processing current 2026 tasks.
        has_metadata = task['requester'] != "" and task['content'] != ""
        is_current = "2026" in task['date']
        return has_metadata and is_current

    def _parse_block_from_list(self, data, start_index):
        """
        Stateful parser that treats a range of rows as a single 'Form Block'.
        Tracks absolute coordinates (anchors) for all metadata fields.
        """
        block_rows = []
        for i in range(start_index, min(start_index + 15, len(data))):
            # If we hit a new numeric ID, the current block ends
            if i > start_index and data[i] and data[i][0].strip().isdigit():
                break
            block_rows.append(data[i])
        
        first_row = block_rows[0]
        task = {
            "row_index": start_index,
            "id": first_row[0].strip(),
            "requester": first_row[3].strip() if len(first_row) > 3 else "",
            "date": first_row[4].strip() if len(first_row) > 4 else "",
            "content": "",
            "english_translation_fallback": "",
            "estimated_hours": 1.0,
            "backlog_id": None,
            "pic": None,
            "current_sheet_status": "",
            "anchors": {} 
        }

        # Multi-row content capture state
        content_capture_active = False
        translation_capture_active = False

        for i, row in enumerate(block_rows):
            abs_row_idx = start_index + i
            
            # --- LABEL-BASED METADATA SEARCH (Restricted to Columns 8+) ---
            for col_idx in range(8, len(row)):
                cell_clean = str(row[col_idx]).strip()
                
                if cell_clean == "PIC" and col_idx + 1 < len(row):
                    # Check the next few cells as PIC/Hours often shift
                    for offset in [1, 2, 3, 4]:
                        if col_idx + offset < len(row):
                            val = row[col_idx + offset].strip()
                            # PIC Validation: Skip if value is empty, a known label, or numeric
                            is_label = val in ["Estimated Hours", "Status", "Ticket", "Backlog ID", "ID"]
                            if val and not is_label and not val.replace(".", "").isdigit():
                                task["pic"] = val
                                task["anchors"]["pic"] = (abs_row_idx, col_idx)
                                break
                
                if cell_clean == "Status" and col_idx + 1 < len(row):
                    task["current_sheet_status"] = row[col_idx + 1].strip()
                    task["anchors"]["status"] = (abs_row_idx, col_idx)
                
                if "Estimated Hours" in cell_clean and col_idx + 1 < len(row):
                    for offset in [1, 2, 3, 4]:
                        if col_idx + offset < len(row) and row[col_idx + offset].strip():
                            try:
                                val = row[col_idx + offset].strip()
                                task["estimated_hours"] = float(val) if val else 1.0
                                task["anchors"]["est_hours"] = (abs_row_idx, col_idx)
                                break
                            except (ValueError, TypeError):
                                continue
                    
                if ("Backlog ID" in cell_clean or "Ticket" in cell_clean or "MD_SD-" in cell_clean) and col_idx + 1 < len(row):
                    # If the cell itself contains the ID, use it, otherwise check the next cell
                    raw_id = cell_clean if "MD_SD-" in cell_clean else row[col_idx + 1].strip()
                    if re.match(r"^[A-Z0-9_]+-\d+$", raw_id):
                        task["backlog_id"] = raw_id
                        task["anchors"]["backlog_id"] = (abs_row_idx, col_idx)

            # --- CONTENT SEARCH (Columns 0-7) ---
            for col_idx in range(0, min(8, len(row))):
                cell_clean = str(row[col_idx]).strip()
                if "内容" in cell_clean or "報告/相談" in cell_clean:
                    content_capture_active = True
                    translation_capture_active = False
                    task["anchors"]["content"] = (abs_row_idx, col_idx)
                    continue

                if ("Translation" in cell_clean or "翻訳" in cell_clean) and col_idx + 1 < len(row):
                    translation_capture_active = True
                    content_capture_active = False
                    task["anchors"]["translation"] = (abs_row_idx, col_idx)
                    continue

            # --- VALUE AGGREGATION ---
            # In this sheet, values are consistently in Column 3 (D)
            if (content_capture_active or translation_capture_active) and len(row) > 3:
                val = row[3].strip()
                
                # Boundary Check
                potential_label = row[1].strip() if len(row) > 1 else ""
                is_boundary = potential_label in ["プロダクト", "希望締切", "エラー/仕様変更", "依頼者名/報告日"]
                
                if is_boundary:
                    content_capture_active = False
                    translation_capture_active = False
                elif val and not any(x in val for x in ["内容", "報告/相談", "翻訳"]):
                    if translation_capture_active:
                        task["english_translation_fallback"] = (task["english_translation_fallback"] + "\n" + val).strip() if task["english_translation_fallback"] else val
                    elif content_capture_active:
                        # If we find clear English content INSIDE the Japanese area, and don't have a fallback, treat it as a potential fallback
                        is_likely_english = all(ord(c) < 128 for c in val.replace("\n", "").replace(" ", "").replace("/", "").replace(":", "").replace("-", ""))
                        if is_likely_english and not task["english_translation_fallback"] and task["content"]:
                             task["english_translation_fallback"] = val
                        else:
                             task["content"] = (task["content"] + "\n" + val).strip() if task["content"] else val

        # Final Cleanup: Strip all multi-line values to ensure stable hashing
        task["content"] = task["content"].strip()
        task["english_translation_fallback"] = task["english_translation_fallback"].strip()

        # Final Fallback for Backlog ID (Check Column J of first row)
        if len(first_row) > 9:
            raw_id = first_row[9].strip()
            if re.match(r"^[A-Z0-9_]+-\d+$", raw_id):
                task["backlog_id"] = raw_id
            
            # ALWAYS set an anchor for Backlog ID if not already found via label.
            # This allows new tickets to be written back to Column J.
            if "backlog_id" not in task["anchors"]:
                task["anchors"]["backlog_id"] = (start_index, 9)

        if task["content"] == "":
            print(f"DEBUG: Task {task['id']} at R{start_index+1} has NO content captured.")

        return task
