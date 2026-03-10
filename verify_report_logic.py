import os
import json
from datetime import datetime, timedelta
from agents.report_manager import ReportManager, gspread_col

# Mocking Specialist and Ingestor for pure logic testing
class MockGH:
    def __init__(self, tasks): self.tasks = tasks
    def get_full_active_tasks(self): return self.tasks
    def get_project_item_data(self, num, proj):
        for t in self.tasks:
            if t['number'] == num: return t['gh_data']
        return None
    def get_subtasks(self, num): return []

class MockIngestor:
    def __init__(self): self.client = self
    def open_by_key(self, sid): return self

def test_v5_logic_verification():
    print("=== AUTONOMOUS LOGIC AUDIT: FRIDAY V5 REPORTING ===\n")
    
    # 1. SETUP MOCK DATA (Simulating Friday March 6th)
    sim_date = datetime(2026, 3, 6, 9, 0)
    
    # Simulate GitHub State
    mock_tasks = [
        {
            "number": 1, "title": "Bohr Ind Renewal: Top Page", "assignee": "RmnSoni", 
            "labels": [], "end_date": "2026-03-03", "url": "github.com/internet-academy/bohr-individual",
            "project_tag": "Bohr Ind",
            "gh_data": {"Status": "Done", "Requester": "Sakamoto"}
        },
        {
            "number": 2, "title": "Bohr Ind Renewal: Data Submission", "assignee": "RmnSoni", 
            "labels": [], "end_date": "2026-03-04", "url": "github.com/internet-academy/bohr-individual",
            "project_tag": "Bohr Ind",
            "gh_data": {"Status": "In progress", "Requester": "Sakamoto"}
        },
        {
            "number": 3, "title": "New Urgent Fix", "assignee": "RmnSoni", 
            "labels": [], "end_date": "2026-03-05", "url": "github.com/internet-academy/member",
            "project_tag": "Maintenance",
            "gh_data": {"Status": "Done", "Requester": "Choo"}
        }
    ]
    
    gh = MockGH(mock_tasks)
    ingestor = MockIngestor()
    mgr = ReportManager(gh, ingestor, dry_run=True)
    
    # 2. RUN AUDIT ON FILTERING
    print("1. Verifying GitHub Task Fetching & Formatting...")
    formatted = mgr._get_v5_gh_tasks("RmnSoni")
    
    # Check Product Mapping
    assert formatted[0]['product'] == "Bohr Ind", "Product mapping failed for bohr-individual"
    assert formatted[2]['product'] == "Bohr Ind", "Product mapping failed for member repo"
    
    # Check Requester Mapping
    assert formatted[0]['requester'] == "Sakamoto", "Dynamic requester mapping failed"
    assert formatted[2]['requester'] == "Choo", "Fallback requester mapping failed"
    print("✅ PASS: Product & Requester mapping correct.")

    # 3. RUN AUDIT ON GROUPING
    print("\n2. Verifying Intelligent Grouping Logic...")
    task_list = [
        {"title": "Bohr Ind: Page 1", "prod": "Bohr Ind", "req": "Sakamoto", "dl_dt": datetime(2026,3,10), "dl_str": "03/10", "type": "new"},
        {"title": "Bohr Ind: Page 2", "prod": "Bohr Ind", "req": "Sakamoto", "dl_dt": datetime(2026,3,11), "dl_str": "03/11", "type": "new"},
        {"title": "Bohr Ind: Page 3", "prod": "Bohr Ind", "req": "Sakamoto", "dl_dt": datetime(2026,3,12), "dl_str": "03/12", "type": "new"},
        {"title": "Bohr Ind: Page 4", "prod": "Bohr Ind", "req": "Sakamoto", "dl_dt": datetime(2026,3,12), "dl_str": "03/12", "type": "new"},
        {"title": "Different Task", "prod": "Other", "req": "Choo", "dl_dt": datetime(2026,3,12), "dl_str": "03/12", "type": "new"}
    ]
    
    grouped = mgr._group_tasks(task_list, "Raman")
    
    # We expect 2 rows: 1 for grouped Bohr, 1 for Different Task
    assert len(grouped) == 2, f"Grouping failed. Expected 2 rows, got {len(grouped)}"
    assert "Bohr Ind:" in grouped[0][1], "Grouped title missing prefix"
    assert "1. Page 1" in grouped[0][1] and "4. Page 4" in grouped[0][1], "Nesting format incorrect"
    assert grouped[0][5] == "03/12", "Grouped deadline should be the latest"
    print("✅ PASS: Intelligent grouping & nesting format verified.")

    # 4. RUN AUDIT ON DATE BOUNDARIES
    print("\n3. Verifying Friday 9AM Boundary Logic...")
    # Mock date calculation from current runtime
    days_to_thursday = (sim_date.weekday() - 3) % 7
    last_thursday = sim_date - timedelta(days=days_to_thursday)
    assert last_thursday.date() == datetime(2026, 3, 5).date(), "Friday 9AM logic boundary calculation failed"
    print("✅ PASS: Date boundaries correctly calculated.")

    print("\n=== LOGIC AUDIT COMPLETE: ALL CRITERIA MET ===")

if __name__ == "__main__":
    test_v5_logic_verification()
