#!/bin/bash

# Global Brain: Cross-Project Knowledge Retrieval
# Usage: ./global_brain.sh [keyword]

KEYWORD=$1

if [ -z "$KEYWORD" ]; then
    echo "❌ Usage: ./global_brain.sh [keyword]"
    exit 1
fi

echo "🧠 Searching Global Brain for: '$KEYWORD'..."

# Define search paths
SEARCH_PATHS=(
    "$HOME/ia"
    "$HOME/projects"
    "$HOME/personal-projects"
)

for path in "${SEARCH_PATHS[@]}"; do
    if [ -d "$path" ]; then
        # Search for LESSONS LEARNED or general logs
        grep -r -i -A 5 -B 2 "$KEYWORD" "$path" 
            --include="active_logs.md" 
            --include="user_profile.md" 
            --include="GEMINI.md" 
            --exclude-dir=".git" 
            --exclude-dir="node_modules" 
            --exclude-dir="venv"
    fi
done
