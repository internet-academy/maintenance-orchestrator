import requests
import os
from datetime import datetime

class LoadBalancer:
    def __init__(self, api_key, space_id):
        self.api_key = api_key
        self.base_url = f"https://{space_id}.backlog.com/api/v2"
        self.DAILY_LIMIT_HOURS = 6.0

    def get_active_workload(self, user_id, project_id=None):
        """
        Fetches active issues updated in the last 7 days and sums their estimated hours.
        """
        endpoint = f"{self.base_url}/issues"
        
        # Calculate date for 7 days ago
        from datetime import datetime, timedelta
        seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        params = {
            "apiKey": self.api_key,
            "assigneeId[]": [user_id],
            "statusId[]": [1, 2], # 1: Open, 2: In Progress
            "updatedSince": seven_days_ago
        }
        if project_id:
            params["projectId[]"] = [project_id]
        
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

    def update_backlog_issue(self, issue_id_or_key, task_data):
        """
        Updates an existing issue in Backlog.
        """
        endpoint = f"{self.base_url}/issues/{issue_id_or_key}"
        
        payload = {
            "apiKey": self.api_key,
            "estimatedHours": task_data.get('estimated_hours'),
            "dueDate": task_data.get('deadline', '')
        }
        # Only include fields that are present to avoid clearing data
        payload = {k: v for k, v in payload.items() if v is not None}
        
        response = requests.patch(endpoint, data=payload)
        response.raise_for_status()
        return response.json()

    def create_backlog_issue(self, user_id, task_data):
        """
        Creates a new issue in Backlog.
        """
        endpoint = f"{self.base_url}/issues"
        
        # Mapping the Ingestor's task data to Backlog's API fields
        payload = {
            "apiKey": self.api_key,
            "projectId": self._get_project_id(), # We need to define which project this goes to
            "summary": f"[ERROR] {task_data['requester']} - {task_data['date']}",
            "description": f"Page: {task_data.get('page_url', 'N/A')}\n\nContent:\n{task_data['content']}\n\nChat URL: {task_data.get('chat_url', 'N/A')}",
            "issueTypeId": 1, # Usually 'Bug' or 'Task' - check your project settings
            "priorityId": 3,  # Normal
            "assigneeId": user_id,
            "estimatedHours": task_data['estimated_hours'],
            "dueDate": task_data.get('deadline', '')
        }
        
        response = requests.post(endpoint, data=payload)
        response.raise_for_status()
        return response.json()

    def _get_project_id(self):
        # You'll need the numeric ID of your Backlog Project
        # You can find this in your Project Settings or I can help you find it.
        return os.getenv('BACKLOG_PROJECT_ID', '12345')

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
