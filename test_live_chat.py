import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def test_real_mention():
    webhook_url = os.getenv('GOOGLE_CHAT_REPORT_WEBHOOK')
    if not webhook_url:
        print("Error: GOOGLE_CHAT_REPORT_WEBHOOK not set.")
        return
    
    today_str = datetime.now().strftime("%Y%m%d")
    thread_key = f"mention_test_{today_str}"
    
    saurabh_id = "102690792983273136159"
    
    full_report = f"📅 *Daily Report {today_str} (Real Mention Test)*\n"
    full_report += "________________________________\n\n"
    
    # Testing the REAL Google Chat mention syntax
    full_report += f"<users/{saurabh_id}>\n"
    full_report += "• [MD_SD-1249] Real mention test successful!\n\n"
    
    print(f"--- Sending REAL Mention Report for Saurabh ({saurabh_id}) ---")
    
    url = f"{webhook_url}&threadKey={thread_key}"
    payload = {"text": full_report}
    
    r = requests.post(url, json=payload)
    r.raise_for_status()
    print("✅ SUCCESS. Saurabh should have received a notification.")

if __name__ == "__main__":
    test_real_mention()
