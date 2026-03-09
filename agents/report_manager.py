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
        print("\nREPORT MANAGER: Starting Thursday Standup Report Sync (SANDBOX TEST)...")
        
        workbook = self.ingestor.client.open_by_key(self.sheet_id)
        # Use Copy tabs for testing
        wr_tab = workbook.worksheet('Weekly Report のコピー')
        twr_tab = workbook.worksheet('Tables for Weekly Report のコピー')
        
        all_last_week_tasks = []
        all_next_week_tasks = []

        # 1. Process each PIC
        for name, config in self.pic_map.items():
            print(f"  - Processing {name}...")
            
            # A. Analyze Plan vs Reality
            next_row, next_col = config['next']
            # Fetch 8 columns (No, Title, Req, Proj, PIC, DL, Result, Remarks)
            planned_block = wr_tab.get_values(f"{gspread_col(next_col)}{next_row}:{gspread_col(next_col+7)}{next_row+3}")
            
            gh_tasks = self._get_all_parent_tasks(config['gh'])
            
            # --- LAST WEEK'S RESULTS LOGIC ---
            last_week_results = []
            seen_titles = []
            
            # 1. Process what was PLANNED
            for row in planned_block:
                if not any(row) or len(row) < 2 or not row[1].strip(): continue
                title = row[1].strip()
                seen_titles.append(title)
                
                # Check GitHub state for this specific title
                match = next((t for t in gh_tasks if t['title'].strip() == title), None)
                if match:
                    # If found on GitHub, check if it's 'Done'
                    gh_item_data = self.gh.get_project_item_data(match['number'], 4)
                    gh_status = gh_item_data.get('Status') if gh_item_data else "Open"
                    row[6] = "〇" if gh_status == "Done" else "×"
                else:
                    # If not found on GitHub (deleted/manual), assume manual check or '×'
                    if row[6] != "〇": row[6] = "×"
                
                last_week_results.append(row)

            # 2. Add "Surprises" (Done but NOT in plan)
            for t in gh_tasks:
                if t['title'].strip() not in seen_titles:
                    gh_item_data = self.gh.get_project_item_data(t['number'], 4)
                    gh_status = gh_item_data.get('Status') if gh_item_data else "Open"
                    if gh_status == "Done":
                        deadline = self._format_deadline(t.get('end_date'))
                        last_week_results.append([
                            "", # No
                            "🆕 " + t['title'], 
                            "Choo", 
                            t.get('clean_tag', "Maintenance"), 
                            name, 
                            deadline, 
                            "〇", # Result
                            "" # Remarks
                        ])

            # --- NEXT WEEK'S PLAN LOGIC ---
            next_week_plan = []
            open_tasks = []
            for t in gh_tasks:
                gh_item_data = self.gh.get_project_item_data(t['number'], 4)
                gh_status = gh_item_data.get('Status') if gh_item_data else "Open"
                if gh_status != "Done":
                    open_tasks.append(t)
            
            for i, t in enumerate(open_tasks[:4]):
                deadline = self._format_deadline(t.get('end_date'))
                next_week_plan.append([
                    str(i+1), 
                    t['title'], 
                    "Choo", 
                    t.get('clean_tag', "Maintenance"), 
                    name, 
                    deadline, 
                    "-", # Result for future
                    "" # Remarks
                ])

            # B. Update Weekly Report Tab
            if not self.dry_run:
                # Update Last Week Block
                last_row, last_col = config['last']
                wr_tab.update(f"{gspread_col(last_col)}{last_row}:{gspread_col(last_col+7)}{last_row+3}", [[""]*8]*4) # Clear
                if last_week_results:
                    wr_tab.update(f"{gspread_col(last_col)}{last_row}:{gspread_col(last_col+7)}{last_row+len(last_week_results)-1}", last_week_results)
                
                # Update Next Week Block
                wr_tab.update(f"{gspread_col(next_col)}{next_row}:{gspread_col(next_col+7)}{next_row+3}", [[""]*8]*4) # Clear
                if next_week_plan:
                    wr_tab.update(f"{gspread_col(next_col)}{next_row}:{gspread_col(next_col+7)}{next_row+len(next_week_plan)-1}", next_week_plan)

            all_last_week_tasks.extend(last_week_results)
            all_next_week_tasks.extend(next_week_plan)

        # 2. Update Final Tables
        self._update_final_tables(twr_tab, all_last_week_tasks, all_next_week_tasks)
        print("REPORT MANAGER: Thursday Sync Complete. ✅")

    def _get_all_parent_tasks(self, github_user):
        """Fetches all parent tasks for a user, adding clean tags."""
        all_tasks = self.gh.get_full_active_tasks()
        filtered = []
        for t in all_tasks:
            if t['assignee'] and t['assignee'].lower() == github_user.lower():
                is_error = 'error' in [l.lower() for l in t.get('labels', [])] or '[ERROR]' in t['title'].upper()
                if is_error: continue
                
                gh_data = self.gh.get_project_item_data(t['number'], 4)
                tag = t['project_tag']
                if tag == "Overall Project Management" and gh_data:
                    tag = gh_data.get('Portfolio Project') or "Maintenance"
                t['clean_tag'] = tag
                filtered.append(t)
        return filtered

    def _format_deadline(self, date_str):
        if not date_str or date_str == 'TBD': return 'TBD'
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%m/%d(%a)")
        except: return date_str

    def _update_final_tables(self, twr_tab, last_tasks, next_tasks):
        # Flatten and index for the master tables
        # Row format: [No, Title, Requester, Project, PIC, Deadline, Result, Remarks]
        clean_last = [r for r in last_tasks if len(r) > 1 and r[1].strip()]
        clean_next = [r for r in next_tasks if len(r) > 1 and r[1].strip()]

        if self.dry_run:
            print(f"\n--- REFINED FINAL TABLES PREVIEW ---")
            print(f"LAST WEEK RESULTS (Count: {len(clean_last)}):")
            for i, r in enumerate(clean_last): print(f"  {i+1}. {r}")
            print(f"\nNEXT WEEK PLAN (Count: {len(clean_next)}):")
            for i, r in enumerate(clean_next): print(f"  {i+1}. {r}")
            return
            
        # Update L18:S31 (Col 12-19)
        last_formatted = [[i+1] + row[1:8] for i, row in enumerate(clean_last)]
        twr_tab.update("L18:S31", [[""]*8]*14)
        if last_formatted:
            twr_tab.update(f"L18:S{18+len(last_formatted)-1}", last_formatted)
            
        # Update L36:S46 (Col 12-19)
        next_formatted = [[i+1] + row[1:8] for i, row in enumerate(clean_next)]
        twr_tab.update("L36:S46", [[""]*8]*11)
        if next_formatted:
            twr_tab.update(f"L36:S{36+len(next_formatted)-1}", next_formatted)

def gspread_col(idx):
    return chr(64 + idx) if idx <= 26 else "A" + chr(64 + idx - 26)
