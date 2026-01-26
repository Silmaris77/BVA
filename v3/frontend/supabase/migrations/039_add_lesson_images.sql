-- Add cover images to existing lessons to give them a "Netflix" look

DO $$
DECLARE
    r RECORD;
    cards jsonb;
    new_cards jsonb;
    img_url text;
BEGIN
    FOR r IN SELECT * FROM lessons LOOP
        cards := r.content->'cards';
        
        -- Default image (abstract/tech)
        img_url := 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1600&q=80';

        -- Determine image based on content keywords
        IF r.title ILIKE '%Fundamenty%' OR r.title ILIKE '%DNA%' OR r.title ILIKE '%Milwaukee Story%' THEN
             -- Industrial/Red tools vibe
            img_url := 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&w=1600&q=80';
        ELSIF r.title ILIKE '%Sprzedaż%' OR r.category = 'Sprzedaż' OR r.title ILIKE '%Wizyta%' THEN
            -- Handshake / Business meeting
            img_url := 'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=1600&q=80';
        ELSIF r.title ILIKE '%Współpraca%' OR r.category = 'Współpraca' THEN
            -- Teamwork
            img_url := 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1600&q=80';
        ELSIF r.title ILIKE '%Application%' OR r.title ILIKE '%Krok%' THEN
             -- Construction site / Field work
            img_url := 'https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1600&q=80';
        END IF;

        -- Check if the first card is a cover card
        IF jsonb_array_length(cards) > 0 AND (cards->0->>'type') = 'cover' THEN
            -- Inject the image property into the first card
            new_cards := jsonb_set(cards, '{0,image}', to_jsonb(img_url));
            
            -- Update the lesson content
            UPDATE lessons 
            SET content = jsonb_set(content, '{cards}', new_cards)
            WHERE lesson_id = r.lesson_id;
            
            RAISE NOTICE 'Updated lesson % with image %', r.title, img_url;
        END IF;
    END LOOP;
END $$;
