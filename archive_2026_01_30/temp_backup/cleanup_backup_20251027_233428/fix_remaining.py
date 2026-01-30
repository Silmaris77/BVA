# -*- coding: utf-8 -*-
"""Zamieniaj wszystkie pozostałe ??"""

with open('views/tools.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Zamień wszystkie pozostałe ?? na emoji
content = content.replace("'??'", "'🎯'")
content = content.replace('"??"', '"🎯"')
content = content.replace(' ?? ', ' 🎯 ')
content = content.replace('>??<', '>🎯<')
content = content.replace('???', '🔧')

with open('views/tools.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Zamieniono wszystkie pozostałe ??')
