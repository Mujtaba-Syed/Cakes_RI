#!/bin/bash

# SSL Certificate Renewal Script for cakebyrimi.com
# This script renews an expired Let's Encrypt certificate

set -e  # Exit on error

DOMAIN="cakebyrimi.com"
EMAIL="mujtaba3198@gmail.com"
WEBROOT_PATH="/var/www/certbot"
CERT_PATH="/etc/letsencrypt/live/${DOMAIN}"

echo "=========================================="
echo "SSL Certificate Renewal Script"
echo "Domain: ${DOMAIN}"
echo "=========================================="
echo ""

# Step 1: Check current certificate expiration (if exists)
if [ -f "${CERT_PATH}/fullchain.pem" ]; then
    echo "Step 1: Checking current certificate expiration..."
    echo "Current certificate expires:"
    openssl x509 -in "${CERT_PATH}/fullchain.pem" -text -noout | grep "Not After" || echo "Could not read certificate"
    echo ""
else
    echo "Step 1: No existing certificate found at ${CERT_PATH}"
    echo "This script will request a new certificate instead."
    echo ""
fi

# Step 2: Create certbot webroot directory
echo "Step 2: Creating certbot webroot directory..."
mkdir -p "${WEBROOT_PATH}"
chmod 755 "${WEBROOT_PATH}"
echo "✓ Directory created: ${WEBROOT_PATH}"
echo ""

# Step 3: Ensure nginx is running and can serve ACME challenge
echo "Step 3: Checking nginx status..."
if docker ps | grep -q nginx_server; then
    echo "✓ nginx_server container is running"
    
    # Test nginx configuration
    echo "Testing nginx configuration..."
    docker exec nginx_server nginx -t
    echo "✓ Nginx configuration is valid"
    echo ""
else
    echo "✗ ERROR: nginx_server container is not running!"
    echo "Please start your containers first: docker-compose up -d"
    exit 1
fi

# Step 4: Renew the certificate
echo "Step 4: Renewing SSL certificate..."
echo "This may take a minute..."
echo ""

if [ -f "${CERT_PATH}/fullchain.pem" ]; then
    # Certificate exists - renew it
    certbot renew \
        --cert-name "${DOMAIN}" \
        --force-renewal \
        --webroot \
        --webroot-path="${WEBROOT_PATH}" \
        --non-interactive \
        --agree-tos \
        --email "${EMAIL}"
else
    # Certificate doesn't exist - request new one
    certbot certonly \
        --webroot \
        --webroot-path="${WEBROOT_PATH}" \
        --email "${EMAIL}" \
        --agree-tos \
        --non-interactive \
        --domains "${DOMAIN}" \
        --domains "www.${DOMAIN}"
fi

if [ $? -eq 0 ]; then
    echo "✓ Certificate renewed successfully!"
    echo ""
else
    echo "✗ ERROR: Certificate renewal failed!"
    echo "Please check the error messages above."
    exit 1
fi

# Step 5: Reload nginx to use the new certificate
echo "Step 5: Reloading nginx to apply new certificate..."
docker exec nginx_server nginx -s reload
if [ $? -eq 0 ]; then
    echo "✓ Nginx reloaded successfully"
    echo ""
else
    echo "✗ WARNING: Nginx reload failed, but certificate was renewed."
    echo "You may need to manually reload: docker exec nginx_server nginx -s reload"
    echo ""
fi

# Step 6: Verify the new certificate
echo "Step 6: Verifying new certificate..."
if [ -f "${CERT_PATH}/fullchain.pem" ]; then
    echo "New certificate expires:"
    openssl x509 -in "${CERT_PATH}/fullchain.pem" -text -noout | grep "Not After"
    echo ""
    echo "=========================================="
    echo "✓ Certificate renewal completed successfully!"
    echo "Your site should now work with HTTPS."
    echo "=========================================="
else
    echo "✗ WARNING: Could not verify certificate file exists"
    exit 1
fi
