import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')
ORG = "internet-academy"

def verify_healing():
    print("=== FINAL HIERARCHY VERIFICATION: PROJECT 4 ===\n")
    headers = {"Authorization": f"token {TOKEN}"}
    
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
                  parent { number }
                }
              }
              fieldValues(first: 20) {
                nodes {
                  ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2Field { name } } }
                }
              }
            }
          }
        }
      }
    }
    """
    
    resp = requests.post("https://api.github.com/graphql", headers=headers, json={"query": query, "variables": {"org": ORG}})
    data = resp.json()
    items = data.get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {}).get('nodes', [])
    
    orphans = []
    linked = []
    
    for item in items:
        content = item.get('content')
        if not content: continue
        
        fields = {fv['field']['name']: fv['name'] for fv in item['fieldValues']['nodes'] if fv.get('field')}
        level = fields.get('Level')
        parent = content.get('parent')
        
        if level == "Child" or "Understand the request" in content['title']:
            if not parent:
                orphans.append(f"#{content['number']} - {content['title']}")
            else:
                linked.append(f"#{content['number']} (Parent: #{parent['number']})")

    print(f"Total Sub-issues Scanned: {len(orphans) + len(linked)}")
    print(f"✅ Successfully Linked:  {len(linked)}")
    print(f"❌ Still Orphaned:       {len(orphans)}")
    
    if orphans:
        print("\nOrphan List:")
        for o in orphans: print(f"  - {o}")
    
    if len(orphans) == 0:
        print("\n✅ VERIFICATION SUCCESS: All child issues are properly linked.")
    else:
        print("\n❌ VERIFICATION FAILURE: Healing is not persisting.")

if __name__ == "__main__":
    verify_healing()
