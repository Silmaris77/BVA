-- Script: Update Learning Path Sequence
-- Purpose: Create/Update 'Foundation Track' for Milwaukee with all 21 lessons
-- Run this AFTER: seed_phase1_coming_soon.sql

DO $$
DECLARE
  milwaukee_id UUID;
  lesson_seq JSONB;
  lesson_count INTEGER;
BEGIN
  -- 1. Get Milwaukee ID
  SELECT id INTO milwaukee_id FROM companies WHERE company_slug = 'milwaukee';
  
  IF milwaukee_id IS NULL THEN
    RAISE NOTICE 'Milwaukee company not found!';
    RETURN;
  END IF;

  -- 2. Construct JSON array of lesson_ids ordered by display_order
  SELECT jsonb_agg(lesson_id ORDER BY display_order), COUNT(*)
  INTO lesson_seq, lesson_count
  FROM lessons
  WHERE company_id = milwaukee_id;
  
  RAISE NOTICE 'Found % lessons for Milwaukee path', lesson_count;

  -- 3. Upsert the Foundation Path
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
    'foundation-track-milwaukee',
    milwaukee_id,
    'Fundamenty Sprzedaży Milwaukee',
    'Kompletna ścieżka wdrożeniowa: Od historii marki, przez produkty, po techniki sprzedaży Application First. Zawiera moduły: Foundations, Standard Wizyty i Application First Canvas.',
    15, -- Estimated ~21 lessons * 45 mins
    'beginner',
    3000, -- Approx total XP
    lesson_seq,
    true,
    ARRAY['JSS', 'ASR', 'KAM', 'BDM', 'FME']::text[]
  )
  ON CONFLICT (path_slug) DO UPDATE SET
    lesson_sequence = EXCLUDED.lesson_sequence,
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    total_xp_reward = EXCLUDED.total_xp_reward,
    updated_at = NOW();

END $$;

-- Verify
SELECT 
  path_slug, 
  title, 
  jsonb_array_length(lesson_sequence) as lesson_count,
  company_id
FROM learning_paths 
WHERE path_slug = 'foundation-track-milwaukee';
