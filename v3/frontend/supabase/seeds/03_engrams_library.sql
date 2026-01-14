-- Day 9 Seed: Biblioteka Engramów (10 Nowych Engramów) - WERSJA POLSKA
-- Leadership: 3, Sales: 3, Strategy: 2, Mindset: 2

-- ========================================
-- KATEGORIA LEADERSHIP (3 engramy)
-- ========================================

-- 1. Podstawy Budowania Zespołu
INSERT INTO engrams (id, title, category, description, xp_reward, estimated_minutes, stat_category, stat_points, prerequisites, content_json)
VALUES (
  'e1000000-0000-0000-0000-000000000001',
  'Podstawy Budowania Zespołu',
  'Leadership',
  'Fundamenty tworzenia wysoko efektywnych zespołów',
  50,
  5,
  'Leadership',
  15,
  '[]'::jsonb,
  $$ {
    "slides": [
      {
        "type": "intro",
        "title": "Podstawy Budowania Zespołu",
        "content": "Poznaj fundamentalne zasady tworzenia i prowadzenia efektywnych zespołów."
      },
      {
        "type": "content",
        "title": "5 Etapów Rozwoju Zespołu",
        "content": "**Model Tuckmana:**\n\n1. **Forming (Formowanie)** - Zespół się tworzy\n2. **Storming (Burza)** - Pojawiają się konflikty\n3. **Norming (Normowanie)** - Ustalane są zasady\n4. **Performing (Działanie)** - Produktywna praca\n5. **Adjourning (Zakończenie)** - Misja wykonana\n\nZrozumienie tych etapów pomaga nawigować dynamiką zespołu."
      },
      {
        "type": "content",
        "title": "Kluczowe Role w Zespole",
        "content": "Każdy wysoko efektywny zespół potrzebuje:\n\n- **Lidera** - Wyznacza kierunek\n- **Koordynatora** - Organizuje pracę\n- **Realizatora** - Wykonuje zadania\n- **Innowatora** - Generuje pomysły\n- **Ewaluatora** - Kontrola jakości"
      },
      {
        "type": "quiz",
        "question": "Jaki jest 3. etap w modelu Tuckmana?",
        "options": [
          "Forming (Formowanie)",
          "Storming (Burza)",
          "Norming (Normowanie)",
          "Performing (Działanie)"
        ],
        "correctAnswer": 2,
        "explanation": "Norming to 3. etap, w którym zespół ustala zasady i normy po przepracowaniu początkowych konfliktów."
      }
    ]
  } $$
);

-- 2. Mistrz Delegowania
INSERT INTO engrams (id, title, category, description, xp_reward, estimated_minutes, stat_category, stat_points, prerequisites, content_json)
VALUES (
  'e1000000-0000-0000-0000-000000000002',
  'Mistrz Delegowania',
  'Leadership',
  'Opanuj sztukę efektywnego delegowania zadań',
  60,
  7,
  'Leadership',
  20,
  '["e1000000-0000-0000-0000-000000000001"]'::jsonb,
  $$ {
    "slides": [
      {
        "type": "intro",
        "title": "Mistrz Delegowania",
        "content": "Delegowanie to nie tylko przerzucanie pracy - to wzmacnianie zespołu."
      },
      {
        "type": "content",
        "title": "4 Poziomy Delegowania",
        "content": "**Poziom 1:** Zróbto dokładnie jak mówię\n**Poziom 2:** Zbadaj temat i wróć z raportem\n**Poziom 3:** Zaproponuj rozwiązanie, potem działaj\n**Poziom 4:** Działaj samodzielnie, raportuj wyniki\n\nDopasuj poziom do doświadczenia osoby i krytyczności zadania."
      },
      {
        "type": "content",
        "title": "Formuła Delegowania",
        "content": "**Delegowanie SMART:**\n\n- **S**pecyficzne - Jasna definicja zadania\n- **M**ierzalne - Jak poznać, że gotowe\n- **A**kceptowalne - W zakresie ich możliwości\n- **R**elevantne - Pasuje do ich roli\n- **T**erminowe - Jasny deadline\n\nTest: Czy osoba wie CO, JAK, KIEDY i PO CO?"
      },
      {
        "type": "quiz",
        "question": "Który poziom delegowania daje największą autonomię?",
        "options": [
          "Poziom 1: Zrób jak mówię",
          "Poziom 2: Zbadaj i raportuj",
          "Poziom 3: Zaproponuj, potem działaj",
          "Poziom 4: Działaj samodzielnie"
        ],
        "correctAnswer": 3,
        "explanation": "Poziom 4 (Działaj samodzielnie, raportuj wyniki) daje maksymalną autonomię - idealny dla doświadczonych członków zespołu przy rutynowych zadaniach."
      }
    ]
  } $$
);

