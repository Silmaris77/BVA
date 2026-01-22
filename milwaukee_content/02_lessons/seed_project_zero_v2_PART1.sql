-- =====================================================
-- PROJECT ZERO - FULL LESSON (Created from scratch)
-- =====================================================
-- Complete safety training lesson based on HTML mockup
-- All JSON uses correct structure: "title" not "heading"
-- Remember boxes use {title, items[]} structure
-- =====================================================

-- Delete old lessons
DELETE FROM lessons WHERE lesson_id IN ('project-zero-full', 'project-zero-test');

-- Insert complete Project Zero lesson
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
    'project-zero-full',
    'Project Zero - Przygotowanie do Pracy',
    'Kompleksowe szkolenie z bezpieczeństwa pracy według standardów Milwaukee Project Zero',
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
                        "title": "PRZYGOTOWANIE STANOWISKA",
                        "items": [
                            "Ocena ryzyka",
                            "Dobór narzędzi",
                            "Zabezpieczenie obszaru",
                            "Sprawdzenie oświetlenia",
                            "Usunięcie przeszkód",
                            "Oznakowanie strefy pracy"
                        ]
                    },
                    {
                        "title": "GOTOWOŚĆ",
                        "items": [
                            "Kompletne środki ochrony osobistej",
                            "Sprawne narzędzia i sprzęt",
                            "Znajomość procedur awaryjnych",
                            "Komunikacja z zespołem",
                            "Przygotowanie umysłowe i fizyczne",
                            "Dostęp do apteczki i gaśnicy"
                        ]
                    }
                ],
                "callout": {
                    "type": "critical",
                    "text": "Najlepszy sposób na uniknięcie wypadku? Przygotuj się zanim zaczniesz. Przemyślana organizacja stanowiska pracy to fundament każdego bezpiecznego projektu."
                }
            },
            {
                "id": "content-1",
                "type": "content",
                "title": "ZERO ACCIDENTS. ZERO EMISSIONS. ZERO DOWNTIME.",
                "sections": [
                    {
                        "title": "Filozofia Project Zero",
                        "content": "Project Zero to nie tylko zestaw zasad – to sposób myślenia. Milwaukee wierzy, że każdy wypadek można było zapobiec, każda emisja da się wyeliminować, a każda przerwa w pracy jest do uniknięcia."
                    },
                    {
                        "title": "Dlaczego to działa?",
                        "items": [
                            "Bo zaczyna się od świadomości",
                            "Bo angażuje cały zespół",
                            "Bo łączy bezpieczeństwo z wydajnością",
                            "Bo opiera się na danych i doświadczeniu",
                            "Bo stawia człowieka na pierwszym miejscu"
                        ]
                    }
                ],
                "remember": {
                    "title": "Zapamiętaj",
                    "items": [
                        "**Bezpieczeństwo nie jest opcją** – to podstawa każdej pracy",
                        "**Zero wypadków** to cel osiągalny przy odpowiednim przygotowaniu",
                        "**Twoja odpowiedzialność** zaczyna się przed pierwszym krokiem"
                    ]
                }
            },
            {
                "id": "lightbulb-1",
                "type": "lightbulb",
                "title": "JAK DZIAŁA TA LEKCJA",
                "content": "Każdy moduł odpowiada na 3 pytania:",
                "accent_color": "yellow",
                "steps": [
                    {
                        "number": 1,
                        "title": "CO MOŻE SIĘ STAĆ? (zagrożenia)"
                    },
                    {
                        "number": 2,
                        "title": "JAK TEGO UNIKNĄĆ? (procedury)"
                    },
                    {
                        "number": 3,
                        "title": "CO ROBIĆ W RAZIE PROBLEMU? (reakcja)"
                    }
                ],
                "insight": "Wiedza bez działania to tylko teoria. Działanie bez wiedzy to hazard."
            },
            {
                "id": "data-1",
                "type": "data",
                "title": "CZY WIESZ, ŻE...",
                "subtitle": "Fakty, które warto znać",
                "stats": [
                    {
                        "value": "84%",
                        "label": "wypadków można było uniknąć dzięki lepszemu przygotowaniu stanowiska"
                    },
                    {
                        "value": "1/3",
                        "label": "urazów dotyczy rąk – najczęściej używanej części ciała w pracy"
                    },
                    {
                        "value": "2,8 mln",
                        "label": "wypadków przy pracy rocznie w Europie (dane Eurostat)"
                    }
                ],
                "callout": {
                    "type": "info",
                    "text": "To nie są abstrakcyjne liczby. To prawdziwi ludzie, którzy mogli wrócić do domu bez urazu."
                }
            },
            {
                "id": "content-2",
                "type": "content",
                "title": "DLACZEGO POWSTAŁ PROJECT ZERO",
                "sections": [
                    {
                        "title": "Wypadkom można zapobiegać",
                        "content": "Większość wypadków nie jest wynikiem \"pecha\" czy \"złego dnia\". Są konsekwencją konkretnych zaniedbań: braku oceny ryzyka, niewłaściwych narzędzi, pośpiechu, zmęczenia lub braku komunikacji."
                    },
                    {
                        "title": "Cele Project Zero",
                        "content": "Zero. Nie \"mniej\". Nie \"lepiej niż w zeszłym roku\". **Zero wypadków, zero emisji, zero przestojów.** Ambitne? Tak. Możliwe? Zdecydowanie. Technologia, procedury i świadomość – to klucz."
                    },
                    {
                        "title": "Bezpieczeństwo bez kompromisów",
                        "content": "Milwaukee nie traktuje bezpieczeństwa jako \"dodatku\" do wydajności. To fundament. Gdy pracujesz bezpiecznie, pracujesz efektywniej. Gdy dbasz o zespół, zespół dba o wynik."
                    }
                ],
                "callout": {
                    "type": "warning",
                    "text": "Każdy wypadek to sygnał, że coś w systemie nie zadziałało. Każdy wypadek to lekcja – ale nie musi być Twoją."
                }
            }
        ]
    }'::jsonb,
    45,
    150,
    'published',
    'safety_fundamentals',
    'foundation',
    ARRAY['safety', 'project-zero', 'przygotowanie']
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
WHERE lesson_id = 'project-zero-full';

-- Success message
DO $$
BEGIN
    RAISE NOTICE '✅ Project Zero FULL lesson created (Part 1 - Introduction)!';
    RAISE NOTICE '📚 Cards so far: 5 (hero, content, lightbulb, data, content)';
    RAISE NOTICE '⏱️ Duration: 45 minutes';
    RAISE NOTICE '⚡ XP Reward: 150';
    RAISE NOTICE '📝 More modules to be added...';
END $$;
