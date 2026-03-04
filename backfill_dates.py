import requests
import os
import re
import time
from dotenv import load_dotenv
from agents.github_specialist import GitHubSpecialist

load_dotenv()

def backfill_all_dates():
    print("--- STARTING GLOBAL DATE BACKFILL ---")
    gh = GitHubSpecialist(os.getenv('GITHUB_TOKEN'))
    org = "internet-academy"

    # 1. Fetch ALL items from Project 3 and Project 4
    def get_project_items(project_num):
        items = {}
        cursor = None
        while True:
            query = """
            query($org: String!, $num: Int!, $cursor: String) {
              organization(login: $org) {
                projectV2(number: $num) {
                  items(first: 100, after: $cursor) {
                    pageInfo { hasNextPage endCursor }
                    nodes {
                      id
                      content { ... on Issue { number id } ... on PullRequest { number id } }
                      fieldValues(first: 20) {
                        nodes {
                          ... on ProjectV2ItemFieldDateValue { date field { ... on ProjectV2Field { name } } }
                          ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2Field { name } } }
                        }
                      }
                    }
                  }
                }
              }
            }
            """
            resp = requests.post(gh.graphql_url, headers=gh.headers, json={"query": query, "variables": {"org": org, "num": project_num, "cursor": cursor}})
            data = resp.json().get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {})
            for node in data.get('nodes', []):
                content = node.get('content')
                if content:
                    # Use the Issue/PR global Node ID as the key for cross-project matching
                    items[content['id']] = {
                        'item_id': node['id'],
                        'number': content['number'],
                        'fields': {fv.get('field', {}).get('name'): (fv.get('date') or fv.get('name')) for fv in node.get('fieldValues', {}).get('nodes', [])}
                    }
            if not data.get('pageInfo', {}).get('hasNextPage'): break
            cursor = data['pageInfo']['endCursor']
        return items

    print("Fetching Project 3 (Management) items...")
    p3_items = get_project_items(3)
    print("Fetching Project 4 (Maintenance) items...")
    p4_items = get_project_items(4)

    # 2. Sync Logic: If P4 has dates and P3 doesn't, copy them
    print("\nChecking for missing dates in Project 3...")
    for content_id, p3_data in p3_items.items():
        # Only check if dates are missing in P3
        p3_start = p3_data['fields'].get('Start date')
        p3_end = p3_data['fields'].get('End date')
        
        if not p3_start or not p3_end:
            # Look for this same issue in Project 4
            if content_id in p4_items:
                p4_data = p4_items[content_id]
                p4_start = p4_data['fields'].get('Start date')
                p4_end = p4_data['fields'].get('End date')
                
                if p4_start and p4_end:
                    print(f"Syncing Dates for Issue #{p3_data['number']}: {p4_start} -> {p4_end}")
                    gh.update_field(3, p3_data['item_id'], 'start_date', p4_start)
                    gh.update_field(3, p3_data['item_id'], 'end_date', p4_end)
                    time.sleep(0.5)
            else:
                # If not in P4, we might not have a source yet
                # print(f"Issue #{p3_data['number']} has no dates and is not in Project 4.")
                pass

    print("\n--- BACKFILL COMPLETE ---")

if __name__ == "__main__":
    backfill_all_dates()