-- 3. Rozwiązywanie Konfliktów 101
INSERT INTO engrams (id, title, category, description, xp_reward, estimated_minutes, stat_category, stat_points, prerequisites, content_json)
VALUES (
  'e1000000-0000-0000-0000-000000000003',
  'Rozwiązywanie Konfliktów 101',
  'Leadership',
  'Nawiguj konflikty zespołowe z pewnością siebie',
  50,
  6,
  'Leadership',
  15,
  '[]'::jsonb,
  $$ {
    "slides": [
      {
        "type": "intro",
        "title": "Rozwiązywanie Konfliktów 101",
        "content": "Konflikt jest nieunikniony - ale nie musi być destrukcyjny."
      },
      {
        "type": "content",
        "title": "5 Stylów Konfliktu (Thomas-Kilmann)",
        "content": "**Konkurowanie** - Wygrać/Przegrać (asertywny, niekooperacyjny)\n**Współpraca** - Wygrać/Wygrać (asertywny, kooperacyjny)\n**Kompromis** - Podział na pół\n**Unikanie** - Wycofanie się z konfliktu\n**Ustępowanie** - Przegrać/Wygrać (ustąpienie innym)\n\nNajlepszy domyślny: **Współpraca** przy ważnych kwestiach."
      },
      {
        "type": "content",
        "title": "3-Krokowy Proces Rozwiązania",
        "content": "1. **Słuchaj Najpierw** - Zrozum obie strony\n2. **Znajdź Wspólny Grunt** - Wspólne cele\n3. **Współtwórz Rozwiązanie** - Zaangażuj obie strony\n\n**Klucz:** Skup się na interesach, nie na pozycjach."
      },
      {
        "type": "quiz",
        "question": "Który styl konfliktu dąży do Wygrać/Wygrać?",
        "options": [
          "Konkurowanie",
          "Unikanie",
          "Współpraca",
          "Kompromis"
        ],
        "correctAnswer": 2,
        "explanation": "Współpraca to styl Wygrać/Wygrać - jednocześnie asertywny ORAZ kooperacyjny, szukający rozwiązań satysfakcjonujących obie strony."
      }
    ]
  } $$
);

-- ========================================
-- KATEGORIA SALES (3 engramy)
-- ========================================

