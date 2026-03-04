import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')
ORG = "internet-academy"
ISSUE_NUM = 2565

def inspect_issue_in_projects():
    query = """
    query($org: String!, $num: Int!) {
      organization(login: $org) {
        projectV2_3: projectV2(number: 3) {
          title
          items(first: 100) {
            nodes {
              id
              content { ... on Issue { number } }
              fieldValues(first: 20) {
                nodes {
                  ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2Field { name } } }
                  ... on ProjectV2ItemFieldNumberValue { number field { ... on ProjectV2Field { name } } }
                  ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2Field { name } } }
                  ... on ProjectV2ItemFieldDateValue { date field { ... on ProjectV2Field { name } } }
                }
              }
            }
          }
        }
        projectV2_4: projectV2(number: 4) {
          title
          items(first: 100) {
            nodes {
              id
              content { ... on Issue { number } }
              fieldValues(first: 20) {
                nodes {
                  ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2Field { name } } }
                  ... on ProjectV2ItemFieldNumberValue { number field { ... on ProjectV2Field { name } } }
                  ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2Field { name } } }
                  ... on ProjectV2ItemFieldDateValue { date field { ... on ProjectV2Field { name } } }
                }
              }
            }
          }
        }
      }
    }
    """
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.post("https://api.github.com/graphql", headers=headers, json={"query": query, "variables": {"org": ORG, "num": ISSUE_NUM}})
    data = response.json()
    
    org_data = data.get("data", {}).get("organization", {})
    
    for p_key in ["projectV2_3", "projectV2_4"]:
        project = org_data.get(p_key)
        if not project: continue
        print(f"--- Project: {project['title']} ---")
        found = False
        for item in project['items']['nodes']:
            if item.get('content', {}).get('number') == ISSUE_NUM:
                found = True
                print(f"Found Issue #{ISSUE_NUM}:")
                for fv in item['fieldValues']['nodes']:
                    field_name = fv.get('field', {}).get('name')
                    val = fv.get('text') or fv.get('number') or fv.get('name') or fv.get('date')
                    print(f"  - {field_name}: {val}")
        if not found:
            print(f"Issue #{ISSUE_NUM} not found in this project.")
        print()

if __name__ == "__main__":
    inspect_issue_in_projects()
