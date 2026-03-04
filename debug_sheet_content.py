import os
import json
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def debug_sheet():
    service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    
    with open(service_account_json, 'r') as f:
        creds_dict = json.load(f)
    
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    
    workbook = client.open_by_key(sheet_id)
    target_pattern = datetime.now().strftime("%y%m")
    print(f"Searching for tab with: {target_pattern}")
    
    target_sheet = None
    for sheet in workbook.worksheets():
        print(f"- Found tab: {sheet.title}")
        if target_pattern in sheet.title:
            target_sheet = sheet
            break
            
    if not target_sheet:
        target_sheet = workbook.get_worksheet(0)
        print(f"Fallback to first tab: {target_sheet.title}")
    else:
        print(f"Selected tab: {target_sheet.title}")
        
    data = target_sheet.get_all_values()
    print(f"Total rows found: {len(data)}")
    
    # Print rows 15-30 (where data usually starts)
    for i in range(min(15, len(data)), min(40, len(data))):
        print(f"Row {i+1}: {data[i]}")

if __name__ == "__main__":
    debug_sheet()
