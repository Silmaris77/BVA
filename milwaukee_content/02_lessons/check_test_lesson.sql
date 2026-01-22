-- Check what's actually in the database for the test lesson
SELECT 
    lesson_id,
    title,
    content->'cards'->0 as first_card,
    content->'cards'->1 as second_card
FROM lessons
WHERE lesson_id = 'project-zero-test';