-- 4. Podstawy SPIN Selling
INSERT INTO engrams (id, title, category, description, xp_reward, estimated_minutes, stat_category, stat_points, prerequisites, content_json)
VALUES (
  'e2000000-0000-0000-0000-000000000001',
  'Podstawy SPIN Selling',
  'Sales',
  'Opanuj technikę pytań SPIN',
  50,
  6,
  'Sales',
  15,
  '[]'::jsonb,
  $$ {
    "slides": [
      {
        "type": "intro",
        "title": "SPIN Selling",
        "content": "SPIN to najbardziej naukowo sprawdzona metodologia sprzedaży - oparta na 35 000 rozmów handlowych."
      },
      {
        "type": "content",
        "title": "Framework SPIN",
        "content": "**S** - Pytania Sytuacyjne (kontekst)\n**P** - Pytania Problemowe (ból)\n**I** - Pytania Implikacyjne (konsekwencje)\n**N** - Pytania Zyskowe (wartość)\n\nPrzykład:\n- S: 'Ilu macie handlowców?'\n- P: 'Jaki jest największy problem z onboardingiem?'\n- I: 'Jak wolny onboarding wpływa na przychody?'\n- N: 'Co by znaczyło skrócenie onboardingu o połowę?'"
      },
      {
        "type": "content",
        "title": "Dlaczego SPIN Działa",
        "content": "Tradycyjna sprzedaż: Mów o features\nSPIN selling: **Pomóż kupującym odkryć własne potrzeby**\n\nKupujący przekonani własnymi argumentami: 85% skuteczności\nKupujący przekonani argumentami sprzedawcy: 13% skuteczności"
      },
      {
        "type": "quiz",
        "question": "Które pytanie SPIN odkrywa punkty bólu?",
        "options": [
          "Sytuacyjne (Situation)",
          "Problemowe (Problem)",
          "Implikacyjne (Implication)",
          "Zyskowe (Need-Payoff)"
        ],
        "correctAnswer": 1,
        "explanation": "Pytania Problemowe identyfikują trudności, wyzwania i punkty bólu w obecnej sytuacji."
      }
    ]
  } $$
);

-- 5. Canvas Propozycji Wartości
INSERT INTO engrams (id, title, category, description, xp_reward, estimated_minutes, stat_category, stat_points, prerequisites, content_json)
VALUES (
  'e2000000-0000-0000-0000-000000000002',
  'Canvas Propozycji Wartości',
  'Sales',
  'Projektuj nieodparte propozycje wartości',
  60,
  8,
  'Sales',
  20,
  '["e2000000-0000-0000-0000-000000000001"]'::jsonb,
  $$ {
    "slides": [
      {
        "type": "intro",
        "title": "Canvas Propozycji Wartości",
        "content": "Propozycja wartości to obietnica wartości do dostarczenia."
      },
      {
        "type": "content",
        "title": "Profil Klienta (Prawa Strona)",
        "content": "**Zadania Klienta (Jobs):**\nCo próbują osiągnąć?\n\n**Bóle (Pains):**\nCo ich frustruje?\n\n**Korzyści (Gains):**\nCo by ich ucieszyło?\n\nPrzykład: CRM dla zespołów sprzedaży\n- Jobs: Śledzić leady, zamykać deale\n- Pains: Wprowadzanie danych, zgubione okazje\n- Gains: Wyższe win rates, automatyzacja"
      },
      {
        "type": "content",
        "title": "Mapa Wartości (Lewa Strona)",
        "content": "**Produkty/Usługi:**\nCo oferujesz\n\n**Łagodzące Bóle:**\nJak redukujesz bóle\n\n**Tworzące Korzyści:**\nJak tworzysz korzyści\n\nPrzykład:\n- Produkt: CRM z AI\n- Łagodzące bóle: Auto-wpis danych, inteligentne alerty\n- Tworzące korzyści: Analityka predykcyjna, +30% win rate"
      },
      {
        "type": "quiz",
        "question": "Co znajduje się w Profilu Klienta?",
        "options": [
          "Produkty i features",
          "Łagodzące bóle i tworzące korzyści",
          "Zadania, bóle i korzyści klienta",
          "Ceny i pakiety"
        ],
        "correctAnswer": 2,
        "explanation": "Profil Klienta (prawa strona) zawiera zadania, bóle i korzyści - zrozumienie klienta przed projektowaniem rozwiązań."
      }
    ]
  } $$
);

