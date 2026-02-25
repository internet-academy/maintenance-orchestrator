#!/bin/bash
# Global Brain (Surgical): Quiet knowledge retrieval.
KEYWORD=$1
[ -z "$KEYWORD" ] && exit 1

echo "🧠 Searching for: '$KEYWORD'..."
# Search only in the root of project directories for main logs
find ~/ia ~/projects ~/personal-projects -maxdepth 2 \( -name "active_logs.md" -o -name "user_profile.md" -o -name "GEMINI.md" \) -exec grep -Hni "$KEYWORD" {} + | head -n 10
