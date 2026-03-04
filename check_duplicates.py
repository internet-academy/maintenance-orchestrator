import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')
ORG = "internet-academy"
REPO = "member"
TASK_IDS = [1, 2, 3, 4, 5, 6, 7, 9, 10]

def check_github_for_duplicates():
    headers = {"Authorization": f"token {TOKEN}"}
    duplicates = []
    
    print(f"Checking GitHub {ORG}/{REPO} for existing task IDs...\n")
    
    for tid in TASK_IDS:
        # Search for "ID: {tid}" in the repository
        query = f"repo:{ORG}/{REPO} \"ID: {tid}\" is:issue"
        url = f"https://api.github.com/search/issues?q={query}"
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            count = data.get('total_count', 0)
            if count > 0:
                issue = data['items'][0]
                print(f"⚠️ MATCH FOUND for Task #{tid}: {issue['html_url']} (Status: {issue['state']})")
                duplicates.append(tid)
            else:
                print(f"✅ No existing GitHub issue for Task #{tid}")
        else:
            print(f"Error searching for Task #{tid}: {response.status_code}")
            
    return duplicates

if __name__ == "__main__":
    check_github_for_duplicates()
