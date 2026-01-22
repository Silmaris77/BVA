import re
import os
import json

src = r"c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FULL.sql"
dst = r"c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FINAL.sql"

if os.path.exists(dst):
    os.remove(dst)

print(f"Reading {src}...")
with open(src, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Heading -> Title
content = content.replace('"heading":', '"title":')

# 2. Polish quotes -> simple quotes
content = content.replace('„', "'").replace('”', "'").replace('“', "'")

# 3. Fix unescaped quotes at end of sentences
content = content.replace('".', "'.")

# 4. Remove any backslashes before single quotes
content = content.replace("\\'", "'")

# 5. Fix remember structure
pattern = r'"remember":\s*\{\s*"icon":\s*"[^"]+",\s*"text":\s*"([^"]+)"\s*\}'
content = re.sub(pattern, lambda m: f'"remember": {{ "title": "Zapamiętaj", "items": ["{m.group(1)}"] }}', content)

# 6. INJECT MISSING DATA using json.dumps for safety
branza_text = "**22,5%** wszystkich wypadków śmiertelnych i **12,9%** pozostałych wypadków w UE to budownictwo.\n\nW Polsce historycznie: **13 wypadków dziennie** na budowach, z jedną osobą tracącą życie co tydzień.\n\n*Źródła: Eurostat (2023), Państwowa Inspekcja Pracy (2016-2020)*"
ryzyko_text = "Pracownicy bez PPE są **3 razy częściej** narażeni na urazy niż ci, którzy używają PPE prawidłowo.\n\nStatystyki pokazują, że około **59,4%** pracowników używa PPE na co dzień regularnie (~59-60%).\n\n*Źródło: OSHAGear (2024)*"

# json.dumps ensures proper escaping of newlines and quotes (produces \n as literal chars)
# E.g. "Line 1\nLine 2" -> becomes string "Line 1\\nLine 2"
branza_json = json.dumps(branza_text, ensure_ascii=False) 
ryzyko_json = json.dumps(ryzyko_text, ensure_ascii=False)

extra_json = f', "infoBoxes": [ {{ "title": "Branża budowlana", "icon": "🏗️", "content": {branza_json} }}, {{ "title": "Ryzyko urazu bez PPE", "icon": "⚠️", "type": "warning", "content": {ryzyko_json} }} ], "table": {{ "title": "Typowe zdarzenia i ich skutki", "headers": ["Zdarzenie z terenu", "Skutek", "Co zrobiono źle"], "rows": [ ["Operator szlifierki bez oceny strefy", "Odprysk trafił pomocnika", "Brak oceny ryzyka + oznakowania strefy"], ["Brak ochrony słuchu", "Uraz słuchu po kilku dniach", "PPE nie dopasowane do hałasu"], ["Tarcza niezgodna z materiałem", "Pęknięcie tarczy", "Niewłaściwy osprzęt"], ["Złe ułożenie ciała", "Przecięcie dłoni", "Brak ergonomii pozycji pracy"], ["Zapchany filtr maski", "Podrażnienie układu oddechowego", "Brak kontroli stanu PPE"] ] }}'

# CRITICAL FIX: re.sub processes backslashes in the replacement string. 
# So \\n becomes \n (newline). We need to double escape backslashes so they survive re.sub.
# This ensures that \\n in json.dumps output remains \\n in the final file.
extra_json_safe = extra_json.replace('\\', '\\\\')

pattern_inject = r'("id":\s*"data-2".*?"stats":\s*\[[^\]]+\])(,\s*"callout")'
content = re.sub(pattern_inject, r'\1' + extra_json_safe + r'\2', content, flags=re.DOTALL)

# 7. Apply Dollar Quoting ($$)
content = content.replace("content = '{", "content = $$ {")
content = content.replace("}'::jsonb", "}$$::jsonb")
if "$$" not in content:
    content = re.sub(r"content\s*=\s*'{", "content = $$ {", content)
    content = re.sub(r"}'::jsonb", "}$$::jsonb", content)

print(f"Writing {dst}...")
with open(dst, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. v11 created with safe re.sub escaping.")
