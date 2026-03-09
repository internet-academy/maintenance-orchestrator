import os
import json
import re
import time
from datetime import datetime, timedelta

class ReportManager:
    def __init__(self, gh_specialist, ingestor, dry_run=False):
        self.gh = gh_specialist
        self.ingestor = ingestor
        self.dry_run = dry_run
        self.sheet_id = '1x0IXmY7cSlN2kRyOVRh_ZbdgPHn8bVaqfu5PAiNxs5M'
        
        # Empirical coordinates from Weekly Report tab (1-based for gspread)
        # Each block is assumed to have 3-4 rows of tasks based on sheet scan
        self.pic_map = {
            "Choo":    {"last": (5, 1),  "next": (12, 1),  "gh": os.getenv('GH_USER_CHOO', 'young-min-choo')},
            "Saurabh": {"last": (5, 10), "next": (12, 10), "gh": os.getenv('GH_USER_SAURABH', 'Saurabh-IA')},
            "Raman":   {"last": (20, 1), "next": (27, 1), "gh": os.getenv('GH_USER_RAMAN', 'RmnSoni')},
            "Ewan":    {"last": (20, 10), "next": (27, 10), "gh": os.getenv('GH_USER_EWAN', 'Froggyyyyyyy')}
        }

    def generate_thursday_report(self):
        """Automates the Thursday Shift and Sync logic."""
        print("\nREPORT MANAGER: Starting Thursday Standup Report Sync...")
        
        workbook = self.ingestor.client.open_by_key(self.sheet_id)
        wr_tab = workbook.worksheet('Weekly Report')
        twr_tab = workbook.worksheet('Tables for Weekly Report')
        
        all_last_week_tasks = []
        all_next_week_tasks = []

        # 1. Process each PIC
        for name, config in self.pic_map.items():
            print(f"  - Processing {name}...")
            
            # A. Shift current 'Next' to 'Last'
            # We read the 'Next' block (Rows 12-15 or 27-30, 6 columns)
            next_row, next_col = config['next']
            next_block = wr_tab.get_values(f"{gspread_col(next_col)}{next_row}:{gspread_col(next_col+5)}{next_row+3}")
            
            # Mark completion status based on GitHub or existing '〇'
            processed_last_block = []
            for row in next_block:
                if not any(row): continue
                # Update status to 〇 if it was completed (Dummy logic for now, can be refined)
                # For now, we preserve the content
                processed_last_block.append(row)
            
            if not self.dry_run and processed_last_block:
                last_row, last_col = config['last']
                wr_tab.update(f"{gspread_col(last_col)}{last_row}:{gspread_col(last_col+5)}{last_row+len(processed_last_block)-1}", processed_last_block)

            # B. Pull Fresh 'Next' from GitHub
            gh_tasks = self._get_filtered_gh_tasks(config['gh'])
            new_next_block = []
            for i, t in enumerate(gh_tasks[:4]): # Max 4 tasks per PIC for the block
                # Format: [No, Title, Requester, Project, PIC, Deadline]
                deadline = t.get('end_date', 'TBD')
                if deadline != 'TBD':
                    try:
                        dt = datetime.strptime(deadline, "%Y-%m-%d")
                        deadline = dt.strftime("%m/%d(%a)")
                    except: pass
                
                new_next_block.append([
                    str(i+1), 
                    t['title'], 
                    "Choo", # Default requester
                    t['project_tag'], 
                    name, 
                    deadline
                ])
            
            if not self.dry_run:
                # Clear old Next block first
                wr_tab.update(f"{gspread_col(next_col)}{next_row}:{gspread_col(next_col+5)}{next_row+3}", [[""]*6]*4)
                if new_next_block:
                    wr_tab.update(f"{gspread_col(next_col)}{next_row}:{gspread_col(next_col+5)}{next_row+len(new_next_block)-1}", new_next_block)

            # Collect for the final tables
            all_last_week_tasks.extend(processed_last_block)
            all_next_week_tasks.extend(new_next_block)

        # 2. Update 'Tables for Weekly Report' (L16:S31 and L34:S46)
        self._update_final_tables(twr_tab, all_last_week_tasks, all_next_week_tasks)
        print("REPORT MANAGER: Thursday Sync Complete. ✅")

    def _get_filtered_gh_tasks(self, github_user):
        all_tasks = self.gh.get_full_active_tasks()
        return [t for t in all_tasks if t['assignee'] and t['assignee'].lower() == github_user.lower() and 'error' not in t['labels']]

    def _update_final_tables(self, twr_tab, last_tasks, next_tasks):
        if self.dry_run:
            print(f"[DRY RUN] Would update final tables with {len(last_tasks)} completed and {len(next_tasks)} planned tasks.")
            return
            
        # Update Last Weeks Results (L18 onwards)
        last_formatted = [[i+1] + row for i, row in enumerate(last_tasks)]
        twr_tab.update("L18:S31", [[""]*8]*14) # Clear
        if last_formatted:
            twr_tab.update(f"L18:S{18+len(last_formatted)-1}", last_formatted)
            
        # Update Next Weeks Results (L36 onwards)
        next_formatted = [[i+1] + row for i, row in enumerate(next_tasks)]
        twr_tab.update("L36:S46", [[""]*8]*11) # Clear
        if next_formatted:
            twr_tab.update(f"L36:S{36+len(next_formatted)-1}", next_formatted)

def gspread_col(idx):
    """Helper to convert 1-based index to A, B, C..."""
    return chr(64 + idx) if idx <= 26 else "A" + chr(64 + idx - 26)
