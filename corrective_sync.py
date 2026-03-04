import requests
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from orchestrator import Orchestrator
from agents.load_balancer import DeveloperTimeline

load_dotenv()

def corrective_sync():
    # Force start date to tomorrow
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"--- Corrective Sync: Resetting Status & Re-scheduling from {tomorrow} ---\n")
    
    orc = Orchestrator(dry_run=False)
    gh = orc.gh_specialist
    
    # 1. Re-initialize Timelines starting from tomorrow
    orc.timelines = {}
    for name, github_user in orc.developer_map.items():
        timeline = DeveloperTimeline(name, start_date=tomorrow)
        # We don't pre-fill with existing load yet, because we are effectively 
        # re-shuffling the deck starting tomorrow.
        orc.timelines[github_user] = timeline

    # 2. Ingest current tasks from sheet (to get anchors and existing GitHub URLs)
    tasks = orc.ingestor.get_live_tasks()
    
    for task in tasks:
        issue_url = task.get('backlog_id')
        if not issue_url or "github.com" not in issue_url:
            continue
            
        print(f"Correcting Task {task['id']} ({issue_url})...")
        
        # Determine PIC
        best_dev = orc._find_best_dev(task['estimated_hours'])
        if not best_dev:
            print(f"  - ERROR: No capacity for re-scheduling Task {task['id']}")
            continue
            
        # Recalculate Dates
        start_date, end_date = orc.timelines[best_dev['id']].fill_hours_with_dates(task['estimated_hours'])
        
        # Find the Project Item ID
        # Extract issue number (e.g. from https://.../issues/2565)
        import re
        match = re.search(r'/issues/(\d+)', issue_url)
        if not match:
            print(f"  - ERROR: Could not parse issue number from {issue_url}")
            continue
        issue_num = int(match.group(1))
        
        # Use GraphQL to find the Item ID in the project
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
        response = requests.post(gh.graphql_url, headers=gh.headers, json={"query": query, "variables": {"org": gh.org, "num": int(issue_num)}})
        items = response.json().get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {}).get('nodes', [])
        
        item_id = None
        for item in items:
            if item.get('content', {}).get('number') == int(issue_num):
                item_id = item['id']
                break
        
        if not item_id:
            print(f"  - ERROR: Could not find Project Item for issue #{issue_num}")
            continue

        # 3. Update GitHub Project
        print(f"  - GitHub: Setting Status to 'To Triage', Dates to {start_date} -> {end_date}")
        gh.update_project_field(item_id, gh.field_ids['status'], gh.status_options['To Triage'], is_option=True)
        gh.update_project_field(item_id, gh.field_ids['start_date'], start_date)
        gh.update_project_field(item_id, gh.field_ids['end_date'], end_date)
        
        # 4. Update Google Sheet
        print(f"  - Sheet:  Setting Status to 'Open', updating Dates and PIC")
        orc.ingestor.write_status(task['anchors'], "Open") # "To Triage" maps to "Open" in staff terms
        orc.ingestor.write_dates(task['anchors'], start_date, end_date)
        if hasattr(orc.ingestor, 'write_pic'):
            orc.ingestor.write_pic(task['anchors'], best_dev['name'])
            
        print(f"  - SUCCESS: Task {task['id']} corrected.\n")

if __name__ == "__main__":
    corrective_sync()
