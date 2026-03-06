import os
import json
import hashlib
import re
from google import genai
from dotenv import load_dotenv
from agents.cloud_ingestor import CloudIngestor
from agents.github_specialist import GitHubSpecialist
from agents.load_balancer import DeveloperTimeline
from agents.git_sync import GitSync
from datetime import datetime

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
        # Compatibility check: if it's a file path, read it; otherwise, use as is
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
            print("WARNING: GEMINI_API_KEY not found. Automated translation will be skipped.")
            self.client = None

        self.ingestor = CloudIngestor(self.google_json, self.sheet_id)
        self.gh_specialist = GitHubSpecialist(self.github_token, dry_run=self.dry_run)
        
        if self.github_token:
            self.git_sync = GitSync(self.github_token, self.ingestor, dry_run=self.dry_run)
        else:
            self.git_sync = None
        
        self.chat_webhook = os.getenv('GOOGLE_CHAT_REPORT_WEBHOOK')
        
        # Developer Mapping to GitHub Usernames
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
        for name, github_user in self.developer_map.items():
            timeline = DeveloperTimeline(name, start_date=self.start_date)
            try:
                actual_load = self.gh_specialist.get_active_workload(github_user)
                timeline.fill_hours(actual_load)
            except Exception as e:
                print(f"WARNING: Could not fetch initial load for {name}: {e}")
            self.timelines[github_user] = timeline

        # Tracking for detailed audit output
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
        content = f"{task['content']}|{task['estimated_hours']}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _detect_priority(self, content):
        """
        Detects priority based on keywords.
        urgent / 至急 (not "not urgent" / "至急ではない") -> P0
        not urgent / 至急ではない -> P2
        default -> P1
        """
        content_lower = content.lower()
        
        is_not_urgent = "not urgent" in content_lower or "至急ではない" in content or "至急ではない" in content_lower
        is_urgent = "urgent" in content_lower or "至急" in content or "至急" in content_lower
        
        if is_not_urgent:
            return "P2"
        if is_urgent:
            return "P0"
        return "P1"

    def run(self):
        print(f"--- Starting Orchestration: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        
        # Stats for reporting
        self.stats = {
            "new_tasks": 0,
            "reassigned": 0,
            "status_syncs": 0,
            "healed_links": 0,
            "date_syncs": 0
        }

        display_date = self.start_date if self.start_date else "Today"
        print(f"\n--- Team Capacity Map (Starting {display_date}) ---")
        for name, github_user in self.developer_map.items():
            timeline = self.timelines[github_user]
            bars = ""
            for b in timeline.buckets:
                fill_ratio = b['used'] / 6.0
                if fill_ratio >= 1.0: bars += "█"
                elif fill_ratio > 0.5: bars += "▓"
                elif fill_ratio > 0: bars += "░"
                else: bars += "."
            print(f"{name.ljust(8)} [{bars}] first day usage: {timeline.get_today_usage()}h")
        print("--------------------------------------------\n")

        try:
            tasks = self.ingestor.get_live_tasks()
            print(f"Found {len(tasks)} valid tasks in Google Sheets.")
            
            if self.git_sync:
                sync_stats = self.git_sync.scan_and_sync(tasks)
                if sync_stats:
                    self.stats["status_syncs"] += sync_stats.get("status_changes", 0)
                    self.stats["healed_links"] += sync_stats.get("healed_links", 0)
                    self.stats["date_syncs"] += sync_stats.get("date_migrations", 0)

            import time
            for task in tasks:
                self.process_task(task)
                if not self.dry_run:
                    time.sleep(2) # Avoid hitting API limits in live run
                else:
                    time.sleep(1) # Faster but still safe for dry run
            
            # --- SYNC REPORT ---
            if any(v > 0 for v in self.stats.values()):
                self._send_sync_report()

            target_hour = int(os.getenv('REPORT_HOUR', '0')) 
            today_date = datetime.now().strftime("%Y-%m-%d")
            if datetime.now().hour == target_hour and self.state.get('last_report_date') != today_date:
                self._send_daily_report(tasks)
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
            # --- AUTO-READY TRIGGER (Sub-issue check) ---
            # If all sub-issues are closed, move parent to 'Ready'
            try:
                # Extract issue number
                match = re.search(r'/issues/(\d+)', task_id)
                if match:
                    issue_num = int(match.group(1))
                    gh_data = self.gh_specialist.get_project_item_data(issue_num, 4)
                    if gh_data and gh_data.get('Status') == "To Triage":
                        title = gh_data.get('Title')
                        if self.gh_specialist.get_child_issues_status(title):
                            print(f"AUTO-READY: All sub-issues closed for #{issue_num}. Moving to 'Ready'.")
                            if not self.dry_run:
                                # We need to add 'Ready' option ID to GitHubSpecialist later, 
                                # using 'Backlog' as a fallback for now
                                ready_opt = "f75ad846" # 'Backlog' in Project 4
                                self.gh_specialist.update_field(4, gh_data['item_id'], 'status', ready_opt, is_option=True)
            except Exception as e:
                print(f"DEBUG: Ready trigger failed: {e}")

            if self.state.get(task_id) == current_hash: return
            self.state[task_id] = current_hash
            return

        if task.get('pic'): return

        full_desc, ai_summary, romaji_name = self._generate_bilingual_description(task)
        best_dev = self._find_best_dev(task['estimated_hours'])
        
        if best_dev:
            start_date, end_date = self.timelines[best_dev['id']].fill_hours_with_dates(task['estimated_hours'])
            priority = self._detect_priority(task['content'])
            
            # --- CONSISTENT TITLE PREFIXING ---
            summary = f"[MAINTENANCE] {ai_summary} ({romaji_name} - #{task['id']})"
            
            # --- INTELLIGENT REPO ROUTING ---
            target_repo = "member"
            content_lower = task['content'].lower()
            if "bohr" in content_lower or "bohr-individual" in content_lower:
                target_repo = "bohr-individual"
            
            if self.dry_run:
                print(f"\n[DRY RUN] NEW TASK CREATION FLOW for Task {task['id']} in {target_repo}:")
                print(f"  1. Parent Issue:  {summary} (@{best_dev['id']}) [Priority: {priority}]")
                print(f"  2. Sub-Issue:     Understand the request: {ai_summary} (0.33h)")
                print(f"  3. Project Setup: Status: To Triage, Level: Parent/Child, Dates: {start_date} to {end_date}")
                print(f"  4. Sheet Update:  Status: Open, URL: [MOCK_URL], PIC: {best_dev['name']}")
                return

            try:
                # Phase 1: Create GitHub Issue (Parent) in the TARGET REPO
                issue = self.gh_specialist.create_issue(
                    repo=target_repo, title=summary, body=full_desc, assignee=best_dev['id'], labels=["staff-report"]
                )
                issue_url = issue['html_url']
                parent_node_id = issue['node_id']
                parent_number = issue['number']
                
                # --- PROJECT 4 (Maintenance) ---
                item_id_p4 = self.gh_specialist.add_to_project(parent_node_id, 4)
                self.gh_specialist.update_field(4, item_id_p4, 'status', self.gh_specialist.projects[4]['options']['status_to_triage'], is_option=True)
                self.gh_specialist.update_field(4, item_id_p4, 'start_date', start_date)
                self.gh_specialist.update_field(4, item_id_p4, 'end_date', end_date)
                self.gh_specialist.update_field(4, item_id_p4, 'priority', self.gh_specialist.projects[4]['options'][f'priority_{priority.lower()}'], is_option=True)
                self.gh_specialist.update_field(4, item_id_p4, 'level', self.gh_specialist.projects[4]['options']['level_parent'], is_option=True)
                self.gh_specialist.update_field(4, item_id_p4, 'hours', task['estimated_hours'])
                
                # --- PROJECT 3 (Overall Project Management) ---
                item_id_p3 = self.gh_specialist.add_to_project(parent_node_id, 3)
                # Set custom field 'project' to 'Maintenance'
                self.gh_specialist.update_field(3, item_id_p3, 'project', self.gh_specialist.projects[3]['options']['project_maintenance'], is_option=True)
                # Set Dates in Project 3
                self.gh_specialist.update_field(3, item_id_p3, 'start_date', start_date)
                self.gh_specialist.update_field(3, item_id_p3, 'end_date', end_date)

                # Phase 2: Create Sub-issue (Understand the Request)
                sub_title = f"Understand the request: {ai_summary} (Sub-issue for #{parent_number})"
                sub_body = f"Mandatory 20-minute task to review and clarify requirements for #{parent_number}."
                sub_issue = self.gh_specialist.create_issue(
                    repo=target_repo, title=sub_title, body=sub_body, assignee=best_dev['id'], labels=["staff-report"]
                )
                sub_node_id = sub_issue['node_id']
                sub_item_id = self.gh_specialist.add_to_project(sub_node_id, 4)

                # Natively link sub-issue to parent
                self.gh_specialist.link_subissue(parent_node_id, sub_node_id)

                
                # Update Sub-issue Fields (Project 4 only)
                self.gh_specialist.update_field(4, sub_item_id, 'status', self.gh_specialist.projects[4]['options']['status_to_triage'], is_option=True)
                self.gh_specialist.update_field(4, sub_item_id, 'level', self.gh_specialist.projects[4]['options']['level_child'], is_option=True)
                self.gh_specialist.update_field(4, sub_item_id, 'hours', 0.33)
                # Link to Parent
                self.gh_specialist.update_field(4, sub_item_id, 'parent_issue', summary)

                # Write back to Sheet
                self.ingestor.write_backlog_id(task['anchors'], issue_url)
                self.ingestor.write_status(task['anchors'], "Open") # "To Triage" maps to "Open" in sheet
                if hasattr(self.ingestor, 'write_pic'): self.ingestor.write_pic(task['anchors'], best_dev['name'])
                if hasattr(self.ingestor, 'write_dates'): self.ingestor.write_dates(task['anchors'], start_date, end_date)
                
                self.stats["new_tasks"] += 1
                self.state[issue_url] = current_hash
                print(f"SUCCESS: Created {issue_url}")
            except Exception as e:
                print(f"ERROR: Failed to process task {task['id']}: {str(e)}")
        else:
            print(f"OVERLOAD: No capacity for Task {task['id']}.")

    def _find_best_dev(self, hours):
        """
        Finds the dev who can finish earliest.
        PRIORITY: Prioritize the team (Saurabh, Raman, Ewan).
        CHOO: Only assign to Choo if the team is completely booked for 14 days.
        """
        team_options = []
        choo_option = None

        for github_user, timeline in self.timelines.items():
            finish_date = timeline.peek_fill(hours)
            if finish_date:
                name = [k for k, v in self.developer_map.items() if v == github_user][0]
                option = {"name": name, "id": github_user, "finish_date": finish_date}
                
                if name == "Choo":
                    choo_option = option
                else:
                    team_options.append(option)
        
        # 1. Try assigning to the team first (earliest finish date)
        if team_options:
            return sorted(team_options, key=lambda x: x['finish_date'])[0]
        
        # 2. If team is overloaded, return Choo's earliest date
        return choo_option

    def _generate_bilingual_description(self, task):
        GID = "635134579"
        title_summary, en_translation = self._translate_and_summarize(task['content'], fallback_translation=task.get('english_translation_fallback', ''))
        romaji_name = self.name_mapping.get(task['requester'], task['requester'])
        row = task['row_index'] + 1
        sheet_link = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/edit?gid={GID}#gid={GID}&range=B{row}:C{row}"
        
        description = f"ID: {task['id']}\nSheet Link: {sheet_link}\n\n"
        
        # Check if we actually got a distinct translation from Gemini
        is_fallback = en_translation.strip() == task['content'].strip()
        
        if is_fallback:
            sheet_translation = task.get('english_translation_fallback', '').strip()
            # If sheet translation is just a URL, treat it as a reference
            is_url_only = sheet_translation.startswith("http") and "\n" not in sheet_translation
            
            if sheet_translation and not is_url_only:
                description += f"## 📝 Description (Sheet Translation)\n\n{sheet_translation}\n\n"
                description += f"## 📄 Source Content (Original)\n\n{task['content']}"
            else:
                is_likely_jp = any(ord(c) > 128 for c in task['content'][:100])
                header = "## 📄 Source Content (Japanese)" if is_likely_jp else "## 📝 Source Content (English)"
                description += f"{header}\n\n{task['content']}"
                if sheet_translation:
                     description += f"\n\n## 🔗 Reference Link\n\n{sheet_translation}"
                if is_likely_jp:
                    description += "\n\n> ⚠️ *Note: Automatic translation unavailable due to API limit.*"
        else:
            # Clean Gemini-generated format
            description += f"## 📝 Description (English)\n\n{en_translation}\n\n"
            description += f"## 📄 Source Content (Original)\n\n{task['content']}"
            
        return description, title_summary, romaji_name

    def _translate_and_summarize(self, text, fallback_translation=""):
        if self.client:
            prompt = f"""
            You are a technical coordinator. Analyze the following bug report from a Google Sheet.
            1. If Japanese, translate to professional English. 2. If English, polish for clarity.
            3. Provide a very concise title (3-7 words) for a GitHub Issue.
            INPUT: {text}
            OUTPUT FORMAT:
            TITLE: <Concise Title>
            TRANSLATION: <Polished/Translated English>
            """
            try:
                response = self.client.models.generate_content(model=self.model_name, contents=prompt)
                result = response.text.strip()
                if "TITLE:" in result and "TRANSLATION:" in result:
                    title = result.split("TITLE:")[1].split("TRANSLATION:")[0].strip().replace("**", "").replace("#", "")
                    trans = result.split("TRANSLATION:")[1].strip()
                    return title, trans
            except Exception as e:
                if "429" not in str(e): print(f"LLM ERROR: {e}")

        # --- REFINED FALLBACK LOGIC ---
        first_line = text.split('\n')[0]
        # Clean up title: no more than 60 chars, don't break words
        if len(first_line) > 60:
            title = first_line[:60].rsplit(' ', 1)[0] + "..."
        else:
            title = first_line
            
        return title, text

    def _send_sync_report(self):
        """Sends a concise action report to Google Chat."""
        msg = "🔄 *Maintenance Sync Complete*\n"
        msg += "________________________________\n"
        if self.stats["new_tasks"] > 0: msg += f"• 🆕 Created *{self.stats['new_tasks']}* new reports\n"
        if self.stats["status_syncs"] > 0: msg += f"• 🔄 Updated *{self.stats['status_syncs']}* sheet statuses\n"
        if self.stats["date_syncs"] > 0: msg += f"• 📅 Mirrored *{self.stats['date_syncs']}* date pairs to Project 3\n"
        if self.stats["healed_links"] > 0: msg += f"• 🩹 Healed *{self.stats['healed_links']}* sub-issue links\n"
        
        print(f"REPORT: Sending Sync Report to Google Chat...")
        if self.dry_run:
            print(f"[DRY RUN] Would post sync report:\n{msg}")
        else:
            self._post_to_chat(msg)

    def _send_daily_report(self, all_tasks):
        today_str = datetime.now().strftime("%Y%m%d")
        full_report = f"📅 *Daily Report {today_str}*\n________________________________\n\n"
        report_data = {}
        for task in all_tasks:
            pic_name = task.get('pic')
            if not pic_name or "complete" in task.get('current_sheet_status', '').lower(): continue
            if pic_name not in report_data: report_data[pic_name] = []
            report_data[pic_name].append(f"• {task.get('content')[:50]}")
        for name, tasks in report_data.items():
            full_report += f"*{name}*\n" + "\n".join(tasks) + "\n\n"
        if not report_data: full_report += "✅ No open tasks!"
        self._post_to_chat(full_report)

    def _post_to_chat(self, text):
        if not self.chat_webhook: return
        try:
            import requests
            requests.post(self.chat_webhook, json={"text": text})
        except: pass

if __name__ == "__main__":
    Orchestrator().run()
