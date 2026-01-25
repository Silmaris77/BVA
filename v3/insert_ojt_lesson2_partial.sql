-- SQL script to insert "Model OJT - 5 Etapów" lesson into Supabase (PARTIAL - first 2 cards only)
-- Run this in Supabase SQL Editor

INSERT INTO lessons (
    id,
    lesson_id,
    title,
    description,
    difficulty,
    duration_minutes,
    xp_reward,
    content
) VALUES (
    gen_random_uuid(),
    'ojt_lesson_2_model',
    'Jak rozwijać pracowników bez odrywania ich od pracy?',
    'Poznaj 5-etapowy model On-the-Job Training, który w 3–4 miesiące zwiększa skuteczność zespołu o 20–50%, skraca czas rozwoju o połowę i realnie uwalnia czas menedżera.',
    'beginner',
    25,
    300,
    '{
      "cards": [
        {
          "id": 1,
          "type": "hero",
          "title": "Jak rozwijać pracowników bez odrywania ich od pracy?",
          "content": "Poznaj 5-etapowy model On-the-Job Training",
          "sections": [
            {
              "icon": "👥",
              "title": "Dla kogo",
              "content": "Menedżerowie, którzy chcą przestać gasić pożary i zbudować zespół, który działa samodzielnie, bez ciągłego angażowania ich czasu."
            },
            {
              "icon": "🎯",
              "title": "Cel",
              "content": "Poznać 5-etapowy model On-the-Job Training, który w 3–4 miesiące:",
              "list": [
                "zwiększa skuteczność zespołu o 20–50%,",
                "skraca czas rozwoju o połowę,",
                "realnie uwalnia czas menedżera."
              ]
            },
            {
              "icon": "💡",
              "title": "Dlaczego to działa",
              "content": "70% kompetencji powstaje w praktyce. OJT to nauka w realnym biznesie + natychmiastowy feedback — 4× szybszy rozwój i trwała zmiana zachowań, nie teoria."
            }
          ],
          "estimated_seconds": 90,
          "xp_points": 10
        },
        {
          "id": 2,
          "type": "data",
          "title": "Dlaczego On-the-Job Training działa?",
          "content": "Większość kompetencji zawodowych rozwija się w praktyce, nie na szkoleniach formalnych (model 70-20-10).\\n\\nOJT skraca czas dojścia do samodzielności, bo łączy naukę z realną pracą i natychmiastowym feedbackiem.\\n\\nBadania L&D pokazują, że uczenie przez działanie ma znacząco wyższą trwałość efektów niż wykłady czy e-learning bez kontekstu.",
          "stats": [
            {
              "value": "70%",
              "label": "Procent wiedzy zawodowej zdobywanej przez praktyczne doświadczenie"
            },
            {
              "value": "4x",
              "label": "Szybciej rozwijają się pracownicy w treningu OJT vs tradycyjne szkolenia"
            },
            {
              "value": "85%",
              "label": "Wskaźnik retencji wiedzy przy nauce przez działanie vs 20% przy wykładach"
            }
          ],
          "callout": {
            "type": "info",
            "title": "Kluczowy wniosek:",
            "text": "Najskuteczniejsze uczenie się odbywa się w kontekście rzeczywistych zadań, z szybkim feedbackiem od bardziej doświadczonej osoby. To zmiana zachowań w pracy, a nie transfer teorii z sali szkoleniowej."
          },
          "sources": "Źródła: Deloitte (model 70-20-10), ATD, literatura L&D",
          "estimated_seconds": 120,
          "xp_points": 10
        }
      ]
    }'::jsonb
);
