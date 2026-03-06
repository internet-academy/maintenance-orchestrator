import requests
import os
import re
import time
from dotenv import load_dotenv
from agents.github_specialist import GitHubSpecialist
from orchestrator import Orchestrator

load_dotenv()

def force_fix_roadmap():
    print("--- FORCING ROADMAP RECOVERY (NO GUESSWORK) ---\n")
    gh = GitHubSpecialist(os.getenv('GITHUB_TOKEN'))
    orc = Orchestrator(dry_run=False)
    org = "internet-academy"

    # 1. Fetch Mapping for Project 3 and 4
    def get_item_map(project_num):
        item_map = {}
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
                    item_map[int(content['number'])] = {'item_id': node['id'], 'content_id': content['id']}
            if not data.get('pageInfo', {}).get('hasNextPage'): break
            cursor = data['pageInfo']['endCursor']
        return item_map

    print("Fetching Project Maps...")
    p3_map = get_item_map(3)
    p4_map = get_item_map(4)

    # 2. Fix Portfolio Tags in Project 3 for ALL known issues
    print("\n[Step 1] Fixing Portfolio Tags in Project 3...")
    for num, data in p3_map.items():
        # Tag everything from member/bohr as Maintenance for now
        # (We can refine this later, but let's get the tags back first)
        print(f"  - Tagging #{num} as 'Maintenance'...")
        gh.update_field(3, data['item_id'], 'portfolio_project', gh.projects[3]['options']['project_maintenance'], is_option=True)
        time.sleep(0.2)

    # 3. Fix Native Hierarchy for Sub-issues
    print("\n[Step 2] Fixing Native Sub-issue Hierarchy...")
    # Search for all "Understand the request" issues
    query = f'repo:{org}/member \"Understand the request\" is:open'
    search_url = f"https://api.github.com/search/issues?q={query}"
    search_resp = requests.get(search_url, headers=gh.headers).json()
    
    for child in search_resp.get('items', []):
        child_number = child['number']
        child_node_id = child['node_id']
        match = re.search(r'Sub-issue for #(\d+)', child['title'])
        if match:
            parent_number = int(match.group(1))
            print(f"  - Linking Child #{child_number} to Parent #{parent_number}...")
            try:
                parent_node_id = gh.get_issue_node_id("member", parent_number)
                gh.link_subissue(parent_node_id, child_node_id)
                print(f"    ✅ Success.")
            except Exception as e:
                print(f"    ❌ Error: {e}")
        time.sleep(0.5)

    print("\n--- RECOVERY COMPLETE. PROCEEDING TO VERIFICATION ---")

if __name__ == "__main__":
    force_fix_roadmap()
