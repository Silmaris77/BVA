-- SQL script to insert OJT Lesson 2 - Cards 21-29
-- PART 5: Data, Story, Quiz, Habit, Checklist, Lightbulb, Test, Achievement, Ending
-- This is the final part - complete lesson!

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
    'ojt_lesson_2_model_part5',  -- Temporary ID for testing
    'OJT Lesson 2 - Cards 21-29 (FINAL)',
    'Test cards 21-29 (Data, Story, Quiz, Habit, Checklist, Lightbulb, Test, Achievement, Ending)',
    'beginner',
    25,
    300,
    '{
      "cards": [
        {
          "id": 21,
          "type": "data",
          "title": "Jak często robić trening OJT?",
          "stats": [
            {
              "value": "1x/tydzień",
              "label": "Minimalną częstotliwość dla efektywnego rozwoju"
            },
            {
              "value": "2-3x/miesiąc",
              "label": "Optymalną intensywność dla utrwalenia umiejętności"
            },
            {
              "value": "1x/kwartał",
              "label": "To za rzadko - efekt rozwoju jest znikomy"
            }
          ],
          "callout": {
            "type": "info",
            "title": "Kluczowy wniosek:",
            "text": "Trening OJT wymaga REGULARNOŚCI. Lepiej 1 dzień co 2 tygodnie przez 3 miesiące niż 3 dni z rzędu raz na pół roku. Mózg potrzebuje czasu na przetworzenie feedbacku i wypróbowanie nowych zachowań."
          },
          "timeline": {
            "title": "Typowy harmonogram rozwoju:",
            "stages": [
              {
                "title": "Nowy pracownik (0-3 miesiące)",
                "frequency": "2-3 razy w tygodniu",
                "description": "Intensywny trening podstawowych umiejętności",
                "color": "green"
              },
              {
                "title": "Rozwijający się pracownik (3-12 miesięcy)",
                "frequency": "1 raz w tygodniu",
                "description": "Praca nad konkretnymi kompetencjami (np. zamykanie, obsługa obiekcji)",
                "color": "blue"
              },
              {
                "title": "Doświadczony pracownik (1+ rok)",
                "frequency": "2-3 razy w miesiącu",
                "description": "Doskonalenie zaawansowanych technik, rozwijanie nowych obszarów",
                "color": "gold"
              }
            ]
          },
          "sources": "Źródła: ATD Coaching Best Practices 2024, Harvard Business Review \\"Frequency of Coaching\\"",
          "estimated_seconds": 140,
          "xp_points": 10
        },
        {
          "id": 22,
          "type": "story",
          "title": "Przykład: Dobry vs Zły Plan Wdrożeniowy",
          "scenarios": [
            {
              "type": "bad",
              "title": "❌ ŹLE (Ogólnikowe deklaracje)",
              "dialogue": [
                {"speaker": "Menedżer", "text": "Co wynosisz z dzisiejszego treningu?"},
                {"speaker": "Handlowiec", "text": "Muszę popracować nad zadawaniem pytań i lepiej słuchać klienta."},
                {"speaker": "Menedżer", "text": "Super, to się tym zajmij. Powodzenia!"}
              ],
              "consequences": [
                "Tydzień później nic się nie zmieniło.",
                "\\"Popracować nad pytaniami\\" to nie plan, to deklaracja.",
                "Brak konkretów = brak zmian."
              ]
            },
            {
              "type": "good",
              "title": "✅ DOBRZE (SMART plan wdrożeniowy)",
              "dialogue": [
                {"speaker": "Menedżer", "text": "Co KONKRETNIE zastosujesz w najbliższym tygodniu?"},
                {"speaker": "Handlowiec", "text": "W każdej rozmowie z klientem zadam min. 3 pytania otwarte zanim przejdę do prezentacji produktu."},
                {"speaker": "Menedżer", "text": "Świetnie! Możesz to zapisać? A jak będziesz mierzył postęp?"},
                {"speaker": "Handlowiec", "text": "(pisze) Po każdej rozmowie zaznaczę w CRM czy zadałem 3+ pytania. W piątek wyślę Ci raport."},
                {"speaker": "Menedżer", "text": "Okej. A co zrobisz, gdy zapomnisz i przeskoczysz od razu do oferty?"},
                {"speaker": "Handlowiec", "text": "Zatrzymam się i powiem: \\"Zanim przejdę dalej, chciałbym zrozumieć Państwa sytuację - jak teraz rozwiązujecie X?\\""},
                {"speaker": "Menedżer", "text": "Doskonale. Umówmy się na feedback za tydzień - zajrzymy do CRM i omówimy jak poszło."}
              ],
              "consequences": [
                "Tydzień później: 12/15 rozmów z min. 3 pytaniami otwarymi.",
                "W 3 rozmowach zapomniał, ale użył techniki \\"cofnięcia się\\".",
                "Konwersja wzrosła o 18%.",
                "**Konkretny plan = mierzalny efekt.**"
              ]
            }
          ],
          "lesson": "Dobry plan wdrożeniowy to: 1-3 konkretne zachowania + sposób mierzenia + plan na wypadek zapomnienia + termin sprawdzenia postępu. Bez tego feedback = strata czasu.",
          "estimated_seconds": 180,
          "xp_points": 10
        },
        {
          "id": 23,
          "type": "quiz",
          "title": "Sprawdź swoją wiedzę: Podsumowanie Modelu OJT",
          "questions": [
            {
              "id": 1,
              "text": "Jaka jest GŁÓWNA różnica między treningiem OJT a tradycyjnym szkoleniem?",
              "options": [
                {"letter": "A", "text": "OJT jest tańszy i szybszy", "correct": false},
                {"letter": "B", "text": "Uczysz się PRACUJĄC, nie przerywasz pracy by się uczyć", "correct": true},
                {"letter": "C", "text": "OJT wymaga mniej przygotowania", "correct": false}
              ],
              "explanation": "W OJT nauka jest integralną częścią pracy - nie odrywasz pracownika od zadań, tylko przekształcasz zadania w okazję do rozwoju. To zasadnicza zmiana paradygmatu."
            },
            {
              "id": 2,
              "text": "Który etap OJT powtarza się 3-5 razy dziennie w cyklu?",
              "options": [
                {"letter": "A", "text": "Rozmowa na początku dnia + Podsumowanie dnia", "correct": false},
                {"letter": "B", "text": "Odprawa → Obserwacja → Analiza (dla każdego zadania)", "correct": true},
                {"letter": "C", "text": "Wszystkie 5 etapów powtarzamy w kółko", "correct": false}
              ],
              "explanation": "Etapy 2-3-4 (Odprawa-Obserwacja-Analiza) tworzą cykl powtarzalny dla każdej rozmowy/zadania. Etap 1 (Start) i 5 (Podsumowanie) ramują cały dzień."
            },
            {
              "id": 3,
              "text": "Jaka jest ZŁOTA ZASADA feedbacku w treningu OJT?",
              "options": [
                {"letter": "A", "text": "Zawsze zacznij od pozytywów (metoda kanapki)", "correct": false},
                {"letter": "B", "text": "Pytaj, nie mów - pomóż pracownikowi samemu odkryć wnioski", "correct": true},
                {"letter": "C", "text": "Dawaj feedback natychmiast po każdym błędzie", "correct": false}
              ],
              "explanation": "\\"Pytaj, nie mów\\" to fundament OJT. 80% czasu pracownik analizuje sam, 20% Ty uzupełniasz perspektywą. Ludzie wspierają świat, który sami stworzyli."
            }
          ],
          "estimated_seconds": 180,
          "xp_points": 20
        },
        {
          "id": 24,
          "type": "habit",
          "title": "Zbuduj swoje nawyki trenera OJT",
          "instruction": "Wybierz **1-2 nawyki**, które chcesz wdrożyć w ciągu najbliższych 30 dni. Zaznacz te, które są dla Ciebie priorytetem:",
          "habits": [
            {
              "id": "habit1",
              "icon": "🗓️",
              "title": "Regularny harmonogram OJT",
              "description": "Zaplanować minimum 1 dzień OJT tygodniowo z każdym kluczowym pracownikiem przez najbliższe 3 miesiące",
              "goal": "Systematyczność, nie jednorazowe akcje"
            },
            {
              "id": "habit2",
              "icon": "📝",
              "title": "Notowanie faktów, nie interpretacji",
              "description": "Podczas obserwacji zapisywać TYLKO to co widzę i słyszę - cytaty, zachowania, reakcje. Zero ocen.",
              "goal": "Obiektywny feedback oparty na faktach"
            },
            {
              "id": "habit3",
              "icon": "❓",
              "title": "5 pytań zanim dam radę",
              "description": "W każdej analizie zadać minimum 5 pytań coachingowych ZANIM powiem co pracownik powinien zrobić",
              "goal": "Rozwijać samodzielność zamiast zależność ode mnie"
            },
            {
              "id": "habit4",
              "icon": "✅",
              "title": "Konkretny plan wdrożeniowy",
              "description": "Kończyć każdą sesję OJT spisanym planem: 1-3 zachowania + sposób mierzenia + termin sprawdzenia",
              "goal": "Przekształcić feedback w realne zmiany"
            }
          ],
          "tip": "Wybierz maksymalnie 2 nawyki. Lepiej wdrożyć 2 w 100% niż 4 w 25%. Po 30 dniach oceń postęp i rozważ dodanie kolejnego.",
          "estimated_seconds": 150,
          "xp_points": 10
        },
        {
          "id": 25,
          "type": "checklist",
          "title": "Twoja Checklista Trenera OJT",
          "instruction": "Użyj tej checklisty przed, w trakcie i po każdej sesji OJT:",
          "sections": [
            {
              "id": "before",
              "title": "📋 Przed wspólnym dniem pracy:",
              "items": [
                {"id": "check1", "text": "Ustalony cel rozwojowy na dzisiejszą sesję (1-2 umiejętności)"},
                {"id": "check2", "text": "Przygotowany plan dnia (lista klientów/zadań)"},
                {"id": "check3", "text": "Notatnik gotowy do zbierania faktów"}
              ]
            },
            {
              "id": "start",
              "title": "🤝 Na początku dnia (Etap 1):",
              "items": [
                {"id": "check4", "text": "Sprzedałem ideę treningu (dlaczego to się opłaca)"},
                {"id": "check5", "text": "Zawarliśmy kontrakt (role, zasady, sygnały pomocy)"},
                {"id": "check6", "text": "Wspólnie ustaliliśmy cele rozwojowe"}
              ]
            },
            {
              "id": "briefing",
              "title": "🔄 Przed każdą rozmową/zadaniem (Etap 2):",
              "items": [
                {"id": "check7", "text": "Przypomnieliśmy cele rozwojowe"},
                {"id": "check8", "text": "Przeanalizowaliśmy sytuację/kontekst"},
                {"id": "check9", "text": "Pracownik ma plan działania"},
                {"id": "check10", "text": "Jeśli potrzeba - pokazałem demonstrację"}
              ]
            },
            {
              "id": "observation",
              "title": "👀 Podczas obserwacji (Etap 3):",
              "items": [
                {"id": "check11", "text": "Zachowuję rolę obserwatora (minimalna aktywność)"},
                {"id": "check12", "text": "Notuję FAKTY (cytaty, zachowania), nie interpretacje"},
                {"id": "check13", "text": "Wchodzę TYLKO zgodnie z kontraktem"}
              ]
            },
            {
              "id": "analysis",
              "title": "💬 Po każdej rozmowie/zadaniu (Etap 4):",
              "items": [
                {"id": "check14", "text": "Zacząłem od ODCZUĆ pracownika"},
                {"id": "check15", "text": "Przypomniałem CELE tej rozmowy"},
                {"id": "check16", "text": "Przeanalizowaliśmy PRZEBIEG (co dobrze, co trudne)"},
                {"id": "check17", "text": "Zadałem pytania o ALTERNATYWY (co inaczej)"},
                {"id": "check18", "text": "Pracownik sformułował konkretne WNIOSKI"}
              ]
            },
            {
              "id": "summary",
              "title": "🏁 Na koniec dnia (Etap 5):",
              "items": [
                {"id": "check19", "text": "Rozliczyliśmy cele całego dnia"},
                {"id": "check20", "text": "Ustaliliśmy 1-3 konkretne zachowania do wdrożenia"},
                {"id": "check21", "text": "Zapisaliśmy plan wdrożeniowy (co, jak mierzyć, kiedy sprawdzić)"},
                {"id": "check22", "text": "Umówiliśmy kolejną sesję OJT"}
              ]
            }
          ],
          "estimated_seconds": 180,
          "xp_points": 15
        },
        {
          "id": 26,
          "type": "lightbulb",
          "icon": "💡",
          "title": "Ostatnie Zrozumienie: OJT to Inwestycja, nie Koszt",
          "content": "Słyszysz czasem: **\\"Nie mam czasu na OJT - mam cele do zrealizowania\\"**?\\n\\nTo jak powiedzieć: \\"Nie mam czasu ostrzyć piły - mam drzewo do ścięcia\\". Oto liczby, które zmienią Twoją perspektywę:",
          "comparison": {
            "headers": ["❌ BEZ OJT (praca tradycyjna)", "✅ Z OJT (systematyczny rozwój)"],
            "rows": [
              {
                "wrong": "**Czas onboardingu:** 6-9 miesięcy do pełnej produktywności",
                "right": "**Czas onboardingu:** 3-4 miesiące do pełnej produktywności"
              },
              {
                "wrong": "**Błędy:** Pracownik uczy się na własnych błędach (kosztownych)",
                "right": "**Błędy:** Minimalizowane przez feedback w czasie rzeczywistym"
              },
              {
                "wrong": "**Rozwój:** Losowy, zależny od doświadczeń",
                "right": "**Rozwój:** Kierunkowy, 4x szybszy"
              },
              {
                "wrong": "**Twój czas:** Ratowanie sytuacji, gaszenie pożarów",
                "right": "**Twój czas:** Inwestycja w kompetencje = mniej pożarów"
              },
              {
                "wrong": "**Wynik:** Zespół zależny od Ciebie",
                "right": "**Wynik:** Zespół samodzielny i rosnący"
              }
            ]
          },
          "caseStudy": {
            "title": "📊 ROI treningu OJT (przykład rzeczywisty):",
            "company": "Zespół sprzedażowy 10 osób, menedżer Tomasz:",
            "investment": [
              "1 dzień/tydzień OJT z każdym handlowcem (rotacja)",
              "52 dni OJT rocznie = ~10% czasu Tomasza"
            ],
            "results": [
              "Średnia konwersja wzrosła z 18% do 27% (+50%)",
              "Średni deal size wzrósł o 15% (lepsza kvalifikacja)",
              "Rotacja zespołu spadła z 25% do 8% rocznie",
              "Tomasz przestał gasić pożary - zespół rozwiązuje problemy sam"
            ],
            "roi": "450% - każda złotówka zainwestowana w OJT wróciła jako 4.5 zł zysku"
          },
          "quote": "\\"Jeśli myślisz, że szkolenie jest drogie - spróbuj ignorancji\\"",
          "quoteAuthor": "Derek Bok, były rektor Uniwersytetu Harvarda",
          "estimated_seconds": 150,
          "xp_points": 10
        },
        {
          "id": 27,
          "type": "test",
          "icon": "🏆",
          "title": "Test Końcowy: Model Treningu OJT",
          "description": "Sprawdź swoją wiedzę z całej lekcji. Musisz uzyskać minimum **80%** aby odblokować certyfikat.",
          "requirements": {
            "questions": 10,
            "time": "2:30",
            "passing_score": "80%"
          },
          "note": "Test obejmuje wszystkie 5 etapów modelu OJT, fakty vs interpretacje, pytania coachingowe i plany wdrożeniowe",
          "estimated_seconds": 900,
          "xp_points": 50
        },
        {
          "id": 28,
          "type": "achievement",
          "badge": "🏆",
          "title": "Certyfikowany Trener OJT!",
          "description": "Gratulacje! Opanowałeś 5-etapowy model treningu On-the-Job. Teraz możesz skutecznie rozwijać kompetencje swojego zespołu bez odrywania się od codziennej pracy.",
          "skillsUnlocked": [
            "Prowadzenie kontraktu na wspólną pracę z psychologicznym bezpieczeństwem",
            "Zbieranie faktów podczas obserwacji (bez interpretacji i osądów)",
            "Prowadzenie 5-etapowej analizy feedbackowej (Odczucia-Cele-Przebieg-Alternatywy-Wnioski)",
            "Zadawanie pytań coachingowych zamiast dawania gotowych rad",
            "Tworzenie konkretnych planów wdrożeniowych (SMART)",
            "Systematyczne rozwijanie zespołu przez cykl powtarzalnych sesji OJT"
          ],
          "xp": 300,
          "badge_name": "OJT Master",
          "estimated_seconds": 60,
          "xp_points": 300
        },
        {
          "id": 29,
          "type": "ending",
          "title": "Twoje Następne Kroki",
          "introduction": "Ukończyłeś lekcję, ale to dopiero początek! Wiedza teoretyczna nic nie da bez wdrożenia. Oto Twój plan na najbliższe 30 dni:",
          "implementationPlan": {
            "title": "📋 Checklist 30 dni wdrożenia:",
            "steps": [
              {"day": "1-3", "task": "Wybierz 1-2 pracowników do pierwszej sesji OJT"},
              {"day": "4-7", "task": "Zaplanuj pierwszą sesję OJT (data, cele rozwojowe, lista klientów/zadań)"},
              {"day": "8", "task": "Przeprowadź pierwszą sesję OJT stosując wszystkie 5 etapów"},
              {"day": "9", "task": "Oceń co poszło dobrze, co trudne - zapisz wnioski"},
              {"day": "15", "task": "Druga sesja OJT (zastosuj wnioski z pierwszej)"},
              {"day": "22", "task": "Trzecia sesja OJT (budowanie rutyny)"},
              {"day": "30", "task": "Ocena postępu - czy widzisz rozwój pracownika? Dostosuj harmonogram"}
            ]
          },
          "resources": [
            {
              "icon": "📄",
              "title": "Szablon kontraktu OJT",
              "description": "Gotowy formularz do uzgodnienia zasad współpracy z pracownikiem"
            },
            {
              "icon": "📝",
              "title": "Karta obserwacji OJT",
              "description": "Szablon do notowania faktów podczas obserwacji rozmów"
            },
            {
              "icon": "✅",
              "title": "Checklist analizy (5 kroków)",
              "description": "Struktura rozmowy feedbackowej do wydruku"
            },
            {
              "icon": "📊",
              "title": "Tracker postępów OJT",
              "description": "Excel do śledzenia rozwoju pracowników (cele → sesje → wnioski)"
            }
          ],
          "finalQuote": {
            "text": "\\"Najlepsi liderzy nie rozwijają ludzi zamiast osiągać cele. Oni osiągają cele poprzez rozwijanie ludzi.\\"",
            "author": "Simon Sinek"
          },
          "closing": "Powodzenia w rozwijaniu Twojego zespołu! 🚀",
          "community": "Masz pytania? Dołącz do społeczności trenerów OJT w zakładce Forum",
          "estimated_seconds": 180,
          "xp_points": 20
        }
      ]
    }'::jsonb
);
