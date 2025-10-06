"""
Skrypt migracji lekcji 11 do struktury z osadzonymi mediami w tabs
Zamienia linki zewnętrzne na osadzone okienka
"""

import json
import os
from datetime import datetime


def migrate_lesson_11_to_embedded_media():
    """Migruje lekcję 11 do struktury z osadzonymi mediami"""
    
    lesson_path = "data/lessons/11. Od słów do zaufania - Conversational Intelligence.json"
    backup_path = f"data/lessons/backup_lesson_11_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Sprawdź czy plik istnieje
    if not os.path.exists(lesson_path):
        print(f"❌ Plik {lesson_path} nie istnieje")
        return False
    
    # Wczytaj lekcję
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            lesson = json.load(f)
        print(f"✅ Wczytano lekcję: {lesson.get('title', 'Bez tytułu')}")
    except Exception as e:
        print(f"❌ Błąd wczytywania: {e}")
        return False
    
    # Utwórz backup
    try:
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(lesson, f, ensure_ascii=False, indent=2)
        print(f"💾 Utworzono backup: {backup_path}")
    except Exception as e:
        print(f"⚠️ Nie udało się utworzyć backupu: {e}")
    
    # Sprawdź obecną strukturę
    if 'sections' not in lesson:
        print("❌ Brak sekcji 'sections' w lekcji")
        return False
    
    if 'learning' not in lesson['sections']:
        print("❌ Brak sekcji 'learning' w lesson.sections")
        return False
    
    learning = lesson['sections']['learning']
    
    # Sprawdź czy już ma tabs
    if 'tabs' in learning:
        print("⚠️ Lekcja już ma strukturę tabs")
        return True
    
    # Pobierz istniejące sections
    existing_sections = learning.get('sections', [])
    print(f"📋 Znaleziono {len(existing_sections)} istniejących sekcji")
    
    # Utwórz nową strukturę tabs z osadzonymi mediami
    new_tabs_structure = [
        {
            "name": "📚 Tekst",
            "sections": existing_sections  # Zachowaj wszystkie istniejące sekcje tekstowe
        },
        {
            "name": "🎧 Podcast", 
            "sections": [
                {
                    "title": "Podcast - Wprowadzenie do Conversational Intelligence",
                    "content": "EMBED_YOUTUBE:1eram4uEQ58",
                    "embed_type": "youtube",
                    "embed_id": "1eram4uEQ58",
                    "start_time": 0,
                    "description": "Podsumowanie kluczowych koncepcji z książki Judith Glaser w formacie audio. Poznaj fundamentalne założenia Conversational Intelligence® i dowiedz się, jak jakość rozmów wpływa na sukces w życiu i biznesie.",
                    "duration": "30:00",
                    "topics": [
                        "Neurobiologia rozmów - oksytocyna vs kortyzol",
                        "Trzy poziomy konwersacji",
                        "Model TRUST",
                        "Agility konwersacyjna"
                    ]
                }
            ]
        },
        {
            "name": "🎬 Video",
            "sections": [
                {
                    "title": "Video - Inteligencja konwersacyjna w pigułce", 
                    "content": "EMBED_YOUTUBE:zWBujW9o2Hc",
                    "embed_type": "youtube",
                    "embed_id": "zWBujW9o2Hc",
                    "start_time": 0,
                    "description": "Dynamiczna prezentacja teorii i praktyki C-IQ w 10 minut. Obejrzyj, jak rozmowy kształtują naszą rzeczywistość poprzez neurobiologię zaufania.",
                    "duration": "10:00",
                    "topics": [
                        "Porwanie amygdali",
                        "Ścieżka strachu vs ścieżka zaufania", 
                        "Transformacja zespołu",
                        "Plan wdrożenia C-IQ"
                    ]
                }
            ]
        }
    ]
    
    # Zastąp strukturę learning
    lesson['sections']['learning'] = {
        "tabs": new_tabs_structure
    }
    
    # Usuń stare sections jeśli były
    # (już przeniesione do tabs["📚 Tekst"])
    
    # Zaktualizuj metadane
    lesson['_template_info']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    lesson['_template_info']['version'] = "2.0 - embedded media"
    
    # Dodaj informację o mediach
    if 'media_info' not in lesson:
        lesson['media_info'] = {
            "has_embedded_media": True,
            "podcast_platform": "YouTube Music",
            "video_platform": "YouTube",
            "total_media_duration": "40:00",
            "media_types": ["audio", "video"]
        }
    
    # Zapisz zmigrowaną lekcję
    try:
        with open(lesson_path, 'w', encoding='utf-8') as f:
            json.dump(lesson, f, ensure_ascii=False, indent=2)
        print(f"✅ Zapisano zmigrowaną lekcję z osadzonymi mediami")
        print(f"📁 Struktura tabs: {[tab['name'] for tab in new_tabs_structure]}")
        return True
    except Exception as e:
        print(f"❌ Błąd zapisu: {e}")
        return False


