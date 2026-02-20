
import os
import requests
from dotenv import load_dotenv

load_dotenv('/home/min/projects/personal-agents/.env')

def get_users():
    api_key = os.getenv('BACKLOG_API_KEY')
    space_id = os.getenv('BACKLOG_SPACE_ID')
    base_url = f"https://{space_id}.backlog.jp/api/v2"
    
    endpoint = f"{base_url}/users"
    params = {"apiKey": api_key}
    
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    users = response.json()
    
    print("--- Backlog User Discovery ---")
    for user in users:
        print(f"Name: {user['name']} | ID: {user['id']} | Role: {user.get('roleType')}")

if __name__ == "__main__":
    get_users()
