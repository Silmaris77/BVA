DO $$
DECLARE
    lesson_id_val TEXT;
    current_cards jsonb;
    final_cards jsonb := '[]'::jsonb;
    card_item jsonb;
BEGIN
    -- 1. Find the lesson
    SELECT lesson_id, content->'cards' INTO lesson_id_val, current_cards
    FROM lessons 
    WHERE title = 'Historia i DNA marki Milwaukee – Nothing but HEAVY DUTY™'
    LIMIT 1;

    IF lesson_id_val IS NOT NULL THEN
        -- 2. Loop through existing cards
        FOR card_item IN SELECT * FROM jsonb_array_elements(current_cards)
        LOOP
            -- Skip the 'Ewolucja Narzędzi' card if it still exists (double check cleanup)
            IF card_item->>'title' = 'Ewolucja Narzędzi' THEN
                CONTINUE;
            END IF;

            -- If it's the COVER card, force update the image
            IF card_item->>'type' = 'cover' THEN
                 card_item := jsonb_set(
                    card_item,
                    '{image}',
                    '"/lessons/milwaukee/history/oldtimesnewtimes.png"'::jsonb
                 );
                 RAISE NOTICE 'Found COVER card. Updated image.';
            END IF;

            -- Append to final array
            final_cards := final_cards || card_item;
        END LOOP;

        -- 3. Update the lesson
        UPDATE lessons
        SET content = jsonb_set(content, '{cards}', final_cards)
        WHERE lesson_id = lesson_id_val;
        
        RAISE NOTICE 'Lesson updated successfully.';
    ELSE
        RAISE NOTICE 'Lesson not found.';
    END IF;
END $$;
