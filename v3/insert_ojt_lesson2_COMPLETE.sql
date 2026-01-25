-- COMPLETE OJT Lesson 2 Implementation - ALL 29 Cards
-- "Model OJT - 5 Etapów treningu On-the-Job"
-- Execute this in Supabase SQL Editor after cleanup

-- CLEANUP (optional - remove old versions)
-- DELETE FROM lessons WHERE lesson_id LIKE 'ojt_lesson_2%';

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
    'Jak rozwijać pracowników bez odrywania ich od pracy?',
    'Poznaj 5-etapowy model On-the-Job Training, który w 3–4 miesiące zwiększa skuteczność zespołu o 20–50%, skraca czas rozwoju o połowę i realnie uwalnia czas menedżera.',
    'beginner',
    25,
    300,
    '{
      "cards": [
        {
          "id": 1,
          "type": "hero",
          "title": "Jak rozwijać pracowników bez odrywania ich od pracy?",
          "content": "Poznaj 5-etapowy model On-the-Job Training",
          "sections": [
            {"icon": "👥", "title": "Dla kogo", "content": "Menedżerowie, którzy chcą przestać gasić pożary i zbudować zespół, który działa samodzielnie, bez ciągłego angażowania ich czasu."},
            {"icon": "🎯", "title": "Cel", "content": "Poznać 5-etapowy model On-the-Job Training, który w 3–4 miesiące:", "list": ["zwiększa skuteczność zespołu o 20–50%,", "skraca czas rozwoju o połowę,", "realnie uwalnia czas menedżera."]},
            {"icon": "💡", "title": "Dlaczego to działa", "content": "70% kompetencji powstaje w praktyce. OJT to nauka w realnym biznesie + natychmiastowy feedback — 4× szybszy rozwój i trwała zmiana zachowań, nie teoria."}
          ],
          "estimated_seconds": 90,
          "xp_points": 10
        }
      ]
    }'::jsonb
);

-- NOTE: This is a TEMPLATE - you need to manually combine all cards from:
-- - insert_ojt_lesson2_full.sql (cards 1-5)
-- - insert_ojt_lesson2_cards_6_10.sql (cards 6-10)
-- - insert_ojt_lesson2_cards_11_15.sql (cards 11-15)
-- - insert_ojt_lesson2_cards_16_20.sql (cards 16-20)
-- - insert_ojt_lesson2_cards_21_29.sql (cards 21-29)
--
-- To create complete lesson:
-- 1. Copy card 1 from Part 1 (above)
-- 2. Add cards 2-5 from Part 1
-- 3. Add cards 6-10 from Part 2
-- 4. Add cards 11-15 from Part 3
-- 5. Add cards 16-20 from Part 4
-- 6. Add cards 21-29 from Part 5
-- 7. Close the cards array with ]
-- 8. Execute in Supabase

-- For easier merging, use a JSON editor or script to combine the arrays
