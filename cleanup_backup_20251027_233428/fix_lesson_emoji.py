# -*- coding: utf-8 -*-
"""Napraw emoji w lesson.py"""

with open('views/lesson.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Mapowanie placeholderów na emoji dla lesson.py
replacements = {
    # Zakładki i sekcje
    '"?? Lekcje dostępne"': '"📚 Lekcje dostępne"',
    '"?? Lekcje niedostępne"': '"🔒 Lekcje niedostępne"',
    '"?? Quiz Samodiagnozy"': '"🔍 Quiz Samodiagnozy"',
    
    # Przyciski i akcje
    '"?? Wróć do listy lekcji"': '"⬅️ Wróć do listy lekcji"',
    '"?? Przystąp ponownie"': '"🔄 Przystąp ponownie"',
    
    # Nawigacja i kroki
    '<div class="lesson-nav-title">?? Nawigacja lekcji</div>': '<div class="lesson-nav-title">🗺️ Nawigacja lekcji</div>',
    'f"?? {step_number}. {step_name}"': 'f"✅ {step_number}. {step_name}"',
    'f"?? {step_number}. {step_name}"': 'f"🔄 {step_number}. {step_name}"',
    
    # Komunikaty
    'st.error("?? ': 'st.error("🚫 ',
    'st.info("?? ': 'st.info("💡 ',
    'st.warning("?? ': 'st.warning("⚠️ ',
    'st.success("?? ': 'st.success("✅ ',
    
    # Sekcje lekcji
    '### ?? Materiał do nauki': '### 📖 Materiał do nauki',
    '### ?? Materiały wideo': '### 🎥 Materiały wideo',
    '#### ?? Opis sytuacji': '#### 📋 Opis sytuacji',
    '### ?? ': '### 📌 ',
    '#### ?? ': '#### 📍 ',
    
    # Tytuły
    'title=f"?? {lesson': 'title=f"📚 {lesson',
    
    # Inne
    '"?? ': '"📌 ',
    "'?? ": "'📌 ",
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open('views/lesson.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Naprawiono emoji w lesson.py')
