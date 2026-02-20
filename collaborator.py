import os
import re
import time
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load configuration
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Paths to memory files
USER_PROFILE = BASE_DIR / "user_profile.md"
ACTIVE_LOGS = BASE_DIR / "active_logs.md"
PROJECT_STATES = BASE_DIR / "project_states.json"
PERSONA_DIR = BASE_DIR / "gemini-active"

def run_shell(command):
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return {"stdout": result.stdout, "stderr": result.stderr, "exit_code": result.returncode}

def get_active_handoff(workspace_path):
    if not workspace_path.exists():
        return None
    content = workspace_path.read_text().replace("**", "")
    target_match = re.search(r\"TO: @(\w+)\", content)
    status_match = re.searchr\"STATUS: \\[   WO◊ã€€ù[ù
BàY\‹ÿYŸ