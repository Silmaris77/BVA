-- ========================================
-- DODAJ LEKCJĘ 7 DO ŚCIEŻKI MATEMATYKI
-- ========================================

-- KROK 1: Dodaj lekcję 7 do bazy (wykonaj insert_math_lesson7.sql najpierw!)

-- KROK 2: Zaktualizuj learning_paths aby zawierała 7 lekcji
UPDATE learning_paths
SET 
    lesson_sequence = '[
        {
            "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
            "type": "module",
            "title": "Matematyka: Liczby i Działania",
            "lessons": ["math-g7-l1", "math-g7-l2", "math-g7-l3", "math-g7-l4", "math-g7-l5", "math-g7-l6", "math-g7-l7"]
        }
    ]'::jsonb,
    total_xp_reward = 820
WHERE path_slug = 'math-grade-7';

-- KROK 3: Weryfikacja
SELECT 
    path_slug, 
    total_xp_reward,
    jsonb_array_length(lesson_sequence -> 0 -> 'lessons') as lessons_count,
    lesson_sequence -> 0 -> 'lessons' as lessons_list
FROM learning_paths
WHERE path_slug = 'math-grade-7';

-- KROK 4: Sprawdź wszystkie 7 lekcji
SELECT lesson_id, title, xp_reward, created_at
FROM lessons 
WHERE module_id = 'd290f1ee-6c54-4b01-90e6-d701748f0851'
ORDER BY lesson_id;

-- Oczekiwane wyniki:
-- lessons_count: 7
-- total_xp_reward: 820 (100+100+100+120+140+120+140)
-- Lekcje: l1-l7
