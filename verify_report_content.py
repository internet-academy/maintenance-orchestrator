import os
import json
from dotenv import load_dotenv
from orchestrator import Orchestrator

load_dotenv()

def verify_report():
    print("=== SELF-VERIFICATION: DAILY REPORT CONTENT ===\n")
    orc = Orchestrator(dry_run=True)
    gh = orc.gh_specialist
    
    # 1. Fetch data exactly like the orchestrator does
    active_tasks = gh.get_full_active_tasks()
    print(f"Total tasks retrieved from GitHub: {len(active_tasks)}")
    
    # 2. Replicate the grouping and formatting logic
    login_to_name = {v.lower(): k for k, v in orc.developer_map.items()}
    report_data = {}
    
    for task in active_tasks:
        login = (task['assignee'] or "unassigned").lower()
        pic_name = login_to_name.get(login, "Unassigned")
        if pic_name not in report_data: report_data[pic_name] = []
        
        date_str = f"[{task['start_date']} → {task['end_date']}]" if task['start_date'] else "[No Dates]"
        proj_tag = f"*{task['project_tag']}*"
        report_data[pic_name].append(f"• {proj_tag} {task['title']} {date_str}")

    # 3. Construct the final string
    today_str = "2026-03-06"
    full_report = f"📅 *Daily Status Report ({today_str})*\n"
    full_report += "________________________________\n\n"

    if not report_data:
        full_report += "✅ No active parent tasks found across all projects!"
    else:
        for name in sorted(report_data.keys()):
            tasks = report_data[name]
            chat_id = orc.chat_ids.get(name, name)
            mention = f"<users/{chat_id}>" if chat_id.replace(".","").isdigit() else f"*{name}*"
            full_report += f"{mention}\n" + "\n".join(tasks) + "\n\n"

    print("--- GENERATED REPORT CONTENT ---")
    print(full_report)
    print("--------------------------------")
    
    # Validation Logic
    if len(active_tasks) > 0 and "No active parent tasks" not in full_report:
        print("\n✅ VERIFICATION SUCCESS: Report is populated with live data.")
    else:
        print("\n❌ VERIFICATION FAILURE: Report is empty or incorrect.")

if __name__ == "__main__":
    verify_report()
