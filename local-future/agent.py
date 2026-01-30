#!/usr/bin/env python3
import sys
import os
import subprocess

# --- CONFIGURATION ---
LLM_COMMAND = ["ollama", "run", "llama3"]
# LLM_COMMAND = ["echo", "LLM backend not connected. Prompt:"] 

AGENTS_DIR = os.path.dirname(os.path.abspath(__file__))

def get_available_agents():
    return [f.replace('.md', '') for f in os.listdir(AGENTS_DIR) if f.endswith('.md') and f != 'router.md']

def load_agent_profile(agent_name):
    filename = os.path.join(AGENTS_DIR, f"{agent_name}.md")
    if not os.path.exists(filename):
        # Fallback for generic
        if agent_name == "general":
            return "You are a helpful AI assistant."
        return None
    with open(filename, 'r') as f:
        return f.read()

def run_llm(system_prompt, user_query, quiet=False):
    full_prompt = f"{system_prompt}\n\nUSER REQUEST: {user_query}\n\nRESPONSE:")
    
    if LLM_COMMAND[0] == "echo":
        if not quiet:
            print(full_prompt)
        return "mock_response"

    try:
        process = subprocess.Popen(
            LLM_COMMAND, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=full_prompt)
        if process.returncode != 0:
            print(f"LLM Error: {stderr}")
            return None
        return stdout.strip()
    except FileNotFoundError:
        print(f"Error: Command '{LLM_COMMAND[0]}' not found.")
        sys.exit(1)

def route_request(query):
    router_profile = load_agent_profile('router')
    if not router_profile:
        return 'general'
    
    # Run the router
    # We pass the query to the router agent
    response = run_llm(router_profile, query, quiet=True)
    
    # Clean up response (sometimes LLMs add extra text)
    predicted_agent = response.split('\n')[-1].strip().lower()
    
    # Remove punctuation
    predicted_agent = "".join(ch for ch in predicted_agent if ch.isalnum())
    
    if predicted_agent in get_available_agents():
        return predicted_agent
    return 'general'

def main():
    if len(sys.argv) < 2:
        print("Usage: agent [agent_name] <query>")
        sys.exit(1)

    available_agents = get_available_agents()
    
    first_arg = sys.argv[1].lower()
    
    target_agent = ""
    query = ""

    # Check if the first argument is a known agent
    if first_arg in available_agents:
        target_agent = first_arg
        query = " ".join(sys.argv[2:])
    else:
        # Auto-detect mode
        query = " ".join(sys.argv[1:])
        print(f"⚡ Analyzing request...")
        target_agent = route_request(query)
        print(f"👉 Routing to: {target_agent.upper()}")

    if not query:
        print("Error: Empty query.")
        sys.exit(1)

    profile = load_agent_profile(target_agent)
    if not profile:
        print(f"Could not load profile for {target_agent}")
        sys.exit(1)

    # Stream the final response to the user
    # We reconstruct the prompt here for the final call
    final_prompt = f"{profile}\n\nUSER REQUEST: {query}\n\nRESPONSE:")
    
    if LLM_COMMAND[0] == "echo":
        print(f"--- [Agent: {target_agent.upper()}] ---")
        print(final_prompt)
    else:
        # For the final output, we want to stream it directly to stdout
        subprocess.run(
            LLM_COMMAND, 
            input=final_prompt, 
            text=True
        )

if __name__ == "__main__":
    main()