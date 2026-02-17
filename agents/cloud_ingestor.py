import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
import re

class CloudIngestor:
    def __init__(self, service_account_json_str, sheet_id):
        # Authenticate with Google
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = json.loads(service_account_json_str)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        self.client = gspread.authorize(creds)
        self.sheet_id = sheet_id

    def get_current_month_worksheet(self):
        """Finds the tab matching the YYMM pattern (e.g., エラー報告_2602)."""
        workbook = self.client.open_by_key(self.sheet_id)
        # Assuming we want the tab that contains current month/year pattern
        target_pattern = datetime.now().strftime("%y%m")
        for sheet in workbook.worksheets():
            if target_pattern in sheet.title:
                return sheet
        return workbook.get_worksheet(0) # Fallback to first tab

    def get_live_tasks(self):
        """Reads the worksheet and uses our block-parsing logic."""
        worksheet = self.get_current_month_worksheet()
        all_data = worksheet.get_all_values()
        
        # We reuse the logic from our ErrorReportParser but on list of lists
        tasks = []
        for i, row in enumerate(all_data):
            if row and row[0].isdigit():
                # Logic to extract data from the row blocks (same as CSV parser)
                task = self._parse_block_from_list(all_data, i)
                if task and self._is_valid(task):
                    tasks.append(task)
        return tasks

    def _is_valid(self, task):
        # Same logic: Filter 2025 and placeholders
        return "2025" not in task['date'] and task['requester'] != ""

    def _parse_block_from_list(self, data, start_index):
        # Implementation of the block extraction logic from previous parser
        # ... (Simplified for brevity in this prototype)
        return {
            "id": data[start_index][0],
            "requester": data[start_index][3],
            "date": data[start_index][4],
            "content": data[start_index + 2][3],
            "estimated_hours": 1.0 # Default fallback
        }
