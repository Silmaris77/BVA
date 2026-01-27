-- ==========================================
-- SKRYPT MIGRACYJNY: Akademia Menedżera Liniowego Sprzedaży
-- ==========================================
-- FIXED: Using valid UUIDs for module IDs
-- CLEANUP: Deleting legacy path 'akademia-menedzera'

-- 0. CLEANUP (Usuwamy starą wersję ścieżki, jeśli istnieje)
DELETE FROM learning_paths WHERE path_slug = 'akademia-menedzera';

-- 1. Zdefiniowanie zmiennych dla ID modułów (UUID v4)
-- Moduł 1: a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11
-- Moduł 2: b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22
-- Moduł 3: c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a33
-- Moduł 4: d0eebc99-9c0b-4ef8-bb6d-6bb9bd380a44 (CORE - Trening on-the-job)
-- Moduł 5: e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a55
-- Moduł 6: f0eebc99-9c0b-4ef8-bb6d-6bb9bd380a66
-- Moduł 7: a1eebc99-9c0b-4ef8-bb6d-6bb9bd380a77

-- 2. INSERTY MODUŁÓW

-- Moduł 1
INSERT INTO modules (id, title, description, track, display_order) VALUES ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Moduł 1: Rola menedżera i fundamenty', 'Przestawienie myślenia z „najlepszy handlowiec” na „lider wyników zespołu”.', 'sales-manager', 1) ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description;

-- Moduł 2
INSERT INTO modules (id, title, description, track, display_order) VALUES ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 'Moduł 2: Cele, wyniki i egzekucja', 'Zarządzanie wynikiem przez działania zespołu, a nie przez presję.', 'sales-manager', 2) ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description;

-- Moduł 3
INSERT INTO modules (id, title, description, track, display_order) VALUES ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a33', 'Moduł 3: Codzienne zarządzanie zespołem', 'Uporządkowanie codzienności: spotkania, komunikacja, priorytety.', 'sales-manager', 3) ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description;

-- Moduł 4 (Trening on-the-job)
INSERT INTO modules (id, title, description, track, display_order) VALUES ('d0eebc99-9c0b-4ef8-bb6d-6bb9bd380a44', 'Moduł 4: Rozwijanie ludzi – Trening On-the-Job', 'Jak rozwijać kompetencje handlowców w realnej pracy (Metodyka treningu on-the-job).', 'sales-manager', 4) ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description;

-- Moduł 5
INSERT INTO modules (id, title, description, track, display_order) VALUES ('e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a55', 'Moduł 5: Feedback i trudne rozmowy', 'Narzędzia do rozmów korygujących i motywujących.', 'sales-manager', 5) ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description;

-- Moduł 6
INSERT INTO modules (id, title, description, track, display_order) VALUES ('f0eebc99-9c0b-4ef8-bb6d-6bb9bd380a66', 'Moduł 6: Motywacja i zaangażowanie', 'Utrzymanie energii zespołu i zapobieganie wypaleniu.', 'sales-manager', 6) ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description;

-- Moduł 7
INSERT INTO modules (id, title, description, track, display_order) VALUES ('a1eebc99-9c0b-4ef8-bb6d-6bb9bd380a77', 'Moduł 7: Samodzielny, dojrzały zespół', 'Budowanie zespołu, który nie potrzebuje ciągłej kontroli.', 'sales-manager', 7) ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description;


-- 3. INSERTY LEKCJI (Dla Modułu 4)

