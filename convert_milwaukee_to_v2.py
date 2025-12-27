"""
Skrypt konwertujący lekcję MILWAUKEE_Application_First_Canvas z v1.0 do v2.0
"""
import json
import os

# Wczytaj plik v1.0
with open('data/lessons/MILWAUKEE_Application_First_Canvas.json', 'r', encoding='utf-8-sig') as f:
    lesson_v1 = json.load(f)

# Utwórz nową strukturę v2.0
lesson_v2 = {
    "_template_info": {
        "version": "2.0",
        "created": "2025-12-19",
        "converted_from": "v1.0"
    },
    "_lesson_info": lesson_v1["_lesson_info"],
    "id": lesson_v1["id"],
    "title": lesson_v1["title"],
    "description": lesson_v1["description"],
    "tag": lesson_v1["tag"],
    "xp_reward": lesson_v1["xp_reward"],
    "difficulty": lesson_v1["difficulty"]
}

# Zaktualizuj wersję w _lesson_info
lesson_v2["_lesson_info"]["version"] = "2.0"

# BLOK 1: wprowadzenie
lesson_v2["wprowadzenie"] = {
    "glowny": lesson_v1["intro"]["main"],
    "case_study": {
        "title": "🎭 Case Study: Dwie wizyty - która prowadzi do sukcesu?",
        "description": "Przeanalizuj dwie wizyty JSS na tej samej budowie. Obie dotyczą montażu instalacji wentylacyjnej (śruby M8 w konstrukcji stalowej, 200-300 połączeń dziennie, 2-osobowa ekipa).",
        "content": lesson_v1["intro"]["case_study"]
    }
}

# BLOK 2: nauka
sekcje = []
for section in lesson_v1["sections"]["learning"]["sections"]:
    sekcje.append({
        "tytul": section["title"],
        "tresc": section["content"]
    })

lesson_v2["nauka"] = {
    "tekst": {
        "sekcje": sekcje
    }
}

# BLOK 3: praktyka
# Konwertuj case_studies na cwiczenia
cwiczenia_html = lesson_v1["sections"]["practical_exercises"]["case_studies"]

lesson_v2["praktyka"] = {
    "cwiczenia": {
        "tresc": cwiczenia_html
    },
    "quiz_koncowy": lesson_v1["sections"]["practical_exercises"]["closing_quiz"]
}

# Dodaj passing_score do quizu
if "passing_score" not in lesson_v2["praktyka"]["quiz_koncowy"]:
    lesson_v2["praktyka"]["quiz_koncowy"]["passing_score"] = 70

# BLOK 4: podsumowanie
summary_main = lesson_v1["summary"]["main"]

# Wyodrębnij action plan z HTML (pola tekstowe: action_today, action_tomorrow, action_week)
szablon_planu = {
    "opis": "Wypełnij poniższy plan działania",
    "pola": [
        {
            "id": "action_today",
            "label": "📅 DZIŚ (15 minut po lekcji)",
            "placeholder": "Co zrobię DZIŚ po tej lekcji? (np. wydrukuję checklist Canvas, zapiszę w telefonie 3 kluczowe pytania z KROKU 1)"
        },
        {
            "id": "action_tomorrow",
            "label": "🎯 JUTRO (Pierwsze zastosowanie)",
            "placeholder": "Jak zastosuję Canvas w pracy JUTRO? (np. na wizycie u klienta X zacznę od KROKU 1 - pytania o aplikację zamiast prezentacji produktu)"
        },
        {
            "id": "action_week",
            "label": "⏰ ZA TYDZIEŃ (Review + powtórka)",
            "placeholder": "Co zrobię ZA TYDZIEŃ? (np. wrócę do quizu końcowego, przejrzę fiszki, porównam moje pierwsze wizyty Canvas z checklistą)"
        }
    ]
}

# Wyodrębnij reflection z HTML (pola: reflection_discovery, reflection_doubts, reflection_application)
dziennik_refleksji = {
    "opis": "Odpowiedz na 3 pytania poniżej",
    "pytania": [
        {
            "id": "reflection_discovery",
            "pytanie": "💡 1. Co było dla mnie NAJWIĘKSZYM odkryciem w tej lekcji?",
            "placeholder": "Np. \"Największe odkrycie to zasada z KROKU 2 - jeśli klient nie nazwie problemu, nie ma decyzji. Zawsze sugerowałem problemy zamiast pozwolić klientowi je nazwać samemu.\""
        },
        {
            "id": "reflection_doubts",
            "pytanie": "🤔 2. Co WCIĄŻ mi nie do końca pasuje? (pytania/wątpliwości)",
            "placeholder": "Np. \"Nie jestem pewien, jak długo powinienem trwać w KROKU 1 (Aplikacja) - 5 minut? 15 minut? Jak poznać, że to czas przejść do KROKU 2?\""
        },
        {
            "id": "reflection_application",
            "pytanie": "🚀 3. Jak KONKRETNIE zastosuję tę wiedzę w ciągu 48 godzin?",
            "placeholder": "Np. \"W czwartek mam wizytę u klienta na budowie (montaż konstrukcji stalowych). Zacznę od KROKU 1 - zadam 5 pytań o aplikację zamiast od razu pokazywać katalog. Cel: zrozumieć Job to be Done przed jakąkolwiek prezentacją produktu.\""
        }
    ]
}

lesson_v2["podsumowanie"] = {
    "glowny": summary_main,
    "szablon_planu_dzialan": szablon_planu,
    "dziennik_refleksji": dziennik_refleksji
}

# Zapisz plik v2.0
output_path = 'data/lessons/MILWAUKEE_Application_First_Canvas.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(lesson_v2, f, ensure_ascii=False, indent=2)

print(f"✅ Konwersja zakończona pomyślnie!")
print(f"📁 Zapisano: {output_path}")
print(f"📊 Struktura v2.0:")
print(f"   - wprowadzenie: glowny + case_study")
print(f"   - nauka: {len(sekcje)} sekcji tekstowych")
print(f"   - praktyka: cwiczenia + quiz_koncowy")
print(f"   - podsumowanie: glowny + szablon_planu_dzialan + dziennik_refleksji")
