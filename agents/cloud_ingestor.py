import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
import re
from datetime import datetime

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
        """Finds the tab matching the YYMM pattern (e.g., エラー報告_2602)."""
        workbook = self.client.open_by_key(self.sheet_id)
        target_pattern = datetime.now().strftime("%y%m")
        for sheet in workbook.worksheets():
            if target_pattern in sheet.title:
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
        
        # VERIFICATION: Anchor is at (row+1, col+1). Value is at (row+1, col+2).
        label_cell = worksheet.cell(row + 1, col + 1).value
        if "Backlog ID" in label_cell or "Ticket" in label_cell:
            worksheet.update_cell(row + 1, col + 2, issue_key)
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
        # row, col are 0-based. gspread is 1-based.
        # Anchor (Label) is at (row+1, col+1).
        # Value is at (row+1, col+2).
        label_cell = worksheet.cell(row + 1, col + 1).value
        if "Status" in label_cell:
            worksheet.update_cell(row + 1, col + 2, status_text)
        else:
            print(f"CRITICAL: Anchor mismatch at R{row+1}C{col+1}. Expected 'Status', found '{label_cell}'. Write ABORTED.")

    def _is_valid(self, task):
        # Reject tasks with no date, no requester, OR no content
        return "2025" not in task['date'] and task['requester'] != "" and task['content'] != ""

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
                        if col_idx + offset < len(row) and row[col_idx + offset].strip():
                            task["pic"] = row[col_idx + offset].strip()
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
                # If we hit another label or an empty row with a known label in Col 1, stop capture
                if len(row) > 1 and row[1].strip() in ["プロダクト", "希望締切", "エラー/仕様変更", "依頼者名/報告日"]:
                    content_capture_active = False
                    translation_capture_active = False
                elif val and not any(x in val for x in ["内容", "報告/相談", "翻訳"]):
                    if content_capture_active:
                        # Heuristic: If it contains many English chars, it might be the start of translation
                        # But the sheet usually has them in order: JA, then EN
                        # For now, let's just append everything to content until we find the Translation label
                        task["content"] = (task["content"] + "\n" + val).strip()
                    elif translation_capture_active:
                        task["english_translation_fallback"] = (task["english_translation_fallback"] + "\n" + val).strip()

        # Final Fallback for Backlog ID (Check Column J of first row)
        if not task["backlog_id"] and len(first_row) > 9:
            raw_id = first_row[9].strip()
            if re.match(r"^[A-Z0-9_]+-\d+$", raw_id):
                task["backlog_id"] = raw_id
                task["anchors"]["backlog_id"] = (start_index, 9)

        if task["content"] == "":
            print(f"DEBUG: Task {task['id']} at R{start_index+1} has NO content captured.")

        return task
