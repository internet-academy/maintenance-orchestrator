import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')
ORG = "internet-academy"
PROJECT_NUMBER = 4

def inspect_items():
    query = """
    query($org: String!, $number: Int!) {
      organization(login: $org) {
        projectV2(number: $number) {
          items(first: 20) {
            nodes {
              id
              fieldValues(first: 20) {
                nodes {
                  ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2Field { name id } } }
                  ... on ProjectV2ItemFieldNumberValue { number field { ... on ProjectV2Field { name id } } }
                  ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2Field { name id } } }
                  ... on ProjectV2ItemFieldDateValue { date field { ... on ProjectV2Field { name id } } }
                  ... on ProjectV2ItemFieldIterationValue { title field { ... on ProjectV2Field { name id } } }
                }
              }
              content {
                ... on Issue {
                  title
                  number
                  assignees(first: 10) { nodes { login } }
                  closed
                }
              }
            }
          }
        }
      }
    }
    """
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.post("https://api.github.com/graphql", headers=headers, json={"query": query, "variables": {"org": ORG, "number": PROJECT_NUMBER}})
    data = response.json()
    
    items = data.get("data", {}).get("organization", {}).get("projectV2", {}).get("items", {}).get("nodes", [])
    print(f"Inspecting {len(items)} items in Project 4:\n")
    
    for item in items:
        content = item.get("content", {})
        title = content.get("title", "No Title")
        assignees = [a['login'] for a in content.get("assignees", {}).get("nodes", [])] if content else []
        
        print(f"Item: {title} (Assignees: {assignees})")
        for fv in item.get("fieldValues", {}).get("nodes", []):
            field_name = fv.get("field", {}).get("name")
            val = fv.get("text") or fv.get("number") or fv.get("name") or fv.get("date") or fv.get("title")
            print(f"  - {field_name}: {val}")
        print("-" * 20)

if __name__ == "__main__":
    inspect_items()
