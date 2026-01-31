-- Insert "Działania na liczbach dodatnich i ujemnych" Lesson
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
    'math-g7-l7',
    'Działania na liczbach dodatnich i ujemnych',
    'Poznaj reguły wykonywania działań na liczbach ujemnych. Dowiedz się, dlaczego "minus razy minus daje plus" i opanuj sztukę liczenia z liczbami o różnych znakach.',
    35,
    140,
    'beginner',
    '{
    "subtitle": "Moduł 1: Liczby i Działania",
    "cards": [
        {
            "type": "intro",
            "title": "Liczby ujemne - kontrowersyjne przez wieki!",
            "description": "Przez setki lat matematycy nie akceptowali liczb ujemnych, uważając je za ''dziwne'' i ''abstrakcyjne''. Dopiero w XVIII wieku uznano je w pełni. Dziś nauczysz się z nimi pewnie działać!"
        },
        {
            "type": "flashcards",
            "title": "Gdzie spotkasz liczby ujemne?",
            "cards": [
                {
                    "front": "🌡️ **Temperatura i pogoda**\\n\\nDziś w nocy było **-5°C**, w dzień temperatura wzrosła o **7°C**. Jaka była temperatura w dzień?",
                    "back": "**Rozwiązanie:** $-5 + 7 = 2$ °C\\n\\nWzrost temperatury = dodawanie!"
                },
                {
                    "front": "💰 **Finanse i oszczędności**\\n\\nMasz dług **-20 zł** u kolegi, dostajesz **50 zł** od rodziców. Ile masz teraz?",
                    "back": "**Rozwiązanie:** $-20 + 50 = 30$ zł\\n\\nDług to liczba ujemna, wpływ to dodawanie!"
                },
                {
                    "front": "🎮 **Punkty w grach**\\n\\nZaczynasz z **100 punktami**, dostajesz karę **-30 punktów**, potem bonus **+50**. Jaki masz wynik?",
                    "back": "**Rozwiązanie:** $100 - 30 + 50 = 120$ punktów\\n\\nKary i bonusy = dodawanie i odejmowanie!"
                },
                {
                    "front": "🏔️ **Geografia i wysokości**\\n\\nMorze Martwe leży na wysokości **-430 m**, lecisz samolotem na **3000 m**. O ile metrów się wzniosłeś?",
                    "back": "**Rozwiązanie:** $3000 - (-430) = 3430$ m\\n\\nWzrost wysokości = odejmowanie liczby ujemnej!"
                }
            ]
        },
        {
            "type": "concept",
            "title": "Przypomnienie: Liczby przeciwne",
            "content": "Każda liczba ma swoją **liczbę przeciwną** - leżącą po drugiej stronie zera na osi liczbowej:\\n\\n- Liczba przeciwna do $5$ to $-5$\\n- Liczba przeciwna do $-3$ to $3$\\n- Liczba przeciwna do $0$ to $0$\\n\\n**Ważne:** Suma liczby i jej liczby przeciwnej zawsze wynosi $0$:\\n$$5 + (-5) = 0$$\\n$$-3 + 3 = 0$$"
        },
        {
            "type": "number-line",
            "title": "Zaznacz na osi",
            "question": "Zaznacz liczbę $-7$ na osi liczbowej.",
            "min": -10,
            "max": 10,
            "step": 1,
            "correctValue": -7,
            "tolerance": 0.3,
            "explanation": "Liczba $-7$ leży 7 jednostek na lewo od zera.",
            "showTooltip": false,
            "labelFrequency": 5
        },
        {
            "type": "concept",
            "title": "Dodawanie liczb: Reguły",
            "content": "**REGUŁA 1: Liczby o tym samym znaku**\\n\\nDodaj ich wartości bezwzględne i zachowaj znak:\\n- $7 + 12 = 19$\\n- $(-7) + (-12) = -19$\\n\\n**REGUŁA 2: Liczby o różnych znakach**\\n\\nOdejmij mniejszą wartość od większej i weź znak tej, która ma większą wartość bezwzględną:\\n- $7 + (-12) = -5$ (bo $12 > 7$, znak od $-12$)\\n- $(-7) + 12 = 5$ (bo $12 > 7$, znak od $12$)"
        },
        {
            "type": "fill-gap",
            "title": "Krok po kroku: Dodawanie",
            "parts": [
                "Obliczmy: $-7 + 12$\\n\\nKrok 1: Która liczba ma większą wartość bezwzględną? $|-7| = 7$, $|12| = 12$, więc większa to ",
                {
                    "id": "gap1",
                    "correctExact": 12,
                    "placeholder": "?"
                },
                "\\n\\nKrok 2: Odejmij mniejszą od większej: $12 - 7 = $",
                {
                    "id": "gap2",
                    "correctExact": 5,
                    "placeholder": "?"
                },
                "\\n\\nKrok 3: Weź znak liczby o większej wartości. Wynik to: ",
                {
                    "id": "gap3",
                    "correctExact": 5,
                    "placeholder": "?"
                }
            ],
            "explanation": "$-7 + 12 = 5$ (znak dodatni, bo $12 > 7$)"
        },
        {
            "type": "input",
            "title": "Ćwiczenie: Dodawanie",
            "question": "Oblicz: $-33 + 44$",
            "correctAnswer": "11",
            "alternateAnswers": ["11", "11,0", "11.0"],
            "placeholder": "wpisz wynik",
            "explanation": "Różne znaki: $44 - 33 = 11$, znak dodatni (bo $44 > 33$)"
        },
        {
            "type": "concept",
            "title": "Odejmowanie = Dodawanie liczby przeciwnej",
            "content": "**Każde odejmowanie można zamienić na dodawanie!**\\n\\nZamiast odejmować liczbę $b$, dodaj jej liczbę przeciwną $-b$:\\n\\n$$a - b = a + (-b)$$\\n\\n**Przykłady:**\\n- $7 - 12 = 7 + (-12) = -5$\\n- $-5 - 8 = -5 + (-8) = -13$\\n- $-30 - (-50) = -30 + 50 = 20$ ✨\\n- $16 - 60 = 16 + (-60) = -44$"
        },
        {
            "type": "true-false",
            "title": "Sprawdź odejmowanie",
            "question": "Oceń, czy podane obliczenia są prawidłowe:",
            "statements": [
                {
                    "id": "s1",
                    "text": "$-30 - (-50) = 20$",
                    "isTrue": true,
                    "explanation": "Poprawnie! $-30 - (-50) = -30 + 50 = 20$"
                },
                {
                    "id": "s2",
                    "text": "$-15 - 25 = 10$",
                    "isTrue": false,
                    "explanation": "Błąd! $-15 - 25 = -15 + (-25) = -40$"
                },
                {
                    "id": "s3",
                    "text": "$5,5 - (-0,8) = 6,3$",
                    "isTrue": true,
                    "explanation": "Poprawnie! $5,5 - (-0,8) = 5,5 + 0,8 = 6,3$"
                }
            ]
        },
        {
            "type": "concept",
            "title": "Mnożenie i dzielenie: Zasady znaków",
            "content": "**Reguły są proste!**\\n\\n**1. Te same znaki → wynik DODATNI (+)**\\n- $(+) \\times (+) = (+)$ np. $15 \\times 3 = 45$\\n- $(−) \\times (−) = (+)$ np. $(-15) \\times (-3) = 45$ ✨\\n- $(+) \\div (+) = (+)$ np. $51 \\div 3 = 17$\\n- $(−) \\div (−) = (+)$ np. $(-51) \\div (-3) = 17$ ✨\\n\\n**2. Różne znaki → wynik UJEMNY (−)**\\n- $(+) \\times (−) = (−)$ np. $15 \\times (-3) = -45$\\n- $(−) \\times (+) = (−)$ np. $(-15) \\times 3 = -45$\\n- $(+) \\div (−) = (−)$ np. $51 \\div (-3) = -17$\\n- $(−) \\div (+) = (−)$ np. $(-51) \\div 3 = -17$"
        },
        {
            "type": "matching",
            "title": "Dopasuj wyniki",
            "question": "Połącz wyrażenia z ich prawidłowymi wynikami:",
            "pairs": [
                {
                    "id": "p1",
                    "left": "$(-15) \\times (-3)$",
                    "right": "$45$"
                },
                {
                    "id": "p2",
                    "left": "$15 \\times (-3)$",
                    "right": "$-45$"
                },
                {
                    "id": "p3",
                    "left": "$(-51) \\div (-3)$",
                    "right": "$17$"
                },
                {
                    "id": "p4",
                    "left": "$51 \\div (-3)$",
                    "right": "$-17$"
                }
            ],
            "explanations": {
                "p1": "Te same znaki (−)(−) = wynik dodatni!",
                "p2": "Różne znaki (+)(−) = wynik ujemny",
                "p3": "Te same znaki (−)(−) = wynik dodatni!",
                "p4": "Różne znaki (+)(−) = wynik ujemny"
            }
        },
        {
            "type": "input",
            "title": "Ćwiczenie: Mnożenie",
            "question": "Oblicz: $(-2,5) \\times 2$",
            "correctAnswer": "-5",
            "alternateAnswers": ["-5", "-5,0", "-5.0"],
            "placeholder": "wpisz wynik",
            "explanation": "Różne znaki → wynik ujemny: $(-2,5) \\times 2 = -5$"
        },
        {
            "type": "curiosity",
            "title": "Z historii: Długa droga do akceptacji",
            "content": "**II w. n.e.** - Chińczycy wynaleźli liczby ujemne (do księgowości - długi!)\\n\\n**VII w. n.e.** - Hinduscy matematycy sformułowali reguły działań na liczbach ujemnych\\n\\n**XII w.** - Liczby ujemne pojawiły się w Europie, ale... nikt im nie ufał!\\n\\n**XVIII w.** - Dopiero w **połowie XVIII wieku** matematycy w pełni zaakceptowali liczby ujemne\\n\\n**Ciekawostka:** Wielcy matematycy jak **Blaise Pascal** uważali liczby ujemne za ''nonsens''!"
        },
        {
            "type": "sign-predictor",
            "title": "Przewidź znak wyniku",
            "question": "Nie licząc dokładnego wyniku, określ czy wynik będzie dodatni, ujemny czy zero:",
            "expression": "$-3\\frac{1}{3} - (-4 \\frac{1}{15})$",
            "correctSign": "positive",
            "explanation": "Odejmujemy liczbę ujemną, więc w rzeczywistości **dodajemy** liczbę dodatnią: $-3\\frac{1}{3} + 4 \\frac{1}{15}$. Ponieważ $4 \\frac{1}{15} > 3\\frac{1}{3}$, wynik będzie **dodatni**!"
        },
        {
            "type": "sign-predictor",
            "title": "Przewidź znak: Mnożenie",
            "question": "Jaki znak będzie miał wynik?",
            "expression": "$(-5) \\times (-7) \\times 2$",
            "correctSign": "positive",
            "explanation": "$(−) \\times (−) = (+)$, czyli $(-5) \\times (-7) = 35$. Potem $35 \\times 2 = 70$ (dodatnie!)"
        },
        {
            "type": "practice",
            "title": "Zadanie: Temperatury",
            "instruction": "Rozwiąż zadanie praktyczne.",
            "scenario": "W Warszawie w nocy temperatura wynosiła **-5°C**. W ciągu dnia temperatura **wzrosła o 7°C**. Jaka była temperatura w dzień?\\n\\nWieczorem temperatura **spadła o 4°C** w stosunku do temperatury dziennej. Jaka była temperatura wieczorem?",
            "inputs": [
                {
                    "label": "Temperatura w dzień (°C)",
                    "placeholder": "wpisz liczbę",
                    "type": "text"
                },
                {
                    "label": "Temperatura wieczorem (°C)",
                    "placeholder": "wpisz liczbę",
                    "type": "text"
                }
            ],
            "sampleAnswers": {
                "title": "Rozwiązanie",
                "answers": [
                    "**W dzień:** $-5 + 7 = 2°C$",
                    "**Wieczorem:** $2 - 4 = -2°C$",
                    "\\nZapamietaj: Wzrost to dodawanie, spadek to odejmowanie!"
                ]
            }
        },
        {
            "type": "fill-gap",
            "title": "Złożone wyrażenie",
            "parts": [
                "Oblicz: $5 - (-12) - 7 + 14$\\n\\nKrok 1: Zamień odejmowanie ujemnej: $5 + 12 - 7 + 14$\\n\\nKrok 2: Od lewej: $5 + 12 = $",
                {
                    "id": "gap1",
                    "correctExact": 17,
                    "placeholder": "?"
                },
                "\\n\\nKrok 3: Dalej: $17 - 7 = $",
                {
                    "id": "gap2",
                    "correctExact": 10,
                    "placeholder": "?"
                },
                "\\n\\nKrok 4: Na koniec: $10 + 14 = $",
                {
                    "id": "gap3",
                    "correctExact": 24,
                    "placeholder": "?"
                }
            ],
            "explanation": "$5 - (-12) - 7 + 14 = 5 + 12 - 7 + 14 = 24$"
        },
        {
            "type": "expression-builder",
            "title": "Zbuduj wyrażenie",
            "instruction": "Użyj dostępnych liczb i operacji, aby uzyskać docelowy wynik. Każdą liczbę możesz użyć tylko raz!",
            "targetValue": -10,
            "availableNumbers": [5, -3, 2, -15],
            "availableOperations": ["+", "-", "*", "/"],
            "sampleSolutions": [
                "$-15 + 5 = -10$",
                "$5 - 15 = -10$"
            ],
            "explanation": "Istnieje wiele sposobów! Najprostsze to: $-15 + 5 = -10$ lub $5 - 15 = -10$"
        },
        {
            "type": "sign-predictor",
            "title": "Przewidź znak: Dzielenie",
            "question": "Jaki znak będzie miał wynik?",
            "expression": "$(-48) : 6 : (-2)$",
            "correctSign": "positive",
            "explanation": "Krok 1: $(-48) : 6 = -8$ (różne znaki).\\nKrok 2: $(-8) : (-2) = 4$ (te same znaki → dodatnie!)"
        },
        {
            "type": "practice",
            "title": "Zadanie: Dług",
            "instruction": "Rozwiąż zadanie z finansami.",
            "scenario": "Jaś miał **-50 zł** długu u kolegi. Spłacił **30 zł**. Ile teraz wynosi jego dług?\\n\\nPotem kolega pożyczył mu jeszcze **20 zł**. Jaki jest całkowity dług Jasia?",
            "inputs": [
                {
                    "label": "Dług po spłacie 30 zł",
                    "placeholder": "wpisz liczbę",
                    "type": "text"
                },
                {
                    "label": "Całkowity dług po kolejnej pożyczce",
                    "placeholder": "wpisz liczbę",
                    "type": "text"
                }
            ],
            "sampleAnswers": {
                "title": "Rozwiązanie",
                "answers": [
                    "**Po spłacie:** $-50 + 30 = -20$ zł (nadal dług!)",
                    "**Po pożyczce:** $-20 + (-20) = -40$ zł",
                    "\\nSpłata długu to dodawanie dodatniej wartości. Nowy dług to dodawanie ujemnej wartości."
                ]
            }
        },
        {
            "type": "input",
            "title": "Ćwiczenie: Oblicz sprytnie",
            "question": "Oblicz sprytnie (grupuj liczby): $15 - (-11) - 15 - 11$",
            "correctAnswer": "0",
            "alternateAnswers": ["0", "0,0", "0.0"],
            "placeholder": "wpisz wynik",
            "explanation": "$15 - (-11) - 15 - 11 = 15 + 11 - 15 - 11 = (15 - 15) + (11 - 11) = 0$"
        },
        {
            "type": "expression-builder",
            "title": "Zbuduj wyrażenie: Trudniejsze",
            "instruction": "Tym razem cel jest większy! Użyj wszystkich dostępnych liczb i operacji.",
            "targetValue": 20,
            "availableNumbers": [10, -5, 4, -2],
            "availableOperations": ["+", "-", "*", "/"],
            "sampleSolutions": [
                "$10 + (-5) \\times (-2) = 10 + 10 = 20$"
            ],
            "explanation": "Sprytne rozwiązanie: $10 + (-5) \\times (-2) = 10 + 10 = 20$. Pamiętaj o kolejności działań!"
        },
        {
            "type": "quiz",
            "title": "Sprawdź, czy umiesz",
            "questions": [
                {
                    "question": "Ile wynosi $-9,85 + 3,4$?",
                    "options": [
                        "$-13,25$",
                        "$-6,45$",
                        "$6,45$",
                        "$13,25$"
                    ],
                    "correctAnswer": 1,
                    "explanation": "Różne znaki: $9,85 - 3,4 = 6,45$, znak ujemny (bo $9,85 > 3,4$), więc $-6,45$"
                },
                {
                    "question": "Ile wynosi $-3,7 - (-9,5)$?",
                    "options": [
                        "$-13,2$",
                        "$5,8$",
                        "$-5,8$",
                        "$13,2$"
                    ],
                    "correctAnswer": 1,
                    "explanation": "$-3,7 - (-9,5) = -3,7 + 9,5 = 5,8$ (dodatnie!)"
                },
                {
                    "question": "Wynikiem $(-3,7) \\times (-2)$ jest:",
                    "options": [
                        "$-7,4$",
                        "$7,4$",
                        "$-1,7$",
                        "$1,85$"
                    ],
                    "correctAnswer": 1,
                    "explanation": "Te same znaki → wynik dodatni: $3,7 \\times 2 = 7,4$"
                },
                {
                    "question": "Które wyrażenie ma wynik UJEMNY?",
                    "options": [
                        "$(-3) \\times (-4)$",
                        "$(-12) \\div (-3)$",
                        "$(-8) \\div 2$",
                        "$(-5) + 10$"
                    ],
                    "correctAnswer": 2,
                    "explanation": "$(-8) \\div 2 = -4$ (różne znaki). Pozostałe dają wyniki dodatnie."
                }
            ]
        },
        {
            "type": "test",
            "title": "Test końcowy",
            "questions": [
                {
                    "question": "Oblicz: $-27 + 12$",
                    "options": [
                        "$-39$",
                        "$-15$",
                        "$15$",
                        "$39$"
                    ],
                    "correctAnswer": 1,
                    "explanation": "Różne znaki: $27 - 12 = 15$, znak ujemny → $-15$"
                },
                {
                    "question": "Oblicz: $-4,5 - 2\\frac{1}{5}$",
                    "options": [
                        "$-6,7$",
                        "$-2,3$",
                        "$2,3$",
                        "$6,7$"
                    ],
                    "correctAnswer": 0,
                    "explanation": "$2\\frac{1}{5} = 2,2$, więc $-4,5 - 2,2 = -4,5 + (-2,2) = -6,7$"
                },
                {
                    "question": "Oblicz: $(-15) \\times (-3)$",
                    "options": [
                        "$-45$",
                        "$45$",
                        "$-5$",
                        "$5$"
                    ],
                    "correctAnswer": 1,
                    "explanation": "Te same znaki → dodatnie: $15 \\times 3 = 45$"
                },
                {
                    "question": "Oblicz: $(-2) \\times (7 - 11)$",
                    "options": [
                        "$-8$",
                        "$8$",
                        "$-36$",
                        "$36$"
                    ],
                    "correctAnswer": 1,
                    "explanation": "Najpierw nawias: $7 - 11 = -4$. Potem: $(-2) \\times (-4) = 8$"
                },
                {
                    "question": "Temperatura spadła z $2°C$ do $-5°C$. O ile stopni spadła?",
                    "options": [
                        "$3°C$",
                        "$-7°C$",
                        "$7°C$",
                        "$-3°C$"
                    ],
                    "correctAnswer": 2,
                    "explanation": "Różnica: $2 - (-5) = 2 + 5 = 7°C$ (wartość bezwzględna spadku)"
                }
            ]
        },
        {
            "type": "summary",
            "title": "Podsumowanie",
            "recap": [
                "**Dodawanie:** Te same znaki → dodaj wartości i zachowaj znak. Różne znaki → odejmij i weź znak większej",
                "**Odejmowanie = dodawanie liczby przeciwnej:** $a - b = a + (-b)$",
                "**Mnożenie/dzielenie:** Te same znaki → wynik **dodatni**. Różne znaki → wynik **ujemny**",
                "**Kilka działań:** Zawsze wykonuj od lewej do prawej, pamiętając o kolejności działań (nawiasy, mnożenie/dzielenie, dodawanie/odejmowanie)"
            ],
            "badge": {
                "title": "Mistrz Znaków",
                "xp": 140
            },
            "nextSteps": "W następnej lekcji poznasz **oś liczbową** i **wartość bezwzględną** - odkryjesz jak mierzyć ''odległość'' liczby od zera!"
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
