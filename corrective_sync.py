import requests
import os
import json
import re
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
    
    # 1. Reset Timelines to start fresh from tomorrow
    orc.timelines = {}
    for name, github_user in orc.developer_map.items():
        # IMPORTANT: Start fresh, don't fill with existing load for this re-shuffle
        orc.timelines[github_user] = DeveloperTimeline(name, start_date=tomorrow)

    # 2. Ingest current tasks from sheet
    tasks = orc.ingestor.get_live_tasks()
    print(f"Total tasks found in sheet: {len(tasks)}")
    
    target_tasks = [t for t in tasks if t.get('backlog_id') and "github.com" in t.get('backlog_id')]
    print(f"Tasks with GitHub IDs to correct: {len(target_tasks)}\n")
    
    for task in target_tasks:
        issue_url = task['backlog_id']
        print(f"Correcting Task {task['id']} ({issue_url})...")
        
        # Determine PIC based on fresh timeline
        best_dev = orc._find_best_dev(task['estimated_hours'])
        if not best_dev:
            print(f"  - ERROR: No capacity for Task {task['id']}")
            continue
            
        start_date, end_date = orc.timelines[best_dev['id']].fill_hours_with_dates(task['estimated_hours'])
        
        # Find Issue Number
        match = re.search(r'/issues/(\d+)', issue_url)
        if not match:
            print(f"  - ERROR: Could not parse issue number from {issue_url}")
            continue
        issue_num = int(match.group(1))
        
        # Get Item ID from Project 4
        query = """
        query($org: String!, $num: Int!) {
          organization(login: $org) {
            projectV2(number: 4) {
              items(first: 100) {
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
        resp = requests.post(gh.graphql_url, headers=gh.headers, json={"query": query, "variables": {"org": gh.org, "num": issue_num}})
        items = resp.json().get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {}).get('nodes', [])
        
        item_id = None
        for item in items:
            if item.get('content', {}).get('number') == issue_num:
                item_id = item['id']
                break
        
        if not item_id:
            print(f"  - ERROR: Item ID not found for #{issue_num}")
            continue

        # 3. Apply Updates
        print(f"  - GitHub: To Triage, {start_date} to {end_date}")
        gh.update_project_field(item_id, gh.field_ids['status'], gh.status_options['To Triage'], is_option=True)
        gh.update_project_field(item_id, gh.field_ids['start_date'], start_date)
        gh.update_project_field(item_id, gh.field_ids['end_date'], end_date)
        
        print(f"  - Sheet:  Open, {start_date} to {end_date}, PIC: {best_dev['name']}")
        orc.ingestor.write_status(task['anchors'], "Open")
        orc.ingestor.write_dates(task['anchors'], start_date, end_date)
        if hasattr(orc.ingestor, 'write_pic'):
            orc.ingestor.write_pic(task['anchors'], best_dev['name'])
            
        print(f"  - SUCCESS: #{issue_num} corrected.\n")

if __name__ == "__main__":
    corrective_sync()
