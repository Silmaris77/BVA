-- Cleanup script: Remove all math lessons before fresh import
-- Run this FIRST in Supabase SQL Editor before running insert_math_path.sql

-- Delete existing math lessons (this will cascade delete from learning_paths)
DELETE FROM lessons WHERE lesson_id IN (
    'math-g7-l1',
    'math-g7-l2', 
    'math-g7-l3',
    'math-g7-l4'
);

-- Delete the learning path
DELETE FROM learning_paths WHERE path_slug = 'math-grade-7';

-- Verify cleanup
SELECT COUNT(*) as remaining_math_lessons 
FROM lessons 
WHERE lesson_id LIKE 'math-g7%';
