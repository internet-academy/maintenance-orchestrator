import os
import json
from parsers.error_report_parser import ErrorReportParser
from agents.load_balancer import LoadBalancer

class Orchestrator:
    def __init__(self, config):
        self.config = config
        self.parser = ErrorReportParser(config['CSV_DIR'])
        self.load_balancer = LoadBalancer(config['BACKLOG_API_KEY'], config['BACKLOG_SPACE_ID'])
        
        # Mapping developer names to their Backlog User IDs
        # In a real setup, these would be in a config file or environment variables
        self.developer_map = {
            "Saurabh": 101,
            "Raman": 102,
            "Ewan": 103,
            "Choo": 104
        }

    def process_new_tasks(self):
        """Main loop to parse, check load, and assign tasks."""
        latest_file = self.parser.get_latest_file()
        if not latest_file:
            print("No new CSV file found to process.")
            return

        tasks = self.parser.parse_file(latest_file)
        print(f"--- Processing {len(tasks)} tasks from {os.path.basename(latest_file)} ---
")

        for task in tasks:
            # Step 1: Check if task already has a PIC assigned in the sheet
            assigned_pic = task.get('pic')
            
            if not assigned_pic:
                # Step 2: Auto-assign logic
                best_match = self._find_available_developer(task['estimated_hours'])
                
                if best_match:
                    print(f"MATCH: Task ID {task['id']} ({task['estimated_hours']}h) -> Assigned to {best_match['name']}")
                    print(f"       New Projected Load: {best_match['projected_load']}h
")
                    # In production: self.load_balancer.assign_task(best_match['id'], task)
                else:
                    print(f"ALERT: Task ID {task['id']} ({task['estimated_hours']}h) - NO DEVELOPER HAS CAPACITY TODAY.
")
            else:
                print(f"SKIP: Task ID {task['id']} already assigned to {assigned_pic}.
")

    def _find_available_developer(self, task_hours):
        """Iterates through developers to find one who can take the load."""
        for name, dev_id in self.developer_map.items():
            # Real call to Backlog API (Mocked in this prototype)
            # result = self.load_balancer.can_assign_task(dev_id, task_hours)
            
            # MOCK LOGIC: Simulating a 4-hour current load for testing
            mock_current_load = 4.0 
            projected_load = mock_current_load + task_hours
            
            if projected_load <= 6.0:
                return {
                    "name": name,
                    "id": dev_id,
                    "projected_load": projected_load
                }
        return None

if __name__ == "__main__":
    # Configuration (Placeholders)
    CONFIG = {
        "CSV_DIR": "/home/min/ia/mini-projects",
        "BACKLOG_API_KEY": "PLACEHOLDER_KEY",
        "BACKLOG_SPACE_ID": "PLACEHOLDER_SPACE"
    }

    orchestrator = Orchestrator(CONFIG)
    orchestrator.process_new_tasks()
