import os
from orchestrator import Orchestrator
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def run_tomorrow_report_test():
    print("--- Testing 'Daily Report' for Tomorrow (2026-02-21) ---")
    
    # 1. Initialize Orchestrator in Dry Run mode
    orchestrator = Orchestrator(dry_run=True)
    
    # 2. Mock some tasks
    mock_tasks = [
        {
            "id": "1",
            "backlog_id": "MD_SD-1249",
            "requester": "Suzuki",
            "pic": "Saurabh",
            "content": "Request to change the first session date for student",
            "title_summary": "Update enrollment date for Riho Kano",
            "current_sheet_status": "In Progress" # Forcing this to show in report
        },
        {
            "id": "2",
            "backlog_id": "MD_SD-1250",
            "requester": "Inaba",
            "pic": "Raman",
            "content": "Possible issue with exam time limits",
            "title_summary": "LMS Exam Time Limit Discrepancy",
            "current_sheet_status": "" # Empty status should also show
        }
    ]

    # 3. Temporarily override the date generation in the instance
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%Y%m%d")
    
    print(f"DEBUG: Simulating Date: {tomorrow_str}")
    
    # Manually trigger the internal report method with our mock data
    # We use a wrapper to use our simulated date
    def mocked_send_report(all_tasks):
        thread_key = f"daily_report_{tomorrow_str}"
        header = f"Daily Report {tomorrow_str}"
        
        print(f"
[REPORT PREVIEW]")
        print(f"Target Thread Key: {thread_key}")
        print(f"Message 1 (Header): {header}")
        
        report_data = {}
        for task in all_tasks:
            pic_name = task.get('pic')
            if not pic_name: continue
            if pic_name not in report_data:
                report_data[pic_name] = []
            
            title = task.get('title_summary', task['content'][:50])
            report_data[pic_name].append(f"- [{task.get('backlog_id', 'NEW')}] {title}")

        for name, tasks in report_data.items():
            chat_id = orchestrator.chat_ids.get(name, name)
            mention = f"<users/{chat_id}>" if chat_id.isdigit() else f"@{name}"
            msg = f"{mention} here are your tasks for today:
" + "
".join(tasks)
            print(f"Message (PIC: {name}): {msg}")

    mocked_send_report(mock_tasks)
    print("
--- Test Complete ---")

if __name__ == "__main__":
    run_tomorrow_report_test()
