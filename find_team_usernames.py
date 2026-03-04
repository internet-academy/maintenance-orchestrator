import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')
ORG = "internet-academy"
TARGETS = ["Saurabh", "Raman", "Ewan", "Choo"]

headers = {"Authorization": f"token {TOKEN}"}

def main():
    if not TOKEN:
        print("GITHUB_TOKEN missing!")
        return

    # List organization members (login only)
    url = f"https://api.github.com/orgs/{ORG}/members?per_page=100"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching members: {response.status_code}")
        return

    members = response.json()
    print(f"Scanning {len(members)} organization members...\n")

    for member in members:
        login = member['login']
        # Fetch full profile for each member to see their real name
        profile_url = f"https://api.github.com/users/{login}"
        profile = requests.get(profile_url, headers=headers).json()
        
        real_name = profile.get('name') or "No Name"
        
        # Match against our targets
        for target in TARGETS:
            if target.lower() in real_name.lower() or target.lower() in login.lower():
                print(f"MATCH FOUND: {target}")
                print(f"- Login: {login}")
                print(f"- Name:  {real_name}")
                print(f"- URL:   {profile.get('html_url')}")
                print("-" * 20)

if __name__ == "__main__":
    main()
