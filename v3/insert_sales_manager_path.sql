-- ==========================================
-- SKRYPT MIGRACYJNY: Akademia Menedżera Liniowego Sprzedaży
-- ==========================================
-- V4: Full 25-card Lesson 4.1 Update with new card types (diagnostic, action)

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
    30,
    500,
    'intermediate',
    $json$
    {
    "subtitle": "Moduł 4: Rozwijanie ludzi",
    "cards": [
        {
            "type": "hero",
            "title": "Jesteś Menedżerem? Teraz jesteś też Trenerem",
            "subtitle": "Zmiana Tożsamości",
            "content": "Większość menedżerów myśli, że ich rolą jest 'dowożenie wyników'. To prawda, ale tylko połowiczna. Jedynym sposobem na DŁUGOFALOWE wyniki jest rozwój ludzi, którzy te wyniki robią.",
            "icon": "users",
            "theme": "primary"
        },
        {
            "type": "concept",
            "title": "Definicja Sukcesu",
            "content": "Jako handlowiec, sukcesem była TWOJA sprzedaż. Jako menedżer, sukcesem jest WZROST sprzedaży Twoich ludzi.",
            "keyPoints": [
                "Stary cel: Być najlepszym graczem na boisku.",
                "Nowy cel: Sprawić, by inni grali lepiej od Ciebie.",
                "Narzędzie: Trening, Feedback, Coaching."
            ],
            "visual": {
                "type": "image",
                "src": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=800&q=80"
            }
        },
        {
            "type": "checklist",
            "title": "Autodiagnoza: Dziś Byłem...",
            "description": "Zaznacz, które czynności wykonałeś w ostatnim tygodniu. Zobaczysz, czy zarządzasz, czy trenujesz.",
            "items": [
                { "id": "1", "text": "Rozwiązałem problem za pracownika (Strażak)" },
                { "id": "2", "text": "Wypełniłem tabelki i raporty (Administrator)" },
                { "id": "3", "text": "Zadałem pytanie: 'Co zrobisz inaczej?' (Trener)" },
                { "id": "4", "text": "Pojechałem na wizytę, żeby TYLKO obserwować (Trener)" }
            ]
        },
        {
            "type": "quote",
            "content": "Najtrudniejsza rzecz dla menedżera to przestać grać i zacząć oglądać grę. Musisz pozwolić innym przejąć kontrolę, nawet jeśli zrobią to gorzej niż Ty.",
            "author": "Sir Alex Ferguson",
            "role": "Menedżer Manchester United"
        },
        {
            "type": "readiness",
            "title": "Poziomy Gotowości (R1-R4)",
            "description": "Zanim zaczniesz kogoś uczyć, musisz wiedzieć, czego on potrzebuje. Nie każdy jest taki sam."
        },
        {
            "type": "diagnostic",
            "title": "Diagnostyka: Przypadek Tomka",
            "description": "Tomek jest w firmie od miesiąca. Biega do klientów z wielką energią, ale często myli produkty. Kiedy zwracasz mu uwagę, mówi: 'Spoko szefie, ogarnę to!'.",
            "questions": [
                {
                    "id": "q1",
                    "text": "Jak oceniasz kompetencje Tomka?",
                    "answers": [
                        { "text": "Wysokie (wie co robi)", "score": "X" },
                        { "text": "Niskie (dopiero się uczy)", "score": "R1" }
                    ]
                },
                {
                    "id": "q2",
                    "text": "Jak oceniasz jego zaangażowanie?",
                    "answers": [
                        { "text": "Wysokie (chce mu się)", "score": "R1" },
                        { "text": "Niskie (jest zgaszony)", "score": "X" }
                    ]
                }
            ],
            "results": [
                {
                    "id": "R1",
                    "title": "To jest R1: Entuzjastyczny Debiutant",
                    "description": "Tomek 'nie wie, czego nie wie'. Ma dużo energii, ale mało wiedzy. Potrzebuje jasnych instrukcji, a nie coachingu.",
                    "color": "#fbbf24"
                },
                {
                    "id": "X",
                    "title": "Spróbuj ponownie",
                    "description": "To nie do końca tak. Tomek ma energię, ale brakuje mu wiedzy.",
                    "color": "#ef4444"
                }
            ]
        },
        {
            "type": "concept",
            "title": "R1: Instrukcja Obsługi",
            "content": "Pracownik R1 jest jak dziecko uczące się chodzić. Ma zapał, ale się przewraca.",
            "keyPoints": [
                "✅ Rób: Dawaj konkretne instrukcje (Krok po kroku).",
                "✅ Rób: Chwal za małe sukcesy.",
                "❌ Nie Rób: 'Zrób jak uważasz' (Delegowanie).",
                "❌ Nie Rób: Głęboki coaching (To go tylko zmyli)."
            ]
        },
        {
            "type": "diagnostic",
            "title": "Diagnostyka: Przypadek Anny",
            "description": "Anna pracuje 4 miesiące. Początkowy zapał minął. Klienci odmawiają, a ona mówi: 'Ten rynek jest trudny, nikt nie chce kupować'. Zaczyna spóźniać się z raportami.",
            "questions": [
                {
                    "id": "q1",
                    "text": "Co się stało z motywacją Anny?",
                    "answers": [
                        { "text": "Spadła (zderzenie z murem)", "score": "R2" },
                        { "text": "Jest wysoka, to tylko gorszy dzień", "score": "X" }
                    ]
                },
                {
                    "id": "q2",
                    "text": "A co z jej umiejętnościami?",
                    "answers": [
                        { "text": "Są już mistrzowskie", "score": "X" },
                        { "text": "Trochę umie, ale to za mało na sukces", "score": "R2" }
                    ]
                }
            ],
            "results": [
                {
                    "id": "R2",
                    "title": "To jest R2: Rozczarowany Adept",
                    "description": "To najtrudniejszy moment. Anna jest w 'Dolinie Rozpaczy'. Uświadomiła sobie, jak dużo jeszcze nie umie.",
                    "color": "#f59e0b"
                },
                {
                    "id": "X",
                    "title": "Spróbuj ponownie",
                    "description": "Anna ewidentnie straciła zapał (motywację). To typowe po kilku miesiącach.",
                    "color": "#ef4444"
                }
            ]
        },
        {
            "type": "concept",
            "title": "R2: Ratunek w Dolinie",
            "content": "To tu rezygnuje najwięcej handlowców. Twoją rolą jest być 'Ratownikiem'.",
            "keyPoints": [
                "Celem jest ODBUDOWA pewności siebie.",
                "Musisz łączyć Instruktaż (nadal się uczy) ze Wsparciem (potrzebuje otuchy).",
                "Pokaż perspektywę: 'To normalne, każdy przez to przechodził'."
            ]
        },
        {
            "type": "warning",
            "title": "Śmiertelny Błąd Menedżera",
            "description": "Najgorsze, co możesz zrobić pracownikowi R2, to zostawić go samego ('Już pracujesz 3 miesiące, radź sobie'). To pewna droga do utraty pracownika."
        },
        {
            "type": "concept",
            "title": "R3 i R4: Kompetentni",
            "content": "Kiedy pracownik przejdzie dolinę, staje się kompetentny.",
            "keyPoints": [
                "R3 (Praktyk): Umie, ale czasem wątpi. Potrzebuje WSPARCIA (pytań).",
                "R4 (Ekspert): Umie i chce. Potrzebuje AUTONOMII i nowych wyzwań."
            ]
        },
        {
            "type": "lightbulb",
            "title": "Pułapka Złotej Klatki",
            "content": "Dlaczego najlepsi (R4) odchodzą? Często dlatego, że menedżer nadal traktuje ich jak R1 (kontroluje, poucza).",
            "insight": "Ekspert potrzebuje powietrza. Jeśli będziesz go mikrozarządzać, udusisz jego motywację."
        },
        {
            "type": "dunning-kruger",
            "title": "Pułapka Ego: Efekt Krugera-Dunninga",
            "description": "Zobacz, jak pewność siebie zmienia się w czasie. Zauważasz tu swoich ludzi?"
        },
        {
            "type": "quiz",
            "title": "Gdzie jest Ignorant?",
            "questions": [
                {
                    "question": "Kto ma najwyższą (i nieuzasadnioną) pewność siebie?",
                    "options": [
                        "Osoba na Szczycie Głupoty",
                        "Ekspert",
                        "Osoba w Dolinie Rozpaczy"
                    ],
                    "correct": 0,
                    "explanation": "To paradoks: Najmniej wiedzą ci, którzy myślą, że wiedzą wszystko. To 'Szczyt Głupoty'."
                }
            ]
        },
        {
            "type": "lightbulb",
            "title": "Paradoks Eksperta",
            "content": "Zauważyłeś, że Twoi najlepsi ludzie często mówią: 'To nic wielkiego, po prostu mi się udało'?",
            "insight": "To Syndrom Oszusta. Eksperci często nie doceniają swoich umiejętności. Twoim zadaniem jest im o nich przypominać."
        },
        {
            "type": "action",
            "title": "Challenge: Doceń Eksperta",
            "description": "Nie czekaj na ocenę roczną. Zrób to teraz.",
            "content": "Hej, myślałem o tej sytuacji z wczoraj. Świetnie to rozegrałeś! Cieszę się, że mam Cię w zespole.",
            "actionType": "sms"
        },
        {
            "type": "cycle-b",
            "cycleType": "kolb",
            "title": "Silnik Treningu: Cykl Kolba",
            "description": "Jak zamienić doświadczenie w wiedzę? Oto mechanizm, którego będziesz używać codziennie."
        },
        {
            "type": "concept",
            "title": "Krok 1: Doświadczenie",
            "content": "Żeby się uczyć, pracownik musi coś ZROBIĆ. Ale uwaga: Ty musisz to WIDZIEĆ.",
            "keyPoints": [
                "Nie możesz trenować na podstawie 'opowieści' pracownika ('Klient był trudny').",
                "Musisz być świadkiem (obserwacja w terenie).",
                "To jest paliwo do procesu."
            ]
        },
        {
            "type": "concept",
            "title": "Krok 2: Refleksja",
            "content": "To najważniejszy moment. Większość menedżerów go pomija i od razu mówi: 'Zrobiłeś to źle'.",
            "remember": {
                "text": "BŁĄD: Mówienie pracownikowi, co zrobił źle.\nSUKCES: Sprawienie, by SAM to zauważył."
            }
        },
        {
            "type": "habit",
            "title": "Narzędzie: 5 Pytań Refleksyjnych",
            "description": "Jak wywołać refleksję? Nie wymyślaj koła na nowo. Użyj tych pytań:",
            "habits": [
                { "id": "q1", "text": "Jak się czujesz po tej wizycie?" },
                { "id": "q2", "text": "Jaki miałeś cel?" },
                { "id": "q3", "text": "Co poszło dokładnie tak, jak chciałeś?" },
                { "id": "q4", "text": "Co Cię zaskoczyło / co poszło nie tak?" },
                { "id": "q5", "text": "Co zrobisz inaczej następnym razem?" }
            ]
        },
        {
            "type": "concept",
            "title": "Krok 3: Wnioski (Teoria)",
            "content": "Dopiero gdy pracownik przeanalizuje błąd, jest gotowy na Twoją wiedzę.",
            "keyPoints": [
                "Teraz możesz powiedzieć: 'Z mojego doświadczenia wynika...'",
                "Teraz możesz pokazać standard firmowy.",
                "To jest moment na 'nauczanie'."
            ]
        },
        {
            "type": "concept",
            "title": "Krok 4: Eksperyment",
            "content": "Wnioski nic nie dają, jeśli nie zostaną wdrożone.",
            "keyPoints": [
                "Trening musi kończyć się planem: 'Na następnej wizycie sprawdzę X'.",
                "Cykl się zamyka - nowe działanie to nowe Doświadczenie."
            ]
        },
        {
            "type": "story",
            "title": "Case Study: Zmarnowany Trening",
            "scenario": "Menedżer Artur pojechał z handlowcem. Po wizycie powiedział: 'Słuchaj, za szybko podałeś cenę. Nie zbadałeś potrzeb. Następnym razem pytaj więcej.' Handlowiec pokiwał głową.",
            "consequences": [
                "Menedżer pominął etap Refleksji.",
                "Handlowiec poczuł się oceniony, a nie nauczony.",
                "Wniosek Artura („pytaj więcej”) wpadł jednym uchem, a wypadł drugim."
            ],
            "lesson": {
                "heading": "Lekcja",
                "text": "Gdyby Artur zapytał: 'Jak myślisz, dlaczego klient tak szybko zapytał o cenę?', handlowiec sam doszedłby do wniosku, że nie zbudował wartości."
            }
        },
        {
            "type": "quiz",
            "title": "Sprawdź Wiedzę",
            "questions": [
                {
                    "question": "Jaki jest główny cel menedżera?",
                    "options": [
                        "Rozwój ludzi, by osiągali wyniki",
                        "Osobiste dowożenie sprzedaży"
                    ],
                    "correct": 0,
                    "explanation": "Twoim produktem jest Twój zespół."
                },
                {
                    "question": "Co robisz z pracownikiem R2 (zniechęconym)?",
                    "options": [
                        "Dajesz mu wolną rękę",
                        "Łączysz wsparcie emocjonalne z instrukcją"
                    ],
                    "correct": 1,
                    "explanation": "R2 potrzebuje 'Ratownika' - zarówno merytoryki, jak i otuchy."
                },
                {
                    "question": "Kiedy dajesz feedback merytoryczny?",
                    "options": [
                        "Od razu po błędzie",
                        "Dopiero po etapie Refleksji pracownika"
                    ],
                    "correct": 1,
                    "explanation": "Zasada: Najpierw zapytaj, potem powiedz. Cykl Kolba."
                }
            ]
        },
        {
            "type": "summary",
            "title": "Twój Nowy System",
            "recap": [
                "Diagnozuj (R1-R4) - nie strzelaj na oślep.",
                "Uważaj na Ego (Dunning-Kruger).",
                "Uruchamiaj Refleksję (Cykl Kolba).",
                "Bądź Trenerem, nie Sędzią."
            ],
            "badge": {
                "title": "Cerytfikat Trenera",
                "xp": 500
            },
            "nextSteps": "Psychologię masz opanowaną. W następnej lekcji dostaniesz twardy proces: Jak zaplanować dzień OJT krok po kroku."
        }
    ]
    }$json$::jsonb,
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
    $json$
    {
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
    }$json$::jsonb,
    'd0eebc99-9c0b-4ef8-bb6d-6bb9bd380a44',
    'sales-manager'
) ON CONFLICT (lesson_id) DO UPDATE SET
    content = EXCLUDED.content,
    title = EXCLUDED.title,
    xp_reward = EXCLUDED.xp_reward,
    module_id = EXCLUDED.module_id;
