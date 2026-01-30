#!/bin/bash

# Agent Sync Utility
# Usage: ./agent-sync.sh [message]

# Target Directory - ADJUST THIS IF NEEDED
AGENT_DIR="$HOME/projects/personal-agents"

if [ -d "$AGENT_DIR" ]; then
    cd "$AGENT_DIR" || exit
else
    echo "❌ Error: Directory $AGENT_DIR not found."
    exit 1
fi

# 1. Pull latest changes (with rebase to avoid merge bubbles)
echo "🔄 Syncing Agent Memories..."
git pull --rebase --autostash origin main

# 2. Add all changes
git add .

# 3. Commit (default message if none provided)
COMMIT_MSG=${1:-"Auto-update: $(date '+%Y-%m-%d %H:%M:%S')"}

# Check if there are changes to commit
if git diff-index --quiet HEAD --; then
    echo "✅ No local changes to save."
else
    git commit -m "$COMMIT_MSG"
    echo "💾 Saved local changes."
    # 4. Push to cloud (only if we committed something or just want to ensure sync)
    git push origin main
    echo "🚀 Agent Memories Synced."
fi
