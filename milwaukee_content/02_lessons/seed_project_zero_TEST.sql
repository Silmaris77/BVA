-- =====================================================
-- PROJECT ZERO - SIMPLE TEST LESSON
-- =====================================================
-- Minimal lesson to test card rendering
-- =====================================================

-- Delete old lesson if exists
DELETE FROM lessons WHERE lesson_id = 'project-zero-test';

-- Delete old lesson if exists
DELETE FROM lessons WHERE lesson_id = 'project-zero-test';

-- Insert simple test lesson (without company_id for now)
INSERT INTO lessons (
    lesson_id,
    title,
    description,
    content,
    duration_minutes,
    xp_reward,
    status,
    module,
    track,
    tags
) VALUES (
    'project-zero-test',
    'Project Zero - Test',
    'Prosty test renderowania kart',
    '{
        "cards": [
            {
                "id": "hero-1",
                "type": "hero",
                "title": "TEST LEKCJI",
                "subtitle": "MILWAUKEE | PROJECT ZERO",
                "tagline": "STAY SAFE. STAY PRODUCTIVE.",
                "icon": "⚠️",
                "theme": "safety",
                "sections": [
                    {
                        "title": "Sekcja 1",
                        "content": "To jest treść pierwszej sekcji.",
                        "items": [
                            "Punkt pierwszy",
                            "Punkt drugi",
                            "Punkt trzeci"
                        ]
                    },
                    {
                        "title": "Sekcja 2",
                        "items": [
                            "Element A",
                            "Element B"
                        ]
                    }
                ],
                "callout": {
                    "type": "critical",
                    "text": "To jest ważne ostrzeżenie testowe."
                }
            },
            {
                "id": "content-1",
                "type": "content",
                "title": "Pierwsza Karta Treści",
                "sections": [
                    {
                        "title": "Dlaczego to ważne",
                        "content": "To jest przykładowa treść karty content."
                    },
                    {
                        "title": "Co należy wiedzieć",
                        "items": [
                            "Pierwsza rzecz do zapamiętania",
                            "Druga rzecz do zapamiętania",
                            "Trzecia rzecz do zapamiętania"
                        ]
                    }
                ],
                "remember": {
                    "title": "Zapamiętaj",
                    "items": [
                        "To jest kluczowa informacja numer 1",
                        "To jest kluczowa informacja numer 2"
                    ]
                }
            },
            {
                "id": "data-1",
                "type": "data",
                "title": "STATYSTYKI",
                "subtitle": "Dane testowe",
                "stats": [
                    {
                        "value": "100%",
                        "label": "skuteczności testów"
                    },
                    {
                        "value": "0",
                        "label": "błędów w renderowaniu"
                    }
                ]
            },
            {
                "id": "quiz-1",
                "type": "quiz",
                "title": "Mini Quiz",
                "subtitle": "Sprawdź swoją wiedzę",
                "questions": [
                    {
                        "question": "Czy ta lekcja działa?",
                        "options": [
                            "Tak",
                            "Nie",
                            "Nie wiem"
                        ],
                        "correctAnswer": 0
                    }
                ]
            },
            {
                "id": "ending-1",
                "type": "ending",
                "title": "GRATULACJE!",
                "subtitle": "Ukończyłeś test",
                "checklist": [
                    {
                        "icon": "✅",
                        "text": "Hero card działa"
                    },
                    {
                        "icon": "✅",
                        "text": "Content card działa"
                    },
                    {
                        "icon": "✅",
                        "text": "Data card działa"
                    },
                    {
                        "icon": "✅",
                        "text": "Quiz działa"
                    }
                ],
                "tagline": "TEST ZAKOŃCZONY SUKCESEM",
                "next_steps": {
                    "text": "Następna lekcja: Pełna wersja Project Zero",
                    "available": false
                }
            }
        ]
    }'::jsonb,
    15,
    50,
    'published',
    'safety_fundamentals',
    'foundation',
    ARRAY['safety', 'test']
);

-- Verification
SELECT 
    lesson_id,
    title,
    duration_minutes,
    xp_reward,
    jsonb_array_length(content->'cards') as card_count,
    status
FROM lessons
WHERE lesson_id = 'project-zero-test';

-- Success message
DO $$
BEGIN
    RAISE NOTICE '✅ Project Zero TEST lesson created!';
    RAISE NOTICE '📚 Total cards: 5 (hero, content, data, quiz, ending)';
    RAISE NOTICE '⏱️ Duration: 15 minutes';
    RAISE NOTICE '⚡ XP Reward: 50';
END $$;
