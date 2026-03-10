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
        """Automates the Standup Sync logic with Dynamic Date Boundaries."""
        print("\nREPORT MANAGER: Starting Standup Report Sync...")
        
        # Friday 9AM JST Logic (Dynamic)
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # Boundary: The most recent Thursday
        days_to_thursday = (today.weekday() - 3) % 7
        last_thursday = today - timedelta(days=days_to_thursday)
        next_thursday = last_thursday + timedelta(days=7)
        
        print(f"  - Boundaries: Last Cycle <= {last_thursday.date()} | Next Cycle <= {next_thursday.date()}")

        workbook = self.ingestor.client.open_by_key(self.sheet_id)
        # LIVE TABS
        wr_tab = workbook.worksheet('Weekly Report')
        twr_tab = workbook.worksheet('Tables for Weekly Report')
        
        all_last_week_tasks = []
        all_next_week_tasks = []

        for name, config in self.pic_map.items():
            print(f"  - Processing {name}...")
            gh_tasks = self._get_v5_gh_tasks(config['gh'])
            
            # 1. Analyze PLANNED (current 'Next' block)
            next_row, next_col = config['next']
            planned_block = wr_tab.get_values(f"{gspread_col(next_col)}{next_row}:{gspread_col(next_col+7)}{next_row+3}")
            
            last_week_results = []
            seen_titles = []
            
            # A. Process PLANNED (Shift to 'Last')
            for row in planned_block:
                if not any(row) or len(row) < 2 or not row[1].strip(): continue
                clean_planned_title = row[1].split(':\n')[0].strip()
                seen_titles.append(clean_planned_title)
                
                match = next((t for t in gh_tasks if clean_planned_title in t['title']), None)
                if match:
                    gh_item_data = self.gh.get_project_item_data(match['number'], 4)
                    gh_status = gh_item_data.get('Status') if gh_item_data else "Open"
                    row[6] = "〇" if gh_status == "Done" else "×"
                else:
                    if row[6] != "〇": row[6] = "×"
                last_week_results.append(row)

            # B. Add Surprise Completions (🆕 tag)
            for t in gh_tasks:
                if t['clean_title'] not in seen_titles:
                    deadline_dt = datetime.strptime(t['raw_deadline'], "%Y-%m-%d")
                    if deadline_dt <= last_thursday:
                        gh_item_data = self.gh.get_project_item_data(t['number'], 4)
                        gh_status = gh_item_data.get('Status') if gh_item_data else "Open"
                        if gh_status == "Done":
                            last_week_results.append(["", "🆕 " + t['full_formatted_title'], t['requester'], t['product'], name, t['formatted_deadline'], "〇", ""])

            # C. Next Week's Plan
            raw_next_tasks = []
            # 1. Rollover from '×'
            for row in last_week_results:
                if row[6] == "×":
                    raw_next_tasks.append({"title": row[1], "req": row[2], "prod": row[3], "dl_dt": datetime.strptime(row[5].split('(')[0], "%m/%d").replace(year=today.year), "dl_str": row[5], "type": "rollover"})
            
            # 2. Planned Open Tasks (Deadline up to next Thursday)
            for t in gh_tasks:
                deadline_dt = datetime.strptime(t['raw_deadline'], "%Y-%m-%d")
                gh_item_data = self.gh.get_project_item_data(t['number'], 4)
                gh_status = gh_item_data.get('Status') if gh_item_data else "Open"
                if gh_status != "Done" and last_thursday < deadline_dt <= next_thursday:
                    if not any(t['clean_title'] in r['title'] for r in raw_next_tasks):
                        raw_next_tasks.append({"title": t['full_formatted_title'], "req": t['requester'], "prod": t['product'], "dl_dt": deadline_dt, "dl_str": t['formatted_deadline'], "type": "new"})

            # GROUPING: Only group if we have more than 4 tasks total for the block
            if len(raw_next_tasks) > 4:
                next_week_plan = self._group_tasks(raw_next_tasks, name)
            else:
                next_week_plan = [["", t['title'], t['req'], t['prod'], name, t['dl_str'], "-", ""] for t in raw_next_tasks]

            if not self.dry_run:
                self._safe_update_block(wr_tab, config['last'], last_week_results)
                self._safe_update_block(wr_tab, config['next'], next_week_plan)

            all_last_week_tasks.extend(last_week_results)
            all_next_week_tasks.extend(next_week_plan)

        self._update_final_tables(twr_tab, all_last_week_tasks, all_next_week_tasks)
        print("REPORT MANAGER: Thursday Sync Complete. ✅")

    def _group_tasks(self, task_list, pic_name):
        """Groups related tasks into a single row."""
        grouped = {}
        for t in task_list:
            prefix = t['title'].split(':')[0].strip()
            key = f"{t['prod']}|{prefix}"
            if key not in grouped: grouped[key] = []
            grouped[key].append(t)
            
        final_rows = []
        for key, members in grouped.items():
            prod, prefix = key.split('|')
            if len(members) > 1:
                sub_items = []
                for m in members:
                    parts = m['title'].split(':')
                    name = parts[1].strip() if len(parts) > 1 else m['title']
                    sub_items.append(name.replace('\n', ' ').strip())
                title = f"{prefix}:\n" + "\n".join([f" {i+1}. {item}" for i, item in enumerate(sub_items)])
                latest_dl = max(members, key=lambda x: x['dl_dt'])
                final_rows.append(["", title, members[0]['req'], prod, pic_name, latest_dl['dl_str'], "-", ""])
            else:
                m = members[0]
                final_rows.append(["", m['title'], m['req'], m['prod'], pic_name, m['dl_str'], "-", ""])
        return final_rows

    def _get_v5_gh_tasks(self, github_user):
        """Fetches and formats parent tasks with dynamic requester and nesting."""
        all_tasks = self.gh.get_full_active_tasks()
        formatted = []
        for t in all_tasks:
            if t['assignee'] and t['assignee'].lower() == github_user.lower():
                if 'error' in [l.lower() for l in t.get('labels', [])] or '[ERROR]' in t['title'].upper(): continue
                if not t.get('end_date'): continue
                
                subtasks = self.gh.get_subtasks(t['number'])
                full_title = t['title']
                if subtasks:
                    full_title = f"{t['title']}:\n" + "\n".join([f" {i+1}. {s['title']}" for i, s in enumerate(subtasks)])
                
                repo_url = t.get('url', '').lower()
                product = "Other"
                gh_item_data = self.gh.get_project_item_data(t['number'], 4)
                requester = gh_item_data.get('Requester') if gh_item_data else None
                
                if "member" in repo_url or "bohr-individual" in repo_url: 
                    product = "Bohr Ind"
                    if not requester: requester = "Sakamoto"
                elif "bohr-corporate" in repo_url: product = "Bohr Corp"
                if "kiku" in t['title'].lower() or "kiku" in t['project_tag'].lower(): product = "Kikuichimonji"
                if not requester: requester = "Choo"

                formatted.append({
                    "number": t['number'], "clean_title": t['title'].strip(), "full_formatted_title": full_title,
                    "product": product, "requester": requester, "raw_deadline": t['end_date'],
                    "formatted_deadline": self._format_deadline(t.get('end_date')), "title": t['title']
                })
        return sorted(formatted, key=lambda x: x['raw_deadline'])

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
