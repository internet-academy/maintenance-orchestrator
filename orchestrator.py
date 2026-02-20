import os
import json
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

        self.ingestor = CloudIngestor(self.google_json, self.sheet_id)
        self.load_balancer = LoadBalancer(self.backlog_key, self.space_id)
        
        # Real Developer Mapping for i-academy space
        self.developer_map = {
            "Saurabh": 984450,
            "Raman": 1819362,
            "Ewan": 1880127,
            "Choo": 1052465
        }
        
        # Initialize Timelines for all developers starting March 2nd
        self.start_date = "2026-03-02"
        self.timelines = {}
        for name, dev_id in self.developer_map.items():
            # For this run, we start fresh on March 2nd as core team is busy until then
            timeline = DeveloperTimeline(name, start_date=self.start_date)
            self.timelines[dev_id] = timeline

    def run(self):
        print(f"--- Starting Orchestration: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        
        print(f"\n--- Team Capacity Map (Starting {self.start_date}) ---")
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

    def _generate_bilingual_description(self, task):
        """Constructs a bilingual description with deep links."""
        # Simple summary logic: first 50 chars of content
        # In a real run, this would be an LLM-refined summary.
        clean_content = task['content'].replace('\n', ' ').strip()
        summary = clean_content[:60] + "..." if len(clean_content) > 60 else clean_content
        
        sheet_url = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/edit#gid={task.get('gid', 0)}&range=A{task['row_index']+1}"
        
        description = f"## English Summary\n{summary}\n\n"
        description += f"## Reference Links\n- **Original Sheet Row**: [Click here to view in Google Sheets]({sheet_url})\n"
        if task.get('chat_url'):
            description += f"- **Google Chat**: [View conversation]({task['chat_url']})\n"
        
        description += f"\n## 原文 (Japanese)\n{task['content']}"
        return description, summary

    def process_task(self, task):
        # Generate Bilingual content and summary for title
        full_desc, ai_summary = self._generate_bilingual_description(task)
        task['description'] = full_desc
        # Informative title
        task['title_summary'] = ai_summary

        # 1. Update Detection Logic
        backlog_id = task.get('backlog_id')
        if backlog_id:
            print(f"UPDATE: Found existing Backlog ID {backlog_id}. Updating fields...")
            
            # WE MUST STILL CALCULATE THE TIMELINE FOR EXISTING TASKS
            best_dev = self._find_best_dev(task['estimated_hours'])
            if best_dev:
                due_date = self.timelines[best_dev['id']].fill_hours(task['estimated_hours'])
                task['deadline'] = due_date
                print(f"DEBUG: Calculated projected finish for update: {due_date}")
            
            if self.dry_run:
                print(f"[DRY RUN] Would update Backlog {backlog_id} with informative description.")
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
            
            print(f"ASSIGNING: Task {task['id']} (Req: {task['requester']}) ({task['estimated_hours']}h) -> {best_dev['name']}")
            print(f"TITLE PREVIEW: [ERROR] {ai_summary} ({task['requester']} - #{task['id']})")
            
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
