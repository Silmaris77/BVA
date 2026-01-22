import re

src = r"c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FULL.sql"
dst = r"c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FINAL.sql"

print(f"Reading {src}...")
with open(src, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Heading -> Title
content = content.replace('"heading":', '"title":')

# 2. Polish quotes -> ingle quotes
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
# We find the data-2 card block and inject infoBoxes and table before callout.
# The card ends with "callout": { ... } inside data-2.
# We look for "id": "data-2" ... "stats": [ ... ], "callout":
# Actually, simplest is to replace the whole data-2 card content? No, regex injection is safer.
# We'll inject before "callout": {
# But there are multiple callouts. We need the one inside data-2.
# "id": "data-2" -> find matching Callout.

# Defining the extra content
extra_json = """,
                "infoBoxes": [
                    {
                        "icon": "🏗️",
                        "title": "Branża budowlana",
                        "content": "**22,5%** wszystkich wypadków śmiertelnych i **12,9%** pozostałych wypadków w UE to budownictwo.\\n\\nW Polsce historycznie: **13 wypadków dziennie** na budowach, z jedną osobą tracącą życie co tydzień.\\n\\n*Źródła: Eurostat (2023), Państwowa Inspekcja Pracy (2016-2020)*"
                    },
                    {
                        "icon": "⚠️",
                        "title": "Ryzyko urazu bez PPE",
                        "content": "Pracownicy bez PPE są **3 razy częściej** narażeni na urazy niż ci, którzy używają PPE prawidłowo.\\n\\nStatystyki pokazują, że około **59,4%** pracowników używa PPE na co dzień regularnie (~59-60%).\\n\\n*Źródło: OSHAGear (2024)*",
                        "type": "warning"
                    }
                ],
                "table": {
                    "title": "Typowe zdarzenia i ich skutki",
                    "headers": ["Zdarzenie z terenu", "Skutek", "Co zrobiono źle"],
                    "rows": [
                        ["Operator szlifierki bez oceny strefy", "Odprysk trafił pomocnika", "Brak oceny ryzyka + oznakowania strefy"],
                        ["Brak ochrony słuchu", "Uraz słuchu po kilku dniach", "PPE nie dopasowane do hałasu"],
                        ["Tarcza niezgodna z materiałem", "Pęknięcie tarczy", "Niewłaściwy osprzęt"],
                        ["Złe ułożenie ciała", "Przecięcie dłoni", "Brak ergonomii pozycji pracy"],
                        ["Zapchany filtr maski", "Podrażnienie układu oddechowego", "Brak kontroli stanu PPE"]
                    ]
                }"""

# Strategy: Find "id": "data-2" block, then find the "callout" inside it, and prepend extra_md.
# The structure is:
# {
#    "id": "data-2",
#    ...
#    "stats": [...],
#    "callout": ...
# }
# We will match: ("id": "data-2".*?"stats": \[.*?\])(,\s*"callout")
# We use DOTALL.
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

print("Done. Injected infoBoxes and table into data-2.")
