-- Insert "Kolejność działań i nawiasy" Lesson
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
    'math-g7-l6',
    'Kolejność działań i nawiasy',
    'Naucz się poprawnie wykonywać złożone obliczenia. Poznaj zasady kolejności działań i dowiedz się, jak prawidłowo używać nawiasów.',
    30,
    120,
    'beginner',
    '{
    "subtitle": "Moduł 1: Liczby i Działania",
    "cards": [
        {
            "type": "intro",
            "title": "Co najpierw?",
            "description": "Oblicz: $2 + 3 \\times 4$. Czy to $20$ czy $14$? W tej lekcji odkryjesz, dlaczego kolejność działań ma znaczenie i jak nawiasy zmieniają wszystko!"
        },
        {
            "type": "concept",
            "title": "Zasada pierwsza: Mnożenie i dzielenie przed dodawaniem i odejmowaniem",
            "content": "Gdy w wyrażeniu występują różne działania, wykonujemy je w **określonej kolejności**:\\n\\n**1. NAWIASY** (jeśli są)\\n**2. MNOŻENIE i DZIELENIE** (od lewej do prawej)\\n**3. DODAWANIE i ODEJMOWANIE** (od lewej do prawej)\\n\\n**Przykład:**\\n$$2 + 3 \\times 4 = 2 + 12 = 14$$\\n\\n**NIE:** $2 + 3 = 5$, potem $5 \\times 4 = 20$ ❌\\n**TAK:** $3 \\times 4 = 12$, potem $2 + 12 = 14$ ✅"
        },
        {
            "type": "true-false",
            "title": "Sprawdź kolejność",
            "question": "Oceń, czy podane obliczenia są prawidłowe:",
            "statements": [
                {
                    "id": "s1",
                    "text": "$5 + 2 \\times 3 = 21$",
                    "isTrue": false,
                    "explanation": "Błąd! Mnożenie przed dodawaniem: $5 + 2 \\times 3 = 5 + 6 = 11$"
                },
                {
                    "id": "s2",
                    "text": "$8 - 4 \\div 2 = 6$",
                    "isTrue": true,
                    "explanation": "Poprawnie! Dzielenie przed odejmowaniem: $8 - 4 \\div 2 = 8 - 2 = 6$"
                },
                {
                    "id": "s3",
                    "text": "$10 \\div 2 + 3 = 8$",
                    "isTrue": true,
                    "explanation": "Poprawnie! Dzielenie przed dodawaniem: $10 \\div 2 + 3 = 5 + 3 = 8$"
                }
            ]
        },
        {
            "type": "input",
            "title": "Ćwiczenie: Bez nawiasów",
            "question": "Oblicz: $6 + 4 \\times 5$",
            "correctAnswer": "26",
            "alternateAnswers": ["26", "26,0", "26.0"],
            "placeholder": "wpisz wynik",
            "explanation": "Mnożenie najpierw: $6 + 4 \\times 5 = 6 + 20 = 26$"
        },
        {
            "type": "concept",
            "title": "Potęga nawiasów",
            "content": "**Nawiasy zmieniają kolejność!**\\n\\nNawiasy **()** mówią nam: ''Zrób to najpierw!''. Zawsze wykonujemy działania **w nawiasach** przed wszystkimi innymi.\\n\\n**Przykład 1:**\\n$$(2 + 3) \\times 4 = 5 \\times 4 = 20$$\\n\\n**Przykład 2:**\\n$$12 \\div (4 - 1) = 12 \\div 3 = 4$$\\n\\n**Przykład 3 (zagnieżdżone nawiasy):**\\n$$2 \\times ((5 + 3) - 2) = 2 \\times (8 - 2) = 2 \\times 6 = 12$$"
        },
        {
            "type": "fill-gap",
            "title": "Krok po kroku",
            "parts": [
                "Obliczmy: $(7 - 3) \\times 2 + 5$\\n\\nKrok 1: Nawias: $7 - 3 = $",
                {
                    "id": "gap1",
                    "correctExact": 4,
                    "placeholder": "?"
                },
                "\\n\\nKrok 2: Mnożenie: $4 \\times 2 = $",
                {
                    "id": "gap2",
                    "correctExact": 8,
                    "placeholder": "?"
                },
                "\\n\\nKrok 3: Dodawanie: $8 + 5 = $",
                {
                    "id": "gap3",
                    "correctExact": 13,
                    "placeholder": "?"
                }
            ],
            "explanation": "$(7 - 3) \\times 2 + 5 = 4 \\times 2 + 5 = 8 + 5 = 13$"
        },
        {
            "type": "input",
            "title": "Ćwiczenie: Z nawiasami",
            "question": "Oblicz: $(8 + 2) \\div 5$",
            "correctAnswer": "2",
            "alternateAnswers": ["2", "2,0", "2.0"],
            "placeholder": "wpisz wynik",
            "explanation": "Najpierw nawias: $(8 + 2) \\div 5 = 10 \\div 5 = 2$"
        },
        {
            "type": "comparison",
            "title": "Z nawiasem czy bez?",
            "expression": {
                "left": "$2 + 3 \\times 4$",
                "right": "$(2 + 3) \\times 4$",
                "relationship": "<"
            },
            "explanation": "Bez nawiasu: $2 + 3 \\times 4 = 2 + 12 = 14$. Z nawiasem: $(2 + 3) \\times 4 = 5 \\times 4 = 20$. Więc $14 < 20$."
        },
        {
            "type": "concept",
            "title": "Działania tego samego rzędu",
            "content": "Gdy mamy tylko **mnożenie i dzielenie** ALBO tylko **dodawanie i odejmowanie**, wykonujemy je **od lewej do prawej**.\\n\\n**Przykład 1:**\\n$$20 \\div 4 \\times 5 = 5 \\times 5 = 25$$\\n\\n**Przykład 2:**\\n$$15 - 7 + 3 = 8 + 3 = 11$$\\n\\n**UWAGA:** NIE rób tak: $15 - (7 + 3) = 15 - 10 = 5$ ❌\\n\\nDziałamy od **lewej do prawej**!"
        },
        {
            "type": "matching",
            "title": "Dopasuj wyniki",
            "question": "Połącz wyrażenia z ich prawidłowymi wynikami:",
            "pairs": [
                {
                    "id": "p1",
                    "left": "$10 - 3 + 2$",
                    "right": "$9$"
                },
                {
                    "id": "p2",
                    "left": "$10 - (3 + 2)$",
                    "right": "$5$"
                },
                {
                    "id": "p3",
                    "left": "$12 \\div 3 \\times 2$",
                    "right": "$8$"
                },
                {
                    "id": "p4",
                    "left": "$12 \\div (3 \\times 2)$",
                    "right": "$2$"
                }
            ],
            "explanations": {
                "p1": "Od lewej: $10 - 3 = 7$, potem $7 + 2 = 9$",
                "p2": "Nawias najpierw: $10 - 5 = 5$",
                "p3": "Od lewej: $12 \\div 3 = 4$, potem $4 \\times 2 = 8$",
                "p4": "Nawias najpierw: $12 \\div 6 = 2$"
            }
        },
        {
            "type": "input",
            "title": "Ćwiczenie: Od lewej do prawej",
            "question": "Oblicz: $24 \\div 6 \\times 2$",
            "correctAnswer": "8",
            "alternateAnswers": ["8", "8,0", "8.0"],
            "placeholder": "wpisz wynik",
            "explanation": "Od lewej: $24 \\div 6 = 4$, potem $4 \\times 2 = 8$"
        },
        {
            "type": "curiosity",
            "title": "Skąd się wzięły nawiasy?",
            "content": "Pierwsze nawiasy w matematyce pojawiły się w **XVI wieku!**\\n\\n- **Rafael Bombelli** (1572) używał poziomej kreski nad wyrażeniem\\n- **1608:** Holenderski matematyk wprowadził okrągłe nawiasy **( )**\\n- **1629:** Albert Girard wprowadził nawiasy kwadratowe **[ ]**\\n- **1629:** Podobny okres - nawiasy klamrowe **{ }**\\n\\nDzięki nawiąsom możemy zapisywać skomplikowane wzory w sposób jednoznaczny!"
        },
        {
            "type": "practice",
            "title": "Zadanie: Zakupy",
            "instruction": "Rozwiąż zadanie praktyczne.",
            "scenario": "Mama kupiła **3 bułki** po **1,20 zł** każda i **2 mleka** po **3,50 zł** każde. Zapłaciła banknotem **20 zł**. Ile złotych otrzymała reszty?",
            "inputs": [
                {
                    "label": "Koszt bułek (zł)",
                    "placeholder": "np. 3.60",
                    "type": "text"
                },
                {
                    "label": "Koszt mleka (zł)",
                    "placeholder": "np. 7.00",
                    "type": "text"
                },
                {
                    "label": "Reszta (zł)",
                    "placeholder": "np. 9.40",
                    "type": "text"
                }
            ],
            "sampleAnswers": {
                "title": "Rozwiązanie",
                "answers": [
                    "**Koszt bułek:** $3 \\times 1,20 = 3,60$ zł",
                    "**Koszt mleka:** $2 \\times 3,50 = 7,00$ zł",
                    "**Całkowity koszt:** $3,60 + 7,00 = 10,60$ zł",
                    "**Reszta:** $20 - 10,60 = 9,40$ zł",
                    "\\nZapisując to jednym wyrażeniem:\\n$$20 - (3 \\times 1,20 + 2 \\times 3,50) = 20 - (3,60 + 7,00) = 20 - 10,60 = 9,40$$"
                ]
            }
        },
        {
            "type": "fill-gap",
            "title": "Wyrażenia złożone",
            "parts": [
                "Oblicz: $100 - 2 \\times (15 + 5)$\\n\\nKrok 1: Nawias wewnętrzny: $15 + 5 = $",
                {
                    "id": "gap1",
                    "correctExact": 20,
                    "placeholder": "?"
                },
                "\\n\\nKrok 2: Mnożenie: $2 \\times 20 = $",
                {
                    "id": "gap2",
                    "correctExact": 40,
                    "placeholder": "?"
                },
                "\\n\\nKrok 3: Odejmowanie: $100 - 40 = $",
                {
                    "id": "gap3",
                    "correctExact": 60,
                    "placeholder": "?"
                }
            ],
            "explanation": "Kolejność: nawiasy → mnożenie → odejmowanie"
        },
        {
            "type": "practice",
            "title": "Zadanie: Prędkość średnia",
            "instruction": "Zastosuj kolejność działań w fizyce.",
            "scenario": "Jaś przejechał rowerem **10 km** w czasie **30 minut**, a potem **15 km** w czasie **45 minut**. Oblicz jego **średnią prędkość** w km/h.\\n\\n**Wzór:** Prędkość średnia = Całkowity dystans ÷ Całkowity czas",
            "inputs": [
                {
                    "label": "Całkowity dystans (km)",
                    "placeholder": "np. 25",
                    "type": "text"
                },
                {
                    "label": "Całkowity czas (h)",
                    "placeholder": "np. 1.25",
                    "type": "text"
                },
                {
                    "label": "Średnia prędkość (km/h)",
                    "placeholder": "np. 20",
                    "type": "text"
                }
            ],
            "sampleAnswers": {
                "title": "Rozwiązanie",
                "answers": [
                    "**Całkowity dystans:** $10 + 15 = 25$ km",
                    "**Całkowity czas:** $30 + 45 = 75$ min $= 75 \\div 60 = 1,25$ h",
                    "**Średnia prędkość:** $25 \\div 1,25 = 20$ km/h",
                    "\\nJednym wyrażeniem:\\n$$\\frac{10 + 15}{(30 + 45) \\div 60} = \\frac{25}{75 \\div 60} = \\frac{25}{1,25} = 20$$"
                ]
            }
        },
        {
            "type": "quiz",
            "title": "Sprawdź, czy umiesz",
            "questions": [
                {
                    "question": "Ile wynosi $5 + 3 \\times 2$?",
                    "options": [
                        "$16$",
                        "$11$",
                        "$13$",
                        "$10$"
                    ],
                    "correctAnswer": 1,
                    "explanation": "Mnożenie przed dodawaniem: $5 + 3 \\times 2 = 5 + 6 = 11$"
                },
                {
                    "question": "Ile wynosi $(8 - 3) \\times 4$?",
                    "options": [
                        "$32$",
                        "$20$",
                        "$17$",
                        "$5$"
                    ],
                    "correctAnswer": 1,
                    "explanation": "Nawias najpierw: $(8 - 3) \\times 4 = 5 \\times 4 = 20$"
                },
                {
                    "question": "Które wyrażenie daje wynik $10$?",
                    "options": [
                        "$2 + 4 \\times 2$",
                        "$(2 + 4) \\times 2$",
                        "$20 \\div 2 + 0$",
                        "$15 - 10 \\div 2$"
                    ],
                    "correctAnswer": 2,
                    "explanation": "$20 \\div 2 + 0 = 10 + 0 = 10$. A: $2 + 8 = 10$ ✅ także daje 10! Ale C jest prostsze."
                },
                {
                    "question": "Ile wynosi $18 \\div 3 \\times 2$?",
                    "options": [
                        "$3$",
                        "$12$",
                        "$6$",
                        "$9$"
                    ],
                    "correctAnswer": 1,
                    "explanation": "Od lewej do prawej: $18 \\div 3 = 6$, potem $6 \\times 2 = 12$"
                }
            ]
        },
        {
            "type": "test",
            "title": "Test końcowy",
            "questions": [
                {
                    "question": "Oblicz: $7 + 2 \\times 5$",
                    "options": [
                        "$45$",
                        "$17$",
                        "$14$",
                        "$70$"
                    ],
                    "correctAnswer": 1,
                    "explanation": "$7 + 2 \\times 5 = 7 + 10 = 17$"
                },
                {
                    "question": "Oblicz: $(10 - 4) \\times 3$",
                    "options": [
                        "$18$",
                        "$22$",
                        "$-2$",
                        "$30$"
                    ],
                    "correctAnswer": 0,
                    "explanation": "$(10 - 4) \\times 3 = 6 \\times 3 = 18$"
                },
                {
                    "question": "Oblicz: $20 \\div 4 + 3 \\times 2$",
                    "options": [
                        "$11$",
                        "$5$",
                        "$2,5$",
                        "$16$"
                    ],
                    "correctAnswer": 0,
                    "explanation": "$20 \\div 4 = 5$, $3 \\times 2 = 6$, więc $5 + 6 = 11$"
                },
                {
                    "question": "Oblicz: $50 - 3 \\times (4 + 6)$",
                    "options": [
                        "$470$",
                        "$20$",
                        "$440$",
                        "$500$"
                    ],
                    "correctAnswer": 1,
                    "explanation": "Nawias: $4 + 6 = 10$. Mnożenie: $3 \\times 10 = 30$. Odejmowanie: $50 - 30 = 20$"
                },
                {
                    "question": "Które wyrażenie NIE równa się $8$?",
                    "options": [
                        "$2 \\times 4$",
                        "$16 \\div 2$",
                        "$10 - 2$",
                        "$3 + 2 \\times 2$"
                    ],
                    "correctAnswer": 3,
                    "explanation": "$3 + 2 \\times 2 = 3 + 4 = 7 \\neq 8$. Pozostałe wszystkie równają się 8."
                }
            ]
        },
        {
            "type": "summary",
            "title": "Podsumowanie",
            "recap": [
                "**Kolejność działań:**\\n1. NAWIASY\\n2. MNOŻENIE i DZIELENIE (od lewej do prawej)\\n3. DODAWANIE i ODEJMOWANIE (od lewej do prawej)",
                "Nawiasy **()** zmieniają kolejność wykonywania działań",
                "Gdy mamy tylko mnożenie/dzielenie lub tylko dodawanie/odejmowanie, działamy **od lewej do prawej**",
                "W wyrażeniach złożonych zawsze najpierw rozwiązuj **nawiasy wewnętrzne**"
            ],
            "badge": {
                "title": "Mistrz Kolejności",
                "xp": 120
            },
            "nextSteps": "W następnej lekcji poznasz **potęgi** i dowiesz się, jak jeszcze bardziej uprościć zapisywanie powtarzających się mnożeń!"
        }
    ]
}'::jsonb,
    'd290f1ee-6c54-4b01-90e6-d701748f0851'
) ON CONFLICT (lesson_id) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    duration_minutes = EXCLUDED.duration_minutes,
    xp_reward = EXCLUDED.xp_reward,
    difficulty = EXCLUDED.difficulty,
    content = EXCLUDED.content,
    module_id = EXCLUDED.module_id;
