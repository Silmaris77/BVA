DO $$
DECLARE
    lesson_id_val TEXT;
    current_content jsonb;
    first_card_type text;
BEGIN
    -- Find the lesson
    SELECT lesson_id, content INTO lesson_id_val, current_content
    FROM lessons 
    WHERE title = 'Historia i DNA marki Milwaukee – Nothing but HEAVY DUTY™'
    LIMIT 1;

    IF lesson_id_val IS NOT NULL THEN
        -- Check if first card is cover
        first_card_type := current_content->'cards'->0->>'type';
        
        IF first_card_type = 'cover' THEN
            -- Update the image of the cover card
            UPDATE lessons
            SET content = jsonb_set(
                content,
                '{cards,0,image}',
                '"/lessons/milwaukee/history/oldtimesnewtimes.png"'::jsonb
            )
            WHERE lesson_id = lesson_id_val;
            
            RAISE NOTICE 'Updated cover image for lesson %', lesson_id_val;
        ELSE
            RAISE NOTICE 'First card is not a cover card (found %), skipping update', first_card_type;
        END IF;
    ELSE
        RAISE NOTICE 'Lesson not found';
    END IF;
END $$;
