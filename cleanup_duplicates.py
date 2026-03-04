import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')
ORG = "internet-academy"

def cleanup_duplicates():
    print("--- STARTING DUPLICATE AUDIT & CLEANUP ---\n")
    headers = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}
    
    # 1. Fetch ALL items in Project 4 (The Maintenance board)
    def get_all_items(project_num):
        items = []
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
                        ... on Issue { 
                          id number title repository { name }
                        } 
                      }
                      fieldValues(first: 30) {
                        nodes {
                          ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2Field { name } } }
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
            resp = requests.post("https://api.github.com/graphql", headers=headers, json={"query": query, "variables": {"org": ORG, "project_number": project_num, "cursor": cursor}})
            data = resp.json().get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {})
            items.extend(data.get('nodes', []))
            if not data.get('pageInfo', {}).get('hasNextPage'): break
            cursor = data['pageInfo']['endCursor']
        return items

    print("Fetching items from Project 4...")
    all_items = get_all_items(4)
    print(f"Found {len(all_items)} items to analyze.\n")

    # 2. Group items by Task ID (extracted from title e.g. #10)
    task_map = {} # TaskID -> List of Items
    for item in all_items:
        content = item.get('content')
        if not content: continue
        title = content.get('title', "")
        
        # Regex to find Task ID like "#10"
        match = re.search(r'#(\d+)', title)
        if not match: continue
        tid = match.group(1)
        
        if tid not in task_map: task_map[tid] = []
        task_map[tid].append(item)

    # 3. Analyze and select the "Golden Record"
    to_delete = []
    for tid, items in task_map.items():
        if len(items) <= 1: continue
        
        print(f"Checking Task #{tid} ({len(items)} instances found):")
        
        # Score items based on data richness
        scored_items = []
        for item in items:
            score = 0
            has_dates = False
            fields = {}
            for fv in item['fieldValues']['nodes']:
                name = fv.get('field', {}).get('name')
                val = fv.get('text') or fv.get('date') or fv.get('name')
                fields[name] = val
                if name in ["Start date", "End date"] and val:
                    score += 10
                    has_dates = True
                if name == "Priority" and val: score += 5
                if name == "Assigned Hours" and val: score += 5
            
            # Sub-issues should NOT be deleted if they are valid children
            is_child = fields.get('Level') == 'Child'
            if is_child:
                print(f"  - Item #{item['content']['number']} is a CHILD. Skipping.")
                continue

            scored_items.append({'item': item, 'score': score, 'has_dates': has_dates, 'num': item['content']['number']})

        # Sort by score descending
        scored_items.sort(key=lambda x: x['score'], reverse=True)
        
        if len(scored_items) > 1:
            golden = scored_items[0]
            print(f"  🏆 GOLDEN: #{golden['num']} (Score: {golden['score']})")
            for other in scored_items[1:]:
                print(f"  🗑️ DELETE: #{other['num']} (Score: {other['score']})")
                to_delete.append(other['item'])
        print()

    # 4. Perform Deletion (Archiving)
    if not to_delete:
        print("No duplicates found to remove.")
        return

    print(f"Proceeding to ARCHIVE {len(to_delete)} duplicate parent items...")
    for item in to_delete:
        issue_num = item['content']['number']
        # 1. Archive from Project 4
        # 2. Delete/Close the Issue itself to be clean
        print(f"Archiving and Closing Issue #{issue_num}...")
        
        # Archive Project Item
        archive_query = """
        mutation($project: ID!, $item: ID!) {
          archiveProjectV2Item(input: {projectId: $project, itemId: $item}) {
            item { id }
          }
        }
        """
        # We need the project ID for Project 4
        P4_ID = "PVT_kwDOA1jKuM4BQoql"
        requests.post("https://api.github.com/graphql", headers=headers, json={"query": archive_query, "variables": {"project": P4_ID, "item": item['id']}})
        
        # Close the actual issue
        repo = item['content']['repository']['name']
        close_url = f"https://api.github.com/repos/{ORG}/{repo}/issues/{issue_num}"
        requests.patch(close_url, headers=headers, json={"state": "closed", "state_reason": "not_planned"})

    print("\n--- CLEANUP COMPLETE ---")

if __name__ == "__main__":
    cleanup_duplicates()
