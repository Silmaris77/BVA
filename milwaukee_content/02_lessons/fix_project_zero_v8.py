import re

src = r"c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FULL.sql"
dst = r"c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FINAL.sql"

print(f"Reading {src}...")
with open(src, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Heading -> Title
content = content.replace('"heading":', '"title":')

# 2. Polish quotes -> simple quotes
content = content.replace('„', "'")
content = content.replace('”', "'")
content = content.replace('“', "'")

# 3. Fix unescaped quotes at end of sentences
content = content.replace('".', "'.")

# 4. Remove any backslashes before single quotes
content = content.replace("\\'", "'")

# 5. Fix remember structure
pattern = r'"remember":\s*\{\s*"icon":\s*"[^"]+",\s*"text":\s*"([^"]+)"\s*\}'
def fix_remember(match):
    text = match.group(1)
    return f'"remember": {{ "title": "Zapamiętaj", "items": ["{text}"] }}'
content = re.sub(pattern, fix_remember, content)


# 6. INJECT MISSING DATA FOR data-2 CARD
# FORCE ONE LINE CONTENT
# We use replace to strip any accidental newlines from the code definition
branza_content = "**22,5%** wszystkich wypadków śmiertelnych i **12,9%** pozostałych wypadków w UE to budownictwo.\\n\\nW Polsce historycznie: **13 wypadków dziennie** na budowach, z jedną osobą tracącą życie co tydzień.\\n\\n*Źródła: Eurostat (2023), Państwowa Inspekcja Pracy (2016-2020)*".replace('\n', '').replace('\r', '')

ryzyko_content = "Pracownicy bez PPE są **3 razy częściej** narażeni na urazy niż ci, którzy używają PPE prawidłowo.\\n\\nStatystyki pokazują, że około **59,4%** pracowników używa PPE na co dzień regularnie (~59-60%).\\n\\n*Źródło: OSHAGear (2024)*".replace('\n', '').replace('\r', '')

# Construct JSON manually to be sure about formatting
# We add enters for readability of the SQL file, but NOT inside values
extra_json = f''',
                "infoBoxes": [
                    {{
                        "title": "Branża budowlana",
                        "icon": "🏗️",
                        "content": "{branza_content}"
                    }},
                    {{
                        "title": "Ryzyko urazu bez PPE",
                        "icon": "⚠️",
                        "type": "warning",
                        "content": "{ryzyko_content}"
                    }}
                ],
                "table": {{
                    "title": "Typowe zdarzenia i ich skutki",
                    "headers": ["Zdarzenie z terenu", "Skutek", "Co zrobiono źle"],
                    "rows": [
                        ["Operator szlifierki bez oceny strefy", "Odprysk trafił pomocnika", "Brak oceny ryzyka + oznakowania strefy"],
                        ["Brak ochrony słuchu", "Uraz słuchu po kilku dniach", "PPE nie dopasowane do hałasu"],
                        ["Tarcza niezgodna z materiałem", "Pęknięcie tarczy", "Niewłaściwy osprzęt"],
                        ["Złe ułożenie ciała", "Przecięcie dłoni", "Brak ergonomii pozycji pracy"],
                        ["Zapchany filtr maski", "Podrażnienie układu oddechowego", "Brak kontroli stanu PPE"]
                    ]
                }}'''

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

print("Done. Injected infoBoxes and table (v8 clean).")
