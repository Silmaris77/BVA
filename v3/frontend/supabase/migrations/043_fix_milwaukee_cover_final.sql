DO $$
DECLARE
    lesson_id_val TEXT;
    current_content jsonb;
    new_cards jsonb;
BEGIN
    -- 1. Find the lesson Using ILIKE to avoid special character issues (TM)
    SELECT lesson_id, content INTO lesson_id_val, current_content
    FROM lessons 
    WHERE title ILIKE '%Historia%Milwaukee%HEAVY DUTY%'
    LIMIT 1;

    IF lesson_id_val IS NOT NULL THEN
        RAISE NOTICE 'Found lesson: %', lesson_id_val;

        -- 2. Construct new cards array
        -- We want to iterate and update the cover, and REMOVE the 'Ewolucja' card if present
        
        -- We can use a SQL-based transformation for simplicity and robustness
        SELECT jsonb_agg(
            CASE 
                -- Update Cover Image
                WHEN elem->>'type' = 'cover' THEN 
                    jsonb_set(elem, '{image}', '"/lessons/milwaukee/history/oldtimesnewtimes.png"'::jsonb)
                -- Keep other cards as is
                ELSE elem
            END
        )
        INTO new_cards
        FROM jsonb_array_elements(current_content->'cards') elem
        WHERE elem->>'title' IS DISTINCT FROM 'Ewolucja Narzędzi'; -- Filter out the duplicate

        -- 3. Update the lesson
        UPDATE lessons
        SET content = jsonb_set(content, '{cards}', new_cards)
        WHERE lesson_id = lesson_id_val;

        RAISE NOTICE 'Updated lesson content successfully.';
    ELSE
        RAISE NOTICE 'Lesson NOT FOUND with ILIKE search.';
    END IF;
END $$;
