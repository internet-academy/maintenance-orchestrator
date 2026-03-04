import os
import re
import json
from github import Github

class GitSync:
    def __init__(self, github_token, ingestor, dry_run=False):
        self.gh = Github(github_token)
        self.ingestor = ingestor
        self.dry_run = dry_run
        
        self.state_file = "git_sync_state.json"
        self.state = self._load_state()

    def _load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f: return json.load(f)
            except: return {}
        return {}

    def _save_state(self):
        with open(self.state_file, 'w') as f: json.dump(self.state, f, indent=2)

    def scan_and_sync(self, tasks):
        """
        Scans current tasks and checks their GitHub status to update the Sheet.
        """
        print(f"GIT: Checking status for {len(tasks)} tasks...")
        
        for task in tasks:
            issue_url = task.get('backlog_id') # Legacy key name
            if not issue_url or "github.com" not in issue_url:
                continue
            
            # Extract Repo and Number
            match = re.search(r'github\.com/([^/]+)/([^/]+)/issues/(\d+)', issue_url)
            if not match: continue
            
            owner, repo_name, number = match.groups()
            
            try:
                repo = self.gh.get_repo(f"{owner}/{repo_name}")
                issue = repo.get_issue(int(number))
                
                # Logic: If issue is closed, Sheet status = "Complete!"
                # If issue has a linked PR (complex via REST, but we can check for keywords/events), status = "In Progress"
                
                current_sheet_status = task.get('current_sheet_status', '')
                
                if issue.state == "closed":
                    if current_sheet_status != "Complete!":
                        print(f"SYNC: GitHub {number} Closed -> Sheet Complete!")
                        if not self.dry_run:
                            self.ingestor.write_status(task['anchors'], "Complete!")
                else:
                    # Check for PR activity (linked pull requests)
                    # We can use the 'events' or just look for keywords in comments
                    # For now, if it's open, it's "In Progress" in our workflow
                    if current_sheet_status == "Waiting for Dev" or current_sheet_status == "Open":
                         if issue.assignees:
                            print(f"SYNC: GitHub {number} Assigned -> Sheet In Progress")
                            if not self.dry_run:
                                self.ingestor.write_status(task['anchors'], "In Progress")

            except Exception as e:
                print(f"GIT ERROR: Failed to sync {issue_url}: {e}")