def validate_embedded_media_structure(lesson_path):
    """Waliduje strukturę lekcji po migracji do osadzonych mediów"""
    
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            lesson = json.load(f)
    except Exception as e:
        print(f"❌ Błąd walidacji: {e}")
        return False
    
    errors = []
    warnings = []
    
    # Sprawdź podstawową strukturę
    if 'sections' not in lesson:
        errors.append("Brak sekcji 'sections'")
        return False
    
    if 'learning' not in lesson['sections']:
        errors.append("Brak sekcji 'learning'")
        return False
    
    learning = lesson['sections']['learning']
    
    if 'tabs' not in learning:
        errors.append("Brak struktury 'tabs' w learning")
        return False
    
    tabs = learning['tabs']
    
    if not isinstance(tabs, list):
        errors.append("'tabs' musi być listą")
        return False
    
    # Sprawdź każdy tab
    expected_tabs = ["📚 Tekst", "🎧 Podcast", "🎬 Video"]
    found_tabs = [tab.get('name', '') for tab in tabs]
    
    for expected_tab in expected_tabs:
        if expected_tab not in found_tabs:
            warnings.append(f"Brak oczekiwanego tab: {expected_tab}")
    
    # Sprawdź media embeds
    media_tabs_found = 0
    for tab in tabs:
        tab_name = tab.get('name', '')
        if tab_name in ["🎧 Podcast", "🎬 Video"]:
            sections = tab.get('sections', [])
            for section in sections:
                content = section.get('content', '')
                embed_type = section.get('embed_type', '')
                
                if content.startswith('EMBED_') or embed_type:
                    media_tabs_found += 1
                    print(f"✅ Znaleziono osadzone media w tab '{tab_name}'")
                    if embed_type == 'youtube':
                        embed_id = section.get('embed_id', '')
                        if embed_id:
                            print(f"   🎬 YouTube ID: {embed_id}")
                        else:
                            warnings.append(f"Brak embed_id w sekcji YouTube")
    
    if media_tabs_found == 0:
        warnings.append("Nie znaleziono żadnych osadzonych mediów")
    
    # Sprawdź metadata
    if 'media_info' in lesson:
        media_info = lesson['media_info']
        if media_info.get('has_embedded_media'):
            print("✅ Metadata mediów poprawne")
        else:
            warnings.append("Metadata nie wskazuje na osadzone media")
    else:
        warnings.append("Brak metadanych mediów")
    
    # Podsumowanie walidacji
    if errors:
        print("❌ Błędy walidacji:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    if warnings:
        print("⚠️ Ostrzeżenia:")
        for warning in warnings:
            print(f"   - {warning}")
    
    print("✅ Walidacja struktury osadzonych mediów zakończona pomyślnie")
    return True


def main():
    """Główna funkcja migracji"""
    print("🚀 Rozpoczynam migrację lekcji 11 do struktury z osadzonymi mediami...")
    print("=" * 70)
    
    # Wykonaj migrację
    success = migrate_lesson_11_to_embedded_media()
    
    if success:
        print("\n" + "=" * 70)
        print("🔍 Walidacja struktury po migracji...")
        
        # Waliduj rezultat
        lesson_path = "data/lessons/11. Od słów do zaufania - Conversational Intelligence.json"
        validate_embedded_media_structure(lesson_path)
        
        print("\n" + "=" * 70)
        print("🎉 Migracja do osadzonych mediów zakończona!")
        print("\n📋 Następne kroki:")
        print("1. Zaktualizuj views/lesson.py aby używać utils/media_embed.py")
        print("2. Przetestuj renderowanie tabs z osadzonymi mediami") 
        print("3. Sprawdź działanie na urządzeniach mobilnych")
        print("4. Rozszerz na inne lekcje")
        
    else:
        print("\n❌ Migracja nie powiodła się")
        print("Sprawdź logi błędów powyżej")


if __name__ == "__main__":
    main()