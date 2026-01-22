-- Migration: 014_add_lesson_status.sql
-- Description: Add status and release_date fields for lesson roadmap visibility
-- Author: BrainVenture V3
-- Date: 2026-01-21

-- ============================================
-- PHASE 1: ADD STATUS FIELD
-- ============================================

-- Add status column to lessons table
ALTER TABLE lessons 
ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'published' 
CHECK (status IN ('draft', 'coming_soon', 'published', 'archived'));

-- Add release_date for coming_soon lessons
ALTER TABLE lessons 
ADD COLUMN IF NOT EXISTS release_date DATE;

-- Add priority order for display
ALTER TABLE lessons 
ADD COLUMN IF NOT EXISTS display_order INTEGER DEFAULT 0;

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_lessons_status ON lessons(status);
CREATE INDEX IF NOT EXISTS idx_lessons_release_date ON lessons(release_date) WHERE release_date IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_lessons_display_order ON lessons(display_order);

-- ============================================
-- PHASE 2: UPDATE EXISTING LESSON
-- ============================================

-- Mark Lesson 1.1 as published (it's already live)
UPDATE lessons 
SET status = 'published', display_order = 1
WHERE lesson_id = 'lesson-1-1-milwaukee-story';

-- ============================================
-- COMMENTS
-- ============================================

COMMENT ON COLUMN lessons.status IS 'Lesson lifecycle state: draft (not visible), coming_soon (roadmap only), published (live), archived (hidden but accessible)';
COMMENT ON COLUMN lessons.release_date IS 'Expected release date for coming_soon lessons (NULL for published)';
COMMENT ON COLUMN lessons.display_order IS 'Display order within module (lower = first)';

-- ============================================
-- VERIFICATION
-- ============================================

-- Check that status column was added
SELECT 
  table_name,
  column_name,
  data_type,
  column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'lessons'
  AND column_name IN ('status', 'release_date', 'display_order')
ORDER BY column_name;

-- Verify Lesson 1.1 status
SELECT id, title, status, display_order, release_date
FROM lessons
WHERE lesson_id = 'lesson-1-1-milwaukee-story';
