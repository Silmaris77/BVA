"""
Skrypt do automatycznej zamiany chaotycznych kolorów na semantyczne klasy
w lekcji Milwaukee Warunki Gwarancji zgodnie ze standardem BVA Educational Styles
"""

import json
import re
from pathlib import Path

# Ścieżka do pliku lekcji
LESSON_FILE = Path(__file__).parent / "data" / "lessons" / "MILWAUKEE_Warunki_Gwarancji.json"
BACKUP_FILE = LESSON_FILE.with_suffix('.json.backup')

# Reguły zamiany (pattern -> replacement)
REPLACEMENTS = [
    # ===== RÓŻOWE/FIOLETOWE GRADIENTY NA HEADER =====
    (
        r"style='background: linear-gradient\(135deg, #f093fb [^']+\); padding: [^']+; border-radius: [^']+; color: white;[^']*'",
        "class='header'"
    ),
    (
        r"style='background: linear-gradient\(135deg, #667eea [^']+\); padding: [^']+; border-radius: [^']+; color: white;[^']*'",
        "class='header'"
    ),
    
    # ===== ZIELONE GRADIENTY NA SUCCESS-BOX =====
    (
        r"style='background: linear-gradient\(135deg, #e8f5e8 [^']+\); padding: [^']+; border-radius: [^']+; margin: [^']*'",
        "class='success-box'"
    ),
    (
        r"style='background: linear-gradient\(135deg, #4caf50 [^']+\); padding: [^']+; border-radius: [^']+;[^']*color: white;[^']*'",
        "class='success-box'"
    ),
    (
        r"style='background: #e8f5e8; padding: [^']+; border-radius: [^']+; margin: [^']+; border-left: 4px solid #4caf50;'",
        "class='success-box'"
    ),
    
    # ===== CZERWONE/RÓŻOWE GRADIENTY NA ERROR-BOX =====
    (
        r"style='background: linear-gradient\(135deg, #ffebee [^']+\); padding: [^']+; border-radius: [^']+[^']*'",
        "class='error-box'"
    ),
    (
        r"style='background: #ffebee; padding: [^']+; border-radius: [^']+; margin: [^']+[^']*'",
        "class='error-box'"
    ),
    
    # ===== NIEBIESKIE GRADIENTY NA INFO-BOX =====
    (
        r"style='background: linear-gradient\(135deg, #e3f2fd [^']+\); padding: [^']+; border-radius: [^']+[^']*'",
        "class='info-box'"
    ),
    (
        r"style='background: #e3f2fd; padding: [^']+; border-radius: [^']+; margin: [^']+[^']*'",
        "class='info-box'"
    ),
    (
        r"style='background: #d1ecf1; padding: [^']+; border-radius: [^']+; border-left: 4px solid #17a2b8;'",
        "class='info-box'"
    ),
    (
        r"style='background: #f8f9fa; padding: [^']+; border-radius: [^']+; margin: [^']+; border-left: 4px solid #f5576c;'",
        "class='info-box'"
    ),
    
    # ===== ŻÓŁTE GRADIENTY/TŁA NA WARNING-BOX =====
    (
        r"style='background: #fff3cd; padding: [^']+; border-radius: [^']+;[^']*'",
        "class='warning-box'"
    ),
    (
        r"style='background: #fff8e1; padding: [^']+; border-radius: [^']+;[^']*'",
        "class='warning-box'"
    ),
    (
        r"style='background: linear-gradient\(135deg, #fff3e0 [^']+\); padding: [^']+; border-radius: [^']+[^']*'",
        "class='warning-box'"
    ),
    (
        r"style='background: linear-gradient\(135deg, #fff8e1 [^']+\); padding: [^']+; border-radius: [^']+[^']*'",
        "class='warning-box'"
    ),
    
    # ===== POMARAŃCZOWE GRADIENTY NA HIGHLIGHT-BOX =====
    (
        r"style='background: linear-gradient\(135deg, #ff9800 [^']+\); padding: [^']+; border-radius: [^']+;[^']*'",
        "class='highlight-box'"
    ),
    (
        r"style='background: #fff3e0; padding: [^']+; border-radius: [^']+; margin: [^']+; border-left: 4px solid #ff9800;'",
        "class='warning-box'"  # Żółty border = warning
    ),
    
    # ===== FIOLETOWE GRADIENTY NA TOOL-BOX (ale nie header!) =====
    (
        r"style='background: linear-gradient\(135deg, #f3e5f5 [^']+\); padding: [^']+; border-radius: [^']+; margin: [^']*'",
        "class='tool-box'"
    ),
    
    # ===== USUWANIE INLINE KOLORÓW Z TEKSTU =====
    (r"style='color: #[0-9a-fA-F]{6};([^']*)'", r"style='\1'"),  # Usuń color ale zostaw resztę
    (r"style='color: #[0-9a-fA-F]{3,6}'", ""),  # Usuń sam color
    (r" style=''", ""),  # Usuń puste style
    
    # ===== NAGŁÓWKI H2/H3 - usuwanie kolorów (powinny dziedziczyć z klasy parent) =====
    (r"<h2 style='color: [^']+;([^']*)'", r"<h2 style='\1'"),
    (r"<h3 style='color: [^']+;([^']*)'", r"<h3 style='\1'"),
    (r"<h4 style='color: [^']+;([^']*)'", r"<h4 style='\1'"),
]

