import os
import json
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

def get_full_dropdown():
    service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    
    with open(service_account_json, 'r') as f:
        creds_dict = json.load(f)
        
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    
    # We use the discovery API or a specific gspread method if available to see validation
    # Actually, gspread doesn't easily expose 'Data Validation' list values.
    # I will try to find a cell that ALREADY has a 'Resolved' style status in it by scanning more rows.
    
    workbook = client.open_by_key(sheet_id)
    sheet = workbook.worksheet('エラー報告_2602')
    
    print("Scanning first 200 rows of Column K for status variants...")
    col_k = sheet.col_values(11)
    
    standard_statuses = ['Resolved', 'Complete!', 'Verified', 'Pending', 'Testing']
    found = []
    for val in col_k:
        if any(s.lower() in val.lower() for s in standard_statuses):
            found.append(val)
            
    print(f"Potential status matches found: {list(set(found))}")

if __name__ == '__main__':
    get_full_dropdown()
