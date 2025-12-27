"""
Czyszczenie inline styles z MILWAUKEE_JSS_Rules_of_Engagement.json
i zamiana na standardowe klasy CSS z lesson.py
"""

import json
import re

# Ścieżka
LESSON_PATH = 'data/lessons/MILWAUKEE_JSS_Rules_of_Engagement.json'

# Wczytaj lekcję
with open(LESSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded lesson: {data['title']}")

# Funkcja czyszcząca inline styles z div class='...'
def clean_inline_styles(html_content):
    """
    Zamienia:
    <div class='info-box' style='...'>  →  <div class='info-box'>
    <div class='warning-box' style='...'>  →  <div class='warning-box'>
    itp.
    """
    # Lista klas do wyczyszczenia
    box_classes = [
        'info-box', 'warning-box', 'highlight-box', 'tool-box', 
        'success-box', 'error-box', 'key-takeaway'
    ]
    
    for box_class in box_classes:
        # Pattern: <div class='box-class' style='...'> lub <div style='...' class='box-class'>
        # Zamień na: <div class='box-class'>
        pattern1 = rf"<div class='{box_class}' style='[^']*'>"
        pattern2 = rf'<div class="{box_class}" style="[^"]*">'
        pattern3 = rf"<div style='[^']*' class='{box_class}'>"
        pattern4 = rf'<div style="[^"]*" class="{box_class}">'
        
        html_content = re.sub(pattern1, f"<div class='{box_class}'>", html_content)
        html_content = re.sub(pattern2, f'<div class="{box_class}">', html_content)
        html_content = re.sub(pattern3, f"<div class='{box_class}'>", html_content)
        html_content = re.sub(pattern4, f'<div class="{box_class}">', html_content)
    
    return html_content

# Wyczyść inline styles w sekcjach learning
if 'sections' in data and 'learning' in data['sections']:
    sections = data['sections']['learning']['sections']
    print(f"\nCzyszczenie {len(sections)} sekcji learning...")
    
    for i, section in enumerate(sections):
        original_length = len(section['content'])
        section['content'] = clean_inline_styles(section['content'])
        new_length = len(section['content'])
        
        if original_length != new_length:
            print(f"  ✓ Sekcja {i+1}: {section['title'][:50]}... ({original_length} → {new_length} chars)")

# Wyczyść inline styles w intro
if 'intro' in data:
    if 'main' in data['intro']:
        original_length = len(data['intro']['main'])
        data['intro']['main'] = clean_inline_styles(data['intro']['main'])
        new_length = len(data['intro']['main'])
        if original_length != new_length:
            print(f"  ✓ Intro main: ({original_length} → {new_length} chars)")
    
    if 'case_study' in data['intro']:
        original_length = len(data['intro']['case_study'])
        data['intro']['case_study'] = clean_inline_styles(data['intro']['case_study'])
        new_length = len(data['intro']['case_study'])
        if original_length != new_length:
            print(f"  ✓ Intro case_study: ({original_length} → {new_length} chars)")

# Wyczyść inline styles w case_studies
if 'practical_exercises' in data and 'case_studies' in data['practical_exercises']:
    case_studies = data['practical_exercises']['case_studies']
    print(f"\nCzyszczenie {len(case_studies)} case studies...")
    
    for i, case_study in enumerate(case_studies):
        original_length = len(case_study['content'])
        case_study['content'] = clean_inline_styles(case_study['content'])
        new_length = len(case_study['content'])
        
        if original_length != new_length:
            print(f"  ✓ Case study {i+1}: {case_study['title'][:50]}... ({original_length} → {new_length} chars)")

# Wyczyść inline styles w summary
if 'summary' in data and 'main' in data['summary']:
    original_length = len(data['summary']['main'])
    data['summary']['main'] = clean_inline_styles(data['summary']['main'])
    new_length = len(data['summary']['main'])
    if original_length != new_length:
        print(f"  ✓ Summary: ({original_length} → {new_length} chars)")

# Zapisz wyczyszczoną wersję
with open(LESSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Zapisano wyczyszczoną lekcję: {LESSON_PATH}")
print("Inline styles usunięte - używamy teraz standardowych klas CSS")
