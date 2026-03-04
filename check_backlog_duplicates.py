import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('BACKLOG_API_KEY')
SPACE_ID = os.getenv('BACKLOG_SPACE_ID')
PROJECT_ID = 528169  # MD_SD
TASK_IDS = [1, 2, 3, 4, 5, 6, 7, 9, 10]

def check_backlog_all():
    if not API_KEY or not SPACE_ID:
        print("Backlog credentials missing.")
        return

    base_url = f"https://{SPACE_ID}.backlog.com/api/v2/issues"
    
    print(f"Checking Backlog space '{SPACE_ID}' for ALL instances of task IDs...\n")
    
    for tid in TASK_IDS:
        params = {
            "apiKey": API_KEY,
            "projectId[]": [PROJECT_ID],
            "keyword": f"ID: {tid}"
        }
        
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            issues = response.json()
            # Verify exact "ID: {tid}" in description or summary
            matches = [i for i in issues if f"ID: {tid}" in (i.get('description') or "") or f"#{tid}" in i.get('summary', '')]
            
            if matches:
                print(f"⚠️ FOUND {len(matches)} matches for Task #{tid}:")
                for m in matches:
                    print(f"  - {m['issueKey']}: {m['summary']} (Created: {m['created']})")
            else:
                print(f"✅ No Backlog match for Task #{tid}")
        else:
            print(f"Error checking Task #{tid}: {response.status_code}")

if __name__ == "__main__":
    check_backlog_all()
