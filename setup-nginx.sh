#!/bin/bash

echo "Setting up nginx for cakebyrimi.com..."

# Copy the nginx configuration
cp nginx/main-nginx.conf /etc/nginx/sites-available/cakebyrimi.com

# Enable the site
ln -s /etc/nginx/sites-available/cakebyrimi.com /etc/nginx/sites-enabled/

# Test nginx configuration
nginx -t

if [ $? -eq 0 ]; then
    echo "Nginx configuration is valid!"
    echo "Reloading nginx..."
    systemctl reload nginx
    echo "Setup completed!"
    echo "Your cake site should now be accessible at: http://cakebyrimi.com"
else
    echo "Error: Nginx configuration test failed!"
    echo "Please check the configuration manually."
fi 