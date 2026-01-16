"""
Custom template tags for automatic minification support.
Automatically uses .min.js and .min.css files in production.
"""
from django import template
from django.conf import settings
from django.templatetags.static import static as django_static
import os
from pathlib import Path

register = template.Library()

@register.simple_tag
def static_min(path):
    """
    Returns the minified version of a static file if it exists and DEBUG is False.
    Otherwise returns the original file.
    
    Usage:
        {% load minify_tags %}
        <script src="{% static_min 'js/home.js' %}"></script>
    """
    # In development, use original files
    if settings.DEBUG:
        return django_static(path)
    
    # In production, try to use .min version
    path_obj = Path(path)
    
    # Check if file already has .min in name
    if '.min.' in path:
        return django_static(path)
    
    # Try to find .min version
    min_path = path_obj.parent / f"{path_obj.stem}.min{path_obj.suffix}"
    min_path_str = str(min_path).replace('\\', '/')
    
    # Check if minified file exists in staticfiles
    static_root = Path(settings.STATIC_ROOT) if hasattr(settings, 'STATIC_ROOT') else None
    if static_root and static_root.exists():
        full_min_path = static_root / min_path_str
        if full_min_path.exists():
            return django_static(min_path_str)
    
    # Check in static directories
    for static_dir in settings.STATICFILES_DIRS:
        full_min_path = Path(static_dir) / min_path_str
        if full_min_path.exists():
            return django_static(min_path_str)
    
    # Fallback to original file
    return django_static(path)

