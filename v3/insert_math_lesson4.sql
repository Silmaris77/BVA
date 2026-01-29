-- Insert "Dodawanie i odejmowanie liczb dodatnich" Lesson
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
    'math-g7-l4',
    'Dodawanie i odejmowanie liczb dodatnich',
    'Naucz się dodawać i odejmować ułamki zwykłe oraz dziesiętne. Poznaj zasadę wspólnego mianownika i zamianę między postaciami ułamków.',
    30,
    120,
    'beginner',
    '{
    "subtitle": "Moduł 1: Liczby i Działania",
    "cards": [
            {
                "type": "intro",
                "title": "Wesele w liczbach",
                "description": "Na weselu goście rodziców panny młodej stanowili ⅔, a rodziców pana młodego ⅛ zaproszonych osób. Pozostałych gości zaprosiła młoda para. **Kto zaprosił najwięcej osób?** W tej lekcji nauczysz się rozwiązywać takie zadania!"
            },
            {
                "type": "concept",
                "title": "Dodawanie ułamków zwykłych",
                "content": "**Przypominamy sobie, jak dodajemy i odejmujemy ułamki zwykłe.**\\n\\nDodając lub odejmując ułamki zwykłe, **sprowadzamy je do wspólnego mianownika**:\\n\\n$$\\frac{1}{2} + \\frac{1}{5} = \\frac{5}{10} + \\frac{2}{10} = \\frac{7}{10}$$\\n\\n$$4\\frac{1}{3} - \\frac{2}{3} = 3\\frac{4}{3} - \\frac{2}{3} = 3\\frac{2}{3}$$\\n\\nPamiętaj:\\n1. Znajdź wspólny mianownik\\n2. Rozszerz ułamki\\n3. Dodaj/odejmij liczniki\\n4. Zostaw ten sam mianownik"
            },
            {
                "type": "input",
                "title": "Proste dodawanie",
                "question": "Oblicz: $\\frac{3}{5} + \\frac{1}{5}$",
                "correctAnswer": "0.8",
                "alternateAnswers": ["4/5"],
                "placeholder": "np. 0.8 lub 4/5",
                "explanation": "Ułamki mają już wspólny mianownik 5, więc: $\\frac{3}{5} + \\frac{1}{5} = \\frac{4}{5} = 0,8$"
            },
            {
                "type": "fill-gap",
                "title": "Wspólny mianownik",
                "parts": [
                    "Oblicz: $\\frac{1}{2} + \\frac{1}{3}$\\n\\nWspólny mianownik to ",
                    {
                        "id": "gap1",
                        "correctExact": 6,
                        "placeholder": "?"
                    },
                    "\\n\\nPo rozszerzeniu: $\\frac{",
                    {
                        "id": "gap2",
                        "correctExact": 3,
                        "placeholder": "?"
                    },
                    "}{6} + \\frac{",
                    {
                        "id": "gap3",
                        "correctExact": 2,
                        "placeholder": "?"
                    },
                    "}{6} = \\frac{",
                    {
                        "id": "gap4",
                        "correctExact": 5,
                        "placeholder": "?"
                    },
                    "}{6}$"
                ],
                "explanation": "Wspólny mianownik dla 2 i 3 to 6. Rozszerzamy: $\\frac{1·3}{2·3} + \\frac{1·2}{3·2} = \\frac{3}{6} + \\frac{2}{6} = \\frac{5}{6}$"
            },
            {
                "type": "concept",
                "title": "Dodawanie liczb dziesiętnych",
                "content": "**Dodając lub odejmując ułamki dziesiętne**, postępujemy jak przy liczbach naturalnych.\\n\\nProste rachunki wykonujemy w pamięci:\\n$$0,9 + 0,4 = 1,3$$\\n$$0,54 - 0,2 = 0,54 - 0,20 = 0,34$$\\n\\nBardziej skomplikowane - sposobem pisemnym:\\n$$14,065 + 2,7 = 16,765$$\\n\\n**Pamiętaj:** Przecinki muszą być pod sobą!"
            },
            {
                "type": "input",
                "title": "Oblicz w pamięci",
                "question": "Oblicz: $1,2 + 2,15$",
                "correctAnswer": "3.35",
                "placeholder": "np. 3.35",
                "explanation": "$1,20 + 2,15 = 3,35$ (dopisujemy zero, żeby mieć tyle samo cyfr po przecinku)"
            },
            {
                "type": "concept",
                "title": "Zamiana postaci ułamków",
                "content": "**Przy dodawaniu i odejmowaniu liczb wymiernych staramy się zawsze przedstawić ułamki w tej samej postaci** — ułamka zwykłego ALBO dziesiętnego.\\n\\n**Przykłady zamiany:**\\n$$\\frac{1}{2} + 0,75 = 0,5 + 0,75 = 1,25$$\\n\\n$$\\frac{2}{5} + 0,3 = \\frac{2}{5} + \\frac{3}{10} = \\frac{4}{10} + \\frac{3}{10} = \\frac{7}{10}$$\\n\\n**Wskazówka:** Zamień wszystkie ułamki na tę postać, która jest łatwiejsza w obliczeniach!"
            },
            {
                "type": "true-false",
                "title": "Sprawdź obliczenia",
                "question": "Oceń, czy poniższe równości są prawdziwe:",
                "statements": [
                    {
                        "id": "s1",
                        "text": "$\\frac{1}{2} + 0,5 = 1$",
                        "isTrue": true,
                        "explanation": "Tak! $\\frac{1}{2} = 0,5$, więc $0,5 + 0,5 = 1,0$"
                    },
                    {
                        "id": "s2",
                        "text": "$0,75 - \\frac{1}{2} = 0,5$",
                        "isTrue": false,
                        "explanation": "Nie! $0,75 - 0,5 = 0,25$ (czyli $\\frac{1}{4}$)"
                    },
                    {
                        "id": "s3",
                        "text": "$1\\frac{1}{4} - 0,5 = 0,75$",
                        "isTrue": true,
                        "explanation": "Tak! $1,25 - 0,5 = 0,75$ (czyli $\\frac{3}{4}$)"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Zadanie z życia: Wesele",
                "instruction": "Rozwiąż zadanie krok po kroku.",
                "scenario": "**Na weselu:**\\n• Goście rodziców panny młodej: **$\\frac{2}{3}$ wszystkich gości**\\n• Goście rodziców pana młodego: **$\\frac{1}{8}$ wszystkich gości**\\n• Pozostali goście: zaproszeni przez młodą parę\\n\\n**Pytanie:** Kto zaprosił najwięcej osób?",
                "inputs": [
                    {
                        "label": "Jaką część gości zaprosiła młoda para? (podaj ułamek lub liczbę dziesiętną)",
                        "placeholder": "np. 5/24 lub 0.208",
                        "type": "text"
                    },
                    {
                        "label": "Która grupa była najliczniejsza? (wpisz: panna młoda / pan młody / para)",
                        "placeholder": "panna młoda, pan młody lub para",
                        "type": "text"
                    }
                ],
                "sampleAnswers": {
                    "title": "Rozwiązanie",
                    "answers": [
                        "Wspólny mianownik dla $\\frac{2}{3}$ i $\\frac{1}{8}$ to 24.",
                        "Rodzice panny młodej: $\\frac{2}{3} = \\frac{16}{24}$",
                        "Rodzice pana młodego: $\\frac{1}{8} = \\frac{3}{24}$",
                        "Młoda para: $1 - \\frac{16}{24} - \\frac{3}{24} = \\frac{24-16-3}{24} = \\frac{5}{24}$",
                        "**Odpowiedź:** Najwięcej gości ($\\frac{16}{24} = \\frac{2}{3}$) zaprosili rodzice panny młodej!"
                    ]
                }
            },
            {
                "type": "practice",
                "title": "Zadanie: Barka na Noteci",
                "instruction": "Rozwiąż zadanie praktyczne.",
                "scenario": "Barka na Noteci w spokojnej wodzie rozwija prędkość **1,4 m/s**. Prędkość nurtu rzeki wynosi **0,28 m/s**.\\n\\n**Oblicz:** Z jaką prędkością barka płynie:\\na) z prądem?\\nb) pod prąd?",
                "inputs": [
                    {
                        "label": "Prędkość z prądem (m/s)",
                        "placeholder": "np. 1.68",
                        "type": "text"
                    },
                    {
                        "label": "Prędkość pod prąd (m/s)",
                        "placeholder": "np. 1.12",
                        "type": "text"
                    }
                ],
                "sampleAnswers": {
                    "title": "Rozwiązanie",
                    "answers": [
                        "**Z prądem:** prędkość barki + prędkość nurtu",
                        "$1,4 + 0,28 = 1,68$ m/s",
                        "**Pod prąd:** prędkość barki - prędkość nurtu",
                        "$1,4 - 0,28 = 1,12$ m/s"
                    ]
                }
            },
            {
                "type": "curiosity",
                "title": "Ciekawostka: Ułamki proste",
                "content": "**Czy wiesz, że każdą liczbę wymierną można przedstawić jako sumę różnych ułamków prostych?**\\n\\n**Ułamkami prostymi** nazywamy ułamki o liczniku 1 i mianownikach będących liczbami naturalnymi: $\\frac{1}{2}, \\frac{1}{3}, \\frac{1}{4}, \\frac{1}{5}$ itd.\\n\\n**Przykład:**\\n$$\\frac{5}{6} = \\frac{1}{2} + \\frac{1}{3}$$\\n\\n$$\\frac{2}{3} = \\frac{1}{2} + \\frac{1}{6}$$\\n\\nStarożytni Egipcjanie zapisywali **wszystkie ułamki** w ten sposób!"
            },
            {
                "type": "matching",
                "title": "Dopasuj wyniki",
                "question": "Połącz działania z ich wynikami:",
                "pairs": [
                    {
                        "id": "p1",
                        "left": "$\\frac{1}{2} + \\frac{1}{4}$",
                        "right": "$\\frac{3}{4}$"
                    },
                    {
                        "id": "p2",
                        "left": "$1 - \\frac{2}{3}$",
                        "right": "$\\frac{1}{3}$"
                    },
                    {
                        "id": "p3",
                        "left": "$0,5 + 0,25$",
                        "right": "$0,75$"
                    },
                    {
                        "id": "p4",
                        "left": "$1,5 - \\frac{2}{3}$",
                        "right": "$\\frac{5}{6}$"
                    }
                ],
                "explanations": {
                    "p1": "$\\frac{1}{2} + \\frac{1}{4} = \\frac{2}{4} + \\frac{1}{4} = \\frac{3}{4}$",
                    "p2": "$1 - \\frac{2}{3} = \\frac{3}{3} - \\frac{2}{3} = \\frac{1}{3}$",
                    "p3": "$0,5 + 0,25 = 0,75$ (pół plus ćwierć to trzy czwarte)",
                    "p4": "$1,5 - \\frac{2}{3} = \\frac{3}{2} - \\frac{2}{3} = \\frac{9}{6} - \\frac{4}{6} = \\frac{5}{6}$"
                }
            },
            {
                "type": "quiz",
                "title": "Sprawdź, czy umiesz",
                "questions": [
                    {
                        "question": "Wynikiem działania $4\\frac{1}{2} - 2,5$ jest:",
                        "options": [
                            "$2\\frac{2}{3}$",
                            "$1\\frac{1}{5}$",
                            "$2$",
                            "$1\\frac{19}{20}$"
                        ],
                        "correctAnswer": 2,
                        "explanation": "$4\\frac{1}{2} = 4,5$, więc $4,5 - 2,5 = 2,0 = 2$"
                    },
                    {
                        "question": "Która suma jest większa: $\\frac{1}{3} + \\frac{1}{4}$ czy $0,5$?",
                        "options": [
                            "$\\frac{1}{3} + \\frac{1}{4}$",
                            "$0,5$",
                            "Są równe"
                        ],
                        "correctAnswer": 0,
                        "explanation": "$\\frac{1}{3} + \\frac{1}{4} = \\frac{4}{12} + \\frac{3}{12} = \\frac{7}{12} \\approx 0,583$ co jest większe od $0,5$"
                    },
                    {
                        "question": "Oblicz: $1 - \\frac{6}{7}$",
                        "options": [
                            "$\\frac{1}{7}$",
                            "$\\frac{5}{7}$",
                            "$\\frac{6}{7}$",
                            "$\\frac{2}{7}$"
                        ],
                        "correctAnswer": 0,
                        "explanation": "$1 - \\frac{6}{7} = \\frac{7}{7} - \\frac{6}{7} = \\frac{1}{7}$"
                    }
                ]
            },
            {
                "type": "test",
                "title": "Test końcowy",
                "questions": [
                    {
                        "question": "Oblicz: $\\frac{3}{4} + \\frac{1}{8}$",
                        "options": [
                            "$\\frac{4}{12}$",
                            "$\\frac{7}{8}$",
                            "$\\frac{5}{8}$",
                            "$1$"
                        ],
                        "correctAnswer": 1,
                        "explanation": "$\\frac{3}{4} = \\frac{6}{8}$, więc $\\frac{6}{8} + \\frac{1}{8} = \\frac{7}{8}$"
                    },
                    {
                        "question": "Oblicz: $2,5 + 1,75$",
                        "options": [
                            "$3,25$",
                            "$4,25$",
                            "$4,75$",
                            "$3,75$"
                        ],
                        "correctAnswer": 1,
                        "explanation": "$2,5 + 1,75 = 2,50 + 1,75 = 4,25$"
                    },
                    {
                        "question": "Oblicz: $5 - 2\\frac{3}{5}$",
                        "options": [
                            "$2\\frac{2}{5}$",
                            "$3\\frac{2}{5}$",
                            "$2\\frac{3}{5}$",
                            "$3\\frac{3}{5}$"
                        ],
                        "correctAnswer": 0,
                        "explanation": "$5 - 2\\frac{3}{5} = 4\\frac{5}{5} - 2\\frac{3}{5} = 2\\frac{2}{5}$"
                    },
                    {
                        "question": "Jaką część pizzy zostało, jeśli zjedliśmy $\\frac{2}{8}$?",
                        "options": [
                            "$\\frac{2}{8}$",
                            "$\\frac{3}{4}$",
                            "$\\frac{1}{4}$",
                            "$\\frac{1}{8}$"
                        ],
                        "correctAnswer": 1,
                        "explanation": "Zostało $1 - \\frac{2}{8} = \\frac{8}{8} - \\frac{2}{8} = \\frac{6}{8} = \\frac{3}{4}$ pizzy"
                    },
                    {
                        "question": "Oblicz: $1,2 - \\frac{1}{2}$",
                        "options": [
                            "$0,7$",
                            "$0,8$",
                            "$0,6$",
                            "$1,1$"
                        ],
                        "correctAnswer": 0,
                        "explanation": "$1,2 - 0,5 = 0,7$ (bo $\\frac{1}{2} = 0,5$)"
                    }
                ]
            },
            {
                "type": "summary",
                "title": "Podsumowanie",
                "recap": [
                    "Dodając lub odejmując ułamki zwykłe, **sprowadzamy je do wspólnego mianownika**.",
                    "Ułamki dziesiętne dodajemy i odejmujemy jak liczby naturalne, ustawiając **przecinki pod sobą**.",
                    "Przy obliczeniach mieszanych (ułamki + dziesiętne) **zamieniamy wszystko na jedną postać**.",
                    "Każdą liczbę wymierną można przedstawić jako sumę **ułamków prostych** (o liczniku 1)."
                ],
                "badge": {
                    "title": "Mistrz Dodawania",
                    "xp": 120
                },
                "nextSteps": "W następnej lekcji nauczysz się **mnożyć i dzielić** liczby wymierne!"
            }
        ]
    }'::jsonb,
    'd290f1ee-6c54-4b01-90e6-d701748f0851'
) ON CONFLICT (lesson_id) DO UPDATE SET
    content = EXCLUDED.content,
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    duration_minutes = EXCLUDED.duration_minutes,
    xp_reward = EXCLUDED.xp_reward,
    difficulty = EXCLUDED.difficulty,
    module_id = EXCLUDED.module_id;
