# -*- coding: utf-8 -*-
"""Napraw wszystkie pozostałe emoji w tools.py"""

with open('views/tools.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Mapowanie placeholderów na emoji
replacements = {
    # Przyciski i akcje
    '"?? Użyj przykładu"': '"✨ Użyj przykładu"',
    '"?? Skanuj poziom C-IQ"': '"🔍 Skanuj poziom C-IQ"',
    '"?? Scanner analizuje': '"🔍 Scanner analizuje',
    '"?? Wygeneruj raport PDF"': '"📄 Wygeneruj raport PDF"',
    '"?? Pobierz raport HTML"': '"📥 Pobierz raport HTML"',
    '"🔧?? Trener"': '"👨‍🏫 Trener"',
    '"?? Menedżer"': '"👔 Menedżer"',
    '"?? Sprzedawca"': '"💼 Sprzedawca"',
    
    # Metryki i wskaźniki
    '"?? Wykryty poziom"': '"📊 Wykryty poziom"',
    '"?? Pewność analizy"': '"🎯 Pewność analizy"',
    '"?? Budowanie zaufania"': '"🤝 Budowanie zaufania"',
    '<strong>?? WYKRYTO</strong>': '<strong>✅ WYKRYTO</strong>',
    
    # Komunikaty i ostrzeżenia
    'f"**?? Twoja najsilniejsza': 'f"**💪 Twoja najsilniejsza',
    'f"**?? Obszar do rozwoju:': 'f"**🎯 Obszar do rozwoju:',
    'f"?? **Gratulacje!**': 'f"🎉 **Gratulacje!**',
    'f"?? **Silna preferencja**': 'f"⚡ **Silna preferencja**',
    'interpretation = f"?? ': 'interpretation = f"📊 ',
    '"?? **Jak zapisać jako PDF:**': '"💡 **Jak zapisać jako PDF:**',
    
    # Nagłówki HTML
    '<h3>?? Twoja pozycja na siatce</h3>': '<h3>📍 Twoja pozycja na siatce</h3>',
    '<h3>?? Interpretacja wymiarów:</h3>': '<h3>📊 Interpretacja wymiarów:</h3>',
    '<h3>?? Obszary do rozwinięcia:</h3>': '<h3>🎯 Obszary do rozwinięcia:</h3>',
    '<strong>?? Zawód:</strong>': '<strong>👔 Zawód:</strong>',
    '<strong>?? Pamiętaj:</strong>': '<strong>💡 Pamiętaj:</strong>',
    '<h4 style=\'margin: 0; color: white;\'>?? Zawód:': '<h4 style=\'margin: 0; color: white;\'>👔 Zawód:',
    '<p style=\'margin: 0 0 10px 0; font-weight: bold;\'>?? Zalecenia rozwojowe:</p>': '<p style=\'margin: 0 0 10px 0; font-weight: bold;\'>💡 Zalecenia rozwojowe:</p>',
    '<b>?? Kluczowa wskazówka:</b>': '<b>💡 Kluczowa wskazówka:</b>',
    
    # Listy i punktory
    'f"?? {w}"': 'f"• {w}"',
    
    # Expandery i sekcje
    '"?? Debug: Zobacz surowy tekst AI"': '"🔧 Debug: Zobacz surowy tekst AI"',
    
    # Inne przypadki
    'else "?? Silne preferencje': 'else "⚡ Silne preferencje',
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open('views/tools.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Naprawiono wszystkie emoji w tools.py')
