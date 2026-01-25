-- SQL script to insert "Model OJT - 5 Etapów" lesson into Supabase
-- PART 1: Cards 1-5 (Hero, Data, Content, Content, Content)
-- Run this in Supabase SQL Editor after running cleanup script

INSERT INTO lessons (
    id,
    lesson_id,
    title,
    description,
    difficulty,
    duration_minutes,
    xp_reward,
    content
) VALUES (
    gen_random_uuid(),
    'ojt_lesson_2_model',
    'Jak rozwijać pracowników bez odrywania ich od pracy?',
    'Poznaj 5-etapowy model On-the-Job Training, który w 3–4 miesiące zwiększa skuteczność zespołu o 20–50%, skraca czas rozwoju o połowę i realnie uwalnia czas menedżera.',
    'beginner',
    25,
    300,
    $$
    {
      "cards": [
        {
          "id": 1,
          "type": "hero",
          "title": "Jak rozwijać pracowników bez odrywania ich od pracy?",
          "content": "Poznaj 5-etapowy model On-the-Job Training",
          "sections": [
            {
              "icon": "👥",
              "title": "Dla kogo",
              "content": "Menedżerowie, którzy chcą przestać gasić pożary i zbudować zespół, który działa samodzielnie, bez ciągłego angażowania ich czasu."
            },
            {
              "icon": "🎯",
              "title": "Cel",
              "content": "Poznać 5-etapowy model On-the-Job Training, który w 3–4 miesiące:",
              "list": [
                "zwiększa skuteczność zespołu o 20–50%,",
                "skraca czas rozwoju o połowę,",
                "realnie uwalnia czas menedżera."
              ]
            },
            {
              "icon": "💡",
              "title": "Dlaczego to działa",
              "content": "70% kompetencji powstaje w praktyce. OJT to nauka w realnym biznesie + natychmiastowy feedback — 4× szybszy rozwój i trwała zmiana zachowań, nie teoria."
            }
          ],
          "estimated_seconds": 90,
          "xp_points": 10
        },
        {
          "id": 2,
          "type": "data",
          "title": "Dlaczego On-the-Job Training działa?",
          "content": "Większość kompetencji zawodowych rozwija się w praktyce, nie na szkoleniach formalnych (model 70-20-10).\n\nOJT skraca czas dojścia do samodzielności, bo łączy naukę z realną pracą i natychmiastowym feedbackiem.\n\nBadania L&D pokazują, że uczenie przez działanie ma znacząco wyższą trwałość efektów niż wykłady czy e-learning bez kontekstu.",
          "stats": [
            {
              "value": "70%",
              "label": "Procent wiedzy zawodowej zdobywanej przez praktyczne doświadczenie"
            },
            {
              "value": "4x",
              "label": "Szybciej rozwijają się pracownicy w treningu OJT vs tradycyjne szkolenia"
            },
            {
              "value": "85%",
              "label": "Wskaźnik retencji wiedzy przy nauce przez działanie vs 20% przy wykładach"
            }
          ],
          "callout": {
            "type": "info",
            "title": "Kluczowy wniosek:",
            "text": "Najskuteczniejsze uczenie się odbywa się w kontekście rzeczywistych zadań, z szybkim feedbackiem od bardziej doświadczonej osoby. To zmiana zachowań w pracy, a nie transfer teorii z sali szkoleniowej."
          },
          "sources": "Źródła: Deloitte (model 70-20-10), ATD, literatura L&D",
          "estimated_seconds": 120,
          "xp_points": 10
        },
        {
          "id": 3,
          "type": "content",
          "title": "Czym jest Model Treningu On-the-Job?",
          "content": "Model OJT to **cykl powtarzających się działań**, który pozwala pracownikowi rozwinąć umiejętności przez:

- **Praktyczne wykonywanie zadań** w rzeczywistym środowisku pracy
- **Obserwację przez doświadczonego mentora/menedżera** podczas wykonywania zadań
- **Konstruktywny feedback** oparty na faktach, nie opiniach
- **Systematyczną analizę** i wyciąganie wniosków na przyszłość

Kluczowa różnica vs tradycyjne szkolenia: **uczysz SIĘ pracując, nie przerywasz pracy, by się uczyć**",
          "remember": {
            "title": "Pamiętaj:",
            "items": [
              "Trening OJT ≠ \"rzucenie na głęboką wodę\"",
              "To systematyczny proces, nie przypadkowa obserwacja",
              "Wymaga przygotowania i struktury od menedżera"
            ]
          },
          "estimated_seconds": 100,
          "xp_points": 5
        },
        {
          "id": 4,
          "type": "content",
          "title": "5 Etapów Cyklu Treningu OJT",
          "content": "**1️⃣ ROZMOWA NA POCZĄTKU DNIA** ⏱️ 10-15 minut
Kontrakt na wspólną pracę, ustalenie celów rozwojowych i planu dnia

🔄 **CYKL POWTARZALNY** (dla każdej rozmowy/zadania - 3-5 razy dziennie)

**2️⃣ ODPRAWA PRZED ROZMOWĄ** ⏱️ 5-10 minut
Przypomnienie celów, analiza sytuacji, plan działania, demonstracja

**3️⃣ OBSERWACJA ROZMOWY** ⏱️ 30-60 minut
Zbieranie faktów, notowanie zachowań pracownika i reakcji klienta

**4️⃣ ANALIZA PO ROZMOWIE** ⏱️ 10-15 minut
Feedback, rozliczenie celów, wyciągnięcie wniosków, plan poprawy

↻ Powrót do etapu 2 dla kolejnej rozmowy/zadania

**5️⃣ PODSUMOWANIE DNIA** ⏱️ 15-20 minut
Rozliczenie celów dnia, wnioski, plan działań wdrożeniowych",
          "estimated_seconds": 120,
          "xp_points": 10
        },
        {
          "id": 5,
          "type": "content",
          "title": "Etap 1: Rozmowa na początku dnia",
          "content": "**Czas:** 10-15 minut na początku wspólnego dnia
**Cel:** Stworzyć fundament współpracy i uzgodnić zasady gry

**4 kluczowe elementy:**

1. **Sprzedanie idei treningu**
   Dlaczego warto wspólnie pracować? Jaki jest cel tej sesji?

2. **Kontrakt na wspólną pracę**
   Jak będziemy pracować? (role, zasady komunikacji, co robisz gdy potrzebuję pomocy)

3. **Ustalenie celów rozwojowych**
   Nad czym będziemy pracować? (1-2 konkretne umiejętności)

4. **Plan dnia**
   Co konkretnie zrobimy? (lista klientów/zadań, harmonogram)",
          "callout": {
            "type": "warning",
            "text": "⚠️ **Częsty błąd:** Pomijanie kontraktowania i wskakiwanie od razu w obserwację. Bez wyraźnej zgody pracownika i wspólnych celów, trening zamienia się w stresującą kontrolę!"
          },
          "remember": {
            "title": "Pamiętaj:",
            "items": [
              "Cele rozwojowe powinny być powiązane z celami biznesowymi (np. \"poprawić zamykanie sprzedaży\" → zwiększenie konwersji)"
            ]
          },
          "estimated_seconds": 120,
          "xp_points": 10
        },
        {
          "id": 6,
          "type": "story",
          "title": "Przykład: Dobry vs Zły Kontrakt",
          "scenarios": [
            {
              "type": "bad",
              "title": "❌ ŹLE: Brak kontraktu",
              "dialogue": [
                {
                  "speaker": "Menedżer",
                  "text": "Dzisiaj jadę z Tobą do klientów. Będę obserwował."
                },
                {
                  "speaker": "Pracownik",
                  "text": "(w myślach: Sprawdza mnie? Ocenia? Szuka błędów?)"
                }
              ],
              "consequences": [
                "Pracownik jest spięty, boi się popełnić błąd",
                "Nie eksperymentuje, gra bezpiecznie",
                "Po wizycie otrzymuje feedback jak krytykę, nie rozwój"
              ]
            },
            {
              "type": "good",
              "title": "✅ DOBRZE: Jasny kontrakt",
              "dialogue": [
                {
                  "speaker": "Menedżer",
                  "text": "Dzisiaj pracujemy razem nad techniką pytań otwartych. Będę obserwował Twoje rozmowy, notował co widzę, a potem porozmawiamy co można poprawić. To NIE jest ocena – to Twoja szansa na eksperyment i naukę. Może być?"
                },
                {
                  "speaker": "Pracownik",
                  "text": "Ok, super! Chcę popracować nad wykrywaniem potrzeb."
                }
              ],
              "consequences": [
                "Pracownik wie, czego się spodziewać",
                "Ma przestrzeń na próby i błędy",
                "Feedback jest oczekiwany i konstruktywny"
              ]
            }
          ],
          "lesson": "Dobry kontrakt = psychologiczne bezpieczeństwo = prawdziwy rozwój",
          "estimated_seconds": 120,
          "xp_points": 10
        }
      ]
    }
    $$::jsonb
);
