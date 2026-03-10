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
        
        # Initialize native GitHub client (PyGithub)
        from github import Github
        self.gh_client = Github(token)
        
        # Project Configurations
        self.projects = {
            3: {
                "id": "PVT_kwDOA1jKuM4BQoor",
                "fields": {
                    "status": "PVTSSF_lADOA1jKuM4BQoorzg-spXY",
                    "portfolio_project": "PVTSSF_lADOA1jKuM4BQoorzg-tC7Q",
                    "start_date": "PVTF_lADOA1jKuM4BQoorzg-xYWY",
                    "end_date": "PVTF_lADOA1jKuM4BQoorzg-xYWs"
                },
                "options": {
                    "project_maintenance": "109c057b",
                    "project_new_dev": "a87ad165",
                    "project_ai": "58bc76f7"
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
                    "parent_issue": "PVTF_lADOA1jKuM4BQoqlzg-squo",
                    "requester": "PVTF_lADOA1jKuM4BQoqlzg_G1E4"
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
        """Updates a field in a project with explicit type handling."""
        project_id = self.projects[project_number]["id"]
        field_id = self.projects[project_number]["fields"].get(field_key)
        if not field_id:
            print(f"ERROR: Field key '{field_key}' not configured for Project {project_number}")
            return

        if self.dry_run:
            print(f"[DRY RUN] Project {project_number} update: {field_key} -> {value}")
            return

        if is_option:
            v_key = "singleSelectOptionId"; v_type = "String"; v_val = str(value)
        elif "-" in str(value) and len(str(value)) == 10:
            v_key = "date"; v_type = "Date"; v_val = str(value)
        elif isinstance(value, (int, float)):
            v_key = "number"; v_type = "Float"; v_val = float(value)
        else:
            v_key = "text"; v_type = "String"; v_val = str(value)

        mutation = f"mutation($project: ID!, $item: ID!, $field: ID!, $value: {v_type}!) {{ updateProjectV2ItemFieldValue(input: {{ projectId: $project, itemId: $item, fieldId: $field, value: {{ {v_key}: $value }} }}) {{ clientMutationId }} }}"
        r = requests.post(self.graphql_url, headers=self.headers, json={"query": mutation, "variables": {"project": project_id, "item": item_id, "field": field_id, "value": v_val}})
        res_json = r.json()
        if "errors" in res_json:
            print(f"ERROR updating project {project_number} field {field_key}: {res_json['errors']}")
        else:
            r.raise_for_status()

    def link_subissue(self, parent_node_id, child_node_id):
        """Natively links a sub-issue to a parent issue in GitHub."""
        if self.dry_run:
            print(f"[DRY RUN] Would link child {child_node_id} to parent {parent_node_id}")
            return

        query = """
        mutation($parent: ID!, $child: ID!) {
          addSubIssue(input: {issueId: $parent, subIssueId: $child}) {
            subIssue { id }
          }
        }
        """
        vars = {"parent": parent_node_id, "child": child_node_id}
        response = requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": vars})
        # We allow for 'duplicate sub-issue' errors as they mean the link is already there
        res_json = response.json()
        if "errors" in res_json:
            msg = res_json["errors"][0].get("message", "")
            if "duplicate sub-issues" in msg:
                return # Already linked
            print(f"ERROR natively linking sub-issue: {res_json['errors']}")
        else:
            response.raise_for_status()

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
                # Extract Assignee safely
                assignee_nodes = content.get('assignees', {}).get('nodes', [])
                assignee_login = assignee_nodes[0].get('login') if assignee_nodes else None
                
                data = {'item_id': item['id'], 'assignee': assignee_login}
                for fv in item.get('fieldValues', {}).get('nodes', []):
                    name = fv.get('field', {}).get('name')
                    val = fv.get('text') or fv.get('number') or fv.get('name') or fv.get('date')
                    if name: data[name] = val
                return data
        return None

    def get_full_active_tasks(self):
        active_tasks = []
        unique_ids = set()
        for p_num in [3, 4]:
            query = "query($org: String!, $number: Int!) { organization(login: $org) { projectV2(number: $number) { title items(first: 100) { nodes { isArchived fieldValues(first: 20) { nodes { ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2Field { name } } } ... on ProjectV2ItemFieldNumberValue { number field { ... on ProjectV2Field { name } } } ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2Field { name } } } ... on ProjectV2ItemFieldDateValue { date field { ... on ProjectV2Field { name } } } } } content { ... on Issue { id number title url closed labels(first: 10) { nodes { name } } assignees(first: 1) { nodes { login } } } ... on PullRequest { id number title url closed labels(first: 10) { nodes { name } } assignees(first: 1) { nodes { login } } } } } } } } }"
            r = requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": {"org": self.org, "number": p_num}})
            data = r.json().get('data', {}).get('organization', {}).get('projectV2', {})
            for item in data.get('items', {}).get('nodes', []):
                content = item.get('content')
                if not content or content.get('closed') or item.get('isArchived'): continue
                if content['id'] in unique_ids: continue
                fields = {fv['field']['name']: (fv.get('text') or fv.get('number') or fv.get('name') or fv.get('date')) for fv in item['fieldValues']['nodes'] if fv.get('field')}
                if fields.get('Level') == 'Child': continue
                # Extract Assignee Login safely
                assignees = content.get('assignees', {}).get('nodes', [])
                login = assignees[0].get('login') if assignees else None
                
                # Extract Labels
                labels = [l['name'] for l in content.get('labels', {}).get('nodes', [])] if 'labels' in content else []

                active_tasks.append({
                    "id": content['id'], "number": content['number'], "title": content['title'], "url": content['url'],
                    "assignee": login,
                    "labels": labels,
                    "project_tag": fields.get('Portfolio Project') or fields.get('project') or data.get('title'),
                    "start_date": fields.get('Start date'), "end_date": fields.get('End date'), "hours": float(fields.get('Assigned Hours') or 0.0)
                })
                unique_ids.add(content['id'])
        return active_tasks

    def get_subtasks(self, parent_number):
        """Fetches all sub-issues linked to a specific parent number."""
        query = """
        query($org: String!, $repo: String!, $num: Int!) {
          repository(owner: $org, name: $repo) {
            issue(number: $num) {
              subIssues(first: 20) {
                nodes {
                  number
                  title
                  state
                }
              }
            }
          }
        }
        """
        vars = {"org": self.org, "repo": "member", "num": parent_number}
        try:
            r = requests.post(self.graphql_url, headers=self.headers, json={"query": query, "variables": vars})
            return r.json().get('data', {}).get('repository', {}).get('issue', {}).get('subIssues', {}).get('nodes', [])
        except:
            return []

    def get_recent_repo_context(self, repo_name, days=3):
        """Fetches a summary of recent file changes in the repository."""
        since = (datetime.now() - timedelta(days=days)).isoformat()
        url = f"https://api.github.com/repos/{self.org}/{repo_name}/commits"
        params = {"since": since, "per_page": 10}
        
        try:
            r = requests.get(url, headers=self.headers, params=params)
            commits = r.json()
            if not isinstance(commits, list): return ""
            
            context = []
            files_changed = set()
            for c in commits:
                msg = c.get('commit', {}).get('message', '').split('\n')[0]
                context.append(f"- {msg}")
                # Optional: fetch files for each commit if we want more depth
            
            summary = "RECENT CODE CHANGES:\n" + "\n".join(context[:5])
            return summary
        except:
            return ""

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

    def get_gist_content(self, gist_id, filename):
        """Fetches the JSON content of a file from a GitHub Gist."""
        try:
            gist = self.gh_client.get_gist(gist_id)
            if filename in gist.files:
                return json.loads(gist.files[filename].content)
        except Exception as e:
            print(f"DEBUG: Could not read Gist {gist_id}: {e}")
        return None

    def update_gist(self, gist_id, filename, content_dict):
        """Updates a GitHub Gist with the provided dictionary as JSON."""
        if self.dry_run:
            print(f"[DRY RUN] Would update Gist {gist_id} with new state.")
            return
        try:
            from github import InputFileContent
            gist = self.gh_client.get_gist(gist_id)
            gist.edit(files={filename: InputFileContent(json.dumps(content_dict, indent=2))})
            print(f"GIST: State saved to {filename} in Gist {gist_id}")
        except Exception as e:
            print(f"ERROR: Failed to update Gist {gist_id}: {e}")
