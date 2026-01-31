-- Insert "Wartość bezwzględna i odległość" Lesson
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
    'math-g7-l8',
    'Wartość bezwzględna i odległość',
    'Odkryj czym jest wartość bezwzględna i jak mierzyć odległość liczb od zera. Naucz się rozwiązywać równania i porównywać liczby używając wartości bezwzględnej.',
    30,
    130,
    'beginner',
    '{
    "subtitle": "Moduł 1: Liczby i Działania",
    "cards": [
        {
            "type": "intro",
            "title": "Odległość liczby od zera",
            "description": "Wyobraź sobie spacer: nie ma znaczenia czy idziesz 5 kroków w prawo czy w lewo - przeszedłeś **5 kroków**. Tak samo z liczbami: **-5** i **+5** są w tej samej **odległości** od zera. Poznaj wartość bezwzględną!"
        },
        {
            "type": "flashcards",
            "title": "Po co nam odległość od zera?",
            "cards": [
                {
                    "front": "📏 **Pomiar odległości**\\n\\nStoisko z lodami jest **5 metrów** w lewo od fontanny. Kiosk **5 metrów** w prawo. Który jest bliżej?",
                    "back": "**Odpowiedź:** Tak samo blisko!\\n\\nOdległość: $|-5| = 5$ i $|5| = 5$\\n\\nKierunek nie ma znaczenia przy mierzeniu odległości."
                },
                {
                    "front": "🌡️ **Różnica temperatur**\\n\\nDziś **-8°C**, wczoraj było **3°C**. O ile stopni spadło?",
                    "back": "**Rozwiązanie:** $|3 - (-8)| = |11| = 11$ stopni\\n\\nWartość bezwzględna pokazuje **wielkość zmiany** bez kierunku."
                },
                {
                    "front": "💰 **Błąd w obliczeniach**\\n\\nPrawidłowa kwota: **500 zł**. Policzyłeś: **485 zł**. Jaki był błąd?",
                    "back": "**Rozwiązanie:** $|500 - 485| = 15$ zł\\n\\nBłąd zawsze mierzymy jako wartość bezwzględną!"
                }
            ]
        },
        {
            "type": "concept",
            "title": "Co to jest wartość bezwzględna?",
            "content": "**Wartość bezwzględna** liczby to jej **odległość od zera** na osi liczbowej.\\n\\n**Oznaczenie:** $|x|$ (czytamy: ''wartość bezwzględna x'')\\n\\n**Przykłady:**\\n- $|5| = 5$ (5 jest 5 jednostek od zera)\\n- $|-5| = 5$ (−5 jest też 5 jednostek od zera!)\\n- $|0| = 0$ (zero jest w zerowej odległości od siebie)\\n- $|-3,7| = 3,7$\\n- $|100| = 100$\\n\\n**Klucz:** Wartość bezwzględna jest **zawsze** nieujemna ($\\geq 0$)!"
        },
        {
            "type": "distance-visualizer",
            "title": "Symetria na osi",
            "question": "Przyjrzyj się liczbom **-7** i **7** na osi liczbowej. Jaka jest odległość każdej z nich od zera?",
            "numbers": [-7, 7],
            "correctDistance": 7,
            "showSymmetry": true,
            "explanation": "Obie liczby leżą w odległości **7 jednostek** od zera - jedna w lewo, druga w prawo. Dlatego $|-7| = |7| = 7$."
        },
        {
            "type": "number-line",
            "title": "Zaznacz liczbę",
            "question": "Znajdź na osi liczbową liczbę **dodatnią**, której wartość bezwzględna wynosi 6.",
            "min": -10,
            "max": 10,
            "step": 1,
            "correctValue": 6,
            "tolerance": 0.3,
            "explanation": "Liczba dodatnia o wartości bezwzględnej 6 to **6**. Druga liczba to **-6**, ale pytanie dotyczyło liczby dodatniej.",
            "showTooltip": false,
            "labelFrequency": 2
        },
        {
            "type": "matching",
            "title": "Dopasuj wartości",
            "question": "Połącz liczby z ich wartościami bezwzględnymi:",
            "pairs": [
                {
                    "id": "p1",
                    "left": "$-12$",
                    "right": "$12$"
                },
                {
                    "id": "p2",
                    "left": "$8$",
                    "right": "$8$"
                },
                {
                    "id": "p3",
                    "left": "$-3,5$",
                    "right": "$3,5$"
                },
                {
                    "id": "p4",
                    "left": "$0$",
                    "right": "$0$"
                }
            ],
            "explanations": {
                "p1": "$|-12| = 12$ (odległość 12 od zera)",
                "p2": "$|8| = 8$ (liczba dodatnia = jej wartość bezwzględna)",
                "p3": "$|-3,5| = 3,5$ (bez znaku minus!)",
                "p4": "$|0| = 0$ (zero jest w zerowej odległości od siebie)"
            }
        },
        {
            "type": "concept",
            "title": "Jak obliczyć wartość bezwzględną?",
            "content": "**REGUŁA PROSTA:**\\n\\n**1. Jeśli liczba jest dodatnia lub zero:**\\n$|x| = x$\\n\\nPrzykłady: $|5| = 5$, $|0| = 0$, $|3,14| = 3,14$\\n\\n**2. Jeśli liczba jest ujemna:**\\n$|x| = -x$ (zmień znak!)\\n\\nPrzykłady: $|-5| = 5$, $|-8| = 8$, $|-100| = 100$\\n\\n**Skrót:** Po prostu **usuń znak minus** (jeśli jest)!"
        },
        {
            "type": "input",
            "title": "Oblicz wartość bezwzględną",
            "question": "Ile wynosi $|-23|$?",
            "correctAnswer": "23",
            "alternateAnswers": ["23", "23,0", "23.0"],
            "placeholder": "wpisz wynik",
            "explanation": "$|-23| = 23$ (usuwamy znak minus)"
        },
        {
            "type": "input",
            "title": "Oblicz wartość bezwzględną",
            "question": "Ile wynosi $|4,7|$?",
            "correctAnswer": "4.7",
            "alternateAnswers": ["4.7", "4,7"],
            "placeholder": "wpisz wynik",
            "explanation": "$|4,7| = 4,7$ (liczba dodatnia, zostaje bez zmian)"
        },
        {
            "type": "true-false",
            "title": "Prawda czy fałsz?",
            "question": "Oceń poniższe stwierdzenia:",
            "statements": [
                {
                    "id": "s1",
                    "text": "$|-9| = 9$",
                    "isTrue": true,
                    "explanation": "Prawda! Wartość bezwzględna $-9$ to $9$."
                },
                {
                    "id": "s2",
                    "text": "$|7| = -7$",
                    "isTrue": false,
                    "explanation": "Fałsz! Wartość bezwzględna jest zawsze nieujemna. $|7| = 7$."
                },
                {
                    "id": "s3",
                    "text": "$|-5| = |5|$",
                    "isTrue": true,
                    "explanation": "Prawda! Obie liczby mają tę samą odległość od zera: $5$."
                },
                {
                    "id": "s4",
                    "text": "$|0| = 0$",
                    "isTrue": true,
                    "explanation": "Prawda! Zero leży w odległości $0$ od siebie."
                }
            ]
        },
        {
            "type": "fill-gap",
            "title": "Oblicz wyrażenie",
            "parts": [
                "Oblicz: $|-8| + |3|$\\n\\nKrok 1: $|-8| = $",
                {
                    "id": "gap1",
                    "correctExact": 8,
                    "placeholder": "?"
                },
                "\\n\\nKrok 2: $|3| = $",
                {
                    "id": "gap2",
                    "correctExact": 3,
                    "placeholder": "?"
                },
                "\\n\\nKrok 3: Zsumuj: $8 + 3 = $",
                {
                    "id": "gap3",
                    "correctExact": 11,
                    "placeholder": "?"
                }
            ],
            "explanation": "$|-8| + |3| = 8 + 3 = 11$"
        },
        {
            "type": "distance-visualizer",
            "title": "Porównaj odległości",
            "question": "Która liczba jest **dalej** od zera: **-12** czy **8**?",
            "numbers": [-12, 8],
            "correctDistance": 12,
            "compareMode": true,
            "explanation": "$|-12| = 12$ i $|8| = 8$. Ponieważ $12 > 8$, liczba **-12** jest dalej od zera niż **8**."
        },
        {
            "type": "concept",
            "title": "Porównywanie za pomocą wartości bezwzględnej",
            "content": "**Jak porównywać liczby ujemne?**\\n\\nDla liczb ujemnych: **większa wartość bezwzględna = mniejsza liczba**\\n\\n**Przykłady:**\\n- $-10$ vs $-3$: $|-10| = 10 > |-3| = 3$, więc $-10 < -3$ ✨\\n- $-7$ vs $-15$: $|-7| = 7 < |-15| = 15$, więc $-7 > -15$\\n\\n**Intuicja:** Im dalej w lewo na osi, tym mniejsza liczba!"
        },
        {
            "type": "input",
            "title": "Równanie z wartością bezwzględną",
            "question": "Znajdź **wszystkie** liczby $x$, dla których $|x| = 9$. Podaj mniejszą z nich:",
            "correctAnswer": "-9",
            "alternateAnswers": ["-9", "-9,0", "-9.0"],
            "placeholder": "wpisz liczbę",
            "explanation": "$|x| = 9$ ma dwa rozwiązania: $x = 9$ lub $x = -9$ (obie liczby w odległości 9 od zera)"
        },
        {
            "type": "practice",
            "title": "Zadanie: Odległości",
            "instruction": "Rozwiąż zadanie praktyczne.",
            "scenario": "Na osi liczbowej punkt A ma współrzędną **-15**, punkt B ma współrzędną **10**.\\n\\nOblicz odległość punktu A od zera oraz odległość punktu B od zera. Który punkt jest dalej od zera?",
            "inputs": [
                {
                    "label": "Odległość A od zera",
                    "placeholder": "wpisz liczbę",
                    "type": "text"
                },
                {
                    "label": "Odległość B od zera",
                    "placeholder": "wpisz liczbę",
                    "type": "text"
                }
            ],
            "sampleAnswers": {
                "title": "Rozwiązanie",
                "answers": [
                    "**Punkt A:** $|-15| = 15$",
                    "**Punkt B:** $|10| = 10$",
                    "\\n**Odpowiedź:** Punkt A jest dalej (15 > 10)"
                ]
            }
        },
        {
            "type": "curiosity",
            "title": "Ciekawostka: Wartość bezwzględna w fizyce",
            "content": "**Prędkość** ma wartość i kierunek, ale **szybkość** to wartość bezwzględna prędkości!\\n\\n🚗 Samochód jedzie z prędkością **-30 km/h** (w lewo) lub **+30 km/h** (w prawo).\\n\\nSzybkość w obu przypadkach: $|-30| = |30| = 30$ km/h\\n\\n**W fizyce:**\\n- Przesunięcie może być ujemne\\n- Droga (wartość bezwzględna przesunięcia) jest zawsze dodatnia\\n\\n**Temperatura bezwzględna** (skala Kelvina) też nie może być ujemna - minimum to 0 K!"
        },
        {
            "type": "quiz",
            "title": "Sprawdź, czy umiesz",
            "questions": [
                {
                    "question": "Ile wynosi $|-17|$?",
                    "options": [
                        "$-17$",
                        "$17$",
                        "$0$",
                        "$34$"
                    ],
                    "correctAnswer": 1,
                    "explanation": "$|-17| = 17$ (odległość od zera)"
                },
                {
                    "question": "Która liczba ma wartość bezwzględną równą 5?",
                    "options": [
                        "Tylko $5$",
                        "Tylko $-5$",
                        "$5$ i $-5$",
                        "Żadna"
                    ],
                    "correctAnswer": 2,
                    "explanation": "Dwie liczby: $|5| = 5$ i $|-5| = 5$"
                },
                {
                    "question": "Ile wynosi $|8| - |-3|$?",
                    "options": [
                        "$5$",
                        "$11$",
                        "$-5$",
                        "$-11$"
                    ],
                    "correctAnswer": 0,
                    "explanation": "$|8| - |-3| = 8 - 3 = 5$"
                },
                {
                    "question": "Która liczba jest **dalej** od zera?",
                    "options": [
                        "$-20$",
                        "$15$",
                        "Tak samo daleko",
                        "Nie da się określić"
                    ],
                    "correctAnswer": 0,
                    "explanation": "$|-20| = 20 > |15| = 15$, więc $-20$ jest dalej"
                }
            ]
        },
        {
            "type": "test",
            "title": "Test końcowy",
            "questions": [
                {
                    "question": "Ile wynosi $|-45|$?",
                    "options": [
                        "$-45$",
                        "$45$",
                        "$0$",
                        "$90$"
                    ],
                    "correctAnswer": 1,
                    "explanation": "$|-45| = 45$"
                },
                {
                    "question": "Oblicz: $|-7| + |-2|$",
                    "options": [
                        "$-9$",
                        "$9$",
                        "$5$",
                        "$-5$"
                    ],
                    "correctAnswer": 1,
                    "explanation": "$|-7| + |-2| = 7 + 2 = 9$"
                },
                {
                    "question": "Dla jakich $x$ prawdziwe jest $|x| = 12$?",
                    "options": [
                        "$x = 12$",
                        "$x = -12$",
                        "$x = 12$ lub $x = -12$",
                        "Brak rozwiązań"
                    ],
                    "correctAnswer": 2,
                    "explanation": "Dwa rozwiązania: $12$ i $-12$ (obie w odległości 12 od zera)"
                },
                {
                    "question": "Która nierówność jest **prawdziwa**?",
                    "options": [
                        "$|-8| < |3|$",
                        "$|-8| = |3|$",
                        "$|-8| > |3|$",
                        "Żadna"
                    ],
                    "correctAnswer": 2,
                    "explanation": "$|-8| = 8$ i $|3| = 3$, więc $8 > 3$"
                },
                {
                    "question": "Temperatura spadła z **2°C** do **-7°C**. Jaka była **wartość bezwzględna** zmiany?",
                    "options": [
                        "$5°C$",
                        "$9°C$",
                        "$-9°C$",
                        "$-5°C$"
                    ],
                    "correctAnswer": 1,
                    "explanation": "Zmiana: $2 - (-7) = 9$. Wartość bezwzględna: $|9| = 9°C$"
                }
            ]
        },
        {
            "type": "summary",
            "title": "Podsumowanie",
            "recap": [
                "**Wartość bezwzględna** $|x|$ to **odległość** liczby $x$ od zera na osi",
                "**Właściwości:** $|x| \\geq 0$ (zawsze nieujemna), $|-x| = |x|$ (symetria)",
                "**Obliczanie:** Dla liczb dodatnich $|x| = x$, dla ujemnych $|x| = -x$ (usuń minus)",
                "**Równania:** $|x| = a$ ma dwa rozwiązania: $x = a$ lub $x = -a$ (jeśli $a > 0$)",
                "**Porównywanie:** Większa wartość bezwzględna = dalej od zera"
            ],
            "badge": {
                "title": "Ekspert Odległości",
                "xp": 130
            },
            "nextSteps": "W następnej lekcji poznasz **ułamki zwykłe** - nauczysz się porównywać, dodawać i odejmować ułamki o różnych mianownikach!"
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
