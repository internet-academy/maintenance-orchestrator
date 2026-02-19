
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def test_connection():
    api_key = os.getenv('BACKLOG_API_KEY')
    space_id = os.getenv('BACKLOG_SPACE_ID')
    project_id = os.getenv('BACKLOG_PROJECT_ID')

    if not all([api_key, space_id]):
        print("ERROR: BACKLOG_API_KEY and BACKLOG_SPACE_ID must be set.")
        return

    base_url = f"https://{space_id}.backlog.com/api/v2"
    
    # 1. Test Project Access
    print(f"--- Testing Connection to Space: {space_id} ---")
    try:
        if project_id:
            endpoint = f"{base_url}/projects/{project_id}"
            params = {"apiKey": api_key}
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            project = response.json()
            print(f"SUCCESS: Accessed Project '{project['name']}' ({project['id']})")
        else:
            # If no project_id, just list projects
            endpoint = f"{base_url}/projects"
            params = {"apiKey": api_key}
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            projects = response.json()
            print(f"SUCCESS: Connected. Found {len(projects)} projects.")
            if projects:
                print(f"Example Project: {projects[0]['name']} (ID: {projects[0]['id']})")

        # 2. Test Issue Retrieval & Load Calculation
        print("\n--- Testing Load Calculation ---")
        # For testing, we'll look for issues in the first project found or the specified one
        pid = project_id or (projects[0]['id'] if projects else None)
        if pid:
            endpoint = f"{base_url}/issues"
            params = {
                "apiKey": api_key,
                "projectId[]": [pid],
                "statusId[]": [1, 2, 3], # Open, In Progress, Resolved
            }
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            issues = response.json()
            
            print(f"Found {len(issues)} active issues.")
            total_hours = 0
            for issue in issues:
                est_raw = issue.get("estimatedHours")
                try:
                    est = float(est_raw) if est_raw is not None else 0.0
                except (ValueError, TypeError):
                    print(f"  ! Warning: Invalid estimate '{est_raw}' for issue {issue['issueKey']}. Defaulting to 0.")
                    est = 0.0
                
                total_hours += est
                print(f"- Issue {issue['issueKey']}: {est} hours")
            
            print(f"\nTOTAL CALCULATED LOAD: {total_hours} hours")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP ERROR: {e}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_connection()
