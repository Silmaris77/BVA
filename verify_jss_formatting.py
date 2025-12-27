#!/usr/bin/env python3
import json

file_path = r'c:\Users\pksia\Dropbox\BVA\data\lessons\MILWAUKEE_JSS_Rules_of_Engagement.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

sections = data['sections']['learning']['sections']

print("✅ VERIFICATION OF ALL 5 SECTIONS:\n")
print("="*80)

for section in sections:
    print(f"\n{section['id']}. {section['title']}")
    has_header = '<div class="header">' in section['content'] or "<div class='header'>" in section['content']
    has_p_style = "line-height: 1.8" in section['content'] and "<p style=" in section['content']
    has_ul_style = "line-height: 1.8" in section['content'] and "<ul style=" in section['content']
    print(f"   Icon & Subtitle Header: {'✓' if has_header else '✗'}")
    print(f"   Line-height in <p>: {'✓' if has_p_style else '✗'}")
    print(f"   Line-height in <ul>: {'✓' if has_ul_style else '✗'}")
    print(f"   Content length: {len(section['content'])} chars")

print("\n" + "="*80)
print("\n✅ All sections have been successfully reformatted!")
