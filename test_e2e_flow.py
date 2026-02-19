
import os
from orchestrator import Orchestrator
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

def run_e2e_dry_test():
    print("--- Starting E2E Dry Run Test ---")
    
    # 1. Verify Environment
    required = ['GOOGLE_SERVICE_ACCOUNT_JSON', 'GOOGLE_SHEET_ID', 'BACKLOG_API_KEY', 'BACKLOG_SPACE_ID']
    missing = [var for var in required if not os.getenv(var)]
    
    if missing:
        print(f"ERROR: Missing environment variables: {', '.join(missing)}")
        return

    # 2. Initialize Orchestrator in Dry Run mode
    orchestrator = Orchestrator(dry_run=True)
    
    # 3. Execute
    orchestrator.run()
    
    print("
--- E2E Dry Run Test Complete ---")

if __name__ == "__main__":
    run_e2e_dry_test()
