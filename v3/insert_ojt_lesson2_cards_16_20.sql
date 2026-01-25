-- SQL script to insert OJT Lesson 2 - Cards 16-20
-- PART 4: Story, Lightbulb, Quiz, Practice, Content
-- Run this after inserting cards 11-15

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
    'ojt_lesson_2_model_part4',  -- Temporary ID for testing
    'OJT Lesson 2 - Cards 16-20',
    'Test cards 16-20 (Story, Lightbulb, Quiz, Practice, Content)',
    'beginner',
    25,
    300,
    '{
      "cards": [
        {
          "id": 16,
          "type": "story",
          "title": "Przykład: Analiza, która zmieniła wszystko",
          "situation": "Karol (handlowiec) wraca z nieudanej rozmowy. Klient powiedział \\"pomyślimy\\". Karol jest sfrustrowany. Menedżer Michał stosuje 5-stopniową analizę:",
          "phases": [
            {
              "title": "1️⃣ ODCZUCIA",
              "dialogue": [
                {"speaker": "Michał", "text": "Jak się czujesz po tej rozmowie?"},
                {"speaker": "Karol", "text": "Źle. Znowu \\"pomyślimy\\". Strata czasu."},
                {"speaker": "Michał", "text": "Rozumiem frustrację. Daj sobie chwilę, a potem przeanalizujmy co się wydarzyło."}
              ]
            },
            {
              "title": "2️⃣ CELE",
              "dialogue": [
                {"speaker": "Michał", "text": "Jaki był Twój cel na tę rozmowę?"},
                {"speaker": "Karol", "text": "Chciałem zamknąć ofertę na 50k."}
              ]
            },
            {
              "title": "3️⃣ PRZEBIEG",
              "dialogue": [
                {"speaker": "Michał", "text": "Co poszło dobrze?"},
                {"speaker": "Karol", "text": "Dobra prezentacja produktu, klient słuchał."},
                {"speaker": "Michał", "text": "A co było trudne?"},
                {"speaker": "Karol", "text": "Gdy zapytałem o decyzję, klient zmienił temat..."}
              ]
            },
            {
              "title": "4️⃣ ALTERNATYWY",
              "dialogue": [
                {"speaker": "Michał", "text": "Co mógłbyś zrobić inaczej w tym momencie?"},
                {"speaker": "Karol", "text": "(myśli) Hmm... może zamiast \\"Czy podpisujemy?\\" zapytać \\"Co musi się wydarzyć, żebyśmy mogli ruszyć do przodu?\\""},
                {"speaker": "Michał", "text": "Dokładnie! A zauważyłeś, że gdy klient zaczął mówić o budżecie, przeskoczyłeś do ceny zamiast dowiedzieć się więcej?"}
              ]
            },
            {
              "title": "5️⃣ WNIOSKI",
              "dialogue": [
                {"speaker": "Michał", "text": "Co wynosisz na przyszłość?"},
                {"speaker": "Karol", "text": "Następnym razem zamiast \\"czy podpisujemy\\" zapytam o konkretne obawy. I będę słuchał sygnałów o budżecie."}
              ]
            }
          ],
          "outcome": "W kolejnej rozmowie Karol zastosował nową technikę pytań. Zamiast \\"pomyślimy\\" dowiedział się, że klient potrzebuje akceptacji szefa. Umówił rozmowę z decydentem i zamknął deal 65k. **Analiza zamieniła porażkę w lekcję.**",
          "lesson": "Dobra analiza to nie krytyka, a odkrywanie razem. Karol SAM doszedł do wniosków - dzięki temu faktycznie je zapamiętał i zastosował.",
          "estimated_seconds": 180,
          "xp_points": 10
        },
        {
          "id": 17,
          "type": "lightbulb",
          "icon": "💡",
          "title": "Pytaj, nie mów - dlaczego to działa?",
          "comparison": {
            "headers": ["❌ GDY MÓWISZ (Dajesz gotowe odpowiedzi)", "✅ GDY PYTASZ (Pomagasz odkryć)"],
            "rows": [
              {
                "wrong": "\\"Powinieneś był zapytać o budżet\\"",
                "right": "\\"Co mogłeś zapytać, żeby dowiedzieć się więcej?\\""
              },
              {
                "wrong": "Pracownik słucha pasywnie",
                "right": "Pracownik aktywnie myśli"
              },
              {
                "wrong": "Zależność od Twojej wiedzy",
                "right": "Budowanie samodzielności"
              },
              {
                "wrong": "\\"Spróbuję to zapamiętać\\"",
                "right": "\\"Sam na to wpadłem - zostanie ze mną\\""
              },
              {
                "wrong": "Możliwa obrona / \\"Ale ja...\\"",
                "right": "Refleksja / \\"Faktycznie, racja...\\""
              }
            ]
          },
          "whenToTell": {
            "title": "Kiedy MÓWIĆ (dawać feedback bezpośrednio)?",
            "cases": [
              "Gdy pracownik nie widzi błędu mimo pytań",
              "Gdy brakuje mu wiedzy technicznej",
              "Gdy zauważasz wzorzec, którego on nie dostrzega",
              "Po tym jak SAM przeanalizował - wtedy dodajesz swoją perspektywę"
            ]
          },
          "highlight": "\\"Ludzie wspierają świat, który sami stworzyli\\"",
          "footnote": "Gdy pracownik SAM odkrywa rozwiązanie, czuje się autorem - i dlatego je wdraża.",
          "estimated_seconds": 110,
          "xp_points": 10
        },
        {
          "id": 18,
          "type": "quiz",
          "title": "Sprawdź swoją wiedzę: Analiza",
          "questions": [
            {
              "id": 1,
              "text": "Jak powinieneś zacząć analizę po rozmowie?",
              "options": [
                {"letter": "A", "text": "\\"Zrobiłeś 3 błędy - omówmy je po kolei\\"", "correct": false},
                {"letter": "B", "text": "\\"Jak się czujesz po tej rozmowie?\\"", "correct": true},
                {"letter": "C", "text": "\\"Jakie były cele tej rozmowy?\\"", "correct": false}
              ],
              "explanation": "Zaczynasz od ODCZUĆ - to rozładowuje emocje i buduje bezpieczną atmosferę. Dopiero potem przecodzisz do analizy merytorycznej."
            },
            {
              "id": 2,
              "text": "Co robisz, gdy pracownik neguje swój błąd mimo faktów?",
              "options": [
                {"letter": "A", "text": "Daję mu rację - nie warto się kłócić", "correct": false},
                {"letter": "B", "text": "Upieramy się - przecież mam notatki!", "correct": false},
                {"letter": "C", "text": "Przedstawiam fakty i pytam o alternatywną interpretację", "correct": true}
              ],
              "explanation": "\\"Zauważyłem, że klient 2 razy wspomniał o budżecie, a Ty kontynuowałeś prezentację premium. Jak Ty to widziałeś?\\". Fakty + otwarte pytanie = przestrzeń na dialog."
            },
            {
              "id": 3,
              "text": "Jak powinny brzmieć dobre WNIOSKI z analizy?",
              "options": [
                {"letter": "A", "text": "\\"Ogólnie było ok, następnym razem lepiej\\"", "correct": false},
                {"letter": "B", "text": "\\"Następnym razem zamiast \\"czy podpisujemy\\" zapytam \\"co musi się wydarzyć, żeby ruszyć do przodu\\"\"", "correct": true},
                {"letter": "C", "text": "\\"Muszę popracować nad zamykaniem sprzedaży\\"", "correct": false}
              ],
              "explanation": "Dobre wnioski są KONKRETNE i WYKONALNE. \\"Następnym razem zrobię X zamiast Y\\" to plan działania, nie ogólnikowa deklaracja."
            }
          ],
          "estimated_seconds": 180,
          "xp_points": 20
        },
        {
          "id": 19,
          "type": "practice",
          "title": "Ćwiczenie: Przekształć krytykę w pytania coachingowe",
          "instruction": "Masz notatkę z obserwacji i chcesz dać feedback. Zamień dyrektywną krytykę na pytania, które pomogą pracownikowi samemu dojść do wniosków:",
          "scenario": "**Scenariusz:**\\n\\nHandlowiec Ania prezentowała produkt klientowi, który wspomniał \\"mamy ograniczony budżet w tym kwartale\\". Ania zignorowała to i dalej prezentowała drogie opcje. Klient się wycofał.\\n\\n**❌ Twój impuls (krytyka):**\\n1. \\"Nie słuchałaś klienta\\"\\n2. \\"Powinnnaś była przejść na tańsze opcje\\"\\n3. \\"Straciłaś szansę na deal\\"",
          "inputs": [
            {
              "label": "Przekształć 1: \\"Nie słuchałaś klienta\\" → Pytanie coachingowe:",
              "placeholder": "Jak możesz to przeformułować jako pytanie?",
              "type": "textarea"
            },
            {
              "label": "Przekształć 2: \\"Powinnaś była przejść na tańsze opcje\\" → Pytanie:",
              "placeholder": "Jak możesz pomóc jej samej dojść do tego wniosku?",
              "type": "textarea"
            },
            {
              "label": "Przekształć 3: \\"Straciłaś szansę\\" → Pytanie o wnioski:",
              "placeholder": "Jak zapytać o plan na przyszłość?",
              "type": "textarea"
            }
          ],
          "sampleAnswers": {
            "title": "Przykładowe pytania coachingowe:",
            "answers": [
              "**\\"Nie słuchałaś\\" →** \\"Zauważyłam, że klient wspomniał o ograniczonym budżecie, a Ty kontynuowałaś prezentację opcji premium. Co się wtedy działo?\\" _(→ Fakty + otwarte pytanie, bez osądu)_",
              "**\\"Powinnaś była przejść na tańsze opcje\\" →** \\"Co mogłaś zrobić w momencie, gdy usłyszałaś \\"ograniczony budżet\\"? Jakie alternatywy miałaś?\\" _(→ Pomoż jej samej znaleźć rozwiązanie)_",
              "**\\"Straciłaś szansę\\" →** \\"Co wynosisz z tej sytuacji na przyszłość? Jak zareagujesz, gdy kolejny klient wspomni o budżecie?\\" _(→ Konkretny plan działania, nie poczucie winy)_"
            ],
            "tip": "**Efekt pytań vs krytyki:**\\n\\n**Krytyka:** Ania czuje się oceniona, wchodzi w obronę: \\"Ale ja chciałam pokazać najlepsze produkty!\\"\\n\\n**Pytania:** Ania analizuje: \\"Faktycznie, powinienem była zapytać o konkretny budżet i dostosować ofertę... następnym razem zacznę od tego pytania\\""
          },
          "estimated_seconds": 200,
          "xp_points": 15
        },
        {
          "id": 20,
          "type": "content",
          "title": "Etap 5: Podsumowanie całego dnia",
          "content": "**Czas:** 15-20 minut na koniec wspólnego dnia pracy\\n**Cel:** Rozliczyć cele dnia i stworzyć plan wdrożeniowy\\n\\n### 3 kluczowe elementy:",
          "elements": [
            {
              "number": 1,
              "emoji": "1️⃣",
              "title": "ROZLICZENIE CELÓW DNIA",
              "questions": [
                "\\"Nad czym pracowaliśmy dziś?\\" (przypomnienie celów z rana)",
                "\\"Co udało Ci się poprawić w stosunku do poprzedniego dnia?\\"",
                "\\"Gdzie widzisz największy postęp?\\""
              ]
            },
            {
              "number": 2,
              "emoji": "2️⃣",
              "title": "PLAN DZIAŁAŃ WDROŻENIOWYCH",
              "description": "**Konkrety na przyszłość:**",
              "items": [
                "Co konkretnie zastosujesz w następnym tygodniu?",
                "Jakie będą pierwsze 3 rzeczy, które zmienisz?",
                "Czego będziesz unikać?"
              ]
            },
            {
              "number": 3,
              "emoji": "3️⃣",
              "title": "UZNANIE I MOTYWACJA",
              "description": "**Wzmocnij postęp:**",
              "items": [
                "Co najbardziej mnie zaskoczyło dzisiaj u Ciebie?",
                "Widzę największy postęp w...",
                "Za tydzień / miesiąc będziesz w stanie..."
              ]
            }
          ],
          "remember": {
            "title": "Pamiętaj:",
            "items": [
              "Podsumowanie NIE to miejsce na nowe wnioski - to miejsce na ROZLICZENIE i PLAN",
              "Kończ POZYTYWNIE - nawet jeśli był trudny dzień, znajdź postęp",
              "Dokumentuj wnioski (np. wspólny dokument/notatka) - będą bazą na kolejny dzień"
            ]
          },
          "estimated_seconds": 120,
          "xp_points": 10
        }
      ]
    }'::jsonb
);
