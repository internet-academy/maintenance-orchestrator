import os
import json
import gspread
import re
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

def inspect_all_numeric_sheets():
    service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    
    if os.path.exists(service_account_json):
        with open(service_account_json, 'r') as f:
            creds_dict = json.load(f)
    else:
        creds_dict = json.loads(service_account_json)
        
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    workbook = client.open_by_key(sheet_id)
    
    numeric_pattern = re.compile(r'^\d{3}$')
    
    print("--- Scanning Numeric Sheets for '受ける' Decision ---")
    for ws in workbook.worksheets():
        if not numeric_pattern.match(ws.title):
            continue
            
        try:
            decision = ws.cell(51, 4).value
            title = ws.cell(4, 4).value
            ticket = ws.cell(83, 1).value or ws.cell(83, 4).value
            
            status_mark = "✅ APPROVED" if decision == "受ける" else "❌ SKIP"
            ticket_mark = " (Has Ticket)" if ticket and "github.com" in str(ticket) else " (No Ticket)"
            
            if decision == "受ける":
                print(f"{status_mark} Sheet {ws.title}: {title}{ticket_mark}")
        except Exception as e:
            print(f"Error reading {ws.title}: {e}")

if __name__ == '__main__':
    inspect_all_numeric_sheets()
