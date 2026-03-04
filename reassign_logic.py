import requests
import os
import re
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from orchestrator import Orchestrator
from agents.load_balancer import DeveloperTimeline

load_dotenv()

def master_reassignment():
    print("--- STARTING MASTER RE-ASSIGNMENT (ENFORCING TEAM > CHOO) ---")
    orc = Orchestrator(dry_run=False)
    gh = orc.gh_specialist
    
    # 1. Reset Timelines starting from tomorrow (2026-03-05)
    # We do NOT pre-fill here because we are performing a total reshuffle of all maintenance work
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    orc.timelines = {}
    for name, github_user in orc.developer_map.items():
        orc.timelines[github_user] = DeveloperTimeline(name, start_date=tomorrow)

    # 2. Map Issue Numbers to Item IDs for both projects
    def get_item_map(project_num):
        item_map = {}
        cursor = None
        while True:
            query = """
            query($org: String!, $project_number: Int!, $cursor: String) {
              organization(login: $org) {
                projectV2(number: $project_number) {
                  items(first: 100, after: $cursor) {
                    pageInfo { hasNextPage endCursor }
                    nodes {
                      id
                      content { ... on Issue { number id } }
                    }
                  }
                }
              }
            }
            """
            resp = requests.post(gh.graphql_url, headers=gh.headers, json={"query": query, "variables": {"org": gh.org, "project_number": project_num, "cursor": cursor}})
            data = resp.json().get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {})
            for node in data.get('nodes', []):
                content = node.get('content')
                if content and 'number' in content:
                    item_map[int(content['number'])] = node['id']
            if not data.get('pageInfo', {}).get('hasNextPage'): break
            cursor = data['pageInfo']['endCursor']
        return item_map

    p3_items = get_item_map(3)
    p4_items = get_item_map(4)

    # 3. Process each task from the sheet
    tasks = orc.ingestor.get_live_tasks()
    for task in tasks:
        issue_url = task.get('backlog_id')
        if not issue_url or "github.com" not in issue_url: continue
        
        match = re.search(r'/issues/(\d+)', issue_url)
        if not match: continue
        issue_num = int(match.group(1))
        
        # Determine the BEST dev using the new Team > Choo logic
        best_dev = orc._find_best_dev(task['estimated_hours'])
        if not best_dev:
            print(f"Task {task['id']} (# {issue_num}): OVERLOAD - No capacity found.")
            continue
            
        start_date, end_date = orc.timelines[best_dev['id']].fill_hours_with_dates(task['estimated_hours'])
        
        print(f"Re-assigning Task {task['id']} (# {issue_num}) -> {best_dev['name']} ({start_date} to {end_date})")
        
        # --- UPDATE GITHUB ---
        # 1. Update Assignee on the Issue itself
        repo = "member" if "member" in issue_url else "bohr-individual"
        assign_url = f"https://api.github.com/repos/{gh.org}/{repo}/issues/{issue_num}"
        requests.patch(assign_url, headers=gh.headers, json={"assignees": [best_dev['id']]})
        
        # 2. Update Project 4 (Maintenance) Fields
        if issue_num in p4_items:
            item_id = p4_items[issue_num]
            gh.update_field(4, item_id, 'start_date', start_date)
            gh.update_field(4, item_id, 'end_date', end_date)
            gh.update_field(4, item_id, 'hours', task['estimated_hours'])
            
        # 3. Update Project 3 (Management) Fields
        if issue_num in p3_items:
            item_id = p3_items[issue_num]
            gh.update_field(3, item_id, 'start_date', start_date)
            gh.update_field(3, item_id, 'end_date', end_date)
            
        # --- UPDATE SHEET ---
        orc.ingestor.write_status(task['anchors'], "Open")
        orc.ingestor.write_pic(task['anchors'], best_dev['name'])
        orc.ingestor.write_dates(task['anchors'], start_date, end_date)
        
        time.sleep(1)

    print("\n--- MASTER RE-ASSIGNMENT COMPLETE ---")

if __name__ == "__main__":
    master_reassignment()
