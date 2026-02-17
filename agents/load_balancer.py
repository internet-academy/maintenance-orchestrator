import requests
import os
from datetime import datetime

class LoadBalancer:
    def __init__(self, api_key, space_id):
        self.api_key = api_key
        self.base_url = f"https://{space_id}.backlog.com/api/v2"
        self.DAILY_LIMIT_HOURS = 6.0

    def get_active_workload(self, user_id):
        """
        Fetches all issues assigned to a user that are NOT closed/merged
        and sums their estimated hours.
        """
        endpoint = f"{self.base_url}/issues"
        params = {
            "apiKey": self.api_key,
            "assigneeId[]": [user_id],
            "statusId[]": [1, 2, 3], # 1: Open, 2: In Progress, 3: Resolved (Pending Release)
        }
        
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        issues = response.json()
        
        total_hours = sum(float(issue.get("estimatedHours") or 0) for issue in issues)
        return total_hours

    def can_assign_task(self, user_id, task_estimated_hours):
        """
        Determines if a developer can take on a new task based on the 6-hour rule.
        """
        current_load = self.get_active_workload(user_id)
        projected_load = current_load + float(task_estimated_hours)
        
        can_accept = projected_load <= self.DAILY_LIMIT_HOURS
        
        return {
            "can_accept": can_accept,
            "current_load": current_load,
            "projected_load": projected_load,
            "remaining_capacity": self.DAILY_LIMIT_HOURS - current_load
        }

# --- Example Usage (Mocked) ---
if __name__ == "__main__":
    # These would be your environment variables
    API_KEY = "your_backlog_api_key"
    SPACE_ID = "your_workspace_name"
    
    # Example Developer ID (Backlog User ID)
    DEV_ID = 12345
    NEW_TASK_ESTIMATE = 1.5
    
    # In a real scenario, this would be triggered by the 'Ingestor' agent
    lb = LoadBalancer(API_KEY, SPACE_ID)
    
    # result = lb.can_assign_task(DEV_ID, NEW_TASK_ESTIMATE)
    # print(f"Can Assign: {result['can_accept']} (Projected Load: {result['projected_load']}h)")
    
    print("Load Balancer Prototype initialized with 6-hour daily limit logic.")
