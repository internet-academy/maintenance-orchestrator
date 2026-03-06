import os
import json
import hashlib
import re
import time
from google import genai
from dotenv import load_dotenv
from agents.cloud_ingestor import CloudIngestor
from agents.github_specialist import GitHubSpecialist
from agents.load_balancer import DeveloperTimeline
from agents.git_sync import GitSync
from datetime import datetime, timedelta

# Load environment variables from .env
load_dotenv()

class Orchestrator:
    def __init__(self, dry_run=None):
        if dry_run is None:
            env_val = os.getenv('DRY_RUN', 'False').lower()
            self.dry_run = env_val in ['true', '1', 't', 'y', 'yes']
        else:
            self.dry_run = dry_run
            
        if self.dry_run:
            print("!!! RUNNING IN DRY RUN MODE - NO API MUTATIONS WILL OCCUR !!!")
        
        self.google_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        if self.google_json and os.path.exists(self.google_json):
            with open(self.google_json, 'r') as f:
                self.google_json = f.read()
                
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.github_token = os.getenv('GITHUB_TOKEN')
        
        self.state_file = "sync_state.json"
        self.state = self._load_state()

        if self.gemini_key:
            self.client = genai.Client(api_key=self.gemini_key)
            self.model_name = 'gemini-flash-latest'
        else:
            self.client = None

        self.ingestor = CloudIngestor(self.google_json, self.sheet_id)
        self.gh_specialist = GitHubSpecialist(self.github_token, dry_run=self.dry_run)
        
        if self.github_token:
            self.git_sync = GitSync(self.github_token, self.ingestor, dry_run=self.dry_run)
        else:
            self.git_sync = None
        
        self.chat_webhook = os.getenv('GOOGLE_CHAT_REPORT_WEBHOOK')
        self.developer_map = {
            "Saurabh": os.getenv('GH_USER_SAURABH', 'Saurabh-IA'),
            "Raman": os.getenv('GH_USER_RAMAN', 'RmnSoni'),
            "Ewan": os.getenv('GH_USER_EWAN', 'Froggyyyyyyy'),
            "Choo": os.getenv('GH_USER_CHOO', 'young-min-choo')
        }
        
        self.chat_ids = {
            "Saurabh": os.getenv('CHAT_ID_SAURABH', 'Saurabh'),
            "Raman": os.getenv('CHAT_ID_RAMAN', 'Raman'),
            "Ewan": os.getenv('CHAT_ID_EWAN', 'Ewan'),
            "Choo": os.getenv('CHAT_ID_CHOO', 'Choo')
        }
        
        self.name_mapping = {
            "鈴木佳子": "Suzuki", "稲葉由衣": "Inaba", "谷川大虎": "Tanikawa",
            "中村駿吾": "Nakamura", "石井陽介": "Ishii", "榎本智香": "Enomoto", "眞尾由紀子": "Mao"
        }
        
        self.start_date = os.getenv('SYNC_START_DATE') 
        self.timelines = {}
        
        print("ORCHESTRATOR: Initializing global capacity map...")
        self.all_active_tasks = self.gh_specialist.get_full_active_tasks()
        
        for name, github_user in self.developer_map.items():
            timeline = DeveloperTimeline(name, start_date=self.start_date)
            user_load = sum(t.get('hours', 0.0) for t in self.all_active_tasks if t['assignee'] and t['assignee'].lower() == github_user.lower())
            timeline.fill_hours(user_load)
            self.timelines[github_user] = timeline

        self.detailed_audit_shown = set()

    def _load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f: return json.load(f)
            except: return {}
        return {}

    def _save_state(self):
        with open(self.state_file, 'w') as f: json.dump(self.state, f, indent=2)

    def _get_task_hash(self, task):
        content = f"{task['content']}|{task.get('estimated_hours', 0)}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _detect_priority(self, content):
        content_lower = content.lower()
        is_not_urgent = "not urgent" in content_lower or "至急ではない" in content_lower
        is_urgent = "urgent" in content_lower or "至急" in content_lower
        if is_not_urgent: return "P2"
        if is_urgent: return "P0"
        return "P1"

    def run(self):
        print(f"--- Starting Orchestration: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        self.stats = { "new_tasks": 0, "reassigned": 0, "status_syncs": 0, "healed_links": 0, "date_syncs": 0 }
        
        display_date = self.start_date if self.start_date else "Today"
        print(f"\n--- Team Capacity Map (Starting {display_date}) ---")
        for name, github_user in self.developer_map.items():
            timeline = self.timelines[github_user]
            bars = "".join(["█" if b['used']/6.0 >= 1.0 else "▓" if b['used']/6.0 > 0.5 else "░" if b['used']/6.0 > 0 else "." for b in timeline.buckets])
            print(f"{name.ljust(8)} [{bars}] first day usage: {timeline.get_today_usage()}h")
        print("--------------------------------------------\n")

        try:
            # 1. Sync GitHub status BACK to Sheet
            tasks = self.ingestor.get_live_tasks()
            if self.git_sync:
                sync_stats = self.git_sync.scan_and_sync(tasks)
                if sync_stats:
                    self.stats["status_syncs"] += sync_stats.get("status_changes", 0)
                    self.stats["healed_links"] += sync_stats.get("healed_links", 0)
                    self.stats["date_syncs"] += sync_stats.get("date_migrations", 0)

            # 2. Process NEW Maintenance Tasks
            for task in tasks:
                self.process_task(task)
                time.sleep(1 if self.dry_run else 2)
            
            # 3. Process NEW Development Requests (Numeric Sheets) - Gated by Feature Toggle
            enable_dev_scan = os.getenv('ENABLE_NEW_DEV_SCAN', 'False').lower() in ['true', '1', 't', 'y', 'yes']
            if enable_dev_scan:
                self.process_dev_requests()
            else:
                print("\nSKIP: New Development scanning is currently DISABLED (ENABLE_NEW_DEV_SCAN=False)")

            if any(v > 0 for v in self.stats.values()):
                self._send_sync_report()

            target_hour = int(os.getenv('REPORT_HOUR', '0')) 
            today_date = datetime.now().strftime("%Y-%m-%d")
            if datetime.now().hour == target_hour and self.state.get('last_report_date') != today_date:
                self._send_daily_report([])
                self.state['last_report_date'] = today_date
            
            self._save_state()
        except Exception as e:
            import traceback
            print(f"CRITICAL ERROR: {str(e)}")
            traceback.print_exc()

    def process_task(self, task):
        task_id = task.get('backlog_id')
        current_hash = self._get_task_hash(task)
        
        if task_id and (task_id.startswith("http") or "#" in task_id):
            try:
                match = re.search(r'/issues/(\d+)', task_id)
                if match:
                    issue_num = int(match.group(1))
                    gh_data = self.gh_specialist.get_project_item_data(issue_num, 4)
                    if gh_data and gh_data.get('Status') == "To Triage":
                        if self.gh_specialist.get_child_issues_status(gh_data.get('Title')):
                            print(f"AUTO-READY: All sub-issues closed for #{issue_num}. Moving to 'Backlog'.")
                            if not self.dry_run:
                                self.gh_specialist.update_field(4, gh_data['item_id'], 'status', "f75ad846", is_option=True)
            except Exception as e: print(f"DEBUG: Ready trigger failed: {e}")
            if self.state.get(task_id) == current_hash: return
            self.state[task_id] = current_hash
            return

        if task.get('pic'): return

        full_desc, ai_summary, romaji_name = self._generate_bilingual_description(task)
        best_dev = self._find_best_dev(task['estimated_hours'])
        
        if best_dev:
            start_date, end_date = self.timelines[best_dev['id']].fill_hours_with_dates(task['estimated_hours'])
            priority = self._detect_priority(task['content'])
            summary = f"[MAINTENANCE] {ai_summary} ({romaji_name} - #{task['id']})"
            target_repo = "member"
            if "bohr" in task['content'].lower(): target_repo = "bohr-individual"
            
            if self.dry_run:
                print(f"[DRY RUN] Would create Parent/Sub issues for Task {task['id']} ({start_date})")
                return

            try:
                # Phase 1: Parent
                issue = self.gh_specialist.create_issue(repo=target_repo, title=summary, body=full_desc, assignee=best_dev['id'], labels=["staff-report"])
                issue_url = issue['html_url']
                p_node = issue['node_id']
                item_p4 = self.gh_specialist.add_to_project(p_node, 4)
                self.gh_specialist.update_field(4, item_p4, 'status', self.gh_specialist.projects[4]['options']['status_to_triage'], is_option=True)
                self.gh_specialist.update_field(4, item_p4, 'start_date', start_date)
                self.gh_specialist.update_field(4, item_p4, 'end_date', end_date)
                self.gh_specialist.update_field(4, item_p4, 'priority', self.gh_specialist.projects[4]['options'][f'priority_{priority.lower()}'], is_option=True)
                self.gh_specialist.update_field(4, item_p4, 'level', self.gh_specialist.projects[4]['options']['level_parent'], is_option=True)
                self.gh_specialist.update_field(4, item_p4, 'hours', task['estimated_hours'])
                
                # Project 3
                item_p3 = self.gh_specialist.add_to_project(p_node, 3)
                self.gh_specialist.update_field(3, item_p3, 'project', self.gh_specialist.projects[3]['options']['project_maintenance'], is_option=True)
                self.gh_specialist.update_field(3, item_p3, 'start_date', start_date)
                self.gh_specialist.update_field(3, item_p3, 'end_date', end_date)

                # Phase 2: Sub-issue
                sub_title = f"Understand the request: {ai_summary} (Sub-issue for #{issue['number']})"
                sub_issue = self.gh_specialist.create_issue(repo=target_repo, title=sub_title, body="Initial review task.", assignee=best_dev['id'])
                self.gh_specialist.link_subissue(p_node, sub_issue['node_id'])
                sub_item = self.gh_specialist.add_to_project(sub_issue['node_id'], 4)
                self.gh_specialist.update_field(4, sub_item, 'level', self.gh_specialist.projects[4]['options']['level_child'], is_option=True)
                self.gh_specialist.update_field(4, sub_item, 'hours', 0.33)
                self.gh_specialist.update_field(4, sub_item, 'start_date', start_date)
                self.gh_specialist.update_field(4, sub_item, 'end_date', start_date)

                self.ingestor.write_backlog_id(task['anchors'], issue_url)
                self.ingestor.write_status(task['anchors'], "Open")
                self.stats["new_tasks"] += 1
                self.state[issue_url] = current_hash
                print(f"SUCCESS: Created {issue_url}")
            except Exception as e: print(f"ERROR: Failed to process task {task['id']}: {e}")
        else: print(f"OVERLOAD: No capacity for Task {task['id']}.")

    def process_dev_requests(self):
        """Scans numeric sheets and creates [NEW DEV] issues for approved requests."""
        print("\n--- Scanning for New Development Requests (Numeric Sheets) ---")
        try:
            dev_tasks = self.ingestor.get_dev_requests()
            print(f"Found {len(dev_tasks)} approved dev requests needing tickets.")
            
            for task in dev_tasks:
                current_hash = hashlib.sha256(task['content'].encode()).hexdigest()
                state_key = f"DEV_{task['id']}"
                if self.state.get(state_key) == current_hash: continue
                    
                full_desc, ai_summary, romaji_name = self._generate_bilingual_description(task)
                dev_title = task['title'] if len(task['title']) > 5 else ai_summary
                summary = f"[NEW DEV] {dev_title} ({romaji_name} - #{task['id']})"
                
                if self.dry_run:
                    print(f"\n[DRY RUN] NEW DEVELOPMENT PLAN for Sheet {task['id']}:")
                    print(f"  - Parent Issue:  {summary}")
                    print(f"  - Sub-Issue:     Understand the request: {ai_summary}")
                    print(f"  - Description Preview:\n{full_desc.split('## 📄 Source Content')[0]}\n")
                    continue
                    
                try:
                    # Phase 1: Parent
                    issue = self.gh_specialist.create_issue(repo="member", title=summary, body=full_desc, assignee=None, labels=["staff-report", "new-development"])
                    issue_url = issue['html_url']
                    p_node = issue['node_id']
                    item_p4 = self.gh_specialist.add_to_project(p_node, 4)
                    item_p3 = self.gh_specialist.add_to_project(p_node, 3)
                    
                    self.gh_specialist.update_field(3, item_p3, 'project', self.gh_specialist.projects[3]['options']['project_new_dev'], is_option=True)
                    self.gh_specialist.update_field(4, item_p4, 'level', self.gh_specialist.projects[4]['options']['level_parent'], is_option=True)
                    self.gh_specialist.update_field(4, item_p4, 'status', self.gh_specialist.projects[4]['options']['status_to_triage'], is_option=True)

                    # Phase 2: Sub-issue
                    sub_title = f"Understand the request: {ai_summary} (Sub-issue for #{issue['number']})"
                    sub_issue = self.gh_specialist.create_issue(repo="member", title=sub_title, body="Initial review task for new development.", assignee=None)
                    self.gh_specialist.link_subissue(p_node, sub_issue['node_id'])
                    sub_item = self.gh_specialist.add_to_project(sub_issue['node_id'], 4)
                    self.gh_specialist.update_field(4, sub_item, 'level', self.gh_specialist.projects[4]['options']['level_child'], is_option=True)
                    self.gh_specialist.update_field(4, sub_item, 'hours', 0.33)
                    
                    # Write-back
                    self.ingestor.write_dev_ticket(task['sheet_name'], issue_url)
                    self.state[state_key] = current_hash
                    self.stats["new_tasks"] += 1
                    print(f"SUCCESS: Created {issue_url}")
                    time.sleep(2)
                except Exception as e: print(f"ERROR: Failed to process dev request {task['id']}: {e}")
        except Exception as e: print(f"ERROR: Dev request scan failed: {e}")

    def _find_best_dev(self, hours):
        team_options = []
        choo_option = None
        for github_user, timeline in self.timelines.items():
            finish_date = timeline.peek_fill(hours)
            if finish_date:
                name = [k for k, v in self.developer_map.items() if v == github_user][0]
                option = {"name": name, "id": github_user, "finish_date": finish_date}
                if name == "Choo": choo_option = option
                else: team_options.append(option)
        if team_options: return sorted(team_options, key=lambda x: x['finish_date'])[0]
        return choo_option

    def _generate_bilingual_description(self, task):
        GID = "635134579"
        title_summary, en_translation = self._translate_and_summarize(task['content'], fallback_translation=task.get('english_translation_fallback', ''))
        romaji_name = self.name_mapping.get(task['requester'], task['requester'])
        row = task.get('row_index', 0) + 1
        sheet_link = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/edit?gid={GID}#gid={GID}&range=B{row}:C{row}"
        if task.get('sheet_name'):
             sheet_link = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/edit#gid=0"
        
        description = f"ID: {task['id']}\nSheet Link: {sheet_link}\n\n"
        is_fallback = en_translation.strip() == task['content'].strip()
        if is_fallback:
            sheet_translation = task.get('english_translation_fallback', '').strip()
            is_url_only = sheet_translation.startswith("http") and "\n" not in sheet_translation
            if sheet_translation and not is_url_only:
                description += f"## 📝 Description (Sheet Translation)\n\n{sheet_translation}\n\n## 📄 Source Content (Original)\n\n{task['content']}"
            else:
                is_likely_jp = any(ord(c) > 128 for c in task['content'][:100])
                header = "## 📄 Source Content (Japanese)" if is_likely_jp else "## 📝 Source Content (English)"
                description += f"{header}\n\n{task['content']}"
                if sheet_translation: description += f"\n\n## 🔗 Reference Link\n\n{sheet_translation}"
                if is_likely_jp: description += "\n\n> ⚠️ *Note: Automatic translation unavailable due to API limit.*"
        else:
            description += f"## 📝 Description (English)\n\n{en_translation}\n\n## 📄 Source Content (Original)\n\n{task['content']}"
        return description, title_summary, romaji_name

    def _translate_and_summarize(self, text, fallback_translation=""):
        if self.client:
            prompt = f"Technical coordinator analyzer. 1. If Japanese, translate. 2. If English, polish. 3. Concise title (3-7 words). INPUT: {text} OUTPUT: TITLE: <title> TRANSLATION: <text>"
            try:
                response = self.client.models.generate_content(model=self.model_name, contents=prompt)
                result = response.text.strip()
                if "TITLE:" in result and "TRANSLATION:" in result:
                    title = result.split("TITLE:")[1].split("TRANSLATION:")[0].strip().replace("**", "").replace("#", "")
                    trans = result.split("TRANSLATION:")[1].strip()
                    return title, trans
            except: pass
        first_line = text.split('\n')[0]
        title = (first_line[:60].rsplit(' ', 1)[0] + "...") if len(first_line) > 60 else first_line
        return title, text

    def _send_sync_report(self):
        msg = "🔄 *Maintenance Sync Complete*\n________________________________\n"
        if self.stats["new_tasks"] > 0: msg += f"• 🆕 Created *{self.stats['new_tasks']}* new reports\n"
        if self.stats["status_syncs"] > 0: msg += f"• 🔄 Updated *{self.stats['status_syncs']}* sheet statuses\n"
        if self.stats["date_syncs"] > 0: msg += f"• 📅 Mirrored *{self.stats['date_syncs']}* date pairs to Project 3\n"
        if self.stats["healed_links"] > 0: msg += f"• 🩹 Healed *{self.stats['healed_links']}* sub-issue links\n"
        if not self.dry_run: self._post_to_chat(msg)
        else: print(f"[DRY RUN] Would post sync report:\n{msg}")

    def _send_daily_report(self, unused):
        today_dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        active_tasks = self.gh_specialist.get_full_active_tasks()
        login_to_name = {v.lower(): k for k, v in self.developer_map.items()}
        in_progress = {}; delayed = {}; unscheduled = []
        for task in active_tasks:
            name = login_to_name.get((task['assignee'] or "unassigned").lower(), "Unassigned")
            start = task.get('start_date'); end = task.get('end_date')
            url = task.get('url', '#')
            task_entry = f"• *{task['project_tag']}* <{url}|{task['title']}>"
            if start: task_entry += f" [{start} → {end}]"
            if not start or not end: unscheduled.append(f"• *{task['project_tag']}* <{url}|{task['title']}> (@{name})")
            else:
                try:
                    s_dt = datetime.strptime(start, "%Y-%m-%d"); e_dt = datetime.strptime(end, "%Y-%m-%d")
                    if e_dt < today_dt:
                        if name not in delayed: delayed[name] = []
                        delayed[name].append(task_entry)
                    elif s_dt <= today_dt <= e_dt:
                        if name not in in_progress: in_progress[name] = []
                        in_progress[name].append(task_entry)
                except: unscheduled.append(f"• *{task['project_tag']}* <{url}|{task['title']}> (@{name})")
        msg = f"📅 *Daily Operations Report ({today_dt.strftime('%Y-%m-%d')})*\n________________________________\n\n"
        if in_progress:
            msg += "🚀 *IN PROGRESS TODAY*\n"
            for n in sorted(in_progress.keys()):
                m = f"<users/{self.chat_ids.get(n, n)}>" if self.chat_ids.get(n, "").replace(".","").isdigit() else f"*{n}*"
                msg += f"{m}\n" + "\n".join(in_progress[n]) + "\n\n"
        if delayed:
            msg += "⚠️ *DELAYED TASKS*\n"
            for n in sorted(delayed.keys()):
                m = f"<users/{self.chat_ids.get(n, n)}>" if self.chat_ids.get(n, "").replace(".","").isdigit() else f"*{n}*"
                msg += f"{m}\n" + "\n".join(delayed[n]) + "\n\n"
        if unscheduled:
            msg += "🔍 *NEEDS SCHEDULING*\n" + "\n".join(unscheduled[:10]) + (f"\n_...and {len(unscheduled)-10} more_" if len(unscheduled)>10 else "") + "\n\n"
        if not any([in_progress, delayed, unscheduled]): msg += "✅ No active parent tasks found!"
        if not self.dry_run: self._post_to_chat(msg)
        else: print(f"[DRY RUN] Would post focused report:\n{msg}")

    def _post_to_chat(self, text):
        if not self.chat_webhook: return
        try:
            import requests
            r = requests.post(self.chat_webhook, json={"text": text})
            if r.status_code != 200: print(f"WEBHOOK ERROR: {r.status_code} - {r.text}")
        except Exception as e: print(f"WEBHOOK EXCEPTION: {e}")

if __name__ == "__main__":
    Orchestrator().run()
