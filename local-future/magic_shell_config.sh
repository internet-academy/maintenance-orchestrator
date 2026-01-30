# === JARVIS MAGIC SHELL HANDLER ===

# This function runs whenever you type a command that doesn't exist.
command_not_found_handle() {
    # $1, $2, etc are the words you typed.
    local input_text="$*"
    
    # Optional: Ignore short typos (1-2 chars) to be less annoying
    if [ ${#1} -le 2 ]; then
        echo "$1: command not found"
        return 127
    fi

    # Visual indicator that AI is taking over
    echo "🔮 invoking agents..."
    
    # Call the python script
    # We use python3 directly to ensure it runs
    python3 /home/konoh/projects/personal-agents/agent.py "$input_text"
    
    # Return 0 so the shell thinks the command succeeded
    return 0
}
