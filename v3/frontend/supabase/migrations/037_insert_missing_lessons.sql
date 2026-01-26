-- 1. Insert missing lessons for Module 4: Współpraca
-- Fixed: Explicit lesson_id AND content (jsonb)

DO $$
DECLARE
    module_id_collab UUID;
BEGIN
    SELECT id INTO module_id_collab FROM modules WHERE title LIKE 'Współpraca%' LIMIT 1;

    -- Lesson 4.1: JSS ↔ ASR
    INSERT INTO lessons (lesson_id, title, description, category, difficulty, duration_minutes, xp_reward, track, module_id, display_order, content)
    VALUES (
        gen_random_uuid(),
        'JSS ↔ ASR Collaboration',
        'Zasady współpracy między JSS (Job Site Solutions) a ASR (Account Sales Reps). Proces przekazywania leadów.',
        'Współpraca',
        'intermediate',
        30,
        75,
        'associate',
        module_id_collab,
        1,
        '{"cards": []}'::jsonb
    );

    -- Lesson 4.2: Sell-In ↔ Sell-Out
    INSERT INTO lessons (lesson_id, title, description, category, difficulty, duration_minutes, xp_reward, track, module_id, display_order, content)
    VALUES (
        gen_random_uuid(),
        'Sell-In ↔ Sell-Out Integration',
        'Zrozumienie pełnego procesu sprzedaży: od dystrybutora do użytkownika końcowego.',
        'Współpraca',
        'intermediate',
        45,
        75,
        'associate',
        module_id_collab,
        2,
        '{"cards": []}'::jsonb
    );

    -- Lesson 4.3 (Update existing)
    UPDATE lessons 
    SET display_order = 3 
    WHERE module_id = module_id_collab AND (title ILIKE '%Cross%' OR title ILIKE '%Expanding%');

    -- Lesson 4.4: Marketing
    INSERT INTO lessons (lesson_id, title, description, category, difficulty, duration_minutes, xp_reward, track, module_id, display_order, content)
    VALUES (
        gen_random_uuid(),
        'Współpraca z Marketingiem',
        'Jak korzystać z zasobów marketingowych, kampanii i wsparcia centrali.',
        'Współpraca',
        'beginner',
        20,
        50,
        'associate',
        module_id_collab,
        4,
        '{"cards": []}'::jsonb
    );

    -- Lesson 4.5: Aftersales
    INSERT INTO lessons (lesson_id, title, description, category, difficulty, duration_minutes, xp_reward, track, module_id, display_order, content)
    VALUES (
        gen_random_uuid(),
        'Współpraca z Aftersales (Serwis)',
        'Obsługa gwarancyjna, serwisowa i wsparcie posprzedażowe. Jak budować zaufanie przez serwis.',
        'Współpraca',
        'beginner',
        30,
        50,
        'associate',
        module_id_collab,
        5,
        '{"cards": []}'::jsonb
    );

END $$;

-- 2. Force correct Module Order
UPDATE modules SET display_order = 1 WHERE title ILIKE 'Milwaukee Foundations%';
UPDATE modules SET display_order = 2 WHERE title ILIKE 'Application First Canvas%';
UPDATE modules SET display_order = 3 WHERE title ILIKE 'Standard Wizyty%';
UPDATE modules SET display_order = 4 WHERE title ILIKE 'Współpraca%';

-- 3. Re-generate Path Sequence
UPDATE learning_paths
SET lesson_sequence = (
    SELECT jsonb_agg(l.lesson_id ORDER BY m.display_order ASC, l.display_order ASC)
    FROM lessons l
    LEFT JOIN modules m ON l.module_id = m.id
    WHERE l.track = 'associate'
)
WHERE path_slug = 'milwaukee-associate-track';
