import os
import re
from github import Github
from agents.load_balancer import LoadBalancer

class GitSync:
    def __init__(self, github_token, backlog_api_key, backlog_space_id, dry_run=False):
        self.gh = Github(github_token)
        self.load_balancer = LoadBalancer(backlog_api_key, backlog_space_id)
        self.dry_run = dry_run
        
        # State tracking for Git activity
        self.state_file = "git_sync_state.json"
        self.state = self._load_state()
        
        # Backlog Status IDs for MD_SD Project (528169)
        self.STATUS_OPEN = 1
        self.STATUS_IN_PROGRESS = 2
        self.STATUS_RESOLVED = 3
        self.STATUS_PENDING_RELEASE = 307448 
        self.STATUS_PENDING_REPORT = 333305
        self.PROJECT_ID = 528169

    def _load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def scan_and_sync(self, repo_name):
        """
        Scans recent activity in a repository and updates Backlog.
        """
        print(f"GIT: Scanning repository {repo_name}...")
        try:
            repo = self.gh.get_repo(repo_name)
        except Exception as e:
            print(f"GIT ERROR: Could not access repo {repo_name}: {e}")
            return
        
        repo_state = self.state.get(repo_name, {"last_pr_id": 0, "processed_commits": []})
        last_pr_id = repo_state.get("last_pr_id", 0)
        
        # 1. Handle Open PRs -> Pending Release
        open_prs = repo.get_pulls(state='open', sort='created', direction='desc')
        for pr in open_prs:
            # Gather all searchable text from PR and its commits
            search_text = f"{pr.title} {pr.head.ref} {pr.body or ''}"
            
            # Scan commits for closing keywords or IDs
            try:
                for commit in pr.get_commits():
                    search_text += f" {commit.commit.message}"
            except:
                pass # Skip if commits aren't accessible
                
            issue_keys = self._extract_issue_keys(search_text)
            
            for key in issue_keys:
                self._update_backlog_status(key, self.STATUS_PENDING_RELEASE, f"PR Open: {pr.html_url}")
            
            if pr.number > last_pr_id:
                last_pr_id = pr.number

        # 2. Handle Merged PRs -> Pending Report
        closed_prs = repo.get_pulls(state='closed', sort='updated', direction='desc')[:15]
        for pr in closed_prs:
            if pr.merged:
                search_text = f"{pr.title} {pr.head.ref} {pr.body or ''}"
                
                # Scan commits for this PR too
                try:
                    for commit in pr.get_commits():
                        search_text += f" {commit.commit.message}"
                except:
                    pass
                    
                issue_keys = self._extract_issue_keys(search_text)
                
                for key in issue_keys:
                    self._update_backlog_status(key, self.STATUS_PENDING_REPORT, f"PR Merged: {pr.html_url}")
        
        # Update state
        self.state[repo_name] = {"last_pr_id": last_pr_id}
        self._save_state()

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
