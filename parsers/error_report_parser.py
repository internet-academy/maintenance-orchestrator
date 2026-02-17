import csv
import os
import re
from datetime import datetime

class ErrorReportParser:
    def __init__(self, directory):
        self.directory = directory
        # Matches the pattern: 🆕UX設計・システム開発管理シート - エラー報告_YYMM.csv
        self.file_pattern = re.compile(r"🆕UX設計・システム開発管理シート - エラー報告_(\d{4})\.csv")

    def get_latest_file(self):
        """Finds the CSV file for the current month/year."""
        files = [f for f in os.listdir(self.directory) if self.file_pattern.match(f)]
        if not files:
            return None
        # Sort by YYMM descending
        files.sort(key=lambda x: self.file_pattern.search(x).group(1), reverse=True)
        return os.path.join(self.directory, files[0])

    def parse_file(self, file_path):
        """Parses the block-style CSV into a list of clean dictionaries."""
        tasks = []
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = list(csv.reader(f))
            
            # Iterate through rows looking for numeric IDs in the first column
            for i, row in enumerate(reader):
                if row and row[0].isdigit():
                    task = self._extract_block(reader, i)
                    if self._is_valid_task(task):
                        tasks.append(task)
        return tasks

    def _extract_block(self, reader, start_index):
        """Extracts data from specific offsets within an ID block."""
        # Row 0: ID, Requester, Date
        # Row 2: Content (Problem)
        # Row 3: Chat URL
        # Row 7: PIC, Est Hours
        # Row 8: Status
        
        try:
            id_val = reader[start_index][0]
            requester = reader[start_index][3]
            date_val = reader[start_index][4]
            content = reader[start_index + 2][3]
            chat_url = reader[start_index + 3][3]
            
            # Offsets for PIC and Status vary slightly in visual blocks, 
            # based on the 'System Development' sub-header location.
            # We look for 'PIC' and 'Status' labels in the nearby rows.
            pic = ""
            est_hours = 0
            status = ""
            
            for offset in range(1, 15):
                search_row = reader[start_index + offset]
                row_str = ",".join(search_row)
                if "PIC" in row_str:
                    pic = search_row[search_row.index("PIC") + 1]
                if "Estimated Hours" in row_str:
                    try:
                        idx = search_row.index("Estimated Hours")
                        est_hours = float(search_row[idx + 1] or 0)
                    except (ValueError, IndexError): pass
                if "Status" in row_str:
                    status = search_row[search_row.index("Status") + 1]

            return {
                "id": id_val,
                "requester": requester,
                "date": date_val,
                "content": content,
                "chat_url": chat_url,
                "pic": pic,
                "estimated_hours": est_hours,
                "status": status.lower().strip()
            }
        except IndexError:
            return None

    def _is_valid_task(self, task):
        """Filters out template data and empty tasks."""
        if not task or not task['requester'] or not task['date']:
            return False
        
        # Filter out 2025 placeholder dates (Current year is 2026)
        if "2025" in task['date']:
            return False
            
        # Ignore if it's already closed or empty
        if not task['content'] or task['status'] == "closed":
            return False
            
        return True

if __name__ == "__main__":
    # Test with the specific directory
    DIR = "/home/min/ia/mini-projects"
    parser = ErrorReportParser(DIR)
    latest = parser.get_latest_file()
    if latest:
        print(f"Analyzing: {latest}")
        results = parser.parse_file(latest)
        for t in results:
            print(f"ID {t['id']}: [{t['pic']}] {t['content'][:50]}... ({t['estimated_hours']}h)")
    else:
        print("No matching CSV found.")
