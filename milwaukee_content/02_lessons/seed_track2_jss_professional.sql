-- Script: Seed Track 2 JSS Professional
-- Purpose: Add "JSS Professional" track (Track 2) with lessons from Modules 4 & 5
-- Target Audience: JSS (Junior Sales Specialist)
-- Release: Q2 2026 (May-June)

DO $$
DECLARE
  milwaukee_id UUID;
  lesson_seq JSONB;
BEGIN
  -- 1. Get Milwaukee ID
  SELECT id INTO milwaukee_id FROM companies WHERE company_slug = 'milwaukee';
  
  IF milwaukee_id IS NULL THEN
    RAISE WARNING 'Milwaukee company not found!';
    RETURN;
  END IF;

  -- ============================================
  -- INSERT LESSONS (Track 2 Content)
  -- ============================================

  -- MODULE 4: JSS Account Management
  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content, target_roles) VALUES
  ('Terytorium i Segmentacja Klientów', 'lesson-4-1-jss-segmentation', 'Jak zarządzać swoim terenem? Segmentacja klientów A/B/C i planowanie tras (Route Optimization). Efektywne wykorzystanie czasu w terenie.', 'Account Management', 30, 150, 'intermediate', 'Module 4: Account Management', 'Professional', 'coming_soon', 30, '2026-05-15', milwaukee_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie dostępna w Q2 2026."}]}'::jsonb, ARRAY['JSS']),
  ('Budowanie Relacji Długofalowych', 'lesson-4-2-jss-relationships', 'Przejście od "transakcji" do "partnerstwa". Mapa decydentów u klienta i budowanie zaufania z kierownikami budów i zakupowcami.', 'Account Management', 25, 125, 'intermediate', 'Module 4: Account Management', 'Professional', 'coming_soon', 31, '2026-05-20', milwaukee_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie dostępna w Q2 2026."}]}'::jsonb, ARRAY['JSS']),
  ('Szkolenia dla Użytkowników Końcowych', 'lesson-4-5-jss-training', 'Jak prowadzić Toolbox Talks? Edukacja użytkowników jako narzędzie sprzedaży i lojalizacji. Safety first.', 'Sales Skills', 35, 175, 'intermediate', 'Module 4: Account Management', 'Professional', 'coming_soon', 32, '2026-05-25', milwaukee_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie dostępna w Q2 2026."}]}'::jsonb, ARRAY['JSS']),
  ('Expanding Wallet Share - Cross-selling', 'lesson-4-7-jss-expansion', 'Strategia "Land & Expand". Jak wejść z jednym narzędziem i przejąć cały warsztat? Analiza potencjału klienta.', 'Sales Skills', 30, 150, 'intermediate', 'Module 4: Account Management', 'Professional', 'coming_soon', 33, '2026-05-30', milwaukee_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie dostępna w Q2 2026."}]}'::jsonb, ARRAY['JSS'])
  ON CONFLICT (lesson_id) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    category = EXCLUDED.category,
    duration_minutes = EXCLUDED.duration_minutes,
    display_order = EXCLUDED.display_order,
    company_id = EXCLUDED.company_id,
    status = EXCLUDED.status,
    content = EXCLUDED.content,
    target_roles = EXCLUDED.target_roles,
    module = 'Module 4: Account Management',
    track = 'Professional';

  -- MODULE 5: Product Masterclass (JSS Focus)
  INSERT INTO lessons (title, lesson_id, description, category, duration_minutes, xp_reward, difficulty, module, track, status, display_order, release_date, company_id, content, target_roles) VALUES
  ('Masterclass: Drilling & Fastening', 'lesson-5-1-drilling', 'Zaawansowane techniki wiercenia i mocowania. M18 FUEL™ vs konkurencja. Dobór akcesoriów SHOCKWAVE™ dla maksymalnej wydajności.', 'Product Knowledge', 40, 200, 'advanced', 'Module 5: Product Deep Dives', 'Professional', 'coming_soon', 40, '2026-06-05', milwaukee_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie dostępna w Q2 2026."}]}'::jsonb, ARRAY['JSS', 'ASR']),
  ('Masterclass: Cutting & Sawing', 'lesson-5-2-cutting', 'Technologia SAWZALL™, HACKZALL™ i pilarek tarczowych. Ostrza TORCH™ i WRECKER™. Demonstracja szybkości i żywotności.', 'Product Knowledge', 40, 200, 'advanced', 'Module 5: Product Deep Dives', 'Professional', 'coming_soon', 41, '2026-06-10', milwaukee_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie dostępna w Q2 2026."}]}'::jsonb, ARRAY['JSS', 'ASR']),
  ('Masterclass: PACKOUT™ Modular Storage', 'lesson-5-4-packout', 'System przechowywania jako klucz do efektywności. Konfiguracja rozwiązań dla elektryków, hydraulików i stolarzy. Upselling through organization.', 'Product Knowledge', 30, 150, 'intermediate', 'Module 5: Product Deep Dives', 'Professional', 'coming_soon', 42, '2026-06-15', milwaukee_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie dostępna w Q2 2026."}]}'::jsonb, ARRAY['JSS', 'ASR']),
  ('Masterclass: MX FUEL™ Heavy Equipment', 'lesson-5-5-mxfuel', 'Rewolucja na placu budowy. Młoty wyburzeniowe, przecinarki i wiertnice diamentowe. ROI vs spalinowe odpowiedniki (Zero Emissions).', 'Product Knowledge', 45, 250, 'advanced', 'Module 5: Product Deep Dives', 'Professional', 'coming_soon', 43, '2026-06-20', milwaukee_id, '{"cards": [{"type": "intro", "title": "W przygotowaniu", "content": "Ta lekcja będzie dostępna w Q2 2026."}]}'::jsonb, ARRAY['JSS', 'ASR'])
  ON CONFLICT (lesson_id) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    category = EXCLUDED.category,
    duration_minutes = EXCLUDED.duration_minutes,
    display_order = EXCLUDED.display_order,
    company_id = EXCLUDED.company_id,
    status = EXCLUDED.status,
    content = EXCLUDED.content,
    target_roles = EXCLUDED.target_roles,
    module = 'Module 5: Product Deep Dives',
    track = 'Professional';

  -- ============================================
  -- CREATE LEARNING PATH: JSS PROFESSIONAL
  -- ============================================

  -- Construct sequence: All newly inserted lessons
  SELECT jsonb_agg(lesson_id ORDER BY display_order)
  INTO lesson_seq
  FROM lessons
  WHERE company_id = milwaukee_id
  AND track = 'Professional'
  AND 'JSS' = ANY(target_roles);

  -- Upsert Path
  INSERT INTO learning_paths (
    path_slug,
    company_id,
    title,
    description,
    estimated_hours,
    difficulty,
    total_xp_reward,
    lesson_sequence,
    requires_all_lessons,
    target_roles
  ) VALUES (
    'jss-professional-track',
    milwaukee_id,
    'JSS Professional: Territory & Product Mastery',
    'Ścieżka dla Specjalistów Sprzedaży (JSS). Opanuj zarządzanie terytorium, budowanie relacji oraz ekspercką wiedzę produktową z kluczowych kategorii (Drilling, Cutting, MX FUEL).',
    25,
    'intermediate',
    4000,
    lesson_seq,
    true,
    ARRAY['JSS']::text[]
  )
  ON CONFLICT (path_slug) DO UPDATE SET
    lesson_sequence = EXCLUDED.lesson_sequence,
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    total_xp_reward = EXCLUDED.total_xp_reward,
    updated_at = NOW();

END $$;
