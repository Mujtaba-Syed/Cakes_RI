#!/usr/bin/env python
"""
Django management command wrapper for minification.
This integrates with Django's management command system.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.core.management import call_command

if __name__ == '__main__':
    # Run the minify script
    from minify_assets import main
    main()

