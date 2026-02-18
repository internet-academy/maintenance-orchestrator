#!/bin/bash
PROJECT_PATH=$1
if [ -z "$PROJECT_PATH" ]; then
    echo "Usage: ./start_autonomy.sh /home/min/projects/your-project"
    exit 1
fi

VENV_PATH="/home/min/projects/personal-agents/venv/bin/activate"
source "$VENV_PATH"

echo "🚀 Launching Autonomous Squad for $PROJECT_PATH..."
python /home/min/projects/personal-agents/collaborator.py "$PROJECT_PATH"
