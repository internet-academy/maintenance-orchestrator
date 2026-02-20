
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv('/home/min/projects/personal-agents/.env')

def diagnose_permissions():
    json_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    try:
        with open(json_path, 'r') as f:
            creds_dict = json.load(f)
        
        email = creds_dict.get('client_email')
        print(f"DIAGNOSIS: Operating as {email}")
        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        print("
--- 1. Testing Drive visibility ---")
        # List all spreadsheets visible to this service account
        files = client.list_spreadsheet_files()
        if not files:
            print("RESULT: Service account sees ZERO files. This confirms a permission issue.")
        else:
            print(f"RESULT: Service account can see {len(files)} files:")
            for f in files:
                print(f"- {f['name']} (ID: {f['id']})")
                if f['id'] == sheet_id:
                    print("  >> FOUND MATCH! The ID in .env is correct.")

        print("
--- 2. Direct Access Test ---")
        try:
            client.open_by_key(sheet_id)
            print("SUCCESS: Direct access to sheet is working now.")
        except Exception as e:
            print(f"FAILURE: Direct access still blocked. Error: {e}")

    except Exception as e:
        print(f"CRITICAL DIAGNOSTIC ERROR: {e}")

if __name__ == "__main__":
    diagnose_permissions()
