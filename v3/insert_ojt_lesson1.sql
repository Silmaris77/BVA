-- SQL script to insert "Wprowadzenie do On-the-Job Training" lesson into Supabase
-- Run this in Supabase SQL Editor

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
    'ojt_lesson_1_wprowadzenie',
    'Wprowadzenie do On-the-Job Training',
    'Odkryj najskuteczniejszą metodę rozwoju pracowników i zbuduj kulturę ciągłego uczenia się. Model 70-20-10, praktyczne narzędzia i mindset trenera.',
    'beginner',
    18,
    200,
    '{
      "cards": [
        {
          "id": 1,
          "type": "hero",
          "title": "Wprowadzenie do On-the-Job Training",
          "content": "Odkryj najskuteczniejszą metodę rozwoju pracowników i zbuduj kulturę ciągłego uczenia się",
          "metadata": {
            "duration": "18 minut",
            "cards": "20 kart",
            "topic": "Fundament OJT",
            "reward": "200 XP"
          },
          "estimated_seconds": 60
        },
        {
          "id": 2,
          "type": "data",
          "title": "70% wiedzy z praktyki",
          "content": "Model 70-20-10: 70% wiedzy z praktyki, 20% od innych ludzi, 10% z formalnych szkoleń. On-the-Job Training to wykorzystanie tych 70% dla celowego rozwoju kompetencji.",
          "stats": [
            {
              "value": "70%",
              "label": "wiedzy zawodowej zdobywamy przez praktykę w miejscu pracy"
            }
          ],
          "callout": {
            "type": "info",
            "text": "Źródło: Model 70-20-10, Deloitte 2024"
          },
          "estimated_seconds": 90,
          "xp_points": 5
        },
        {
          "id": 3,
          "type": "story",
          "title": "Szkolenie które nic nie zmieniło",
          "content": "**Marcin**, dyrektor sprzedaży w firmie tech, wysłał 12 handlowców na 2-dniowe szkolenie z technik sprzedaży (koszt: 18 000 PLN).\\n\\n**❌ Co się stało 2 tygodnie później:**\\n\\n• Tylko 3 osoby stosują nowe techniki\\n• Reszta wróciła do starych nawyków\\n• Wyniki sprzedaży bez zmian\\n• ROI szkolenia ≈ 0%\\n\\n**Co Marcin zrobił inaczej 3 miesiące później:** Zamiast szkolenia wprowadził program OJT - 2 godziny tygodniowo z każdym handlowcem.\\n\\n**✅ Rezultat po 6 tygodniach:**\\n\\n• 11/12 osób stosuje nowe techniki konsekwentnie\\n• Conversion rate +23%\\n• Wartość średniej transakcji +18%\\n• ROI: 340% (mierzalny wzrost sprzedaży)\\n\\n💡 **Kluczowa różnica:** Nauka w kontekście + natychmiastowy feedback + praktyka w rzeczywistych sytuacjach = trwała zmiana zachowań",
          "estimated_seconds": 180,
          "xp_points": 10
        },
        {
          "id": 4,
          "type": "content",
          "title": "5 Powodów Dlaczego OJT Działa",
          "content": "Dlaczego to najskuteczniejsza metoda rozwoju pracowników?\\n\\n**1️⃣ Nauka w kontekście**\\nPracownik uczy się w RZECZYWISTYCH sytuacjach, nie symulacjach. Przeniesienie wiedzy do praktyki = 0 wysiłku.\\n\\n**2️⃣ Natychmiastowy feedback**\\nBłędy korygowane od razu, sukcesy wzmacniane na gorąco. Nie czekasz 2 tygodnie na ''debrief''.\\n\\n**3️⃣ Spersonalizowane tempo**\\nDostosowane do poziomu pracownika. Nie za wolno (nuda), nie za szybko (frustracja).\\n\\n**4️⃣ Budowanie relacji**\\nTrening 1-na-1 lub w małych grupach buduje zaufanie, które przekłada się na otwartość na rozwój.\\n\\n**5️⃣ ROI mierzalny w tygodniach**\\nWyniki widoczne szybko: lepsze metody pracy → lepsze rezultaty biznesowe. Nie czekasz 6 miesięcy.",
          "estimated_seconds": 150,
          "xp_points": 10
        },
        {
          "id": 5,
          "type": "flashcard",
          "title": "5 Mitów o On-the-Job Training",
          "content": "Kliknij kartę aby odkryć prawdę",
          "front": "Jakie są najpopularniejsze MITY o OJT?\\n\\n(i dlaczego są fałszywe)",
          "back": "**❌ Mit 1:** ''To tylko pokazywanie jak się robi''\\n✅ Prawda: OJT = obserwacja + demo + praktyka + feedback + analiza\\n\\n**❌ Mit 2:** ''Nie mam czasu na OJT''\\n✅ Prawda: 2h OJT = 20h oszczędności w przyszłości (mniej błędów)\\n\\n**❌ Mit 3:** ''Tylko dla juniorów''\\n✅ Prawda: Seniorzy rozwijają się najszybciej przez OJT (feedback w kontekście)\\n\\n**❌ Mit 4:** ''Potrzebuję certyfikatu trenera''\\n✅ Prawda: Potrzebujesz struktury i umiejętności feedbacku (nauczysz się tutaj)\\n\\n**❌ Mit 5:** ''To strata czasu - mogą się nauczyć sami''\\n✅ Prawda: Samodzielna nauka = 3x dłużej + nawyki błędne utrwalają się",
          "estimated_seconds": 120,
          "xp_points": 10
        },
        {
          "id": 6,
          "type": "comparison",
          "title": "Słabe OJT vs Silne OJT",
          "content": "Jaka jest różnica między ''pokazywaniem'' a prawdziwym treningiem?",
          "left": {
            "title": "❌ Słabe OJT (nieskuteczne)",
            "items": [
              "**Brak struktury** - ''Zobacz jak ja to robię''",
              "**Monolog trenera** - Zero pytań do pracownika",
              "**Brak feedbacku** - Lub feedback ogólnikowy",
              "**Brak planu** - Randomowe sesje bez ciągłości",
              "**Brak pomiaru** - Nie wiesz czy zadziałało"
            ]
          },
          "right": {
            "title": "✅ Silne OJT (skuteczne)",
            "items": [
              "**5-stopniowy model** - Odczucia → Cele → Przebieg → Alternatywy → Wnioski",
              "**Pytania coachingowe** - Pracownik SAM dochodzi do wniosków",
              "**Konkretny feedback** - Opisujesz zachowania, nie oceniasz osoby",
              "**Plan rozwoju** - 1-3 cele na każdą sesję",
              "**Mierzalne efekty** - Wiesz co się zmieniło"
            ]
          },
          "estimated_seconds": 120,
          "xp_points": 10
        },
        {
          "id": 7,
          "type": "content",
          "title": "3 Filary Skutecznego OJT",
          "content": "**📋 STRUKTURA**\\nModel 5 kroków, jasny plan sesji\\n\\n**🛠️ NARZĘDZIA**\\nKontraktowanie, słuchanie, pytania, feedback\\n\\n**🧠 MINDSET**\\nTrener = Coach, nie wykładowca\\n\\n---\\n\\n**📚 W tym kursie nauczysz się:**\\n\\n• Lekcja 1: Fundamenty OJT (tutaj jesteś)\\n• Lekcja 2: Model 5 Kroków (struktura sesji)\\n• Lekcja 3: 4 Narzędzia Trenera (kontraktowanie, słuchanie, pytania, feedback)",
          "estimated_seconds": 100,
          "xp_points": 5
        },
        {
          "id": 8,
          "type": "practice",
          "title": "Zdiagnozuj swój styl trenera",
          "content": "Przypomnij sobie ostatnią sytuację, gdy uczyłeś kogoś nowej umiejętności. Odpowiedz szczerze:",
          "questions": [
            {
              "id": "q1",
              "label": "1. Czy ustaliłeś cel sesji PRZED rozpoczęciem?",
              "placeholder": "Np. ''Nie, po prostu pokazałem jak robię'' lub ''Tak, ustaliliśmy że pracujemy nad...''"
            },
            {
              "id": "q2",
              "label": "2. Czy zadawałeś pytania czy głównie tłumaczyłeś?",
              "placeholder": "Np. ''Głównie mówiłem co i jak'' lub ''Pytałem co sądzi, co by zmienił...''"
            },
            {
              "id": "q3",
              "label": "3. Czy dałeś konkretny feedback czy ogólną opinię?",
              "placeholder": "Np. ''Powiedziałem że było OK'' lub ''Wskazałem 3 konkretne zachowania...''"
            }
          ],
          "interpretation": "**0-1 TAK:** Styl ''pokazywania'' - działa na krótką metę, ale brak struktury. Po tym kursie będziesz trenować systematycznie.\\n\\n**2 TAK:** Styl ''częściowo coachingowy'' - masz intuicję, brakuje Ci narzędzi. Kurs da Ci konkretne techniki.\\n\\n**3 TAK:** Styl ''coachingowy'' - robisz to dobrze! Kurs uporządkuje wiedzę i doda zaawansowane techniki.",
          "estimated_seconds": 180,
          "xp_points": 15
        },
        {
          "id": 9,
          "type": "quiz",
          "title": "✅ Checkpoint 1: Fundamenty OJT",
          "questions": [
            {
              "question": "Model 70-20-10 mówi, że 70% wiedzy zdobywamy przez:",
              "options": [
                "Szkolenia formalne",
                "Praktykę w miejscu pracy",
                "Czytanie książek",
                "Obserwację innych"
              ],
              "correctAnswer": 1,
              "explanation": "Model 70-20-10 zakłada, że 70% wiedzy zawodowej pochodzi z praktyki w miejscu pracy, 20% od innych ludzi (mentorzy, współpracownicy), a tylko 10% z formalnych szkoleń."
            },
            {
              "question": "Główna przewaga OJT nad klasycznym szkoleniem to:",
              "options": [
                "Niższy koszt",
                "Nauka w rzeczywistym kontekście + natychmiastowy feedback",
                "Certyfikat ukończenia",
                "Krótszy czas trwania"
              ],
              "correctAnswer": 1,
              "explanation": "Największa siła OJT to nauka w RZECZYWISTYCH sytuacjach + feedback na gorąco, co eliminuje problem transferu wiedzy z sali szkoleniowej do pracy."
            },
            {
              "question": "Który element NIE należy do silnego OJT?",
              "options": [
                "5-stopniowy model",
                "Pytania coachingowe",
                "Monolog trenera bez interakcji",
                "Konkretny feedback"
              ],
              "correctAnswer": 2,
              "explanation": "Monolog trenera bez interakcji to cecha słabego OJT. Silne OJT opiera się na pytaniach, dialogu i zaangażowaniu pracownika."
            }
          ],
          "estimated_seconds": 120,
          "xp_points": 15
        },
        {
          "id": 10,
          "type": "content",
          "title": "Kiedy Stosować OJT?",
          "content": "**✅ OJT IDEALNE dla:**\\n\\n• Onboarding nowych pracowników\\n• Rozwój umiejętności ''miękkich'' (sprzedaż, negocjacje, prezentacje)\\n• Zmiana nawyków (np. nowa metodologia pracy)\\n• Korekta błędów w czasie rzeczywistym\\n• Przygotowanie do awansu\\n• Przekazanie wiedzy eksperckiej (shadowing)\\n\\n**❌ OJT NIE dla:**\\n\\n• Wiedza teoretyczna (lepiej: e-learning, książki)\\n• Certyfikacje formalne (wymagana sala egzaminacyjna)\\n• Szkolenia BHP (regulacje prawne)\\n• Duże grupy 20+ osób (za mało czasu na każdego)\\n• Wiedza ogólna ''nice to have'' (ROI zbyt niskie)\\n\\n---\\n\\n💡 **Zasada:** OJT = umiejętności praktyczne w kontekście. Teoria + masa = inne metody.",
          "estimated_seconds": 150,
          "xp_points": 10
        },
        {
          "id": 11,
          "type": "scenario",
          "title": "Scenariusz: Wybierz właściwą metodę",
          "content": "Masz 5 pracowników i różne potrzeby rozwojowe. Zdecyduj: OJT czy inna metoda?",
          "scenarios": [
            {
              "id": "A",
              "title": "Anna - Junior handlowiec, problem z zamykaniem transakcji",
              "description": "Potrzebuje: Obserwacja rozmów + feedback w czasie rzeczywistym",
              "correct": true
            },
            {
              "id": "B",
              "title": "Tomasz - Programista, chce nauczyć się nowego języka",
              "description": "Potrzebuje: Kurs online + dokumentacja + projekty własne",
              "correct": false
            },
            {
              "id": "C",
              "title": "Kasia - Manager, za dużo mówi, za mało słucha w 1-1",
              "description": "Potrzebuje: Shadowing podczas jej rozmów + coaching pytaniami",
              "correct": true
            },
            {
              "id": "D",
              "title": "Paweł - Cały zespół 15 osób, aktualizacja procedury ISO",
              "description": "Potrzebuje: Webinar grupowy + test wiedzy + materiały do pobrania",
              "correct": false
            },
            {
              "id": "E",
              "title": "Marcin - Senior, plateau kariery, chce zostać team leadem",
              "description": "Potrzebuje: OJT z obecnym liderem (shadowing + delegowanie zadań + feedback)",
              "correct": true
            }
          ],
          "answer_key": "A, C, E = OJT ✅ | B, D = inne metody ❌",
          "estimated_seconds": 150,
          "xp_points": 15
        },
        {
          "id": 12,
          "type": "story",
          "title": "Od ''problemu'' do gwiazdora w 8 tygodni",
          "content": "**Katarzyna**, manager zespołu customer success, miała problem z Michałem - doświadczonym CSM, który miał najgorsze wyniki zadowolenia klientów (CSAT 6.2/10).\\n\\n**🔍 Diagnoza (tydzień 1):**\\nKatarzyna obserwowała 3 rozmowy Michała. Odkryła: Michał doskonale zna produkt, ale NIE słucha klienta. Przerywa, narzuca rozwiązania, nie pyta o kontekst.\\n\\n**🎯 Plan OJT (8 tygodni, 1.5h/tydzień):**\\n\\n• **Tydzień 1-2:** Aktywne słuchanie (parafraza, odzwierciedlanie emocji)\\n• **Tydzień 3-4:** Pytania odkrywające (zamiast ''masz problem X'' → ''opowiedz mi o...'')\\n• **Tydzień 5-6:** Budowanie rozwiązań RAZEM z klientem\\n• **Tydzień 7-8:** Konsolidacja i samodzielność\\n\\n**✅ Rezultat po 8 tygodniach:**\\n\\n• CSAT wzrósł z 6.2 do 9.1/10\\n• Retention rate klientów Michała: +34%\\n• Michał otrzymał awans na Senior CSM\\n• Teraz SAM szkoli nowych CSM-ów!\\n\\n💡 **Kluczowy wniosek:** Michał nie był ''słabym pracownikiem''. Miał 1 konkretny gap (słuchanie), który OJT wyeliminowało w 8 tygodni.",
          "estimated_seconds": 180,
          "xp_points": 10
        },
        {
          "id": 13,
          "type": "content",
          "title": "3 Role w Procesie OJT",
          "content": "**👨‍🏫 TRENER (Ty)**\\nProwadzi sesję, zadaje pytania, daje feedback, monitoruje postęp\\n\\n*Twoje zadania:* Obserwacja → Demo → Wspieranie praktyki → Analiza → Plan wdrożenia\\n\\n---\\n\\n**🎯 PRACOWNIK (Trainee)**\\nUczy się, praktykuje, zadaje pytania, dostaje feedback\\n\\n*Jego zadania:* Próbowanie → Refleksja → Zadawanie pytań → Wdrażanie zmian\\n\\n---\\n\\n**🏢 ORGANIZACJA**\\nZapewnia czas, narzędzia, kulturę wspierającą rozwój\\n\\n*Odpowiedzialność:* Czas na OJT w kalendarzu + Uznanie dla trenerów + Pomiar efektów",
          "estimated_seconds": 120,
          "xp_points": 10
        },
        {
          "id": 14,
          "type": "comparison",
          "title": "Mentor vs Coach vs Trener OJT",
          "content": "Jaka jest różnica?",
          "columns": [
            {
              "icon": "🧙",
              "title": "MENTOR",
              "items": [
                "**Rola:** Doradca z doświadczeniem",
                "**Fokus:** Rozwój kariery długoterminowy",
                "**Metoda:** Dzielenie się historią, radami",
                "**Czas:** Miesięcy/lata"
              ]
            },
            {
              "icon": "🎓",
              "title": "COACH",
              "items": [
                "**Rola:** Facylitator rozwoju",
                "**Fokus:** Cel konkretny (1-3 obszary)",
                "**Metoda:** Pytania, nie odpowiedzi",
                "**Czas:** Tygodni/miesięcy"
              ]
            },
            {
              "icon": "👨‍🏫",
              "title": "TRENER OJT",
              "items": [
                "**Rola:** Nauczyciel + Coach",
                "**Fokus:** Umiejętności praktyczne",
                "**Metoda:** Demo + praktyka + feedback",
                "**Czas:** Dni/tygodni"
              ]
            }
          ],
          "callout": {
            "type": "info",
            "text": "💡 Trener OJT = Hybrid: Pokazujesz JAK (jak nauczyciel) + Pytasz DLACZEGO (jak coach) + Dzielisz się doświadczeniem (jak mentor)"
          },
          "estimated_seconds": 120,
          "xp_points": 10
        },
        {
          "id": 15,
          "type": "content",
          "title": "Mindset Trenera OJT",
          "content": "7 przekonań skutecznego trenera:\\n\\n**1. ''Moja rola to odkrywać, nie tłumaczyć''**\\nWięcej pytań niż odpowiedzi. Pracownik SAM dochodzi do wniosków.\\n\\n**2. ''Feedback to dar, nie ocena''**\\nOpisuję zachowania (fakty), nie oceniam osoby. ''Nie patrzyłeś w oczy'' ≠ ''Jesteś nieśmiały''.\\n\\n**3. ''Błędy to materiał do nauki''**\\nNie unikam błędów - analizuję je. ''Co mógłbyś zrobić inaczej?'' zamiast ''Źle to zrobiłeś''.\\n\\n**4. ''Tempo pracownika > mój harmonogram''**\\nDostosowuję tempo. Jeden potrzebuje 3 sesji, drugi 10. Obie sytuacje OK.\\n\\n**5. ''Mierzę rezultaty, nie czas''**\\nSukces = zmiana zachowań + lepsze wyniki. Nie: ''Przeszliśmy 20 slajdów''.\\n\\n**6. ''Trening to inwestycja, nie koszt''**\\n2h OJT teraz = 20h oszczędności w przyszłości + lepsze wyniki.\\n\\n**7. ''Każdy może się rozwinąć''**\\nNie ma ''beznadziejnych przypadków''. Są tylko niewłaściwe metody lub brak czasu.",
          "estimated_seconds": 180,
          "xp_points": 15
        },
        {
          "id": 16,
          "type": "poll",
          "title": "Co Cię najbardziej martwi w roli trenera?",
          "content": "Wybierz 1-2 obawy (anonimowe)",
          "options": [
            {
              "id": "time",
              "title": "⏰ ''Nie mam czasu na OJT''",
              "description": "Odpowiedź: Zacznij od 1h/tydzień. ROI widoczne po 2-3 tygodniach."
            },
            {
              "id": "cert",
              "title": "🎓 ''Nie mam certyfikatu/przeszkolenia''",
              "description": "Odpowiedź: Ten kurs + praktyka = wystarczy. Certyfikat nie gwarantuje umiejętności."
            },
            {
              "id": "feedback",
              "title": "😰 ''Boję się dawać krytyczny feedback''",
              "description": "Odpowiedź: Lekcja 3 nauczy Cię technik (AID, FISH, FUKO) - feedback bez konfliktów."
            },
            {
              "id": "knowledge",
              "title": "❓ ''Co jeśli nie znam odpowiedzi?''",
              "description": "Odpowiedź: Trener OJT zadaje pytania, nie musi znać wszystkich odpowiedzi. ''Nie wiem, sprawdźmy razem'' = OK."
            },
            {
              "id": "metrics",
              "title": "📊 ''Nie wiem jak mierzyć efekty''",
              "description": "Odpowiedź: Lekcja 2 (krok 5) + gotowe szablony do śledzenia postępów."
            },
            {
              "id": "resistance",
              "title": "🙅 ''Pracownik nie chce się uczyć''",
              "description": "Odpowiedź: Kontraktowanie (Lekcja 3) rozwiązuje opór. Pokazujesz WIIFM (What''s In It For Me)."
            }
          ],
          "estimated_seconds": 120,
          "xp_points": 5
        },
        {
          "id": 17,
          "type": "quiz",
          "title": "✅ Checkpoint 2: Role i Mindset",
          "questions": [
            {
              "question": "Główna różnica między trenerem OJT a coachem to:",
              "options": [
                "Trener ma certyfikat, coach nie",
                "Trener pokazuje JAK + pyta DLACZEGO, coach tylko pyta",
                "Coach pracuje tylko z managerami",
                "Trener pracuje grupowo, coach 1-na-1"
              ],
              "correctAnswer": 1,
              "explanation": "Trener OJT łączy elementy nauczyciela (pokazuje JAK zrobić) i coacha (pyta DLACZEGO, co pomaga pracownikowi zrozumieć kontekst)."
            },
            {
              "question": "Które przekonanie NIE należy do mindset trenera OJT?",
              "options": [
                "''Moja rola to odkrywać, nie tłumaczyć''",
                "''Błędy to materiał do nauki''",
                "''Muszę znać odpowiedzi na wszystkie pytania''",
                "''Każdy może się rozwinąć''"
              ],
              "correctAnswer": 2,
              "explanation": "Trener OJT NIE musi znać wszystkich odpowiedzi. Jego rola to facylitować proces uczenia się przez pytania, nie być wszystkowiedzącym ekspertem."
            },
            {
              "question": "OJT NIE nadaje się do:",
              "options": [
                "Onboardingu nowych pracowników",
                "Rozwoju umiejętności sprzedażowych",
                "Szkoleń BHP dla 50 osób jednocześnie",
                "Zmiany nawyków w pracy"
              ],
              "correctAnswer": 2,
              "explanation": "OJT wymaga indywidualnej uwagi i feedbacku, więc nie sprawdza się przy dużych grupach 20+ osób. BHP dla 50 osób lepiej zrealizować webinarem."
            }
          ],
          "estimated_seconds": 120,
          "xp_points": 15
        },
        {
          "id": 18,
          "type": "test",
          "title": "📝 Egzamin Końcowy",
          "content": "10 pytań | Min. 70% do zaliczenia",
          "passing_score": 70,
          "questions": [
            {
              "question": "Model 70-20-10 mówi, że ile % wiedzy zawodowej zdobywamy przez praktykę?",
              "options": ["20%", "50%", "70%", "90%"],
              "correctAnswer": 2,
              "explanation": "Model 70-20-10 zakłada 70% praktyka, 20% ludzie, 10% szkolenia formalne."
            },
            {
              "question": "Jaka jest główna przewaga OJT nad klasycznym szkoleniem?",
              "options": [
                "Niższy koszt",
                "Nauka w rzeczywistym kontekście + natychmiastowy feedback",
                "Certyfikat ukończenia",
                "Krótszy czas trwania"
              ],
              "correctAnswer": 1,
              "explanation": "OJT eliminuje problem transferu wiedzy - uczysz się tam, gdzie pracujesz."
            },
            {
              "question": "Które stwierdzenie to MIT o OJT?",
              "options": [
                "''OJT to tylko pokazywanie jak się robi''",
                "''OJT łączy obserwację, demo, praktykę i feedback''",
                "''OJT działa dla juniorów i seniorów''",
                "''OJT wymaga struktury i narzędzi''"
              ],
              "correctAnswer": 0,
              "explanation": "OJT to o wiele więcej niż ''pokazywanie'' - wymaga struktury 5 kroków + narzędzi coachingowych."
            },
            {
              "question": "Co charakteryzuje SILNE OJT (nie słabe)?",
              "options": [
                "Brak struktury - ''Zobacz jak ja to robię''",
                "Monolog trenera bez pytań",
                "5-stopniowy model + pytania coachingowe + konkretny feedback",
                "Randomowe sesje bez planu"
              ],
              "correctAnswer": 2,
              "explanation": "Silne OJT ma strukturę (5 kroków), narzędzia (pytania) i mindset (coach)."
            },
            {
              "question": "Które NIE należy do 3 filarów skutecznego OJT?",
              "options": [
                "Struktura (Model 5 kroków)",
                "Narzędzia (kontraktowanie, pytania, feedback)",
                "Mindset (trener = coach)",
                "Certyfikat trenera"
              ],
              "correctAnswer": 3,
              "explanation": "3 filary to: Struktura, Narzędzia, Mindset. Certyfikat nie jest wymagany."
            },
            {
              "question": "OJT IDEALNE dla:",
              "options": [
                "Wiedzy teoretycznej (lepiej e-learning)",
                "Onboardingu i rozwoju umiejętności miękkich",
                "Certyfikacji formalnych",
                "Szkoleń BHP dla dużych grup"
              ],
              "correctAnswer": 1,
              "explanation": "OJT świetnie sprawdza się przy umiejętnościach praktycznych i onboardingu."
            },
            {
              "question": "Zadanie TRENERA OJT to:",
              "options": [
                "Obserwacja → Demo → Praktyka → Analiza → Plan wdrożenia",
                "Tylko wykładanie teorii",
                "Zapewnienie czasu i narzędzi (to rola organizacji)",
                "Tylko obserwowanie bez ingerencji"
              ],
              "correctAnswer": 0,
              "explanation": "Trener przeprowadza pełny cykl: obserwacja, demonstracja, praktyka, analiza, wdrożenie."
            },
            {
              "question": "Trener OJT różni się od coacha tym, że:",
              "options": [
                "Pracuje tylko z juniorami",
                "Pokazuje JAK (demo) + pyta DLACZEGO (coaching)",
                "Nie zadaje pytań, tylko tłumaczy",
                "Pracuje tylko grupowo"
              ],
              "correctAnswer": 1,
              "explanation": "Trener OJT łączy demo (pokazuje JAK) z coachingiem (pyta DLACZEGO, odkrywa przez pytania)."
            },
            {
              "question": "Które przekonanie NALEŻY do mindset trenera OJT?",
              "options": [
                "''Muszę znać odpowiedzi na wszystkie pytania''",
                "''Błędy to materiał do nauki, nie porażka''",
                "''Trening to koszt, nie inwestycja''",
                "''Są pracownicy beznadziejni do rozwoju''"
              ],
              "correctAnswer": 1,
              "explanation": "Mindset trenera: błędy to źródło nauki, każdy może się rozwinąć."
            },
            {
              "question": "Feedback skuteczny to:",
              "options": [
                "''Jesteś nieśmiały'' (ocena osoby)",
                "''Nie patrzyłeś w oczy klienta'' (opis zachowania)",
                "''Brakuje Ci determinacji'' (interpretacja)",
                "''Ogólnie było OK'' (brak konkretów)"
              ],
              "correctAnswer": 1,
              "explanation": "Feedback oparty na faktach (zachowaniach) jest skuteczny. Unikamy oceniania osoby."
            }
          ],
          "estimated_seconds": 300,
          "xp_points": 30
        },
        {
          "id": 19,
          "type": "habit",
          "title": "🎯 Twój Plan na Najbliższe 7 Dni",
          "content": "Wybierz 1 działanie do wdrożenia:",
          "habits": [
            {
              "id": "observe",
              "title": "🔍 Zaobserwuj 1 pracownika w pracy",
              "description": "Obserwuj 30 min bez ingerencji. Notuj co działa, co można poprawić."
            },
            {
              "id": "feedback",
              "title": "💬 Daj 1 konkretny feedback",
              "description": "Opisz zachowanie (fakty), nie oceniaj osoby. ''Nie patrzyłeś w oczy'' zamiast ''Byłeś nieśmiały''."
            },
            {
              "id": "questions",
              "title": "❓ Zadaj 5 pytań zamiast 5 instrukcji",
              "description": "W następnej sytuacji ''szkoleniowej'' pytaj ''Co sądzisz?'' zamiast ''Zrób tak...''"
            },
            {
              "id": "schedule",
              "title": "📅 Zaplanuj 1. sesję OJT (1h)",
              "description": "Wybierz pracownika + umów sesję + przygotuj 1 cel do pracy"
            }
          ],
          "estimated_seconds": 120,
          "xp_points": 10
        },
        {
          "id": 20,
          "type": "ending",
          "title": "Fundamenty Opanowane!",
          "content": "Gratulacje! Znasz już podstawy On-the-Job Training",
          "checklist": [
            { "icon": "✅", "text": "Model 70-20-10 i dlaczego OJT działa" },
            { "icon": "✅", "text": "Różnica między słabym a silnym OJT" },
            { "icon": "✅", "text": "3 Filary skutecznego OJT (Struktura, Narzędzia, Mindset)" },
            { "icon": "✅", "text": "Kiedy stosować OJT (i kiedy nie)" },
            { "icon": "✅", "text": "Role w procesie + Mindset trenera" }
          ],
          "rewards": {
            "xp": 200,
            "badge": "OJT Starter",
            "unlocks": "Dostęp do Lekcji 2: Model 5 Kroków"
          },
          "next_steps": {
            "text": "• Wdróż 1 nawyk z Habit Builder w ciągu 7 dni\\n• Przejdź do Lekcji 2: Model Treningu On-the-Job (5 Kroków)\\n• LUB: Eksploruj narzędzia (Lekcja 3: Kontraktowanie, Słuchanie, Pytania, Feedback)",
            "available": true
          },
          "quote": {
            "text": "Najlepsi menedżerowie nie budują biznesu. Budują ludzi, a ludzie budują biznes.",
            "author": "Marcus Buckingham"
          },
          "estimated_seconds": 120
        }
      ]
    }'::jsonb
);
