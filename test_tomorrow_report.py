import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from orchestrator import Orchestrator

load_dotenv()

def test_reports():
    orc = Orchestrator(dry_run=True)
    gh = orc.gh_specialist
    
    print("Fetching live data from GitHub...")
    active_tasks = gh.get_full_active_tasks()
    login_to_name = {v.lower(): k for k, v in orc.developer_map.items()}

    def generate_preview(target_date):
        target_str = target_date.strftime("%Y-%m-%d")
        print(f"\n--- PREVIEW FOR DATE: {target_str} ---")
        
        in_progress = {}
        delayed = {}
        unscheduled = []

        for task in active_tasks:
            login = (task['assignee'] or "unassigned").lower()
            name = login_to_name.get(login, "Unassigned")
            start = task.get('start_date')
            end = task.get('end_date')
            
            task_entry = f"• *{task['project_tag']}* {task['title']}"
            if start: task_entry += f" [{start} → {end}]"

            if not start or not end:
                unscheduled.append(f"• *{task['project_tag']}* {task['title']} (@{name})")
            else:
                start_dt = datetime.strptime(start, "%Y-%m-%d")
                end_dt = datetime.strptime(end, "%Y-%m-%d")
                
                # We use the same comparison logic as the orchestrator
                if end_dt < target_date.replace(hour=0, minute=0, second=0, microsecond=0):
                    if name not in delayed: delayed[name] = []
                    delayed[name].append(task_entry)
                elif start_dt <= target_date <= (end_dt + timedelta(days=1)):
                    if name not in in_progress: in_progress[name] = []
                    in_progress[name].append(task_entry)

        # Print simple console version
        if in_progress:
            print("🚀 IN PROGRESS:")
            for n, t in in_progress.items(): print(f"  {n}: {len(t)} tasks")
        if delayed:
            print("⚠️ DELAYED:")
            for n, t in delayed.items(): print(f"  {n}: {len(t)} tasks")
        print(f"🔍 UNSCHEDULED: {len(unscheduled)} tasks")

    # Run for Today and Tomorrow
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    
    generate_preview(today)
    generate_preview(tomorrow)

if __name__ == "__main__":
    test_reports()
