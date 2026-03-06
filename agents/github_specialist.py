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
                    "project": "PVTSSF_lADOA1jKuM4BQoorzg-tC7Q",
                    "start_date": "PVTF_lADOA1jKuM4BQoorzg-xYWY",
                    "end_date": "PVTF_lADOA1jKuM4BQoorzg-xYWs"
                },
                "options": {
                    "project_maintenance": "109c057b",
                    "project_new_dev": "a87ad165"
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
        url = f"https://api.github.com/repos/{self.org}/{repo}/issues"
        payload = {"title": title, "body": body}
        if assignee: payload["assignees"] = [assignee]
        if labels: payload["labels"] = labels
        if self.dry_run:
            print(f"[DRY RUN] Creating issue: {title}")
            return {"number": 2500, "html_url": "mock_url", "node_id": "MOCK_NODE_ID"}
        r = requests.post(url, headers=self.headers, json=payload)
        r.raise_for_status()
        return r.json()

    def add_to_project(self, node_id, project_number):
        project_id = self.projects[project_number]["id"]
        if self.dry_run: return "MOCK_ITEM_ID"
        query = "mutation($project: ID!, $content: ID!) { addProjectV2ItemById(input: {projectId: $project, contentId: $content}) { item { id } } }"
        r = requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": {"project": project_id, "content": node_id}})
        r.raise_for_status()
        return r.json()["data"]["addProjectV2ItemById"]["item"]["id"]

    def update_field(self, project_number, item_id, field_key, value, is_option=False):
        project_id = self.projects[project_number]["id"]
        field_id = self.projects[project_number]["fields"].get(field_key)
        if not field_id or self.dry_run: return
        v_key = "singleSelectOptionId" if is_option else ("date" if "-" in str(value) and len(str(value)) == 10 else ("number" if isinstance(value, (int, float)) else "text"))
        val_type = "Float" if v_key == "number" else "String"
        mutation = f"mutation($project: ID!, $item: ID!, $field: ID!, $value: {val_type}!) {{ updateProjectV2ItemFieldValue(input: {{ projectId: $project, itemId: $item, fieldId: $field, value: {{ {v_key}: $value }} }}) {{ clientMutationId }} }}"
        r = requests.post(self.graphql_url, headers=self.headers, json={"query": mutation, "variables": {"project": project_id, "item": item_id, "field": field_id, "value": value if v_key == "number" else str(value)}})
        r.raise_for_status()

    def link_subissue(self, parent_node_id, child_node_id):
        if self.dry_run: return
        query = "mutation($parent: ID!, $child: ID!) { addSubIssue(input: {issueId: $parent, subIssueId: $child}) { parentIssue { id } } }"
        requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": {"parent": parent_node_id, "child": child_node_id}}).raise_for_status()

    def get_issue_node_id(self, repo, number):
        r = requests.get(f"https://api.github.com/repos/{self.org}/{repo}/issues/{number}", headers=self.headers)
        r.raise_for_status()
        return r.json()['node_id']

    def get_project_item_data(self, issue_number, project_number=4):
        query = "query($org: String!, $number: Int!) { organization(login: $org) { projectV2(number: $number) { items(first: 100) { nodes { id fieldValues(first: 20) { nodes { ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2Field { name id } } } ... on ProjectV2ItemFieldNumberValue { number field { ... on ProjectV2Field { name id } } } ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2Field { name id } } } ... on ProjectV2ItemFieldDateValue { date field { ... on ProjectV2Field { name id } } } } } content { ... on Issue { number assignees(first: 1) { nodes { login } } } } } } } } }"
        r = requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": {"org": self.org, "number": project_number}})
        items = r.json().get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {}).get('nodes', [])
        for item in items:
            content = item.get('content')
            if content and content.get('number') == issue_number:
                data = {'item_id': item['id'], 'assignee': content.get('assignees', {}).get('nodes', [{}])[0].get('login')}
                for fv in item.get('fieldValues', {}).get('nodes', []):
                    name = fv.get('field', {}).get('name')
                    val = fv.get('text') or fv.get('number') or fv.get('name') or fv.get('date')
                    if name: data[name] = val
                return data
        return None

    def get_active_workload(self, github_username):
        tasks = self.get_full_active_tasks()
        load = 0.0
        for t in tasks:
            if t['assignee'] and t['assignee'].lower() == github_username.lower():
                load += t.get('hours', 0.0)
        return load

    def get_full_active_tasks(self):
        """Fetches all active parent tasks across key projects with simplified robust logic."""
        active_tasks = []
        unique_ids = set()
        
        # We target the most critical projects by number
        for p_num in [3, 4]:
            query = """
            query($org: String!, $number: Int!) {
              organization(login: $org) {
                projectV2(number: $number) {
                  title
                  items(first: 100) {
                    nodes {
                      id
                      isArchived
                      content {
                        ... on Issue { id number title url closed assignees(first: 1) { nodes { login } } }
                        ... on PullRequest { id number title url closed assignees(first: 1) { nodes { login } } }
                      }
                      fieldValues(first: 20) {
                        nodes {
                          ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2Field { name } } }
                          ... on ProjectV2ItemFieldNumberValue { number field { ... on ProjectV2Field { name } } }
                          ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2Field { name } } }
                          ... on ProjectV2ItemFieldDateValue { date field { ... on ProjectV2Field { name } } }
                        }
                      }
                    }
                  }
                }
              }
            }
            """
            try:
                r = requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": {"org": self.org, "number": p_num}})
                data = r.json().get('data', {}).get('organization', {}).get('projectV2', {})
                if not data:
                    print(f"WARNING: Project {p_num} returned no data.")
                    continue
                    
                for item in data.get('items', {}).get('nodes', []):
                    content = item.get('content')
                    if not content: continue
                    
                    # Skip if closed or archived
                    if content.get('closed') or item.get('isArchived'): continue
                    if content['id'] in unique_ids: continue
                    
                    # Extract fields into a flat map
                    fields = {}
                    for fv in item.get('fieldValues', {}).get('nodes', []):
                        f_name = fv.get('field', {}).get('name')
                        f_val = fv.get('text') or fv.get('number') or fv.get('name') or fv.get('date')
                        if f_name: fields[f_name] = f_val
                    
                    # Logic: Only Parent tasks go in the daily report
                    if fields.get('Level') == 'Child': continue
                    
                    # Map back to standard object
                    assignees = content.get('assignees', {}).get('nodes', [])
                    active_tasks.append({
                        "id": content['id'],
                        "number": content.get('number'),
                        "title": content.get('title'),
                        "url": content.get('url'),
                        "assignee": assignees[0].get('login') if assignees else None,
                        "project_tag": fields.get('Portfolio Project') or fields.get('project') or data.get('title'),
                        "start_date": fields.get('Start date'),
                        "end_date": fields.get('End date'),
                        "hours": float(fields.get('Assigned Hours') or 0.0)
                    })
                    unique_ids.add(content['id'])
            except Exception as e:
                print(f"ERROR querying project {p_num}: {e}")
                
        return active_tasks

    def get_child_issues_status(self, parent_title):
        query = "query($org: String!) { organization(login: $org) { projectV2(number: 4) { items(first: 100) { nodes { fieldValues(first: 20) { nodes { ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2Field { name } } } ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2Field { name } } } } } content { ... on Issue { state } } } } } } }"
        r = requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": {"org": self.org}})
        items = r.json().get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {}).get('nodes', [])
        found = closed = 0
        for item in items:
            fields = {fv['field']['name']: (fv.get('text') or fv.get('name')) for fv in item['fieldValues']['nodes'] if fv.get('field')}
            if fields.get('Level') == 'Child' and fields.get('Parent issue') == parent_title:
                found += 1
                if item.get('content', {}).get('state') == 'CLOSED': closed += 1
        return found > 0 and found == closed
