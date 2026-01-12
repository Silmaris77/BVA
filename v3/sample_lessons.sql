-- Sample lessons for BrainVenture V3
-- Run this in Supabase SQL Editor

INSERT INTO lessons (
  title,
  description,
  category,
  difficulty,
  duration_minutes,
  xp_reward,
  card_count,
  content_json
) VALUES
(
  'Milwaukee Canvas - Krok 4/7',
  'Zaawansowane techniki sprzedaży B2B z wykorzystaniem metodyki Milwaukee Canvas. Naucz się skutecznie prezentować wartość swojego produktu klientom biznesowym.',
  'Komunikacja',
  'intermediate',
  12,
  50,
  7,
  '{"cards": []}'
),
(
  'Neural Implant: Leadership Basics',
  'Poznaj podstawy efektywnego przywództwa. Ten kurs wprowadzi Cię w świat zarządzania zespołem, motywowania pracowników i budowania kultury organizacyjnej.',
  'Leadership',
  'beginner',
  24,
  100,
  12,
  '{"cards": []}'
),
(
  'Tygodniowe Wyzwanie: 5 lekcji',
  'Kompleksowy program rozwojowy obejmujący strategię, negocjacje i zarządzanie projektami. Ukończ wszystkie moduły aby zdobyć bonus XP!',
  'Strategy',
  'advanced',
  50,
  200,
  20,
  '{"cards": []}'
),
(
  'Conversational Intelligence',
  'Opanuj sztukę skutecznej komunikacji interpersonalnej. Dowiedz się jak prowadzić trudne rozmowy, budować relacje i rozwiązywać konflikty.',
  'Komunikacja',
  'intermediate',
  18,
  75,
  10,
  '{"cards": []}'
),
(
  'Sales Mastery: Cold Calling',
  'Profesjonalne techniki cold callingu. Naucz się jak przełamywać opór klienta, budować zainteresowanie i zamykać spotkania sprzedażowe.',
  'Sales',
  'advanced',
  30,
  120,
  15,
  '{"cards": []}'
),
(
  'Podstawy Zarządzania Czasem',
  'Efektywne planowanie i priorytetyzacja zadań. Poznaj sprawdzone metody jak Matrix Eisenhowera, Pomodoro i Getting Things Done.',
  'Leadership',
  'beginner',
  15,
  60,
  8,
  '{"cards": []}'
),
(
  'Negocjacje Win-Win',
  'Strategiczne podejście do negocjacji biznesowych. Naucz się jak osiągać porozumienia korzystne dla obu stron i budować długoterminowe relacje.',
  'Strategy',
  'intermediate',
  25,
  90,
  13,
  '{"cards": []}'
),
(
  'Prezentacje Wysokiego Impaktu',
  'Twórz i prowadź prezentacje które zapadają w pamięć. Od storytellingu po wizualizację danych - wszystko czego potrzebujesz.',
  'Komunikacja',
  'beginner',
  20,
  80,
  11,
  '{"cards": []}'
);

-- Verify the data
SELECT id, title, category, difficulty, xp_reward FROM lessons ORDER BY created_at DESC;
