#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fix encoding issues in business_games.py"""

filepath = 'c:/Users/pksia/Dropbox/BVA/views/business_games.py'

# Read file
with open(filepath, 'rb') as f:
    content = f.read()

# Remove BOM if present
if content.startswith(b'\xef\xbb\xbf'):
    content = content[3:]
    print("Removed BOM")

# Write back without BOM
with open(filepath, 'wb') as f:
    f.write(content)

print("File fixed!")
