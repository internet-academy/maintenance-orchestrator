import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('BACKLOG_API_KEY')
space_id = os.getenv('BACKLOG_SPACE_ID')
project_id = 528169 # MD_SD

url = f"https://{space_id}.backlog.com/api/v2/projects/{project_id}/statuses"
params = {"apiKey": api_key}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    statuses = response.json()
    
    print(f"Statuses for Project {project_id}:")
    for s in statuses:
        print(f"  - {s['name']} (ID: {s['id']})")
except Exception as e:
    print(f"ERROR: {e}")
