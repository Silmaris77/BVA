-- Skrypt: Przypisanie ścieżki Matematyka do firmy Szkoła i roli Uczeń
-- 1. Tworzy firmę 'Szkoła' (jeśli nie istnieje).
-- 2. Tworzy rolę 'Uczeń' (jeśli nie istnieje).
-- 3. Przypisuje lekcje i ścieżkę do tej firmy.

DO $$
DECLARE
    school_id UUID;
    student_role_id UUID;
BEGIN
    -- 1. Utwórz firmę 'Szkoła'
    INSERT INTO companies (company_slug, name, is_general_group, logo_url)
    VALUES ('szkola', 'Szkoła', false, 'https://cdn-icons-png.flaticon.com/512/167/167707.png')
    ON CONFLICT (company_slug) DO UPDATE SET name = EXCLUDED.name
    RETURNING id INTO school_id;

    -- 2. Utwórz rolę 'Uczeń'
    INSERT INTO user_roles (role_slug, display_name, description)
    VALUES ('student', 'Uczeń', 'Uczeń szkoły podstawowej/średniej')
    ON CONFLICT (role_slug) DO UPDATE SET display_name = EXCLUDED.display_name
    RETURNING id INTO student_role_id;

    -- 3. Przypisz lekcje matematyki do firmy 'Szkoła'
    -- (Dzięki temu tylko users z company_id = school_id będą je widzieć)
    UPDATE lessons 
    SET company_id = school_id 
    WHERE lesson_id IN ('math-g7-l1', 'math-g7-l2');

    -- 4. Przypisz ścieżkę do firmy 'Szkoła'
    UPDATE learning_paths
    SET company_id = school_id
    WHERE path_slug = 'math-grade-7';
    
    -- (Opcjonalnie) Możemy też przypisać moduły, jeśli tabela modules ma company_id
    -- W obecnej migracji modules nie miało company_id, ale warto sprawdzić w schema.
    -- Zakładamy, że modules są publiczne lub filtrowane przez lekcje.

    RAISE NOTICE 'Przypisano zawartość do firmy Szkoła (ID: %) i roli Uczeń (ID: %)', school_id, student_role_id;
END $$;
