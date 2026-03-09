import os
import json
from datetime import datetime
from dotenv import load_dotenv
from orchestrator import Orchestrator
from agents.report_manager import ReportManager

load_dotenv()

def test_next_week_grouping():
    print("=== TESTING NEXT WEEK ASSIGNMENTS & GROUPING ===\n")
    orc = Orchestrator(dry_run=True)
    report_mgr = ReportManager(orc.gh_specialist, orc.ingestor, dry_run=True)
    
    # Range for simulation:
    sim_last_thursday = datetime(2026, 3, 5)
    sim_next_thursday = datetime(2026, 3, 12)
    
    print(f"Target Window: Due after {sim_last_thursday.date()} up to {sim_next_thursday.date()}\n")

    for name, config in report_mgr.pic_map.items():
        print(f"[{name}]:")
        gh_tasks = report_mgr._get_v5_gh_tasks(config['gh'])
        
        # Filter for the window
        qualifying_raw = []
        for t in gh_tasks:
            deadline_dt = datetime.strptime(t['raw_deadline'], "%Y-%m-%d")
            gh_item_data = orc.gh_specialist.get_project_item_data(t['number'], 4)
            gh_status = gh_item_data.get('Status') if gh_item_data else "Open"
            
            if gh_status != "Done" and sim_last_thursday < deadline_dt <= sim_next_thursday:
                qualifying_raw.append({
                    "title": t['full_formatted_title'],
                    "req": t['requester'],
                    "prod": t['product'],
                    "dl_dt": deadline_dt,
                    "dl_str": t['formatted_deadline']
                })
        
        if not qualifying_raw:
            print("  (No qualifying tasks found)")
            continue
            
        # Apply Grouping
        grouped_rows = report_mgr._group_tasks(qualifying_raw, name)
        
        for i, row in enumerate(grouped_rows):
            # row format: ["", title, req, prod, pic, deadline, result, remarks]
            print(f"  Row {i+1}:")
            print(f"    Product:  {row[3]}")
            print(f"    Deadline: {row[5]}")
            print(f"    Title Content:\n{row[1]}")
            print("-" * 30)

if __name__ == "__main__":
    test_next_week_grouping()
