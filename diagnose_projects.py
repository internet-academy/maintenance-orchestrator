import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')
ORG = "internet-academy"

def diagnose():
    headers = {"Authorization": f"token {TOKEN}"}
    
    # Query to get field types and IDs for both projects
    query = """
    query($org: String!) {
      organization(login: $org) {
        p3: projectV2(number: 3) {
          title
          fields(first: 50) {
            nodes {
              ... on ProjectV2Field { id name dataType }
              ... on ProjectV2IterationField { id name dataType }
              ... on ProjectV2SingleSelectField { id name dataType options { id name } }
            }
          }
        }
        p4: projectV2(number: 4) {
          title
          fields(first: 50) {
            nodes {
              ... on ProjectV2Field { id name dataType }
              ... on ProjectV2IterationField { id name dataType }
              ... on ProjectV2SingleSelectField { id name dataType options { id name } }
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

    projects = data.get("data", {}).get("organization", {})
    for p_key in ["p3", "p4"]:
        p = projects.get(p_key)
        if not p: continue
        print(f"=== {p['title']} (Project {p_key[1:]}) ===")
        for field in p['fields']['nodes']:
            print(f"- {field['name']} (ID: {field['id']}, Type: {field.get('dataType')})")
            if 'options' in field:
                for opt in field['options']:
                    print(f"  * {opt['name']} (ID: {opt['id']})")
        print()

if __name__ == "__main__":
    diagnose()
