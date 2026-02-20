import os
import json
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

        if self.gemini_key:
            self.client = genai.Client(api_key=self.gemini_key)
            self.model_name = 'gemini-flash-latest'
        else:
            print("WARNING: GEMINI_API_KEY not found. Automated translation will be skipped.")
            self.client = None

        self.ingestor = CloudIngestor(self.google_json, self.sheet_id)
        self.load_balancer = LoadBalancer(self.backlog_key, self.space_id)
        
        # Real Developer Mapping for i-academy space
        self.developer_map = {
            "Saurabh": 984450,
            "Raman": 1819362,
            "Ewan": 1880127,
            "Choo": 1052465
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

        except Exception as e:
            import traceback
            print(f"CRITICAL ERROR: {str(e)}")
            traceback.print_exc()

    def _translate_and_summarize(self, text):
        """Uses Gemini to translate Japanese to English and generate a title."""
        if not self.client:
            # Fallback if no Gemini key
            snippet = text.replace('\n', ' ').strip()[:60] + "..."
            return snippet, snippet

        prompt = f"""
        You are a translation assistant for a software development team.
        Translate the following Japanese bug report/task description into professional English.
        The translation should be full-text and include all details.
        
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
            
            title = "Bug Report"
            translation = text
            
            if "TITLE:" in result and "TRANSLATION:" in result:
                title_part = result.split("TITLE:")[1].split("TRANSLATION:")[0].strip()
                translation_part = result.split("TRANSLATION:")[1].strip()
                return title_part, translation_part
                
            return title, translation
        except Exception as e:
            print(f"ERROR calling Gemini API: {e}")
            snippet = text.replace('\n', ' ').strip()[:60] + "..."
            return snippet, snippet

    def _generate_bilingual_description(self, task):
        """Constructs a bilingual description with deep links and automated translation."""
        # Constants for precision linking
        GID = "635134579"
        
        # Determine Title Summary and English Translation via Gemini
        title_summary, en_translation = self._translate_and_summarize(task['content'])
            
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
            
            # 1. Primary Check: Unique Task ID (e.g., "ID: 1")
            id_marker = f"ID: {task['id']}\n"
            if id_marker in desc:
                return True
                
            # 2. Secondary Check: Sheet Link range (e.g., "range=B20:C20")
            row_num = task['row_index'] + 1
            range_pattern = fr"range=B{row_num}:C{row_num}"
            if range_pattern in desc:
                return True
            
            print(f"⚠️ COLLISION DETECTED: {backlog_id} belongs to a different row (ID or Range mismatch).")
            return False
        except Exception as e:
            print(f"DEBUG: Could not verify ownership for {backlog_id} (might be deleted): {e}")
            return False

    def process_task(self, task):
        # Generate Bilingual content, summary, and localized name
        full_desc, ai_summary, romaji_name = self._generate_bilingual_description(task)
        task['description'] = full_desc
        task['title_summary'] = ai_summary
        task['summary'] = f"[ERROR] {ai_summary} ({romaji_name} - #{task['id']})"

        # 1. Update Detection & Ownership Verification
        backlog_id = task.get('backlog_id')
        if backlog_id:
            # NEW: Verify that this ID wasn't just copy-pasted from another row
            is_rightful_owner = self._verify_ownership(backlog_id, task)
            
            if is_rightful_owner:
                print(f"UPDATE: Found verified Backlog ID {backlog_id} (Req: {romaji_name}). Updating fields...")
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
            except Exception as e:
                print(f"ERROR: Failed to update {backlog_id}: {str(e)}")
            return

        # 2. Skip if already assigned in sheet
        if task.get('pic'):
            print(f"SKIP: Task {task['id']} already has PIC: {task['pic']}")
            return

        # 3. New Task Assignment Logic
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
