import os
import json
from dotenv import load_dotenv
from orchestrator import Orchestrator

load_dotenv()

def debug_report():
    print("--- Debugging Daily Report Generation ---")
    orc = Orchestrator(dry_run=True)
    gh = orc.gh_specialist
    
    print("\n1. Fetching all active tasks from GitHub...")
    active_tasks = gh.get_full_active_tasks()
    print(f"Total active tasks found (excluding children): {len(active_tasks)}")
    
    if len(active_tasks) > 0:
        print("\nSample Task Data:")
        print(json.dumps(active_tasks[0], indent=2))
    
    print("\n2. Simulating report grouping...")
    login_to_name = {v.lower(): k for k, v in orc.developer_map.items()}
    report_data = {}
    for task in active_tasks:
        login = (task['assignee'] or "unassigned").lower()
        pic_name = login_to_name.get(login, "Unassigned")
        if pic_name not in report_data: report_data[pic_name] = []
        date_str = f"[{task['start_date']} -> {task['end_date']}]" if task['start_date'] else "[No Dates]"
        report_data[pic_name].append(f"• *{task['project_tag']}* {task['title']} {date_str}")

    print(f"Groups found: {list(report_data.keys())}")
    
    print("\n3. Final Message Preview:")
    today_str = "2026-03-06"
    full_report = f"📅 *Daily Status Report ({today_str})*\n________________________________\n\n"
    if not report_data:
        full_report += "✅ No active parent tasks found across all projects!"
    else:
        for name in sorted(report_data.keys()):
            tasks = report_data[name]
            chat_id = orc.chat_ids.get(name, name)
            mention = f"<users/{chat_id}>" if chat_id.replace(".","").isdigit() else f"*{name}*"
            full_report += f"{mention}\n" + "\n".join(tasks) + "\n\n"
    
    print(full_report)

if __name__ == "__main__":
    debug_report()
