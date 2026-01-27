
-- Insert "Matematyka" Module
INSERT INTO modules (
    id,
    title,
    description,
    track,
    display_order
) VALUES (
    'd290f1ee-6c54-4b01-90e6-d701748f0851',
    'Matematyka: Liczby i Działania',
    'Liczby całkowite, ułamki i działania.',
    'math',
    1
) ON CONFLICT (id) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description;

-- Insert "Liczby" Lesson
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
    'math-g7-l1',
    'Liczby',
    'W tej lekcji uporządkujemy Twoją wiedzę o liczbach. Przypomnisz sobie, czym są liczby naturalne, całkowite i wymierne.',
    20,
    100,
    'beginner',
    '{
    "subtitle": "Moduł 1: Liczby i Działania",
    "cards": [
            {
                "type": "intro",
                "title": "Witaj w świecie liczb!",
                "description": "W tej lekcji uporządkujemy Twoją wiedzę o liczbach. Przypomnisz sobie, czym są liczby naturalne, całkowite i wymierne, oraz poznasz ich historię."
            },
            {
                "type": "concept",
                "title": "Rodzaje liczb",
                "content": "Do tej pory używałeś różnych liczb. Czas je uporządkować w **zbiory**:\\n\\n*   **Liczby naturalne ($\\mathbb{N}$)**: $0, 1, 2, 3, 4, ...$. Są to liczby, którymi liczymy przedmioty.\\n*   **Liczby całkowite ($\\mathbb{Z}$)**: $... -3, -2, -1, 0, 1, 2, 3, ...$. Są to liczby naturalne oraz ich **przeciwności**.\\n*   **Liczby wymierne ($\\mathbb{Q}$)**: Wszystkie liczby, które można zapisać w postaci ułamka $\\frac{p}{q}$ (gdzie $p$ i $q$ są całkowite i $q \\neq 0$)."
            },
            {
                "type": "curiosity",
                "title": "Z historii: Skąd mamy cyfry?",
                "content": "Dziesiątkowy system pozycyjny, którym się posługujemy, stworzyli **Hindusi** około 1500 lat temu.\\n\\n*   Hindusi używali słowa **\"sunya\"** (znaczącego \"pusty\" lub \"nic\") na określenie zera.\\n*   W języku arabskim to słowo przetłumaczono na **\"sifr\"**.\\n*   Gdy system ten dotarł do Europy, słowa \"sifr\" (czyli cyfra) początkowo używano właśnie dla zera!\\n\\nCiekawostka: W niektórych językach (np. francuskim) słowa oznaczające \"szyfr\" i \"cyfrę\" brzmią i pisze się prawie tak samo."
            },
            {
                "type": "concept",
                "title": "Ułamki zwykłe i dziesiętne",
                "content": "Każdą liczbę wymierną możemy zapisać na różne sposoby. Zobacz przykłady:\\n\\n| Ułamek zwykły | Metoda zamiany | Ułamek dziesiętny |\\n| :--- | :--- | :--- |\\n| $\\frac{17}{20}$ | $\\frac{17 \\cdot 5}{20 \\cdot 5} = \\frac{85}{100}$ | $0.85$ |\\n| $\\frac{1}{4}$ | $\\frac{1 \\cdot 25}{4 \\cdot 25} = \\frac{25}{100}$ | $0.25$ |\\n| $5\\frac{2}{7}$ | (dzielenie $2:7$) | $5.285...$ |\\n| $14\\frac{9}{20}$ | $14\\frac{9 \\cdot 5}{20 \\cdot 5} = 14\\frac{45}{100}$ | $14.45$ |"
            },
            {
                "type": "input",
                "title": "Sprawdź się: Zamiana",
                "question": "Zamień ułamek $\\frac{3}{4}$ na postać dziesiętną.",
                "correctAnswer": "0.75",
                "placeholder": "np. 0.5",
                "explanation": "$\\frac{3 \\cdot 25}{4 \\cdot 25} = \\frac{75}{100} = 0.75$"
            },
            {
                "type": "fill-gap",
                "title": "Uzupełnij lukę",
                "parts": [
                    "Wiem, że $0.5$ to inaczej ",
                    {
                        "id": "gap1",
                        "correctExact": 1,
                        "placeholder": "?"
                    },
                    "/2."
                ],
                "explanation": "Połowa to $1/2$, czyli $0.5$."
            },
            {
                "type": "number-line",
                "title": "Liczby na osi",
                "question": "Zaznacz liczbę $-2$ na osi liczbowej.",
                "min": -5,
                "max": 5,
                "step": 1,
                "correctValue": -2,
                "tolerance": 0.2,
                "explanation": "Liczby ujemne leżą na lewo od zera.",
                "showTooltip": false,
                "labelFrequency": 5
            },
            {
                "type": "number-line",
                "title": "Ułamki na osi",
                "question": "Zaznacz liczbę $1\\frac{1}{4}$ (czyli $1.25$).",
                "min": 0,
                "max": 3,
                "step": 0.25,
                "correctValue": 1.25,
                "tolerance": 0.1,
                "explanation": "$1.25$ to jeden i jedna czwarta kratki.",
                "showTooltip": false,
                "labelFrequency": 1
            },
            {
                "type": "comparison",
                "title": "Porównywanie liczb",
                "expression": {
                    "left": "$-5$",
                    "right": "$-2$",
                    "relationship": "<"
                },
                "explanation": "Wśród liczb ujemnych, większa jest ta, która leży bliżej zera. $-2$ jest ''cieplejsze'' niż $-5$."
            },
            {
                "type": "number-sort",
                "title": "Uporządkuj liczby",
                "question": "Ustaw liczby od najmniejszej do największej:",
                "numbers": [
                    -3.1,
                    -3,
                    0,
                    0.12,
                    1.25
                ],
                "order": "asc"
            },
            {
                "type": "true-false",
                "title": "Prawda czy Fałsz?",
                "question": "Oceń prawdziwość zdań:",
                "statements": [
                    {
                        "id": "s1",
                        "text": "Każda liczba całkowita jest liczbą naturalną.",
                        "isTrue": false,
                        "explanation": "Nie, np. $-5$ jest całkowita, ale nie jest naturalna."
                    },
                    {
                        "id": "s2",
                        "text": "Każda liczba naturalna jest liczbą całkowitą.",
                        "isTrue": true,
                        "explanation": "Tak, zbiór liczb naturalnych zawiera się w całkowitych."
                    },
                    {
                        "id": "s3",
                        "text": "Każda liczba wymierna jest całkowita.",
                        "isTrue": false,
                        "explanation": "Nie, np. $\\frac{1}{2}$ jest wymierna, ale nie całkowita."
                    }
                ]
            },
            {
                "type": "matching",
                "title": "Liczby przeciwne",
                "question": "Połącz w pary liczby przeciwne:",
                "pairs": [
                    {
                        "id": "p1",
                        "left": "$5$",
                        "right": "$-5$"
                    },
                    {
                        "id": "p2",
                        "left": "$-2.5$",
                        "right": "$2.5$"
                    },
                    {
                        "id": "p3",
                        "left": "$\\frac{1}{4}$",
                        "right": "$-\\frac{1}{4}$"
                    },
                    {
                        "id": "p4",
                        "left": "$1$",
                        "right": "$-1$"
                    }
                ],
                "explanations": {
                    "p1": "Liczby przeciwne leżą symetrycznie względem zera."
                }
            },
            {
                "type": "practice",
                "title": "Zadanie z życia: Pizza",
                "instruction": "Rozwiąż zadanie krok po kroku.",
                "scenario": "Pięcioosobowa rodzina (rodzice i troje dzieci) zamówiła dwie takie same pizze. \\n*   **Rodzice** podzielili swoją pizzę na **6 kawałków** i zjedli 5 z nich.\\n*   **Dzieci** podzieliły swoją na **12 kawałków**.\\n\\nKto zjadł więcej pizzy – dzieci czy rodzice?",
                "inputs": [
                    {
                        "label": "Jaką część pizzy zjedli rodzice?",
                        "placeholder": "np. 5/6",
                        "type": "text"
                    },
                    {
                        "label": "Jeśli dzieci zjadły tyle samo pizzy co rodzice (co do wielkości), ile kawałków zjadły?",
                        "placeholder": "Liczba kawałków",
                        "type": "text"
                    }
                ],
                "sampleAnswers": {
                    "title": "Rozwiązanie",
                    "answers": [
                        "Rodzice zjedli 5 z 6 kawałków, czyli ułamek $\\frac{5}{6}$.",
                        "Dzieci miały podział na 12 kawałków. $\\frac{5}{6} = \\frac{10}{12}$.",
                        "Zatem jeśli dzieci zjadły tyle samo, musiały zjeść **10 kawałków**."
                    ]
                }
            },
            {
                "type": "quiz",
                "title": "Sprawdź, czy umiesz",
                "questions": [
                    {
                        "question": "Ułamek $0.015$ jest równy:",
                        "options": [
                            "$\\frac{3}{20}$",
                            "$\\frac{3}{200}$",
                            "$\\frac{1}{15}$",
                            "$\\frac{3}{250}$"
                        ],
                        "correctAnswer": 1,
                        "explanation": "$0.015 = \\frac{15}{1000} = \\frac{3}{200}$ (po skróceniu przez 5)"
                    },
                    {
                        "question": "Która liczba jest liczbą całkowitą?",
                        "options": [
                            "$-5.5$",
                            "$\\frac{6}{3}$",
                            "$0.7$",
                            "$-1\\frac{1}{5}$"
                        ],
                        "correctAnswer": 1,
                        "explanation": "$\\frac{6}{3} = 2$, a 2 jest liczbą całkowitą."
                    },
                    {
                        "question": "Liczba przeciwna do $-1.5$ to:",
                        "options": [
                            "$-1.5$",
                            "$1.5$",
                            "$\\frac{1}{1.5}$",
                            "Zero"
                        ],
                        "correctAnswer": 1,
                        "explanation": "Liczba przeciwna ma przeciwny znak."
                    },
                    {
                        "question": "Które zdanie jest prawdziwe?",
                        "options": [
                            "Każda liczba naturalna jest całkowita.",
                            "Każda liczba wymierna jest naturalna.",
                            "Zero jest liczbą dodatnią.",
                            "Liczby ujemne są większe od zera."
                        ],
                        "correctAnswer": 0,
                        "explanation": "Zbiór liczb naturalnych zawiera się w zbiorze liczb całkowitych."
                    }
                ]
            },
            {
                "type": "test",
                "title": "Końcowy Test: Liczby",
                "questions": [
                    {
                        "question": "Liczba -3 należy do zbioru liczb:",
                        "options": [
                            "Naturalnych",
                            "Całkowitych",
                            "Żadnego z powyższych"
                        ],
                        "correctAnswer": 1,
                        "explanation": "-3 jest liczbą całkowitą ujemną."
                    },
                    {
                        "question": "Która para to liczby przeciwne?",
                        "options": [
                            "1 i 0.1",
                            "-5 i 5",
                            "2 i 1/2"
                        ],
                        "correctAnswer": 1,
                        "explanation": "Liczby przeciwne różnią się tylko znakiem."
                    },
                    {
                        "question": "Ułamek 3/4 to w postaci dziesiętnej:",
                        "options": [
                            "0.34",
                            "0.75",
                            "3.4",
                            "0.43"
                        ],
                        "correctAnswer": 1,
                        "explanation": "3 podzielić na 4 to 0.75."
                    },
                    {
                        "question": "Co jest prawdą?",
                        "options": [
                            "Zbiór liczb naturalnych zawiera się w całkowitych",
                            "Liczby wymierne to tylko ułamki zwykłe",
                            "Zero jest liczbą dodatnią"
                        ],
                        "correctAnswer": 0,
                        "explanation": "Prawda. Każda liczba naturalna jest też całkowita."
                    },
                    {
                        "question": "Jeśli zjesz 2 z 8 kawałków pizzy, jaka część została?",
                        "options": [
                            "2/8",
                            "3/4",
                            "1/4",
                            "1/8"
                        ],
                        "correctAnswer": 1,
                        "explanation": "Zostało 8 - 2 = 6 kawałków. 6/8 to po skróceniu 3/4."
                    }
                ]
            },
            {
                "type": "summary",
                "title": "Podsumowanie",
                "recap": [
                    "Liczby naturalne (N), całkowite (Z) i wymierne (Q) tworzą coraz szersze zbiory.",
                    "Liczby wymierne można zapisać jako ułamek zwykły lub dziesiętny.",
                    "Każda liczba ma swoją liczbę przeciwną (leżącą symetrycznie po drugiej stronie zera).",
                    "Wartość liczby rośnie na osi liczbowej w prawą stronę (dlatego -2 > -5)."
                ],
                "badge": {
                    "title": "Mistrz Liczb",
                    "xp": 100
                },
                "nextSteps": "W następnej lekcji zajmiemy się rozwinięciami dziesiętnymi i okresami."
            }
        ]
    }'::jsonb,
    'd290f1ee-6c54-4b01-90e6-d701748f0851'
) ON CONFLICT (lesson_id) DO UPDATE SET
    content = EXCLUDED.content,
    title = EXCLUDED.title,
    xp_reward = EXCLUDED.xp_reward,
    module_id = EXCLUDED.module_id;


