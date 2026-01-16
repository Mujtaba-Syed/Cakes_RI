#!/bin/sh

# Remove any existing default.conf first
rm -f /etc/nginx/conf.d/default.conf

# Check if DJANGO_ENV is set to production
if [ "$DJANGO_ENV" = "production" ]; then
    echo "Using production nginx config (with SSL)"
    cp /tmp/nginx.prod.conf /etc/nginx/conf.d/default.conf
else
    echo "Using development nginx config (HTTP only)"
    cp /tmp/nginx.dev.conf /etc/nginx/conf.d/default.conf
fi

# Test nginx configuration
nginx -t

# Start nginx
exec nginx -g "daemon off;"

