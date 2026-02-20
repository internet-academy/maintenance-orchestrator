
import os
from orchestrator import Orchestrator
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

def run_live_sync():
    print("🚀 INITIALIZING LIVE SYNC 🚀")
    print("Target: Backlog Project MD_SD")
    print("Start Date: 2026-03-02")
    print("--------------------------------------------")
    
    # 1. Initialize Orchestrator in LIVE mode
    orchestrator = Orchestrator(dry_run=False)
    
    # 2. Execute
    orchestrator.run()
    
    print("\n✅ LIVE SYNC COMPLETE ✅")

if __name__ == "__main__":
    run_live_sync()