-- Insert "Rozwinięcia dziesiętne" Lesson
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
    'math-g7-l2',
    'Rozwinięcia dziesiętne',
    'W tej lekcji uporządkujemy Twoją wiedzę o liczbach. Przypomnisz sobie, czym są liczby naturalne, całkowite i wymierne.',
    20,
    100,
    'beginner',
    '{
    "subtitle": "Moduł 1: Liczby i Działania",
    "cards": [
            {
                "type": "intro",
                "title": "Czy dzielenie zawsze się kończy?",
                "description": "Wiesz już, że każdy ułamek zwykły to tak naprawdę dzielenie. Ale co się stanie, gdy reszta z dzielenia nigdy nie będzie zerem? W tej lekcji odkryjesz tajemnice rozwinięć dziesiętnych!"
            },
            {
                "type": "concept",
                "title": "Ułamek jako dzielenie",
                "content": "Pamiętasz? Kreska ułamkowa zastępuje znak dzielenia.\\n\\n$$\\frac{3}{4} = 3 : 4 = 0,75$$\\n\\nW tym przypadku dzielenie się skończyło (reszta wyszła 0). Otrzymaliśmy **rozwinięcie dziesiętne skończone**."
            },
            {
                "type": "matching",
                "title": "Dopasuj rozwinięcia skończone",
                "question": "Połącz ułamki zwykłe z ich postaciami dziesiętnymi.",
                "pairs": [
                    { "id": "p1", "left": "1/2", "right": "0,5" },
                    { "id": "p2", "left": "3/4", "right": "0,75" },
                    { "id": "p3", "left": "1/5", "right": "0,2" },
                    { "id": "p4", "left": "1/8", "right": "0,125" }
                ],
                "explanations": {
                    "p1": "1 podzielić przez 2 to pół, czyli 0,5",
                    "p2": "Trzy czwarte to 0,75",
                    "p3": "1 podzielić przez 5 to 0,2",
                    "p4": "1 podzielić przez 8 to 0,125"
                }
            },
            {
                "type": "concept",
                "title": "Gdy dzielenie nie ma końca...",
                "content": "Spróbujmy zamienić $\\frac{1}{3}$ na ułamek dziesiętny.\\n\\n$$1 : 3 = 0,33333...$$\\n\\nDzielenie nigdy się nie skończy! Trójki będą się powtarzać w nieskończoność.\\nTaką liczbę nazywamy **ułamkiem okresowym**.\\n\\nZapisujemy to w skrócie, biorąc powtarzającą się część w nawias:\\n$$0,333... = 0,(3)$$\\nTo co w nawiasie, nazywamy **okresem**."
            },
            {
                "type": "fill-gap",
                "title": "Zapisz okres",
                "parts": [
                    "Ułamek $\\frac{4}{9} = 0,444...$ zapiszemy jako 0, (",
                    { "id": "g1", "placeholder": "?", "correctExact": 4 },
                    ")",
                    "\n\nUłamek $\\frac{5}{33} = 0,151515...$ zapiszemy jako 0, (",
                    { "id": "g2", "placeholder": "?", "correctExact": 15 },
                    ")"
                ],
                "explanation": "W nawias wpisujemy cyfry, które się powtarzają. Dla 4/9 jest to 4, a dla 5/33 jest to 15."
            },
            {
                "type": "curiosity",
                "title": "Sekret mianowników",
                "content": "Czy wiesz, że możesz przewidzieć, czy ułamek będzie miał rozwinięcie skończone, nie wykonując dzielenia?\\n\\n**ZASADA:** Jeśli mianownik ułamka nieskracalnego rozłożysz na czynniki pierwsze i otrzymasz **tylko dwójki i piątki**, to rozwinięcie będzie **skończone**.\\n\\nJeśli pojawi się jakakolwiek inna liczba (np. 3, 7, 11) - rozwinięcie będzie nieskończone okresowe!\\n\\nPrzykłady:\\n* $\\frac{1}{20}$ (20 = 2·2·5) -> Skończone\\n* $\\frac{1}{6}$ (6 = 2·3) -> Nieskończone (bo jest 3)"
            },
            {
                "type": "true-false",
                "title": "Skończone czy nieskończone?",
                "question": "Oceń prawdziwość zdań, korzystając z ''Sekretu mianowników''.",
                "statements": [
                    {
                        "id": "s1",
                        "text": "Ułamek 1/7 ma rozwinięcie skończone.",
                        "isTrue": false,
                        "explanation": "Mianownik to 7 (liczba inna niż 2 i 5), więc rozwinięcie jest nieskończone."
                    },
                    {
                        "id": "s2",
                        "text": "Ułamek 1/25 ma rozwinięcie skończone.",
                        "isTrue": true,
                        "explanation": "25 to 5·5. Są same piątki, więc rozwinięcie jest skończone (0,04)."
                    },
                    {
                        "id": "s3",
                        "text": "Ułamek 1/30 ma rozwinięcie skończone.",
                        "isTrue": false,
                        "explanation": "30 = 2·3·5. Pojawia się trójka, więc rozwinięcie jest nieskończone."
                    }
                ]
            },
            {
                "type": "quiz",
                "title": "Sprawdź, czy umiesz",
                "questions": [
                    {
                        "question": "Ułamek $0,015$ jest równy:",
                        "options": ["$\\frac{3}{20}$", "$\\frac{3}{200}$", "$\\frac{1}{15}$", "$\\frac{3}{250}$"],
                        "correctAnswer": 1,
                        "explanation": "$0,015 = \\frac{15}{1000}$. Skracamy przez 5: $\\frac{15:5}{1000:5} = \\frac{3}{200}$."
                    },
                    {
                        "question": "Która liczba jest większa: $0,(3)$ czy $0,33$?",
                        "options": ["$0,(3)$", "$0,33$", "Są równe"],
                        "correctAnswer": 0,
                        "explanation": "$0,(3) = 0,3333...$ co jest większe od $0,3300$."
                    },
                    {
                        "question": "Jaka jest czwarta cyfra po przecinku liczby $1,2(34)$?",
                        "options": ["2", "3", "4", "Nie ma czwartej cyfry"],
                        "correctAnswer": 1,
                        "explanation": "Rozpiszmy: $1,2343434...$. Kolejne cyfry po przecinku: 2, 3, 4, 3, 4... Czwarta cyfra to 3."
                    }
                ]
            },
            {
                "type": "test",
                "title": "Test końcowy",
                "questions": [
                    {
                        "id": "q1",
                        "type": "choice",
                        "question": "Zamień $\\frac{1}{8}$ na ułamek dziesiętny.",
                        "options": ["0,25", "0,125", "0,15", "0,8"],
                        "correctAnswer": 1
                    },
                    {
                        "id": "q2",
                        "type": "choice",
                        "question": "Który zapis jest poprawny dla $2,727272...$?",
                        "options": ["$2,7(2)$", "$2,(72)$", "$2,72(7)$", "$2,(7)$"],
                        "correctAnswer": 1
                    },
                    {
                        "id": "q3",
                        "type": "choice",
                        "question": "Które uporządkowanie liczb jest poprawne?",
                        "options": [
                            "$0,3 < 0,33 < 0,(3)$",
                            "$0,(3) < 0,33 < 0,3$",
                            "$0,33 < 0,(3) < 0,3$",
                            "$0,3 < 0,(3) < 0,33$"
                        ],
                        "correctAnswer": 0
                    }
                ]
            },
            {
                "type": "summary",
                "title": "Podsumowanie",
                "recap": [
                    "Ułamek zwykły to dzielenie (licznik przez mianownik).",
                    "Rozwinięcie dziesiętne może być **skończone** (np. 0,5) lub **nieskończone okresowe** (np. 0,333...).",
                    "Okres to powtarzająca się cyfra lub grupa cyfr, którą zapisujemy w nawiasie: $0,(3)$."
                ]
            }
        ]
    }'::jsonb,
    'd290f1ee-6c54-4b01-90e6-d701748f0851'
) ON CONFLICT (lesson_id) DO UPDATE SET
    content = EXCLUDED.content,
    title = EXCLUDED.title,
    xp_reward = EXCLUDED.xp_reward,
    module_id = EXCLUDED.module_id;

-- Insert "Matematyka - 7 klasa" Path with "Matematyka: Liczby i Działania" Module
INSERT INTO learning_paths (
    path_slug,
    title,
    description,
    difficulty,
    total_xp_reward,
    lesson_sequence,
    requires_all_lessons
) VALUES (
    'math-grade-7',
    'Matematyka - 7 klasa',
    'Kompletny kurs matematyki dla klasy 7, zgodny z podstawą programową. Odkryj fascynujący świat liczb, algebry i geometrii.',
    'beginner',
    1000,
    -- Structure with Module info.
    '[
        {
            "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
            "type": "module",
            "title": "Matematyka: Liczby i Działania",
            "lessons": ["math-g7-l1", "math-g7-l2"]
        }
    ]'::jsonb,
    true
) ON CONFLICT (path_slug) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    lesson_sequence = EXCLUDED.lesson_sequence;
