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
        
        # Initialize Timelines for all developers
        self.timelines = {}
        for name, dev_id in self.developer_map.items():
            timeline = DeveloperTimeline(name)
            # Pre-fill with actual Backlog load (last 7 days)
            actual_load = self.load_balancer.get_active_workload(dev_id, project_id=528169)
            timeline.fill_hours(actual_load)
            self.timelines[dev_id] = timeline

    def run(self):
        print(f"--- Starting Orchestration: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        
        print("\n--- Current Team Load (Initial State) ---")
        for name, dev_id in self.developer_map.items():
            usage = self.timelines[dev_id].get_today_usage()
            print(f"- {name}: {usage}h / {self.load_balancer.DAILY_LIMIT_HOURS}h limit today")
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

    def process_task(self, task):
        # 1. Update Detection Logic
        backlog_id = task.get('backlog_id')
        if backlog_id:
            print(f"UPDATE: Found existing Backlog ID {backlog_id}. Updating fields...")
            if self.dry_run:
                print(f"[DRY RUN] Would update Backlog {backlog_id}")
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
            print(f"PROJECTED FINISH: {due_date}")
            
            if self.dry_run:
                print(f"[DRY RUN] Would create Backlog Issue for {best_dev['name']} with DueDate: {due_date}")
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
