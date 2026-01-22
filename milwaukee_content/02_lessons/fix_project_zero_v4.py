import re

src = r"c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FULL.sql"
dst = r"c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FINAL.sql"

print(f"Reading {src}...")
with open(src, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Heading -> Title
content = content.replace('"heading":', '"title":')

# 2. Polish quotes -> single quotes
content = content.replace('„', "'")
content = content.replace('”', "'")
content = content.replace('“', "'")

# 3. Fix unescaped quotes at end of sentences
content = content.replace('".', "'.")

# 4. Fix remember structure
pattern = r'"remember":\s*\{\s*"icon":\s*"[^"]+",\s*"text":\s*"([^"]+)"\s*\}'
def fix_remember(match):
    text = match.group(1)
    return f'"remember": {{ "title": "Zapamiętaj", "items": ["{text}"] }}'
content = re.sub(pattern, fix_remember, content)

# 5. CRITICAL FIX: Use Dollar Quoting ($$) for SQL string
# Replace content = '{ with content = $$ {
content = content.replace("content = '{", "content = $$ {")
# Replace }'::jsonb with }$$::jsonb
content = content.replace("}'::jsonb", "}$$::jsonb")

# Also handle if there were newlines or spaces in the original hook points
# Fallback regex for robust replacement if simple string replace fails?
# The file structure is pretty consistent, but let's be safe.
if "$$" not in content:
    # Try regex if simple replace failed due to whitespace
    content = re.sub(r"content\s*=\s*'{", "content = $$ {", content)
    content = re.sub(r"}'::jsonb", "}$$::jsonb", content)

print(f"Writing {dst}...")
with open(dst, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. File created with $$ quoting.")