-- 6. Radzenie Sobie z Obiekcjami
INSERT INTO engrams (id, title, category, description, xp_reward, estimated_minutes, stat_category, stat_points, prerequisites, content_json)
VALUES (
  'e2000000-0000-0000-0000-000000000003',
  'Radzenie Sobie z Obiekcjami',
  'Sales',
  'Zamień obiekcje w szanse',
  50,
  5,
  'Sales',
  15,
  '[]'::jsonb,
  $$ {
    "slides": [
      {
        "type": "intro",
        "title": "Radzenie Sobie z Obiekcjami",
        "content": "Obiekcje to nie odrzucenie - to prośba o więcej informacji."
      },
      {
        "type": "content",
        "title": "4-Krokowy Framework",
        "content": "**1. Słuchaj** - Pozwól im dokończyć\n**2. Potwierdź** - Pokaż, że słyszałeś\n**3. Wyjaśnij** - Zadawaj pytania\n**4. Odpowiedz** - Adresuj prawdziwy problem\n\nPrzykład:\n- Obiekcja: 'Za drogie'\n- Potwierdź: 'Rozumiem, że budżet to obawa'\n- Wyjaśnij: 'Z czym to porównujesz?'\n- Odpowiedz: 'Spójrzmy na ROI...'"
      },
      {
        "type": "content",
        "title": "Częste Obiekcje",
        "content": "**Cena:** Pokaż ROI i koszt bezczynności\n**Timing:** Stwórz pilność z deadlinami\n**Konkurencja:** Wyróżnij się wartością\n**Autorytet:** Znajdź prawdziwego decydenta\n**Potrzeba:** Odkryj ukryte punkty bólu"
      },
      {
        "type": "quiz",
        "question": "Jaki jest pierwszy krok w radzeniu sobie z obiekcjami?",
        "options": [
          "Odpowiedz natychmiast",
          "Słuchaj w pełni",
          "Grzecznie nie zgadzaj się",
          "Zaoferuj zniżkę"
        ],
        "correctAnswer": 1,
        "explanation": "Zawsze najpierw słuchaj w pełni - wiele obiekcji rozwiązuje się samo, kiedy ludzie czują się wysłuchani."
      }
    ]
  } $$
);

-- ========================================
-- KATEGORIA STRATEGY (2 engramy)
-- ========================================

-- 7. Strategia Błękitnego Oceanu
INSERT INTO engrams (id, title, category, description, xp_reward, estimated_minutes, stat_category, stat_points, prerequisites, content_json)
VALUES (
  'e3000000-0000-0000-0000-000000000001',
  'Strategia Błękitnego Oceanu',
  'Strategy',
  'Stwórz niekwestionowaną przestrzeń rynkową',
  60,
  8,
  'Strategy',
  20,
  '[]'::jsonb,
  $$ {
    "slides": [
      {
        "type": "intro",
        "title": "Strategia Błękitnego Oceanu",
        "content": "Przestań konkurować w krwawych czerwonych oceanach. Twórz błękitne oceany, gdzie konkurencja jest nieistotna."
      },
      {
        "type": "content",
        "title": "Czerwony Ocean vs Błękitny Ocean",
        "content": "**Czerwony Ocean:**\n- Konkuruj na istniejącym rynku\n- Pokonaj konkurencję\n- Wykorzystaj istniejący popyt\n\n**Błękitny Ocean:**\n- Stwórz nową przestrzeń rynkową\n- Uczyń konkurencję nieistotną\n- Stwórz i przechwyć nowy popyt\n\nPrzykład: Cirque du Soleil (nie cyrk, nie teatr - oba)"
      },
      {
        "type": "content",
        "title": "Siatka ERRC (Wyeliminuj-Zredukuj-Podnieś-Stwórz)",
        "content": "**Wyeliminuj:** Co możemy usunąć?\n**Zredukuj:** Co możemy zmniejszyć poniżej standardu?\n**Podnieś:** Co możemy podnieść powyżej standardu?\n**Stwórz:** Co możemy stworzyć, czego nigdy nie było?\n\nPrzykład - Yellow Tail Wine:\n- Wyeliminuj: Wiek, skomplikowana terminologia\n- Zredukuj: Cena, marketing\n- Podnieś: Łatwość picia, zabawa\n- Stwórz: Branding przygoda/lifestyle"
      },
      {
        "type": "quiz",
        "question": "Do czego dąży Strategia Błękitnego Oceanu?",
        "options": [
          "Pokonać konkurentów ich metodami",
          "Stworzyć niekwestionowaną przestrzeń rynkową",
          "Obniżyć ceny dla zdobycia udziału",
          "Kopiować udanych konkurentów"
        ],
        "correctAnswer": 1,
        "explanation": "Strategia Błękitnego Oceanu tworzy nową niekwestionowaną przestrzeń rynkową, czyniąc konkurencję nieistotną."
      }
    ]
  } $$
);

