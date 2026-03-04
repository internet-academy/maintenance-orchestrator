import requests
import os
import re
import json
from github import Github

class GitSync:
    def __init__(self, github_token, ingestor, dry_run=False):
        self.gh_client = Github(github_token)
        self.ingestor = ingestor
        self.dry_run = dry_run
        
        # We need the GitHubSpecialist's specialized GraphQL logic here
        from agents.github_specialist import GitHubSpecialist
        self.gh_specialist = GitHubSpecialist(github_token, dry_run=dry_run)

    def scan_and_sync(self, tasks):
        """
        Pulls Status, PIC, and Dates from GitHub Project and updates the Sheet.
        """
        print(f"GIT: Syncing {len(tasks)} tasks from GitHub to Sheet...")
        
        # Build Name -> Human Name map for PIC write-back
        # (Inverse of developer_map in orchestrator)
        user_to_name = {
            os.getenv('GH_USER_SAURABH', 'Saurabh-IA').lower(): "Saurabh",
            os.getenv('GH_USER_RAMAN', 'RmnSoni').lower(): "Raman",
            os.getenv('GH_USER_EWAN', 'Froggyyyyyyy').lower(): "Ewan",
            os.getenv('GH_USER_CHOO', 'young-min-choo').lower(): "Choo"
        }

        for task in tasks:
            issue_url = task.get('backlog_id')
            if not issue_url or "github.com" not in issue_url:
                continue
            
            # Extract Issue Number
            match = re.search(r'/issues/(\d+)', issue_url)
            if not match: continue
            issue_num = int(match.group(1))
            
            try:
                # 1. Fetch live data from GitHub Project 4 (Maintenance)
                gh_data = self.gh_specialist.get_project_item_data(issue_num, project_number=4)
                if not gh_data:
                    continue
                
                # 2. Map GitHub Status to Sheet Display
                gh_status = gh_data.get('Status')
                sheet_status = task.get('current_sheet_status', '')
                
                new_sheet_status = None
                if gh_status == "Done":
                    new_sheet_status = "Complete!"
                elif gh_status == "In progress":
                    new_sheet_status = "In Progress"
                elif gh_status in ["To Triage", "Backlog", "Ready"]:
                    new_sheet_status = "Open"
                
                # 3. Apply Status Update
                if new_sheet_status and new_sheet_status != sheet_status:
                    print(f"  - SYNC: Issue #{issue_num} Status: {gh_status} -> Sheet: {new_sheet_status}")
                    if not self.dry_run:
                        self.ingestor.write_status(task['anchors'], new_sheet_status)

                # 4. Pull PIC/Assignee
                gh_assignee = (gh_data.get('assignee') or "").lower()
                current_pic = task.get('pic', '')
                new_pic_name = user_to_name.get(gh_assignee)
                
                if new_pic_name and new_pic_name != current_pic:
                    print(f"  - SYNC: Issue #{issue_num} Assignee: {gh_assignee} -> Sheet: {new_pic_name}")
                    if not self.dry_run:
                        self.ingestor.write_pic(task['anchors'], new_pic_name)

                # 5. Pull Dates from Project 4
                gh_start = gh_data.get('Start date')
                gh_end = gh_data.get('End date')
                
                if gh_start and gh_end:
                    if not self.dry_run:
                        self.ingestor.write_dates(task['anchors'], gh_start, gh_end)
                        
                        # --- AUTO-SYNC TO PROJECT 3 ---
                        # If we have dates in P4, ensure they exist in P3 too
                        try:
                            p3_data = self.gh_specialist.get_project_item_data(issue_num, project_number=3)
                            if p3_data and (not p3_data.get('Start date') or not p3_data.get('End date')):
                                print(f"  - AUTO-SYNC: Copying dates for #{issue_num} from P4 to P3")
                                self.gh_specialist.update_field(3, p3_data['item_id'], 'start_date', gh_start)
                                self.gh_specialist.update_field(3, p3_data['item_id'], 'end_date', gh_end)
                        except Exception as e:
                            print(f"DEBUG: P3 auto-sync failed for #{issue_num}: {e}")

            except Exception as e:
                print(f"GIT SYNC ERROR for Issue #{issue_num}: {e}")
