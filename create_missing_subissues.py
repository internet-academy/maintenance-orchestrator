import requests
import os
import re
import time
from dotenv import load_dotenv
from orchestrator import Orchestrator

load_dotenv()

def create_subissues():
    print("--- CREATING MISSING SUB-ISSUES FOR EXISTING TASKS ---")
    orc = Orchestrator(dry_run=False)
    gh = orc.gh_specialist
    org = "internet-academy"

    # 1. Ingest tasks from sheet to get parent issue info
    tasks = orc.ingestor.get_live_tasks()
    
    for task in tasks:
        issue_url = task.get('backlog_id')
        if not issue_url or "github.com" not in issue_url: continue
        
        match = re.search(r'/issues/(\d+)', issue_url)
        if not match: continue
        parent_number = int(match.group(1))
        
        # Get parent details to construct sub-issue title
        parent_resp = requests.get(f"https://api.github.com/repos/{org}/member/issues/{parent_number}", headers=gh.headers)
        if parent_resp.status_code != 200: continue
        parent_data = parent_resp.json()
        parent_title = parent_data['title']
        parent_assignee = parent_data['assignees'][0]['login'] if parent_data['assignees'] else None
        
        # Strip [MAINTENANCE] prefix for the sub-issue title consistency
        clean_title = parent_title.replace("[MAINTENANCE] ", "").split(" (")[0]
        
        sub_title = f"Understand the request: {clean_title} (Sub-issue for #{parent_number})"
        sub_body = f"Mandatory 20-minute task to review and clarify requirements for #{parent_number}."
        
        print(f"Creating sub-issue for Parent #{parent_number}...")
        
        try:
            # Create Sub-issue
            sub_issue = gh.create_issue(
                repo="member",
                title=sub_title,
                body=sub_body,
                assignee=parent_assignee,
                labels=["staff-report"]
            )
            sub_node_id = sub_issue['node_id']
            
            # Add to Project 4
            sub_item_id = gh.add_to_project(sub_node_id, 4)
            
            # Set Sub-issue Fields
            gh.update_field(4, sub_item_id, 'status', gh.projects[4]['options']['status_to_triage'], is_option=True)
            gh.update_field(4, sub_item_id, 'level', gh.projects[4]['options']['level_child'], is_option=True)
            gh.update_field(4, sub_item_id, 'hours', 0.33)
            # Link to Parent by title (GitHub Project Parent issue field matches on title)
            gh.update_field(4, sub_item_id, 'parent_issue', parent_title)
            
            print(f"  - SUCCESS: Created Sub-issue #{sub_issue['number']} linked to #{parent_number}\n")
            time.sleep(1)
            
        except Exception as e:
            print(f"  - ERROR: Failed for Parent #{parent_number}: {e}")

if __name__ == "__main__":
    create_subissues()
