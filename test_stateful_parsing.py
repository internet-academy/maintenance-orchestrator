import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.cloud_ingestor import CloudIngestor
import re

def test_parsing_logic():
    print("--- Testing Stateful Parsing Logic (Mock Data) ---")
    
    # Mock data representing a typical form-block sheet layout
    mock_data = [
        ["ID", "", "", "Requester", "Date", "", "", "", "", "Backlog ID", "Status"], # Header (Row 17)
        ["1", "", "", "Suzuki", "2026-02-24", "", "", "", "", "PROJ-123", "Open"], # Task Start (Row 18)
        ["", "", "", "Details", "", "", "", "", "", "PIC", "Ewan"],
        ["", "", "", "Actual Content", "", "", "", "", "", "Status", "In Progress"],
        ["", "", "", "Translation Fallback", "", "", "", "", "", "Estimated Hours", "4.0"],
        ["2", "", "", "Inaba", "2026-02-24", "", "", "", "", "", ""], # Next Task
        ["", "", "", "More Content", "", "", "", "", "", "PIC", "Choo"],
    ]

    # We need to bypass __init__'s gspread auth for a unit test of the parser
    # Using a dummy ingestor
    class DummyIngestor(CloudIngestor):
        def __init__(self):
            pass

    ingestor = DummyIngestor()
    
    # Test Task 1
    task1 = ingestor._parse_block_from_list(mock_data, 1)
    
    print(f"Task 1 ID: {task1['id']}")
    print(f"Task 1 PIC: {task1['pic']} (Anchor: {task1['anchors'].get('pic')})")
    print(f"Task 1 Status: {task1['current_sheet_status']} (Anchor: {task1['anchors'].get('status')})")
    print(f"Task 1 Hours: {task1['estimated_hours']} (Anchor: {task1['anchors'].get('est_hours')})")
    
    assert task1['id'] == "1"
    assert task1['pic'] == "Ewan"
    assert task1['current_sheet_status'] == "In Progress"
    assert task1['estimated_hours'] == 4.0
    assert task1['anchors']['pic'] == (2, 9)
    assert task1['anchors']['status'] == (3, 9)

    # Test Task 2
    task2 = ingestor._parse_block_from_list(mock_data, 5)
    print(f"\nTask 2 ID: {task2['id']}")
    print(f"Task 2 PIC: {task2['pic']} (Anchor: {task2['anchors'].get('pic')})")
    
    assert task2['id'] == "2"
    assert task2['pic'] == "Choo"
    assert task2['anchors']['pic'] == (6, 9)

    print("\n[SUCCESS] MOCK DATA PARSING TEST PASSED")
✅ MOCK DATA PARSING TEST PASSED")

if __name__ == "__main__":
    test_parsing_logic()
