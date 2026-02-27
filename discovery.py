import requests
import os
import json
from dotenv import load_dotenv

# To run this locally:
# 1. Create a .env file with BACKLOG_API_KEY and BACKLOG_SPACE_ID
# 2. Or set them in your terminal: export BACKLOG_API_KEY=your_key
load_dotenv()

def discover_backlog_ids():
    api_key = os.getenv('BACKLOG_API_KEY')
    space_id = os.getenv('BACKLOG_SPACE_ID')

    if not api_key or not space_id:
        print("ERROR: Please set BACKLOG_API_KEY and BACKLOG_SPACE_ID environment variables.")
        return

    base_url = f"https://{space_id}.backlog.com/api/v2"
    
    print(f"--- Discovery for Space: {space_id} ---")

    # 1. Discover Projects
    print("\n[PROJECTS]")
    try:
        proj_resp = requests.get(f"{base_url}/projects", params={"apiKey": api_key})
        proj_resp.raise_for_status()
        for p in proj_resp.json():
            print(f"ID: {p['id']} | Name: {p['name']} | Key: {p['projectKey']}")
    except Exception as e:
        print(f"Could not fetch projects: {e}")

    # 2. Discover Users (Developers)
    print("\n[USERS / DEVELOPERS]")
    try:
        user_resp = requests.get(f"{base_url}/users", params={"apiKey": api_key})
        user_resp.raise_for_status()
        for u in user_resp.json():
            print(f"ID: {u['id']} | Name: {u['name']} | Role: {u['roleType']}")
    except Exception as e:
        print(f"Could not fetch users: {e}")

    # 3. Discover Issue Types (To find 'Bug' or 'Task' ID)
    print("
[ISSUE TYPES (Run this after finding your Project ID)]")
    print("Set PROJECT_ID_OR_KEY env var to see issue types for a specific project.")
    proj_id = os.getenv('PROJECT_ID_OR_KEY')
    if proj_id:
        try:
            type_resp = requests.get(f"{base_url}/projects/{proj_id}/issueTypes", params={"apiKey": api_key})
            type_resp.raise_for_status()
            for t in type_resp.json():
                print(f"ID: {t['id']} | Name: {t['name']}")
        except Exception as e:
            print(f"Could not fetch issue types: {e}")

if __name__ == "__main__":
    discover_backlog_ids()
