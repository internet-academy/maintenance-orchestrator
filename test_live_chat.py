import requests
from datetime import datetime

def test_consolidated_report():
    webhook_url = "https://chat.googleapis.com/v1/spaces/AAAAXcdPfl0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=KtPxcNd14wnTFjomO2kr1Z4oQbTEZ75t_4LYq6m5Q_w"
    
    today_str = datetime.now().strftime("%Y%m%d")
    # Using a NEW test key so it appears as a fresh single message
    thread_key = f"consolidated_test_{today_str}"
    
    full_report = f"📅 *Daily Report {today_str} (Consolidated Test)*\n"
    full_report += "________________________________\n\n"
    
    # Mocking real mention format (if we had IDs) vs current bold names
    full_report += "*Saurabh*\n• [MD_SD-1249] Update enrollment date for Riho Kano\n\n"
    full_report += "*Raman*\n• [MD_SD-1250] LMS Exam Time Limit Discrepancy\n\n"
    
    print("--- Sending Consolidated Report to Google Chat ---")
    
    url = f"{webhook_url}&threadKey={thread_key}"
    payload = {"text": full_report}
    
    r = requests.post(url, json=payload)
    r.raise_for_status()
    print("✅ SUCCESS. Check the chat for a single unified bubble.")

if __name__ == "__main__":
    test_consolidated_report()
