#!/bin/bash

# Notion-GitHub Sync Script
# Usage: ./sync.sh [sync|pull|push|status]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Default command is 'sync'
COMMAND=${1:-sync}

echo "🚀 Running notion_sync $COMMAND..."
echo ""

python -m notion_sync "$COMMAND" "${@:2}"

