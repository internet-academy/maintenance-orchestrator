import os
import json
import hashlib
from google import genai
from dotenv import load_dotenv
from agents.cloud_ingestor import CloudIngestor
from agents.load_balancer import LoadBalancer, DeveloperTimeline
from agents.git_sync import GitSync
from datetime import datetime

# Load environment variables from .env
load_dotenv()

class Orchestrator:
    def __init__(self, dry_run=None):
        if dry_run is None:
            # Respect environment variable, default to False (Live)
            env_val = os.getenv('DRY_RUN', 'False').lower()
            self.dry_run = env_val in ['true', '1', 't', 'y', 'yes']
        else:
            self.dry_run = dry_run
            
        if self.dry_run:
            print("!!! RUNNING IN DRY RUN MODE - NO API MUTATIONS WILL OCCUR !!!")
        
        self.google_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
        self.backlog_key = os.getenv('BACKLOG_API_KEY')
        self.space_id = os.getenv('BACKLOG_SPACE_ID')
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.github_token = os.getenv('GITHUB_TOKEN')
        
        # State tracking to prevent redundant updates
        self.state_file = "sync_state.json"
        self.state = self._load_state()

        if self.gemini_key:
            self.client = genai.Client(api_key=self.gemini_key)
            self.model_name = 'gemini-flash-latest'
        else:
            print("WARNING: GEMINI_API_KEY not found. Automated translation will be skipped.")
            self.client = None

        self.ingestor = CloudIngestor(self.google_json, self.sheet_id)
        self.load_balancer = LoadBalancer(self.backlog_key, self.space_id)
        
        # Initialize GitSync if token is available
        if self.github_token:
            self.git_sync = GitSync(self.github_token, self.backlog_key, self.space_id, dry_run=self.dry_run)
        else:
            print("WARNING: GITHUB_TOKEN not found. Git-to-Backlog sync will be skipped.")
            self.git_sync = None
        
        # Google Chat Webhook for Reporting
        self.chat_webhook = os.getenv('GOOGLE_CHAT_REPORT_WEBHOOK')
        
        # Real Developer Mapping for i-academy space
        self.developer_map = {
            "Saurabh": 984450,
            "Raman": 1819362,
            "Ewan": 1880127,
            "Choo": 1052465
        }
        
        # Google Chat IDs for @mentions (User needs to provide these)
        self.chat_ids = {
            "Saurabh": os.getenv('CHAT_ID_SAURABH', 'Saurabh'),
            "Raman": os.getenv('CHAT_ID_RAMAN', 'Raman'),
            "Ewan": os.getenv('CHAT_ID_EWAN', 'Ewan'),
            "Choo": os.getenv('CHAT_ID_CHOO', 'Choo')
        }
        
        # Name Mapping (Localized to English)
        self.name_mapping = {
            "鈴木佳子": "Suzuki",
            "稲葉由衣": "Inaba",
            "谷川大虎": "Tanikawa",
            "中村駿吾": "Nakamura",
            "石井陽介": "Ishii",
            "榎本智香": "Enomoto",
            "眞尾由紀子": "Mao"
        }
        
        # Initialize Timelines for all developers
        # Defaults to Today, but can be overridden via env var (e.g. for March start)
        self.start_date = os.getenv('SYNC_START_DATE') 
        
        self.timelines = {}
        for name, dev_id in self.developer_map.items():
            timeline = DeveloperTimeline(name, start_date=self.start_date)
            # ALWAYS pre-fill with actual Backlog load to ensure real-time accuracy
            try:
                actual_load = self.load_balancer.get_active_workload(dev_id, project_id=528169)
                timeline.fill_hours(actual_load)
            except Exception as e:
                print(f"WARNING: Could not fetch initial load for {name}: {e}")
            
            self.timelines[dev_id] = timeline

    def _load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_state(self):
        # We allow saving state in dry_run mode for validation purposes
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def _get_task_hash(self, task):
        """Generates a hash of the raw task content to detect changes."""
        # Use only raw sheet data for the hash to avoid AI non-determinism flapping.
        # Include content and estimated hours.
        content = f"{task['content']}|{task['estimated_hours']}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _get_or_create_parent_task(self, target_date_str):
        """
        Determines the parent task summary based on the target date's month end.
        Finds or creates the parent '◆リクエラ(YYYY/M/D)' task.
        """
        # Parse date and find end of month
        dt = datetime.strptime(target_date_str, "%Y-%m-%d")
        import calendar
        last_day = calendar.monthrange(dt.year, dt.month)[1]
        
        # Format: YYYY/M/D (no leading zeros for M/D)
        month_end_label = f"{dt.year}/{dt.month}/{last_day}"
        summary = f"◆リクエラ({month_end_label})"
        project_id = 528169
        
        # 1. Search for existing
        parent = self.load_balancer.find_issue_by_summary(summary, project_id)
        if parent:
            print(f"HIERARCHY: Found existing parent task '{summary}' (ID: {parent['id']})")
            return parent['id']
            
        # 2. Create if not exists
        print(f"HIERARCHY: Creating new parent task '{summary}'...")
        if self.dry_run:
            return "MOCK_PARENT_ID"
            
        # Create a top-level task for the parent
        parent_payload = {
            "projectId": project_id,
            "summary": summary,
            "description": f"Parent task for error reports ending {month_end_label}",
            "issueTypeId": 2750765, # バグ (or use a Task type if available)
            "priorityId": 3,
            "estimatedHours": 0
        }
        
        endpoint = f"{self.load_balancer.base_url}/issues"
        params = {"apiKey": self.load_balancer.api_key}
        import requests
        r = requests.post(endpoint, params=params, data=parent_payload)
        r.raise_for_status()
        new_parent = r.json()
        return new_parent['id']

    def run(self):
        print(f"--- Starting Orchestration: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        
        display_date = self.start_date if self.start_date else "Today"
        print(f"\n--- Team Capacity Map (Starting {display_date}) ---")
        for name, dev_id in self.developer_map.items():
            timeline = self.timelines[dev_id]
            # Simple bar chart: [######....]
            bars = ""
            for b in timeline.buckets:
                fill_ratio = b['used'] / self.load_balancer.DAILY_LIMIT_HOURS
                if fill_ratio >= 1.0: bars += "█"
                elif fill_ratio > 0.5: bars += "▓"
                elif fill_ratio > 0: bars += "░"
                else: bars += "."
            print(f"{name.ljust(8)} [{bars}] first day usage: {timeline.get_today_usage()}h")
        print("--------------------------------------------\n")

        try:
            # 0. Sync Git Activity (GitHub -> Backlog)
            self.sync_git_activity()

            # 1. Ingest Tasks (Sheet -> Standardized Objects)
            tasks = self.ingestor.get_live_tasks()
            print(f"Found {len(tasks)} valid tasks in Google Sheets.")
            
            # --- TASK LIMITING FOR FASTER TESTING ---
            task_limit = int(os.getenv('TASK_LIMIT', '0'))
            if task_limit > 0:
                tasks = tasks[:task_limit]
                print(f"LIMIT: Processing only the first {task_limit} tasks.")

            for task in tasks:
                self.process_task(task)
            
            # --- TIME-GATED DAILY REPORT ---
            # Default to hour 0 (9 AM JST) if not specified
            target_hour = int(os.getenv('REPORT_HOUR', '0')) 
            today_date = datetime.now().strftime("%Y-%m-%d")
            current_hour = datetime.now().hour

            if current_hour == target_hour:
                if self.state.get('last_report_date') != today_date:
                    print(f"REPORT WINDOW OPEN: Sending Daily Report for {today_date}...")
                    self._send_daily_report(tasks)
                    self.state['last_report_date'] = today_date
                else:
                    print("REPORT SKIP: Already sent today.")
            else:
                print(f"REPORT SKIP: Current hour {current_hour} != Target {target_hour}.")
            
            self._save_state()

        except Exception as e:
            import traceback
            print(f"CRITICAL ERROR: {str(e)}")
            traceback.print_exc()

    def sync_git_activity(self):
        """Scans configured repositories for PR activity and updates Backlog."""
        if not self.git_sync:
            return

        repos = [
            "internet-academy/bohr-individual",
            "internet-academy/member"
        ]
        
        print("\n--- Starting Git-to-Backlog Sync ---")
        for repo in repos:
            self.git_sync.scan_and_sync(repo)
        print("--- Git Sync Complete ---\n")

    def _post_to_chat(self, text, thread_key=None):
        """Sends a message to Google Chat via webhook."""
        if not self.chat_webhook:
            print("DEBUG: No Google Chat webhook configured. Skipping message.")
            return

        url = self.chat_webhook
        if thread_key:
            # threadKey automatically groups messages into a single thread in Google Chat
            url += f"&threadKey={thread_key}"

        payload = {"text": text}
        try:
            import requests
            r = requests.post(url, json=payload)
            r.raise_for_status()
        except Exception as e:
            print(f"ERROR posting to Google Chat: {e}")

    def _send_daily_report(self, all_tasks):
        """Aggregates all open tasks into a single consolidated message."""
        today_str = datetime.now().strftime("%Y%m%d")
        thread_key = f"daily_report_{today_str}"
        
        # 1. Build the Report Header
        full_report = f"📅 *Daily Report {today_str}*\n"
        full_report += "________________________________\n\n"

        # 2. Group tasks by current PIC
        report_data = {}
        for task in all_tasks:
            status = task.get('current_sheet_status', '').lower()
            if "complete" in status or "closed" in status or "resolved" in status:
                continue
            
            pic_name = task.get('pic')
            if not pic_name:
                continue
                
            if pic_name not in report_data:
                report_data[pic_name] = []
            
            title = task.get('title_summary', task['content'][:50])
            report_data[pic_name].append(f"• [{task.get('backlog_id', 'NEW')}] {title}")

        # 3. Build the single message body
        if not report_data:
            full_report += "✅ No open tasks for today!"
        else:
            for name, tasks in report_data.items():
                chat_id = self.chat_ids.get(name, name)
                # If chat_id is numeric, use mention format, otherwise use plain text name
                mention = f"<users/{chat_id}>" if chat_id.isdigit() else f"*{name}*"
                
                full_report += f"{mention}\n" + "\n".join(tasks) + "\n\n"

        # 4. Post the entire report as ONE message
        print(f"REPORT: Sending consolidated Daily Report to Google Chat...")
        if self.dry_run:
            print(f"[DRY RUN] Would post consolidated report:\n{full_report}")
        else:
            self._post_to_chat(full_report, thread_key=thread_key)

    def _translate_and_summarize(self, text, fallback_translation=""):
        """Uses Gemini to translate Japanese to English and generate a title with retries."""
        if not self.client:
            # Fallback to sheet's google translation if client is missing
            return "Bug Report", fallback_translation if fallback_translation else text

        if fallback_translation:
            prompt = f"""
            You are a translation assistant for a software development team.
            
            We already have a rough English translation for a Japanese bug report.
            Please polish this English translation to be professional and clear, ensuring it captures all nuances from the original Japanese text.
            
            Also, provide a very concise (3-7 words) English summary for a ticket title.
            
            Output format:
            TITLE: <Concise Title>
            TRANSLATION: <Polished Full English Translation>
            
            ORIGINAL JAPANESE:
            {text}
            
            ROUGH TRANSLATION:
            {fallback_translation}
            """
        else:
            prompt = f"""
            You are a translation assistant for a software development team.
            Translate the following Japanese bug report/task description into professional English.
            The translation should be full-text and include ALL details from the original.
            
            Also, provide a very concise (3-7 words) English summary for a ticket title.
            
            Output format:
            TITLE: <Concise Title>
            TRANSLATION: <Full English Translation>
            
            TEXT TO TRANSLATE:
            {text}
            """
        
        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                result = response.text.strip()
                
                if "TITLE:" in result and "TRANSLATION:" in result:
                    title_part = result.split("TITLE:")[1].split("TRANSLATION:")[0].strip()
                    translation_part = result.split("TRANSLATION:")[1].strip()
                    # Clean up any potential markdown headers if Gemini included them
                    title_part = title_part.replace("**", "").replace("#", "").strip()
                    return title_part, translation_part
                
                # If format is unexpected but we got a response, break retry and use fallback
                break
                
            except Exception as e:
                if "503" in str(e) and attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    print(f"WARNING: Gemini 503 (Busy). Retrying in {wait_time}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                print(f"ERROR calling Gemini API: {e}")
                break

        # Fallback Logic
        title = "Bug Report"
        if fallback_translation:
            first_line = fallback_translation.split('\n')[0]
            if len(first_line) > 10:
                title = first_line[:50] + "..." if len(first_line) > 50 else first_line
        return title, fallback_translation if fallback_translation else text

    def _generate_bilingual_description(self, task):
        """Constructs a bilingual description with deep links and automated translation."""
        # Constants for precision linking
        GID = "635134579"
        
        # Determine Title Summary and English Translation via Gemini (with Sheet fallback)
        title_summary, en_translation = self._translate_and_summarize(
            task['content'], 
            fallback_translation=task.get('english_translation_fallback', '')
        )
            
        # Get localized name
        romaji_name = self.name_mapping.get(task['requester'], task['requester'])
        
        # Construct Precision Sheet Link
        row = task['row_index'] + 1
        sheet_link = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/edit?gid={GID}#gid={GID}&range=B{row}:C{row}"
        
        # Build Description Body
        description = f"ID: {task['id']}\n"
        description += f"Sheet Link: {sheet_link}\n\n"
        description += f"## English Translation\n\n{en_translation}\n\n"
        description += f"## 原文 (Japanese)\n\n{task['content']}"
        
        return description, title_summary, romaji_name

    def _verify_ownership(self, backlog_id, task):
        """
        Verifies if the existing Backlog ticket actually belongs to this row.
        Returns True if it matches, False if it's a copied ID from elsewhere.
        """
        try:
            issue = self.load_balancer.get_issue(backlog_id)
            desc = issue.get('description', '')
            
            # 1. Primary Check: Unique Task ID stamp (e.g., "ID: 1")
            id_marker = f"ID: {task['id']}\n"
            if id_marker in desc:
                return True
                
            # 2. Secondary Check: Sheet Link range (Flexible matching)
            row_num = task['row_index'] + 1
            # Check for range=A20, range=B20, or range=B20:C20
            patterns = [
                f"range=A{row_num}",
                f"range=B{row_num}",
                f"range=B{row_num}:C{row_num}"
            ]
            
            for p in patterns:
                if p in desc:
                    return True
            
            print(f"⚠️ COLLISION DETECTED: {backlog_id} belongs to a different row.")
            return False
        except Exception as e:
            print(f"DEBUG: Could not verify ownership for {backlog_id}: {e}")
            return False

    def process_task(self, task):
        # 1. Update Detection & Ownership Verification
        backlog_id = task.get('backlog_id')
        latest_backlog_issue = None
        
        # Calculate current content hash for change detection
        current_hash = self._get_task_hash(task)
        
        if backlog_id:
            # NEW: Verify that this ID wasn't just copy-pasted from another row
            is_rightful_owner = self._verify_ownership(backlog_id, task)
            
            if is_rightful_owner:
                # Fetch full issue to get latest status and metadata (Reverse Sync)
                try:
                    latest_backlog_issue = self.load_balancer.get_issue(backlog_id)
                    
                    # --- REVERSE STATUS SYNC (Backlog -> Sheet) ---
                    backlog_status = latest_backlog_issue.get('status', {}).get('name')
                    sheet_status = task.get('current_sheet_status', '')
                    
                    # Map Backlog name to Sheet display
                    status_map = {
                        "Open": "Open",
                        "In Progress": "In Progress",
                        "Resolved": "Resolved",
                        "Closed": "Complete!"
                    }
                    mapped_status = status_map.get(backlog_status, backlog_status)
                    
                    if mapped_status and mapped_status != sheet_status:
                        print(f"STATUS SYNC: Backlog ({mapped_status}) != Sheet ({sheet_status}). Updating Sheet...")
                        if not self.dry_run:
                            self.ingestor.write_status(task['anchors'], mapped_status)
                except Exception as e:
                    print(f"WARNING: Could not fetch latest status for {backlog_id}: {e}")

                # --- CHANGE DETECTION (Sheet -> Backlog) ---
                if self.state.get(backlog_id) == current_hash:
                    print(f"SKIP: No content changes detected for {backlog_id}.")
                    return

                # If we reach here, content or metadata (hours) has changed.
                print(f"UPDATE: Changes detected for {backlog_id}. Regenerating content...")
                
                # Generate Bilingual content, summary, and localized name
                full_desc, ai_summary, romaji_name = self._generate_bilingual_description(task)
                
                # Prepare update payload
                update_payload = {
                    'description': full_desc,
                    'summary': f"[ERROR] {ai_summary} ({romaji_name} - #{task['id']})",
                    'estimated_hours': task['estimated_hours']
                }

                # CRITICAL: Only recalculate deadline if estimated_hours changed 
                # OR if the existing ticket has no deadline.
                # Do NOT fill the timeline here, as existing active tasks were already 
                # counted in __init__.
                old_hours = latest_backlog_issue.get('estimatedHours')
                old_due = latest_backlog_issue.get('dueDate')
                
                if float(task['estimated_hours']) != float(old_hours or 0) or not old_due:
                    print(f"RE-SCHEDULING: Hours changed ({old_hours} -> {task['estimated_hours']}) or missing deadline.")
                    best_dev = self._find_best_dev(task['estimated_hours'])
                    if best_dev:
                        # We use peek_fill here because the ticket's original hours ARE in the 
                        # current timeline buckets already (fetched from get_active_workload).
                        # Using fill_hours would double-count the same task.
                        new_due = self.timelines[best_dev['id']].peek_fill(task['estimated_hours'])
                        update_payload['deadline'] = new_due
                        update_payload['parent_id'] = self._get_or_create_parent_task(new_due)
                
                # Perform the update
                if self.dry_run:
                    print(f"[DRY RUN] Would update verified Backlog {backlog_id} with: {update_payload}")
                else:
                    try:
                        self.load_balancer.update_backlog_issue(backlog_id, update_payload)
                        print(f"SUCCESS: Updated Backlog {backlog_id}")
                        self.state[backlog_id] = current_hash
                    except Exception as e:
                        print(f"ERROR: Failed to update {backlog_id}: {str(e)}")
                return
            else:
                print(f"ACTION: ID {backlog_id} appears to be a copy. Resetting to CREATE mode for this row.")
                backlog_id = None # Force creation of a fresh ticket

        # 2. Skip if already assigned in sheet (New Task Only)
        if task.get('pic'):
            print(f"SKIP: Task {task['id']} already has PIC: {task['pic']}")
            return

        # 3. New Task Assignment Logic
        # Generate Bilingual content, summary, and localized name
        full_desc, ai_summary, romaji_name = self._generate_bilingual_description(task)
        task['description'] = full_desc
        task['title_summary'] = ai_summary
        task['summary'] = f"[ERROR] {ai_summary} ({romaji_name} - #{task['id']})"

        best_dev = self._find_best_dev(task['estimated_hours'])
        
        if best_dev:
            # The completion date is the calculated deadline
            due_date = self.timelines[best_dev['id']].fill_hours(task['estimated_hours'])
            task['deadline'] = due_date
            
            # LINK TO PARENT based on deadline
            task['parent_id'] = self._get_or_create_parent_task(due_date)
            
            print(f"ASSIGNING: Task {task['id']} (Req: {romaji_name}) ({task['estimated_hours']}h) -> {best_dev['name']}")
            print(f"TITLE PREVIEW: {task['summary']}")
            print(f"HIERARCHY: Linking to Parent ID {task['parent_id']}")
            
            if self.dry_run:
                print(f"[DRY RUN] Would create Backlog Issue for {best_dev['name']} with deep-link and parent.")
                return
            try:
                issue = self.load_balancer.create_backlog_issue(best_dev['id'], task)
                issue_key = issue['issueKey']
                print(f"CREATED: Backlog Issue {issue_key}")
                self.ingestor.write_backlog_id(task['anchors'], issue_key)
                # Update local state
                self.state[issue_key] = current_hash
            except Exception as e:
                print(f"ERROR: Failed to create issue: {str(e)}")
        else:
            print(f"OVERLOAD: No capacity for Task {task['id']} even in 14-day window.")

        # 2. Skip if already assigned in sheet (New Task Only)
        if task.get('pic'):
            print(f"SKIP: Task {task['id']} already has PIC: {task['pic']}")
            return

        # 3. New Task Assignment Logic
        # Generate Bilingual content, summary, and localized name
        full_desc, ai_summary, romaji_name = self._generate_bilingual_description(task)
        task['description'] = full_desc
        task['title_summary'] = ai_summary
        task['summary'] = f"[ERROR] {ai_summary} ({romaji_name} - #{task['id']})"

        best_dev = self._find_best_dev(task['estimated_hours'])
        
        if best_dev:
            # The completion date is the calculated deadline
            due_date = self.timelines[best_dev['id']].fill_hours(task['estimated_hours'])
            task['deadline'] = due_date
            
            # LINK TO PARENT based on deadline
            task['parent_id'] = self._get_or_create_parent_task(due_date)
            
            print(f"ASSIGNING: Task {task['id']} (Req: {romaji_name}) ({task['estimated_hours']}h) -> {best_dev['name']}")
            print(f"TITLE PREVIEW: {task['summary']}")
            print(f"HIERARCHY: Linking to Parent ID {task['parent_id']}")
            
            if self.dry_run:
                print(f"[DRY RUN] Would create Backlog Issue for {best_dev['name']} with deep-link and parent.")
                return
            try:
                issue = self.load_balancer.create_backlog_issue(best_dev['id'], task)
                issue_key = issue['issueKey']
                print(f"CREATED: Backlog Issue {issue_key}")
                self.ingestor.write_backlog_id(task['anchors'], issue_key)
                # Update local state
                self.state[issue_key] = current_hash
            except Exception as e:
                print(f"ERROR: Failed to create issue: {str(e)}")
        else:
            print(f"OVERLOAD: No capacity for Task {task['id']} even in 14-day window.")

    def _find_best_dev(self, hours):
        """Finds the dev who can finish the hours earliest, prioritizing Core."""
        core_options = []
        manager_option = None

        for name, dev_id in self.developer_map.items():
            timeline = self.timelines[dev_id]
            finish_date = timeline.peek_fill(hours)
            
            if finish_date:
                option = {"name": name, "id": dev_id, "finish_date": finish_date}
                if name == "Choo":
                    manager_option = option
                else:
                    core_options.append(option)
        
        # Sort core options by finish_date (earliest first)
        if core_options:
            return sorted(core_options, key=lambda x: x['finish_date'])[0]
        
        return manager_option

if __name__ == "__main__":
    manager = Orchestrator()
    manager.run()
