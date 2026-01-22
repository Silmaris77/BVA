import re
import os

src = r"c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FULL.sql"
dst = r"c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FINAL.sql"

print(f"Reading {src}...")
with open(src, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Heading -> Title
content = content.replace('"heading":', '"title":')

# 2. Polish quotes
content = content.replace('„', "'")
content = content.replace('”', "'")
content = content.replace('“', "'")

# 3. Fix unescaped quotes at end of sentences (Quote followed by Dot)
# Matches " followed by . and replaces with '.
content = content.replace('".', "'.")

# 4. Fix remember structure
# From: "remember": { "icon": "...", "text": "..." }
# To: "remember": { "title": "Zapamiętaj", "items": ["..."] }
# Using dotall to match across lines if needed, but usually on one line or close.
# We capture the text content.
# We trust that the text content's quotes are handled or the regex effectively captures until the closing " of the value.
# The previous step replaced ". with '. so typical sentence end is safe.
# We typically have "text": "Some text." }
# The regex will look for "text":\s*" (content) " \s* }
pattern = r'"remember":\s*\{\s*"icon":\s*"[^"]+",\s*"text":\s*"([^"]+)"\s*\}'

def fix_remember(match):
    text = match.group(1)
    # Ensure any remaining inner quotes in text are escaped or handled? 
    # Whatever was captured is safe definition-wise.
    return f'"remember": {{ "title": "Zapamiętaj", "items": ["{text}"] }}'

content = re.sub(pattern, fix_remember, content)

print(f"Writing {dst}...")
with open(dst, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. File created.")
