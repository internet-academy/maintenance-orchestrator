import os
import re
import json
import requests
from github import Github

class GitSync:
    def __init__(self, github_token, ingestor, dry_run=False):
        self.gh_client = Github(github_token)
        self.ingestor = ingestor
        self.dry_run = dry_run
        
        from agents.github_specialist import GitHubSpecialist
        self.gh_specialist = GitHubSpecialist(github_token, dry_run=dry_run)

    def scan_and_sync(self, tasks):
        """Pulls Status, PIC, and Dates from GitHub Project and updates the Sheet."""
        print(f"GIT: Syncing {len(tasks)} tasks from GitHub to Sheet...")
        stats = {"status_changes": 0, "pic_updates": 0, "date_migrations": 0, "healed_links": 0}

        user_to_name = {
            os.getenv('GH_USER_SAURABH', 'Saurabh-IA').lower(): "Saurabh",
            os.getenv('GH_USER_RAMAN', 'RmnSoni').lower(): "Raman",
            os.getenv('GH_USER_EWAN', 'Froggyyyyyyy').lower(): "Ewan",
            os.getenv('GH_USER_CHOO', 'young-min-choo').lower(): "Choo"
        }

        for task in tasks:
            issue_url = task.get('backlog_id')
            if not issue_url or "github.com" not in issue_url: continue
            
            match = re.search(r'/issues/(\d+)', issue_url)
            if not match: continue
            issue_num = int(match.group(1))
            
            try:
                gh_data = self.gh_specialist.get_project_item_data(issue_num, project_number=4)
                if not gh_data: continue
                
                gh_status = gh_data.get('Status')
                sheet_status = task.get('current_sheet_status', '')

                # --- PR DETECTION ENGINE ---
                has_active_pr = False
                has_merged_pr = False
                try:
                    # Search for OPEN PRs
                    pr_query = f'repo:{self.gh_specialist.org}/member "{issue_num}" is:pr is:open'
                    pr_search = self.gh_client.search_issues(query=pr_query)
                    if pr_search.totalCount > 0:
                        has_active_pr = True
                    
                    # Search for MERGED PRs
                    merged_query = f'repo:{self.gh_specialist.org}/member "{issue_num}" is:pr is:merged'
                    merged_search = self.gh_client.search_issues(query=merged_query)
                    if merged_search.totalCount > 0:
                        has_merged_pr = True
                except: pass

                new_sheet_status = None
                if gh_status == "Done" or has_merged_pr: 
                    # If merged or Project is Done, it's ready for client review/verification
                    new_sheet_status = "pending review"
                elif gh_status == "In progress" or has_active_pr: 
                    new_sheet_status = "in progress"
                elif gh_status in ["To Triage", "Backlog", "Ready"]: 
                    new_sheet_status = "not started"

                
                if new_sheet_status and new_sheet_status != sheet_status:
                    print(f"  - SYNC: Issue #{issue_num} Status: {gh_status} -> Sheet: {new_sheet_status}")
                    if not self.dry_run:
                        self.ingestor.write_status(task['anchors'], new_sheet_status)
                        stats["status_changes"] += 1

                gh_assignee = (gh_data.get('assignee') or "").lower()
                current_pic = task.get('pic', '')
                new_pic_name = user_to_name.get(gh_assignee)
                if new_pic_name and new_pic_name != current_pic:
                    print(f"  - SYNC: Issue #{issue_num} Assignee: {gh_assignee} -> Sheet: {new_pic_name}")
                    if not self.dry_run:
                        self.ingestor.write_pic(task['anchors'], new_pic_name)
                        stats["pic_updates"] += 1

                # 5. BIDIRECTIONAL DATE SYNC (P4 <-> P3 <-> Sheet)
                p4_start = gh_data.get('Start date')
                p4_end = gh_data.get('End date')
                
                # Fetch Project 3 Data for comparison
                p3_data = self.gh_specialist.get_project_item_data(issue_num, project_number=3)
                p3_start = p3_data.get('Start date') if p3_data else None
                p3_end = p3_data.get('End date') if p3_data else None

                # SYNC LOGIC:
                # 1. If P4 has dates and P3 doesn't (or they differ) -> Mirror P4 to P3
                if p4_start and p4_end:
                    if p4_start != p3_start or p4_end != p3_end:
                        if p3_data:
                            print(f"  - DATE SYNC: Mirroring P4 Dates to P3 for #{issue_num}")
                            if not self.dry_run:
                                self.gh_specialist.update_field(3, p3_data['item_id'], 'start_date', p4_start)
                                self.gh_specialist.update_field(3, p3_data['item_id'], 'end_date', p4_end)
                                stats["date_migrations"] += 1
                    
                    # Also sync to Google Sheet
                    if not self.dry_run:
                        self.ingestor.write_dates(task['anchors'], p4_start, p4_end)

                # 2. If P3 has dates and P4 doesn't -> Mirror P3 to P4
                elif p3_start and p3_end and not (p4_start and p4_end):
                    print(f"  - DATE SYNC: Mirroring P3 Dates to P4 for #{issue_num}")
                    if not self.dry_run:
                        self.gh_specialist.update_field(4, gh_data['item_id'], 'start_date', p3_start)
                        self.gh_specialist.update_field(4, gh_data['item_id'], 'end_date', p3_end)
                        self.ingestor.write_dates(task['anchors'], p3_start, p3_end)
                        stats["date_migrations"] += 1

                # 6. HEALING & CASCADING
                try:
                    parent_title = gh_data.get('Title')
                    child_search_query = f'repo:{self.gh_specialist.org}/member "Sub-issue for #{issue_num}" is:open'
                    search_results = self.gh_client.search_issues(query=child_search_query)
                    
                    for child in search_results:
                        if f"Sub-issue for #{issue_num}" in child.title:
                            print(f"    - HEALING: Natively linking Child #{child.number} to Parent #{issue_num}")
                            
                            # ROBUST LINK: Re-open parent if closed (linking requires parent to be open)
                            repo_obj = self.gh_client.get_repo(f"{self.gh_specialist.org}/member")
                            parent_issue_obj = repo_obj.get_issue(issue_num)
                            
                            was_closed = parent_issue_obj.state == "closed"
                            if was_closed:
                                parent_issue_obj.edit(state="open")
                            
                            self.gh_specialist.link_subissue(
                                self.gh_specialist.get_issue_node_id("member", issue_num),
                                child.node_id
                            )
                            
                            if was_closed:
                                parent_issue_obj.edit(state="closed")

                            # STATUS CASCADING: If Parent is Done, close the sub-issue
                            if gh_status == "Done":
                                print(f"    - CASCADING: Closing sub-issue #{child.number} because Parent #{issue_num} is Done.")
                                child.edit(state='closed', state_reason='completed')
                            
                            stats["healed_links"] += 1
                except Exception as e:
                    print(f"DEBUG: Hierarchy healing failed for #{issue_num}: {e}")

            except Exception as e:
                print(f"GIT SYNC ERROR for Issue #{issue_num}: {e}")
        
        return stats
