#!/bin/bash
# Setup cron job for automated folder analysis

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_SCRIPT="$SCRIPT_DIR/run-analysis.sh"

echo "Setting up cron job to run every 6 hours..."

# Create cron entry
CRON_ENTRY="0 */6 * * * $CRON_SCRIPT >> $SCRIPT_DIR/analysis-reports/cron.log 2>&1"

# Check if cron entry already exists
if crontab -l 2>/dev/null | grep -q "$CRON_SCRIPT"; then
    echo "Cron job already exists!"
    echo "Current cron jobs:"
    crontab -l | grep "$CRON_SCRIPT"
else
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    echo "✓ Cron job added successfully!"
    echo ""
    echo "Schedule: Every 6 hours (at 00:00, 06:00, 12:00, 18:00)"
    echo "Script: $CRON_SCRIPT"
    echo "Reports: $SCRIPT_DIR/analysis-reports/"
fi

echo ""
echo "To view all cron jobs:"
echo "  crontab -l"
echo ""
echo "To remove this cron job:"
echo "  crontab -l | grep -v '$CRON_SCRIPT' | crontab -"
echo ""
echo "To test the script manually:"
echo "  $CRON_SCRIPT"
