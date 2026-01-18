-- Migration: 008_add_lesson_category.sql
-- Description: Add category column to lessons for topic filtering
-- Author: BrainVenture V3
-- Date: 2026-01-18

-- ============================================
-- ADD CATEGORY COLUMN
-- ============================================

-- Add category column to lessons
ALTER TABLE lessons 
ADD COLUMN IF NOT EXISTS category TEXT;

-- Create index for category filtering
CREATE INDEX IF NOT EXISTS idx_lessons_category ON lessons(category);

-- ============================================
-- UPDATE EXISTING LESSONS WITH CATEGORIES
-- ============================================

-- Lesson 1: Torque - Wiedza produktowa (Product Knowledge)
UPDATE lessons 
SET category = 'Wiedza produktowa'
WHERE lesson_id = 'lesson-1-torque-automotive';

-- Lesson 2: SPIN Selling - Sprzedaż (Sales)
UPDATE lessons 
SET category = 'Sprzedaż'
WHERE lesson_id = 'lesson-2-consultative-selling';

-- ============================================
-- VERIFICATION
-- ============================================

SELECT lesson_id, title, category, difficulty
FROM lessons
ORDER BY lesson_id;

-- Expected categories:
-- Wiedza produktowa, Sprzedaż, Leadership, Negocjacje, Produktywność, etc.
