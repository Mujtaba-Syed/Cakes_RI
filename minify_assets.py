#!/usr/bin/env python
"""
Minify JavaScript and CSS files for production.
Run this script before deploying or after making changes to JS/CSS files.

Usage:
    python minify_assets.py
"""
import os
import sys
import re
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Try to import minification libraries
try:
    import rjsmin
    import rcssmin
    HAS_MINIFIERS = True
except ImportError:
    HAS_MINIFIERS = False
    print("Warning: rjsmin and rcssmin not installed. Installing...")
    print("Run: pip install rjsmin rcssmin")
    print("\nUsing basic minification (removes comments and whitespace only)")

def basic_js_minify(content):
    """Basic JavaScript minification (removes comments and extra whitespace)"""
    # Remove single-line comments
    content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
    # Remove multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    # Remove extra whitespace
    content = re.sub(r'\s+', ' ', content)
    # Remove whitespace around operators
    content = re.sub(r'\s*([=+\-*/%<>!&|,;:{}()\[\]])\s*', r'\1', content)
    # Remove whitespace at start/end of lines
    content = re.sub(r'^\s+|\s+$', '', content, flags=re.MULTILINE)
    return content.strip()

def basic_css_minify(content):
    """Basic CSS minification (removes comments and extra whitespace)"""
    # Remove comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    # Remove extra whitespace
    content = re.sub(r'\s+', ' ', content)
    # Remove whitespace around colons, semicolons, braces
    content = re.sub(r'\s*([:;{}])\s*', r'\1', content)
    # Remove whitespace around commas
    content = re.sub(r'\s*,\s*', ',', content)
    # Remove leading/trailing whitespace
    content = content.strip()
    return content

def minify_file(file_path, file_type):
    """Minify a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already minified (contains .min in filename)
        if '.min.' in str(file_path):
            print(f"  Skipping {file_path.name} (already minified)")
            return False
        
        # Minify based on type
        if file_type == 'js':
            if HAS_MINIFIERS:
                minified = rjsmin.jsmin(content)
            else:
                minified = basic_js_minify(content)
        elif file_type == 'css':
            if HAS_MINIFIERS:
                minified = rcssmin.cssmin(content)
            else:
                minified = basic_css_minify(content)
        else:
            return False
        
        # Create .min version
        min_file_path = file_path.parent / f"{file_path.stem}.min{file_path.suffix}"
        
        with open(min_file_path, 'w', encoding='utf-8') as f:
            f.write(minified)
        
        # Calculate size reduction
        original_size = len(content)
        minified_size = len(minified)
        reduction = ((original_size - minified_size) / original_size) * 100
        
        print(f"  ✓ {file_path.name} → {min_file_path.name}")
        print(f"    {original_size:,} bytes → {minified_size:,} bytes ({reduction:.1f}% reduction)")
        
        return True
    except Exception as e:
        print(f"  ✗ Error minifying {file_path.name}: {e}")
        return False

def main():
    """Main minification function"""
    print("=" * 60)
    print("Minifying JavaScript and CSS files...")
    print("=" * 60)
    
    static_dir = BASE_DIR / 'static'
    
    if not static_dir.exists():
        print(f"Error: Static directory not found at {static_dir}")
        return
    
    # Files to minify
    js_files = []
    css_files = []
    
    # Find JS files
    for js_file in static_dir.rglob('*.js'):
        if '.min.' not in str(js_file):
            js_files.append(js_file)
    
    # Find CSS files
    for css_file in static_dir.rglob('*.css'):
        if '.min.' not in str(css_file):
            css_files.append(css_file)
    
    print(f"\nFound {len(js_files)} JavaScript files and {len(css_files)} CSS files")
    print("\nMinifying JavaScript files...")
    js_count = 0
    for js_file in js_files:
        if minify_file(js_file, 'js'):
            js_count += 1
    
    print("\nMinifying CSS files...")
    css_count = 0
    for css_file in css_files:
        if minify_file(css_file, 'css'):
            css_count += 1
    
    print("\n" + "=" * 60)
    print(f"Minification complete!")
    print(f"  JavaScript: {js_count} files minified")
    print(f"  CSS: {css_count} files minified")
    print("=" * 60)
    
    if not HAS_MINIFIERS:
        print("\n💡 Tip: Install rjsmin and rcssmin for better minification:")
        print("   pip install rjsmin rcssmin")

if __name__ == '__main__':
    main()

