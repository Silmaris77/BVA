-- Create Milwaukee Foundations Learning Path
-- Run this AFTER applying migration 012

-- Milwaukee Company ID: d73705b5-f27d-49f7-a516-63a1158cb75a

INSERT INTO learning_paths (
  path_slug,
  title,
  description,
  difficulty,
  estimated_hours,
  total_xp_reward,
  company_id,
  lesson_sequence,
  target_roles,
  requires_all_lessons,
  min_lessons_required
) VALUES (
  'milwaukee-foundations',
  'Milwaukee Foundations',
  'Fundamentalna wiedza dla każdego pracownika Milwaukee. Historia, wartości, filozofia Application First i podstawy systemów M12/M18/MX FUEL.',
  'beginner',
  20, -- estimated hours for full track
  2000, -- massive XP for completing path (certification)
  'd73705b5-f27d-49f7-a516-63a1158cb75a'::uuid,
  '["lesson-1-1-milwaukee-story"]'::jsonb, -- Currently only one lesson
  ARRAY['JSS', 'ASR', 'KAM', 'BDM', 'FME'],
  true,
  0
)
ON CONFLICT (path_slug) DO UPDATE SET
  title = EXCLUDED.title,
  description = EXCLUDED.description,
  lesson_sequence = EXCLUDED.lesson_sequence,
  company_id = EXCLUDED.company_id,
  target_roles = EXCLUDED.target_roles,
  updated_at = NOW();

-- Verify
SELECT * FROM learning_paths WHERE path_slug = 'milwaukee-foundations';
