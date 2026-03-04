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
    
    # 1. Reset Timelines starting from tomorrow
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    orc.timelines = {}
    for name, github_user in orc.developer_map.items():
        orc.timelines[github_user] = DeveloperTimeline(name, start_date=tomorrow)

    # 2. Map Issue Numbers to Item IDs
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

    # 3. Optimize Sheet updates
    ws = orc.ingestor.get_current_month_worksheet()
    all_values = ws.get_all_values()

    # 4. Process each task
    tasks = orc.ingestor.get_live_tasks()
    for task in tasks:
        issue_url = task.get('backlog_id')
        if not issue_url or "github.com" not in issue_url: continue
        
        match = re.search(r'/issues/(\d+)', issue_url)
        if not match: continue
        issue_num = int(match.group(1))
        
        # Determine the BEST dev
        best_dev = orc._find_best_dev(task['estimated_hours'])
        if not best_dev: continue
            
        start_date, end_date = orc.timelines[best_dev['id']].fill_hours_with_dates(task['estimated_hours'])
        
        # Check current PIC in sheet to skip already optimized ones
        row_idx, col_idx = task['anchors']['pic']
        current_pic_in_sheet = all_values[row_idx][col_idx + 1]
        
        if current_pic_in_sheet == best_dev['name'] and all_values[task['anchors']['status'][0]][task['anchors']['status'][1] + 1] == "Open":
            print(f"Skipping Task {task['id']} (already optimized).")
            continue

        print(f"Updating Task {task['id']} (# {issue_num}) -> {best_dev['name']}...")
        
        # --- GITHUB UPDATES ---
        repo = "member" if "member" in issue_url else "bohr-individual"
        assign_url = f"https://api.github.com/repos/{gh.org}/{repo}/issues/{issue_num}"
        requests.patch(assign_url, headers=gh.headers, json={"assignees": [best_dev['id']]})
        
        if issue_num in p4_items:
            gh.update_field(4, p4_items[issue_num], 'start_date', start_date)
            gh.update_field(4, p4_items[issue_num], 'end_date', end_date)
            gh.update_field(4, p4_items[issue_num], 'hours', task['estimated_hours'])
            
        if issue_num in p3_items:
            gh.update_field(3, p3_items[issue_num], 'start_date', start_date)
            gh.update_field(3, p3_items[issue_num], 'end_date', end_date)
            
        # --- SHEET UPDATES (Minimized) ---
        ws.update_cell(task['anchors']['status'][0] + 1, task['anchors']['status'][1] + 2, "Open")
        ws.update_cell(task['anchors']['pic'][0] + 1, task['anchors']['pic'][1] + 2, best_dev['name'])
        
        # write_dates heuristic
        for r in range(task['anchors']['status'][0], task['anchors']['status'][0] + 10):
            row_data = all_values[r]
            for c, val in enumerate(row_data):
                if "Start date" in str(val):
                    ws.update_cell(r + 1, c + 2, start_date)
                if "End date" in str(val) or "Finish date" in str(val):
                    ws.update_cell(r + 1, c + 2, end_date)
        
        time.sleep(2) # Safety delay

    print("\n--- MASTER RE-ASSIGNMENT COMPLETE ---")

if __name__ == "__main__":
    master_reassignment()
