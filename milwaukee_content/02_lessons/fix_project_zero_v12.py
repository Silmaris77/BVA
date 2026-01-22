import re
import os
import json

src = r"c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FULL.sql"
dst = r"c:\Users\pksia\Dropbox\BVA\milwaukee_content\02_lessons\seed_project_zero_FINAL.sql"

if os.path.exists(dst):
    # We will overwrite it anyway, but good to know.
    pass

print(f"Reading {src}...")
with open(src, 'r', encoding='utf-8') as f:
    content = f.read()

# --- v11 STEPS ---

# 1. Heading -> Title
content = content.replace('"heading":', '"title":')

# 2. Polish quotes
content = content.replace('„', "'").replace('”', "'").replace('“', "'")

# 3. Fix unescaped quotes at end of sentences
content = content.replace('".', "'.")

# 4. Remove any backslashes before single quotes
content = content.replace("\\'", "'")

# 5. Fix remember structure
pattern = r'"remember":\s*\{\s*"icon":\s*"[^"]+",\s*"text":\s*"([^"]+)"\s*\}'
content = re.sub(pattern, lambda m: f'"remember": {{ "title": "Zapamiętaj", "items": ["{m.group(1)}"] }}', content)

# 6. INJECT MISSING DATA (Data-2 Card)
branza_text = "**22,5%** wszystkich wypadków śmiertelnych i **12,9%** pozostałych wypadków w UE to budownictwo.\n\nW Polsce historycznie: **13 wypadków dziennie** na budowach, z jedną osobą tracącą życie co tydzień.\n\n*Źródła: Eurostat (2023), Państwowa Inspekcja Pracy (2016-2020)*"
ryzyko_text = "Pracownicy bez PPE są **3 razy częściej** narażeni na urazy niż ci, którzy używają PPE prawidłowo.\n\nStatystyki pokazują, że około **59,4%** pracowników używa PPE na co dzień regularnie (~59-60%).\n\n*Źródło: OSHAGear (2024)*"

branza_json = json.dumps(branza_text, ensure_ascii=False) 
ryzyko_json = json.dumps(ryzyko_text, ensure_ascii=False)

extra_json = f', "infoBoxes": [ {{ "title": "Branża budowlana", "icon": "🏗️", "content": {branza_json} }}, {{ "title": "Ryzyko urazu bez PPE", "icon": "⚠️", "type": "warning", "content": {ryzyko_json} }} ], "table": {{ "title": "Typowe zdarzenia i ich skutki", "headers": ["Zdarzenie z terenu", "Skutek", "Co zrobiono źle"], "rows": [ ["Operator szlifierki bez oceny strefy", "Odprysk trafił pomocnika", "Brak oceny ryzyka + oznakowania strefy"], ["Brak ochrony słuchu", "Uraz słuchu po kilku dniach", "PPE nie dopasowane do hałasu"], ["Tarcza niezgodna z materiałem", "Pęknięcie tarczy", "Niewłaściwy osprzęt"], ["Złe ułożenie ciała", "Przecięcie dłoni", "Brak ergonomii pozycji pracy"], ["Zapchany filtr maski", "Podrażnienie układu oddechowego", "Brak kontroli stanu PPE"] ] }}'

# Double escape backslashes for re.sub safety
extra_json_safe = extra_json.replace('\\', '\\\\')

pattern_inject = r'("id":\s*"data-2".*?"stats":\s*\[[^\]]+\])(,\s*"callout")'
content = re.sub(pattern_inject, r'\1' + extra_json_safe + r'\2', content, flags=re.DOTALL)

# --- NEW STEP ---
# 8. INJECT ACHIEVEMENT CARD (v12)
# We want to inject it before the closing of the "cards" array.
# The cards array ends with a closing bracket ] and then closing brace } of the content object.
# We will look for the last card (usually ending-1) and append after it.

achievement_card = {
    "id": "achievement-final",
    "type": "achievement",
    "title": "Project Zero - Przygotowanie do Pracy - ZALICZONA!",
    "description": "Gratulacje! Jesteś gotowy do bezpiecznej pracy z Milwaukee Tools",
    "icon": "trophy",
    "stats": [
        { "value": "+100", "label": "XP zdobyte" },
        { "value": "25", "label": "Kart ukończonych" },
        { "value": "30", "label": "Minut nauki" }
    ],
    "badge": "Project Zero Safety Champion"
}

achievement_json = json.dumps(achievement_card, ensure_ascii=False, indent=4)
# Double escape backslashes again if json.dumps produced any (unlikely here but good practice)
achievement_json_safe = achievement_json.replace('\\', '\\\\')

# Looking for the last closing brace of a card object, followed by whitespace and then closing bracket of array
# We need to be careful. The last card in Full SQL is `lightbulb-1`? 
# Wait, seed_project_zero_FULL.sql is the source. It might NOT have ending-1.
# Let's check what's the last card in FULL.sql.
# In previous steps, I saw `lightbulb-1` at the end of FULL.sql.
# Let's assume we append to the end of the `cards` array.

# Regex to find the end of the cards array:  ] (whitespace) } (end of content)
# We replace `\s*]\s*}` with `, <new_card> ] }`

pattern_end_array = r'(\s*]\s*})'
# We need to insert a comma before the last card if we were appending, but we are replacing the end of array.
# Actually, the last card in the array doesn't have a comma after it.
# So we need to: Find the LAST closing brace of an object inside the array. Add comma. Add new object. End array.
# Or simpler: Replace the closing definition of the array.

# Use rsplit to find the last occurrence of ']'
last_bracket_index = content.rfind(']')
if last_bracket_index != -1:
    # Insert before the last bracket
    insertion = ",\n" + achievement_json_safe + "\n"
    content = content[:last_bracket_index] + insertion + content[last_bracket_index:]
else:
    print("WARNING: Could not find closing bracket for cards array!")

# 7. Apply Dollar Quoting ($$) - done LAST to ensure JSON structure is ready
content = content.replace("content = '{", "content = $$ {")
content = content.replace("}'::jsonb", "}$$::jsonb")
if "$$" not in content:
    content = re.sub(r"content\s*=\s*'{", "content = $$ {", content)
    content = re.sub(r"}'::jsonb", "}$$::jsonb", content)

print(f"Writing {dst}...")
with open(dst, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. v12 created with Achievement Card specific injection.")
