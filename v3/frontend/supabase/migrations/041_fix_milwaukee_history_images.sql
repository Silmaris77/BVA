DO $$
DECLARE
    lesson_id_val TEXT;
    current_content jsonb;
    inputs jsonb;
    new_cards jsonb;
BEGIN
    -- 1. Find the lesson
    SELECT lesson_id, content INTO lesson_id_val, current_content
    FROM lessons 
    WHERE title = 'Historia i DNA marki Milwaukee – Nothing but HEAVY DUTY™'
    LIMIT 1;

    IF lesson_id_val IS NOT NULL THEN
        RAISE NOTICE 'Found lesson %', lesson_id_val;

        -- 2. Filter out the unwanted "extra" card (from previous attempt)
        -- We reconstruct the cards array excluding the specific title
        SELECT jsonb_agg(elem) INTO new_cards
        FROM jsonb_array_elements(current_content->'cards') elem
        WHERE elem->>'title' IS DISTINCT FROM 'Ewolucja Narzędzi';

        -- 3. Update the FIRST card (Cover) with the image
        -- We assume the first card (index 0) is the Cover. 
        -- We modify the first element of our NEW filtered array.
        IF jsonb_array_length(new_cards) > 0 THEN
             new_cards := jsonb_set(
                new_cards, 
                '{0,image}', 
                '"/lessons/milwaukee/history/oldtimesnewtimes.png"'::jsonb
             );
        END IF;

        -- 4. Update the lesson record
        UPDATE lessons
        SET content = jsonb_set(content, '{cards}', new_cards)
        WHERE lesson_id = lesson_id_val;

        RAISE NOTICE 'Successfully cleaned up cards and updated cover image.';
    ELSE
        RAISE NOTICE 'Lesson not found. Please check if the lesson title exactly matches.';
    END IF;
END $$;
