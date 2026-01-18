-- Migration: 007_seed_learning_paths.sql
-- Description: Seed example learning paths
-- Author: BrainVenture V3
-- Date: 2026-01-18
-- Run this after migration 006 (lessons content seed)

-- ============================================
-- SEED LEARNING PATHS
-- ============================================

-- Path 1: Milwaukee PPE Sales Specialist
-- Comprehensive path for PPE product salespeople
INSERT INTO learning_paths (
  path_slug,
  title,
  description,
  estimated_hours,
  difficulty,
  total_xp_reward,
  lesson_sequence,
  requires_all_lessons,
  min_lessons_required
) VALUES (
  'milwaukee-ppe-sales',
  'Sprzedawca PPE Milwaukee',
  'Kompletna ścieżka dla specjalisty sprzedaży produktów PPE (Personal Protective Equipment). Naucz się technik sprzedaży doradczej i doboru produktów Milwaukee.',
  3,
  'beginner',
  300,
  '["lesson-1-torque-automotive", "lesson-2-consultative-selling"]'::jsonb,
  true,
  NULL
)
ON CONFLICT (path_slug) DO UPDATE SET
  title = EXCLUDED.title,
  description = EXCLUDED.description,
  lesson_sequence = EXCLUDED.lesson_sequence,
  total_xp_reward = EXCLUDED.total_xp_reward;

-- Path 2: Automotive Workshop Excellence
-- For salespeople serving automotive workshops
INSERT INTO learning_paths (
  path_slug,
  title,
  description,
  estimated_hours,
  difficulty,
  total_xp_reward,
  lesson_sequence,
  requires_all_lessons,
  min_lessons_required
) VALUES (
  'automotive-workshop',
  'Ekspert Warsztatów Samochodowych',
  'Ścieżka dla przedstawicieli obsługujących warsztaty samochodowe. Poznaj produkty i techniki sprzedaży dedykowane dla automotive.',
  2,
  'intermediate',
  150,
  '["lesson-1-torque-automotive"]'::jsonb,
  true,
  NULL
)
ON CONFLICT (path_slug) DO UPDATE SET
  title = EXCLUDED.title,
  description = EXCLUDED.description,
  lesson_sequence = EXCLUDED.lesson_sequence,
  total_xp_reward = EXCLUDED.total_xp_reward;

-- Path 3: Consultative Selling Mastery
-- For all salespeople - core selling skills
INSERT INTO learning_paths (
  path_slug,
  title,
  description,
  estimated_hours,
  difficulty,
  total_xp_reward,
  lesson_sequence,
  requires_all_lessons,
  min_lessons_required
) VALUES (
  'consultative-selling-mastery',
  'Mistrz Sprzedaży Doradczej',
  'Opanuj sztukę sprzedaży konsultacyjnej. Od SPIN Selling po zaawansowane techniki zadawania pytań.',
  2,
  'intermediate',
  150,
  '["lesson-2-consultative-selling"]'::jsonb,
  true,
  NULL
)
ON CONFLICT (path_slug) DO UPDATE SET
  title = EXCLUDED.title,
  description = EXCLUDED.description,
  lesson_sequence = EXCLUDED.lesson_sequence,
  total_xp_reward = EXCLUDED.total_xp_reward;

-- ============================================
-- VERIFICATION
-- ============================================

-- View inserted learning paths
SELECT 
  path_slug,
  title,
  difficulty,
  total_xp_reward,
  estimated_hours,
  jsonb_array_length(lesson_sequence) as lesson_count
FROM learning_paths
ORDER BY path_slug;

-- Expected result: 3 learning paths
-- - automotive-workshop (1 lesson)
-- - consultative-selling-mastery (1 lesson)
-- - milwaukee-ppe-sales (2 lessons)
