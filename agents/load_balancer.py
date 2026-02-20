import requests
import os
import holidays
from datetime import datetime, timedelta

class DeveloperTimeline:
    def __init__(self, name, daily_limit=6.0, days_count=14, start_date=None):
        self.name = name
        self.daily_limit = daily_limit
        self.buckets = [] # List of {'date': date, 'used': hours, 'remaining': hours}
        
        # Initialize Japanese holidays
        jp_holidays = holidays.Japan()
        
        if start_date:
            current = datetime.strptime(start_date, "%Y-%m-%d")
        else:
            current = datetime.now()

        while len(self.buckets) < days_count:
            # Skip weekends (5: Sat, 6: Sun) AND Japanese public holidays
            is_holiday = current.strftime("%Y-%m-%d") in jp_holidays
            if current.weekday() < 5 and not is_holiday:
                self.buckets.append({
                    'date': current.strftime("%Y-%m-%d"),
                    'used': 0.0,
                    'remaining': daily_limit
                })
            elif is_holiday:
                print(f"DEBUG: {name}'s timeline skipping Japanese Holiday: {current.strftime('%Y-%m-%d')} ({jp_holidays.get(current)})")
            
            current += timedelta(days=1)

    def fill_hours(self, hours):
        """Pours hours into buckets sequentially. Returns the completion date or None if overloaded."""
        remaining_to_pour = float(hours)
        last_date = None
        
        for bucket in self.buckets:
            if remaining_to_pour <= 0:
                break
            
            can_take = min(remaining_to_pour, bucket['remaining'])
            if can_take > 0:
                bucket['used'] += can_take
                bucket['remaining'] -= can_take
                remaining_to_pour -= can_take
                last_date = bucket['date']
        
        if remaining_to_pour > 0:
            return None # Could not fit in 14 days
            
        return last_date or self.buckets[0]['date']

    def get_today_usage(self):
        return self.buckets[0]['used']

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
        Legacy method.
        """
        current_load = self.get_active_workload(user_id)
        projected_load = current_load + float(task_estimated_hours)
        can_accept = projected_load <= self.DAILY_LIMIT_HOURS
        return {"can_accept": can_accept, "current_load": current_load}

    def update_backlog_issue(self, issue_id_or_key, task_data):
        """
        Updates an existing issue in Backlog.
        """
        endpoint = f"{self.base_url}/issues/{issue_id_or_key}"
        params = {"apiKey": self.api_key}
        
        payload = {
            "estimatedHours": task_data.get('estimated_hours'),
            "dueDate": task_data.get('deadline', '')
        }
        # Only include fields that are present to avoid clearing data
        payload = {k: v for k, v in payload.items() if v is not None}
        
        response = requests.patch(endpoint, params=params, data=payload)
        response.raise_for_status()
        return response.json()

    def create_backlog_issue(self, user_id, task_data):
        """
        Creates a new issue in Backlog.
        """
        endpoint = f"{self.base_url}/issues"
        params = {"apiKey": self.api_key}
        
        # Mapping the Ingestor's task data to Backlog's API fields
        payload = {
            "projectId": 528169, # System Development (MD_SD)
            "summary": f"[ERROR] {task_data['requester']} - {task_data['id']}",
            "description": f"Page: {task_data.get('page_url', 'N/A')}\n\nContent:\n{task_data['content']}\n\nChat URL: {task_data.get('chat_url', 'N/A')}",
            "issueTypeId": 2750765, # バグ (MD_SD Project specific)
            "priorityId": 3,  # Normal
            "assigneeId": user_id,
            "estimatedHours": task_data['estimated_hours'],
            "dueDate": task_data.get('deadline', '')
        }
        
        response = requests.post(endpoint, params=params, data=payload)
        response.raise_for_status()
        return response.json()
