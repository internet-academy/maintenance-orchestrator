import os
import json
from dotenv import load_dotenv
from orchestrator import Orchestrator

load_dotenv()

def inspect_github_tasks():
    print("=== EMPIRICAL GITHUB TASK SCAN: 03/06 to 03/12 ===\n")
    orc = Orchestrator(dry_run=True)
    gh = orc.gh_specialist
    
    # Range for simulation:
    # Start: 2026-03-06
    # End:   2026-03-12 (inclusive)
    
    all_tasks = gh.get_full_active_tasks()
    pic_results = {
        "Choo": [], "Saurabh": [], "Raman": [], "Ewan": []
    }
    
    login_to_name = {
        os.getenv('GH_USER_CHOO', 'young-min-choo').lower(): "Choo",
        os.getenv('GH_USER_SAURABH', 'Saurabh-IA').lower(): "Saurabh",
        os.getenv('GH_USER_RAMAN', 'RmnSoni').lower(): "Raman",
        os.getenv('GH_USER_EWAN', 'Froggyyyyyyy').lower(): "Ewan"
    }

    print(f"Total parent tasks found on Project 3/4: {len(all_tasks)}")
    
    for t in all_tasks:
        login = (t['assignee'] or "").lower()
        if login in login_to_name:
            name = login_to_name[login]
            deadline = t.get('end_date')
            
            if deadline:
                # Add to results if within the sim range
                if "2026-03-06" <= deadline <= "2026-03-12":
                    pic_results[name].append(f"  - #{t['number']} | {deadline} | {t['title']}")
                else:
                    # Log outliers for debugging
                    if "2026-03" in deadline:
                        print(f"DEBUG: Found task outside sim range: {name} | #{t['number']} | {deadline}")

    print("\n--- QUALIFYING TASKS FOR NEXT WEEK (SIM) ---")
    for name, tasks in pic_results.items():
        print(f"\n[{name}]:")
        if not tasks: print("  (No tasks found in range)")
        for task in tasks: print(task)

if __name__ == "__main__":
    inspect_github_tasks()
