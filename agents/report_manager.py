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
        
        self.pic_map = {
            "Choo":    {"last": (5, 1),  "next": (12, 1),  "gh": os.getenv('GH_USER_CHOO', 'young-min-choo')},
            "Saurabh": {"last": (5, 10), "next": (12, 10), "gh": os.getenv('GH_USER_SAURABH', 'Saurabh-IA')},
            "Raman":   {"last": (20, 1), "next": (27, 1), "gh": os.getenv('GH_USER_RAMAN', 'RmnSoni')},
            "Ewan":    {"last": (20, 10), "next": (27, 10), "gh": os.getenv('GH_USER_EWAN', 'Froggyyyyyyy')}
        }

    def generate_thursday_report(self):
        """Automates the Standup Sync logic with Simulated Date Boundaries."""
        print("\nREPORT MANAGER: Starting Standup Report Sync (SIMULATED FOR 03/06 FRI)...")
        
        # SIMULATED BOUNDARIES for Test:
        # Run Date: 2026-03-06 (Fri)
        # Last Week Boundary: <= 2026-03-05 (Thu)
        # Next Week Boundary: > 2026-03-05 (Thu) AND <= 2026-03-12 (Thu)
        
        sim_last_thursday = datetime(2026, 3, 5).replace(hour=0, minute=0, second=0, microsecond=0)
        sim_next_thursday = datetime(2026, 3, 12).replace(hour=0, minute=0, second=0, microsecond=0)
        
        print(f"  - Simulated Logic: Last Cycle ended {sim_last_thursday.date()} | Next Cycle ends {sim_next_thursday.date()}")

        workbook = self.ingestor.client.open_by_key(self.sheet_id)
        # Sandbox tabs
        wr_tab = workbook.worksheet('Weekly Report のコピー')
        twr_tab = workbook.worksheet('Tables for Weekly Report のコピー')
        
        all_last_week_tasks = []
        all_next_week_tasks = []

        for name, config in self.pic_map.items():
            print(f"  - Processing {name}...")
            
            # 1. Fetch ALL parent tasks from GitHub for this user
            gh_tasks = self._get_v5_gh_tasks(config['gh'])
            
            # 2. Analyze PLANNED (current 'Next' block)
            next_row, next_col = config['next']
            planned_block = wr_tab.get_values(f"{gspread_col(next_col)}{next_row}:{gspread_col(next_col+7)}{next_row+3}")
            
            last_week_results = []
            seen_titles = []
            
            # A. Process PLANNED (Shift from 'Next' to 'Last')
            for row in planned_block:
                if not any(row) or len(row) < 2 or not row[1].strip(): continue
                clean_planned_title = row[1].split(':\n')[0].strip()
                seen_titles.append(clean_planned_title)
                
                # Check GitHub state
                match = next((t for t in gh_tasks if clean_planned_title in t['title']), None)
                if match:
                    gh_item_data = self.gh.get_project_item_data(match['number'], 4)
                    gh_status = gh_item_data.get('Status') if gh_item_data else "Open"
                    row[6] = "〇" if gh_status == "Done" else "×"
                else:
                    if row[6] != "〇": row[6] = "×"
                last_week_results.append(row)

            # B. Add Surprise Completions (🆕 tag)
            # Logic: Due by sim_last_thursday but not in seen_titles
            for t in gh_tasks:
                if t['clean_title'] not in seen_titles:
                    deadline_dt = datetime.strptime(t['raw_deadline'], "%Y-%m-%d")
                    if deadline_dt <= sim_last_thursday:
                        gh_item_data = self.gh.get_project_item_data(t['number'], 4)
                        gh_status = gh_item_data.get('Status') if gh_item_data else "Open"
                        if gh_status == "Done":
                            last_week_results.append([
                                "", "🆕 " + t['full_formatted_title'], t['requester'], t['product'], name, t['formatted_deadline'], "〇", ""
                            ])

            # C. Next Week's Plan
            next_week_plan = []
            # 1. Rollover
            for row in last_week_results:
                if row[6] == "×":
                    next_week_plan.append(["", row[1], row[2], row[3], name, row[5], "-", "Rollover"])
            
            # 2. Planned Open Tasks
            for t in gh_tasks:
                deadline_dt = datetime.strptime(t['raw_deadline'], "%Y-%m-%d")
                gh_item_data = self.gh.get_project_item_data(t['number'], 4)
                gh_status = gh_item_data.get('Status') if gh_item_data else "Open"
                
                if gh_status != "Done" and sim_last_thursday < deadline_dt <= sim_next_thursday:
                    if not any(t['clean_title'] in row[1] for row in next_week_plan):
                        next_week_plan.append(["", t['full_formatted_title'], t['requester'], t['product'], name, t['formatted_deadline'], "-", ""])

            if not self.dry_run:
                self._safe_update_block(wr_tab, config['last'], last_week_results)
                self._safe_update_block(wr_tab, config['next'], next_week_plan)

            all_last_week_tasks.extend(last_week_results)
            all_next_week_tasks.extend(next_week_plan)

        self._update_final_tables(twr_tab, all_last_week_tasks, all_next_week_tasks)
        print("REPORT MANAGER: Sync Complete. ✅")

    def _get_v5_gh_tasks(self, github_user):
        """Fetches and formats parent tasks with dynamic requester and nesting."""
        all_tasks = self.gh.get_full_active_tasks()
        formatted = []
        for t in all_tasks:
            if t['assignee'] and t['assignee'].lower() == github_user.lower():
                if 'error' in [l.lower() for l in t.get('labels', [])] or '[ERROR]' in t['title'].upper(): continue
                if not t.get('end_date'): continue
                
                # Nesting
                subtasks = self.gh.get_subtasks(t['number'])
                full_title = t['title']
                if subtasks:
                    full_title = f"{t['title']}:\n" + "\n".join([f" {i+1}. {s['title']}" for i, s in enumerate(subtasks)])
                
                # Product & Dynamic Requester
                repo_url = t.get('url', '').lower()
                product = "Other"
                gh_item_data = self.gh.get_project_item_data(t['number'], 4)
                requester = gh_item_data.get('Requester') if gh_item_data else None
                
                if "member" in repo_url or "bohr-individual" in repo_url: 
                    product = "Bohr Ind"
                    if not requester: requester = "Sakamoto"
                elif "bohr-corporate" in repo_url: 
                    product = "Bohr Corp"
                if "kiku" in t['title'].lower() or "kiku" in t['project_tag'].lower(): 
                    product = "Kikuichimonji"
                
                if not requester: requester = "Choo"

                formatted.append({
                    "number": t['number'],
                    "clean_title": t['title'].strip(),
                    "full_formatted_title": full_title,
                    "product": product,
                    "requester": requester,
                    "raw_deadline": t['end_date'],
                    "formatted_deadline": self._format_deadline(t.get('end_date')),
                    "title": t['title']
                })
        return formatted

    def _format_deadline(self, date_str):
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%m/%d(%a)")
        except: return date_str

    def _safe_update_block(self, tab, coord, data):
        r, c = coord
        tab.update(f"{gspread_col(c)}{r}:{gspread_col(c+7)}{r+3}", [[""]*8]*4)
        if data:
            for i, row in enumerate(data[:4]): row[0] = str(i+1)
            tab.update(f"{gspread_col(c)}{r}:{gspread_col(c+7)}{r+len(data[:4])-1}", data[:4])

    def _update_final_tables(self, twr_tab, last_tasks, next_tasks):
        clean_last = [r for r in last_tasks if len(r) > 1 and r[1].strip()]
        clean_next = [r for r in next_tasks if len(r) > 1 and r[1].strip()]
        
        twr_tab.update("L18:S31", [[""]*8]*14)
        if clean_last:
            twr_tab.update(f"L18:S{18+len(clean_last)-1}", [[i+1] + r[1:8] for i, r in enumerate(clean_last[:14])])
            
        twr_tab.update("L36:S46", [[""]*8]*11)
        if clean_next:
            twr_tab.update(f"L36:S{36+len(clean_next)-1}", [[i+1] + r[1:8] for i, r in enumerate(clean_next[:11])])

def gspread_col(idx):
    return chr(64 + idx) if idx <= 26 else "A" + chr(64 + idx - 26)
