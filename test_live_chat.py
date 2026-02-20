import os
import requests
from orchestrator import Orchestrator
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def run_live_chat_test():
    webhook_url = "https://chat.googleapis.com/v1/spaces/AAAAXcdPfl0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=KtPxcNd14wnTFjomO2kr1Z4oQbTEZ75t_4LYq6m5Q_w"
    
    print("--- Sending LIVE Test Report to Google Chat ---")
    
    # We'll use a unique test key so it doesn't interfere with real daily reports
    test_date_str = "20260221_TEST"
    thread_key = f"daily_report_{test_date_str}"
    
    # 1. Helper for posting (bypassing the Orchestrator instance for a quick test)
    def post_msg(text):
        url = f"{webhook_url}&threadKey={thread_key}"
        payload = {"text": text}
        r = requests.post(url, json=payload)
        r.raise_for_status()
        print(f"Sent: {text[:30]}...")

    try:
        # Message 1: The Thread Header
        post_msg(f"🧪 [System Test] Daily Report {test_date_str}")
        
        # Message 2: Mock developer update
        post_msg("@Saurabh here are your tasks for today:
- [MD_SD-1249] Update enrollment date for Riho Kano")
        
        # Message 3: Mock developer update
        post_msg("@Raman here are your tasks for today:
- [MD_SD-1250] LMS Exam Time Limit Discrepancy")
        
        print("
✅ LIVE TEST COMPLETE. Please check your Google Chat space.")
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")

if __name__ == "__main__":
    run_live_chat_test()
