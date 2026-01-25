-- SQL script to insert "Lesson 2: Model Treningu On-the-Job" into Supabase
-- Run this in Supabase SQL Editor

-- 1. First, cleanup any existing version of this lesson to avoid duplicates
DELETE FROM lessons WHERE lesson_id = 'ojt_lesson_2_model';

-- 2. Insert the new lesson with rich interactive content
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
    'ojt_lesson_2_model',
    'Model Treningu On-the-Job (5 Kroków)',
    'Poznaj 5-etapowy cykl skutecznego treningu w terenie. Od kontraktowania, przez obserwację, aż po feedback zmieniający zachowania.',
    'intermediate',
    25,
    300,
    '{
      "cards": [
        {
          "id": 1,
          "type": "hero",
          "title": "Model Treningu OJT",
          "subtitle": "5 Kroków do Skutecznego Rozwoju",
          "content": "Dla menedżerów, którzy chcą rozwijać zespół bez odrywania się od pracy.",
          "icon": "rocket",
          "sections": [
            { "title": "Dla kogo", "content": "Liderzy zespołów sprzedażowych i obsługi" },
            { "title": "Cel", "content": "Opanować cykl: Odprawa -> Obserwacja -> Analiza" }
          ],
          "metadata": {
            "duration": "25 minut",
            "cards": "22 karty",
            "topic": "Metodyka OJT",
            "reward": "300 XP"
          }
        },
        {
          "id": 2,
          "type": "data",
          "title": "Dlaczego OJT działa?",
          "subtitle": "Liczby nie kłamią",
          "content": "Większość szkoleń to strata czasu, bo wiedza nie jest przenoszona do praktyki.",
          "stats": [
            { "value": "70%", "label": "Wiedzy pochodzi z praktyki (Model 70-20-10)" },
            { "value": "4x", "label": "Szybszy rozwój kompetencji" },
            { "value": "85%", "label": "Retencja wiedzy (vs 10% przy wykładzie)" }
          ],
          "callout": {
            "type": "info",
            "text": "Uczysz się pracując, nie przerywasz pracy by się uczyć."
          }
        },
        {
          "id": 3,
          "type": "timeline",
          "title": "Twój Dzień OJT",
          "data": {
            "items": [
              { "year": "8:00", "title": "Rozmowa Startowa", "description": "Kontrakt i ustalenie zasad współpracy na dziś.", "icon": "handshake" },
              { "year": "Cykl", "title": "Odprawa (Przed)", "description": "3-5 min przed wizytą. Ustalenie JEDNEGO celu.", "icon": "target" },
              { "year": "Cykl", "title": "Obserwacja", "description": "Wizyta u klienta. Jesteś cieniem. Notujesz fakty.", "icon": "eye" },
              { "year": "Cykl", "title": "Analiza (Po)", "description": "Feedback na gorąco. Pracownik mówi pierwszy.", "icon": "message-circle" },
              { "year": "16:00", "title": "Podsumowanie", "description": "Wnioski z całego dnia i plan wdrożeniowy.", "icon": "flag" }
            ]
          }
        },
        {
          "id": 4,
          "type": "content",
          "title": "Krok 1: Kontrakt (Fundament)",
          "content": "Zanim wsiądziesz do samochodu, musisz ustalić zasady gry. Bez tego pracownik będzie czuł lęk przed oceną.\\n\\n**4 Elementy Kontraktu:**\\n1. **Cel:** ''Dziś pracujemy nad zamykaniem sprzedaży''\\n2. **Rola:** ''Jestem cieniem, nie szefem''\\n3. **Zasady:** ''Nie wtrącam się, chyba że mnie poprosisz''\\n4. **Korzyść:** ''Chcę, żebyś zarabiał więcej''"
        },
        {
          "id": 5,
          "type": "story",
          "title": "Dobry vs Zły Kontrakt",
          "icon": "users",
          "scenario": {
            "heading": "Sytuacja",
            "text": "Dwaj menedżerowie zabierają handlowców w teren."
          },
          "consequences": [
            { "heading": "❌ Tomasz (Zły)", "text": "''Jadę z Tobą posłuchać jak Ci idzie.'' -> Pracownik spięty, boi się oceny, ukrywa błędy." },
            { "heading": "✅ Michał (Dobry)", "text": "''Jadę Ci pomóc w zamykaniu. Wejdę tylko na Twój znak. Resztę czasu milczę.'' -> Pracownik czuje wsparcie, eksperymentuje." }
          ],
          "lesson": {
            "heading": "Wniosek",
            "text": "Dobry kontrakt buduje psychologiczne bezpieczeństwo. Pracownik musi wiedzieć: Pracujemy NAD tobą, nie PRZECIWKO tobie."
          }
        },
        {
          "id": 6,
          "type": "quiz",
          "title": "Sprawdź Instynkt",
          "questions": [
            {
              "question": "Pracownik pyta: ''Czy będziesz mnie oceniał?'' Co odpowiadasz?",
              "options": [
                "Tak, to część mojej pracy, muszę wypełnić arkusz oceny.",
                "Nie, jestem tu żeby Ci pomóc zarabiać więcej. Nie oceniam Ciebie, tylko szukamy sposobów na lepsze wyniki.",
                "Zależy jak Ci pójdzie.",
                "Nie martw się tym teraz."
              ],
              "correct": 1,
              "explanation": "Zdejmij presję oceny. Skup się na rozwoju i korzyściach dla pracownika (więcej zarobi, szybciej awansuje)."
            }
          ]
        },
        {
          "id": 7,
          "type": "content",
          "title": "Krok 2: Odprawa (Briefing)",
          "content": "To ''strojenie instrumentu'' przed występem. Robisz to w samochodzie lub przed drzwiami klienta. Trwa 3 minuty.\\n\\n**Pytania do zadania:**\\n• ''Jaki jest Twój cel na tę wizytę?''\\n• ''Jaką jedną rzecz chcesz przećwiczyć?''\\n• ''Jak zaczniesz rozmowę?''"
        },
        {
          "id": 8,
          "type": "flashcards",
          "title": "Ćwiczenie: Pytania na Odprawę",
          "cards": [
            {
              "front": "Sytuacja: Idziecie do trudnego klienta, który ostatnio zrezygnował.\\nTwój cel: Odzyskać go.\\n\\nDobre pytanie na odprawę?",
              "back": "''Jaki masz plan na pierwsze 30 sekund, żeby przełamać lody i nie wyrzucił nas za drzwi?''"
            },
            {
              "front": "Sytuacja: Pracujesz z handlowcem nad badaniem potrzeb.\\n\\nDobre pytanie na odprawę?",
              "back": "''Jakie 2 pytania otwarte zadasz na pewno w tej rozmowie?''"
            }
          ]
        },
        {
          "id": 9,
          "type": "lightbulb",
          "title": "Zasada Jednego Celu",
          "insight": "Mniej znaczy więcej. Trenuj 1 rzecz naraz.",
          "content": "Jeśli powiesz pracownikowi: ''Popraw uśmiech, zadawaj pytania i szybciej zamykaj'' - nie zrobi niczego dobrze.\\n\\nWybierz **JEDEN** priorytet na jedną wizytę.",
          "accent_color": "#ffcc00"
        },
        {
          "id": 10,
          "type": "content",
          "title": "Krok 3: Obserwacja",
          "content": "Wchodzisz do klienta. Jesteś duchem. Nie istniejesz.\\n\\n**Twoje zadania:**\\n1. **Milcz.** (Chyba że ustaliliście inaczej)\\n2. **Notuj.** (Ale co notować?)\\n3. **Nie ratuj.** (Pozwól mu popełnić błąd, jeśli nie zabije relacji)"
        },
        {
          "id": 11,
          "type": "flashcards",
          "title": "Trening: Fakt czy Opinia?",
          "cards": [
            {
              "front": "Notatka: ''Klient był znudzony''\\nFakt czy Opinia?",
              "back": "❌ OPINIA (To Twoja interpretacja). Fakt: ''Klient patrzył w telefon i ziewał''."
            },
            {
              "front": "Notatka: ''Zadałeś 3 pytania zamknięte pod rząd''\\nFakt czy Opinia?",
              "back": "✅ FAKT (To się wydarzyło, nie da się zaprzeczyć)."
            },
            {
              "front": "Notatka: ''Byłeś niepewny siebie''\\nFakt czy Opinia?",
              "back": "❌ OPINIA. Fakt: ''Mówiłeś cicho i unikałeś kontaktu wzrokowego''."
            }
          ]
        },
        {
          "id": 12,
          "type": "lightbulb",
          "title": "Siła Faktów",
          "insight": "Fakty budują świadomość. Opinie budują opór.",
          "content": "Gdy mówisz: ''Byłeś niepewny'', pracownik myśli: ''Wcale nie!''.\\nGdy mówisz: ''Mówiłeś cicho'', pracownik myśli: ''Faktycznie, muszę mówić głośniej''.",
          "accent_color": "#00ff88"
        },
        {
          "id": 13,
          "type": "content",
          "title": "Krok 4: Analiza (Feedback)",
          "content": "Najważniejszy moment. Dzieje się od razu po wyjściu. Nie w biurze, nie jutro - TERAZ.\\n\\n**Sekwencja 5 Kroków:**\\n1. **Odczucia** (''Jak Ci się poszło?'')\\n2. **Cele** (''Jaki był nasz cel?'')\\n3. **Przebieg** (''Co poszło dobrze, a co źle?'')\\n4. **Alternatywy** (''Co mogłeś zrobić inaczej?'')\\n5. **Wnioski** (''Co bierzesz na przyszłość?'')"
        },
        {
          "id": 14,
          "type": "story",
          "title": "Karol i ''Pomyślimy''",
          "icon": "trending-up",
          "scenario": {
            "heading": "Porażka",
            "text": "Karol wychodzi od klienta z niczym (''Pomyślimy''). Jest zły. Menedżer Michał mógłby go skrytykować, ale stosuje model 5 kroków."
          },
          "consequences": [
            { "heading": "Rozmowa (Skrót)", "text": "Michał: ''Co mogłeś zrobić inaczej?''\\nKarol: ''Mogłem zapytać o budżet wcześniej...''\\nMichał: ''Dokładnie. Jak zapytasz następnym razem?''" },
            { "heading": "Efekt", "text": "Karol SAM doszedł do wniosku. Wziął odpowiedzialność za zmianę." }
          ],
          "lesson": {
            "heading": "Złota Zasada",
            "text": "Mów 20% czasu, słuchaj 80%. Niech pracownik sam oceni swoją pracę."
          }
        },
        {
          "id": 15,
          "type": "content",
          "title": "Coaching: Zamień Krytykę w Pytanie",
          "content": "Twoim odruchem jest powiedzenie: ''Źle to zrobiłeś''. Powstrzymaj się. Zamień to na pytanie."
        },
        {
          "id": 16,
          "type": "flashcards",
          "title": "Ćwiczenie: Transformacja Feedbacku",
          "cards": [
            {
              "front": "Chcesz powiedzieć: ''Nie słuchałeś klienta!''\\n\\nJak zapytać?",
              "back": "''Co powiedział klient o swoim budżecie? Jak się do tego odniosłeś?''"
            },
            {
              "front": "Chcesz powiedzieć: ''Za szybko przeszedłeś do ceny!''\\n\\nJak zapytać?",
              "back": "''W którym momencie klient był gotowy na ofertę? Co by się stało, gdybyś poczekał chwilę dłużej?''"
            },
            {
              "front": "Chcesz powiedzieć: ''To była katastrofa.''\\n\\nJak zapytać?",
              "back": "''Jak oceniasz tę rozmowę w skali 1-10? Co zabrakło do 10?''"
            }
          ]
        },
        {
          "id": 17,
          "type": "content",
          "title": "Krok 5: Podsumowanie Dnia",
          "content": "Koniec dnia w terenie. Niech to nie będzie ''Dzięki, cześć''.\\n\\n**Co zrobić:**\\n1. Przejrzyjcie notatki z całego dnia.\\n2. Znajdźcie WZORCE (powtarzające się błędy lub sukcesy).\\n3. Ustalcie PLAN WDROŻENIOWY na jutro."
        },
        {
          "id": 18,
          "type": "habit",
          "title": "Plan Wdrożeniowy",
          "description": "Zaznacz nawyki, które wdrożysz od jutra.",
          "habits": [
            { "id": "h1", "text": "W każdej OJT ustalam kontrakt przed startem" },
            { "id": "h2", "text": "Notuję tylko fakty, nie opinie" },
            { "id": "h3", "text": "Zadaję 5 pytań zanim dam własną radę" }
          ]
        },
        {
          "id": 19,
          "type": "data",
          "title": "Częstotliwość OJT",
          "content": "Jak często to robić, żeby działało?",
          "stats": [
            { "value": "2-3x", "label": "w tyg. dla Nowego Pracownika (Onboarding)" },
            { "value": "1x", "label": "w tyg. dla Rozwijającego się (Junior/Mid)" },
            { "value": "2x", "label": "w miesiącu dla Seniora (Mastery)" }
          ],
          "callout": {
            "type": "warning",
            "text": "Regularność > Długość. Lepiej 1h co tydzień niż cały dzień raz na kwartał."
          }
        },
        {
          "id": 20,
          "type": "quiz",
          "title": "Test Końcowy",
          "questions": [
            {
              "question": "Jaka jest najważniejsza zasada podczas Obserwacji (Krok 3)?",
              "options": [
                "Notować każdą myśl",
                "Ingerować, gdy pracownik robi błąd",
                "Być cieniem i notować tylko fakty",
                "Przejąć rozmowę gdy idzie źle"
              ],
              "correct": 2,
              "explanation": "Twoim celem jest zobaczenie prawdziwych zachowań pracownika. Jeśli ingerujesz, zmieniasz wynik eksperymentu."
            },
            {
              "question": "Kto powinien mówić pierwszy podczas Analizy po rozmowie?",
              "options": [
                "Ty (Trener) - żeby ustawić ramy",
                "Pracownik - żeby dokonał samooceny",
                "Klient - jeśli jest obecny",
                "Najpierw cisza"
              ],
              "correct": 1,
              "explanation": "Zawsze najpierw pracownik. Jeśli Ty powiesz pierwszy co myślisz, on dostosuje swoje zdanie do Twojego."
            },
            {
              "question": "Dlaczego notujemy fakty (''patrzył w telefon''), a nie opinie (''nudził się'')?",
              "options": [
                "Bo fakty są krótsze",
                "Bo opinie rodzą opór i obronę, a fakty skłaniają do refleksji",
                "Bo tak mówi HR",
                "Nie ma różnicy"
              ],
              "correct": 1,
              "explanation": "Fakty są niepodważalne. Z opinią można dyskutować. Fakt otwiera dyskusję o przyczynach."
            }
          ]
        },
        {
          "id": 21,
          "type": "achievement",
          "title": "Certyfikowany Trener OJT",
          "description": "Opanowałeś 5-stopniowy model skutecznego rozwoju w terenie!",
          "xp": 300,
          "level": "Master",
          "icon": "trophy",
          "stats": [
             { "value": "5/5", "label": "Kroków Modelu" },
             { "value": "100%", "label": "Gotowości" }
          ]
        },
        {
          "id": 22,
          "type": "ending",
          "title": "Misja Ukończona!",
          "checklist": [
            { "icon": "✅", "text": "Znasz 5 kroków OJT" },
            { "icon": "✅", "text": "Rozróżniasz fakty od opinii" },
            { "icon": "✅", "text": "Umiesz zamieniać krytykę w pytania" }
          ],
          "next_steps": {
            "text": "Zaplanuj swoją pierwszą sesję OJT na ten tydzień! Wybierz pracownika i JEDEN cel.",
            "available": true
          }
        }
      ]
    }'::jsonb
);
