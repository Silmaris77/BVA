# -*- coding: utf-8 -*-
"""Napraw pozostałe emoji w lesson.py"""

with open('views/lesson.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Dodatkowe zamiany
replacements = {
    # Mapa myśli
    '"??? Mapa myśli"': '"🗺️ Mapa myśli"',
    '### ??? Interaktywna mapa myśli': '### 🗺️ Interaktywna mapa myśli',
    '"??? Eksportuj Obraz"': '"📸 Eksportuj Obraz"',
    
    # Komunikaty o ukończeniu
    '<h2 style="margin: 0 0 10px 0;">?? Lekcja ukończona!</h2>': '<h2 style="margin: 0 0 10px 0;">🎉 Lekcja ukończona!</h2>',
    '<h3 style="margin: 0 0 10px 0;">?? {lesson': '<h3 style="margin: 0 0 10px 0;">📚 {lesson',
    '<span>?? {current_xp}/{max_xp} XP</span>': '<span>⭐ {current_xp}/{max_xp} XP</span>',
    
    # Wyniki i wykresy
    '<h3>?? Twój wynik:': '<h3>📊 Twój wynik:',
    '## ?? Twoje spersonalizowane wyniki': '## 📊 Twoje spersonalizowane wyniki',
    '<h3 style=\'color: #2196F3; margin: 0;\'>?? Łączna suma punktów</h3>': '<h3 style=\'color: #2196F3; margin: 0;\'>📊 Łączna suma punktów</h3>',
    
    # Komunikaty rozwoju
    '?? **Kompleksowy rozwój:**': '🎯 **Kompleksowy rozwój:**',
    '?? **Selektywny rozwój:**': '🎯 **Selektywny rozwój:**',
    
    # Ikony poziomów
    '"Bardzo wysoka": "??",': '"Bardzo wysoka": "🔥",',
    '"Średnia": "??",': '"Średnia": "⚡",',
    '"Niska": "??"': '"Niska": "💡"',
    'relevance_icons.get(matching_level[\'name\'], "??")': 'relevance_icons.get(matching_level[\'name\'], "📌")',
    'relevance_icon = "??"': 'relevance_icon = "📌"',
    'status_icon = "??"': 'status_icon = "✅"',
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open('views/lesson.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Naprawiono pozostałe emoji w lesson.py')
