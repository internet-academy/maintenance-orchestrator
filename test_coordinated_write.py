import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.cloud_ingestor import CloudIngestor
from unittest.mock import MagicMock

def test_write_verification():
    print("--- Testing Coordinated Write Verification ---")
    
    # Mock worksheet
    mock_worksheet = MagicMock()
    
    # Setup for Success case
    # Cell check is for the Anchor (Label) cell
    # (row=2, col=9) in 0-based -> (row=3, col=10) in 1-based. NO. 
    # Row 2 -> index 2 -> 3rd row -> cell(3, ...)
    # Col 9 -> index 9 -> 10th col -> cell(..., 10)
    mock_worksheet.cell.side_effect = lambda r, c: MagicMock(value="Status" if r == 3 and c == 10 else "Wrong")

    class DummyIngestor(CloudIngestor):
        def __init__(self):
            pass
        def get_current_month_worksheet(self):
            return mock_worksheet

    ingestor = DummyIngestor()
    
    # 1. Test Successful Write
    anchor_map = {"status": (2, 9)} # 0-based index
    ingestor.write_status(anchor_map, "Resolved")
    
    # Check if update_cell was called on (3, 11) (1-based for col 9 + 2)
    mock_worksheet.update_cell.assert_called_with(3, 11, "Resolved")
    print("SUCCESS Case Verified.")

    # 2. Test Anchor Mismatch (Failure)
    # Move the anchor map to a row that doesn't have "Status"
    fail_anchor = {"status": (5, 9)}
    ingestor.write_status(fail_anchor, "Resolved")
    
    # update_cell should NOT have been called for this new attempt
    # assert_called_with would still be the old one, so we check call count
    assert mock_worksheet.update_cell.call_count == 1
    print("FAILURE (Mismatch) Case Verified.")

    print("\n[SUCCESS] COORDINATED WRITE TEST PASSED")

if __name__ == "__main__":
    test_write_verification()
