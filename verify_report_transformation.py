import os
import json
from dotenv import load_dotenv
from orchestrator import Orchestrator
from agents.report_manager import ReportManager, gspread_col

load_dotenv()

def verify_transformation():
    print("=== EMPIRICAL VERIFICATION: THURSDAY REPORT TRANSFORMATION ===\n")
    orc = Orchestrator(dry_run=True)
    report_mgr = ReportManager(orc.gh_specialist, orc.ingestor, dry_run=True)
    
    workbook = orc.ingestor.client.open_by_key(report_mgr.sheet_id)
    wr_tab = workbook.worksheet('Weekly Report')
    
    # Let's use CHOO as the primary example for clarity
    name = "Choo"
    config = report_mgr.pic_map[name]
    
    # 1. FETCH 'BEFORE' STATE
    last_row, last_col = config['last']
    next_row, next_col = config['next']
    
    before_last = wr_tab.get_values(f"{gspread_col(last_col)}{last_row}:{gspread_col(last_col+5)}{last_row+3}")
    before_next = wr_tab.get_values(f"{gspread_col(next_col)}{next_row}:{gspread_col(next_col+5)}{next_row+3}")
    
    print(f"--- [BEFORE] {name}'s Blocks in 'Weekly Report' ---")
    print(f"LAST WEEK (Rows {last_row}-{last_row+3}):")
    for r in before_last: print(f"  {r}")
    print(f"\nTHIS WEEK (Rows {next_row}-{next_row+3}):")
    for r in before_next: print(f"  {r}")
    
    # 2. SIMULATE 'AFTER' STATE
    print(f"\n--- [AFTER SIMULATION] {name}'s Blocks ---")
    
    # Logic: This Week's data becomes Last Week's data
    after_last = [row for row in before_next if any(row)]
    
    # Logic: Pull fresh tasks from GitHub for 'Next Week'
    gh_tasks = report_mgr._get_filtered_gh_tasks(config['gh'])
    after_next = []
    for i, t in enumerate(gh_tasks[:4]):
        deadline = t.get('end_date', 'TBD')
        after_next.append([str(i+1), t['title'], "Choo", t['project_tag'], name, deadline])
        
    print(f"LAST WEEK (Shifted from above):")
    for r in after_last: print(f"  {r}")
    print(f"\nTHIS WEEK (Pulled from GitHub):")
    for r in after_next: print(f"  {r}")

    # 3. TABLES FOR WEEKLY REPORT PREVIEW
    print("\n--- [FINAL TABLES PREVIEW] (Tables for Weekly Report Tab) ---")
    print("Range L18:S31 (Completed) will contain all 'Shifted' tasks from all 4 PICs.")
    print("Range L36:S46 (Planned) will contain all 'Pulled' tasks from all 4 PICs.")
    
if __name__ == "__main__":
    verify_transformation()
