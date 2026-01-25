-- Cleanup script to remove OJT lessons that were seeded with incorrect data structures
-- Run this in the Supabase SQL Editor

DELETE FROM lessons 
WHERE title = 'Narzędzia Trenera OJT'
   OR title = 'Model Treningu OJT: 5 Kroków'
   OR title = 'Wprowadzenie do On-the-Job Training'
   OR title = 'Mentoring i Coaching'
   OR title LIKE '%OJT%';

-- Verify they are gone
SELECT id, title FROM lessons WHERE title LIKE '%OJT%';
