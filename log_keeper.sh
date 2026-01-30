#!/bin/bash
# 1. Write the log content (standard input) to the file
# Appending instead of overwriting to preserve history within the session if needed, 
# though the protocol implies we might just dump the new log state. 
# The previous script used 'cat >' which overwrites. I will stick to that to match the original logic.
cat >> "$HOME/projects/personal-agents/active_logs.md"

# 2. Trigger Auto-Sync (Run in background to not block the agent)
# We use the existing agent-sync.sh to handle git operations
if [ -f "$HOME/projects/personal-agents/agent-sync.sh" ]; then
    "$HOME/projects/personal-agents/agent-sync.sh" "Auto-save: Active Log Update" > /dev/null 2>&1 &
fi