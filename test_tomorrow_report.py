import os
from dotenv import load_dotenv
from orchestrator import Orchestrator
from agents.report_manager import ReportManager

load_dotenv()

def test_report_logic():
    print("=== TESTING REPORT MANAGER: THURSDAY SHIFT & SYNC (DRY RUN) ===\n")
    orc = Orchestrator(dry_run=True)
    report_mgr = ReportManager(orc.gh_specialist, orc.ingestor, dry_run=True)
    
    # Run the report logic
    report_mgr.generate_thursday_report()
    
    print("\nDRY RUN VERIFICATION COMPLETE.")

if __name__ == "__main__":
    test_report_logic()
