-- ========================================
-- DIAGNOZA I NAPRAWA ŚCIEŻKI MATEMATYKI
-- ========================================

-- KROK 1: Sprawdź aktualny stan ścieżki
SELECT path_slug, title, lesson_sequence, total_xp_reward
FROM learning_paths
WHERE path_slug = 'math-grade-7';

-- KROK 2: Sprawdź ile lekcji jest w bazie
SELECT lesson_id, title, xp_reward, created_at
FROM lessons 
WHERE module_id = 'd290f1ee-6c54-4b01-90e6-d701748f0851'
ORDER BY lesson_id;

-- KROK 3: UPDATE - Odkomentowany i gotowy do wykonania!

UPDATE learning_paths
SET 
    lesson_sequence = '[
        {
            "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
            "type": "module",
            "title": "Matematyka: Liczby i Działania",
            "lessons": ["math-g7-l1", "math-g7-l2", "math-g7-l3", "math-g7-l4", "math-g7-l5", "math-g7-l6"]
        }
    ]'::jsonb,
    total_xp_reward = 680
WHERE path_slug = 'math-grade-7';

-- KROK 4: Weryfikacja po UPDATE
SELECT path_slug, 
       jsonb_array_length(lesson_sequence) as modules_count,
       lesson_sequence -> 0 -> 'lessons' as lessons_in_module,
       jsonb_array_length(lesson_sequence -> 0 -> 'lessons') as lessons_count
FROM learning_paths
WHERE path_slug = 'math-grade-7';

-- KROK 5: Pełna zawartość lesson_sequence (skopiuj cały JSON)
SELECT lesson_sequence 
FROM learning_paths 
WHERE path_slug = 'math-grade-7';

-- KROK 6: Sprawdź każdą lekcję osobno
SELECT 
    l.lesson_id,
    l.title,
    l.module_id,
    CASE 
        WHEN lp.lesson_sequence::text LIKE '%' || l.lesson_id || '%' 
        THEN '✅ W ŚCIEŻCE' 
        ELSE '❌ BRAK' 
    END as status
FROM lessons l
CROSS JOIN learning_paths lp
WHERE l.module_id = 'd290f1ee-6c54-4b01-90e6-d701748f0851'
  AND lp.path_slug = 'math-grade-7'
ORDER BY l.lesson_id;
