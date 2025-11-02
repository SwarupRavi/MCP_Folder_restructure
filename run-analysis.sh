#!/bin/bash
# Automated folder analysis script - runs every 6 hours

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/analysis-reports"
ANALYZE_DIR="$HOME/Downloads"  # Change this to analyze different directories

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Generate timestamp for filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_FILE="$OUTPUT_DIR/analysis_${TIMESTAMP}.json"

# Run all analyses and combine into one report
echo "Running folder analysis at $(date)" > "$OUTPUT_DIR/last_run.log"

# Create JSON report
cat > "$REPORT_FILE" << EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "analyzed_directory": "$ANALYZE_DIR",
EOF

# Large files analysis
echo "  \"large_files\": " >> "$REPORT_FILE"
python3 "$SCRIPT_DIR/folder_restructure_mcp/cli.py" large "$ANALYZE_DIR" 50 20 >> "$REPORT_FILE" 2>> "$OUTPUT_DIR/last_run.log"
echo "," >> "$REPORT_FILE"

# Duplicates analysis
echo "  \"duplicates\": " >> "$REPORT_FILE"
python3 "$SCRIPT_DIR/folder_restructure_mcp/cli.py" duplicates "$ANALYZE_DIR" 100 >> "$REPORT_FILE" 2>> "$OUTPUT_DIR/last_run.log"
echo "," >> "$REPORT_FILE"

# File statistics
echo "  \"statistics\": " >> "$REPORT_FILE"
python3 "$SCRIPT_DIR/folder_restructure_mcp/cli.py" stats "$ANALYZE_DIR" >> "$REPORT_FILE" 2>> "$OUTPUT_DIR/last_run.log"
echo "," >> "$REPORT_FILE"

# Extensions analysis
echo "  \"extensions\": " >> "$REPORT_FILE"
python3 "$SCRIPT_DIR/folder_restructure_mcp/cli.py" extensions "$ANALYZE_DIR" 15 >> "$REPORT_FILE" 2>> "$OUTPUT_DIR/last_run.log"
echo "," >> "$REPORT_FILE"

# Cleanup suggestions
echo "  \"cleanup_suggestions\": " >> "$REPORT_FILE"
python3 "$SCRIPT_DIR/folder_restructure_mcp/cli.py" cleanup "$ANALYZE_DIR" 180 5 >> "$REPORT_FILE" 2>> "$OUTPUT_DIR/last_run.log"

# Close JSON
echo "}" >> "$REPORT_FILE"

# Log completion
echo "Analysis completed at $(date)" >> "$OUTPUT_DIR/last_run.log"
echo "Report saved to: $REPORT_FILE" >> "$OUTPUT_DIR/last_run.log"

# Keep only last 30 reports (cleanup old ones)
cd "$OUTPUT_DIR"
ls -t analysis_*.json | tail -n +31 | xargs -r rm

echo "Report generated: $REPORT_FILE"
