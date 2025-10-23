"""Fix use_container_width deprecation warning"""
import os
from pathlib import Path

def fix_file(filepath):
    """Replace use_container_width with width in a file"""
    try:
        # Read with UTF-8 encoding
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if any changes needed
        if 'use_container_width' not in content:
            return False
        
        # Make replacements
        original = content
        content = content.replace('use_container_width=True', 'width="stretch"')
        content = content.replace('use_container_width=False', 'width="content"')
        
        # Write back with UTF-8 encoding
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {filepath}")
            return True
        else:
            print(f"⚠️ No changes needed: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing {filepath}: {e}")
        return False

# Find all Python files in views directory
views_dir = Path(r"c:\Users\pksia\Dropbox\BVA\views")
fixed_count = 0

for py_file in views_dir.glob("*.py"):
    if fix_file(py_file):
        fixed_count += 1

print(f"\n🎉 Fixed {fixed_count} files")
