-- Seed Script: Phase 1 Coming Soon Lessons
-- Purpose: Add all 21 Phase 1 lessons to roadmap with "coming_soon" status
-- Based on: curriculum_implementation_plan.md (3-Track System)
-- Run this AFTER: migration 014
-- UPDATED: Added idempotency (ON CONFLICT DO UPDATE)

-- Get Milwaukee company ID
DO $$
DECLARE
  milwaukee_company_id UUID;
BEGIN
  SELECT id INTO milwaukee_company_id FROM companies WHERE company_slug = 'milwaukee';
  
  -- ============================================
  -- MODULE 1: FOUNDATIONS (Lessons 1.2-1.6)
  -- ============================================
  
  -- Lesson 1.2: Portfolio Overview
  INSERT INTO lessons (
    title, lesson_id, description, category, duration_minutes, xp_reward,
    difficulty, module, track, status, display_order, release_date, company_id, content
  ) VALUES (
    'Portfolio Overview - Ekosystem M12/M18/MX FUEL',
    'lesson-1-2-portfolio-overview',
    'Poznaj 3 platformy Milwaukee (M12™ Compact, M18™ Versatile, MX FUEL™ Heavy Equipment) i zrozum filozofię ONE BATTERY SYSTEM. Dowiedz się kiedy używać której platformy i jak budować kompletne rozwiązania systemowe.',
    'Product Knowledge',
    25,
    100,
    'beginner',
    'Module 1: Foundations',
    'Foundation',
    'coming_soon',
    2,
    '2026-02-01',
    milwaukee_company_id,
    '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna. Zostaniesz powiadomiony gdy będzie gotowa."}]}'::jsonb
  )
  ON CONFLICT (lesson_id) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    company_id = EXCLUDED.company_id,
    status = EXCLUDED.status,
    release_date = EXCLUDED.release_date,
    content = EXCLUDED.content;

  -- Lesson 1.3: Application First Deep Dive
  INSERT INTO lessons (
    title, lesson_id, description, category, duration_minutes, xp_reward,
    difficulty, module, track, status, display_order, release_date, company_id, content
  ) VALUES (
    'Application First Deep Dive - 7 Kroków Canvas',
    'lesson-1-3-application-first',
    'Głębokie zanurzenie w filozofię Application First. Poznaj 7-stopniowy framework (Aplikacja → Problem → Konsekwencje → Rozwiązanie → Demo → Wartość → Next Steps) i naucz się zadawać właściwe pytania diagnostyczne zamiast recytować specyfikacje produktów.',
    'Sales Methodology',
    30,
    125,
    'intermediate',
    'Module 1: Foundations',
    'Foundation',
    'coming_soon',
    3,
    '2026-02-05',
    milwaukee_company_id,
    '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna. Zostaniesz powiadomiony gdy będzie gotowa."}]}'::jsonb
  )
  ON CONFLICT (lesson_id) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    company_id = EXCLUDED.company_id,
    status = EXCLUDED.status,
    release_date = EXCLUDED.release_date,
    content = EXCLUDED.content;

  -- Lesson 1.4: SYSTEM Milwaukee
  INSERT INTO lessons (
    title, lesson_id, description, category, duration_minutes, xp_reward,
    difficulty, module, track, status, display_order, release_date, company_id, content
  ) VALUES (
    'SYSTEM Milwaukee - 4 Elementy',
    'lesson-1-4-system-milwaukee',
    'Dlaczego sprzedajemy SYSTEM, nie produkt? Poznaj 4 elementy kompletnego rozwiązania: Narzędzie + Platforma (Battery) + Osprzęt (Bits/Blades) + Ochrona (PPE). Naucz się budować wartość przez system thinking.',
    'Product Knowledge',
    20,
    100,
    'beginner',
    'Module 1: Foundations',
    'Foundation',
    'coming_soon',
    4,
    '2026-02-10',
    milwaukee_company_id,
    '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna. Zostaniesz powiadomiony gdy będzie gotowa."}]}'::jsonb
  )
  ON CONFLICT (lesson_id) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    company_id = EXCLUDED.company_id,
    status = EXCLUDED.status,
    release_date = EXCLUDED.release_date,
    content = EXCLUDED.content;

  -- Lesson 1.5: Competition Landscape
  INSERT INTO lessons (
    title, lesson_id, description, category, duration_minutes, xp_reward,
    difficulty, module, track, status, display_order, release_date, company_id, content
  ) VALUES (
    'Competition Landscape & Positioning',
    'lesson-1-5-competition',
    'Obiektywna analiza konkurencji: Milwaukee vs DeWalt vs Makita vs Bosch. Poznaj Battle Cards, TCO comparison i kluczowe różnice pozycjonowania. Naucz się odpowiadać na "Ale DeWalt jest tańszy..." bez defensywności.',
    'Sales Skills',
    25,
    100,
    'intermediate',
    'Module 1: Foundations',
    'Foundation',
    'coming_soon',
    5,
    '2026-02-15',
    milwaukee_company_id,
    '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna. Zostaniesz powiadomiony gdy będzie gotowa."}]}'::jsonb
  )
  ON CONFLICT (lesson_id) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    company_id = EXCLUDED.company_id,
    status = EXCLUDED.status,
    release_date = EXCLUDED.release_date,
    content = EXCLUDED.content;

  -- Lesson 1.6: Brand Voice
  INSERT INTO lessons (
    title, lesson_id, description, category, duration_minutes, xp_reward,
    difficulty, module, track, status, display_order, release_date, company_id, content
  ) VALUES (
    'Brand Voice & Communication Standards',
    'lesson-1-6-brand-voice',
    'Jak komunikować się "Milwaukee way"? Poznaj tone of voice (confident, professional, obsessed with user), terminology standards, visual identity (Milwaukee Red™) i demo best practices. Jobsite language, NOT showroom language.',
    'Brand & Marketing',
    20,
    75,
    'beginner',
    'Module 1: Foundations',
    'Foundation',
    'coming_soon',
    6,
    '2026-02-20',
    milwaukee_company_id,
    '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna. Zostaniesz powiadomiony gdy będzie gotowa."}]}'::jsonb
  )
  ON CONFLICT (lesson_id) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    company_id = EXCLUDED.company_id,
    status = EXCLUDED.status,
    release_date = EXCLUDED.release_date,
    content = EXCLUDED.content;

  -- ============================================
  -- MODULE 2: STANDARD WIZYTY (8 lessons)
  -- ============================================

  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content) VALUES
  ('Przygotowanie do Wizyty', 'lesson-2-1-prep', 'CRM research, SMART goals i pre-visit checklist. Jak przygotować się do wizyty w 15 minut i zwiększyć szanse na sukces o 60%.', 'Sales Skills', 20, 75, 'beginner', 'Module 2: Standard Wizyty', 'Foundation', 'coming_soon', 7, '2026-02-25', milwaukee_company_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna."}]}'::jsonb)
  ON CONFLICT (lesson_id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description, status = EXCLUDED.status, release_date = EXCLUDED.release_date, content = EXCLUDED.content;
  
  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content) VALUES
  ('Otwarcie Wizyty & Building Rapport', 'lesson-2-2-opening', 'Pierwsze 2 minuty decydują o wszystkim. Intro, komunikacja celu wizyty i budowanie relacji bez sztuczności.', 'Sales Skills', 20, 75, 'beginner', 'Module 2: Standard Wizyty', 'Foundation', 'coming_soon', 8, '2026-03-01', milwaukee_company_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna."}]}'::jsonb)
  ON CONFLICT (lesson_id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description, status = EXCLUDED.status, release_date = EXCLUDED.release_date, content = EXCLUDED.content;
  
  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content) VALUES
  ('Discovery & Diagnoza - Zadawanie Pytań', 'lesson-2-3-discovery', 'Pytania otwarte, aktywne słuchanie i reguła 80/20. Question bank + parafrazowanie. To najważniejsza umiejętność sprzedażowa.', 'Sales Skills', 25, 100, 'intermediate', 'Module 2: Standard Wizyty', 'Foundation', 'coming_soon', 9, '2026-03-05', milwaukee_company_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna."}]}'::jsonb)
  ON CONFLICT (lesson_id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description, status = EXCLUDED.status, release_date = EXCLUDED.release_date, content = EXCLUDED.content;
  
  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content) VALUES
  ('Prowadzenie Rozmowy - Struktura', 'lesson-2-4-structure', 'Full conversation flow: Cel → Diagnoza → Rekomendacja → Domknięcie. Jak nie zgubić się w chaotycznej rozmowie.', 'Sales Skills', 25, 100, 'intermediate', 'Module 2: Standard Wizyty', 'Foundation', 'coming_soon', 10, '2026-03-10', milwaukee_company_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna."}]}'::jsonb)
  ON CONFLICT (lesson_id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description, status = EXCLUDED.status, release_date = EXCLUDED.release_date, content = EXCLUDED.content;
  
  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content) VALUES
  ('Presentation Skills - Jak Prezentować', 'lesson-2-5-presentation', 'Features → Benefits transformation. FAB technique, storytelling i visual aids. Klient kupuje wartość, nie specyfikacje.', 'Sales Skills', 20, 75, 'beginner', 'Module 2: Standard Wizyty', 'Foundation', 'coming_soon', 11, '2026-03-15', milwaukee_company_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna."}]}'::jsonb)
  ON CONFLICT (lesson_id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description, status = EXCLUDED.status, release_date = EXCLUDED.release_date, content = EXCLUDED.content;
  
  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content) VALUES
  ('Handling Objections', 'lesson-2-6-objections', 'Top 10 obiekcji + gotowe response scripts. Feel-Felt-Found technique i overcoming resistance bez agresji.', 'Sales Skills', 25, 100, 'intermediate', 'Module 2: Standard Wizyty', 'Foundation', 'coming_soon', 12, '2026-03-20', milwaukee_company_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna."}]}'::jsonb)
  ON CONFLICT (lesson_id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description, status = EXCLUDED.status, release_date = EXCLUDED.release_date, content = EXCLUDED.content;
  
  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content) VALUES
  ('Closing & Next Steps', 'lesson-2-7-closing', 'KTO-CO-KIEDY formula. Closing techniques, follow-up rules i kontraktowanie bez presji. Domykanie ≠ manipulacja.', 'Sales Skills', 25, 100, 'intermediate', 'Module 2: Standard Wizyty', 'Foundation', 'coming_soon', 13, '2026-03-25', milwaukee_company_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna."}]}'::jsonb)
  ON CONFLICT (lesson_id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description, status = EXCLUDED.status, release_date = EXCLUDED.release_date, content = EXCLUDED.content;
  
  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content) VALUES
  ('Follow-Up & CRM Documentation', 'lesson-2-8-followup', '≤24h rule, email templates i what to log in CRM. 80% sprzedaży dzieje się w follow-up, nie w pierwszej wizycie.', 'Sales Skills', 20, 75, 'beginner', 'Module 2: Standard Wizyty', 'Foundation', 'coming_soon', 14, '2026-03-30', milwaukee_company_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna."}]}'::jsonb)
  ON CONFLICT (lesson_id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description, status = EXCLUDED.status, release_date = EXCLUDED.release_date, content = EXCLUDED.content;

  -- ============================================
  -- MODULE 3: APPLICATION FIRST CANVAS (7 lessons)
  -- ============================================

  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content) VALUES
  ('KROK 1 - Aplikacja (Job to be Done)', 'lesson-3-1-application', 'Obserwacja i mapowanie pracy klienta. Jak zbierać parametry aplikacji bez narzucania rozwiązań.', 'Sales Methodology', 25, 100, 'intermediate', 'Module 3: Application First Canvas', 'Foundation', 'coming_soon', 15, '2026-04-05', milwaukee_company_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna."}]}'::jsonb)
  ON CONFLICT (lesson_id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description, status = EXCLUDED.status, release_date = EXCLUDED.release_date, content = EXCLUDED.content;
  
  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content) VALUES
  ('KROK 2 - Problem (Pain Points)', 'lesson-3-2-problem', 'Klient sam nazywa ból. Pytania pogłębiające i parafrazowanie. Problem ≠ brak produktu.', 'Sales Methodology', 25, 100, 'intermediate', 'Module 3: Application First Canvas', 'Foundation', 'coming_soon', 16, '2026-04-10', milwaukee_company_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna."}]}'::jsonb)
  ON CONFLICT (lesson_id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description, status = EXCLUDED.status, release_date = EXCLUDED.release_date, content = EXCLUDED.content;
  
  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content) VALUES
  ('KROK 3 - Konsekwencje (Impact)', 'lesson-3-3-consequences', 'Klient liczy straty sam. Kwantyfikacja problemu (czas, pieniądze, bezpieczeństwo). Value selling starts here.', 'Sales Methodology', 25, 100, 'intermediate', 'Module 3: Application First Canvas', 'Foundation', 'coming_soon', 17, '2026-04-15', milwaukee_company_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna."}]}'::jsonb)
  ON CONFLICT (lesson_id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description, status = EXCLUDED.status, release_date = EXCLUDED.release_date, content = EXCLUDED.content;
  
  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content) VALUES
  ('KROK 4 - Rozwiązanie (SYSTEM)', 'lesson-3-4-solution', 'Dopasowanie 4-elementowego systemu do zdiagnozowanego bólu. Narzędzie + Platforma + Osprzęt + Ochrona.', 'Sales Methodology', 25, 100, 'intermediate', 'Module 3: Application First Canvas', 'Foundation', 'coming_soon', 18, '2026-04-20', milwaukee_company_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna."}]}'::jsonb)
  ON CONFLICT (lesson_id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description, status = EXCLUDED.status, release_date = EXCLUDED.release_date, content = EXCLUDED.content;
  
  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content) VALUES
  ('KROK 5 - Demo Aplikacyjne (Proof)', 'lesson-3-5-demo', 'Klient pracuje, JSS przewodzi. Demo checklist i success criteria. Hands-on experience = conviction.', 'Sales Methodology', 25, 100, 'intermediate', 'Module 3: Application First Canvas', 'Foundation', 'coming_soon', 19, '2026-04-25', milwaukee_company_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna."}]}'::jsonb)
  ON CONFLICT (lesson_id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description, status = EXCLUDED.status, release_date = EXCLUDED.release_date, content = EXCLUDED.content;
  
  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content) VALUES
  ('KROK 6 - Wartość (Value)', 'lesson-3-6-value', 'Klient sam opisuje wartość którą dostaje. Value articulation techniques. Nie TY sprzedajesz, klient kupuje.', 'Sales Methodology', 25, 100, 'intermediate', 'Module 3: Application First Canvas', 'Foundation', 'coming_soon', 20, '2026-04-30', milwaukee_company_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna."}]}'::jsonb)
  ON CONFLICT (lesson_id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description, status = EXCLUDED.status, release_date = EXCLUDED.release_date, content = EXCLUDED.content;
  
  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content) VALUES
  ('KROK 7 - Next Steps (Domknięcie)', 'lesson-3-7-next-steps', 'KTO-CO-KIEDY + follow-up ≤24h. Kontraktowanie, closing simulation i follow-up templates.', 'Sales Methodology', 25, 100, 'intermediate', 'Module 3: Application First Canvas', 'Foundation', 'coming_soon', 21, '2026-05-05', milwaukee_company_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie wkrótce dostępna."}]}'::jsonb)
  ON CONFLICT (lesson_id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description, status = EXCLUDED.status, release_date = EXCLUDED.release_date, content = EXCLUDED.content;

END $$;

-- ============================================
-- VERIFICATION
-- ============================================

-- Count coming_soon lessons
SELECT 
  status,
  COUNT(*) as lesson_count,
  SUM(duration_minutes) as total_minutes
FROM lessons
GROUP BY status
ORDER BY status;

-- Show roadmap by module
SELECT 
  module,
  COUNT(*) as lessons,
  STRING_AGG(title, ' | ' ORDER BY display_order) as lesson_titles
FROM lessons
WHERE status IN ('published', 'coming_soon')
GROUP BY module
ORDER BY MIN(display_order);

-- Timeline view
SELECT 
  display_order,
  title,
  status,
  release_date,
  duration_minutes,
  xp_reward
FROM lessons
WHERE company_id = (SELECT id FROM companies WHERE company_slug = 'milwaukee')
ORDER BY display_order;
