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
        """Updates a field in a project with explicit type handling."""
        project_id = self.projects[project_number]["id"]
        field_id = self.projects[project_number]["fields"].get(field_key)
        if not field_id: return

        if self.dry_run:
            print(f"[DRY RUN] Project {project_number} update: {field_key} -> {value}")
            return

        # Explicit type selection based on value and field configuration
        if is_option:
            v_key = "singleSelectOptionId"
            v_type = "String"
            v_val = str(value)
        elif "-" in str(value) and len(str(value)) == 10:
            v_key = "date"
            v_type = "Date"
            v_val = str(value)
        elif isinstance(value, (int, float)):
            v_key = "number"
            v_type = "Float"
            v_val = float(value)
        else:
            v_key = "text"
            v_type = "String"
            v_val = str(value)

        mutation = """
        mutation($project: ID!, $item: ID!, $field: ID!, $value: %VAL_TYPE%!) {
          updateProjectV2ItemFieldValue(input: {
            projectId: $project, itemId: $item, fieldId: $field,
            value: { %KEY%: $value }
          }) { clientMutationId }
        }
        """
        query = mutation.replace("%VAL_TYPE%", v_type).replace("%KEY%", v_key)
        variables = {"project": project_id, "item": item_id, "field": field_id, "value": v_val}
        
        response = requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": variables})
        res_json = response.json()
        if "errors" in res_json:
            print(f"ERROR updating project {project_number} field {field_key}: {res_json['errors']}")
        response.raise_for_status()

    def link_subissue(self, parent_node_id, child_node_id):
        """Natively links a sub-issue to a parent issue in GitHub."""
        if self.dry_run:
            print(f"[DRY RUN] Would link child {child_node_id} to parent {parent_node_id}")
            return

        query = """
        mutation($parent: ID!, $child: ID!) {
          addSubIssue(input: {issueId: $parent, subIssueId: $child}) {
            parentIssue { id }
          }
        }
        """
        vars = {"parent": parent_node_id, "child": child_node_id}
        response = requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": vars})
        response.raise_for_status()

    def get_issue_node_id(self, repo, number):
        """Fetches the global Node ID for a specific issue number."""
        url = f"https://api.github.com/repos/{self.org}/{repo}/issues/{number}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()['node_id']

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
        """
        Fetches active issues for a user across ALL projects in the organization
        and sums their 'Assigned Hours', de-duplicating by Issue/PR ID.
        """
        # 1. Fetch all project numbers for the organization
        query_projects = """
        query($org: String!) {
          organization(login: $org) {
            projectsV2(first: 20) {
              nodes { number title }
            }
          }
        }
        """
        try:
            resp_projects = requests.post(self.graphql_url, headers=self.headers, json={"query": query_projects, "variables": {"org": self.org}})
            proj_json = resp_projects.json()
            project_nodes = proj_json.get('data', {}).get('organization', {}).get('projectsV2', {}).get('nodes', [])
            if not project_nodes:
                return 0.0
            project_nums = [p['number'] for p in project_nodes if p.get('number')]
        except Exception as e:
            print(f"DEBUG: Failed to fetch projects: {e}")
            return 0.0

        unique_tasks = {} # content_id -> hours
        
        for p_num in project_nums:
            query_items = """
            query($org: String!, $number: Int!) {
              organization(login: $org) {
                projectV2(number: $number) {
                  items(first: 100) {
                    nodes {
                      fieldValues(first: 20) {
                        nodes {
                          ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2Field { name } } }
                          ... on ProjectV2ItemFieldNumberValue { number field { ... on ProjectV2Field { name } } }
                          ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2Field { name } } }
                        }
                      }
                      content {
                        ... on Issue { id assignees(first: 10) { nodes { login } } closed }
                        ... on PullRequest { id assignees(first: 10) { nodes { login } } closed }
                      }
                    }
                  }
                }
              }
            }
            """
            try:
                resp_items = requests.post(self.graphql_url, headers=self.headers, json={"query": query_items, "variables": {"org": self.org, "number": p_num}})
                items_json = resp_items.json()
                items = items_json.get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {}).get('nodes', [])
                if not items: continue
                
                for item in items:
                    content = item.get("content")
                    if not content or content.get("closed") is True: continue
                    
                    assignees = [a["login"].lower() for a in content.get("assignees", {}).get("nodes", []) if a.get("login")]
                    if github_username.lower() not in assignees: continue
                    
                    # Extract Hours
                    hours = 0.0
                    is_done = False
                    for fv in item.get("fieldValues", {}).get("nodes", []):
                        field_data = fv.get("field", {})
                        if not field_data: continue
                        field_name = field_data.get("name")
                        if field_name and "Hours" in field_name:
                            hours = float(fv.get("number") or fv.get("text") or 0.0)
                        if field_name == "Status" and fv.get("name") == "Done":
                            is_done = True
                    
                    if not is_done:
                        content_id = content['id']
                        unique_tasks[content_id] = max(unique_tasks.get(content_id, 0.0), hours)
            except Exception as e:
                print(f"DEBUG: Failed to fetch items for project {p_num}: {e}")
                continue

        return sum(unique_tasks.values())

    def get_full_active_tasks(self):
        """Fetches detailed data for all active tasks across all org projects."""
        query_projects = """
        query($org: String!) { organization(login: $org) { projectsV2(first: 20) { nodes { number } } } }
        """
        resp_projects = requests.post(self.graphql_url, headers=self.headers, json={"query": query_projects, "variables": {"org": self.org}})
        project_nums = [p['number'] for p in resp_projects.json().get('data', {}).get('organization', {}).get('projectsV2', {}).get('nodes', [])]

        active_tasks = []
        unique_ids = set()

        for p_num in project_nums:
            query_items = """
            query($org: String!, $number: Int!) {
              organization(login: $org) {
                projectV2(number: $number) {
                  items(first: 100) {
                    nodes {
                      fieldValues(first: 20) {
                        nodes {
                          ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2Field { name } } }
                          ... on ProjectV2ItemFieldNumberValue { number field { ... on ProjectV2Field { name } } }
                          ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2Field { name } } }
                          ... on ProjectV2ItemFieldDateValue { date field { ... on ProjectV2Field { name } } }
                        }
                      }
                      content {
                        ... on Issue { id number title assignees(first: 1) { nodes { login } } closed url }
                        ... on PullRequest { id number title assignees(first: 1) { nodes { login } } closed url }
                      }
                    }
                  }
                }
              }
            }
            """
            resp_items = requests.post(self.graphql_url, headers=self.headers, json={"query": query_items, "variables": {"org": self.org, "number": p_num}})
            items = resp_items.json().get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {}).get('nodes', [])
            if not items: continue

            for item in items:
                content = item.get("content")
                if not content or content.get("closed") is True: continue
                if content['id'] in unique_ids: continue

                fields = {}
                for fv in item.get("fieldValues", {}).get("nodes", []):
                    name = fv.get("field", {}).get("name")
                    val = fv.get("number") or fv.get("text") or fv.get("name") or fv.get("date")
                    if name: fields[name] = val
                
                # We only want Parent tasks for the daily summary
                if fields.get("Level") == "Child": continue

                # Safely extract the first assignee if one exists
                assignee_nodes = content.get("assignees", {}).get("nodes", [])
                assignee_login = assignee_nodes[0].get("login") if assignee_nodes else None

                active_tasks.append({
                    "id": content['id'],
                    "number": content['number'],
                    "title": content['title'],
                    "url": content['url'],
                    "assignee": assignee_login,
                    "project_tag": fields.get("Portfolio Project") or fields.get("project") or "Maintenance",
                    "start_date": fields.get("Start date"),
                    "end_date": fields.get("End date"),
                    "status": fields.get("Status")
                })
                unique_ids.add(content['id'])
        
        return active_tasks

    def get_child_issues_status(self, parent_title):
        query = """
        query($org: String!) { organization(login: $org) { projectV2(number: 4) { items(first: 100) { nodes {
          fieldValues(first: 20) { nodes { ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2Field { name } } } 
          ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2Field { name } } } } }
          content { ... on Issue { state } }
        } } } } }
        """
        response = requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": {"org": self.org}})
        items = response.json().get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {}).get('nodes', [])
        children_found = 0
        children_closed = 0
        for item in items:
            fields = {fv.get('field', {}).get('name'): (fv.get('text') or fv.get('name')) for fv in item.get('fieldValues', {}).get('nodes', [])}
            if fields.get('Level') == 'Child' and fields.get('Parent issue') == parent_title:
                children_found += 1
                if item.get('content', {}).get('state') == 'CLOSED': children_closed += 1
        return children_found > 0 and children_found == children_closed
