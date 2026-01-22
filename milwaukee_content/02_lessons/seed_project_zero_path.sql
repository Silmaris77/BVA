-- =====================================================
-- PROJECT ZERO - Safety Training Path & Lesson
-- =====================================================
-- This script creates:
-- 1. Learning Path: "Project Zero - Safety Training"
-- 2. Lesson: "Przygotowanie do Pracy" (Work Preparation)
-- 3. Links the lesson to the path
-- =====================================================

-- STEP 1: Insert the lesson with content
INSERT INTO lessons (
    lesson_id,
    title,
    description,
    category,
    difficulty,
    duration_minutes,
    xp_reward,
    status,
    release_date,
    track,
    module,
    company_id,
    content
) VALUES (
    'project-zero-przygotowanie',
    'Project Zero: Przygotowanie do Pracy',
    'Naucz się, jak bezpiecznie przygotować się do pracy z narzędziami Milwaukee. Poznaj zasady oceny ryzyka, doboru PPE i sprawdzania sprzętu przed rozpoczęciem zadania.',
    'Safety & PPE',
    'beginner',
    25,
    100,
    'published',
    NOW(),
    'Project Zero',
    'Safety Fundamentals',
    (SELECT id FROM companies WHERE name = 'Milwaukee' LIMIT 1),
    '{
        "cards": [
            {
                "id": "hero-1",
                "type": "hero",
                "title": "PRZYGOTOWANIE DO PRACY",
                "subtitle": "MILWAUKEE | PROJECT ZERO",
                "tagline": "STAY SAFE. STAY PRODUCTIVE.",
                "icon": "⚠️",
                "theme": "safety",
                "sections": [
                    {
                        "title": "Dla kogo jest ta lekcja",
                        "content": "Ta lekcja została stworzona dla osób, które pracują narzędziami każdego dnia:",
                        "items": [
                            "🏗️ Budowa",
                            "🚗 Warsztat samochodowy",
                            "⚡ Elektryka",
                            "🚰 Hydraulika",
                            "🪵 Stolarnia",
                            "🛠️ Serwis / utrzymanie ruchu"
                        ]
                    },
                    {
                        "title": "Cel tej lekcji",
                        "content": "Po tej lekcji będziesz potrafił:",
                        "items": [
                            "pracować **szybciej**, bo bez chaosu i improwizacji",
                            "pracować **bezpieczniej**, bez niepotrzebnego ryzyka",
                            "unikać **przestojów, kontuzji i uszkodzeń sprzętu**"
                        ]
                    }
                ],
                "callout": {
                    "type": "critical",
                    "text": "Najwięcej wypadków nie wydarza się przy trudnej robocie. Wydarzają się przy tej, którą robimy „tylko na chwilę\"."
                }
            },
            {
                "id": "content-1",
                "type": "content",
                "icon": "🟥",
                "subtitle": "MILWAUKEE | PROJECT ZERO",
                "title": "ZERO ACCIDENTS. ZERO EMISSIONS. ZERO COMPROMISES.",
                "sections": [
                    {
                        "heading": "Czym jest Project Zero",
                        "type": "important",
                        "content": "**Project Zero** to globalna inicjatywa **Milwaukee Tools**, której celem jest **eliminowanie zagrożeń w miejscu pracy** — zanim doprowadzą do wypadku.",
                        "items": [
                            "edukacji i budowaniu świadomości",
                            "bezpieczniejszych, lepiej zaprojektowanych narzędziach",
                            "kulturze codziennych, właściwych nawyków"
                        ]
                    }
                ],
                "callout": {
                    "type": "highlight",
                    "text": "Bezpieczeństwo nie zaczyna się po wypadku. **Zaczyna się przed uruchomieniem narzędzia.**"
                }
            },
            {
                "id": "data-1",
                "type": "data",
                "icon": "🧠",
                "title": "CZY WIESZ, ŻE…",
                "subtitle": "Fakty, które robią różnicę",
                "stats": [
                    {
                        "value": "84%",
                        "label": "urazów na budowie ma miejsce, gdy pracownicy **nie noszą kasku ochronnego**"
                    },
                    {
                        "value": "1/3",
                        "label": "wypadków śmiertelnych w budownictwie powodują **spadające przedmioty**"
                    },
                    {
                        "value": "2,8 mln",
                        "label": "wypadków ma miejsce **każdego roku** w europejskim budownictwie"
                    }
                ],
                "callout": {
                    "type": "warning",
                    "text": "To nie są „ekstremalne sytuacje\". To **codzienne warunki pracy**."
                }
            },
            {
                "id": "lightbulb-1",
                "type": "lightbulb",
                "icon": "💡",
                "title": "JAK DZIAŁA TA LEKCJA",
                "content": "Każdy moduł odpowiada na 3 pytania:",
                "steps": [
                    {
                        "number": 1,
                        "title": "Co może pójść nie tak?"
                    },
                    {
                        "number": 2,
                        "title": "Jak to sprawdzić w 30 sekund?"
                    },
                    {
                        "number": 3,
                        "title": "Co zrobić, żeby robota była bezpieczna i szła sprawnie?"
                    }
                ]
            },
            {
                "id": "content-2",
                "type": "content",
                "icon": "🔍",
                "subtitle": "MODUŁ 1/9",
                "title": "ZATRZYMAJ SIĘ PRZED ROBOTĄ (OCENA RYZYKA)",
                "sections": [
                    {
                        "heading": "Dlaczego to ważne",
                        "type": "important",
                        "content": "Zanim odpalisz narzędzie, zatrzymaj się na chwilę. Nie po to, żeby tracić czas – tylko żeby nie stracić palców, zdrowia albo sprzętu."
                    },
                    {
                        "heading": "Co sprawdzasz (30 sekund)",
                        "content": "Zadaj sobie 4 pytania:",
                        "items": [
                            "**Co robię?** (cięcie, wiercenie, szlifowanie, skręcanie)",
                            "**Z czego?** (beton, stal, drewno, instalacja, auto)",
                            "**Co mnie może skrzywdzić?** pył, hałas, odrzut, wirujące części, prąd",
                            "**Kto jest obok mnie?**"
                        ]
                    },
                    {
                        "heading": "Typowe błędy",
                        "type": "warning",
                        "items": [
                            "❌ „Zawsze tak robię\"",
                            "❌ „To tylko jeden otwór\"",
                            "❌ „Zaraz skończę\""
                        ]
                    }
                ],
                "remember": {
                    "icon": "💡",
                    "text": "Jeśli się skaleczysz, robota i tak stanie. Lepiej stracić 30 sekund niż pół dnia albo zdrowie."
                }
            },
            {
                "id": "story-1",
                "type": "story",
                "icon": "⚠️",
                "badge": "📍 Przypadek z terenu",
                "title": "Cięcie betonu bez oceny ryzyka",
                "scenario": {
                    "heading": "Co się stało:",
                    "text": "Na budowie operator zaczyna ciąć beton szlifierką kątową bez wcześniejszego sprawdzenia strefy odrzutu oraz ustawienia osłon."
                },
                "consequences": [
                    "Pył trafia w oczy pomocnika stojącego obok",
                    "Przerwa w pracy, wizyta w szpitalu, potencjalne uszkodzenie wzroku"
                ],
                "lesson": {
                    "heading": "✅ Czego mogło zapobiec:",
                    "text": "**STOP–LOOK–ASSESS–ACT:** Gdyby wykonano ocenę ryzyka, strefa odrzutu zostałaby ograniczona, a pomocnik wiedziałby gdzie stać. Okulary ochronne + maska przeciwpyłowa = zero urazu."
                }
            },
            {
                "id": "content-3",
                "type": "content",
                "icon": "🛡️",
                "subtitle": "MODUŁ 2/9",
                "title": "OCHRONA OSOBISTA (PPE) – CO ZAKŁADAĆ I KIEDY",
                "sections": [
                    {
                        "heading": "Dlaczego to ważne",
                        "type": "important",
                        "content": "Okulary, rękawice czy maska to nie wstyd, tylko narzędzie pracy, tak samo jak wkrętarka."
                    },
                    {
                        "heading": "Minimum, które musisz dobrać do roboty",
                        "items": [
                            "**Oczy** – przy cięciu, wierceniu, szlifowaniu",
                            "**Słuch** – przy młotach, szlifierkach, pilarkach",
                            "**Ręce** – przy ostrych krawędziach, chemii, ciężkich elementach",
                            "**Oddech** – przy pyle, betonie, drewnie, rdzy",
                            "**Buty / kask** – gdy coś może spaść lub przygnieść"
                        ]
                    },
                    {
                        "heading": "Typowe błędy",
                        "type": "warning",
                        "items": [
                            "❌ Brak okularów „bo niewygodne\"",
                            "❌ Jedne rękawice do wszystkiego",
                            "❌ Brak ochrony słuchu „bo chwilę głośno\""
                        ]
                    }
                ],
                "remember": {
                    "icon": "💡",
                    "text": "PPE dobierasz do roboty, a nie do przyzwyczajeń."
                }
            },
            {
                "id": "quiz-1",
                "type": "quiz",
                "title": "🎯 Sprawdź się - Quiz (Moduły 1-2)",
                "subtitle": "Zaznacz poprawne odpowiedzi",
                "questions": [
                    {
                        "question": "Co to znaczy \"zatrzymać się przed robotą\"?",
                        "options": [
                            "Zrobić przerwę na kawę",
                            "Zadać sobie 4 pytania: co robię, z czego, co może skrzywdzić, kto obok",
                            "Przeczytać instrukcję narzędzia"
                        ],
                        "correctAnswer": 1
                    },
                    {
                        "question": "Kiedy zakładasz ochronę słuchu?",
                        "options": [
                            "Tylko przy pracy w hali produkcyjnej",
                            "Przy młotach, szlifierkach, pilarkach - nawet \"na chwilę\"",
                            "Gdy ktoś się skarży na hałas"
                        ],
                        "correctAnswer": 1
                    },
                    {
                        "question": "Co to znaczy \"PPE dobierasz do roboty\"?",
                        "options": [
                            "Zawsze te same rękawice i okulary",
                            "Każde zadanie wymaga odpowiedniego PPE - oczy, słuch, ręce, oddech dopasowane do zagrożenia",
                            "PPE tylko przy niebezpiecznych robotach"
                        ],
                        "correctAnswer": 1
                    }
                ]
            },
            {
                "id": "ending-1",
                "type": "ending",
                "icon": "✅",
                "title": "GRATULACJE!",
                "subtitle": "Ukończyłeś lekcję Project Zero: Przygotowanie do Pracy",
                "checklist": [
                    {
                        "icon": "✅",
                        "text": "Wiesz, jak zatrzymać się przed robotą i ocenić ryzyko w 30 sekund"
                    },
                    {
                        "icon": "✅",
                        "text": "Potrafisz dobrać właściwe PPE do zadania"
                    },
                    {
                        "icon": "✅",
                        "text": "Rozumiesz, dlaczego \"na chwilę\" to najniebezpieczniejsze podejście"
                    },
                    {
                        "icon": "✅",
                        "text": "Znasz statystyki i realne przypadki z terenu"
                    }
                ],
                "tagline": "ZERO ACCIDENTS. ZERO COMPROMISES.",
                "next_steps": {
                    "text": "Następna lekcja: **Bezpieczna Praca z Narzędziami Elektrycznymi**",
                    "available": false
                }
            }
        ]
    }'::jsonb
)
ON CONFLICT (lesson_id) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    content = EXCLUDED.content,
    duration_minutes = EXCLUDED.duration_minutes,
    xp_reward = EXCLUDED.xp_reward,
    status = EXCLUDED.status,
    track = EXCLUDED.track,
    module = EXCLUDED.module,
    updated_at = NOW();

