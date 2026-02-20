
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv('/home/min/projects/personal-agents/.env')

def inspect_sheet():
    json_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    with open(json_path, 'r') as f:
        creds_dict = json.load(f)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    workbook = client.open_by_key(sheet_id)
    target_pattern = "2602" # Current month
    target_sheet = None
    for ws in workbook.worksheets():
        if target_pattern in ws.title:
            target_sheet = ws
            break
    
    if not target_sheet:
        print(f"Tab with {target_pattern} not found. Tabs available: {[s.title for s in workbook.worksheets()]}")
        target_sheet = workbook.get_worksheet(0)

    print(f"--- Inspecting Tab: {target_sheet.title} ---")
    data = target_sheet.get_all_values()
    
    print("--- Sheet Row Inspection (First 50 rows) ---")
    for i, row in enumerate(data[:50]):
        # Print only rows that have content
        if any(row):
            print(f"Row {i}: {row}")

if __name__ == "__main__":
    inspect_sheet()
