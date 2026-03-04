import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')
ORG = "internet-academy"
PROJECT_NUMBER = 4

headers = {"Authorization": f"token {TOKEN}"}

query = """
query($org: String!, $number: Int!) {
  organization(login: $org) {
    projectV2(number: $number) {
      id
      title
      fields(first: 20) {
        nodes {
          ... on ProjectV2Field {
            id
            name
          }
          ... on ProjectV2IterationField {
            id
            name
          }
          ... on ProjectV2SingleSelectField {
            id
            name
            options {
              id
              name
            }
          }
        }
      }
    }
  }
}
"""

def main():
    if not TOKEN:
        print("GITHUB_TOKEN missing!")
        return

    response = requests.post(
        "https://api.github.com/graphql",
        headers=headers,
        json={"query": query, "variables": {"org": ORG, "number": PROJECT_NUMBER}}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"DEBUG: Response data: {data}")
        project = data.get("data", {}).get("organization", {}).get("projectV2")
        if project:
            print(f"Project Title: {project['title']}")
            print(f"Project Node ID: {project['id']}")
            print("\nFields:")
            for field in project['fields']['nodes']:
                print(f"- {field['name']} (ID: {field['id']})")
                if 'options' in field:
                    for opt in field['options']:
                        print(f"  * {opt['name']} (ID: {opt['id']})")
        else:
            print("Project not found.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()
