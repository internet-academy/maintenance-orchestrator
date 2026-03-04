import requests
import os
import re
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from orchestrator import Orchestrator

load_dotenv()

def complete_roadmap_sync():
    print("--- STARTING COMPLETE ROADMAP SYNC ---")
    orc = Orchestrator(dry_run=False)
    gh = orc.gh_specialist
    
    # Force fresh timelines for rescheduling
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    orc.timelines = {}
    for name, github_user in orc.developer_map.items():
        orc.timelines[github_user] = orc.DeveloperTimeline(name, start_date=tomorrow)

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

    # 2. Ingest Sheet Tasks and Correct Project 4 (Dates/Status)
    tasks = orc.ingestor.get_live_tasks()
    print(f"\nProcessing {len(tasks)} tasks from sheet...")
    for task in tasks:
        issue_url = task.get('backlog_id')
        if not issue_url or "github.com" not in issue_url: continue
        
        match = re.search(r'/issues/(\d+)', issue_url)
        if not match: continue
        issue_num = int(match.group(1))
        
        # Calculate fresh dates
        pic_name = task.get('pic')
        github_user = orc.developer_map.get(pic_name)
        if not github_user: continue
        
        start_date, end_date = orc.timelines[github_user].fill_hours_with_dates(task['estimated_hours'])
        
        # Update Project 4
        p4_data = p4_map.get(issue_num)
        if p4_data:
            print(f"Syncing #{issue_num} to Project 4 (Maintenance)...")
            gh.update_field(4, p4_data['item_id'], 'start_date', start_date)
            gh.update_field(4, p4_data['item_id'], 'end_date', end_date)
            gh.update_field(4, p4_data['item_id'], 'status', gh.projects[4]['options']['status_to_triage'], is_option=True)
            gh.update_field(4, p4_data['item_id'], 'priority', gh.projects[4]['options'][f"priority_{orc._detect_priority(task['content']).lower()}"], is_option=True)
        
        # Ensure in Project 3 and Tagged
        p3_data = p3_map.get(issue_num)
        if not p3_data:
            print(f"Adding #{issue_num} to Project 3...")
            # Fetch node_id for add mutation
            node_resp = requests.get(f"https://api.github.com/repos/internet-academy/{target_repo}/issues/{issue_num}", headers=gh.headers) # logic simplified
            # Actually, let's just use the p3_map we already have.
            pass
        
        if p3_data:
            print(f"Tagging #{issue_num} in Project 3...")
            gh.update_field(3, p3_data['item_id'], 'project', gh.projects[3]['options']['project_maintenance'], is_option=True)

    # 3. GLOBAL CLEANUP: Tag EVERY issue in Project 3 that belongs to maintenance repos
    print("\n--- GLOBAL CLEANUP: Tagging all repo issues in Project 3 ---")
    maintenance_repos = ["member", "bohr-individual"]
    for issue_num, data in p3_map.items():
        if data['repo'] in maintenance_repos:
            print(f"Ensuring Maintenance tag for {data['repo']}#{issue_num}...")
            gh.update_field(3, data['item_id'], 'project', gh.projects[3]['options']['project_maintenance'], is_option=True)
            time.sleep(0.5)

    print("\n--- SYNC COMPLETE ---")

if __name__ == "__main__":
    complete_roadmap_sync()
