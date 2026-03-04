import requests
import os
import re
import time
from dotenv import load_dotenv
from orchestrator import Orchestrator

load_dotenv()

def resync_dates():
    print("--- Resyncing Start/End Dates to GitHub Project 4 ---\n")
    
    orc = Orchestrator(dry_run=False)
    gh = orc.gh_specialist
    
    # 1. Ingest tasks from sheet
    tasks = orc.ingestor.get_live_tasks()
    
    # 2. Map Issue Number to Item ID in Project 4
    print("Fetching Project 4 items...")
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
    
    print(f"Mapped {len(item_map)} items.\n")

    for task in tasks:
        issue_url = task.get('backlog_id')
        if not issue_url or "github.com" not in issue_url: continue
        
        match = re.search(r'/issues/(\d+)', issue_url)
        if not match: continue
        issue_num = int(match.group(1))
        
        item_id = item_map.get(issue_num)
        if not item_id: continue

        # Pull dates from the sheet (via task dict)
        # Note: In our current run, the orchestrator calculated them. 
        # In a resync, we need to make sure they are in the task object.
        # Let's recalculate them based on the PIC already in the sheet to be safe and accurate.
        pic_name = task.get('pic')
        github_user = orc.developer_map.get(pic_name)
        
        if not github_user:
            print(f"Skipping Task {task['id']} (No PIC mapping for {pic_name})")
            continue

        # Use the timeline to get the dates (starting from tomorrow since we reset them earlier)
        # However, to be EXACTLY as they are in the sheet, let's just use the orchestrator's current timeline state.
        # Since we just ran corrective_sync, the sheet and the timeline calculation SHOULD match.
        best_dev = {"name": pic_name, "id": github_user}
        start_date, end_date = orc.timelines[github_user].fill_hours_with_dates(task['estimated_hours'])

        print(f"Updating Issue #{issue_num} (Task {task['id']}) for {pic_name}:")
        print(f"  - Dates: {start_date} to {end_date}")
        print(f"  - Hours: {task['estimated_hours']}")
        
        gh.update_field(4, item_id, 'start_date', start_date)
        gh.update_field(4, item_id, 'end_date', end_date)
        gh.update_field(4, item_id, 'hours', task['estimated_hours'])
        
        print(f"  - SUCCESS: #{issue_num} dates synced.\n")
        time.sleep(1)

if __name__ == "__main__":
    resync_dates()
