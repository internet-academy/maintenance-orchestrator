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
        """Automates the Thursday Shift and Sync logic with V3 Formatting."""
        print("\nREPORT MANAGER: Starting Thursday Standup Report Sync (V3)...")
        
        workbook = self.ingestor.client.open_by_key(self.sheet_id)
        # Sandbox tabs
        wr_tab = workbook.worksheet('Weekly Report のコピー')
        twr_tab = workbook.worksheet('Tables for Weekly Report のコピー')
        
        all_last_week_tasks = []
        all_next_week_tasks = []

        for name, config in self.pic_map.items():
            print(f"  - Processing {name}...")
            
            # 1. Analyze what was PLANNED
            next_row, next_col = config['next']
            planned_block = wr_tab.get_values(f"{gspread_col(next_col)}{next_row}:{gspread_col(next_col+7)}{next_row+3}")
            gh_tasks = self._get_v3_gh_tasks(config['gh'])
            
            # 2. Shift to LAST WEEK
            last_week_results = []
            seen_titles = []
            for row in planned_block:
                if not any(row) or len(row) < 2 or not row[1].strip(): continue
                # Match title without the Parent: header if it was nested
                clean_planned_title = row[1].split(']:')[0].replace('[', '').strip()
                seen_titles.append(clean_planned_title)
                
                match = next((t for t in gh_tasks if clean_planned_title in t['title']), None)
                if match:
                    gh_status = self.gh.get_project_item_data(match['number'], 4).get('Status')
                    row[6] = "〇" if gh_status == "Done" else "×"
                else:
                    if row[6] != "〇": row[6] = "×"
                last_week_results.append(row)

            # 3. Add Surprises (Done but not in plan)
            for t in gh_tasks:
                if t['clean_title'] not in seen_titles:
                    gh_status = self.gh.get_project_item_data(t['number'], 4).get('Status')
                    if gh_status == "Done":
                        last_week_results.append([
                            "", "🆕 " + t['full_formatted_title'], "Choo", t['product'], name, t['formatted_deadline'], "〇", ""
                        ])

            # 4. Next Week's Plan (All non-Done with Deadlines)
            next_week_plan = []
            open_tasks = [t for t in gh_tasks if self.gh.get_project_item_data(t['number'], 4).get('Status') != "Done"]
            for i, t in enumerate(open_tasks[:4]):
                next_week_plan.append([
                    str(i+1), t['full_formatted_title'], "Choo", t['product'], name, t['formatted_deadline'], "-", ""
                ])

            if not self.dry_run:
                # Update WR Copy Tab
                self._safe_update_block(wr_tab, config['last'], last_week_results)
                self._safe_update_block(wr_tab, config['next'], next_week_plan)

            all_last_week_tasks.extend(last_week_results)
            all_next_week_tasks.extend(next_week_plan)

        self._update_final_tables(twr_tab, all_last_week_tasks, all_next_week_tasks)
        print("REPORT MANAGER: Thursday Sync Complete. ✅")

    def _get_v3_gh_tasks(self, github_user):
        """Fetches and formats tasks with Parent-Child nesting and Product mapping."""
        all_tasks = self.gh.get_full_active_tasks()
        formatted = []
        for t in all_tasks:
            if t['assignee'] and t['assignee'].lower() == github_user.lower():
                # Filter errors and tasks without deadlines
                if 'error' in [l.lower() for l in t.get('labels', [])] or '[ERROR]' in t['title'].upper(): continue
                if not t.get('end_date'): continue
                
                # 1. Nesting Logic
                subtasks = self.gh.get_subtasks(t['number'])
                full_title = t['title']
                if subtasks:
                    full_title = f"[{t['title']}]:\n" + "\n".join([f" {i+1}. {s['title']}" for i, s in enumerate(subtasks)])
                
                # 2. Product Mapping
                repo_url = t.get('url', '')
                product = "Other"
                if "member" in repo_url or "bohr-individual" in repo_url: product = "Bohr Ind"
                elif "bohr-corporate" in repo_url: product = "Bohr Corp"
                
                # Refine Kikuichimonji
                if "kiku" in t['title'].lower() or "kiku" in t['project_tag'].lower(): product = "Kikuichimonji"

                formatted.append({
                    "number": t['number'],
                    "clean_title": t['title'].strip(),
                    "full_formatted_title": full_title,
                    "product": product,
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
        """Updates a block while clearing old data first."""
        r, c = coord
        tab.update(f"{gspread_col(c)}{r}:{gspread_col(c+7)}{r+3}", [[""]*8]*4)
        if data:
            tab.update(f"{gspread_col(c)}{r}:{gspread_col(c+7)}{r+len(data)-1}", data)

    def _update_final_tables(self, twr_tab, last_tasks, next_tasks):
        clean_last = [r for r in last_tasks if len(r) > 1 and r[1].strip()]
        clean_next = [r for r in next_tasks if len(r) > 1 and r[1].strip()]
        
        if self.dry_run:
            print("\n--- FINAL V3 TABLES PREVIEW ---")
            for i, r in enumerate(clean_last): print(f"L: {r[1][:30]}...")
            return

        twr_tab.update("L18:S31", [[""]*8]*14)
        if clean_last:
            twr_tab.update(f"L18:S{18+len(clean_last)-1}", [[i+1] + r[1:8] for i, r in enumerate(clean_last)])
            
        twr_tab.update("L36:S46", [[""]*8]*11)
        if clean_next:
            twr_tab.update(f"L36:S{36+len(clean_next)-1}", [[i+1] + r[1:8] for i, r in enumerate(clean_next)])

def gspread_col(idx):
    return chr(64 + idx) if idx <= 26 else "A" + chr(64 + idx - 26)
