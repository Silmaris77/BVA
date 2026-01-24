-- Migration: 019_update_drill_types_and_seed.sql
-- Description: Update drill_type constraint and seed initial drill content
-- Author: BrainVenture V3

-- 1. Update drill_type constraint
ALTER TABLE drills DROP CONSTRAINT IF EXISTS drills_drill_type_check;
ALTER TABLE drills ADD CONSTRAINT drills_drill_type_check 
  CHECK (drill_type IN ('speed_run', 'analysis', 'quiz', 'scenario', 'daily'));

-- 2. Seed Data
-- Clear existing drills to avoid duplicates/conflicts during development
TRUNCATE TABLE drills CASCADE;

-- Insert Drill 1: Zbijanie Obiekcji (Speed Run)
INSERT INTO drills (drill_id, title, description, drill_type, time_limit_seconds, max_xp, questions)
VALUES (
  'drill_objection_001',
  'Zbijanie Obiekcji: Cena',
  '10 losowych obiekcji cenowych. Masz 15 sekund na każdą. Trenuj automatyzmy językowe.',
  'speed_run',
  120,
  50,
  '[
    {
      "id": "q1",
      "question": "To za drogo. Konkurencja ma to samo za połowę ceny.",
      "options": [
        "Rozumiem, że cena jest ważna. Czy poza ceną coś jeszcze Pana powstrzymuje?",
        "To niemożliwe, nasz produkt jest lepszy.",
        "Proszę sprawdzić dokładnie co oni oferują."
      ],
      "correctIndex": 0,
      "feedback": "Świetnie! Parafraza i sprawdzenie intencji (izolacja obiekcji) to najlepszy pierwszy krok."
    },
    {
      "id": "q2",
      "question": "Nie mam teraz budżetu.",
      "options": [
        "Szkoda, to zadzwońmy w przyszłym roku.",
        "A kiedy będzie Pan miał budżet?",
        "Rozumiem. A gdybyśmy rozłożyli to na raty lub przesunęli płatność, czy rozwiązanie by Państwa interesowało?"
      ],
      "correctIndex": 2,
      "feedback": "Dokładnie! Szukaj rozwiązań finansowania, zamiast rezygnować."
    },
    {
      "id": "q3",
      "question": "Muszę to przemyśleć.",
      "options": [
        "Jasne, ile czasu Pan potrzebuje?",
        "Co konkretnie budzi Pana wątpliwości? Może wyjaśnimy to teraz, żeby zaoszczędzić czas?",
        "Dobrze, zadzwonię jutro."
      ],
      "correctIndex": 1,
      "feedback": "Bardzo dobrze. \"Muszę przemyśleć\" to często zasłona dymna. Dopytaj o konkrety."
    }
  ]'::jsonb
);

-- Insert Drill 2: Typologia Klienta (Analysis)
INSERT INTO drills (drill_id, title, description, drill_type, time_limit_seconds, max_xp, questions)
VALUES (
  'drill_disc_001',
  'Typologia Klienta: Analiza',
  'Przeczytaj wypowiedź i przyporządkuj styl komunikacji klienta (D/I/S/C).',
  'analysis',
  180,
  30,
  '[
    {
      "id": "q1",
      "question": "Słuchaj, potrzebuję tego na wczoraj! Nie interesują mnie detale, ma działać i przynieść zysk. Ile to kosztuje i kiedy wdrożycie?",
      "options": ["Styl D (Dominujący)", "Styl I (Inspirujący)", "Styl S (Stały)", "Styl C (Sumienny)"],
      "correctIndex": 0,
      "feedback": "Tak! Krótko, na temat, orientacja na cel i wynik. To typowy styl D."
    },
    {
      "id": "q2",
      "question": "Czy możemy przeanalizować te dane jeszcze raz? Chciałbym zobaczyć tabelę porównawczą i specyfikację techniczną przed podjęciem decyzji.",
      "options": ["Styl D (Dominujący)", "Styl I (Inspirujący)", "Styl S (Stały)", "Styl C (Sumienny)"],
      "correctIndex": 3,
      "feedback": "Brawo. Dbałość o szczegóły, dane i fakty to domena stylu C."
    },
    {
      "id": "q3",
      "question": "Ważne jest dla mnie, żeby mój zespół czuł się z tym komfortowo. Nie chcę wprowadzać nerwowej atmosfery zmianami.",
      "options": ["Styl D", "Styl I", "Styl S", "Styl C"],
      "correctIndex": 2,
      "feedback": "Zgadza się. Troska o ludzi, stabilność i bezpieczeństwo to cechy stylu S."
    }
  ]'::jsonb
);

-- Insert Drill 3: Aktywne Słuchanie (Daily)
INSERT INTO drills (drill_id, title, description, drill_type, time_limit_seconds, max_xp, questions)
VALUES (
  'drill_daily_001',
  'Aktywne Słuchanie',
  'Parafrazuj wypowiedzi klienta. Wybierz najlepszą opcję.',
  'daily',
  60,
  20,
  '[
    {
      "id": "q1",
      "question": "Klient: \"Jestem zmęczony tym, że dostawy ciągle się spóźniają. To paraliżuje moją produkcję!\"",
      "options": [
        "Spokojnie, naprawimy to.",
        "To nie nasza wina, korki są.",
        "Rozumiem, że opóźnienia dostaw są dla Pana frustrujące, bo wstrzymują linię produkcyjną?"
      ],
      "correctIndex": 2,
      "feedback": "Perfekcyjna parafraza emocjonalno-treściowa (Empatia + Fakt)."
    }
  ]'::jsonb
);
