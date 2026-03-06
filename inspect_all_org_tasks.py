import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')
ORG = "internet-academy"

def inspect_all():
    headers = {"Authorization": f"token {TOKEN}"}
    
    # 1. First, let's just see what issues are open in the member repo
    print("--- Open Issues in internet-academy/member ---")
    url = f"https://api.github.com/repos/{ORG}/member/issues?state=open&per_page=50"
    resp = requests.get(url, headers=headers)
    issues = resp.json()
    
    for i in issues:
        # Skip PRs
        if 'pull_request' in i: continue
        print(f"#{i['number']}: {i['title']} (Assignees: {[a['login'] for a in i['assignees']]})")

    # 2. Now let's see why the Project query might be missing them
    print("\n--- ProjectV2 Items Diagnostic ---")
    query = """
    query($org: String!) {
      organization(login: $org) {
        projectsV2(first: 20) {
          nodes {
            number
            title
            items(first: 20) {
              nodes {
                content {
                  ... on Issue { number title closed }
                }
                fieldValues(first: 20) {
                  nodes {
                    ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2Field { name } } }
                    ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2Field { name } } }
                  }
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
    
    projects = data.get('data', {}).get('organization', {}).get('projectsV2', {}).get('nodes', [])
    for p in projects:
        print(f"\nProject: {p['title']} (#{p['number']})")
        items = p['items']['nodes']
        if not items:
            print("  (No items)")
            continue
        for item in items:
            content = item.get('content')
            if not content: continue
            
            fields = {fv.get('field', {}).get('name'): (fv.get('text') or fv.get('name')) for fv in item['fieldValues']['nodes'] if fv.get('field')}
            print(f"  - #{content.get('number')}: {content.get('title')[:40]}...")
            print(f"    Status: {fields.get('Status')} | Level: {fields.get('Level')} | Closed: {content.get('closed')}")

if __name__ == "__main__":
    inspect_all()
