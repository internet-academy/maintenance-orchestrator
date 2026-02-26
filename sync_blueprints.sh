#!/bin/bash

# Continuous Blueprint Sync: Keeping L1-L4 maps aligned with code.
# Usage: ./sync_blueprints.sh [member|bohr]

REPO=$1
BASE_DIR="$HOME/projects/personal-agents"
VENV_PY="$BASE_DIR/venv/bin/python"

echo "🔄 Syncing Blueprints for: ${REPO:-ALL}..."

sync_repo() {
    local name=$1
    local path=$2
    local output=$3
    
    echo "🏗  Refreshing $name (L1-L3)..."
    $VENV_PY "$BASE_DIR/scanner.py" "$path" --output "$BASE_DIR/$output"
    
    echo "🧠 Refreshing $name Semantics (L4)..."
    # Note: Semantic indexer uses caching, so it only scans NEW/CHANGED files.
    $VENV_PY "$BASE_DIR/semantic_indexer.py" "$path" "$BASE_DIR/${name}_semantics.md"
    
    # Merge L4 into main blueprint
    sed -i '/### 🌌 L4 SEMANTIC/,$d' "$BASE_DIR/$output"
    cat "$BASE_DIR/${name}_semantics.md" >> "$BASE_DIR/$output"
}

if [ "$REPO" == "member" ]; then
    sync_repo "member" "$HOME/ia/member" "member_blueprint.md"
elif [ "$REPO" == "bohr" ]; then
    sync_repo "bohr" "$HOME/ia/bohr-individual" "bohr_blueprint.md"
else
    sync_repo "member" "$HOME/ia/member" "member_blueprint.md"
    sync_repo "bohr" "$HOME/ia/bohr-individual" "bohr_blueprint.md"
fi

echo "✅ Blueprints Synchronized."
