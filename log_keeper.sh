#!/bin/bash
# 1. Write the log content (standard input) to the file
cat > /home/konoh/projects/personal-agents/active_logs.md

# 2. Trigger Auto-Sync (Run in background to not block the agent)
# We use the existing agent-sync.sh to handle git operations
if [ -f "/home/konoh/projects/personal-agents/agent-sync.sh" ]; then
    /home/konoh/projects/personal-agents/agent-sync.sh "Auto-save: Active Log Update" > /dev/null 2>&1 &
fi
