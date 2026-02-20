import os
import json
import hashlib
from google import genai
from agents.cloud_ingestor import CloudIngestor
from agents.load_balancer import LoadBalancer, DeveloperTimeline
from datetime import datetime

class Orchestrator:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        if self.dry_run:
            print("!!! RUNNING IN DRY RUN MODE - NO API MUTATIONS WILL OCCUR !!!")
        
        self.google_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
        self.backlog_key = os.getenv('BACKLOG_API_KEY')
        self.space_id = os.getenv('BACKLOG_SPACE_ID')
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        
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
        content = f"{task['content']}|{task['estimated_hours']}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

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
            tasks = self.ingestor.get_live_tasks()
            print(f"Found {len(tasks)} valid tasks in Google Sheets.")

            for task in tasks:
                self.process_task(task)
            
            # --- POST-SYNC REPORTING ---
            self._send_daily_report(tasks)
            
            self._save_state()

        except Exception as e:
            import traceback
            print(f"CRITICAL ERROR: {str(e)}")
            traceback.print_exc()

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
        """Aggregates open tasks and posts to the daily thread."""
        today_str = datetime.now().strftime("%Y%m%d")
        thread_key = f"daily_report_{today_str}"
        
        # 1. Create/Update Header
        header = f"Daily Report {today_str}"
        print(f"REPORT: Sending {header} to Google Chat...")
        if self.dry_run:
            print(f"[DRY RUN] Would post header: {header}")
        else:
            self._post_to_chat(header, thread_key=thread_key)

        # 2. Group tasks by current PIC (based on Sheet PIC or load balancer assignment)
        # Note: In a real run, we look at current_sheet_status
        report_data = {}
        for task in all_tasks:
            status = task.get('current_sheet_status', '').lower()
            if "complete" in status or "closed" in status or "resolved" in status:
                continue
            
            # We look at the PIC column in the sheet
            pic_name = task.get('pic')
            if not pic_name:
                continue
                
            if pic_name not in report_data:
                report_data[pic_name] = []
            
            # Use the English summary we generated earlier if available
            title = task.get('title_summary', task['content'][:50])
            report_data[pic_name].append(f"- [{task.get('backlog_id', 'NEW')}] {title}")

        # 3. Send individual messages for each PIC
        for name, tasks in report_data.items():
            chat_id = self.chat_ids.get(name, name)
            mention = f"<users/{chat_id}>" if chat_id.isdigit() else f"@{name}"
            
            msg = f"{mention} here are your tasks for today:\n" + "\n".join(tasks)
            
            if self.dry_run:
                print(f"[DRY RUN] Would post task list for {name}: {msg}")
            else:
                self._post_to_chat(msg, thread_key=thread_key)

    def _translate_and_summarize(self, text, fallback_translation=""):
        """Uses Gemini to translate Japanese to English and generate a title."""
        if not self.client:
            # Fallback to sheet's google translation if client is missing
            return "Bug Report", fallback_translation if fallback_translation else text

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
                
            return "Bug Report", fallback_translation if fallback_translation else text
        except Exception as e:
            print(f"ERROR calling Gemini API: {e}")
            # Hierarchy: Try to use sheet's translation as fallback if AI fails
            title = "Bug Report"
            if fallback_translation:
                # Try to extract a simple title from the fallback
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
        
        # Calculate current content hash
        current_hash = self._get_task_hash(task)
        
        if backlog_id:
            # NEW: Verify that this ID wasn't just copy-pasted from another row
            is_rightful_owner = self._verify_ownership(backlog_id, task)
            
            if is_rightful_owner:
                print(f"UPDATE: Found verified Backlog ID {backlog_id}. Checking for changes...")
                
                # Fetch full issue to get latest status (Reverse Sync)
                try:
                    latest_backlog_issue = self.load_balancer.get_issue(backlog_id)
                    
                    # --- REVERSE STATUS SYNC ---
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
                            self.ingestor.write_status(task['row_index'], mapped_status)
                except Exception as e:
                    print(f"WARNING: Could not fetch latest status for {backlog_id}: {e}")

                # --- CHANGE DETECTION (Sheet -> Backlog) ---
                if self.state.get(backlog_id) == current_hash:
                    print(f"SKIP: No content changes detected for {backlog_id}.")
                    return

                # If we reach here, content has changed.
                # Update local state so next run skips if still unchanged
                self.state[backlog_id] = current_hash

                # Generate Bilingual content, summary, and localized name
                full_desc, ai_summary, romaji_name = self._generate_bilingual_description(task)
                task['description'] = full_desc
                task['title_summary'] = ai_summary
                task['summary'] = f"[ERROR] {ai_summary} ({romaji_name} - #{task['id']})"

                # CALCULATE TIMELINE FOR UPDATES
                best_dev = self._find_best_dev(task['estimated_hours'])
                if best_dev:
                    due_date = self.timelines[best_dev['id']].fill_hours(task['estimated_hours'])
                    task['deadline'] = due_date
                    print(f"DEBUG: Calculated projected finish for verified update: {due_date}")
            else:
                print(f"ACTION: ID {backlog_id} appears to be a copy. Resetting to CREATE mode for this row.")
                backlog_id = None # Force creation of a fresh ticket
        
        if backlog_id: # This only executes if verified above
            if self.dry_run:
                print(f"[DRY RUN] Would update verified Backlog {backlog_id}")
                return
            try:
                self.load_balancer.update_backlog_issue(backlog_id, task)
                print(f"SUCCESS: Updated Backlog {backlog_id}")
                # Update local state
                self.state[backlog_id] = current_hash
            except Exception as e:
                print(f"ERROR: Failed to update {backlog_id}: {str(e)}")
            return

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
            
            print(f"ASSIGNING: Task {task['id']} (Req: {romaji_name}) ({task['estimated_hours']}h) -> {best_dev['name']}")
            print(f"TITLE PREVIEW: {task['summary']}")
            
            if self.dry_run:
                print(f"[DRY RUN] Would create Backlog Issue for {best_dev['name']} with deep-link and summary.")
                return
            try:
                issue = self.load_balancer.create_backlog_issue(best_dev['id'], task)
                issue_key = issue['issueKey']
                print(f"CREATED: Backlog Issue {issue_key}")
                self.ingestor.write_backlog_id(task['row_index'], issue_key)
                # Update local state
                self.state[issue_key] = current_hash
            except Exception as e:
                print(f"ERROR: Failed to create issue: {str(e)}")
        else:
            print(f"OVERLOAD: No capacity for Task {task['id']} even in 14-day window.")

    def _find_best_dev(self, hours):
        """Finds the dev with the lowest Today's usage, prioritizing Core."""
        core_options = []
        manager_option = None

        for name, dev_id in self.developer_map.items():
            timeline = self.timelines[dev_id]
            today_usage = timeline.get_today_usage()
            
            # Check if Today has any space at all
            if today_usage < self.load_balancer.DAILY_LIMIT_HOURS:
                option = {"name": name, "id": dev_id, "usage": today_usage}
                if name == "Choo":
                    manager_option = option
                else:
                    core_options.append(option)
        
        if core_options:
            return sorted(core_options, key=lambda x: x['usage'])[0]
        
        return manager_option

if __name__ == "__main__":
    manager = Orchestrator()
    manager.run()
