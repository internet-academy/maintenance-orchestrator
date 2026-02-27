#!/bin/bash

# Continuous Blueprint Sync: Keeping L1-L4 maps aligned with code.
# Optimized to avoid rate limits by excluding large static/media assets.
# Usage: ./sync_blueprints.sh [member|bohr]

REPO=$1
BASE_DIR="$HOME/projects/personal-agents"
VENV_PY="$BASE_DIR/venv/bin/python"
TEMP_DIR="/tmp/blueprint_sync_$REPO"

echo "🔄 Syncing Blueprints for: ${REPO:-ALL}..."

sync_repo() {
    local name=$1
    local src_path=$2
    local output=$3
    
    echo "🧹 Preparing clean copy for $name (excluding static/media)..."
    rm -rf "$TEMP_DIR"
    mkdir -p "$TEMP_DIR"
    # Use rsync to create a slimmed-down copy of the code for analysis
    rsync -av --exclude='static/' --exclude='media/' --exclude='.git/' --exclude='.venv/' "$src_path/" "$TEMP_DIR/" > /dev/null

    echo "🏗  Refreshing $name (L1-L3)..."
    $VENV_PY "$BASE_DIR/scanner.py" "$TEMP_DIR" --output "$BASE_DIR/$output"
    
    echo "🧠 Refreshing $name Semantics (L4)..."
    $VENV_PY "$BASE_DIR/semantic_indexer.py" "$TEMP_DIR" "$BASE_DIR/${name}_semantics.md"
    
    # Merge L4 into main blueprint
    sed -i '/### 🌌 L4 SEMANTIC/,$d' "$BASE_DIR/$output"
    cat "$BASE_DIR/${name}_semantics.md" >> "$BASE_DIR/$output"
    
    rm -rf "$TEMP_DIR"
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
