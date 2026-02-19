import os
import re
import time
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load configuration
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

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
    content = workspace_path.read_text()
    target_match = re.search(r"TO: @(\w+)", content)
    status_match = re.search(r"STATUS: \[(\w+)\]", content)
    message_match = re.search(r"### 📝 MESSAGE / INSTRUCTION\n> (.*)", content, re.DOTALL)
    
    if target_match and status_match:
        return {
            "target": target_match.group(1).lower(),
            "status": status_match.group(1),
            "instruction": message_match.group(1).strip() if message_match else ""
        }
    return None

def update_workspace(workspace_path, source, target, status, message):
    content = workspace_path.read_text()
    # Update Active Handoff (Simple string replacement for prototype)
    content = re.sub(r"FROM: @\w+", f"FROM: @{source}", content)
    content = re.sub(r"TO: @\w+", f"TO: @{target}", content)
    content = re.sub(r"STATUS: \[\w+\]", f"STATUS: [{status}]", content)
    
    # Update Message (Rudimentary replacement)
    content += f"\n\n### 📝 LATEST UPDATE FROM @{source}\n> {message}\n"
    
    workspace_path.write_text(content)

def collaborate(project_path):
    workspace_path = Path(project_path) / "WORKSPACE.md"
    handoff = get_active_handoff(workspace_path)
    
    if not handoff or handoff["status"] == "COMPLETED":
        print("No active handoff found.")
        return

    print(f"--- Collaboration active for {project_path.name} ---")
    # This script is a template for the external logic to drive.
    # The actual LLM calls happen via the Gemini CLI Orchestrator.

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        collaborate(Path(sys.argv[1]).absolute())
    else:
        print("Usage: python collaborator.py /path/to/project")
