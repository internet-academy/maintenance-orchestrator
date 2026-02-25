import os
import re
from github import Github
from agents.load_balancer import LoadBalancer

class GitSync:
    def __init__(self, github_token, backlog_api_key, backlog_space_id, dry_run=False):
        self.gh = Github(github_token)
        self.load_balancer = LoadBalancer(backlog_api_key, backlog_space_id)
        self.dry_run = dry_run
        
        # Backlog Status IDs for MD_SD Project (528169)
        self.STATUS_OPEN = 1
        self.STATUS_IN_PROGRESS = 2
        self.STATUS_RESOLVED = 3
        self.STATUS_PENDING_RELEASE = 307448 
        self.STATUS_PENDING_REPORT = 333305
        self.PROJECT_ID = 528169

    def scan_and_sync(self, repo_name):
        """
        Scans recent Pull Requests in a repository and updates Backlog.
        """
        print(f"GIT: Scanning repository {repo_name}...")
        try:
            repo = self.gh.get_repo(repo_name)
        except Exception as e:
            print(f"GIT ERROR: Could not access repo {repo_name}: {e}")
            return
        
        # 1. Handle Open PRs -> Pending Release
        open_prs = repo.get_pulls(state='open', sort='created', direction='desc')
        for pr in open_prs:
            # Check PR title and branch name for issue keys
            search_text = f"{pr.title} {pr.head.ref}"
            issue_keys = self._extract_issue_keys(search_text)
            
            for key in issue_keys:
                self._update_backlog_status(key, self.STATUS_PENDING_RELEASE, f"PR Open: {pr.html_url}")

        # 2. Handle Merged PRs -> Pending Report
        closed_prs = repo.get_pulls(state='closed', sort='updated', direction='desc')[:15]
        for pr in closed_prs:
            if pr.merged:
                search_text = f"{pr.title} {pr.head.ref}"
                issue_keys = self._extract_issue_keys(search_text)
                
                for key in issue_keys:
                    self._update_backlog_status(key, self.STATUS_PENDING_REPORT, f"PR Merged: {pr.html_url}")

    def _extract_issue_keys(self, text):
        """Extracts Backlog issue keys like MD_SD-123 from text."""
        # Case-insensitive match for project key followed by dash and numbers
        keys = re.findall(r'MD_SD-\d+', text, re.IGNORECASE)
        # Standardize to uppercase
        return list(set(k.upper() for k in keys))

    def _update_backlog_status(self, issue_key, target_status_id, context_msg):
        """Updates the status of a Backlog issue if it moves it forward."""
        try:
            issue = self.load_balancer.get_issue(issue_key)
            current_status_id = issue.get('status', {}).get('id')
            
            # Status Progression Map (Prevent Reverting)
            # Only allow moving "Forward"
            # 1 (Open) -> 2 (In Progress) -> 3 (Resolved) -> 307448 (Release) -> 333305 (Report)
            
            progression = {
                self.STATUS_OPEN: 1,
                self.STATUS_IN_PROGRESS: 2,
                self.STATUS_RESOLVED: 3,
                self.STATUS_PENDING_RELEASE: 4,
                self.STATUS_PENDING_REPORT: 5
            }
            
            current_rank = progression.get(current_status_id, 0)
            target_rank = progression.get(target_status_id, 0)
            
            if target_rank > current_rank:
                print(f"GIT: Moving {issue_key} {current_status_id} -> {target_status_id} ({context_msg})")
                if self.dry_run:
                    print(f"[DRY RUN] Would update {issue_key} status to {target_status_id}")
                else:
                    self.load_balancer.update_issue_status(issue_key, target_status_id)
            else:
                # print(f"GIT: Skip {issue_key} (Already at rank {current_rank}, target was {target_rank})")
                pass
                
        except Exception as e:
            print(f"GIT ERROR: Failed to update {issue_key}: {e}")
