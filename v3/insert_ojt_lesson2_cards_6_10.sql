-- SQL script to insert OJT Lesson 2 - Cards 6-10
-- PART 2: Story, Lightbulb, Content, Practice, Story
-- Run this after inserting cards 1-5

-- First, fetch the existing lesson to update it
-- This script updates the content field by adding cards 6-10 to the existing cards array

-- For now, use this standalone INSERT for testing cards 6-10 independently
-- (In production, you'd UPDATE the existing lesson to append these cards)

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
    'ojt_lesson_2_model_part2',  -- Temporary ID for testing
    'OJT Lesson 2 - Cards 6-10',
    'Test cards 6-10 (Story, Lightbulb, Content, Practice, Story)',
    'beginner',
    25,
    300,
    '{
      "cards": [
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
        },
        {
          "id": 7,
          "type": "lightbulb",
          "icon": "💡",
          "title": "Kontrakt = Psychologiczne Bezpieczeństwo",
          "content": "Bez wyraźnej umowy pracownik **domyśla się** Twoich intencji i często myli:",
          "comparison": {
            "headers": ["Co pracownik myśli", "Co naprawdę chcesz"],
            "rows": [
              {
                "wrong": "❌ Ocena / Kontrola",
                "right": "✅ Rozwój / Wsparcie"
              },
              {
                "wrong": "❌ Krytyka",
                "right": "✅ Konstruktywny feedback"
              },
              {
                "wrong": "❌ Test kompetencji",
                "right": "✅ Eksperyment / Nauka"
              },
              {
                "wrong": "❌ \\"Szukanie błędów\\"",
                "right": "✅ Identyfikacja obszarów rozwoju"
              }
            ]
          },
          "highlight": "\\"Pracujemy NAD tobą, nie PRZECIWKO tobie\\"",
          "footnote": "Dobry kontrakt eliminuje lęk i otwiera pracownika na feedback. To fundament całego procesu OJT.",
          "estimated_seconds": 100,
          "xp_points": 10
        },
        {
          "id": 8,
          "type": "content",
          "title": "Etap 2: Odprawa przed rozmową z klientem",
          "content": "**Czas:** 5-10 minut przed każdą rozmową/zadaniem\\n**Cel:** Przygotować pracownika do świadomego działania\\n\\n**4 kluczowe elementy:**\\n\\n1. **Przypomnienie celów**\\n   Na czym się dziś koncentrujemy? (np. \\"Pracujemy nad techniką pytań otwartych\\")\\n\\n2. **Analiza sytuacji**\\n   Co wiemy o kliencie/zadaniu? Jakie mamy narzędzia? Jaki jest kontekst?\\n\\n3. **Plan działania**\\n   Jak zamierzasz to przeprowadzić? Jaki masz pomysł? Co chcesz osiągnąć?\\n\\n4. **Demonstracja (opcjonalnie)**\\n   Pokażę Ci, jak to wygląda w praktyce (krótki roleplay/przykład)",
          "remember": {
            "title": "Pamiętaj:",
            "items": [
              "To NIE jest przesłuchanie – pytaj, nie odpytuj",
              "Pozwól pracownikowi samodzielnie opracować plan (Ty tylko koryguj/sugeruj)",
              "Demonstracja ≠ robienie za pracownika (pokazujesz technikę, nie rozwiązujesz problem)"
            ]
          },
          "estimated_seconds": 110,
          "xp_points": 10
        },
        {
          "id": 9,
          "type": "practice",
          "title": "Ćwiczenie: Przygotuj pytania na odprawę",
          "scenario": "Pracujesz z handlowcem Markiem nad umiejętnością **wykrywania potrzeb klienta**. Za 10 minut jedziecie do klienta \\"XYZ Sp. z o.o.\\" (średnia firma budowlana, 2 lata współpracy, ostatnio spadek zamówień).",
          "instruction": "Napisz 3 pytania, które zadasz Markowi na odprawie PRZED rozmową:",
          "inputs": [
            {
              "label": "1. Pytanie o cel rozwojowy:",
              "placeholder": "Wpisz swoje pytanie..."
            },
            {
              "label": "2. Pytanie o sytuację klienta:",
              "placeholder": "Wpisz swoje pytanie..."
            },
            {
              "label": "3. Pytanie o plan działania:",
              "placeholder": "Wpisz swoje pytanie..."
            }
          ],
          "sampleAnswers": {
            "title": "Przykładowe pytania:",
            "answers": [
              "\\"Na jakich pytaniach się dzisiaj skupiamy, żeby wykryć realne potrzeby klienta XYZ?\\"",
              "\\"Co wiesz o sytuacji XYZ? Dlaczego ich zamówienia spadły?\\"",
              "\\"Jak planujesz rozpocząć rozmowę, żeby klient otworzył się na temat swoich wyzwań?\\""
            ]
          },
          "estimated_seconds": 180,
          "xp_points": 15
        },
        {
          "id": 10,
          "type": "story",
          "title": "Przykład: Siła Demonstracji",
          "situation": "Menedżer Anna pracuje z młodym handlowcem Piotrem nad **radzeniem sobie z obiekcją cenową**. Piotr teoretycznie zna techniki, ale w praktyce się wycofuje.",
          "phases": [
            {
              "title": "Przed wizytą (odprawa):",
              "type": "briefing",
              "dialogue": [
                {
                  "speaker": "Anna",
                  "text": "Pokaż mi, jak odpowiesz, gdy klient powie: \\"To za drogie\\"?"
                },
                {
                  "speaker": "Piotr",
                  "text": "(niepewnie) \\"No... powiem że mamy najlepszą jakość...\\""
                },
                {
                  "speaker": "Anna",
                  "text": "Okej, zobacz jak ja bym to zrobiła. Ty jesteś klientem."
                }
              ]
            },
            {
              "title": "Demonstracja (roleplay 2 min):",
              "type": "demonstration",
              "dialogue": [
                {
                  "speaker": "Piotr (jako klient)",
                  "text": "To za drogie."
                },
                {
                  "speaker": "Anna",
                  "text": "(spokojnie) \\"Rozumiem. A z czym Pan porównuje? (pauza) Bo widzę, że korzysta Pan teraz z X, prawda? Jakie ma Pan z tym doświadczenia?\\""
                }
              ]
            }
          ],
          "outcome": "Piotr WIDZI, jak spokojnie zadać pytanie zamiast bronić się. W prawdziwej rozmowie użył tej techniki i zdobył informację, że klient porównuje cenę z najtańszą ofertą (bez serwisu). Dzięki temu wygrał kontrakt podkreślając wartość wsparcia.",
          "lesson": "Demonstracja buduje pewność siebie i pokazuje \\"jak to się robi naprawdę\\". Warto 2 minuty roleplayu niż 20 minut teorii.",
          "estimated_seconds": 150,
          "xp_points": 10
        }
      ]
    }'::jsonb
);
