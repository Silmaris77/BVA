import re
import os

src = r"c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FULL.sql"
dst = r"c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FINAL.sql"

if os.path.exists(dst):
    os.remove(dst)
    print(f"Removed old {dst}")

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

# 6. INJECT MISSING DATA (Strict Single Line Construction)
# Construct strings by parts to avoid ANY newlines from source code editor
branza_c  = "**22,5%** wszystkich wypadków śmiertelnych i **12,9%** pozostałych wypadków w UE to budownictwo."
branza_c += "\\n\\nW Polsce historycznie: **13 wypadków dziennie** na budowach, z jedną osobą tracącą życie co tydzień."
branza_c += "\\n\\n*Źródła: Eurostat (2023), Państwowa Inspekcja Pracy (2016-2020)*"

ryzyko_c  = "Pracownicy bez PPE są **3 razy częściej** narażeni na urazy niż ci, którzy używają PPE prawidłowo."
ryzyko_c += "\\n\\nStatystyki pokazują, że około **59,4%** pracowników używa PPE na co dzień regularnie (~59-60%)."
ryzyko_c += "\\n\\n*Źródło: OSHAGear (2024)*"

# Build JSON block. Use explicit \n for formatting between fields, but NOT in values.
extra_json =  ',\n'
extra_json += '                "infoBoxes": [\n'
extra_json += '                    {\n'
extra_json += '                        "title": "Branża budowlana",\n'
extra_json += '                        "icon": "🏗️",\n'
extra_json += f'                        "content": "{branza_c}"\n'
extra_json += '                    },\n'
extra_json += '                    {\n'
extra_json += '                        "title": "Ryzyko urazu bez PPE",\n'
extra_json += '                        "icon": "⚠️",\n'
extra_json += '                        "type": "warning",\n'
extra_json += f'                        "content": "{ryzyko_c}"\n'
extra_json += '                    }\n'
extra_json += '                ],\n'
extra_json += '                "table": {\n'
extra_json += '                    "title": "Typowe zdarzenia i ich skutki",\n'
extra_json += '                    "headers": ["Zdarzenie z terenu", "Skutek", "Co zrobiono źle"],\n'
extra_json += '                    "rows": [\n'
extra_json += '                        ["Operator szlifierki bez oceny strefy", "Odprysk trafił pomocnika", "Brak oceny ryzyka + oznakowania strefy"],\n'
extra_json += '                        ["Brak ochrony słuchu", "Uraz słuchu po kilku dniach", "PPE nie dopasowane do hałasu"],\n'
extra_json += '                        ["Tarcza niezgodna z materiałem", "Pęknięcie tarczy", "Niewłaściwy osprzęt"],\n'
extra_json += '                        ["Złe ułożenie ciała", "Przecięcie dłoni", "Brak ergonomii pozycji pracy"],\n'
extra_json += '                        ["Zapchany filtr maski", "Podrażnienie układu oddechowego", "Brak kontroli stanu PPE"]\n'
extra_json += '                    ]\n'
extra_json += '                }'

pattern_inject = r'("id":\s*"data-2".*?"stats":\s*\[[^\]]+\])(,\s*"callout")'
content = re.sub(pattern_inject, r'\1' + extra_json + r'\2', content, flags=re.DOTALL)

# 7. Apply Dollar Quoting ($$)
content = content.replace("content = '{", "content = $$ {")
content = content.replace("}'::jsonb", "}$$::jsonb")
if "$$" not in content:
    content = re.sub(r"content\s*=\s*'{", "content = $$ {", content)
    content = re.sub(r"}'::jsonb", "}$$::jsonb", content)

print(f"Writing {dst}...")
with open(dst, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. v9 created.")
