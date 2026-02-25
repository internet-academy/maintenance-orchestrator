#!/bin/bash

# Log-Miner Specialist: Proactive Debugging Tool
# Usage: ./log_miner.sh [source] [lines] [filter]

SOURCE=${1:-"local"}
LINES=${2:-50}
FILTER=${3:-""}

echo "🔍 Mining logs: Source=$SOURCE, Lines=$LINES, Filter=$FILTER"

case $SOURCE in
    "local")
        # Search for common log locations
        LOG_FILES=$(find ~/ia -name "*.log" -o -name "logfile")
        for f in $LOG_FILES; do
            echo "--- File: $f ---"
            if [ -n "$FILTER" ]; then
                tail -n "$LINES" "$f" | grep -i "$FILTER"
            else
                tail -n "$LINES" "$f"
            fi
        done
        ;;
    "journal")
        if [ -n "$FILTER" ]; then
            journalctl -n "$LINES" | grep -i "$FILTER"
        else
            journalctl -n "$LINES"
        fi
        ;;
    "docker")
        CONTAINERS=$(docker ps --format "{{.Names}}")
        for c in $CONTAINERS; do
            echo "--- Container: $c ---"
            if [ -n "$FILTER" ]; then
                docker logs --tail "$LINES" "$c" 2>&1 | grep -i "$FILTER"
            else
                docker logs --tail "$LINES" "$c" 2>&1
            fi
        done
        ;;
    *)
        echo "❌ Error: Unknown source. Use local, journal, or docker."
        exit 1
        ;;
esac