INSERT INTO lessons (
    lesson_id,
    title,
    description,
    duration_minutes,
    xp_reward,
    difficulty,
    content,
    module_id,
    track
) VALUES (
    'sm-m4-l1-psychologia',
    'Jak ludzie się uczą i jaka jest rola menedżera',
    'Zrozum psychologię uczenia się dorosłych, 4 poziomy kompetencji i zmień swoje nastawienie z naprawiania na rozwijanie.',
    15,
    300,
    'intermediate',
    '{
    "subtitle": "Moduł 4: Rozwijanie ludzi",
    "cards": [
        {
            "type": "intro",
            "title": "Mindset: Ogrodnik, nie Mechanik",
            "description": "Wielu menedżerów myśli, że pracownik to maszyna, którą trzeba naprawić szybkim feedbackiem. To błąd. Rozwój to proces organiczny, który wymaga warunków, a nie tylko instrukcji."
        },
        {
            "type": "concept",
            "title": "Menedżer jako Trener",
            "content": "Rola menedżera ewoluuje. Oprócz celów biznesowych, Twoim zadaniem jest:",
            "keyPoints": [
                "Odkrywaniem pasji i mocnych stron pracowników",
                "Współtworzeniem planów rozwoju",
                "Dostarczaniem narzędzi i wiedzy",
                "Budowaniem bezpiecznego środowiska do nauki",
                "Narzucaniem tempa rozwoju (akceleracja)"
            ],
            "visual": {
                "type": "image",
                "src": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80"
            }
        },
        {
            "type": "learning-path",
            "title": "4 Poziomy Kompetencji",
            "description": "Zanim zaczniesz kogoś uczyć, musisz wiedzieć, gdzie on jest. Kliknij, aby zobaczyć etapy.",
            "levels": [
                {
                    "stage": 0,
                    "title": "START",
                    "subtitle": "Nieświadoma niekompetencja",
                    "details": "„Nie wiem, że nie wiem”. Stan, w którym pracownik nie jest świadom popełnianych błędów. Potrzeba rozwoju jest tutaj niska, bo nie widać problemu.",
                    "status": "completed",
                    "color": "#9ca3af"
                },
                {
                    "stage": 1,
                    "title": "UŚWIADOMIENIE",
                    "subtitle": "Świadoma niekompetencja",
                    "details": "„Wiem, czego nie wiem”. Moment zderzenia z rzeczywistością. Pracownik widzi swoje braki. To budzi motywację, ale może też rodzić frustrację.",
                    "status": "current",
                    "color": "#fbbf24"
                },
                {
                    "stage": 2,
                    "title": "PRAKTYKA",
                    "subtitle": "Świadoma kompetencja",
                    "details": "„Wiem, co wiem”. Pojawiają się pierwsze rezultaty, ale wymagają one dużego skupienia i wysiłku. Działanie nie jest jeszcze płynne.",
                    "status": "locked",
                    "color": "#34d399"
                },
                {
                    "stage": 3,
                    "title": "MISTRZOSTWO",
                    "subtitle": "Nieświadoma kompetencja",
                    "details": "„Nie wiem, co wiem”. Pełny automatyzm. Pracownik działa intuicyjnie, szybko i bezbłędnie. Wiedza stała się nawykiem.",
                    "status": "locked",
                    "color": "#00d4ff"
                }
            ]
        },
        {
            "type": "readiness",
            "title": "Poziomy Gotowości (R1-R4)",
            "description": "Każdy pracownik może być na innym poziomie gotowości w zależności od zadania. Poznaj model Przywództwa Sytuacyjnego."
        },
        {
            "type": "dunning-kruger",
            "title": "Pułapka: Efekt Krugera-Dunninga",
            "description": "Dlaczego najsłabsi handlowcy są często najbardziej pewni siebie?",
            "points": [
                {
                    "stage": 0,
                    "title": "Szczyt Głupoty",
                    "label": "Terytorium Ignoranta",
                    "description": "Wysoka pewność, znikoma wiedza",
                    "details": "„Sprzedaż? To proste!” Nowy handlowiec często przecenia swoje siły, bo nie wie, czego nie wie.",
                    "color": "#ef4444"
                },
                {
                    "stage": 1,
                    "title": "Dolina Rozpaczy",
                    "label": "Szok Rzeczywistości",
                    "description": "Upadek pewności",
                    "details": "Pierwsze porażki. Uświadamia sobie, jak trudna jest ta praca. Pewność siebie szoruje o dno.",
                    "color": "#f59e0b"
                },
                {
                    "stage": 2,
                    "title": "Droga Oświecenia",
                    "label": "Nauka i Praktyka",
                    "description": "Odbudowa pewności",
                    "details": "Zaczyna rozumieć mechanizmy. Uczy się na błędach. Pewność rośnie, ale tym razem ma solidne podstawy.",
                    "color": "#10b981"
                },
                {
                    "stage": 3,
                    "title": "Płaskowyż Stabilności",
                    "label": "Ekspert",
                    "description": "Kompetencja i pokora",
                    "details": "Wie, co robi. Działa intuicyjnie. Rozumie też, że zawsze można się czegoś jeszcze nauczyć.",
                    "color": "#3b82f6"
                }
            ]
        },
        {
            "type": "cycle-b",
            "cycleType": "kolb",
            "title": "Cykl Kolba: Jak uczy się mózg?",
            "description": "Dorośli uczą się najskuteczniej przechodząc przez 4 etapy. Zobacz interaktywny model.",
            "steps": [
                {
                    "id": 1,
                    "title": "Doświadczenie",
                    "description": "Konkretne zdarzenie, np. rozmowa z klientem. Co się stało? - to punkt wyjścia.",
                    "icon": "target",
                    "color": "#00d4ff"
                },
                {
                    "id": 2,
                    "title": "Refleksja",
                    "description": "Analiza tego zdarzenia. Dlaczego tak poszło? Co czułem? Dystans do emocji.",
                    "icon": "brain",
                    "color": "#7dd956"
                },
                {
                    "id": 3,
                    "title": "Teoria (Wniosek)",
                    "description": "Szukanie reguł. Co zrobię inaczej? Łączenie praktyki z modelem działania.",
                    "icon": "lightbulb",
                    "color": "#ffd700"
                },
                {
                    "id": 4,
                    "title": "Eksperyment",
                    "description": "Testowanie nowego podejścia w praktyce. Sprawdzam! Cykl się zamyka.",
                    "icon": "check",
                    "color": "#ff0055"
                }
            ]
        },
        {
            "type": "story",
            "title": "Błąd Młodego Menedżera",
            "scenario": "Tomek, świeżo upieczony lider, próbował uczyć doświadczonego handlowca (Jana) metodą „mikrozarządzania” – mówił mu dokładnie, co ma robić w każdej minucie.",
            "consequences": [
                "Jan poczuł się niedoceniony (utrata motywacji).",
                "Wyniki Jana spadły, mimo dobrych intencji Tomka.",
                "Relacja uległa pogorszeniu."
            ],
            "lesson": {
                "heading": "Wniosek",
                "text": "Tomek użył stylu dyrektywnego wobec pracownika na poziomie Świadomej Kompetencji. To błąd w dopasowaniu stylu do poziomu gotowości."
            }
        },
        {
            "type": "quiz",
            "title": "Sprawdź wiedzę",
            "questions": [
                {
                    "question": "Na którym etapie pracownik wie, że czegoś nie potrafi i to go motywuje?",
                    "options": [
                        "Nieświadoma niekompetencja",
                        "Świadoma niekompetencja",
                        "Nieświadoma kompetencja"
                    ],
                    "correct": 1,
                    "explanation": "Świadoma niekompetencja to moment, w którym uświadamiamy sobie braki, co jest impulsem do nauki."
                },
                {
                    "question": "Co charakteryzuje efekt Krugera-Dunninga?",
                    "options": [
                        "Eksperci przeceniają się",
                        "Nowicjusze przeceniają swoje umiejętności",
                        "Wszyscy oceniają się obiektywnie"
                    ],
                    "correct": 1,
                    "explanation": "Efekt ten polega na tym, że osoby o niskich kompetencjach nie dostrzegają swoich błędów i przeceniają swoją wiedzę."
                }
            ]
        },
        {
            "type": "summary",
            "title": "Fundamenty Zbudowane",
            "recap": [
                "Przestajesz być Mechanikiem od naprawiania, stajesz się Ogrodnikiem tworzącym warunki.",
                "Rozumiesz mechanizm 4 Poziomów Kompetencji i Efekt Krugera-Dunninga.",
                "Wiesz, że bez Refleksji (Cykl Kolba) nie ma trwałej nauki."
            ],
            "badge": {
                "title": "Psychologia Rozwoju",
                "xp": 300
            },
            "nextSteps": "W następnej lekcji przełożymy tę teorię na konkretne narzędzie: Trening On-the-Job."
        }
    ]
    }'::jsonb,
    'd0eebc99-9c0b-4ef8-bb6d-6bb9bd380a44',
    'sales-manager'
),
(
    'sm-m4-l2-definicja-ojt',
    'Czym naprawdę jest trening on-the-job?',
    'Dowiedz się, czym różni się OJT od zwykłej wizyty handlowej i poznaj strukturę procesu.',
    20,
    300,
    'intermediate',
    '{
    "subtitle": "Moduł 4: Rozwijanie ludzi",
    "cards": [
        {
            "type": "intro",
            "title": "Wizyta vs Trening",
            "description": "Wielu menedżerów jeździ z handlowcami w te-ren, ale rzadko kto prowadzi prawdziwy trening. Czy wiesz, jaka jest różnica?"
        },
        {
            "type": "comparison",
            "title": "Wspólna wizyta vs OJT",
            "description": "Zobacz różnicę w intencji i przebiegu:",
            "leftTitle": "Zwykła wspólna wizyta",
            "rightTitle": "Trening On-the-Job (OJT)",
            "items": [
                {
                    "left": "Cel: Dowieźć sprzedaż za wszelką cenę.",
                    "right": "Cel: Rozwinąć konkretną umiejętność (sprzedaż jest skutkiem)."
                },
                {
                    "left": "Menedżer przejmuje stery, gdy robi się trudno.",
                    "right": "Menedżer pozwala pracownikowi działać (nawet z błędami), o ile nie psuje to relacji."
                },
                {
                    "left": "Feedback jest chaotyczny, w windzie.",
                    "right": "Feedback jest zaplanowany, po wizycie, oparty na faktach."
                }
            ]
        },
        {
            "type": "concept",
            "title": "Struktura Cyklu OJT",
            "content": "Prawdziwy trening składa się z 3 etapów:\\n\\n1.  🕐 **PRZED (Odprawa):** Ustalenie JEDNEGO celu rozwojowego. (Nad czym dziś pracujemy?)\\n2.  🕑 **W TRAKCIE (Obserwacja):** Menedżer milczy i notuje fakty. Pracownik gra pierwsze skrzypce.\\n3.  🕒 **PO (Analiza):** Rozmowa rozwojowa (Refleksja + Wnioski)."
        },
        {
            "type": "summary",
            "title": "Podsumowanie",
            "recap": [
                "OJT to proces rozwojowy, a nie tylko wspólna jazda.",
                "Cel OJT to rozwój kompetencji, a nie tylko wynik tu i teraz.",
                "Struktura: Odprawa -> Obserwacja -> Analiza."
            ],
            "badge": {
                "title": "Definicja OJT",
                "xp": 300
            },
            "nextSteps": "W kolejnej lekcji nauczysz się, jak wybrać ten JEDEN cel rozwojowy, żeby nie przytłoczyć pracownika."
        }
    ]
    }'::jsonb,
    'd0eebc99-9c0b-4ef8-bb6d-6bb9bd380a44',
    'sales-manager'
) ON CONFLICT (lesson_id) DO UPDATE SET
    content = EXCLUDED.content,
    title = EXCLUDED.title,
    xp_reward = EXCLUDED.xp_reward,
    module_id = EXCLUDED.module_id;
