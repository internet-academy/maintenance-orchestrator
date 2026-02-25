#!/bin/bash
# Janitor Protocol: Workspace Maintenance
echo "🧹 Janitor: Cleaning up workspace..."

# 1. Remove orphaned Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# 2. Remove temporary simulation files
rm -f simulation_request.txt 2>/dev/null

# 3. List but don't delete blueprints (they are useful)
echo "✅ Blueprints preserved. Temporary files cleared."
