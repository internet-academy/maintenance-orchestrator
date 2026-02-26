import os
import json
from agents.cloud_ingestor import CloudIngestor
from dotenv import load_dotenv

load_dotenv()

json_str = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
sheet_id = os.getenv('GOOGLE_SHEET_ID')

ingestor = CloudIngestor(json_str, sheet_id)
tasks = ingestor.get_live_tasks()

print(f"--- Parsing Results Verification ---")
for task in tasks[:3]:
    print(f"
[TASK ID: {task['id']}]")
    print(f"--- JAPANESE CONTENT ---")
    print(task['content'])
    print(f"--- ENGLISH FALLBACK ---")
    print(task['english_translation_fallback'])
    print("-" * 30)
