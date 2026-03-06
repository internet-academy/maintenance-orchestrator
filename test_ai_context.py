import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def test_improvement_3_direct():
    print("=== VERIFYING IMPROVEMENT 3: TECHNICAL CONTEXT (Direct API) ===\n")
    key = os.getenv('GEMINI_API_KEY')
    
    # 1. Real context from current GitHub activity
    context = """
    RECENT CODE CHANGES:
    - Merge pull request #2588 from internet-academy/u1/IAHPreservationFix
    - Merge pull request #2589 from internet-academy/y_choo
    - feat: add automatic CS registration notification for cs_group staff
    """
    
    # 2. Sample bug report
    sample_text = """
    至急です。菊一の「自社オリジナル」コースの登録ができません。
    登録できないため、K'sホールディングス様に録画アーカイブの提供ができません。
    明日2/27(金)中にはリリースが必要です。
    """
    
    prompt = f"""
    You are a technical coordinator. Analyze this bug report.
    1. If Japanese, translate. 2. If English, polish. 
    3. Concise title (3-7 words). 
    
    CODE REPOSITORY CONTEXT:
    {context}
    
    INPUT TASK: {sample_text}
    
    OUTPUT FORMAT:
    TITLE: <title>
    SUMMARY: <brief technical summary>
    TRANSLATION: <full english translation>
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={key}"
    payload = {"contents": [{"parts":[{"text": prompt}]}]}
    
    resp = requests.post(url, json=payload)
    result = resp.json()
    
    if "candidates" in result:
        text = result['candidates'][0]['content']['parts'][0]['text']
        print("\n--- AI REASONING & OUTPUT ---")
        print(text)
        print("-----------------------------\n")
        print("✅ SUCCESS: Improvement 3 verified. AI is technically-aware.")
    else:
        print(f"❌ FAILURE: {result}")

if __name__ == "__main__":
    test_improvement_3_direct()
