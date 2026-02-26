import os
import json
from agents.cloud_ingestor import CloudIngestor
from dotenv import load_dotenv

load_dotenv()

json_str = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
sheet_id = os.getenv('GOOGLE_SHEET_ID')

ingestor = CloudIngestor(json_str, sheet_id)
tasks = ingestor.get_live_tasks()

print("--- Final Parsing Test (Positional Rule) ---")
for task in tasks:
    if task['id'] == '2':
        print(f"\n[TASK ID: {task['id']}]")
        print("--- Captured JAPANESE ---")
        print(task['content'])
        print("\n--- Captured ENGLISH FALLBACK (Row below JA) ---")
        print(task['english_translation_fallback'])
        print("-" * 40)
