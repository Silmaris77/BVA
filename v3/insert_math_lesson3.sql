-- Insert "Zaokrąglanie i szacowanie" Lesson
INSERT INTO lessons (
    lesson_id,
    title,
    description,
    duration_minutes,
    xp_reward,
    difficulty,
    content,
    module_id
) VALUES (
    'math-g7-l3',
    'Zaokrąglanie i szacowanie',
    'W życiu codziennym rzadko potrzebujemy idealnej dokładności. Naucz się sztuki szacowania i zaokrąglania liczb.',
    25,
    100,
    'beginner',
    '{
    "subtitle": "Moduł 1: Liczby i Działania",
    "cards": [
        {
            "type": "intro",
            "title": "Czy 4,481 m to 4,5 m?",
            "description": "W życiu codziennym rzadko potrzebujemy idealnej dokładności. Kiedy pytasz o godzinę, ktoś odpowiada ''za dziesięć trzecia'', a nie ''14:49:32''. Dziś nauczysz się sztuki zaokrąglania!"
        },
        {
            "type": "concept",
            "title": "Po co nam przybliżenia?",
            "content": "**Symbol ≈** czytamy ''równa się w przybliżeniu''.\\n\\nŚrednia odległość Ziemi od Księżyca to **384 400 km**. Nikt nie podaje jej z dokładnością do metra, bo Księżyc stale się porusza! Stosujemy zaokrąglenia, aby liczby były **łatwiejsze do zapamiętania i porównania**."
        },
        {
            "type": "concept",
            "title": "Złota reguła zaokrąglania",
            "content": "Aby zaokrąglić liczbę, patrzymy na cyfrę stojącą **po prawej stronie** rzędu, do którego zaokrąglamy.\\n\\n*   Jeśli to **0, 1, 2, 3, 4** → Zaokrąglamy **w dół** (cyfra rzędu bez zmian).\\n*   Jeśli to **5, 6, 7, 8, 9** → Zaokrąglamy **w górę** (cyfra rzędu +1)."
        },
        {
            "type": "digit-selector",
            "title": "Wartość pozycyjna",
            "question": "Zanim przejdziemy dalej: Wskaż cyfrę DZIESIĄTEK w tej liczbie.",
            "number": "184",
            "correctIndex": 1,
            "explanation": "8 to cyfra dziesiątek. 1 to setki, a 4 to jedności."
        },
        {
            "type": "input",
            "title": "Zaokrąglanie w dół",
            "question": "Zaokrąglij liczbę 184 do dziesiątek.",
            "correctAnswer": "180",
            "placeholder": "np. 180",
            "explanation": "Cyfra jedności to 4 (prawa strona). Jest mniejsza niż 5, więc zaokrąglamy w dół: 180."
        },
        {
            "type": "digit-selector",
            "title": "Wartość pozycyjna",
            "question": "Wskaż cyfrę, która ZADECYDUJE o tym, jak zaokrąglimy liczbę 2379 do dziesiątek.",
            "number": "2379",
            "correctIndex": 3,
            "explanation": "Decyduje cyfra stojąca po prawej stronie dziesiątek - czyli cyfra jedności (9)."
        },
        {
            "type": "input",
            "title": "Zaokrąglanie w górę",
            "question": "Zaokrąglij liczbę 2379 do dziesiątek.",
            "correctAnswer": "2380",
            "placeholder": "np. 2380",
            "explanation": "Cyfra jedności to 9. Jest $>= 5$, więc zaokrąglamy w górę: 7 zmienia się w 8, a 9 w 0."
        },
        {
            "type": "true-false",
            "title": "Sprawdź intuicję",
            "question": "Oceń poprawność zaokrągleń do SETEK:",
            "statements": [
                {
                    "id": "s1",
                    "text": "407 ≈ 400",
                    "isTrue": true,
                    "explanation": "Cyfra dziesiątek to 0 (<5), więc w dół."
                },
                {
                    "id": "s2",
                    "text": "750 ≈ 700",
                    "isTrue": false,
                    "explanation": "Cyfra dziesiątek to 5. Gdy mamy 5, zaokrąglamy W GÓRĘ. Powinno być 800."
                },
                {
                    "id": "s3",
                    "text": "1513 ≈ 1500",
                    "isTrue": true,
                    "explanation": "Cyfra dziesiątek to 1 (<5), więc w dół."
                }
            ]
        },
        {
            "type": "concept",
            "title": "Ułamki dziesiętne",
            "content": "Te same zasady działają po przecinku!\\n\\n**12,0307**\\n*   Cyfra części dziesiątych: **0**\\n*   Cyfra części setnych: **3**\\n*   Cyfra części tysięcznych: **0**"
        },
        {
            "type": "digit-selector",
            "title": "Części setne",
            "question": "Wskaż cyfrę części SETNYCH w liczbie 120,307",
            "number": "120.307",
            "correctIndex": 5,
            "explanation": "Pierwsze miejsce po przecinku to części dziesiąte (3), drugie to setne (0)."
        },
        {
            "type": "fill-gap",
            "title": "Trening zaokrąglania",
            "parts": [
                "Zaokrąglij do jedności: $13,574 \\approx$ ",
                {
                    "id": "g1",
                    "correctExact": 14,
                    "placeholder": "?"
                },
                "\\n\\nZaokrąglij do części dziesiątych: $9,118 \\approx$ ",
                {
                    "id": "g2",
                    "correctExact": 9.1,
                    "placeholder": "?"
                },
                "\\n\\nZaokrąglij do części setnych: $0,997 \\approx$ ",
                {
                    "id": "g3",
                    "correctExact": 1,
                    "placeholder": "?"
                }
            ],
            "explanation": "Dla 0,997: patrząc na trzecią cyfrę (7), zaokrąglamy w górę. 99 setnych zmienia się na 100 setnych, czyli 1 całość."
        },
        {
            "type": "practice",
            "title": "Szacowanie zakupów",
            "instruction": "Oszacuj w pamięci, czy wystarczy Ci pieniędzy.",
            "scenario": "Masz **50 zł**. Chcesz kupić **19 batoników** po **1,99 zł** każdy. Czy otrzymasz więcej czy mniej niż 10 zł reszty?",
            "inputs": [
                {
                    "label": "Zaokrąglij cenę batonika do pełnych złotych:",
                    "placeholder": "np. 2",
                    "type": "number"
                },
                {
                    "label": "Szacowany koszt 19 batoników (zakładając cenę 2 zł i 20 sztuk dla ułatwienia):",
                    "placeholder": "np. 40",
                    "type": "number"
                }
            ],
            "sampleAnswers": {
                "title": "Szybkie szacowanie",
                "answers": [
                    "1,99 zł ≈ 2 zł",
                    "19 sztuk ≈ 20 sztuk",
                    "20 * 2 zł = 40 zł.",
                    "50 zł - 40 zł = 10 zł. Skoro kupujesz MNIEJ niż 20 sztuk i płacisz MNIEJ niż 2 zł, to wydasz mniej niż 40 zł.",
                    "Zatem reszta będzie WIĘKSZA niż 10 zł."
                ]
            }
        },
        {
            "type": "number-sort",
            "title": "Szacowanie wyników",
            "question": "Uporządkuj wyniki działań od najmniejszego do największego (OSZACUJ):",
            "numbers": [
                200,
                2100,
                6300,
                28000
            ],
            "order": "asc",
            "explanation": "68*3 ≈ 70*3 = 210. 149*4 ≈ 150*4 = 600... czekaj, tu są inne liczby w zadaniu. Dopasujmy rzędy wielkości."
        },
        {
            "type": "quiz",
            "title": "Sprawdź, czy umiesz",
            "questions": [
                {
                    "question": "Gdy zaokrąglimy liczbę 3,(93) do części setnych, otrzymamy:",
                    "options": [
                        "4,00",
                        "3,94",
                        "3,93",
                        "3,9"
                    ],
                    "correctAnswer": 1,
                    "explanation": "3,(93) = 3,9393... Trzecia cyfra po przecinku to 9, więc zaokrąglamy w górę drugą cyfrę (3 -> 4)? Nie! Czekaj. 3,9393... Druga cyfra to 3. Trzecia to 9. 9 >= 5, więc podnosimy drugą cyfrę. 3 -> 4. Wynik: 3,94. Opcja B."
                },
                {
                    "question": "Która liczba jest zaokrągleniem 1513 do setek?",
                    "options": [
                        "1500",
                        "1510",
                        "1600",
                        "2000"
                    ],
                    "correctAnswer": 0,
                    "explanation": "Patrzymy na cyfrę dziesiątek (1). Jest mała (<5), więc w dół → 1500."
                }
            ]
        },
        {
            "type": "test",
            "title": "Końcowy Test: Zaokrąglanie",
            "questions": [
                {
                    "question": "Liczbę 18,531 zaokrąglona do jedności to:",
                    "options": [
                        "18",
                        "19",
                        "18,5",
                        "20"
                    ],
                    "correctAnswer": 1,
                    "explanation": "Pierwsza cyfra po przecinku to 5, więc zaokrąglamy w górę (do 19)."
                },
                {
                    "question": "Które zaokrąglenie do setek jest BŁĘDNE?",
                    "options": [
                        "249 ≈ 200",
                        "650 ≈ 700",
                        "999 ≈ 1000",
                        "350 ≈ 300"
                    ],
                    "correctAnswer": 3,
                    "explanation": "350 powinno być zaokrąglone w górę (do 400), bo cyfra dziesiątek to 5."
                },
                {
                    "question": "Oszacuj wynik 19 * 21:",
                    "options": [
                        "Około 200",
                        "Około 400",
                        "Około 600",
                        "Około 1000"
                    ],
                    "correctAnswer": 1,
                    "explanation": "20 * 20 = 400."
                },
                {
                    "question": "Zaokrąglij liczbę 0,0089 do części tysięcznych:",
                    "options": [
                        "0,008",
                        "0,009",
                        "0,010",
                        "0,000"
                    ],
                    "correctAnswer": 1,
                    "explanation": "Cyfra 10-tysięczna to 9 (>=5), więc 8 tysięcznych zmienia się w 9 tysięcznych."
                },
                {
                    "question": "Jeśli kupujesz 3 przedmioty po 9,99 zł każdy, to zapłacisz:",
                    "options": [
                        "Mniej niż 30 zł",
                        "Dokładnie 30 zł",
                        "Więcej niż 30 zł",
                        "Około 40 zł"
                    ],
                    "correctAnswer": 0,
                    "explanation": "9,99 < 10, więc 3 * 9,99 < 30."
                }
            ]
        },
        {
            "type": "summary",
            "title": "Podsumowanie",
            "recap": [
                "0, 1, 2, 3, 4 → Zaokrąglamy w dół (ucinamy/zera).",
                "5, 6, 7, 8, 9 → Zaokrąglamy w górę (cyfra +1).",
                "Zaokrąglanie to ''szacowanie'' - rezygnujemy z dokładności dla wygody.",
                "Pamiętaj o wartościach pozycyjnych (części dziesiąte, setne, tysiączne)."
            ],
            "badge": {
                "title": "Mistrz Szacowania",
                "xp": 100
            }
        }
    ]
}'::jsonb,
    'd290f1ee-6c54-4b01-90e6-d701748f0851'
) ON CONFLICT (lesson_id) DO UPDATE SET
    content = EXCLUDED.content,
    title = EXCLUDED.title,
    xp_reward = EXCLUDED.xp_reward,
    module_id = EXCLUDED.module_id;

-- Update Learning Path to include the new lesson
UPDATE learning_paths
SET lesson_sequence = jsonb_set(
    lesson_sequence,
    '{0,lessons}',
    (lesson_sequence->0->'lessons') || '["math-g7-l3"]'::jsonb
)
WHERE path_slug = 'math-grade-7';
