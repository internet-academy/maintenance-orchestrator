import requests
import os
import json
import re
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from orchestrator import Orchestrator
from agents.load_balancer import DeveloperTimeline

load_dotenv()

def corrective_sync():
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"--- Corrective Sync: Resetting Status & Re-scheduling from {tomorrow} ---\n")
    
    orc = Orchestrator(dry_run=False)
    gh = orc.gh_specialist
    
    # 1. Reset Timelines
    orc.timelines = {}
    for name, github_user in orc.developer_map.items():
        orc.timelines[github_user] = DeveloperTimeline(name, start_date=tomorrow)

    # 2. Ingest current tasks
    tasks = orc.ingestor.get_live_tasks()
    target_tasks = [t for t in tasks if t.get('backlog_id') and "github.com" in t.get('backlog_id')]
    
    # 3. Fetch Project items
    item_map = {}
    cursor = None
    while True:
        query = """
        query($org: String!, $cursor: String) {
          organization(login: $org) {
            projectV2(number: 4) {
              items(first: 100, after: $cursor) {
                pageInfo { hasNextPage endCursor }
                nodes {
                  id
                  content { ... on Issue { number } }
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
        if not data.get('pageInfo', {}).get('hasNextPage'): break
        cursor = data['pageInfo']['endCursor']

    # 4. Fetch Worksheet data ONCE to avoid 429
    ws = orc.ingestor.get_current_month_worksheet()
    all_values = ws.get_all_values()

    for task in target_tasks:
        issue_url = task['backlog_id']
        match = re.search(r'/issues/(\d+)', issue_url)
        if not match: continue
        issue_num = int(match.group(1))
        
        # Check current sheet status to skip already corrected ones
        row_idx, col_idx = task['anchors']['status']
        current_status = all_values[row_idx][col_idx + 1]
        
        # Determine PIC and Dates (must do this for ALL tasks to maintain timeline order)
        best_dev = orc._find_best_dev(task['estimated_hours'])
        start_date, end_date = orc.timelines[best_dev['id']].fill_hours_with_dates(task['estimated_hours'])

        if current_status == "Open":
            print(f"Skipping Task {task['id']} (already Open).")
            continue

        item_id = item_map.get(issue_num)
        if not item_id: continue

        print(f"Updating Task {task['id']} (##{issue_num})...")
        
        # GitHub Update
        gh.update_project_field(item_id, gh.field_ids['status'], gh.status_options['To Triage'], is_option=True)
        gh.update_project_field(item_id, gh.field_ids['start_date'], start_date)
        gh.update_project_field(item_id, gh.field_ids['end_date'], end_date)
        
        # Sheet Update (Manual Cell Updates to minimize API calls)
        # write_status
        ws.update_cell(row_idx + 1, col_idx + 2, "Open")
        
        # write_pic
        p_row, p_col = task['anchors']['pic']
        ws.update_cell(p_row + 1, p_col + 2, best_dev['name'])
        
        # write_dates (Heuristic)
        for r in range(row_idx, row_idx + 10):
            row_data = all_values[r]
            for c, val in enumerate(row_data):
                if "Start date" in str(val):
                    ws.update_cell(r + 1, c + 2, start_date)
                if "End date" in str(val) or "Finish date" in str(val):
                    ws.update_cell(r + 1, c + 2, end_date)
        
        print(f"  - SUCCESS: #{issue_num} corrected.")
        time.sleep(2) # Safety delay

if __name__ == "__main__":
    corrective_sync()
