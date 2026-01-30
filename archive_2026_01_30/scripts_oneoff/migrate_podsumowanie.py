#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migracja sekcji podsumowanie z v1.0 do v2.0
"""

import json

v1_path = r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json'
v2_path = r'c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence V2.json'

# Wczytaj oba pliki
with open(v1_path, 'r', encoding='utf-8') as f:
    v1 = json.load(f)

with open(v2_path, 'r', encoding='utf-8') as f:
    v2 = json.load(f)

# Pobierz sekcję summary z v1.0
summary = v1.get('summary', {})

print("=== SEKCJA SUMMARY W v1.0 ===")
print(f"Klucze: {list(summary.keys())}")

# Utwórz strukturę podsumowanie zgodną z template V2
v2['podsumowanie'] = {
    # Główna treść podsumowania
    "glowny": summary.get('main', ''),
    
    # Closing case study
    "case_study": {
        "title": "🌱 Closing Case Study – rozmowa, która odbudowała zaufanie",
        "description": "Powrót do historii Marty i jej zespołu",
        "resolution": summary.get('case_study', '')
    },
    
    # Mapa myśli
    "mapa_mysli": summary.get('mind_map', {}),
    
    # Ściągawka (cheat sheet)
    "sciagawka": {
        "title": "📄 Cheat Sheet - Conversational Intelligence",
        "description": "Szybki przewodnik po najważniejszych technikach C-IQ",
        "content": summary.get('cheatsheet', '')
    },
    
    # Szablon planu działań (opcjonalny)
    "szablon_planu_dzialan": {
        "title": "📋 Action Plan - Co wdrożę?",
        "description": "Zaplanuj wykorzystanie C-IQ w swojej pracy",
        "sections": [
            {
                "title": "1. Pierwsza zmiana w moich rozmowach",
                "prompt": "Którą technikę C-IQ zastosujesz jako pierwszą? Kiedy to wypróbujesz?"
            },
            {
                "title": "2. Rytuał rozmów zespołowych",
                "prompt": "Jak zaprojektujesz rytuał rozmów w swoim zespole? Jakie pytanie zadasz na początku spotkania?"
            },
            {
                "title": "3. Przejście na Poziom III",
                "prompt": "W jakiej sytuacji najczęściej pozostajesz na Poziomie II? Jak możesz to zmienić?"
            },
            {
                "title": "4. Mierzenie postępów",
                "prompt": "Jak będziesz mierzyć poprawę jakości rozmów? (np. liczba pytań Poziomu III, poziom zaangażowania)"
            }
        ]
    },
    
    # Dziennik refleksji (opcjonalny)
    "dziennik_refleksji": {
        "title": "📓 Dziennik Refleksji",
        "description": "3 pytania do przemyślenia",
        "pytania": [
            {
                "id": "q1",
                "pytanie": "Która z koncepcji C-IQ zrobiła na Tobie największe wrażenie?",
                "placeholder": "Neurobiologia rozmowy, poziomy rozmów, architektura rozmowy..."
            },
            {
                "id": "q2",
                "pytanie": "W jakich sytuacjach najczęściej aktywujesz kortyzol u innych?",
                "placeholder": "Feedback, spotkania zespołowe, trudne rozmowy..."
            },
            {
                "id": "q3",
                "pytanie": "Jak zmieniłaby się kultura Twojego zespołu, gdyby wszyscy stosowali zasady C-IQ?",
                "placeholder": "Więcej zaufania, otwartości, innowacji..."
            }
        ]
    }
}

# Zapisz
with open(v2_path, 'w', encoding='utf-8') as f:
    json.dump(v2, f, ensure_ascii=False, indent=2)

print("\n✅ SEKCJA PODSUMOWANIE ZMIGROWANA!")
print("\n📊 Struktura podsumowanie (zgodna z V2 template):")
print(f"- glowny: ✅ ({len(summary.get('main', ''))} znaków)")
print(f"- case_study: ✅ ({len(summary.get('case_study', ''))} znaków)")
print(f"- mapa_mysli: ✅ ({len(summary.get('mind_map', {}))} elementów)")
print(f"- sciagawka: ✅ ({len(summary.get('cheatsheet', ''))} znaków)")
print(f"- szablon_planu_dzialan: ✅ (4 sekcje)")
print(f"- dziennik_refleksji: ✅ (3 pytania)")
print("\n🎉 MIGRACJA KOMPLETNA - wszystkie sekcje gotowe!")
