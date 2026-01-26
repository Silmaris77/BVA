-- Re-generate the lesson_sequence for the Associate Track
-- This time, we order by the MODULE'S display_order first, then the LESSON'S display_order.
-- This ensures 'Application First' (Module 2) comes before 'Standard Wizyty' (Module 3).

UPDATE learning_paths
SET lesson_sequence = (
    SELECT jsonb_agg(l.lesson_id ORDER BY m.display_order ASC, l.display_order ASC)
    FROM lessons l
    LEFT JOIN modules m ON l.module_id = m.id
    WHERE l.track = 'associate'
)
WHERE path_slug = 'milwaukee-associate-track';

-- Verify tracks for Współpraca lessons (just in case they were missed/null)
UPDATE lessons
SET track = 'associate',
    module_id = (SELECT id FROM modules WHERE title ILIKE 'Współpraca%' LIMIT 1)
WHERE title ILIKE '%Współpraca%' 
   OR title ILIKE '%Cross-Sell%'
   OR title ILIKE '%JSS ↔ ASR%' 
   OR title ILIKE '%Sell-In ↔ Sell-Out%';
