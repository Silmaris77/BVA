#!/usr/bin/env python3
"""
Add line-height: 1.8 to all <p>, <ul>, and <ol> tags in JSS Rules sections
"""
import json
import re

file_path = r'c:\Users\pksia\Dropbox\BVA\data\lessons\MILWAUKEE_JSS_Rules_of_Engagement.json'

# Read file
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Process each section
sections = data['sections']['learning']['sections']
for section in sections:
    content = section['content']
    
    # Add line-height to <p> tags that don't have it
    content = re.sub(
        r'<p>',
        r"<p style='line-height: 1.8;'>",
        content
    )
    
    # Add line-height to <ul> tags that don't have it
    content = re.sub(
        r'<ul>',
        r"<ul style='line-height: 1.8;'>",
        content
    )
    
    # Add line-height to <ol> tags that don't have it
    content = re.sub(
        r'<ol>',
        r"<ol style='line-height: 1.8;'>",
        content
    )
    
    section['content'] = content
    print(f"✓ Processed Section {section['id']}: {section['title'][:50]}...")

# Save file
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Successfully added line-height styling to all 5 sections!")
print(f"📄 File: {file_path}")
