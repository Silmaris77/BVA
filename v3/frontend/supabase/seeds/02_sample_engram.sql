-- Sample Engram: Value Quantification Basics
-- Run this in Supabase SQL Editor to add a test engram

DELETE FROM engrams WHERE id = 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12';

INSERT INTO engrams (
    id,
    title,
    category,
    description,
    xp_reward,
    estimated_minutes,
    content_json
) VALUES (
    'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'Value Quantification Basics',
    'Milwaukee',
    'Learn the fundamentals of quantifying value in client conversations.',
    50,
    5,
    jsonb_build_object(
        'slides', jsonb_build_array(
            jsonb_build_object(
                'id', 1,
                'type', 'intro',
                'title', 'Value Quantification',
                'content', E'## Why Quantify Value?\n\nIn client conversations, **concrete numbers** beat vague promises every time.\n\n**Goal:** Learn to translate pain points into measurable business impact.'
            ),
            jsonb_build_object(
                'id', 2,
                'type', 'content',
                'title', 'The Formula',
                'content', E'## Value Quantification Formula\n\n**Pain Point** → **Frequency** → **Time Cost** → **Dollar Value**\n\n### Example:\n* Pain: "Batteries die during work"\n* Frequency: "3 times per week"\n* Time: "15 min waiting each time"\n* **Value:** 45 min/week = 3h/month = **1 workday lost**'
            ),
            jsonb_build_object(
                'id', 3,
                'type', 'quiz',
                'title', 'Quick Check',
                'question', 'Client says: "We waste time changing drill bits." What should you ask FIRST?',
                'options', jsonb_build_array(
                    'What drill bits do you use?',
                    'How often do you change bits per day?',
                    'Have you tried Milwaukee bits?',
                    'What''s your budget for new tools?'
                ),
                'correctAnswer', 1,
                'explanation', 'Always quantify FREQUENCY first. "How often?" helps you calculate total time/cost impact.'
            ),
            jsonb_build_object(
                'id', 4,
                'type', 'content',
                'title', 'Client-Led Discovery',
                'content', E'## Let Client Calculate\n\n❌ **Wrong:** "I calculate you lose $500/month"\n\n✅ **Right:** "How much does 15h of downtime cost you?"\n\n**Why?** When client SAM calculates, they **own** the decision!'
            ),
            jsonb_build_object(
                'id', 5,
                'type', 'summary',
                'title', 'Key Takeaways',
                'content', E'## Remember:\n\n* ✓ Quantify early (ask "how often?")\n* ✓ Let client do the math\n* ✓ Translate time → money\n* ✓ Use client''s own numbers in proposal\n\n**Next:** Practice this in your next 3 client calls!'
            )
        )
    )
);
