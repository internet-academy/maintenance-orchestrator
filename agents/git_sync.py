import os
import re
from github import Github
from agents.load_balancer import LoadBalancer

class GitSync:
    def __init__(self, github_token, backlog_api_key, backlog_space_id):
        self.gh = Github(github_token)
        self.load_balancer = LoadBalancer(backlog_api_key, backlog_space_id)
        
        # Backlog Status IDs for MD_SD Project (528169)
        # TODO: Verify these IDs
        self.STATUS_PENDING_RELEASE = None 
        self.STATUS_PENDING_REPORT = None
        self.PROJECT_ID = 528169

    def scan_and_sync(self, repo_name):
        """
        Scans recent Pull Requests in a repository and updates Backlog.
        """
        print(f"GIT: Scanning repository {repo_name}...")
        repo = self.gh.get_repo(repo_name)
        
        # 1. Handle Open PRs -> Pending Release
        open_prs = repo.get_pulls(state='open', sort='created', direction='desc')
        for pr in open_prs:
            issue_keys = self._extract_issue_keys(pr.title + " " + pr.head.ref)
            for key in issue_keys:
                self._update_backlog_status(key, "Pending Release")

        # 2. Handle Merged PRs -> Pending Report
        # Note: We only look at recently merged PRs to avoid redundant API calls
        # For simplicity in this prototype, we'll check the last 10 merged PRs
        closed_prs = repo.get_pulls(state='closed', sort='updated', direction='desc')[:10]
        for pr in closed_prs:
            if pr.merged:
                issue_keys = self._extract_issue_keys(pr.title + " " + pr.head.ref)
                for key in issue_keys:
                    self._update_backlog_status(key, "Pending Report")

    def _extract_issue_keys(self, text):
        """Extracts Backlog issue keys like MD_SD-123 from text."""
        # Pattern: ProjectKey-Number (e.g., MD_SD-1234)
        return re.findall(r'[A-Z0-9_]+-\d+', text)

    def _update_backlog_status(self, issue_key, target_status_name):
        """Updates the status of a Backlog issue if it's not already correct."""
        # This will require mapping status names to IDs
        print(f"GIT: Would move {issue_key} to {target_status_name}")
        # Implementation details depend on the status ID discovery
