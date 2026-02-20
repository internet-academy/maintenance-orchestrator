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

    def write_backlog_id(self, row_index, issue_key):
        """Writes the Backlog ID to the 10th column (J) of the sheet."""
        worksheet = self.get_current_month_worksheet()
        # gspread uses 1-based indexing
        worksheet.update_cell(row_index + 1, 10, issue_key)

    def _is_valid(self, task):
        return "2025" not in task['date'] and task['requester'] != ""

    def _parse_block_from_list(self, data, start_index):
        row = data[start_index]
        content_row = data[start_index + 2] if (start_index + 2) < len(data) else [""] * 10
        
        # SEARCH for the specific row containing 'PIC' and 'Estimated Hours'
        est_hours = 0.0
        pic = None
        for offset in range(1, 15):
            if (start_index + offset) >= len(data):
                break
            
            search_row = data[start_index + offset]
            
            # According to inspection, PIC and Estimated Hours are in the same row
            if len(search_row) > 12 and search_row[9] == "PIC" and "Estimated Hours" in search_row[12]:
                # PIC is in index 10
                pic = search_row[10].strip() if search_row[10] else None
                
                # Hours are in index 13
                try:
                    val = search_row[13] if len(search_row) > 13 else "0"
                    est_hours = float(val) if val and str(val).strip() else 0.0
                except (ValueError, TypeError):
                    est_hours = 1.0 # Fallback
                break

        # Validate Backlog ID format (e.g., MD_SD-1234)
        raw_backlog_id = row[9] if len(row) > 9 else None
        backlog_id = None
        if raw_backlog_id and re.match(r"^[A-Z0-9_]+-\d+$", raw_backlog_id):
            backlog_id = raw_backlog_id
        
        return {
            "row_index": start_index,
            "id": row[0],
            "requester": row[3],
            "date": row[4],
            "content": content_row[3] if len(content_row) > 3 else "",
            "estimated_hours": est_hours,
            "backlog_id": backlog_id,
            "pic": pic
        }
