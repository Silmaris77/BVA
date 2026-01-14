-- Day 9 Seed: Definicje Combo (3 Synergy Combos) - WERSJA POLSKA

-- ========================================
-- COMBO 1: Mistrz Negocjacji
-- ========================================
INSERT INTO combo_definitions (id, name, required_engrams, bonus_type, bonus_value, description)
VALUES (
  'c0000000-0000-0000-0000-000000000001',
  'Mistrz Negocjacji',
  '["b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12", "e2000000-0000-0000-0000-000000000002", "e2000000-0000-0000-0000-000000000003"]'::jsonb,
  'xp_multiplier',
  '{"category": "Sales", "multiplier": 1.5}'::jsonb,
  'Opanuj negocjacje łącząc OODA Loop (szybkie decyzje), Canvas Propozycji Wartości i Radzenie Sobie z Obiekcjami. Odblokuj +50% XP ze wszystkich lekcji Sales.'
);

-- ========================================
-- COMBO 2: Strategiczny Lider
-- ========================================
INSERT INTO combo_definitions (id, name, required_engrams, bonus_type, bonus_value, description)
VALUES (
  'c0000000-0000-0000-0000-000000000002',
  'Strategiczny Lider',
  '["e1000000-0000-0000-0000-000000000001", "e1000000-0000-0000-0000-000000000002", "e3000000-0000-0000-0000-000000000002"]'::jsonb,
  'xp_multiplier',
  '{"category": "Leadership", "multiplier": 1.25}'::jsonb,
  'Połącz Budowanie Zespołu, Delegowanie i Canvas Modelu Biznesowego dla doskonałości strategicznego przywództwa. Odblokuj +25% XP z lekcji Leadership.'
);

-- ========================================
-- COMBO 3: Potęga Sprzedaży
-- ========================================
INSERT INTO combo_definitions (id, name, required_engrams, bonus_type, bonus_value, description)
VALUES (
  'c0000000-0000-0000-0000-000000000003',
  'Potęga Sprzedaży',
  '["e2000000-0000-0000-0000-000000000001", "e2000000-0000-0000-0000-000000000002", "e2000000-0000-0000-0000-000000000003"]'::jsonb,
  'resource_unlock',
  '{"resource_ids": ["sales-templates-pack"]}'::jsonb,
  'Ukończ trójcę SPIN Selling, Canvas Propozycji Wartości i Radzenie Sobie z Obiekcjami aby odblokować ekskluzywny pakiet Szablonów Sprzedażowych.'
);

-- Uwaga: Mapowanie wymaganych ID engramów
-- Combo 1 (Mistrz Negocjacji):
  -- b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12 = OODA Loop (istniejący przykładowy engram)
  -- e2000000-0000-0000-0000-000000000002 = Canvas Propozycji Wartości
  -- e2000000-0000-0000-0000-000000000003 = Radzenie Sobie z Obiekcjami

-- Combo 2 (Strategiczny Lider):
  -- e1000000-0000-0000-0000-000000000001 = Podstawy Budowania Zespołu
  -- e1000000-0000-0000-0000-000000000002 = Mistrz Delegowania
  -- e3000000-0000-0000-0000-000000000002 = Canvas Modelu Biznesowego

-- Combo 3 (Potęga Sprzedaży):
  -- e2000000-0000-0000-0000-000000000001 = Podstawy SPIN Selling
  -- e2000000-0000-0000-0000-000000000002 = Canvas Propozycji Wartości
  -- e2000000-0000-0000-0000-000000000003 = Radzenie Sobie z Obiekcjami
