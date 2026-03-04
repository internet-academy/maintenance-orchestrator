import os
import json
from dotenv import load_dotenv
from orchestrator import Orchestrator

load_dotenv()

def final_audit():
    orc = Orchestrator(dry_run=True)
    tasks = orc.ingestor.get_live_tasks()
    
    print(f"=== FINAL AUDIT: {len(tasks)} TASKS READY FOR SYNC ===\n")
    
    for i, task in enumerate(tasks):
        best_dev = orc._find_best_dev(task['estimated_hours'])
        if not best_dev:
            print(f"TASK #{task['id']}: [OVERLOAD] No capacity found.")
            continue
            
        start, end = orc.timelines[best_dev['id']].fill_hours_with_dates(task['estimated_hours'])
        priority = orc._detect_priority(task['content'])
        desc, title, _ = orc._generate_bilingual_description(task)
        
        # Prepare Title with prefix
        full_title = f"[ERROR] {title} ({orc.name_mapping.get(task['requester'], task['requester'])} - #{task['id']})"
        
        print(f"--- TASK {i+1}/9: ID {task['id']} ---")
        print(f"PIC:         {best_dev['name']} (@{best_dev['id']})")
        print(f"TITLE:       {full_title}")
        print(f"PRIORITY:    {priority}")
        print(f"LEVEL:       Parent")
        print(f"DATES:       {start} to {end}")
        print(f"DESCRIPTION CONTENT:\n{desc}")
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    final_audit()
