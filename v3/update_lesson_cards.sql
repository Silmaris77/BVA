-- Update sample lessons with actual card content for Day 5 testing
-- Run this in Supabase SQL Editor

UPDATE lessons 
SET content_json = '{
  "cards": [
    {
      "type": "intro",
      "title": "Milwaukee Canvas - Krok 4/7",
      "subtitle": "Zaawansowane techniki sprzedaży B2B",
      "description": "W tej lekcji poznasz krok 4 metodyki Milwaukee Canvas - Application First. Dowiesz się jak skutecznie prezentować wartość swojego produktu klientom biznesowym.",
      "icon": "🎯"
    },
    {
      "type": "concept",
      "title": "Czym jest Application First?",
      "content": "Application First to podejście koncentrujące się na **zastosowaniu produktu** zamiast jego cech technicznych.\n\nKluczowe zasady:\n- Zrozumienie kontekstu klienta\n- Dopasowanie rozwiązania do potrzeb\n- Prezentacja wartości biznesowej",
      "keyPoints": [
        "Zacznij od zrozumienia potrzeb klienta",
        "Dopasuj rozwiązanie do kontekstu biznesowego",
        "Przedstaw konkretne korzyści, nie cechy"
      ]
    },
    {
      "type": "question",
      "question": "Co jest najważniejsze w podejściu Application First?",
      "options": [
        "Prezentacja wszystkich funkcji produktu",
        "Zrozumienie potrzeb i kontekstu klienta",
        "Najniższa cena na rynku",
        "Szybka dostępność produktu"
      ],
      "correctAnswer": 1,
      "explanation": "Application First koncentruje się na potrzebach klienta. Musisz najpierw zrozumieć jego kontekst biznesowy, aby móc zaproponować odpowiednie rozwiązanie."
    },
    {
      "type": "summary",
      "title": "Lekcja ukończona!",
      "recap": [
        "Poznałeś metodykę Application First",
        "Zrozumiałeś znaczenie kontekstu klienta",
        "Przećwiczyłeś podejście w quizie praktycznym"
      ],
      "nextSteps": "Przejdź do kolejnej lekcji Milwaukee Canvas",
      "badge": {
        "xp": 50,
        "title": "Milwaukee Expert"
      }
    }
  ]
}'::jsonb
WHERE title = 'Milwaukee Canvas - Krok 4/7';

-- Update another lesson with sample content
UPDATE lessons 
SET content_json = '{
  "cards": [
    {
      "type": "intro",
      "title": "Neural Implant: Leadership Basics",
      "subtitle": "Podstawy efektywnego przywództwa",
      "description": "Ten kurs wprowadzi Cię w świat zarządzania zespołem, motywowania pracowników i budowania kultury organizacyjnej.",
      "icon": "👑"
    },
    {
      "type": "concept",
      "title": "Cztery filary przywództwa",
      "content": "Efektywne przywództwo opiera się na czterech fundamentach:\n\n**1. Wizja** - Określ jasny kierunek\n**2. Komunikacja** - Dziel się wizją regularnie\n**3. Inspiracja** - Motywuj przez przykład\n**4. Rozwój** - Inwestuj w ludzi",
      "keyPoints": [
        "Lider musi mieć jasną wizję przyszłości",
        "Regularna komunikacja buduje zaufanie",
        "Przykład jest silniejszy niż słowa"
      ]
    },
    {
      "type": "question",
      "question": "Który element NIE jest filarem przywództwa?",
      "options": [
        "Wizja",
        "Kontrola",
        "Inspiracja",
        "Rozwój"
      ],
      "correctAnswer": 1,
      "explanation": "Kontrola nie jest filarem przywództwa. Skuteczny lider inspiruje i rozwija zespół, zamiast go kontrolować."
    },
    {
      "type": "summary",
      "title": "Gratulacje ukończenia!",
      "recap": [
        "Poznałeś cztery filary przywództwa",
        "Zrozumiałeś różnicę między liderem a szefem",
        "Przećwiczyłeś wiedzę w quizie"
      ],
      "nextSteps": "Zastosuj poznate zasady w praktyce ze swoim zespołem",
      "badge": {
        "xp": 100,
        "title": "Leadership Beginner"
      }
    }
  ]
}'::jsonb
WHERE title = 'Neural Implant: Leadership Basics';

-- Verify the updates
SELECT id, title, content_json->'cards'->0->>'type' as first_card_type
FROM lessons 
WHERE content_json IS NOT NULL AND content_json != '{}'::jsonb
LIMIT 5;