-- 8. Canvas Modelu Biznesowego
INSERT INTO engrams (id, title, category, description, xp_reward, estimated_minutes, stat_category, stat_points, prerequisites, content_json)
VALUES (
  'e3000000-0000-0000-0000-000000000002',
  'Canvas Modelu Biznesowego',
  'Strategy',
  'Projektuj i analizuj modele biznesowe',
  60,
  10,
  'Strategy',
  20,
  '[]'::jsonb,
  $$ {
    "slides": [
      {
        "type": "intro",
        "title": "Canvas Modelu Biznesowego",
        "content": "Framework 9 bloków do projektowania modeli biznesowych."
      },
      {
        "type": "content",
        "title": "9 Bloków Budujących",
        "content": "**Prawa Strona (Wartość):**\n1. Segmenty Klientów\n2. Propozycje Wartości\n3. Kanały\n4. Relacje z Klientami\n5. Strumienie Przychodów\n\n**Lewa Strona (Infrastruktura):**\n6. Kluczowe Zasoby\n7. Kluczowe Aktywności\n8. Kluczowi Partnerzy\n9. Struktura Kosztów"
      },
      {
        "type": "content",
        "title": "Jak Używać",
        "content": "**1. Zacznij od Segmentów Klientów** - Kogo obsługujemy?\n**2. Zdefiniuj Propozycje Wartości** - Jaki problem rozwiązujemy?\n**3. Zaprojektuj Kanały** - Jak do nich docieramy?\n**4. Zmapuj Strumienie Przychodów** - Jak zarabiamy?\n**5. Zidentyfikuj Kluczowe Zasoby** - Czego potrzebujemy?\n**6. Oblicz Koszty** - Ile to kosztuje?\n\nTest: Przychody > Koszty?"
      },
      {
        "type": "quiz",
        "question": "Od czego zaczynamy projektując BMC?",
        "options": [
          "Strumienie Przychodów",
          "Kluczowe Zasoby",
          "Segmenty Klientów",
          "Struktura Kosztów"
        ],
        "correctAnswer": 2,
        "explanation": "Zawsze zaczynamy od Segmentów Klientów - zrozumienie kogo obsługujemy napędza wszystkie inne decyzje."
      }
    ]
  } $$
);

-- ========================================
-- KATEGORIA MINDSET (2 engramy)
-- ========================================

