import json
import re

# Wczytaj JSON
with open('data/lessons/MILWAUKEE_JSS_Rules_of_Engagement_V2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def fix_html_quotes(text):
    """Zamienia apostrofy na cudzysłowy w atrybutach HTML"""
    # Zamiana class='...' na class="..."
    text = re.sub(r"class='([^']*?)'", r'class="\1"', text)
    # Zamiana style='...' na style="..."
    text = re.sub(r"style='([^']*?)'", r'style="\1"', text)
    return text

# Napraw wprowadzenie
if 'glowny' in data['wprowadzenie']:
    data['wprowadzenie']['glowny'] = fix_html_quotes(data['wprowadzenie']['glowny'])

# Napraw nauka sekcje
for sekcja in data['nauka']['tekst']['sekcje']:
    sekcja['tresc'] = fix_html_quotes(sekcja['tresc'])

# Napraw podsumowanie
if 'glowny' in data['podsumowanie']:
    data['podsumowanie']['glowny'] = fix_html_quotes(data['podsumowanie']['glowny'])

# Zapisz naprawiony JSON
with open('data/lessons/MILWAUKEE_JSS_Rules_of_Engagement_V2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Zamieniono apostrofy na cudzysłowy w atrybutach HTML")
print("   - class='...' → class=\"...\"")
print("   - style='...' → style=\"...\"")
