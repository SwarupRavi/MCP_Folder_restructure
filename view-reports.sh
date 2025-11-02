#!/bin/bash
# View analysis reports

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORTS_DIR="$SCRIPT_DIR/analysis-reports"

if [ ! -d "$REPORTS_DIR" ]; then
    echo "No reports directory found. Run an analysis first."
    exit 1
fi

echo "=== Folder Analysis Reports ==="
echo ""

# Show last run info
if [ -f "$REPORTS_DIR/last_run.log" ]; then
    echo "Last run:"
    tail -2 "$REPORTS_DIR/last_run.log"
    echo ""
fi

# List all reports
echo "Available reports:"
ls -lht "$REPORTS_DIR"/analysis_*.json | head -10

echo ""
echo "Commands:"
echo "  View latest report:     cat $REPORTS_DIR/\$(ls -t $REPORTS_DIR/analysis_*.json | head -1)"
echo "  View with formatting:   cat $REPORTS_DIR/\$(ls -t $REPORTS_DIR/analysis_*.json | head -1) | python3 -m json.tool"
echo "  Open in editor:         open $REPORTS_DIR/\$(ls -t $REPORTS_DIR/analysis_*.json | head -1)"

# Show latest report summary if requested
if [ "$1" == "--latest" ] || [ "$1" == "-l" ]; then
    LATEST=$(ls -t "$REPORTS_DIR"/analysis_*.json | head -1)
    echo ""
    echo "=== Latest Report Summary ==="
    echo "File: $LATEST"
    echo ""
    python3 -m json.tool "$LATEST" | head -50
fi
