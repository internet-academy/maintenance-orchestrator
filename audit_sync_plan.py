import os
import json
from dotenv import load_dotenv
from agents.github_specialist import GitHubSpecialist
from agents.cloud_ingestor import CloudIngestor
from agents.load_balancer import DeveloperTimeline
from orchestrator import Orchestrator

load_dotenv()

def audit():
    orc = Orchestrator(dry_run=True)
    gh = orc.gh_specialist
    
    print("=== CURRENT GITHUB WORKLOAD (Project 4: Maintenance) ===")
    for name, gh_user in orc.developer_map.items():
        load = gh.get_active_workload(gh_user)
        print(f"{name} (@{gh_user}): {load}h currently assigned.")
    
    print("\n=== PLANNED SHEET UPDATES (DRY RUN RESULTS) ===")
    tasks = orc.ingestor.get_live_tasks()
    print(f"Found {len(tasks)} tasks to process.\n")
    
    for task in tasks:
        best_dev = orc._find_best_dev(task['estimated_hours'])
        if best_dev:
            # We use peek_fill here to simulate without consuming the bucket for the next task in the loop
            # But for a true audit of a 'run', we use fill_hours_with_dates as the orchestrator does.
            start, end = orc.timelines[best_dev['id']].fill_hours_with_dates(task['estimated_hours'])
            
            print(f"TASK #{task['id']}: {task['content'][:40]}...")
            print(f"  -> PIC Update:        {best_dev['name']}")
            print(f"  -> Start Date:        {start}")
            print(f"  -> End Date:          {end}")
            print(f"  -> GitHub Issue:      (New Issue in internet-academy/member)")
            print(f"  -> Status:            In Progress")
            print("-" * 30)
        else:
            print(f"TASK #{task['id']}: [OVERLOAD] No capacity found.")

if __name__ == "__main__":
    audit()
