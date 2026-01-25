-- COMPLETE OJT Lesson 2 - Converted 1:1 from lesson2_ojt_model.html mockup
-- All 29 cards - exact content match
DELETE FROM lessons WHERE lesson_id = 'ojt_lesson_2_model';

INSERT INTO lessons (
  lesson_id, 
  title, 
  description, 
  category, 
  difficulty, 
  duration_minutes, 
  xp_reward,
  content
)
VALUES (
  'ojt_lesson_2_model',
  'Model Treningu On-the-Job: 5 Kroków do Skutecznego Rozwoju',
  'Jak rozwijać pracowników bez odrywania ich od pracy? Poznaj 5-etapowy model On-the-Job Training, który w 3–4 miesiące zwiększa skuteczność zespołu o 20–50%.',
  'Praktyka: Sales Management',
  'intermediate',
  45,
  300,
  $${
    "cards": [
      {
        "id": 1,
        "type": "hero",
        "title": "Jak rozwijać pracowników bez odrywania ich od pracy?",
        "sections": [
          {
            "title": "👥 Dla kogo",
            "content": "Menedżerowie, którzy chcą przestać gasić pożary i zbudować zespół, który działa samodzielnie, bez ciągłego angażowania ich czasu."
          },
          {
            "title": "🎯 Cel",
            "content": "Poznać 5-etapowy model On-the-Job Training, który w 3–4 miesiące:\n\n- zwiększa skuteczność zespołu o 20–50%,\n- skraca czas rozwoju o połowę,\n- realnie uwalnia czas menedżera."
          },
          {
            "title": "💡 Dlaczego to działa",
            "content": "**70% kompetencji** powstaje w praktyce.\n\nOJT to nauka w realnym biznesie + natychmiastowy feedback — **4× szybszy rozwój** i trwała zmiana zachowań, nie teoria."
          }
        ],
        "estimated_seconds": 60,
        "xp_points": 0
      },
      {
        "id": 2,
        "type": "data",
        "title": "Dlaczego On-the-Job Training działa?",
        "stats": [
          {
            "value": "70%",
            "label": "Procent wiedzy zawodowej zdobywanej przez praktyczne doświadczenie",
            "trend": "up"
          },
          {
            "value": "4x",
            "label": "Szybciej rozwijają się pracownicy w treningu OJT vs tradycyjne szkolenia",
            "trend": "up"
          },
          {
            "value": "85%",
            "label": "Wskaźnik retencji wiedzy przy nauce przez działanie vs 20% przy wykładach",
            "trend": "up"
          }
        ],
        "callout": {
          "type": "info",
          "text": "**Kluczowy wniosek:** Najskuteczniejsze uczenie się odbywa się w kontekście rzeczywistych zadań, z natychmiastowym feedbackiem od doświadczonego mentora. To nie teoria z sali szkoleniowej, a praktyka w terenie."
        },
        "sources": ["Deloitte 70-20-10 Model", "Association for Talent Development (ATD) 2023", "Edgar Dale Learning Pyramid"],
        "estimated_seconds": 90,
        "xp_points": 10
      },
      {
        "id": 3,
        "type": "content",
        "title": "Czym jest Model Treningu On-the-Job?",
        "content": "Model OJT to **cykl powtarzających się działań**, który pozwala pracownikowi rozwinąć umiejętności przez:\n\n- **Praktyczne wykonywanie zadań** w rzeczywistym środowisku pracy\n- **Obserwację przez doświadczonego mentora/menedżera** podczas wykonywania zadań\n- **Konstruktywny feedback** oparty na faktach, nie opiniach\n- **Systematyczną analizę** i wyciąganie wniosków na przyszłość\n\n**Kluczowa różnica vs tradycyjne szkolenia:** uczysz SIĘ pracując, nie przerywasz pracy, by się uczyć",
        "remember": {
          "title": "Pamiętaj:",
          "items": [
            "Trening OJT ≠ \"rzucenie na głęboką wodę\"",
            "To systematyczny proces, nie przypadkowa obserwacja",
            "Wymaga przygotowania i struktury od menedżera"
          ]
        },
        "estimated_seconds": 120,
        "xp_points": 15
      },
      {
        "id": 4,
        "type": "timeline",
        "title": "5 Etapów Cyklu Treningu OJT",
        "data": {
          "items": [
            {
              "year": "START",
              "title": "1️⃣ ROZMOWA NA POCZĄTKU DNIA",
              "description": "**⏱️ 10-15 minut**\n\nKontrakt na wspólną pracę, ustalenie celów rozwojowych i planu dnia",
              "icon": "🤝"
            },
            {
              "year": "ETAP 2",
              "title": "2️⃣ ODPRAWA PRZED ROZMOWĄ",
              "description": "**⏱️ 5-10 minut**\n\nPrzypomnienie celów, analiza sytuacji, plan działania, demonstracja\n\n🔄 **CYKL POWTARZALNY** (dla każdej rozmowy/zadania - 3-5 razy dziennie)",
              "icon": "📋"
            },
            {
              "year": "ETAP 3",
              "title": "3️⃣ OBSERWACJA ROZMOWY",
              "description": "**⏱️ 30-60 minut**\n\nZbieranie faktów, notowanie zachowań pracownika i reakcji klienta",
              "icon": "👀"
            },
            {
              "year": "ETAP 4",
              "title": "4️⃣ ANALIZA PO ROZMOWIE",
              "description": "**⏱️ 10-15 minut**\n\nFeedback, rozliczenie celów, wyciągnięcie wniosków, plan poprawy\n\n↻ **Powrót do etapu 2** dla kolejnej rozmowy/zadania",
              "icon": "💬"
            },
            {
              "year": "KONIEC",
              "title": "5️⃣ PODSUMOWANIE DNIA",
              "description": "**⏱️ 15-20 minut**\n\nRozliczenie celów dnia, wnioski, plan działań wdrożeniowych",
              "icon": "🏁"
            }
          ]
        },
        "estimated_seconds": 180,
        "xp_points": 20
      },
      {
        "id": 5,
        "type": "content",
        "title": "Etap 1: Rozmowa na początku dnia",
        "content": "**Czas:** 10-15 minut na początku wspólnego dnia\n**Cel:** Stworzyć fundament współpracy i uzgodnić zasady gry\n\n### 4 kluczowe elementy:\n\n**1. Sprzedanie idei treningu**\nDlaczego warto wspólnie pracować? Jaki jest cel tej sesji?\n\n**2. Kontrakt na wspólną pracę**\nJak będziemy pracować? (role, zasady komunikacji, co robisz gdy potrzebuję pomocy)\n\n**3. Ustalenie celów rozwojowych**\nNad czym będziemy pracować? (1-2 konkretne umiejętności)\n\n**4. Plan dnia**\nCo konkretnie zrobimy? (lista klientów/zadań, harmonogram)",
        "callout": {
          "type": "warning",
          "text": "⚠️ **Częsty błąd:** Pomijanie kontraktowania i wskakiwanie od razu w obserwację. Bez wyraźnej zgody pracownika i wspólnych celów, trening zamienia się w stresującą kontrolę!"
        },
        "remember": {
          "title": "Pamiętaj:",
          "items": [
            "Cele rozwojowe powinny być powiązane z celami biznesowymi (np. \"poprawić zamykanie sprzedaży\" → zwiększenie konwersji)"
          ]
        },
        "estimated_seconds": 150,
        "xp_points": 15
      },
      {
        "id": 6,
        "type": "story",
        "title": "Przykład: Dobry vs Zły Kontrakt",
        "scenarios": [
          {
            "type": "bad",
            "title": "❌ ŹLE (Brak kontraktu)",
            "dialogue": [
              {
                "speaker": "Menedżer Tomasz",
                "text": "Dzisiaj jedziemy razem do klientów. Ja będę słuchał."
              },
              {
                "speaker": "Handlowiec Ania",
                "text": "(myśli: \"Ocenianie? Stres... będę sztywna w rozmowach\")",
                "isThought": true
              }
            ],
            "outcome": "Ania unika trudnych tematów, nie pokazuje prawdziwych umiejętności, zero rozwoju. Po dniu pracy Tomasz mówi \"było ok\", ale oboje wiedzą, że to była stracona szansa."
          },
          {
            "type": "good",
            "title": "✅ DOBRZE (Pełny kontrakt)",
            "dialogue": [
              {
                "speaker": "Tomasz",
                "text": "Dzisiaj jedziemy razem, żeby popracować nad Twoim zamykaniem sprzedaży. Chcę, żebyś widziała, jak radzisz sobie z obiekcjami i co możesz poprawić. Ja będę obserwatorem – nie wejdę do rozmowy, chyba że Ty mnie poprosisz. Po każdej wizycie przejdziemy co się udało i co możesz zrobić lepiej. Okej?"
              },
              {
                "speaker": "Ania",
                "text": "Super, od dawna chciałam nad tym popracować. Jak będziemy komunikować się przy kliencie?"
              },
              {
                "speaker": "Tomasz",
                "text": "Jeśli będziesz potrzebować pomocy, po prostu spojrzyj na mnie. Wtedy mogę wejść."
              }
            ],
            "outcome": "Ania czuje się bezpiecznie, wie czego się spodziewać, jest otwarta na feedback. W rozmowach eksperymentuje z nowymi technikami, bo wie, że to trening, nie egzamin."
          }
        ],
        "lesson": "Dobry kontrakt = psychologiczne bezpieczeństwo = prawdziwy rozwój",
        "estimated_seconds": 180,
        "xp_points": 20
      },
      {
        "id": 7,
        "type": "lightbulb",
        "title": "Kontrakt = Psychologiczne Bezpieczeństwo",
        "content": "Bez wyraźnej umowy pracownik **domyśla się** Twoich intencji i często myli:",
        "comparison": {
          "left": "Co pracownik myśli",
          "right": "Co naprawdę chcesz",
          "rows": [
            {
              "left": "❌ Ocena / Kontrola",
              "right": "✅ Rozwój / Wsparcie"
            },
            {
              "left": "❌ Krytyka",
              "right": "✅ Konstruktywny feedback"
            },
            {
              "left": "❌ Test kompetencji",
              "right": "✅ Eksperyment / Nauka"
            },
            {
              "left": "❌ \"Szukanie błędów\"",
              "right": "✅ Identyfikacja obszarów rozwoju"
            }
          ]
        },
        "quote": "\"Pracujemy NAD tobą, nie PRZECIWKO tobie\"",
        "callout": {
          "type": "info",
          "text": "Dobry kontrakt eliminuje lęk i otwiera pracownika na feedback. To fundament całego procesu OJT."
        },
        "estimated_seconds": 150,
        "xp_points": 15
      },
      {
        "id": 8,
        "type": "content",
        "title": "Etap 2: Odprawa przed rozmową z klientem",
        "content": "**Czas:** 5-10 minut przed każdą rozmową/zadaniem\n**Cel:** Przygotować pracownika do świadomego działania\n\n### 4 kluczowe elementy:\n\n**1. Przypomnienie celów**\nNa czym się dziś koncentrujemy? (np. \"Pracujemy nad techniką pytań otwartych\")\n\n**2. Analiza sytuacji**\nCo wiemy o kliencie/zadaniu? Jakie mamy narzędzia? Jaki jest kontekst?\n\n**3. Plan działania**\nJak zamierzasz to przeprowadzić? Jaki masz pomysł? Co chcesz osiągnąć?\n\n**4. Demonstracja (opcjonalnie)**\nPokażę Ci, jak to wygląda w praktyce (krótki roleplay/przykład)",
        "remember": {
          "title": "Pamiętaj:",
          "items": [
            "To NIE jest przesłuchanie – pytaj, nie odpytuj",
            "Pozwól pracownikowi samodzielnie opracować plan (Ty tylko koryguj/sugeruj)",
            "Demonstracja ≠ robienie za pracownika (pokazujesz technikę, nie rozwiązujesz problem)"
          ]
        },
        "estimated_seconds": 150,
        "xp_points": 15
      },
      {
        "id": 9,
        "type": "practice",
        "title": "Ćwiczenie: Przygotuj pytania na odprawę",
        "scenario": "Pracujesz z handlowcem Markiem nad umiejętnością **wykrywania potrzeb klienta**. Za 10 minut jedziecie do klienta \"XYZ Sp. z o.o.\" (średnia firma budowlana, 2 lata współpracy, ostatnio spadek zamówień).",
        "instruction": "Napisz 3 pytania, które zadasz Markowi na odprawie PRZED rozmową:",
        "inputs": [
          {
            "label": "1. Pytanie o cel rozwojowy:",
            "placeholder": "Wpisz swoje pytanie..."
          },
          {
            "label": "2. Pytanie o sytuację klienta:",
            "placeholder": "Wpisz swoje pytanie..."
          },
          {
            "label": "3. Pytanie o plan działania:",
            "placeholder": "Wpisz swoje pytanie..."
          }
        ],
        "sampleAnswers": [
          {
            "title": "O cel:",
            "answer": "\"Na jakich pytaniach się dzisiaj skupiamy, żeby wykryć realne potrzeby klienta XYZ?\""
          },
          {
            "title": "O sytuację:",
            "answer": "\"Co wiesz o sytuacji XYZ? Dlaczego ich zamówienia spadły?\""
          },
          {
            "title": "O plan:",
            "answer": "\"Jak planujesz rozpocząć rozmowę, żeby klient otworzył się na temat swoich wyzwań?\""
          }
        ],
        "estimated_seconds": 300,
        "xp_points": 25
      },
      {
        "id": 10,
        "type": "story",
        "title": "Przykład: Siła Demonstracji",
        "phases": [
          {
            "title": "Sytuacja:",
            "content": "Menedżer Anna pracuje z młodym handlowcem Piotrem nad **radzeniem sobie z obiekcją cenową**. Piotr teoretycznie zna techniki, ale w praktyce się wycofuje."
          },
          {
            "title": "Przed wizytą (odprawa):",
            "dialogue": [
              {
                "speaker": "Anna",
                "text": "Pokaż mi, jak odpowiesz, gdy klient powie: 'To za drogie'?"
              },
              {
                "speaker": "Piotr",
                "text": "(niepewnie) \"No... powiem że mamy najlepszą jakość...\"",
                "isThought": true
              },
              {
                "speaker": "Anna",
                "text": "Okej, zobacz jak ja bym to zrobiła. Ty jesteś klientem."
              }
            ]
          },
          {
            "title": "Demonstracja (roleplay 2 min):",
            "dialogue": [
              {
                "speaker": "Piotr (jako klient)",
                "text": "To za drogie."
              },
              {
                "speaker": "Anna",
                "text": "(spokojnie) \"Rozumiem. A z czym Pan porównuje? (pauza) Bo widzę, że korzysta Pan teraz z X, prawda? Jakie ma Pan z tym doświadczenia?\""
              }
            ]
          },
          {
            "title": "Efekt:",
            "content": "Piotr WIDZI, jak spokojnie zadać pytanie zamiast bronić się. W prawdziwej rozmowie użył tej techniki i zdobył informację, że klient porównuje cenę z najtańszą ofertą (bez serwisu). Dzięki temu wygrał kontrakt podkreślając wartość wsparcia.",
            "type": "success"
          }
        ],
        "lesson": "Demonstracja buduje pewność siebie i pokazuje \"jak to się robi naprawdę\". Warto 2 minuty roleplayu niż 20 minut teorii.",
        "estimated_seconds": 200,
        "xp_points": 20
      },
      {
        "id": 11,
        "type": "content",
        "title": "Etap 3: Obserwacja rozmowy z klientem",
        "content": "**Czas:** 30-60 minut (czas trwania zadania/rozmowy)\n**Twoja rola:** OBSERWATOR (nie uczestnik!)\n\n### Główne zasady:\n\n1. **Minimalizuj swoją aktywność** – Im mniej mówisz, tym lepiej\n2. **Zbieraj FAKTY, nie interpretacje** – Notuj co się dzieje, nie co myślisz\n3. **Zachowaj kontrakt** – Wchodź tylko gdy umówiliście się na to\n4. **Notuj kluczowe momenty** – Cytaty, reakcje klienta, sekwencja zdarzeń\n\n### Różnica: Fakty vs Interpretacje\n\n| ✅ FAKTY (notuj to) | ❌ INTERPRETACJE (unikaj) |\n|---------------------|---------------------------|\n| \"Klient zapytał: 'Ile to kosztuje?'\" | \"Klient był zainteresowany ceną\" |\n| \"Ania odpowiedziała po 3 sekundach\" | \"Ania była niepewna\" |\n| \"Klient przerwał i zmienił temat na...\" | \"Klient nie był przekonany\" |\n| \"Żadnego zamknięcia sprzedaży nie było\" | \"Brakuje jej asertywności\" |",
        "callout": {
          "type": "warning",
          "text": "⚠️ **Częsty błąd:** Wskakiwanie do rozmowy i \"ratowanie\" pracownika. To niszczy jego autorytet i odbiera szansę na naukę przez błędy!"
        },
        "estimated_seconds": 180,
        "xp_points": 20
      },
      {
        "id": 12,
        "type": "lightbulb",
        "title": "Dlaczego Fakty > Interpretacje?",
        "content": "**Interpretacje są subiektywne** - Twoja ocena \"był niepewny\" może być błędna.\n**Fakty są obiektywne** - \"Odpowiedział po 3 sekundach\" - nie do podważenia.\n\n### W analizie po rozmowie:\n\n✅ **Fakty** pozwalają pracownikowi samemu dojść do wniosków\n\n❌ **Interpretacje** wywołują obronę i sprzeciw\n\n### Przykład w praktyce:",
        "comparison": {
          "left": "❌ Interpretacja",
          "right": "✅ Fakt + Pytanie",
          "rows": [
            {
              "left": "\"Byłeś niepewny i dlatego klient się wycofał\"\nReakcja: \"Wcale nie byłem niepewny!\" → Obrona",
              "right": "\"Zauważyłem, że po pytaniu klienta o cenę odpowiedziałeś po 3 sekundach. Co się wtedy działo?\"\nReakcja: \"Tak... faktycznie się zawahałem, bo nie byłem pewien marży...\" → Refleksja"
            }
          ]
        },
        "estimated_seconds": 150,
        "xp_points": 15
      },
      {
        "id": 13,
        "type": "quiz",
        "title": "Sprawdź swoją wiedzę: Obserwacja",
        "questions": [
          {
            "question": "Która notatka jest FAKTEM, nie interpretacją?",
            "options": [
              "Klient był niezadowolony z oferty",
              "Pracownik nie miał pewności siebie",
              "Klient zapytał 3 razy o cenę konkurencji"
            ],
            "correctIndex": 2,
            "explanation": "✅ **Poprawnie!** Opcja C to czysty fakt - obiektywna obserwacja bez oceny. A i B to interpretacje, które mogą być błędne."
          },
          {
            "question": "Kiedy powinieneś wejść do rozmowy jako obserwator?",
            "options": [
              "Gdy widzę, że pracownik popełnia błąd",
              "Gdy pracownik poprosi o pomoc (zgodnie z kontraktem)",
              "Gdy rozmowa się przeciąga"
            ],
            "correctIndex": 1,
            "explanation": "✅ **Dokładnie!** Wchodzisz TYLKO gdy umówiliście się na to w kontrakcie lub gdy pracownik wyraźnie prosi. Inaczej odbierasz mu szansę na naukę."
          },
          {
            "question": "Co robisz, gdy klient zaczyna zadawać Tobie pytania (pomimo że jesteś obserwatorem)?",
            "options": [
              "Odpowiadam szczegółowo - nie mogę ignorować klienta",
              "Przekierowuję do pracownika: \"To świetne pytanie - Ania najlepiej odpowie\"",
              "Przejmuję rozmowę - to wyjątkowa sytuacja"
            ],
            "correctIndex": 1,
            "explanation": "✅ **Świetnie!** Przekierowujesz do pracownika i wzmacniasz jego autorytet. Jeśli odpowiesz sam, klient będzie kierować kolejne pytania do Ciebie, niszcząc pozycję pracownika."
          }
        ],
        "estimated_seconds": 180,
        "xp_points": 20
      },
      {
        "id": 14,
        "type": "practice",
        "title": "Ćwiczenie: Przekształć interpretacje w fakty",
        "instruction": "Masz notatki z obserwacji. Przekształć interpretacje w obiektywne fakty:",
        "scenario": "**Twoje notatki (INTERPRETACJE):**\n\n1. \"Pracownik nie słuchał klienta\"\n2. \"Klient był zdezorientowany\"\n3. \"Brak profesjonalizmu w zamknięciu\"",
        "inputs": [
          {
            "label": "1. Fakty zamiast \"nie słuchał klienta\":",
            "placeholder": "Np. Co konkretnie zaobserwowałeś?",
            "type": "textarea"
          },
          {
            "label": "2. Fakty zamiast \"klient był zdezorientowany\":",
            "placeholder": "Np. Co powiedział/zrobił klient?",
            "type": "textarea"
          },
          {
            "label": "3. Fakty zamiast \"brak profesjonalizmu\":",
            "placeholder": "Np. Co konkretnie się wydarzyło (lub NIE wydarzyło)?",
            "type": "textarea"
          }
        ],
        "sampleAnswers": [
          {
            "title": "\"Nie słuchał klienta\" →",
            "answer": "\"Klient 2 razy wspomniał o budżecie, ale pracownik kontynuował prezentację produktu premium bez odniesienia się do tej informacji\""
          },
          {
            "title": "\"Klient był zdezorientowany\" →",
            "answer": "\"Klient zapytał: 'Czyli jak to dokładnie działa?' i 'Przepraszam, nie rozumiem różnicy między X a Y'\""
          },
          {
            "title": "\"Brak profesjonalizmu\" →",
            "answer": "\"Rozmowa zakończyła się bez pytania o następne kroki. Pracownik powiedział: 'To tyle z mojej strony' i wstał\"",
            "tip": "💡 **Kluczowa różnica:** Fakty pozwalają pracownikowi samemu dojść do wniosku. Gdy powiesz \"Klient 2 razy wspomniał o budżecie...\" pracownik powie: \"Racja, powinienem był się do tego odnieść!\". Gdy powiesz \"Nie słuchałeś\" - włączy obronę."
          }
        ],
        "estimated_seconds": 360,
        "xp_points": 30
      },
      {
        "id": 15,
        "type": "content",
        "title": "Etap 4: Analiza po rozmowie z klientem",
        "content": "**Czas:** 10-15 minut po każdej rozmowie/zadaniu\n**Cel:** Przekształcić doświadczenie w wiedzę i plan rozwoju\n\n### 5-stopniowa struktura analizy:\n\n**1️⃣ ODCZUCIA** (⏱️ 1-2 minuty)\n**Pytanie:** \"Jak się czujesz po tej rozmowie?\"\n**Cel:** Rozładowanie emocji, budowanie zaufania\n\n**2️⃣ CELE** (⏱️ 1 minuta)\n**Pytanie:** \"Jakie były Twoje cele? Co chciałeś osiągnąć?\"\n**Cel:** Przypomnienie punktu odniesienia\n\n**3️⃣ PRZEBIEG** (⏱️ 3-5 minut)\n**Pytania:** \"Co poszło dobrze? Co było trudne? Co cię zaskoczyło?\"\n**Cel:** Analiza faktów, samoocena pracownika\n\n**4️⃣ ALTERNATYWY** (⏱️ 2-3 minuty)\n**Pytania:** \"Co mógłbyś zrobić inaczej? Jakie inne opcje miałeś?\"\n**Cel:** Rozwijanie myślenia strategicznego\n\n**5️⃣ WNIOSKI** (⏱️ 2-3 minuty)\n**Pytania:** \"Co wynosisz z tej rozmowy? Co zastosujesz następnym razem?\"\n**Cel:** Konkretny plan rozwoju",
        "remember": {
          "title": "Złota zasada:",
          "items": [
            "80% czasu - PRACOWNIK mówi i analizuje",
            "20% czasu - TY dajesz feedback i sugestujesz",
            "Im więcej pracownik sam odkryje, tym szybciej się rozwinie!"
          ]
        },
        "estimated_seconds": 200,
        "xp_points": 25
      },
      {
        "id": 16,
        "type": "story",
        "title": "Przykład: Analiza, która zmieniła wszystko",
        "situation": "Karol (handlowiec) wraca z nieudanej rozmowy. Klient powiedział \"pomyślimy\". Karol jest sfrustrowany. Menedżer Michał stosuje 5-stopniową analizę:",
        "phases": [
          {
            "title": "1️⃣ ODCZUCIA",
            "dialogue": [
              {
                "speaker": "Michał",
                "text": "Jak się czujesz po tej rozmowie?"
              },
              {
                "speaker": "Karol",
                "text": "Źle. Znowu 'pomyślimy'. Strata czasu."
              },
              {
                "speaker": "Michał",
                "text": "Rozumiem frustrację. Daj sobie chwilę, a potem przeanalizujmy co się wydarzyło."
              }
            ]
          },
          {
            "title": "2️⃣ CELE",
            "dialogue": [
              {
                "speaker": "Michał",
                "text": "Jaki był Twój cel na tę rozmowę?"
              },
              {
                "speaker": "Karol",
                "text": "Chciałem zamknąć ofertę na 50k."
              }
            ]
          },
          {
            "title": "3️⃣ PRZEBIEG",
            "dialogue": [
              {
                "speaker": "Michał",
                "text": "Co poszło dobrze?"
              },
              {
                "speaker": "Karol",
                "text": "Dobra prezentacja produktu, klient słuchał."
              },
              {
                "speaker": "Michał",
                "text": "A co było trudne?"
              },
              {
                "speaker": "Karol",
                "text": "Gdy zapytałem o decyzję, klient zmienił temat..."
              }
            ]
          },
          {
            "title": "4️⃣ ALTERNATYWY",
            "dialogue": [
              {
                "speaker": "Michał",
                "text": "Co mógłbyś zrobić inaczej w tym momencie?"
              },
              {
                "speaker": "Karol",
                "text": "(myśli) \"Hmm... może zamiast 'Czy podpisujemy?' zapytać 'Co musi się wydarzyć, żebyśmy mogli ruszyć do przodu?'\"",
                "isThought": true
              },
              {
                "speaker": "Michał",
                "text": "Dokładnie! A zauważyłeś, że gdy klient zaczął mówić o budżecie, przeskoczyłeś do ceny zamiast dowiedzieć się więcej?"
              }
            ]
          },
          {
            "title": "5️⃣ WNIOSKI",
            "dialogue": [
              {
                "speaker": "Michał",
                "text": "Co wynosisz na przyszłość?"
              },
              {
                "speaker": "Karol",
                "text": "Następnym razem zamiast 'czy podpisujemy' zapytam o konkretne obawy. I będę słuchał sygnałów o budżecie."
              }
            ]
          },
          {
            "title": "Efekt:",
            "content": "W kolejnej rozmowie Karol zastosował nową technikę pytań. Zamiast \"pomyślimy\" dowiedział się, że klient potrzebuje akceptacji szefa. Umówił rozmowę z decydentem i zamknął deal 65k. **Analiza zamieniła porażkę w lekcję.**",
            "type": "success"
          }
        ],
        "lesson": "Dobra analiza to nie krytyka, a odkrywanie razem. Karol SAM doszedł do wniosków - dzięki temu faktycznie je zapamiętał i zastosował.",
        "estimated_seconds": 250,
        "xp_points": 25
      },
      {
        "id": 17,
        "type": "lightbulb",
        "title": "Pytaj, nie mów - dlaczego to działa?",
        "comparison": {
          "left": "❌ GDY MÓWISZ (Dajesz gotowe odpowiedzi)",
          "right": "✅ GDY PYTASZ (Pomagasz odkryć)",
          "rows": [
            {
              "left": "\"Powinieneś był zapytać o budżet\"",
              "right": "\"Co mogłeś zapytać, żeby dowiedzieć się więcej?\""
            },
            {
              "left": "Pracownik słucha pasywnie",
              "right": "Pracownik aktywnie myśli"
            },
            {
              "left": "Zależność od Twojej wiedzy",
              "right": "Budowanie samodzielności"
            },
            {
              "left": "\"Spróbuję to zapamiętać\"",
              "right": "\"Sam na to wpadłem - zostanie ze mną\""
            },
            {
              "left": "Możliwa obrona / \"Ale ja...\"",
              "right": "Refleksja / \"Faktycznie, racja...\""
            }
          ]
        },
        "whenToTell": {
          "title": "Kiedy MÓWIĆ (dawać feedback bezpośrednio)?",
          "items": [
            "✅ Gdy pracownik nie widzi błędu mimo pytań",
            "✅ Gdy brakuje mu wiedzy technicznej",
            "✅ Gdy zauważasz wzorzec, którego on nie dostrzega",
            "✅ Po tym jak SAM przeanalizował - wtedy dodajesz swoją perspektywę"
          ]
        },
        "quote": "\"Ludzie wspierają świat, który sami stworzyli\"",
        "callout": {
          "type": "info",
          "text": "Gdy pracownik SAM odkrywa rozwiązanie, czuje się autorem - i dlatego je wdraża."
        },
        "estimated_seconds": 180,
        "xp_points": 20
      },
      {
        "id": 18,
        "type": "quiz",
        "title": "Sprawdź swoją wiedzę: Analiza",
        "questions": [
          {
            "question": "Jak powinieneś zacząć analizę po rozmowie?",
            "options": [
              "\"Zrobiłeś 3 błędy - omówmy je po kolei\"",
              "\"Jak się czujesz po tej rozmowie?\"",
              "\"Jakie były cele tej rozmowy?\""
            ],
            "correctIndex": 1,
            "explanation": "✅ **Dokładnie!** Zaczynasz od ODCZUĆ - to rozładowuje emocje i buduje bezpieczną atmosferę. Dopiero potem przecodzisz do analizy merytorycznej."
          },
          {
            "question": "Co robisz, gdy pracownik neguje swój błąd mimo faktów?",
            "options": [
              "Daję mu rację - nie warto się kłócić",
              "Upieramy się - przecież mam notatki!",
              "Przedstawiam fakty i pytam o alternatywną interpretację"
            ],
            "correctIndex": 2,
            "explanation": "✅ **Świetnie!** \"Zauważyłem, że klient 2 razy wspomniał o budżecie, a Ty kontynuowałeś prezentację premium. Jak Ty to widziałeś?\". Fakty + otwarte pytanie = przestrzeń na dialog."
          },
          {
            "question": "Jak powinny brzmieć dobre WNIOSKI z analizy?",
            "options": [
              "\"Ogólnie było ok, następnym razem lepiej\"",
              "\"Następnym razem zamiast 'czy podpisujemy' zapytam 'co musi się wydarzyć, żeby ruszyć do przodu'\"",
              "\"Muszę popracować nad zamykaniem sprzedaży\""
            ],
            "correctIndex": 1,
            "explanation": "✅ **Dokładnie!** Dobre wnioski są KONKRETNE i WYKONALNE. \"Następnym razem zrobię X zamiast Y\" to plan działania, nie ogólnikowa deklaracja."
          }
        ],
        "estimated_seconds": 180,
        "xp_points": 20
      },
      {
        "id": 19,
        "type": "practice",
        "title": "Ćwiczenie: Przekształć krytykę w pytania coachingowe",
        "instruction": "Masz notatkę z obserwacji i chcesz dać feedback. Zamień dyrektywną krytykę na pytania, które pomogą pracownikowi samemu dojść do wniosków:",
        "scenario": "**Scenariusz:**\n\nHandlowiec Ania prezentowała produkt klientowi, który wspomniał \"mamy ograniczony budżet w tym kwartale\". Ania zignorowała to i dalej prezentowała drogie opcje. Klient się wycofał.\n\n**❌ Twój impuls (krytyka):**\n\n1. \"Nie słuchałaś klienta\"\n2. \"Powinnaś była przejść na tańsze opcje\"\n3. \"Straciłaś szansę na deal\"",
        "inputs": [
          {
            "label": "Przekształć 1: \"Nie słuchałaś klienta\" → Pytanie coachingowe:",
            "placeholder": "Jak możesz to przeformułować jako pytanie?",
            "type": "textarea"
          },
          {
            "label": "Przekształć 2: \"Powinnaś była przejść na tańsze opcje\" → Pytanie:",
            "placeholder": "Jak możesz pomóc jej samej dojść do tego wniosku?",
            "type": "textarea"
          },
          {
            "label": "Przekształć 3: \"Straciłaś szansę\" → Pytanie o wnioski:",
            "placeholder": "Jak zapytać o plan na przyszłość?",
            "type": "textarea"
          }
        ],
        "sampleAnswers": [
          {
            "title": "\"Nie słuchałaś\" →",
            "answer": "\"Zauważyłam, że klient wspomniał o ograniczonym budżecie, a Ty kontynuowałaś prezentację opcji premium. Co się wtedy działo?\"",
            "explanation": "→ Fakty + otwarte pytanie, bez osądu"
          },
          {
            "title": "\"Powinnaś była przejść na tańsze opcje\" →",
            "answer": "\"Co mogłaś zrobić w momencie, gdy usłyszałaś 'ograniczony budżet'? Jakie alternatywy miałaś?\"",
            "explanation": "→ Pomoż jej samej znaleźć rozwiązanie"
          },
          {
            "title": "\"Straciłaś szansę\" →",
            "answer": "\"Co wynosisz z tej sytuacji na przyszłość? Jak zareagujesz, gdy kolejny klient wspomni o budżecie?\"",
            "explanation": "→ Konkretny plan działania, nie poczucie winy",
            "tip": "**Efekt pytań vs krytyki:**\n\n**Krytyka:** Ania czuje się oceniona, wchodzi w obronę: \"Ale ja chciałam pokazać najlepsze produkty!\"\n\n**Pytania:** Ania analizuje: \"Faktycznie, powinienem była zapytać o konkretny budżet i dostosować ofertę... następnym razem zacznę od tego pytania\""
          }
        ],
        "estimated_seconds": 420,
        "xp_points": 35
      },
      {
        "id": 20,
        "type": "content",
        "title": "Etap 5: Podsumowanie całego dnia",
        "content": "**Czas:** 15-20 minut na koniec wspólnego dnia pracy\n**Cel:** Rozliczyć cele dnia i stworzyć plan wdrożeniowy\n\n### 3 kluczowe elementy:\n\n**1️⃣ ROZLICZENIE CELÓW DNIA**\n\n**Pytania:**\n- \"Nad czym pracowaliśmy dziś?\" (przypomnienie celów z rana)\n- \"Co udało Ci się poprawić w stosunku do poprzedniego dnia?\"\n- \"Gdzie widzisz największy postęp?\"\n\n**2️⃣ PLAN DZIAŁAŃ WDROŻENIOWYCH**\n\n**Konkrety na przyszłość:**\n- 1-3 konkretne zachowania do zastosowania w najbliższym tygodniu\n- Mierzalne cele (np. \"Zadać min. 3 pytania otwarte w każdej rozmowie\")\n- Umówienie kolejnej sesji OJT (jeśli proces trwa dalej)\n\n**3️⃣ RAPORT / POTWIERDZENIE**\n\n**Dokumentacja:**\n- Pracownik zapisuje swoje wnioski (własność procesu)\n- Ty zapisujesz obserwacje i plan na następną sesję\n- Wspólne potwierdzenie planu wdrożeniowego",
        "remember": {
          "title": "Pamiętaj:",
          "items": [
            "Podsumowanie ≠ podsumowanie TYLKO Twoich obserwacji",
            "To przede wszystkim refleksja PRACOWNIKA nad całym dniem",
            "Dokumentuj plan wdrożeniowy - to commitment, nie deklaracja"
          ]
        },
        "callout": {
          "type": "warning",
          "text": "⚠️ **Częsty błąd:** Kończenie dnia \"ogólnie było dobrze, dzięki za czas\". Bez konkretnego planu wdrożenia wnioski się rozplywają w ciągu tygodnia!"
        },
        "estimated_seconds": 200,
        "xp_points": 25
      },
      {
        "id": 21,
        "type": "data",
        "title": "Jak często robić trening OJT?",
        "stats": [
          {
            "value": "1x/tydzień",
            "label": "Minimalną częstotliwość dla efektywnego rozwoju",
            "trend": "up"
          },
          {
            "value": "2-3x/miesiąc",
            "label": "Optymalną intensywność dla utrwalenia umiejętności",
            "trend": "up"
          },
          {
            "value": "1x/kwartał",
            "label": "To za rzadko - efekt rozwoju jest znikomy",
            "trend": "down"
          }
        ],
        "callout": {
          "type": "info",
          "text": "**Kluczowy wniosek:** Trening OJT wymaga REGULARNOŚCI. Lepiej 1 dzień co 2 tygodnie przez 3 miesiące niż 3 dni z rzędu raz na pół roku. Mózg potrzebuje czasu na przetworzenie feedbacku i wypróbowanie nowych zachowań."
        },
        "infoBoxes": [
          {
            "title": "✅ Nowy pracownik (0-3 miesiące):",
            "content": "2-3 razy w tygodniu - intensywny trening podstawowych umiejętności"
          },
          {
            "title": "✅ Rozwijający się pracownik (3-12 miesięcy):",
            "content": "1 raz w tygodniu - praca nad konkretnymi kompetencjami (np. zamykanie, obsługa obiekcji)"
          },
          {
            "title": "✅ Doświadczony pracownik (1+ rok):",
            "content": "2-3 razy w miesiącu - doskonalenie zaawansowanych technik, rozwijanie nowych obszarów"
          }
        ],
        "sources": ["ATD Coaching Best Practices 2024", "Harvard Business Review \"Frequency of Coaching\""],
        "estimated_seconds": 180,
        "xp_points": 20
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
              {
                "speaker": "Menedżer",
                "text": "Co wynosisz z dzisiejszego treningu?"
              },
              {
                "speaker": "Handlowiec",
                "text": "Muszę popracować nad zadawaniem pytań i lepiej słuchać klienta."
              },
              {
                "speaker": "Menedżer",
                "text": "Super, to się tym zajmij. Powodzenia!"
              }
            ],
            "outcome": "Tydzień później nic się nie zmieniło. \"Popracować nad pytaniami\" to nie plan, to deklaracja. Brak konkretów = brak zmian."
          },
          {
            "type": "good",
            "title": "✅ DOBRZE (SMART plan wdrożeniowy)",
            "dialogue": [
              {
                "speaker": "Menedżer",
                "text": "Co KONKRETNIE zastosujesz w najbliższym tygodniu?"
              },
              {
                "speaker": "Handlowiec",
                "text": "W każdej rozmowie z klientem zadam min. 3 pytania otwarte zanim przejdę do prezentacji produktu."
              },
              {
                "speaker": "Menedżer",
                "text": "Świetnie! Możesz to zapisać? A jak będziesz mierzył postęp?"
              },
              {
                "speaker": "Handlowiec",
                "text": "(pisze) \"Po każdej rozmowie zaznaczę w CRM czy zadałem 3+ pytania. W piątek wyślę Ci raport.\""
              },
              {
                "speaker": "Menedżer",
                "text": "Okej. A co zrobisz, gdy zapomnisz i przeskoczysz od razu do oferty?"
              },
              {
                "speaker": "Handlowiec",
                "text": "Zatrzymam się i powiem: 'Zanim przejdę dalej, chciałbym zrozumieć Państwa sytuację - jak teraz rozwiązujecie X?'"
              },
              {
                "speaker": "Menedżer",
                "text": "Doskonale. Umówmy się na feedback za tydzień - zajrzymy do CRM i omówimy jak poszło."
              }
            ],
            "outcome": "Tydzień później: 12/15 rozmów z min. 3 pytaniami otwarymi. W 3 rozmowach zapomniał, ale użył techniki \"cofnięcia się\". Konwersja wzrosła o 18%. **Konkretny plan = mierzalny efekt.**"
          }
        ],
        "lesson": "Dobry plan wdrożeniowy to: 1-3 konkretne zachowania + sposób mierzenia + plan na wypadek zapomnienia + termin sprawdzenia postępu. Bez tego feedback = strata czasu.",
        "estimated_seconds": 220,
        "xp_points": 25
      },
      {
        "id": 23,
        "type": "quiz",
        "title": "Sprawdź swoją wiedzę: Podsumowanie Modelu OJT",
        "questions": [
          {
            "question": "Jaka jest GŁÓWNA różnica między treningiem OJT a tradycyjnym szkoleniem?",
            "options": [
              "OJT jest tańszy i szybszy",
              "Uczysz się PRACUJĄC, nie przerywasz pracy by się uczyć",
              "OJT wymaga mniej przygotowania"
            ],
            "correctIndex": 1,
            "explanation": "✅ **Dokładnie!** W OJT nauka jest integralną częścią pracy - nie odrywasz pracownika od zadań, tylko przekształcasz zadania w okazję do rozwoju. To zasadnicza zmiana paradygmatu."
          },
          {
            "question": "Który etap OJT powtarza się 3-5 razy dziennie w cyklu?",
            "options": [
              "Rozmowa na początku dnia + Podsumowanie dnia",
              "Odprawa → Obserwacja → Analiza (dla każdego zadania)",
              "Wszystkie 5 etapów powtarzamy w kółko"
            ],
            "correctIndex": 1,
            "explanation": "✅ **Świetnie!** Etapy 2-3-4 (Odprawa-Obserwacja-Analiza) tworzą cykl powtarzalny dla każdej rozmowy/zadania. Etap 1 (Start) i 5 (Podsumowanie) ramują cały dzień."
          },
          {
            "question": "Jaka jest ZŁOTA ZASADA feedbacku w treningu OJT?",
            "options": [
              "Zawsze zacznij od pozytywów (metoda kanapki)",
              "Pytaj, nie mów - pomóż pracownikowi samemu odkryć wnioski",
              "Dawaj feedback natychmiast po każdym błędzie"
            ],
            "correctIndex": 1,
            "explanation": "✅ **Doskonale!** \"Pytaj, nie mów\" to fundament OJT. 80% czasu pracownik analizuje sam, 20% Ty uzupełniasz perspektywą. Ludzie wspierają świat, który sami stworzyli."
          }
        ],
        "estimated_seconds": 180,
        "xp_points": 20
      },
      {
        "id": 24,
        "type": "habit",
        "title": "Zbuduj swoje nawyki trenera OJT",
        "description": "Wybierz **1-2 nawyki**, które chcesz wdrożyć w ciągu najbliższych 30 dni. Zaznacz te, które są dla Ciebie priorytetem:",
        "habits": [
          {
            "id": "habit_1",
            "icon": "🗓️",
            "title": "Regularny harmonogram OJT",
            "description": "Zaplanować minimum 1 dzień OJT tygodniowo z każdym kluczowym pracownikiem przez najbliższe 3 miesiące",
            "goal": "→ Cel: Systematyczność, nie jednorazowe akcje"
          },
          {
            "id": "habit_2",
            "icon": "📝",
            "title": "Notowanie faktów, nie interpretacji",
            "description": "Podczas obserwacji zapisywać TYLKO to co widzę i słyszę - cytaty, zachowania, reakcje. Zero ocen.",
            "goal": "→ Cel: Obiektywny feedback oparty na faktach"
          },
          {
            "id": "habit_3",
            "icon": "❓",
            "title": "5 pytań zanim dam radę",
            "description": "W każdej analizie zadać minimum 5 pytań coachingowych ZANIM powiem co pracownik powinien zrobić",
            "goal": "→ Cel: Rozwijać samodzielność zamiast zależność ode mnie"
          },
          {
            "id": "habit_4",
            "icon": "✅",
            "title": "Konkretny plan wdrożeniowy",
            "description": "Kończyć każdą sesję OJT spisanym planem: 1-3 zachowania + sposób mierzenia + termin sprawdzenia",
            "goal": "→ Cel: Przekształcić feedback w realne zmiany"
          }
        ],
        "tip": "💡 **Wskazówka:** Wybierz maksymalnie 2 nawyki. Lepiej wdrożyć 2 w 100% niż 4 w 25%. Po 30 dniach oceń postęp i rozważ dodanie kolejnego.",
        "estimated_seconds": 180,
        "xp_points": 20
      },
      {
        "id": 25,
        "type": "checklist",
        "title": "Twoja Checklista Trenera OJT",
        "description": "Użyj tej checklisty przed, w trakcie i po każdej sesji OJT:",
        "sections": [
          {
            "title": "📋 Przed wspólnym dniem pracy:",
            "items": [
              "Ustalony cel rozwojowy na dzisiejszą sesję (1-2 umiejętności)",
              "Przygotowany plan dnia (lista klientów/zadań)",
              "Notatnik gotowy do zbierania faktów"
            ]
          },
          {
            "title": "🤝 Na początku dnia (Etap 1):",
            "items": [
              "Sprzedałem ideę treningu (dlaczego to się opłaca)",
              "Zawarliśmy kontrakt (role, zasady, sygnały pomocy)",
              "Wspólnie ustaliliśmy cele rozwojowe"
            ]
          },
          {
            "title": "🔄 Przed każdą rozmową/zadaniem (Etap 2):",
            "items": [
              "Przypomnieliśmy cele rozwojowe",
              "Przeanalizowaliśmy sytuację/kontekst",
              "Pracownik ma plan działania",
              "Jeśli potrzeba - pokazałem demonstrację"
            ]
          },
          {
            "title": "👀 Podczas obserwacji (Etap 3):",
            "items": [
              "Zachowuję rolę obserwatora (minimalna aktywność)",
              "Notuję FAKTY (cytaty, zachowania), nie interpretacje",
              "Wchodzę TYLKO zgodnie z kontraktem"
            ]
          },
          {
            "title": "💬 Po każdej rozmowie/zadaniu (Etap 4):",
            "items": [
              "Zacząłem od ODCZUĆ pracownika",
              "Przypomniałem CELE tej rozmowy",
              "Przeanalizowaliśmy PRZEBIEG (co dobrze, co trudne)",
              "Zadałem pytania o ALTERNATYWY (co inaczej)",
              "Pracownik sformułował konkretne WNIOSKI"
            ]
          },
          {
            "title": "🏁 Na koniec dnia (Etap 5):",
            "items": [
              "Rozliczyliśmy cele całego dnia",
              "Ustaliliśmy 1-3 konkretne zachowania do wdrożenia",
              "Zapisaliśmy plan wdrożeniowy (co, jak mierzyć, kiedy sprawdzić)",
              "Umówiliśmy kolejną sesję OJT"
            ]
          }
        ],
        "estimated_seconds": 180,
        "xp_points": 20
      },
      {
        "id": 26,
        "type": "lightbulb",
        "title": "Ostatnie Zrozumienie: OJT to Inwestycja, nie Koszt",
        "content": "Słyszysz czasem: **\"Nie mam czasu na OJT - mam cele do zrealizowania\"**?\n\nTo jak powiedzieć: \"Nie mam czasu ostrzyć piły - mam drzewo do ścięcia\". Oto liczby, które zmienią Twoją perspektywę:",
        "comparison": {
          "left": "❌ BEZ OJT (praca tradycyjna)",
          "right": "✅ Z OJT (systematyczny rozwój)",
          "rows": [
            {
              "left": "**Czas onboardingu:** 6-9 miesięcy do pełnej produktywności",
              "right": "**Czas onboardingu:** 3-4 miesiące do pełnej produktywności"
            },
            {
              "left": "**Błędy:** Pracownik uczy się na własnych błędach (kosztownych)",
              "right": "**Błędy:** Minimalizowane przez feedback w czasie rzeczywistym"
            },
            {
              "left": "**Rozwój:** Losowy, zależny od doświadczeń",
              "right": "**Rozwój:** Kierunkowy, 4x szybszy"
            },
            {
              "left": "**Twój czas:** Ratowanie sytuacji, gaszenie pożarów",
              "right": "**Twój czas:** Inwestycja w kompetencje = mniej pożarów"
            },
            {
              "left": "**Wynik:** Zespół zależny od Ciebie",
              "right": "**Wynik:** Zespół samodzielny i rosnący"
            }
          ]
        },
        "caseStudy": {
          "title": "📊 ROI treningu OJT (przykład rzeczywisty):",
          "content": "**Zespół sprzedażowy 10 osób, menedżer Tomasz:**\n\n**Inwestycja:**\n• 1 dzień/tydzień OJT z każdym handlowcem (rotacja)\n• 52 dni OJT rocznie = ~10% czasu Tomasza\n\n**Efekt po 6 miesiącach:**\n• Średnia konwersja wzrosła z 18% do 27% (+50%)\n• Średni deal size wzrósł o 15% (lepsza kvalifikacja)\n• Rotacja zespołu spadła z 25% do 8% rocznie\n• Tomasz przestał gasić pożary - zespół rozwiązuje problemy sam\n\n**ROI: 450%** - każda złotówka zainwestowana w OJT wróciła jako 4.5 zł zysku"
        },
        "quote": "\"Jeśli myślisz, że szkolenie jest drogie - spróbuj ignorancji\"\n\n- Derek Bok, były rektor Uniwersytetu Harvarda",
        "estimated_seconds": 200,
        "xp_points": 25
      },
      {
        "id": 27,
        "type": "test",
        "title": "Test Końcowy: Model Treningu OJT",
        "description": "Sprawdź swoją wiedzę z całej lekcji. Musisz uzyskać minimum **80%** aby odblokować certyfikat.",
        "requirements": {
          "questions": 10,
          "timeLimit": "2:30",
          "passingScore": "80%"
        },
        "note": "💡 Test obejmuje wszystkie 5 etapów modelu OJT, fakty vs interpretacje, pytania coachingowe i plany wdrożeniowe",
        "estimated_seconds": 600,
        "xp_points": 50
      },
      {
        "id": 28,
        "type": "achievement",
        "badge": "🏆",
        "title": "Certyfikowany Trener OJT!",
        "description": "Gratulacje! Opanowałeś 5-etapowy model treningu On-the-Job. Teraz możesz skutecznie rozwijać kompetencje swojego zespołu bez odrywania się od codziennej pracy.",
        "skills": [
          "✅ Prowadzenie kontraktu na wspólną pracę z psychologicznym bezpieczeństwem",
          "✅ Zbieranie faktów podczas obserwacji (bez interpretacji i osądów)",
          "✅ Prowadzenie 5-etapowej analizy feedbackowej (Odczucia-Cele-Przebieg-Alternatywy-Wnioski)",
          "✅ Zadawanie pytań coachingowych zamiast dawania gotowych rad",
          "✅ Tworzenie konkretnych planów wdrożeniowych (SMART)",
          "✅ Systematyczne rozwijanie zespołu przez cykl powtarzalnych sesji OJT"
        ],
        "xpReward": 300,
        "badgeName": "OJT Master",
        "estimated_seconds": 60,
        "xp_points": 300
      },
      {
        "id": 29,
        "type": "ending",
        "title": "Twoje Następne Kroki",
        "content": "Ukończyłeś lekcję, ale to dopiero początek! Wiedza teoretyczna nic nie da bez wdrożenia. Oto Twój plan na najbliższe 30 dni:",
        "checklist": {
          "title": "📋 Checklist 30 dni wdrożenia:",
          "items": [
            "**Dzień 1-3:** Wybierz 1-2 pracowników do pierwszej sesji OJT",
            "**Dzień 4-7:** Zaplanuj pierwszą sesję OJT (data, cele rozwojowe, lista klientów/zadań)",
            "**Dzień 8:** Przeprowadź pierwszą sesję OJT stosując wszystkie 5 etapów",
            "**Dzień 9:** Oceń co poszło dobrze, co trudne - zapisz wnioski",
            "**Dzień 15:** Druga sesja OJT (zastosuj wnioski z pierwszej)",
            "**Dzień 22:** Trzecia sesja OJT (budowanie rutyny)",
            "**Dzień 30:** Ocena postępu - czy widzisz rozwój pracownika? Dostosuj harmonogram"
          ]
        },
        "resources": [
          {
            "title": "📄 Szablon kontraktu OJT",
            "description": "Gotowy formularz do uzgodnienia zasad współpracy z pracownikiem"
          },
          {
            "title": "📝 Karta obserwacji OJT",
            "description": "Szablon do notowania faktów podczas obserwacji rozmów"
          },
          {
            "title": "✅ Checklist analizy (5 kroków)",
            "description": "Struktura rozmowy feedbackowej do wydruku"
          },
          {
            "title": "📊 Tracker postępów OJT",
            "description": "Excel do śledzenia rozwoju pracowników (cele → sesje → wnioski)"
          }
        ],
        "quote": "\"Najlepsi liderzy nie rozwijają ludzi *zamiast* osiągać cele.\nOni osiągają cele *poprzez* rozwijanie ludzi.\"\n\n- Simon Sinek",
        "finalMessage": "Powodzenia w rozwijaniu Twojego zespołu! 🚀\n\nMasz pytania? Dołącz do społeczności trenerów OJT w zakładce Forum",
        "estimated_seconds": 180,
        "xp_points": 0
      }
    ]
  }$$::jsonb
);
