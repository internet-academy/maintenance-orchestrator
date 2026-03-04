import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')
ORG = "internet-academy"
PROJECT_ID = "PVT_kwDOA1jKuM4BQoor" # Project 3

def create_fields():
    headers = {"Authorization": f"token {TOKEN}"}
    fields_to_create = [
        {"name": "Start date", "type": "DATE"},
        {"name": "End date", "type": "DATE"}
    ]
    
    created_fields = {}
    
    for field in fields_to_create:
        print(f"Creating field '{field['name']}'...")
        query = """
        mutation($projectId: ID!, $name: String!, $dataType: ProjectV2CustomFieldType!) {
          createProjectV2Field(input: {projectId: $projectId, name: $name, dataType: $dataType}) {
            projectV2Field {
              ... on ProjectV2Field {
                id
                name
              }
            }
          }
        }
        """
        variables = {
            "projectId": PROJECT_ID,
            "name": field['name'],
            "dataType": field['type']
        }
        
        response = requests.post("https://api.github.com/graphql", headers=headers, json={"query": query, "variables": variables})
        data = response.json()
        
        if "errors" in data:
            # Check if it already exists
            if any("already exists" in err.get('message', '').lower() for err in data['errors']):
                print(f"Field '{field['name']}' already exists. Skipping creation.")
            else:
                print(f"Error creating '{field['name']}':", json.dumps(data["errors"], indent=2))
        else:
            field_data = data.get("data", {}).get("createProjectV2Field", {}).get("projectV2Field", {})
            print(f"Successfully created '{field['name']}' (ID: {field_data.get('id')})")
            created_fields[field['name']] = field_data.get('id')
            
    return created_fields

if __name__ == "__main__":
    create_fields()
