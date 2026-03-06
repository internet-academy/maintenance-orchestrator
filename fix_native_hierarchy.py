import requests
import os
import re
import time
from dotenv import load_dotenv
from agents.github_specialist import GitHubSpecialist

load_dotenv()

def fix_hierarchy():
    print("--- FIXING NATIVE SUB-ISSUE HIERARCHY ---\n")
    gh = GitHubSpecialist(os.getenv('GITHUB_TOKEN'))
    org = "internet-academy"
    repo = "member"

    # 1. Fetch all items in Project 4 to find sub-issues
    query = """
    query($org: String!) {
      organization(login: $org) {
        projectV2(number: 4) {
          items(first: 100) {
            nodes {
              content {
                ... on Issue {
                  number
                  title
                  id
                }
              }
            }
          }
        }
      }
    }
    """
    response = requests.post(gh.graphql_url, headers=gh.headers, json={"query": query, "variables": {"org": org}})
    items = response.json().get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {}).get('nodes', [])
    
    # 2. Identify Sub-issues and their Parent numbers from title
    # Pattern: "... (Sub-issue for #2565)"
    for item in items:
        content = item.get('content')
        if not content: continue
        
        title = content['title']
        child_number = content['number']
        child_node_id = content['id']
        
        match = re.search(r'Sub-issue for #(\d+)', title)
        if match:
            parent_number = int(match.group(1))
            print(f"Linking Child #{child_number} to Parent #{parent_number}...")
            
            try:
                # Get Parent Node ID
                parent_node_id = gh.get_issue_node_id(repo, parent_number)
                
                # Apply native link
                gh.link_subissue(parent_node_id, child_node_id)
                print(f"  - SUCCESS: Linked natively.\n")
                time.sleep(1)
            except Exception as e:
                print(f"  - ERROR: {e}\n")

if __name__ == "__main__":
    fix_hierarchy()
