#!/bin/bash
# Minification script for Cake by Rimi
# Run this before deploying to production

echo "Starting minification process..."

# Install minification libraries if not already installed
pip install -q rjsmin rcssmin

# Run the minification script
python minify_assets.py

# Collect static files (Django will use the .min versions if available)
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "Minification complete! ✅"

