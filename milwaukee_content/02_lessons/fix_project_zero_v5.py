import re

src = r"c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FULL.sql"
dst = r"c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FINAL.sql"

print(f"Reading {src}...")
with open(src, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Heading -> Title
content = content.replace('"heading":', '"title":')

# 2. Polish quotes -> single quotes (NO ESCAPE NEEDED for $$ quoting)
content = content.replace('„', "'")
content = content.replace('”', "'")
content = content.replace('“', "'")

# 3. Fix quotes at end of sentences
# Replace ". with '. (Quote Dot -> SingleQuote Dot)
content = content.replace('".', "'.")

# 4. Remove any backslashes before single quotes if they exist
# In case source had \' or previous tools introduced it
content = content.replace("\\'", "'")

# 5. Fix remember structure
pattern = r'"remember":\s*\{\s*"icon":\s*"[^"]+",\s*"text":\s*"([^"]+)"\s*\}'
def fix_remember(match):
    text = match.group(1)
    # Ensure text doesn't contain unescaped double quotes (JSON strict)
    # But usually text inside definition was safe.
    # If text has ', it's fine.
    return f'"remember": {{ "title": "Zapamiętaj", "items": ["{text}"] }}'
content = re.sub(pattern, fix_remember, content)

# 6. Apply Dollar Quoting ($$)
content = content.replace("content = '{", "content = $$ {")
content = content.replace("}'::jsonb", "}$$::jsonb")
if "$$" not in content:
    content = re.sub(r"content\s*=\s*'{", "content = $$ {", content)
    content = re.sub(r"}'::jsonb", "}$$::jsonb", content)

print(f"Writing {dst}...")
with open(dst, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. No escaped single quotes allowed in JSON.")
