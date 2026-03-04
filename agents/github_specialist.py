import os
import requests
import json
import re
from datetime import datetime, timedelta

class GitHubSpecialist:
    def __init__(self, token, org="internet-academy", dry_run=False):
        self.token = token
        self.org = org
        self.dry_run = dry_run
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        }
        self.graphql_url = "https://api.github.com/graphql"
        
        # Project Configurations
        self.projects = {
            3: {
                "id": "PVT_kwDOA1jKuM4BQoor",
                "fields": {
                    "status": "PVTSSF_lADOA1jKuM4BQoorzg-spXY",
                    "project": "PVTSSF_lADOA1jKuM4BQoorzg-tC7Q"
                },
                "options": {
                    "project_maintenance": "47686791"
                }
            },
            4: {
                "id": "PVT_kwDOA1jKuM4BQoql",
                "fields": {
                    "status": "PVTSSF_lADOA1jKuM4BQoqlzg-squM",
                    "start_date": "PVTF_lADOA1jKuM4BQoqlzg-sq_Q",
                    "end_date": "PVTF_lADOA1jKuM4BQoqlzg-sq_U",
                    "finish_date": "PVTF_lADOA1jKuM4BQoqlzg-s8Hg",
                    "hours": "PVTF_lADOA1jKuM4BQoqlzg-sq_I",
                    "priority": "PVTSSF_lADOA1jKuM4BQoqlzg-sq_A",
                    "level": "PVTSSF_lADOA1jKuM4BQoqlzg-svGQ",
                    "parent_issue": "PVTF_lADOA1jKuM4BQoqlzg-squo"
                },
                "options": {
                    "status_to_triage": "23799a6c",
                    "status_in_progress": "47fc9ee4",
                    "status_done": "98236657",
                    "priority_p0": "79628723",
                    "priority_p1": "0a877460",
                    "priority_p2": "da944a9c",
                    "level_parent": "bae6dbb7",
                    "level_child": "8c0ea3a0"
                }
            }
        }

    def create_issue(self, repo, title, body, assignee=None, labels=None):
        """Creates a GitHub Issue and optionally assigns it."""
        url = f"https://api.github.com/repos/{self.org}/{repo}/issues"
        payload = {"title": title, "body": body}
        if assignee: payload["assignees"] = [assignee]
        if labels: payload["labels"] = labels

        if self.dry_run:
            print(f"[DRY RUN] Would create GitHub issue in {repo}: {title}")
            return {"number": 2500, "html_url": f"https://github.com/{self.org}/{repo}/issues/2500", "node_id": "MOCK_NODE_ID"}

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def add_to_project(self, node_id, project_number):
        """Adds a content node (Issue/PR) to a specific project number."""
        project_id = self.projects[project_number]["id"]
        if self.dry_run:
            print(f"[DRY RUN] Would add node {node_id} to Project {project_number}")
            return "MOCK_ITEM_ID"

        query = """
        mutation($project: ID!, $content: ID!) {
          addProjectV2ItemById(input: {projectId: $project, contentId: $content}) {
            item { id }
          }
        }
        """
        vars = {"project": project_id, "content": node_id}
        response = requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": vars})
        response.raise_for_status()
        return response.json()["data"]["addProjectV2ItemById"]["item"]["id"]

    def update_field(self, project_number, item_id, field_key, value, is_option=False):
        """Updates a field in a project."""
        project_id = self.projects[project_number]["id"]
        field_id = self.projects[project_number]["fields"].get(field_key)
        if not field_id: return

        if self.dry_run:
            print(f"[DRY RUN] Project {project_number} update: {field_key} -> {value}")
            return

        mutation = """
        mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {
          updateProjectV2ItemFieldValue(input: {
            projectId: $project, itemId: $item, fieldId: $field,
            value: { %VALUE_TYPE%: $value }
          }) { clientMutationId }
        }
        """
        v_type = "singleSelectOptionId" if is_option else ("date" if "-" in str(value) and len(str(value)) == 10 else "text")
        if not is_option and isinstance(value, (int, float)): v_type = "number"
        
        query = mutation.replace("%VALUE_TYPE%", v_type)
        variables = {"project": project_id, "item": item_id, "field": field_id, "value": str(value) if v_type != "number" else value}
        
        response = requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": variables})
        response.raise_for_status()

    def get_project_item_data(self, issue_number, project_number=4):
        """Fetches all project field values for a specific issue number."""
        project_id = self.projects[project_number]["id"]
        query = """
        query($org: String!, $project_number: Int!) {
          organization(login: $org) {
            projectV2(number: $project_number) {
              items(first: 100) {
                nodes {
                  id
                  fieldValues(first: 20) {
                    nodes {
                      ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2Field { name id } } }
                      ... on ProjectV2ItemFieldNumberValue { number field { ... on ProjectV2Field { name id } } }
                      ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2Field { name id } } }
                      ... on ProjectV2ItemFieldDateValue { date field { ... on ProjectV2Field { name id } } }
                    }
                  }
                  content { ... on Issue { number assignees(first: 1) { nodes { login } } } }
                }
              }
            }
          }
        }
        """
        response = requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": {"org": self.org, "project_number": project_number}})
        items = response.json().get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {}).get('nodes', [])
        
        for item in items:
            content = item.get('content')
            if content and content.get('number') == issue_number:
                data = {'item_id': item['id'], 'assignee': content.get('assignees', {}).get('nodes', [{}])[0].get('login')}
                for fv in item.get('fieldValues', {}).get('nodes', []):
                    name = fv.get('field', {}).get('name')
                    val = fv.get('text') or fv.get('number') or fv.get('name') or fv.get('date')
                    data[name] = val
                return data
        return None

    def get_active_workload(self, github_username):
        """Fetches active issues for a user in Project 4 and sums their 'Assigned Hours'."""
        project_id = self.projects[4]["id"]
        query = """
        query($org: String!, $number: Int!) {
          organization(login: $org) {
            projectV2(number: $number) {
              items(first: 100) {
                nodes {
                  fieldValues(first: 20) {
                    nodes {
                      ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2Field { id name } } }
                      ... on ProjectV2ItemFieldNumberValue { number field { ... on ProjectV2Field { id name } } }
                      ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2Field { id name } } }
                    }
                  }
                  content {
                    ... on Issue { assignees(first: 10) { nodes { login } } closed }
                    ... on DraftIssue { assignees(first: 10) { nodes { login } } }
                  }
                }
              }
            }
          }
        }
        """
        response = requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": {"org": self.org, "number": 4}})
        data = response.json()
        items = data.get("data", {}).get("organization", {}).get("projectV2", {}).get("items", {}).get("nodes", [])
        
        load = 0.0
        target_field_id = self.projects[4]["fields"]["hours"]
        for item in items:
            content = item.get("content", {})
            if not content or content.get("closed") is True: continue
            assignees = [a["login"].lower() for a in content.get("assignees", {}).get("nodes", [])]
            if github_username.lower() not in assignees: continue
            
            hours = 0.0
            is_done = False
            for fv in item.get("fieldValues", {}).get("nodes", []):
                field_data = fv.get("field", {})
                if field_data.get("id") == target_field_id or field_data.get("name") == "Assigned Hours":
                    hours = float(fv.get("number") or fv.get("text") or 0.0)
                if field_data.get("name") == "Status" and fv.get("name") == "Done": is_done = True
            if not is_done: load += hours
        return load

    def get_issue_status(self, issue_url):
        match = re.search(r'github\.com/([^/]+)/([^/]+)/issues/(\d+)', issue_url)
        if not match: return "Unknown"
        owner, repo, number = match.groups()
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/issues/{number}", headers=self.headers)
        if response.status_code != 200: return "Unknown"
        return "Closed" if response.json().get("state") == "closed" else "Open"
