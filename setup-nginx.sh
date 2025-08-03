#!/bin/bash

echo "Setting up nginx for both domains..."

# Backup current nginx config
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# Copy the combined nginx configuration
cp nginx/combined-nginx.conf /etc/nginx/nginx.conf

# Test nginx configuration
nginx -t

if [ $? -eq 0 ]; then
    echo "Nginx configuration is valid!"
    echo "Reloading nginx..."
    systemctl reload nginx
    echo "Setup completed!"
    echo "Your sites should now be accessible at:"
    echo "- QnH Enterprises: https://qhenterprises.com"
    echo "- Cake project: http://cakebyrimi.com"
else
    echo "Error: Nginx configuration test failed!"
    echo "Restoring backup..."
    cp /etc/nginx/nginx.conf.backup /etc/nginx/nginx.conf
    echo "Please check the configuration manually."
fi 