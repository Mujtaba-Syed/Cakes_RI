#!/bin/bash

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Collect static files
python manage.py collectstatic --noinput

# Run the development server
python manage.py runserver 0.0.0.0:8000 