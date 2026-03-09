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
            
            # A. Read current 'Next' block to prepare for shifting
            next_row, next_col = config['next']
            # We fetch 4 rows of data for the block
            current_next_block = wr_tab.get_values(f"{gspread_col(next_col)}{next_row}:{gspread_col(next_col+5)}{next_row+3}")
            
            # Clean and prepare shifted block
            # We assume anything in 'Next' that wasn't empty is now 'Last'
            shifted_last_block = []
            existing_planned_titles = []
            for row in current_next_block:
                if not any(row): continue
                shifted_last_block.append(row)
                if len(row) > 1: existing_planned_titles.append(row[1].strip())
            
            if not self.dry_run and shifted_last_block:
                last_row, last_col = config['last']
                # Clear last block first
                wr_tab.update(f"{gspread_col(last_col)}{last_row}:{gspread_col(last_col+5)}{last_row+3}", [[""]*6]*4)
                # Write shifted data
                wr_tab.update(f"{gspread_col(last_col)}{last_row}:{gspread_col(last_col+5)}{last_row+len(shifted_last_block)-1}", shifted_last_block)

            # B. Pull Fresh 'Next' from GitHub (all non-Done tasks)
            gh_tasks = self._get_filtered_gh_tasks(config['gh'])
            new_next_block = []
            for i, t in enumerate(gh_tasks[:4]): 
                deadline = t.get('end_date', 'TBD')
                if deadline != 'TBD':
                    try:
                        dt = datetime.strptime(deadline, "%Y-%m-%d")
                        deadline = dt.strftime("%m/%d(%a)")
                    except: pass
                
                title = t['title']
                # Visual differentiation: If this wasn't in our plan, mark it as 🆕
                if title.strip() not in existing_planned_titles:
                    title = "🆕 " + title

                new_next_block.append([
                    str(i+1), 
                    title, 
                    "Choo", # Default requester
                    t.get('clean_tag', t['project_tag']), 
                    name, 
                    deadline
                ])
            
            if not self.dry_run:
                # Clear and Update Next block
                wr_tab.update(f"{gspread_col(next_col)}{next_row}:{gspread_col(next_col+5)}{next_row+3}", [[""]*6]*4)
                if new_next_block:
                    wr_tab.update(f"{gspread_col(next_col)}{next_row}:{gspread_col(next_col+5)}{next_row+len(new_next_block)-1}", new_next_block)

            all_last_week_tasks.extend(shifted_last_block)
            all_next_week_tasks.extend(new_next_block)

        # 2. Update 'Tables for Weekly Report' (L16:S31 and L34:S46)
        self._update_final_tables(twr_tab, all_last_week_tasks, all_next_week_tasks)
        print("REPORT MANAGER: Thursday Sync Complete. ✅")

    def _get_filtered_gh_tasks(self, github_user):
        """Fetches all tasks for a user that are NOT 'Done' and NOT errors."""
        all_tasks = self.gh.get_full_active_tasks()
        filtered = []
        for t in all_tasks:
            if t['assignee'] and t['assignee'].lower() == github_user.lower():
                # 1. Strict Error Filtering
                is_error = 'error' in [l.lower() for l in t.get('labels', [])] or '[ERROR]' in t['title'].upper()
                if is_error: continue

                # 2. Status Check
                gh_data = self.gh.get_project_item_data(t['number'], 4)
                if gh_data and gh_data.get('Status') != "Done":
                    # 3. Improved Project Tag
                    tag = t['project_tag']
                    if tag == "Overall Project Management":
                        # Attempt to find a better tag from Portfolio Project field
                        tag = gh_data.get('Portfolio Project') or "Maintenance"

                    t['clean_tag'] = tag
                    filtered.append(t)
        return filtered

    def _update_final_tables(self, twr_tab, last_tasks, next_tasks):
        # Remove empty rows from the sources
        clean_last = [r for r in last_tasks if len(r) > 1 and r[1].strip()]
        clean_next = [r for r in next_tasks if len(r) > 1 and r[1].strip()]

        if self.dry_run:
            print(f"\n--- REFINED FINAL TABLES PREVIEW ---")
            print(f"COMPLETED TASKS (Count: {len(clean_last)}):")
            for i, r in enumerate(clean_last): print(f"  {i+1}. {r}")
            print(f"\nPLANNED TASKS (Count: {len(clean_next)}):")
            for i, r in enumerate(clean_next): print(f"  {i+1}. {r}")
            return

        # Update Last Weeks Results (L18 onwards)
        last_formatted = [[i+1] + row[1:] for i, row in enumerate(clean_last)]
        twr_tab.update("L18:S31", [[""]*8]*14) # Clear
        if last_formatted:
            twr_tab.update(f"L18:S{18+len(last_formatted)-1}", last_formatted)

        # Update Next Weeks Results (L36 onwards)
        next_formatted = [[i+1] + row[1:] for i, row in enumerate(clean_next)]
        twr_tab.update("L36:S46", [[""]*8]*11) # Clear
        if next_formatted:
            twr_tab.update(f"L36:S{36+len(next_formatted)-1}", next_formatted)


def gspread_col(idx):
    """Helper to convert 1-based index to A, B, C..."""
    return chr(64 + idx) if idx <= 26 else "A" + chr(64 + idx - 26)
