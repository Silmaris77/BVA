
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
            "order": "asc"
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
                    "explanation": "3,(93) = 3,9393... Trzecia cyfra po przecinku to 9, więc zaokrąglamy w górę: 3,94."
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
    description = EXCLUDED.description,
    duration_minutes = EXCLUDED.duration_minutes,
    xp_reward = EXCLUDED.xp_reward,
    difficulty = EXCLUDED.difficulty,
    module_id = EXCLUDED.module_id;

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
                "correctAnswer": "4/5",
                "alternateAnswers": ["0.8", "0,8", "4/5", "⅘"],
                "placeholder": "wpisz wynik",
                "explanation": "Ułamki mają już wspólny mianownik 5, więc: $\\frac{3}{5} + \\frac{1}{5} = \\frac{4}{5} = 0,8$"
            },
            {
                "type": "fill-gap",
                "title": "Wspólny mianownik",
                "parts": [
                    "Oblicz: $\\frac{1}{2} + \\frac{1}{3}$",
                    "\\n\\nKrok 1: Wspólny mianownik to ",
                    {
                        "id": "gap1",
                        "correctExact": 6,
                        "placeholder": "?"
                    },
                    "\\n\\nKrok 2: Po rozszerzeniu licznik pierwszego ułamka to ",
                    {
                        "id": "gap2",
                        "correctExact": 3,
                        "placeholder": "?"
                    },
                    ", a drugiego ",
                    {
                        "id": "gap3",
                        "correctExact": 2,
                        "placeholder": "?"
                    },
                    "\\n\\nKrok 3: Suma liczników wynosi ",
                    {
                        "id": "gap4",
                        "correctExact": 5,
                        "placeholder": "?"
                    }
                ],
                "explanation": "Wspólny mianownik dla 2 i 3 to 6. Po rozszerzeniu: $\\frac{1 \\cdot 3}{2 \\cdot 3} + \\frac{1 \\cdot 2}{3 \\cdot 2} = \\frac{3}{6} + \\frac{2}{6} = \\frac{5}{6}$"
            },
            {
                "type": "concept",
                "title": "Dodawanie liczb dziesiętnych",
                "content": "**Dodając lub odejmując ułamki dziesiętne**, postępujemy jak przy liczbach naturalnych.\\n\\nProste rachunki wykonujemy w pamięci:\\n\\n$$0,9 + 0,4 = 1,3$$\\n\\n$$0,54 - 0,2 = 0,54 - 0,20 = 0,34$$\\n\\nBardziej skomplikowane - sposobem pisemnym (liczby jedna pod drugą):\\n\\n$$\\begin{array}{r} 14,065 \\\\[2pt] + \\; 2,700 \\\\[2pt] \\hline 16,765 \\end{array}$$\\n\\n**Pamiętaj:** Przecinki muszą być pod sobą!"
            },
            {
                "type": "input",
                "title": "Oblicz w pamięci",
                "question": "Oblicz: $1,2 + 2,15$",
                "correctAnswer": "3,35",
                "alternateAnswers": ["3.35", "3,35"],
                "placeholder": "wpisz wynik",
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
                "scenario": "Na weselu goście rodziców panny młodej stanowili $\\frac{2}{3}$ wszystkich gości, a goście rodziców pana młodego $\\frac{1}{8}$ wszystkich gości. Pozostałych gości zaprosiła młoda para.\n\n**Pytanie:** Kto zaprosił najwięcej osób?",
                "inputs": [
                    {
                        "label": "Jaką część gości zaprosiła młoda para? (podaj ułamek lub liczbę dziesiętną)",
                        "placeholder": "np. 1/4 lub 0.25",
                        "type": "text"
                    },
                    {
                        "label": "Która grupa była najliczniejsza? (wpisz: panna młoda / pan młody / para)",
                        "placeholder": "wpisz jedną z opcji",
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
                "scenario": "Barka na Noteci w spokojnej wodzie rozwija prędkość 1,4 m/s. Prędkość nurtu rzeki wynosi 0,28 m/s.\n\nOblicz, z jaką prędkością barka płynie z prądem i pod prąd.",
                "inputs": [
                    {
                        "label": "Prędkość z prądem (m/s)",
                        "placeholder": "np. 2.5",
                        "type": "text"
                    },
                    {
                        "label": "Prędkość pod prąd (m/s)",
                        "placeholder": "np. 1.5",
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
                        "question": "Co jest większe: $\\frac{1}{3} + \\frac{1}{4}$ czy $0,5$?",
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
                "nextSteps": "W następnej lekcji nauczysz się mnożyć i dzielić liczby wymierne!"
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
    1270,
    -- Structure with Module info.
    '[
        {
            "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
            "type": "module",
            "title": "Matematyka: Liczby i Działania",
            "lessons": ["math-g7-l1", "math-g7-l2", "math-g7-l3", "math-g7-l4", "math-g7-l5", "math-g7-l6", "math-g7-l7", "math-g7-l8"]
        }
    ]'::jsonb,
    true
) ON CONFLICT (path_slug) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    lesson_sequence = EXCLUDED.lesson_sequence,
    total_xp_reward = EXCLUDED.total_xp_reward;

-- LESSON 5: Mnożenie i dzielenie liczb dodatnich
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
    'math-g7-l5',
    'Mnożenie i dzielenie liczb dodatnich',
    'Naucz się mnożyć i dzielić ułamki zwykłe i dziesiętne, przesuwać przecinek oraz stosować te umiejętności w praktyce.',
    35,
    140,
    'beginner',
    '{
        "cards": [
            {
                "id": 1,
                "type": "intro",
                "title": "Mnożenie i dzielenie liczb dodatnich",
                "description": "Mnożenie i dzielenie to kluczowe operacje matematyczne, które pozwalają na rozwiązywanie wielu praktycznych problemów. W tej lekcji nauczysz się mnożyć i dzielić zarówno ułamki zwykłe, jak i liczby dziesiętne, a także odkryjesz proste sposoby na przesuwanie przecinka."
            },
            {
                "id": 2,
                "type": "concept",
                "title": "Mnożenie ułamków zwykłych",
                "content": "Aby pomnożyć ułamki zwykłe:\n\n1. **Liczby mieszane** zamień na ułamki niewłaściwe\n2. **Skróć krzyżowo** (mnożnik przez mianownik, licznik przez licznik)\n3. **Pomnóż** liczniki przez liczniki i mianowniki przez mianowniki\n\n**Przykład:**\n$$2\\frac{1}{5} \\times \\frac{2}{9} = \\frac{11}{5} \\times \\frac{2}{9} = \\frac{22}{45}$$\n\n**Przykład ze skracaniem:**\n$$\\frac{3}{5} \\times \\frac{7}{9} = \\frac{3 \\times 7}{5 \\times 9} = \\frac{21}{45} = \\frac{7}{15}$$"
            },
            {
                "id": 3,
                "type": "input",
                "title": "Ćwiczenie: Mnożenie ułamków",
                "question": "Oblicz: $$\\frac{2}{3} \\times \\frac{3}{4}$$",
                "correctAnswer": "1/2",
                "alternateAnswers": ["0,5", "0.5", "1/2", "½", "6/12"],
                "placeholder": "wpisz wynik",
                "hint": "Pomnóż liczniki przez liczniki i mianowniki przez mianowniki, następnie skróć."
            },
            {
                "id": 4,
                "type": "concept",
                "title": "Dzielenie ułamków zwykłych",
                "content": "Aby podzielić ułamki zwykłe:\n\n1. **Liczby mieszane** zamień na ułamki niewłaściwe\n2. **Odwróć drugi ułamek** (dzielnik)\n3. **Wykonaj mnożenie** pierwszego ułamka przez odwrotność drugiego\n\n**Przykład:**\n$$\\frac{3}{5} \\div \\frac{2}{3} = \\frac{3}{5} \\times \\frac{3}{2} = \\frac{9}{10}$$\n\n**Pamiętaj:** Dzielenie przez ułamek to mnożenie przez jego odwrotność!"
            },
            {
                "id": 5,
                "type": "input",
                "title": "Ćwiczenie: Dzielenie ułamków",
                "question": "Oblicz: $$\\frac{4}{5} \\div \\frac{2}{3}$$",
                "correctAnswer": "6/5",
                "alternateAnswers": ["1,2", "1.2", "6/5", "1 1/5"],
                "placeholder": "wpisz wynik",
                "hint": "Odwróć drugi ułamek i pomnóż: 4/5 × 3/2"
            },
            {
                "id": 6,
                "type": "concept",
                "title": "Mnożenie i dzielenie liczb dziesiętnych",
                "content": "**Mnożenie dziesiętnych:**\n\nWykonujemy mnożenie jak na liczbach naturalnych, a następnie oddzielamy przecinkiem tyle cyfr od prawej, ile było wszystkich miejsc po przecinku w obu czynnikach.\n\n**Przykład:** $$1,35 \\times 2,7 = 3,645$$ (2+1=3 miejsca po przecinku)\n\n**Dzielenie dziesiętnych:**\n\nPrzed wykonaniem dzielenia przesuwamy przecinek w obu liczbach o tyle samo miejsc, aby dzielnik był liczbą całkowitą.\n\n**Przykład:** $$30,24 \\div 1,5 = 302,4 \\div 15 = 20,16$$"
            },
            {
                "id": 7,
                "type": "input",
                "title": "Ćwiczenie: Mnożenie dziesiętnych",
                "question": "Oblicz: $$2,5 \\times 0,4$$",
                "correctAnswer": "1",
                "alternateAnswers": ["1", "1,0", "1.0"],
                "placeholder": "wpisz wynik",
                "hint": "25 × 4 = 100, więc 2,5 × 0,4 = 1,00"
            },
            {
                "id": 8,
                "type": "curiosity",
                "title": "Przesuwanie przecinka",
                "content": "**Szybkie mnożenie i dzielenie przez 10, 100, 1000...**\n\n**Mnożenie:** Przesuń przecinek w **prawo**\n- $$3,27 \\times 100 = 327$$\n- $$5,12 \\times 1000 = 5120$$\n\n**Dzielenie:** Przesuń przecinek w **lewo**\n- $$73,4 \\div 100 = 0,734$$\n- $$5,12 \\div 1000 = 0,00512$$\n\nTo bardzo przydatny trick przy konwersji jednostek (np. metrów na centymetry)!"
            },
            {
                "id": 9,
                "type": "input",
                "title": "Ćwiczenie: Przesuwanie przecinka",
                "question": "Oblicz: $$4,25 \\div 100$$",
                "correctAnswer": "0,0425",
                "alternateAnswers": ["0,0425", "0.0425"],
                "placeholder": "wpisz wynik",
                "hint": "Dzielenie przez 100 to przesunięcie przecinka o 2 miejsca w lewo."
            },
            {
                "id": 10,
                "type": "fill-gap",
                "title": "Uzupełnij obliczenia",
                "parts": [
                    "$$67,2 \\div 0,24 = $$",
                    {
                        "id": "gap1",
                        "correctExact": 6720,
                        "placeholder": "?"
                    },
                    "$$ \\div $$",
                    {
                        "id": "gap2",
                        "correctExact": 24,
                        "placeholder": "?"
                    },
                    "$$ = 280$$"
                ],
                "explanation": "Przesuwamy przecinek w obu liczbach o 2 miejsca w prawo: $$67,2 \\div 0,24 = 6720 \\div 24 = 280$$"
            },
            {
                "id": 11,
                "type": "practice",
                "title": "Zadanie: Worek cukru",
                "scenario": "W trzech szklankach mieści się 0,63 kg mąki. Ile waży mąka w jednej szklance? Ile to gramów?",
                "instruction": "Oblicz wagę mąki w jednej szklance i wyraź w gramach.",
                "inputs": [
                    {"id": "kg", "label": "Waga jednej szklanki (w kg)", "placeholder": "wpisz wynik"},
                    {"id": "g", "label": "Waga jednej szklanki (w gramach)", "placeholder": "wpisz wynik"}
                ],
                "sampleAnswers": {
                    "title": "Przykładowe rozwiązanie",
                    "answers": [
                        "0,63 kg ÷ 3 = 0,21 kg",
                        "0,21 kg = 0,21 × 1000 g = 210 g"
                    ],
                    "tip": "Pamiętaj: 1 kg = 1000 g"
                },
                "correctAnswers": {
                    "kg": ["0,21", "0.21"],
                    "g": ["210"]
                }
            },
            {
                "id": 12,
                "type": "practice",
                "title": "Zadanie: Konwersja jednostek",
                "scenario": "Wyraź 0,3 m w centymetrach.",
                "instruction": "Pamiętaj, że 1 m = 100 cm.",
                "inputs": [
                    {"id": "cm", "label": "Wynik (w cm)", "placeholder": "wpisz wynik"}
                ],
                "sampleAnswers": {
                    "title": "Przykładowe rozwiązanie",
                    "answers": [
                        "0,3 m = 0,3 × 100 cm = 30 cm"
                    ],
                    "tip": "Mnożenie przez 100 to przesunięcie przecinka o 2 miejsca w prawo."
                },
                "correctAnswers": {
                    "cm": ["30"]
                }
            },
            {
                "id": 13,
                "type": "quiz",
                "title": "Quiz: Mnożenie i dzielenie",
                "questions": [
                    {
                        "question": "Ile wynosi $\\frac{3}{4} \\times \\frac{2}{3}$?",
                        "options": [
                            "$\\frac{1}{2}$",
                            "$\\frac{2}{3}$",
                            "$\\frac{3}{4}$",
                            "$\\frac{9}{8}$"
                        ],
                        "correctAnswer": 0,
                        "explanation": "$\\frac{3}{4} \\times \\frac{2}{3} = \\frac{6}{12} = \\frac{1}{2}$"
                    },
                    {
                        "question": "Ile wynosi $1,5 \\times 0,2$?",
                        "options": [
                            "0,03",
                            "0,3",
                            "3",
                            "30"
                        ],
                        "correctAnswer": 1,
                        "explanation": "$1,5 \\times 0,2 = 0,3$ (1+1=2 miejsca po przecinku: 15×2=30)"
                    },
                    {
                        "question": "Ile wynosi $5,6 \\div 0,7$?",
                        "options": [
                            "0,8",
                            "8",
                            "80",
                            "800"
                        ],
                        "correctAnswer": 1,
                        "explanation": "$5,6 \\div 0,7 = 56 \\div 7 = 8$"
                    },
                    {
                        "question": "Co otrzymamy dzieląc liczbę przez ułamek mniejszy od 1?",
                        "options": [
                            "Liczbę mniejszą niż dzielna",
                            "Liczbę większą niż dzielna",
                            "Zero",
                            "Zawsze 1"
                        ],
                        "correctAnswer": 1,
                        "explanation": "Dzielenie przez ułamek mniejszy od 1 (np. 1/2) to mnożenie przez liczbę większą od 1 (np. 2), więc wynik jest większy."
                    }
                ]
            },
            {
                "id": 14,
                "type": "test",
                "title": "Sprawdzian",
                "questions": [
                    {
                        "id": 1,
                        "question": "Oblicz: $$\\frac{2}{5} \\times \\frac{5}{6}$$",
                        "correctAnswer": "1/3",
                        "alternateAnswers": ["1/3", "⅓", "0,333", "0.333", "0,33", "0.33"],
                        "placeholder": "wpisz wynik"
                    },
                    {
                        "id": 2,
                        "question": "Oblicz: $$\\frac{3}{4} \\div \\frac{1}{2}$$",
                        "correctAnswer": "3/2",
                        "alternateAnswers": ["3/2", "1,5", "1.5", "1 1/2"],
                        "placeholder": "wpisz wynik"
                    },
                    {
                        "id": 3,
                        "question": "Oblicz: $$2,4 \\times 0,5$$",
                        "correctAnswer": "1,2",
                        "alternateAnswers": ["1,2", "1.2"],
                        "placeholder": "wpisz wynik"
                    },
                    {
                        "id": 4,
                        "question": "Oblicz: $$8,4 \\div 0,2$$",
                        "correctAnswer": "42",
                        "alternateAnswers": ["42", "42,0", "42.0"],
                        "placeholder": "wpisz wynik"
                    },
                    {
                        "id": 5,
                        "question": "Ile to jest $$3,7 \\times 100$$?",
                        "correctAnswer": "370",
                        "alternateAnswers": ["370", "370,0", "370.0"],
                        "placeholder": "wpisz wynik"
                    }
                ]
            },
            {
                "id": 15,
                "type": "summary",
                "title": "Podsumowanie",
                "content": "Świetna robota! Opanowałeś kluczowe umiejętności:",
                "keyPoints": [
                    "**Mnożenie ułamków:** zamień na niewłaściwe, skróć, pomnóż liczniki i mianowniki",
                    "**Dzielenie ułamków:** odwróć drugi ułamek i wykonaj mnożenie",
                    "**Mnożenie dziesiętnych:** pomnóż jak liczby naturalne, oddziel odpowiednią liczbę miejsc po przecinku",
                    "**Dzielenie dziesiętnych:** przesuń przecinek aby dzielnik był całkowity",
                    "**Przesuwanie przecinka:** mnożenie przez 10, 100... to przesunięcie w prawo, dzielenie w lewo"
                ],
                "nextSteps": "W kolejnej lekcji nauczysz się obliczać wartości wyrażeń arytmetycznych z wieloma działaniami. Poznasz zasady kolejności wykonywania działań i dowiesz się, jak prawidłowo używać nawiasów w obliczeniach."
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
    content = EXCLUDED.content;
