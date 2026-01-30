#!/usr/bin/env python3
"""
Skrypt migracji lekcji Conversational Intelligence z v1.0 do v2.0
"""

import json
import sys
from pathlib import Path

def migrate_lesson_to_v2(old_file_path, new_file_path):
    """Migruje lekcję ze starej struktury v1.0 do nowej v2.0"""
    
    print(f"📖 Wczytywanie starego pliku: {old_file_path}")
    with open(old_file_path, 'r', encoding='utf-8') as f:
        old_lesson = json.load(f)
    
    print("🔄 Rozpoczynam migrację...")
    
    # Nowa struktura v2.0
    new_lesson = {
        "_template_info": {
            "version": "2.0",
            "description": "Lekcja v2.0 - Conversational Intelligence",
            "last_updated": "2025-12-24",
            "migration_notes": "Zmigrowane ze struktury v1.0 do v2.0 przez skrypt"
        },
        
        # Metadane podstawowe
        "id": old_lesson.get("id"),
        "title": old_lesson.get("title"),
        "description": old_lesson.get("description", "").replace("OOOdkryj", "Odkryj"),  # Fix literówki
        "tag": old_lesson.get("tag"),
        "xp_reward": old_lesson.get("xp_reward"),
        "difficulty": old_lesson.get("difficulty"),
        "available": old_lesson.get("available", True),
        "estimated_time": "90 min",
        "learning_objectives": [
            "Zrozumiesz, jak rozmowy wpływają na neurochemię mózgu (oksytocyna vs kortyzol)",
            "Nauczysz się rozpoznawać 3 poziomy rozmów i świadomie przechodzić na Poziom III",
            "Opanujesz praktyczne narzędzia C-IQ: TRUST, Trzy R, Leadershift",
            "Dowiesz się, jak budować kulturę zaufania przez codzienne rytuały konwersacyjne"
        ],
        "prerequisites": [],
        "tags": ["neuroprzywództwo", "komunikacja", "zaufanie", "C-IQ", "Judith Glaser"]
    }
    
    # ===== WPROWADZENIE =====
    print("  ✓ Migracja: intro → wprowadzenie")
    intro = old_lesson.get("intro", {})
    
    new_lesson["wprowadzenie"] = {
        "glowny": intro.get("main", ""),
        "case_study": {
            "title": "Opening Case Study – Rozmowa, która zmieniła kierunek projektu",
            "description": "Historia Marty i jej zespołu marketingowego pokazuje, jak jedna rozmowa może albo zbudować, albo zniszczyć zaufanie w zespole.",
            "content": intro.get("case_study", ""),
            "questions": [
                {
                    "id": "q1",
                    "question": "Co, Twoim zdaniem, wydarzyło się w tej rozmowie na poziomie emocji i zaufania?",
                    "placeholder": "Pomyśl o reakcjach zespołu, języku ciała, emocjach..."
                },
                {
                    "id": "q2",
                    "question": "Jakie reakcje chemiczne mogły zajść w mózgach uczestników tej rozmowy?",
                    "placeholder": "Kortyzol, oksytocyna, porwanie amygdali..."
                },
                {
                    "id": "q3",
                    "question": "Jak można by poprowadzić tę rozmowę inaczej, by otworzyć zespół na współpracę?",
                    "placeholder": "Jakie pytania, jaki ton, jakie podejście..."
                }
            ]
        },
        "quiz_samodiagnozy": intro.get("quiz_samodiagnozy", {})
    }
    
    # ===== NAUKA =====
    print("  ✓ Migracja: sections.learning → nauka")
    sections = old_lesson.get("sections", {})
    learning = sections.get("learning", {})
    tabs = learning.get("tabs", [])
    
    new_lesson["nauka"] = {}
    
    # Znajdź zakładki
    for tab in tabs:
        tab_id = tab.get("id", "")
        
        if tab_id == "tekst":
            # Tekst - sekcje
            new_lesson["nauka"]["tekst"] = {
                "sekcje": []
            }
            for section in tab.get("sections", []):
                new_lesson["nauka"]["tekst"]["sekcje"].append({
                    "title": section.get("title", ""),
                    "content": section.get("content", "")
                })
        
        elif tab_id == "podcast":
            # Podcast
            podcast_section = tab.get("sections", [{}])[0]
            new_lesson["nauka"]["podcast"] = {
                "title": podcast_section.get("title", "🎧 Podcast"),
                "description": "Słuchaj kluczowych koncepcji C-IQ w formie audio",
                "url": "https://www.youtube.com/watch?v=696MjcaTCns",
                "duration": "25 min",
                "content": podcast_section.get("content", "")
            }
        
        elif tab_id == "video":
            # Video
            video_section = tab.get("sections", [{}])[0]
            new_lesson["nauka"]["video"] = {
                "title": video_section.get("title", "🎬 Video"),
                "description": "Obejrzyj dynamiczną prezentację koncepcji C-IQ",
                "url": "https://youtu.be/zWBujW9o2Hc",
                "duration": "10 min",
                "content": video_section.get("content", "")
            }
    
    # ===== PRAKTYKA =====
    print("  ✓ Migracja: sections → praktyka")
    new_lesson["praktyka"] = {}
    
    # Practical exercises (jeśli istnieją)
    practical = sections.get("practical_exercises", {})
    if practical:
        new_lesson["praktyka"]["cwiczenia"] = practical.get("exercises", [])
    
    # Final quiz
    final_quiz = sections.get("final_quiz", {})
    if final_quiz:
        new_lesson["praktyka"]["quiz_koncowy"] = {
            "title": final_quiz.get("title", "📝 Quiz Końcowy"),
            "description": final_quiz.get("description", "Sprawdź swoją wiedzę o C-IQ"),
            "passing_score": final_quiz.get("passing_score", 70),
            "pytania": final_quiz.get("questions", [])
        }
    
    # ===== PODSUMOWANIE =====
    print("  ✓ Migracja: summary → podsumowanie")
    summary = old_lesson.get("summary", {})
    
    new_lesson["podsumowanie"] = {
        "glowny": summary.get("main", ""),
        "case_study": {
            "title": "Closing Case Study - Co dalej?",
            "description": "Rezultaty wdrożenia C-IQ",
            "resolution": summary.get("case_study", "")
        },
        "mapa_mysli": summary.get("mind_map", {}),
        "key_points": summary.get("key_points", []),
        "next_steps": summary.get("next_steps", [])
    }
    
    # Zapis nowego pliku
    print(f"💾 Zapisywanie nowego pliku: {new_file_path}")
    with open(new_file_path, 'w', encoding='utf-8') as f:
        json.dump(new_lesson, f, ensure_ascii=False, indent=2)
    
    print("✅ Migracja zakończona pomyślnie!")
    print(f"📊 Statystyki:")
    print(f"   - Sekcje tekstowe: {len(new_lesson.get('nauka', {}).get('tekst', {}).get('sekcje', []))}")
    print(f"   - Podcast: {'✓' if 'podcast' in new_lesson.get('nauka', {}) else '✗'}")
    print(f"   - Video: {'✓' if 'video' in new_lesson.get('nauka', {}) else '✗'}")
    print(f"   - Quiz końcowy: {'✓' if 'quiz_koncowy' in new_lesson.get('praktyka', {}) else '✗'}")
    print(f"   - Mind map: {'✓' if 'mapa_mysli' in new_lesson.get('podsumowanie', {}) else '✗'}")


if __name__ == "__main__":
    # Ścieżki plików
    old_file = Path(r"c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json")
    new_file = Path(r"c:\Users\pksia\Dropbox\BVA\data\lessons\11_Conversational_Intelligence_V2_FULL.json")
    
    if not old_file.exists():
        print(f"❌ Błąd: Nie znaleziono pliku {old_file}")
        sys.exit(1)
    
    migrate_lesson_to_v2(old_file, new_file)
    
    print("\n🎉 Gotowe! Możesz teraz:")
    print(f"   1. Sprawdzić nowy plik: {new_file}")
    print(f"   2. Porównać ze starym: {old_file}")
    print(f"   3. Po weryfikacji zamienić stary plik na nowy")