# Specjalne zamiany dla konkretnych sekcji (bardziej precyzyjne)
SPECIFIC_REPLACEMENTS = [
    # Intro - główny header
    (
        r"<div style='background: linear-gradient\(135deg, #f093fb 0%, #f5576c 100%\);[^>]+>",
        "<div class='header'>"
    ),
    
    # Case study w intro
    (
        r"<div style='background: #fff3cd; padding: 25px; border-radius: 12px; border-left: 5px solid #ffc107; margin: 20px 0;'>",
        "<div class='highlight-box'>"
    ),
    
    # Pytania do przemyślenia w case study
    (
        r"<div style='background: #d1ecf1; padding: 20px; border-radius: 8px; border-left: 4px solid #17a2b8;'>",
        "<div class='warning-box'>"
    ),
]

def clean_html_content(html: str) -> str:
    """Czyści HTML z chaotycznych kolorów i zamienia na semantyczne klasy"""
    result = html
    
    # Najpierw specyficzne zamiany (najbardziej precyzyjne)
    for pattern, replacement in SPECIFIC_REPLACEMENTS:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    # Potem ogólne reguły
    for pattern, replacement in REPLACEMENTS:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    return result

def update_lesson_colors():
    """Główna funkcja aktualizująca kolory w lekcji"""
    
    # Backup
    if LESSON_FILE.exists():
        print(f"Tworzę backup: {BACKUP_FILE}")
        BACKUP_FILE.write_text(LESSON_FILE.read_text(encoding='utf-8'), encoding='utf-8')
    
    # Wczytaj JSON
    print(f"Wczytuję lekcję: {LESSON_FILE}")
    with open(LESSON_FILE, 'r', encoding='utf-8') as f:
        lesson_data = json.load(f)
    
    # Przetwórz wszystkie sekcje z HTML
    sections_updated = 0
    
    # Intro
    if 'intro' in lesson_data:
        for key in ['main', 'case_study']:
            if key in lesson_data['intro']:
                old_html = lesson_data['intro'][key]
                new_html = clean_html_content(old_html)
                if old_html != new_html:
                    lesson_data['intro'][key] = new_html
                    sections_updated += 1
                    print(f"  ✅ Zaktualizowano intro.{key}")
    
    # Learning sections
    if 'sections' in lesson_data and 'learning' in lesson_data['sections']:
        tabs = lesson_data['sections']['learning'].get('tabs', [])
        for tab in tabs:
            for section in tab.get('sections', []):
                if 'content' in section:
                    old_html = section['content']
                    new_html = clean_html_content(old_html)
                    if old_html != new_html:
                        section['content'] = new_html
                        sections_updated += 1
                        print(f"  ✅ Zaktualizowano sekcję: {section.get('title', 'bez nazwy')}")
    
    # Practical exercises
    if 'practical_exercises' in lesson_data and 'exercises' in lesson_data['practical_exercises']:
        for section in lesson_data['practical_exercises']['exercises'].get('sections', []):
            if 'content' in section:
                old_html = section['content']
                new_html = clean_html_content(old_html)
                if old_html != new_html:
                    section['content'] = new_html
                    sections_updated += 1
                    print(f"  ✅ Zaktualizowano ćwiczenie: {section.get('title', 'bez nazwy')}")
    
    # Summary
    if 'summary' in lesson_data:
        for key in ['main', 'case_study']:
            if key in lesson_data['summary']:
                old_html = lesson_data['summary'][key]
                new_html = clean_html_content(old_html)
                if old_html != new_html:
                    lesson_data['summary'][key] = new_html
                    sections_updated += 1
                    print(f"  ✅ Zaktualizowano summary.{key}")
    
    # Zapisz zaktualizowany JSON
    print(f"\nZapisz zaktualizowany plik...")
    with open(LESSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(lesson_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 SUKCES! Zaktualizowano {sections_updated} sekcji")
    print(f"📁 Backup: {BACKUP_FILE}")
    print(f"📁 Nowy plik: {LESSON_FILE}")
    print(f"\n✨ Lekcja Milwaukee teraz używa semantycznych kolorów zgodnych ze standardem BVA!")

if __name__ == "__main__":
    update_lesson_colors()
