-- Migration: 006_seed_lessons_content.sql
-- Description: Seed Lesson 1 (Torque) and Lesson 2 (Consultative Selling) content
-- Author: BrainVenture V3
-- Date: 2026-01-16
-- Run this after migration 005 (companies/roles seed)

-- ============================================
-- SEED LESSON CONTENT
-- ============================================

-- Lesson 1: Dobór Właściwego Momentu Obrotowego (Automotive)
INSERT INTO lessons (
  lesson_id,
  title,
  description,
  duration_minutes,
  xp_reward,
  difficulty,
  content
) VALUES (
  'lesson-1-torque-automotive',
  'Dobór Właściwego Momentu Obrotowego',
  'Od aplikacji do wyboru klucza - warsztaty samochodowe. Naucz się dopasowywać klucze Milwaukee do zastosowań automotive.',
  35,
  150,
  'beginner',
  '{
    "cards": [
      {
        "id": "card-1",
        "type": "hero",
        "title": "Dobór Właściwego Momentu Obrotowego",
        "subtitle": "Application-first selling dla narzędzi automotive",
        "content": "**Najczęstszy błąd sprzedawców:** Polecanie klucza na podstawie ceny, a nie aplikacji. W tej lekcji nauczysz się jak dopasować narzędzie Milwaukee do potrzeb warsztatu samochodowego."
      },
      {
        "id": "card-2",
        "type": "content",
        "title": "Co to jest Moment Obrotowy (Nm)?",
        "content": "Moment obrotowy mierzony w Niutonometrach (Nm) określa siłę dokręcania. **Przykłady:** Koła samochodu: 90-120 Nm, Podwozie: 40-80 Nm, Elementy silnika: 20-60 Nm. Klucz musi mieć WYŻSZY maksymalny moment niż potrzeba aplikacji."
      },
      {
        "id": "card-3",
        "type": "content",
        "title": "3 Kategorie Kluczy Udarowych",
        "content": "**Subkompaktowe (M12):** Do 135 Nm - delikatne prace, ciasne przestrzenie. **Kompaktowe (M18):** Do 300 Nm - codzienne zastosowania warsztatowe. **Wysokomomentowe (M18 FHIWF):** Do 1000+ Nm - ciężkie aplikacje, koła ciężarówek."
      },
      {
        "id": "card-4",
        "type": "interactive",
        "title": "Dopasuj klucz do aplikacji",
        "quiz": {
          "question": "Klient serwisuje osobówki i SUV-y. Która kategoria kluczy będzie najlepsza?",
          "options": [
            "M12 Subkompaktowy (135 Nm)",
            "M18 Kompaktowy (300 Nm)",
            "M18 Wysokomomentowy (1000+ Nm)"
          ],
          "correct": 1,
          "explanation": "M18 Kompaktowy 300 Nm to sweet spot dla warsztatów osobowych. Wystarczający moment na koła i podwozie, a nie przepłaca za nadmiarową moc."
        }
      }
    ]
  }'::jsonb
)
ON CONFLICT (lesson_id) DO NOTHING;

-- Lesson 2: Sprzedaż Konsultacyjna - SPIN (Automotive/PPE)
INSERT INTO lessons (
  lesson_id,
  title,
  description,
  duration_minutes,
  xp_reward,
  difficulty,
  content
) VALUES (
  'lesson-2-consultative-selling',
  'Sprzedaż Konsultacyjna - Metoda SPIN',
  'Odkryj jak zadawać właściwe pytania zamiast cisnąć features. SPIN to framework do consultative selling dla produktów Milwaukee.',
  35,
  150,
  'intermediate',
  '{
    "cards": [
      {
        "id": "card-1",
        "type": "hero",
        "title": "Sprzedaż Konsultacyjna - SPIN",
        "subtitle": "Od features do value - jak sprzedawać doradczo",
        "content": "**Problem tradycyjnej sprzedaży:** Przedstawiciel bombarduje klienta features (\"Ma bezszczotkowy silnik! 5.0 Ah baterie!\"). Klient nie rozumie po co mu to. W tej lekcji nauczysz się SPIN - pytania które odkrywają prawdziwe potrzeby."
      },
      {
        "id": "card-2",
        "type": "content",
        "title": "S - Situation Questions (Pytania Sytuacyjne)",
        "content": "**Cel:** Zrozumieć obecną sytuację klienta. **Przykłady:** Jakie narzędzia obecnie używasz? Ile mechaników pracuje w warsztacie? Jakie masz najczęstsze aplikacje? **UWAGA:** Nie zadawaj za dużo - nudne dla klienta."
      },
      {
        "id": "card-3",
        "type": "content",
        "title": "P - Problem Questions (Pytania Problemowe)",
        "content": "**Cel:** Odkryć problemy i frustracje. **Przykłady:** Czy zdarza się że klucz nie radzi sobie z zardzewiałymi śrubami? Ile czasu tracisz na ładowanie narzędzi? Czy masz kłopoty z przechowywaniem nasadek? **TRICK:** Problemy to szanse sprzedażowe!"
      },
      {
        "id": "card-4",
        "type": "interactive",
        "title": "SPIN w akcji - scenariusz",
        "quiz": {
          "question": "Klient mówi: ''Mam już klucze pneumatyczne, działają OK''. Które pytanie odkryje problem?",
          "options": [
            "Czy wiesz że Milwaukee ma bezszczotkowy motor?",
            "Czy sprężarka czasem Cię zawodzi albo hałasuje?",
            "Milwaukee jest najlepszy na rynku, chcesz kupić?"
          ],
          "correct": 1,
          "explanation": "Pytanie problemowe odkrywa pain point (zawodna sprężarka). Teraz możesz pokazać value akumulatorów jako rozwiązanie."
        }
      }
    ]
  }'::jsonb
)
ON CONFLICT (lesson_id) DO NOTHING;

-- ============================================
-- VERIFICATION
-- ============================================

-- View inserted lessons
SELECT 
  lesson_id,
  title,
  difficulty,
  xp_reward,
  duration_minutes
FROM lessons
ORDER BY lesson_id;

-- Expected result: 2 lessons
-- - lesson-1-torque-automotive
-- - lesson-2-consultative-selling
