#!/bin/bash

# Setup script for automatic SSL certificate renewal via cron
# This will add a cron job to renew certificates every 60 days

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RENEWAL_SCRIPT="${SCRIPT_DIR}/renew-certbot-cron.sh"

echo "Setting up automatic SSL certificate renewal..."
echo ""

# Make the renewal script executable
chmod +x "$RENEWAL_SCRIPT"
echo "✓ Made renewal script executable"

# Create log directory if it doesn't exist
mkdir -p /var/log
echo "✓ Log directory ready"

# Add cron job (runs monthly on the 1st at 3 AM)
# Note: Certbot will only actually renew if certificate expires within 30 days
# This is safer than waiting 60 days - we check monthly but only renew when needed
CRON_JOB="0 3 1 * * $RENEWAL_SCRIPT"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "renew-certbot-cron.sh"; then
    echo "⚠ Cron job already exists. Removing old entry..."
    crontab -l 2>/dev/null | grep -v "renew-certbot-cron.sh" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
echo "✓ Cron job added successfully"
echo ""
echo "Cron job details:"
echo "  Schedule: Monthly on the 1st at 3:00 AM"
echo "  Script: $RENEWAL_SCRIPT"
echo "  Log: /var/log/certbot-renewal.log"
echo "  Note: Certbot will only renew if certificate expires within 30 days"
echo ""
echo "To view your cron jobs: crontab -l"
echo "To remove this cron job: crontab -e (then delete the line)"
echo ""
echo "✓ Automatic renewal setup complete!"
