import os
import json
from dotenv import load_dotenv
from orchestrator import Orchestrator

load_dotenv()

def test_improvement_3():
    print("=== VERIFYING IMPROVEMENT 3: TECHNICAL CONTEXT ===\n")
    orc = Orchestrator(dry_run=True)
    gh = orc.gh_specialist
    
    # 1. Fetch real context from the repo
    print("1. Fetching recent repo context (Last 3 days)...")
    context = gh.get_recent_repo_context("member")
    print(f"--- Context Found ---\n{context}\n---------------------\n")
    
    # 2. Pick a sample task (Task #10 - Urgent Kikuichi issue)
    sample_text = """
    至急です。菊一の「自社オリジナル」コースの登録ができません。
    登録できないため、K'sホールディングス様に録画アーカイブの提供ができません。
    明日2/27(金)中にはリリースが必要です。
    """
    
    print("2. Asking Gemini to summarize WITH this context...")
    title, translation = orc._translate_and_summarize(sample_text, code_context=context)
    
    print("\n--- AI OUTPUT ---")
    print(f"TITLE: {title}")
    print(f"TRANSLATION: {translation}")
    print("-----------------\n")
    
    # Logic check
    if any(line.strip() in translation for line in context.split('\n') if line.strip().startswith('-')):
        print("✅ SUCCESS: Gemini integrated repo context into the summary.")
    else:
        print("ℹ️  INFO: Gemini provided a clean summary. (Integration depends on relevance of commits to the task)")

if __name__ == "__main__":
    test_improvement_3()
