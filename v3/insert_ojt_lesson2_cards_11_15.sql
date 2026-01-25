-- SQL script to insert OJT Lesson 2 - Cards 11-15
-- PART 3: Content, Lightbulb, Quiz, Practice, Content
-- Run this after inserting cards 6-10

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
    'ojt_lesson_2_model_part3',  -- Temporary ID for testing
    'OJT Lesson 2 - Cards 11-15',
    'Test cards 11-15 (Content, Lightbulb, Quiz, Practice, Content)',
    'beginner',
    25,
    300,
    '{
      "cards": [
        {
          "id": 11,
          "type": "content",
          "title": "Etap 3: Obserwacja rozmowy z klientem",
          "content": "**Czas:** 30-60 minut (czas trwania zadania/rozmowy)\\n**Twoja rola:** OBSERWATOR (nie uczestnik!)\\n\\n**Główne zasady:**\\n\\n1. **Minimalizuj swoją aktywność** – Im mniej mówisz, tym lepiej\\n\\n2. **Zbieraj FAKTY, nie interpretacje** – Notuj co się dzieje, nie co myślisz\\n\\n3. **Zachowaj kontrakt** – Wchodź tylko gdy umówiliście się na to\\n\\n4. **Notuj kluczowe momenty** – Cytaty, reakcje klienta, sekwencja zdarzeń\\n\\n### Różnica: Fakty vs Interpretacje",
          "comparison": {
            "headers": ["✅ FAKTY (notuj to)", "❌ INTERPRETACJE (unikaj)"],
            "rows": [
              {
                "correct": "\\"Klient zapytał: \\"Ile to kosztuje?\\"\\"",
                "wrong": "\\"Klient był zainteresowany ceną\\""
              },
              {
                "correct": "\\"Ania odpowiedziała po 3 sekundach\\"",
                "wrong": "\\"Ania była niepewna\\""
              },
              {
                "correct": "\\"Klient przerwał i zmienił temat na...\\"",
                "wrong": "\\"Klient nie był przekonany\\""
              },
              {
                "correct": "\\"Żadnego zamknięcia sprzedaży nie było\\"",
                "wrong": "\\"Brakuje jej asertywności\\""
              }
            ]
          },
          "callout": {
            "type": "warning",
            "text": "Wskakiwanie do rozmowy i \\"ratowanie\\" pracownika. To niszczy jego autorytet i odbiera szansę na naukę przez błędy!"
          },
          "estimated_seconds": 120,
          "xp_points": 10
        },
        {
          "id": 12,
          "type": "lightbulb",
          "icon": "💡",
          "title": "Dlaczego Fakty > Interpretacje?",
          "content": "**Interpretacje są subiektywne** - Twoja ocena \\"był niepewny\\" może być błędna.\\n**Fakty są obiektywne** - \\"Odpowiedział po 3 sekundach\\" - nie do podważenia.",
          "insights": [
            {
              "type": "positive",
              "text": "✅ Fakty pozwalają pracownikowi samemu dojść do wniosków"
            },
            {
              "type": "negative",
              "text": "❌ Interpretacje wywołują obronę i sprzeciw"
            }
          ],
          "examples": [
            {
              "type": "wrong",
              "label": "❌ Interpretacja:",
              "text": "\\"Byłeś niepewny i dlatego klient się wycofał\\"",
              "reaction": "\\"Wcale nie byłem niepewny!\\" → Obrona, zaprzeczanie"
            },
            {
              "type": "correct",
              "label": "✅ Fakt + Pytanie:",
              "text": "\\"Zauważyłem, że po pytaniu klienta o cenę odpowiedziałeś po 3 sekundach. Co się wtedy działo?\\"",
              "reaction": "\\"Tak... faktycznie się zawahałem, bo nie byłem pewien marży...\\" → Refleksja, uczenie się"
            }
          ],
          "estimated_seconds": 100,
          "xp_points": 10
        },
        {
          "id": 13,
          "type": "quiz",
          "title": "Sprawdź swoją wiedzę: Obserwacja",
          "questions": [
            {
              "id": 1,
              "text": "Która notatka jest FAKTEM, nie interpretacją?",
              "options": [
                {
                  "letter": "A",
                  "text": "Klient był niezadowolony z oferty",
                  "correct": false
                },
                {
                  "letter": "B",
                  "text": "Pracownik nie miał pewności siebie",
                  "correct": false
                },
                {
                  "letter": "C",
                  "text": "Klient zapytał 3 razy o cenę konkurencji",
                  "correct": true
                }
              ],
              "explanation": "Opcja C to czysty fakt - obiektywna obserwacja bez oceny. A i B to interpretacje, które mogą być błędne."
            },
            {
              "id": 2,
              "text": "Kiedy powinieneś wejść do rozmowy jako obserwator?",
              "options": [
                {
                  "letter": "A",
                  "text": "Gdy widzę, że pracownik popełnia błąd",
                  "correct": false
                },
                {
                  "letter": "B",
                  "text": "Gdy pracownik poprosi o pomoc (zgodnie z kontraktem)",
                  "correct": true
                },
                {
                  "letter": "C",
                  "text": "Gdy rozmowa się przeciąga",
                  "correct": false
                }
              ],
              "explanation": "Wchodzisz TYLKO gdy umówiliście się na to w kontrakcie lub gdy pracownik wyraźnie prosi. Inaczej odbierasz mu szansę na naukę."
            },
            {
              "id": 3,
              "text": "Co robisz, gdy klient zaczyna zadawać Tobie pytania (pomimo że jesteś obserwatorem)?",
              "options": [
                {
                  "letter": "A",
                  "text": "Odpowiadam szczegółowo - nie mogę ignorować klienta",
                  "correct": false
                },
                {
                  "letter": "B",
                  "text": "Przekierowuję do pracownika: \\"To świetne pytanie - Ania najlepiej odpowie\\"",
                  "correct": true
                },
                {
                  "letter": "C",
                  "text": "Przejmuję rozmowę - to wyjątkowa sytuacja",
                  "correct": false
                }
              ],
              "explanation": "Przekierowujesz do pracownika i wzmacniasz jego autorytet. Jeśli odpowiesz sam, klient będzie kierować kolejne pytania do Ciebie, niszcząc pozycję pracownika."
            }
          ],
          "estimated_seconds": 180,
          "xp_points": 20
        },
        {
          "id": 14,
          "type": "practice",
          "title": "Ćwiczenie: Przekształć interpretacje w fakty",
          "instruction": "Masz notatki z obserwacji. Przekształć interpretacje w obiektywne fakty:",
          "scenario": "**Twoje notatki (INTERPRETACJE):**\\n1. \\"Pracownik nie słuchał klienta\\"\\n2. \\"Klient był zdezorientowany\\"\\n3. \\"Brak profesjonalizmu w zamknięciu\\"",
          "inputs": [
            {
              "label": "1. Fakty zamiast \\"nie słuchał klienta\\":",
              "placeholder": "Np. Co konkretnie zaobserwowałeś?",
              "type": "textarea"
            },
            {
              "label": "2. Fakty zamiast \\"klient był zdezorientowany\\":",
              "placeholder": "Np. Co powiedział/zrobił klient?",
              "type": "textarea"
            },
            {
              "label": "3. Fakty zamiast \\"brak profesjonalizmu\\":",
              "placeholder": "Np. Co konkretnie się wydarzyło (lub NIE wydarzyło)?",
              "type": "textarea"
            }
          ],
          "sampleAnswers": {
            "title": "Przykładowe przekształcenia:",
            "answers": [
              "**\\"Nie słuchał klienta\\" →** \\"Klient 2 razy wspomniał o budżecie, ale pracownik kontynuował prezentację produktu premium bez odniesienia się do tej informacji\\"",
              "**\\"Klient był zdezorientowany\\" →** \\"Klient zapytał: \\"Czyli jak to dokładnie działa?\\" i \\"Przepraszam, nie rozumiem różnicy między X a Y\\"\"",
              "**\\"Brak profesjonalizmu\\" →** \\"Rozmowa zakończyła się bez pytania o następne kroki. Pracownik powiedział: \\"To tyle z mojej strony\\" i wstał\\""
            ],
            "tip": "Fakty pozwalają pracownikowi samemu dojść do wniosku. Gdy powiesz \\"Klient 2 razy wspomniał o budżecie...\\" pracownik powie: \\"Racja, powinienem był się do tego odnieść!\\". Gdy powiesz \\"Nie słuchałeś\\" - włączy obronę."
          },
          "estimated_seconds": 200,
          "xp_points": 15
        },
        {
          "id": 15,
          "type": "content",
          "title": "Etap 4: Analiza po rozmowie z klientem",
          "content": "**Czas:** 10-15 minut po każdej rozmowie/zadaniu\\n**Cel:** Przekształcić doświadczenie w wiedzę i plan rozwoju\\n\\n### 5-stopniowa struktura analizy:",
          "steps": [
            {
              "number": 1,
              "emoji": "1️⃣",
              "title": "ODCZUCIA",
              "question": "Jak się czujesz po tej rozmowie?",
              "goal": "Rozładowanie emocji, budowanie zaufania",
              "time": "1-2 minuty"
            },
            {
              "number": 2,
              "emoji": "2️⃣",
              "title": "CELE",
              "question": "Jakie były Twoje cele? Co chciałeś osiągnąć?",
              "goal": "Przypomnienie punktu odniesienia",
              "time": "1 minuta"
            },
            {
              "number": 3,
              "emoji": "3️⃣",
              "title": "PRZEBIEG",
              "question": "Co poszło dobrze? Co było trudne? Co cię zaskoczyło?",
              "goal": "Analiza faktów, samoocena pracownika",
              "time": "3-5 minut"
            },
            {
              "number": 4,
              "emoji": "4️⃣",
              "title": "ALTERNATYWY",
              "question": "Co mógłbyś zrobić inaczej? Jakie inne opcje miałeś?",
              "goal": "Rozwijanie kreatywnego myślenia",
              "time": "2-3 minuty"
            },
            {
              "number": 5,
              "emoji": "5️⃣",
              "title": "WNIOSKI I PLAN",
              "question": "Czego się nauczyłeś? Co zrobisz inaczej następnym razem?",
              "goal": "Konkretny plan wdrożeniowy",
              "time": "2-3 minuty"
            }
          ],
          "estimated_seconds": 120,
          "xp_points": 10
        }
      ]
    }'::jsonb
);
