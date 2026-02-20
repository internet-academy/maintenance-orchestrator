
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv('/home/min/projects/personal-agents/.env')

def inspect_more_rows():
    json_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json.load(open(json_path)), scope)
    client = gspread.authorize(creds)
    
    workbook = client.open_by_key(sheet_id)
    target_sheet = workbook.worksheet("エラー報告_2602")
    data = target_sheet.get_all_values()
    
    print("--- Inspecting Rows 60 - 100 ---")
    for i, row in enumerate(data[60:100], start=60):
        if row and row[0].strip():
            print(f"Row {i}: {row[:10]}") # Only first 10 cols for brevity

if __name__ == "__main__":
    inspect_more_rows()
