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
    print("--- STARTING COMPLETE ROADMAP SYNC (POPULATING PORTFOLIO PROJECT) ---")
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
                      content { 
                        ... on Issue { number repository { name } } 
                        ... on PullRequest { number repository { name } }
                      }
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
    
    # 2. GLOBAL CLEANUP: Tag EVERY issue in Project 3 that belongs to maintenance repos
    print("\n--- GLOBAL CLEANUP: Tagging all repo issues in Project 3 ---")
    maintenance_repos = ["member", "bohr-individual", "bohr-corporate", "bohr-core"]
    
    for issue_num, data in p3_map.items():
        if data['repo'] in maintenance_repos:
            print(f"Ensuring 'Maintenance' tag for {data['repo']}#{issue_num}...")
            # We use the internal key 'project' which maps to the 'Portfolio Project' field ID
            gh.update_field(3, data['item_id'], 'project', gh.projects[3]['options']['project_maintenance'], is_option=True)
            time.sleep(0.5)

    print("\n--- SYNC COMPLETE ---")

if __name__ == "__main__":
    complete_roadmap_sync()
