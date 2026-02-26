import os
import json
from agents.cloud_ingestor import CloudIngestor
from dotenv import load_dotenv

load_dotenv()

json_str = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
sheet_id = os.getenv('GOOGLE_SHEET_ID')

ingestor = CloudIngestor(json_str, sheet_id)
worksheet = ingestor.get_current_month_worksheet()
data = worksheet.get_all_values()

print(f"--- Layout Inspection (Sheet: {worksheet.title}) ---")
for i in range(17, 35): # Rows 18 to 35
    row = data[i]
    print(f"Row {i+1}: {row}")
