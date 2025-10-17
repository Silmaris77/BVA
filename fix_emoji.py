#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Skrypt do naprawy emoji w plikach"""

import re

def fix_emoji_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Mapowanie placeholderów na emoji - uporządkowane od najdłuższych
    replacements = {
        # Nagłówki i duże sekcje
        '"??? Narzędzia AI"': '"🧠 Narzędzia AI"',
        '"?? Autodiagnoza"': '"🔍 Autodiagnoza"',
        '"?? C-IQ Tools"': '"💬 C-IQ Tools"',
        '"?? Symulatory"': '"🎭 Symulatory"',
        '"?? Kreatywność"': '"💡 Kreatywność"',
        '"?? Analityki"': '"📊 Analityki"',
        '"?? AI Asystent"': '"🤖 AI Asystent"',
        
        # Testy i funkcje
        '"?? Test': '"🎯 Test',
        '"?? Rozp': '"▶️ Rozp',
        '"?? Obl': '"📊 Obl',
        '"?? Kolb': '"🔄 Kolb',
        '"?? Uruch': '"🚀 Uruch',
        '<h4>?? ': '<h4>🎯 ',
        '<h3 style="margin: 0 0 10px 0; font-size: 16px; font-weight: bold;">?? ': '<h3 style="margin: 0 0 10px 0; font-size: 16px; font-weight: bold;">💡 ',
        '<li>?? ': '<li>✅ ',
        '### ?? ': '### 🎯 ',
        '<h4 style=\'margin: 0; color: #2c3e50;\'>?? ': '<h4 style=\'margin: 0; color: #2c3e50;\'>📝 ',
        '<h4 style=\'margin: 30px 0 20px 0; color: #333;\'>?? ': '<h4 style=\'margin: 30px 0 20px 0; color: #333;\'>🔄 ',
        'st.warning("?? ': 'st.warning("⚠️ ',
        'st.info("?? ': 'st.info("💡 ',
        'st.success("?? ': 'st.success("✅ ',
        
        # Emoji w kontenerach/słownikach  
        '<div style=\'font-size: 2.5em; margin-bottom: 15px;\'>??</div>': '<div style=\'font-size: 2.5em; margin-bottom: 15px;\'>🎓</div>',
        '\'optymalne warunki\': \'??\',': '\'optymalne warunki\': \'✨\',',
        '\'warunki\': \'??\',': '\'warunki\': \'🌟\',',
        '\'nauki\': \'??\',': '\'nauki\': \'📚\',',
        '\'mocne strony\': \'??\',': '\'mocne strony\': \'💪\',',
        '\'wzmacniać\': \'??\',': '\'wzmacniać\': \'⬆️\',',
        '\'silne\': \'??\',': '\'silne\': \'🔥\',',
        '\'obszary do rozwoju\': \'??\',': '\'obszary do rozwoju\': \'🎯\',',
        '\'rozwijać\': \'??\',': '\'rozwijać\': \'🌱\',',
        '\'słabe\': \'??\',': '\'słabe\': \'⚡\',',
        '\'rozwój\': \'??\',': '\'rozwój\': \'📈\',',
        '\'metody\': \'??\',': '\'metody\': \'🛠️\',',
        '\'technik\': \'??\',': '\'technik\': \'⚙️\',',
        '\'narzędzi\': \'???\',': '\'narzędzi\': \'🔧\',',
        '\'strategi\': \'??\',': '\'strategi\': \'🎯\',',
        '\'ćwicz\': \'??\',': '\'ćwicz\': \'💪\',',
        '\'zalec\': \'??\',': '\'zalec\': \'✅\',',
        '\'unikaj\': \'??\',': '\'unikaj\': \'❌\',',
        '\'tips\': \'??\',': '\'tips\': \'💡\',',
        '\'wskazówk\': \'??\',': '\'wskazówk\': \'📌\',',
        '\'zastosow\': \'??\',': '\'zastosow\': \'🎯\',',
        '\'sposób\': \'??\',': '\'sposób\': \'📝\',',
        '\'korzyść\': \'??\',': '\'korzyść\': \'✨\',',
        
        # Icon assignments
        'icon = \'??\'': 'icon = \'🎯\'',
        
        # Emoji w danych Kolba
        '"emoji": "??"': '"emoji": "🎯"',
        '"CE": {"name": "Konkretne Doświadczenie", "emoji": "??",': '"CE": {"name": "Konkretne Doświadczenie", "emoji": "🤚",',
        '"RO": {"name": "Refleksyjna Obserwacja", "emoji": "??",': '"RO": {"name": "Refleksyjna Obserwacja", "emoji": "🤔",',
        '"AC": {"name": "Abstrakcyjna Konceptualizacja", "emoji": "??",': '"AC": {"name": "Abstrakcyjna Konceptualizacja", "emoji": "💭",',
        '"AE": {"name": "Aktywne Eksperymentowanie", "emoji": "??",': '"AE": {"name": "Aktywne Eksperymentowanie", "emoji": "🔬",',
        
        # Szczególne przypadki w opisach
        '"?? 12 pytań': '"❓ 12 pytań',
        '"?? Identyfikacja': '"🔍 Identyfikacja',
        '"?? Analiza': '"📊 Analiza',
        '"?? Spersonalizowane': '"🎯 Spersonalizowane',
        '"?? Zrozumienie': '"💡 Zrozumienie',
        '"?? Kompleksowa': '"📋 Kompleksowa',
        '"?? Wykres': '"📈 Wykres',
        '"?? Dopasowanie': '"🎯 Dopasowanie',
        '"?? Cykl': '"🔄 Cykl',
        '"?? Odpowiedz': '"📝 Odpowiedz',
        '"?? Proszę': '"⚠️ Proszę',
        '"?? W przygotowaniu': '"🚧 W przygotowaniu',
        '"?? 8 scenariuszy': '"🎬 8 scenariuszy',
        '"?? 3 poziomy': '"📊 3 poziomy',
        '"?? AI generuje': '"🤖 AI generuje',
        '"?? Możliwość': '"✨ Możliwość',
        '"?? Scenariusze': '"🎯 Scenariusze',
        '"?? Techniki': '"🛠️ Techniki',
    }
    
    # Zastosuj zamiany
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Zapisz
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Naprawiono emoji w {filepath}")

if __name__ == "__main__":
    fix_emoji_in_file("views/tools.py")
