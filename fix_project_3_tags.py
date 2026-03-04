import requests
import os
import re
import time
from dotenv import load_dotenv
from orchestrator import Orchestrator

load_dotenv()

def fix_project_3_tags():
    print("--- Fixing 'project' tags in Project 3 (Overall Project Management) ---\n")
    
    orc = Orchestrator(dry_run=False)
    gh = orc.gh_specialist
    
    # 1. Ingest current tasks from sheet to get the GitHub URLs
    tasks = orc.ingestor.get_live_tasks()
    target_numbers = []
    for t in tasks:
        issue_url = t.get('backlog_id')
        if issue_url and "github.com" in issue_url:
            match = re.search(r'/issues/(\d+)', issue_url)
            if match:
                target_numbers.append(int(match.group(1)))
    
    print(f"Found {len(target_numbers)} issues in sheet to verify in Project 3.\n")
    
    # 2. Fetch ALL project items from Project 3
    print("Fetching items from Project 3...")
    item_map = {} # Issue Num -> Item ID
    cursor = None
    while True:
        query = """
        query($org: String!, $cursor: String) {
          organization(login: $org) {
            projectV2(number: 3) {
              items(first: 100, after: $cursor) {
                pageInfo { hasNextPage endCursor }
                nodes {
                  id
                  content {
                    ... on Issue { number }
                  }
                }
              }
            }
          }
        }
        """
        resp = requests.post(gh.graphql_url, headers=gh.headers, json={"query": query, "variables": {"org": gh.org, "cursor": cursor}})
        data = resp.json().get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {})
        for node in data.get('nodes', []):
            content = node.get('content')
            if content and 'number' in content:
                item_map[int(content['number'])] = node['id']
        
        if not data.get('pageInfo', {}).get('hasNextPage'):
            break
        cursor = data['pageInfo']['endCursor']
    
    print(f"Mapped {len(item_map)} items in Project 3.\n")

    # 3. Update the field for each target issue
    for num in target_numbers:
        item_id = item_map.get(num)
        if not item_id:
            print(f"Issue #{num} not found in Project 3. Adding it now...")
            # We need the node_id of the issue itself to add it to the project
            # For simplicity in this script, let's fetch it
            node_resp = requests.get(f"https://api.github.com/repos/internet-academy/member/issues/{num}", headers=gh.headers)
            if node_resp.status_code == 200:
                issue_node_id = node_resp.json().get('node_id')
                item_id = gh.add_to_project(issue_node_id, 3)
                print(f"  - Added #{num} to Project 3 (Item: {item_id})")
            else:
                print(f"  - ERROR: Could not fetch Issue #{num}")
                continue

        print(f"Updating Issue #{num} project tag...")
        gh.update_field(3, item_id, 'project', gh.projects[3]['options']['project_maintenance'], is_option=True)
        print(f"  - SUCCESS: Project tag set to 'Maintenance' for #{num}")
        time.sleep(1)

if __name__ == "__main__":
    fix_project_3_tags()
