#!/bin/bash

echo "Setting up Docker nginx for cakebyrimi.com..."

# Remove any existing system nginx config for cake project
rm -f /etc/nginx/sites-enabled/cakebyrimi.com
rm -f /etc/nginx/sites-available/cakebyrimi.com

echo "System nginx config removed."
echo "Using Docker nginx only."
echo ""
echo "To start your cake project:"
echo "docker-compose up -d --build"
echo ""
echo "Your cake site will be accessible at: http://cakebyrimi.com:8002" 