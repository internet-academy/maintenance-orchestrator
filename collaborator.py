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
    target_match = re.search(r"TO: @(\w+)", content)
    status_match = re.search(r"STATUS: \[?(\w+)\]?", content)
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
    # Update Active Handoff
    content = re.sub(r"\*\*FROM:\*\* @\w+", f"**FROM:** @{source.capitalize()}", content)
    content = re.sub(r"\*\*TO:\*\* @\w+", f"**TO:** @{target.capitalize()}", content)
    content = re.sub(r"\*\*STATUS:\*\* \[?\w+\]?", f"**STATUS:** [{status}]", content)
    
    # Update Message
    instruction_pattern = r"(### 📝 MESSAGE / INSTRUCTION\n> ).*?(\n\n---)"
    new_instruction = f"\\1{message}\\2"
    content = re.sub(instruction_pattern, new_instruction, content, flags=re.DOTALL)
    
    # Add to log
    log_entry = f"| {time.strftime('%Y-%m-%d %H:%M:%S')} | @{source.capitalize()} | @{target.capitalize()} | {message[:50]}... |\n"
    content += log_entry
    
    workspace_path.write_text(content)

def collaborate(project_path):
    workspace_path = Path(project_path) / "WORKSPACE.md"
    handoff = get_active_handoff(workspace_path)
    
    if not handoff or handoff["status"] == "COMPLETED":
        print("No active handoff found.")
        return

    agent_name = handoff["target"]
    persona_path = PERSONA_DIR / f"{agent_name}.md"
    
    if not persona_path.exists():
        print(f"Error: Persona {agent_name} not found.")
        return

    print(f"🤖 Waking up @{agent_name} for project {project_path.name}...")
    
    # Assemble Context
    persona = persona_path.read_text()
    profile = USER_PROFILE.read_text()
    logs = ACTIVE_LOGS.read_text()
    states = PROJECT_STATES.read_text()

    prompt = f"""
{persona}

--- SYSTEM CONTEXT ---
USER PROFILE:
{profile}

ACTIVE LOGS:
{logs}

PROJECT STATES:
{states}

--- PROJECT WORKSPACE ---
Path: {project_path}
Instruction: {handoff['instruction']}

--- TASK ---
You are operating autonomously. You must fulfill the instruction above.
You can output SHELL commands to execute your work.
Format your response as:
THOUGHT: [Your reasoning]
COMMAND: [A single shell command to execute]
OR
FINAL_MESSAGE: [Your handoff message to the next agent or user]
NEXT_AGENT: [The name of the next agent or 'User' or 'COMPLETED']
"""

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt).text
    
    # Basic Loop for Command Execution
    max_turns = 10
    turns = 0
    while "COMMAND:" in response and turns < max_turns:
        turns += 1
        cmd_match = re.search(r"COMMAND:\s*(.*)", response)
        if cmd_match:
            cmd = cmd_match.group(1).strip()
            result = run_shell(f"cd {project_path} && {cmd}")
            feedback_prompt = f"Command output:\n{json.dumps(result, indent=2)}\n\nWhat is your next step?"
            response = model.generate_content(feedback_prompt).text
        else:
            break

    if "FINAL_MESSAGE:" in response:
        msg_match = re.search(r"FINAL_MESSAGE:\s*(.*)", response, re.DOTALL)
        next_match = re.search(r"NEXT_AGENT:\s*@?(\w+)", response)
        if msg_match and next_match:
            msg = msg_match.group(1).strip()
            next_agent = next_match.group(1).lower()
            status = "COMPLETED" if next_agent == "completed" else "IN_PROGRESS"
            update_workspace(workspace_path, agent_name, next_agent, status, msg)
            print(f"✅ Task finished. Handed off to @{next_agent}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        collaborate(Path(sys.argv[1]).absolute())
    else:
        print("Usage: python collaborator.py /path/to/project")
