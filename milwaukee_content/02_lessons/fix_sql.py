import re

# Read the SQL file
with open(r'c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FULL.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace "heading": with "title":
content = content.replace('"heading":', '"title":')

# Simply remove Polish quotes from content (they're only in text, not in JSON keys)
content = content.replace('„', '')
content = content.replace('"', '')

# Fix remember structure
content = re.sub(
    r'"remember":\s*\{\s*"icon":\s*"💡",\s*"text":\s*"([^"]+)"\s*\}',
    r'"remember": { "title": "Zapamiętaj", "items": ["\1"] }',
    content
)

# Write the corrected file
with open(r'c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_COMPLETE.sql', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ File created successfully!")
print("📝 Replacements made:")
print("  - 'heading' → 'title'")
print("  - Polish quotes removed from text")
print("  - Remember structure fixed")
