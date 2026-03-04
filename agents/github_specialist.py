import os
import requests
import json
import re
from datetime import datetime, timedelta

class GitHubSpecialist:
    def __init__(self, token, org="internet-academy", project_number=4, dry_run=False):
        self.token = token
        self.org = org
        self.project_number = project_number
        self.dry_run = dry_run
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        }
        self.graphql_url = "https://api.github.com/graphql"
        
        # Project IDs (Cached from research)
        self.project_id = "PVT_kwDOA1jKuM4BQoql"
        self.field_ids = {
            "status": "PVTSSF_lADOA1jKuM4BQoqlzg-squM",
            "start_date": "PVTF_lADOA1jKuM4BQoqlzg-sq_Q",
            "end_date": "PVTF_lADOA1jKuM4BQoqlzg-sq_U",
            "finish_date": "PVTF_lADOA1jKuM4BQoqlzg-s8Hg",
            "hours": "PVTF_lADOA1jKuM4BQoqlzg-sq_I"
        }
        self.status_options = {
            "In progress": "47fc9ee4",
            "Done": "98236657",
            "To Triage": "23799a6c"
        }

    def create_issue(self, repo, title, body, assignee=None, labels=None):
        """Creates a GitHub Issue and optionally assigns it."""
        url = f"https://api.github.com/repos/{self.org}/{repo}/issues"
        payload = {
            "title": title,
            "body": body,
        }
        if assignee:
            payload["assignees"] = [assignee]
        if labels:
            payload["labels"] = labels

        if self.dry_run:
            print(f"[DRY RUN] Would create GitHub issue in {repo}: {title}")
            return {"number": 999, "html_url": f"https://github.com/{self.org}/{repo}/issues/999", "node_id": "MOCK_NODE_ID"}

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def add_to_project(self, issue_node_id):
        """Adds a GitHub Issue to ProjectV2."""
        if self.dry_run:
            print(f"[DRY RUN] Would add node {issue_node_id} to Project {self.project_id}")
            return "MOCK_ITEM_ID"

        query = """
        mutation($project: ID!, $content: ID!) {
          addProjectV2ItemById(input: {projectId: $project, contentId: $content}) {
            item { id }
          }
        }
        """
        variables = {"project": self.project_id, "content": issue_node_id}
        response = requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": variables})
        response.raise_for_status()
        data = response.json()
        return data["data"]["addProjectV2ItemById"]["item"]["id"]

    def update_project_field(self, item_id, field_id, value, is_option=False):
        """Updates a field in ProjectV2 (Text, Date, or SingleSelect)."""
        if self.dry_run:
            print(f"[DRY RUN] Would update item {item_id} field {field_id} to {value}")
            return

        mutation = """
        mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {
          updateProjectV2ItemFieldValue(input: {
            projectId: $project,
            itemId: $item,
            fieldId: $field,
            value: { text: $value }
          }) { clientMutationId }
        }
        """
        if is_option:
             mutation = mutation.replace("text: $value", "singleSelectOptionId: $value")
        elif "-" in str(value) and len(str(value)) == 10: # Date format YYYY-MM-DD
             mutation = mutation.replace("text: $value", "date: $value")

        variables = {"project": self.project_id, "item": item_id, "field": field_id, "value": str(value)}
        response = requests.post(self.graphql_url, headers=self.headers, json={"query": mutation, "variables": variables})
        response.raise_for_status()

    def get_active_workload(self, github_username):
        """
        Fetches active issues for a user in Project 4 and sums their 'Assigned Hours'.
        """
        query = """
        query($org: String!, $number: Int!) {
          organization(login: $org) {
            projectV2(number: $number) {
              items(first: 100) {
                nodes {
                  fieldValues(first: 20) {
                    nodes {
                      ... on ProjectV2ItemFieldTextValue { 
                        text 
                        field { ... on ProjectV2Field { id name } } 
                      }
                      ... on ProjectV2ItemFieldNumberValue { 
                        number 
                        field { ... on ProjectV2Field { id name } } 
                      }
                      ... on ProjectV2ItemFieldSingleSelectValue { 
                        name 
                        field { ... on ProjectV2Field { id name } } 
                      }
                    }
                  }
                  content {
                    ... on Issue {
                      assignees(first: 10) { nodes { login } }
                      closed
                    }
                    ... on DraftIssue {
                      assignees(first: 10) { nodes { login } }
                    }
                  }
                }
              }
            }
          }
        }
        """
        variables = {"org": self.org, "number": self.project_number}
        response = requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": variables})
        response.raise_for_status()
        data = response.json()
        
        items = data.get("data", {}).get("organization", {}).get("projectV2", {}).get("items", {}).get("nodes", [])
        
        active_load = 0.0
        target_field_id = self.field_ids['hours'] # PVTF_lADOA1jKuM4BQoqlzg-sq_I
        
        for item in items:
            content = item.get("content", {})
            # Skip if content is missing or issue is explicitly closed
            if not content or content.get("closed") is True:
                continue
                
            assignees = [a["login"] for a in content.get("assignees", {}).get("nodes", [])]
            # Match case-insensitive for safety
            if github_username.lower() not in [a.lower() for a in assignees]:
                continue
            
            # Extract hours from the specific field ID
            hours = 0.0
            is_done = False
            
            for fv in item.get("fieldValues", {}).get("nodes", []):
                field_data = fv.get("field", {})
                field_id = field_data.get("id")
                field_name = field_data.get("name")
                
                # Check Hours (Target by ID or exact Name)
                if field_id == target_field_id or field_name == "Assigned Hours":
                    try:
                        # Try 'number' first, then fallback to 'text'
                        val = fv.get("number")
                        if val is not None:
                            hours = float(val)
                        else:
                            hours = float(fv.get("text", "0.0"))
                    except (ValueError, TypeError):
                        hours = 0.0
                
                # Check if Status is 'Done' (to skip)
                if (field_id == self.field_ids['status'] or field_name == "Status") and fv.get("name") == "Done":
                    is_done = True
            
            if not is_done:
                active_load += hours
            
        return active_load

    def get_issue_status(self, issue_url):
        """Fetches the current status of an issue (Open/Closed) and its linked PRs."""
        # Extract repo and number from URL
        match = re.search(r'github\.com/([^/]+)/([^/]+)/issues/(\d+)', issue_url)
        if not match:
            return "Unknown"
        
        owner, repo, number = match.groups()
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{number}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            return "Unknown"
            
        issue_data = response.json()
        if issue_data.get("state") == "closed":
            return "Closed"
            
        # Check for linked PRs (This is complex via REST, but we can look for 'In Progress' logic)
        return "Open"