-- STEP 2: Create the Project Zero learning path
INSERT INTO learning_paths (
    path_slug,
    title,
    description,
    difficulty,
    estimated_hours,
    total_xp_reward,
    company_id,
    target_roles,
    tags,
    lesson_sequence
) VALUES (
    'project-zero-safety',
    'Project Zero - Safety Training',
    'Kompleksowe szkolenie z bezpieczeństwa pracy Milwaukee. Naucz się, jak pracować bezpiecznie, efektywnie i zgodnie z najlepszymi praktykami branżowymi. Zero wypadków. Zero kompromisów.',
    'beginner',
    2.0,
    500,
    (SELECT id FROM companies WHERE name = 'Milwaukee' LIMIT 1),
    ARRAY['JSS', 'ASR', 'KAM', 'BDM', 'FME'],
    ARRAY['safety', 'ppe', 'project-zero', 'fundamentals'],
    jsonb_build_array(
        'project-zero-przygotowanie'
    )
)
ON CONFLICT (path_slug) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    lesson_sequence = EXCLUDED.lesson_sequence,
    estimated_hours = EXCLUDED.estimated_hours,
    total_xp_reward = EXCLUDED.total_xp_reward,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- STEP 3: Verification queries
SELECT 
    lesson_id,
    title,
    category,
    track,
    module,
    duration_minutes,
    xp_reward,
    status
FROM lessons
WHERE lesson_id = 'project-zero-przygotowanie';

SELECT 
    path_slug,
    title,
    difficulty,
    estimated_hours,
    total_xp_reward,
    jsonb_array_length(lesson_sequence) as lesson_count
FROM learning_paths
WHERE path_slug = 'project-zero-safety';

-- Success message
DO $$
BEGIN
    RAISE NOTICE '✅ Project Zero path and lesson created successfully!';
    RAISE NOTICE '📚 Lesson: "Przygotowanie do Pracy" with 10 cards';
    RAISE NOTICE '🎯 Path: "Project Zero - Safety Training"';
    RAISE NOTICE '⚡ Ready to view in frontend!';
END $$;
