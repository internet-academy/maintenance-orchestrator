import os
import json
from agents.cloud_ingestor import CloudIngestor
from agents.load_balancer import LoadBalancer
from datetime import datetime

class Orchestrator:
    def __init__(self, dry_run=False):
        # Load from Environment Variables (set by GitHub Secrets)
        self.dry_run = dry_run
        if self.dry_run:
            print("!!! RUNNING IN DRY RUN MODE - NO API MUTATIONS WILL OCCUR !!!")
        
        self.google_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
        self.backlog_key = os.getenv('BACKLOG_API_KEY')
        self.space_id = os.getenv('BACKLOG_SPACE_ID')

        self.ingestor = CloudIngestor(self.google_json, self.sheet_id)
        self.load_balancer = LoadBalancer(self.backlog_key, self.space_id)
        
        # In-memory tracking for this specific run to prevent over-assignment
        self.session_load = {} # { dev_id: running_total_hours }

        # Real Developer Mapping for i-academy space
        self.developer_map = {
            "Saurabh": 984450,
            "Raman": 1819362,
            "Ewan": 1880127,
            "Choo": 1052465
        }

    def run(self):
        print(f"--- Starting Orchestration: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        
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
                print(f"[DRY RUN] Would update Backlog {backlog_id} with {task['estimated_hours']}h")
                return
            try:
                self.load_balancer.update_backlog_issue(backlog_id, task)
                print(f"SUCCESS: Updated Backlog {backlog_id}")
            except Exception as e:
                print(f"ERROR: Failed to update {backlog_id}: {str(e)}")
            return

        # 2. Skip if already assigned in sheet (Legacy check)
        if task.get('pic'):
            print(f"SKIP: Task {task['id']} already has PIC: {task['pic']}")
            return

        # 3. New Task Assignment Logic
        best_dev = self._find_best_dev(task['estimated_hours'])
        
        if best_dev:
            print(f"ASSIGNING: Task {task['id']} ({task['estimated_hours']}h) -> {best_dev['name']}")
            if self.dry_run:
                print(f"[DRY RUN] Would create Backlog Issue for {best_dev['name']} and write back to sheet.")
                return
            try:
                issue = self.load_balancer.create_backlog_issue(best_dev['id'], task)
                issue_key = issue['issueKey']
                print(f"CREATED: Backlog Issue {issue_key}")
                
                # Write back to Sheet
                self.ingestor.write_backlog_id(task['row_index'], issue_key)
                print(f"SYNC: Wrote {issue_key} back to Google Sheet row {task['row_index']}")
            except Exception as e:
                print(f"ERROR: Failed to create issue for task {task['id']}: {str(e)}")
        else:
            print(f"OVERLOAD: No capacity for Task {task['id']} ({task['estimated_hours']}h) today.")

    def _get_dev_session_load(self, dev_id):
        """Gets current load from API + what we've assigned this session."""
        if dev_id not in self.session_load:
            # First time this run: get actual load from Backlog API
            try:
                actual_load = self.load_balancer.get_active_workload(dev_id)
            except:
                actual_load = 0.0 # Fallback
            self.session_load[dev_id] = actual_load
            
        return self.session_load[dev_id]

    def _find_best_dev(self, hours):
        """Finds the dev with the lowest current load who is under the 6h limit."""
        options = []
        for name, dev_id in self.developer_map.items():
            current_total = self._get_dev_session_load(dev_id)
            projected = current_total + float(hours)
            
            if projected <= self.load_balancer.DAILY_LIMIT_HOURS:
                options.append({
                    "name": name, 
                    "id": dev_id, 
                    "load": current_total
                })
        
        # Sort by current load (ascending) to balance the team
        if options:
            best = sorted(options, key=lambda x: x['load'])[0]
            # Update in-memory load for the NEXT task in this run
            self.session_load[best['id']] += float(hours)
            print(f"DEBUG: {best['name']} running load: {self.session_load[best['id']]}h")
            return best
        return None

if __name__ == "__main__":
    manager = Orchestrator()
    manager.run()
