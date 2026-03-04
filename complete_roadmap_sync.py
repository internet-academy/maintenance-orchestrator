import requests
import os
import re
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from orchestrator import Orchestrator
from agents.load_balancer import DeveloperTimeline

load_dotenv()

def complete_roadmap_sync():
    print("--- STARTING COMPLETE ROADMAP SYNC (BACKFILLING DATES TO P3) ---")
    orc = Orchestrator(dry_run=False)
    gh = orc.gh_specialist
    
    # Force fresh timelines for rescheduling
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    orc.timelines = {}
    for name, github_user in orc.developer_map.items():
        orc.timelines[github_user] = DeveloperTimeline(name, start_date=tomorrow)

    # 1. Fetch Mapping for both projects
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
                      content { ... on Issue { number repository { name } } }
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
                    item_map[int(content['number'])] = {
                        'item_id': node['id'],
                        'repo': content['repository']['name']
                    }
            if not data.get('pageInfo', {}).get('hasNextPage'): break
            cursor = data['pageInfo']['endCursor']
        return item_map

    print("Mapping Project 3 (Management)...")
    p3_map = get_item_map(3)
    print("Mapping Project 4 (Maintenance)...")
    p4_map = get_item_map(4)

    # 2. Ingest Sheet Tasks
    tasks = orc.ingestor.get_live_tasks()
    print(f"\nProcessing {len(tasks)} tasks from sheet...")
    for task in tasks:
        issue_url = task.get('backlog_id')
        if not issue_url or "github.com" not in issue_url: continue
        
        match = re.search(r'/issues/(\d+)', issue_url)
        if not match: continue
        issue_num = int(match.group(1))
        
        # Calculate fresh dates based on PIC in sheet
        pic_name = task.get('pic')
        github_user = orc.developer_map.get(pic_name)
        if not github_user: continue
        
        start_date, end_date = orc.timelines[github_user].fill_hours_with_dates(task['estimated_hours'])
        
        # Update Project 4 (Dates/Status)
        p4_data = p4_map.get(issue_num)
        if p4_data:
            print(f"Syncing #{issue_num} to Project 4...")
            gh.update_field(4, p4_data['item_id'], 'start_date', start_date)
            gh.update_field(4, p4_data['item_id'], 'end_date', end_date)
        
        # Update Project 3 (Dates/Tag)
        p3_data = p3_map.get(issue_num)
        if p3_data:
            print(f"Syncing #{issue_num} to Project 3 (Dates + Tag)...")
            gh.update_field(3, p3_data['item_id'], 'start_date', start_date)
            gh.update_field(3, p3_data['item_id'], 'end_date', end_date)
            gh.update_field(3, p3_data['item_id'], 'project', gh.projects[3]['options']['project_maintenance'], is_option=True)
        
        time.sleep(0.5)

    print("\n--- SYNC COMPLETE ---")

if __name__ == "__main__":
    complete_roadmap_sync()