-- 9. Fundamenty Growth Mindset
INSERT INTO engrams (id, title, category, description, xp_reward, estimated_minutes, stat_category, stat_points, prerequisites, content_json)
VALUES (
  'e4000000-0000-0000-0000-000000000001',
  'Fundamenty Growth Mindset',
  'Mindset',
  'Rozwijaj nastawienie ciągłego wzrostu',
  50,
  6,
  'Mindset',
  15,
  '[]'::jsonb,
  $$ {
    "slides": [
      {
        "type": "intro",
        "title": "Growth Mindset",
        "content": "Twoje nastawienie determinuje sukces bardziej niż talent."
      },
      {
        "type": "content",
        "title": "Fixed vs Growth Mindset",
        "content": "**Fixed Mindset (Stałe):**\n- 'Albo potrafię, albo nie'\n- Unika wyzwań\n- Łatwo się poddaje\n- Widzi feedback jako krytykę\n\n**Growth Mindset (Wzrostu):**\n- 'Mogę nauczyć się wszystkiego dzięki wysiłkowi'\n- Przyjmuje wyzwania\n- Wytrwa mimo niepowodzeń\n- Widzi feedback jako lekcję"
      },
      {
        "type": "content",
        "title": "Moc Słowa 'Jeszcze'",
        "content": "**Fixed:** 'Nie potrafię tego'\n**Growth:** 'Nie potrafię tego **jeszcze**'\n\nNeuronauka: Twój mózg jest jak mięsień - rośnie z wyzwaniami.\n\nBadanie: Uczniowie chwaleni za wysiłek przewyższyli o 30% tych chwalonych za inteligencję."
      },
      {
        "type": "quiz",
        "question": "Co charakteryzuje growth mindset?",
        "options": [
          "Wiara, że talent jest stały",
          "Unikanie trudnych wyzwań",
          "Widzenie wysiłku jako drogi do mistrzostwa",
          "Poddawanie się gdy jest ciężko"
        ],
        "correctAnswer": 2,
        "explanation": "Growth mindset widzi wysiłek i praktykę jako drogę do mistrzostwa, nie wrodzony talent."
      }
    ]
  } $$
);

-- 10. Budowanie Resilience
INSERT INTO engrams (id, title, category, description, xp_reward, estimated_minutes, stat_category, stat_points, prerequisites, content_json)
VALUES (
  'e4000000-0000-0000-0000-000000000002',
  'Budowanie Resilience',
  'Mindset',
  'Wracaj silniejszy po niepowodzeniach',
  50,
  7,
  'Mindset',
  15,
  '["e4000000-0000-0000-0000-000000000001"]'::jsonb,
  $$ {
    "slides": [
      {
        "type": "intro",
        "title": "Budowanie Resilience",
        "content": "Resilience to nie unikanie porażek - to szybkie wracanie do formy."
      },
      {
        "type": "content",
        "title": "3 Filary Resilience",
        "content": "**1. Challenge (Wyzwanie)** - Widzieć problemy jako szanse\n**2. Control (Kontrola)** - Skupić się na tym, co możesz zmienić\n**3. Commitment (Zaangażowanie)** - Pozostać zaangażowanym mimo trudności\n\nResilience = Przeciwności × Reakcja\n\nNie kontrolujesz przeciwności, ale kontrolujesz swoją reakcję."
      },
      {
        "type": "content",
        "title": "Cykl Resilience",
        "content": "**1. Acknowledge (Uznaj)** - Zaakceptuj co się stało\n**2. Analyze (Analizuj)** - Czego mogę się nauczyć?\n**3. Action (Działaj)** - Jaki jest mój następny krok?\n**4. Adjust (Dostosuj)** - Adaptuj bazując na feedbacku\n\nPrzykład: Nieudany launch produktu\n- Acknowledge: Nie zadziałało\n- Analyze: Zły market fit\n- Action: Pivot do nowego segmentu\n- Adjust: Podejście test-and-learn"
      },
      {
        "type": "quiz",
        "question": "Jaki jest klucz do resilience?",
        "options": [
          "Unikanie wszystkich porażek",
          "Nigdy nie przyznawanie się do błędów",
          "Kontrolowanie reakcji na przeciwności",
          "Bycie naturalnie 'twardym'"
        ],
        "correctAnswer": 2,
        "explanation": "Resilience polega na kontrolowaniu reakcji na przeciwności - nie kontrolujesz co się dzieje, ale kontrolujesz jak reagujesz."
      }
    ]
  } $$
);
