#!/bin/bash

# Automated SSL Certificate Renewal Script for Cron
# This script is designed to be run automatically (e.g., every 60 days)
# It only renews if the certificate is close to expiring (within 30 days)

set -e

DOMAIN="cakebyrimi.com"
WEBROOT_PATH="/var/www/certbot"
CERT_PATH="/etc/letsencrypt/live/${DOMAIN}"
NGINX_CONTAINER="nginx_server"
LOG_FILE="/var/log/certbot-renewal.log"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "Starting certificate renewal check..."
log "=========================================="

# Check if certificate exists
if [ ! -f "${CERT_PATH}/fullchain.pem" ]; then
    log "ERROR: Certificate not found at ${CERT_PATH}/fullchain.pem"
    exit 1
fi

# Check if nginx container is running
if ! docker ps | grep -q "$NGINX_CONTAINER"; then
    log "ERROR: nginx_server container is not running!"
    exit 1
fi

# Ensure webroot directory exists
mkdir -p "${WEBROOT_PATH}"
chmod 755 "${WEBROOT_PATH}"

# Use certbot's built-in renewal (it only renews if within 30 days of expiration)
log "Attempting certificate renewal..."
if certbot renew --webroot --webroot-path="${WEBROOT_PATH}" --quiet --no-random-sleep-on-renewal; then
    # Check if certificate was actually renewed
    if [ -f "${CERT_PATH}/fullchain.pem" ]; then
        # Get expiration date
        EXPIRY=$(openssl x509 -in "${CERT_PATH}/fullchain.pem" -text -noout | grep "Not After" | cut -d: -f2-)
        log "Certificate renewed successfully. New expiry: $EXPIRY"
        
        # Reload nginx
        if docker exec "$NGINX_CONTAINER" nginx -s reload; then
            log "Nginx reloaded successfully"
        else
            log "WARNING: Nginx reload failed, but certificate was renewed"
        fi
    else
        log "Certificate was not renewed (still valid for more than 30 days)"
    fi
else
    log "ERROR: Certificate renewal failed!"
    exit 1
fi

log "Renewal check completed"
log "=========================================="
