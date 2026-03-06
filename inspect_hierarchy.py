import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')
ORG = "internet-academy"

def inspect_hierarchy():
    headers = {"Authorization": f"token {TOKEN}"}
    
    # Query to fetch items from Project 4 and check their sub-issue relationship
    query = """
    query($org: String!) {
      organization(login: $org) {
        projectV2(number: 4) {
          items(first: 50) {
            nodes {
              id
              content {
                ... on Issue {
                  number
                  title
                  subIssues(first: 10) {
                    nodes {
                      number
                      title
                    }
                  }
                  parent {
                    number
                    title
                  }
                }
              }
              fieldValues(first: 20) {
                nodes {
                  ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2Field { name } } }
                  ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2Field { name } } }
                }
              }
            }
          }
        }
      }
    }
    """
    
    response = requests.post("https://api.github.com/graphql", headers=headers, json={"query": query, "variables": {"org": ORG}})
    data = response.json()
    
    if "errors" in data:
        print("GraphQL Errors:", json.dumps(data["errors"], indent=2))
        return

    items = data.get("data", {}).get("organization", {}).get("projectV2", {}).get("items", {}).get("nodes", [])
    
    print(f"Inspecting {len(items)} items in Project 4 hierarchy...\n")
    
    for item in items:
        content = item.get('content')
        if not content: continue
        
        title = content.get('title')
        num = content.get('number')
        
        # Check native GitHub relationship
        parent = content.get('parent')
        sub_issues = content.get('subIssues', {}).get('nodes', [])
        
        # Check Project Fields
        fields = {fv.get('field', {}).get('name'): (fv.get('text') or fv.get('name')) for fv in item['fieldValues']['nodes']}
        level = fields.get('Level')
        project_parent = fields.get('Parent issue')
        
        if "Understand the request" in title or level == "Child":
            print(f"CHILD: #{num} - {title}")
            print(f"  - Native Parent: {'#' + str(parent['number']) if parent else 'NONE'}")
            print(f"  - Project 'Parent issue' field: {project_parent or 'EMPTY'}")
            print("-" * 20)
        elif level == "Parent":
            print(f"PARENT: #{num} - {title}")
            print(f"  - Native Children: {[s['number'] for s in sub_issues] if sub_issues else 'NONE'}")
            print("-" * 20)

if __name__ == "__main__":
    inspect_hierarchy()
