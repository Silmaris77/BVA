-- Migration: 009_add_category_to_engrams_tools.sql
-- Description: Add category column to engrams and tools tables for filtering
-- Author: BrainVenture V3
-- Date: 2026-01-18

-- ============================================
-- ADD CATEGORY COLUMNS
-- ============================================

-- Add category to engrams
ALTER TABLE engrams 
ADD COLUMN IF NOT EXISTS category TEXT;

-- Add category to tools
ALTER TABLE tools 
ADD COLUMN IF NOT EXISTS category TEXT;

-- Create indexes for category filtering
CREATE INDEX IF NOT EXISTS idx_engrams_category ON engrams(category);
CREATE INDEX IF NOT EXISTS idx_tools_category ON tools(category);

-- ============================================
-- SEED SAMPLE ENGRAMS
-- ============================================

-- Engram 1: SPIN Questions
INSERT INTO engrams (
  engram_id,
  title,
  category,
  slides,
  quiz_pool,
  install_xp,
  refresh_xp
) VALUES (
  'engram-spin-questions',
  'Pytania SPIN',
  'Sprzedaż',
  '[
    {"id": "s1", "title": "Co to SPIN?", "content": "SPIN to framework pytań: Situation, Problem, Implication, Need-payoff."},
    {"id": "s2", "title": "Situation Questions", "content": "Poznaj sytuację klienta: Jakie narzędzia obecnie używasz?"},
    {"id": "s3", "title": "Problem Questions", "content": "Odkryj problemy: Czy masz kłopoty z...?"}
  ]'::jsonb,
  '[
    {"q": "Co oznacza S w SPIN?", "a": "Situation", "wrong": ["Sales", "Solution", "Service"]},
    {"q": "Które pytania odkrywają frustracje?", "a": "Problem", "wrong": ["Situation", "Implication", "Need-payoff"]}
  ]'::jsonb,
  50,
  25
)
ON CONFLICT (engram_id) DO UPDATE SET
  title = EXCLUDED.title,
  category = EXCLUDED.category;

-- Engram 2: M18 vs M12
INSERT INTO engrams (
  engram_id,
  title,
  category,
  slides,
  quiz_pool,
  install_xp,
  refresh_xp
) VALUES (
  'engram-m18-vs-m12',
  'Platforma M18 vs M12',
  'Wiedza produktowa',
  '[
    {"id": "s1", "title": "Dwie platformy", "content": "Milwaukee oferuje M12 (kompaktowy) i M18 (pełnowymiarowy)."},
    {"id": "s2", "title": "M12 - Kiedy?", "content": "Ciasne przestrzenie, precyzyjne prace, lekkie zastosowania."},
    {"id": "s3", "title": "M18 - Kiedy?", "content": "Duża moc, ciężkie aplikacje, długi czas pracy."}
  ]'::jsonb,
  '[
    {"q": "Która platforma dla ciasnych przestrzeni?", "a": "M12", "wrong": ["M18", "MX FUEL", "M28"]},
    {"q": "Co oznacza M18?", "a": "18V platforma", "wrong": ["Model 18", "18 narzędzi", "18 lat gwarancji"]}
  ]'::jsonb,
  50,
  25
)
ON CONFLICT (engram_id) DO UPDATE SET
  title = EXCLUDED.title,
  category = EXCLUDED.category;

-- Engram 3: Feedback Framework
INSERT INTO engrams (
  engram_id,
  title,
  category,
  slides,
  quiz_pool,
  install_xp,
  refresh_xp
) VALUES (
  'engram-feedback-sbi',
  'Framework SBI do feedbacku',
  'Leadership',
  '[
    {"id": "s1", "title": "Co to SBI?", "content": "Situation-Behavior-Impact: prosty framework do dawania feedbacku."},
    {"id": "s2", "title": "Situation", "content": "Opisz konkretną sytuację: kiedy, gdzie."},
    {"id": "s3", "title": "Behavior + Impact", "content": "Opisz zachowanie (nie osobę) i jego wpływ na zespół/wyniki."}
  ]'::jsonb,
  '[
    {"q": "Co oznacza B w SBI?", "a": "Behavior", "wrong": ["Business", "Belief", "Benefit"]},
    {"q": "SBI skupia się na?", "a": "Zachowaniu, nie osobie", "wrong": ["Osobie", "Wynikach", "Celach"]}
  ]'::jsonb,
  50,
  25
)
ON CONFLICT (engram_id) DO UPDATE SET
  title = EXCLUDED.title,
  category = EXCLUDED.category;

-- ============================================
-- SEED SAMPLE TOOLS
-- ============================================

-- Tool 1: Kalkulator Momentu
INSERT INTO tools (
  tool_id,
  title,
  description,
  category,
  tier,
  usage_xp,
  config
) VALUES (
  'tool-torque-calculator',
  'Kalkulator Momentu Obrotowego',
  'Oblicz wymagany moment obrotowy na podstawie aplikacji i rozmiaru śruby.',
  'Wiedza produktowa',
  1,
  25,
  '{
    "type": "calculator",
    "inputs": [
      {"name": "application", "type": "select", "options": ["Koła osobowe", "Koła ciężarowe", "Podwozie", "Silnik"]},
      {"name": "bolt_size", "type": "select", "options": ["M10", "M12", "M14", "M16", "M18", "M20"]}
    ],
    "output": "recommended_tool"
  }'::jsonb
)
ON CONFLICT (tool_id) DO UPDATE SET
  title = EXCLUDED.title,
  category = EXCLUDED.category;

-- Tool 2: Generator pytań SPIN
INSERT INTO tools (
  tool_id,
  title,
  description,
  category,
  tier,
  usage_xp,
  config
) VALUES (
  'tool-spin-generator',
  'Generator pytań SPIN',
  'Wygeneruj pytania SPIN dopasowane do branży i sytuacji klienta.',
  'Sprzedaż',
  2,
  50,
  '{
    "type": "generator",
    "inputs": [
      {"name": "industry", "type": "select", "options": ["Automotive", "Budownictwo", "Przemysł", "MRO"]},
      {"name": "pain_point", "type": "text", "placeholder": "Główny problem klienta..."}
    ],
    "output": "spin_questions"
  }'::jsonb
)
ON CONFLICT (tool_id) DO UPDATE SET
  title = EXCLUDED.title,
  category = EXCLUDED.category;

-- ============================================
-- VERIFICATION
-- ============================================

SELECT engram_id, title, category FROM engrams ORDER BY engram_id;
SELECT tool_id, title, category, tier FROM tools ORDER BY tier, tool_id;
