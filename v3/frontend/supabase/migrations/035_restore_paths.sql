-- Insert "Milwaukee Associate" Learning Path
-- Corrected: lesson_sequence is JSONB, not TEXT[]
INSERT INTO learning_paths (
    path_slug,
    title,
    description,
    estimated_hours,
    total_xp_reward,
    difficulty,
    lesson_sequence
)
SELECT 
    'milwaukee-associate-track',
    'Milwaukee Associate (Track 1)',
    'Kompleksowy program wdrożeniowy dla każdego pracownika. Poznaj historię, wartości i standard sprzedaży Milwaukee.',
    20,
    2100,
    'beginner',
    (
        SELECT jsonb_agg(lesson_id ORDER BY display_order ASC)
        FROM lessons 
        WHERE track = 'associate' 
    )
WHERE NOT EXISTS (
    SELECT 1 FROM learning_paths WHERE path_slug = 'milwaukee-associate-track'
);
