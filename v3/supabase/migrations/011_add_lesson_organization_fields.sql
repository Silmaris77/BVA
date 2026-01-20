-- Migration: 011_add_lesson_organization_fields.sql
-- Description: Add company, module, track, and role-based fields to lessons
-- Author: BrainVenture V3
-- Date: 2026-01-20
-- Purpose: Enable multi-tenant support and learning path organization

-- ============================================
-- ADD ORGANIZATION FIELDS TO LESSONS
-- ============================================

-- Add new columns to lessons table
ALTER TABLE lessons
  ADD COLUMN IF NOT EXISTS company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  ADD COLUMN IF NOT EXISTS module TEXT,  -- e.g. "Module 1: Foundations"
  ADD COLUMN IF NOT EXISTS track TEXT,   -- e.g. "Foundation Track", "Professional Track"
  ADD COLUMN IF NOT EXISTS target_roles TEXT[],  -- e.g. ['JSS', 'ASR', 'KAM', 'BDM', 'FME']
  ADD COLUMN IF NOT EXISTS tags TEXT[];  -- e.g. ['milwaukee', 'history', 'sales', 'onboarding']

-- Create indexes for filtering and performance
CREATE INDEX IF NOT EXISTS idx_lessons_company_id ON lessons(company_id);
CREATE INDEX IF NOT EXISTS idx_lessons_module ON lessons(module);
CREATE INDEX IF NOT EXISTS idx_lessons_track ON lessons(track);
CREATE INDEX IF NOT EXISTS idx_lessons_target_roles ON lessons USING GIN(target_roles);
CREATE INDEX IF NOT EXISTS idx_lessons_tags ON lessons USING GIN(tags);

-- Add comments for documentation
COMMENT ON COLUMN lessons.company_id IS 'FK to companies - null means available to all companies';
COMMENT ON COLUMN lessons.module IS 'Module name for grouping lessons (e.g. "Module 1: Foundations")';
COMMENT ON COLUMN lessons.track IS 'Learning track name (e.g. "Foundation Track", "JSS Professional")';
COMMENT ON COLUMN lessons.target_roles IS 'Array of roles this lesson is intended for (null = all roles)';
COMMENT ON COLUMN lessons.tags IS 'Array of tags for categorization and search';

-- ============================================
-- ADD SAME FIELDS TO OTHER CONTENT TYPES
-- ============================================

-- Engrams
ALTER TABLE engrams
  ADD COLUMN IF NOT EXISTS company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  ADD COLUMN IF NOT EXISTS category TEXT,  -- e.g. "learning", "productivity", "sales"
  ADD COLUMN IF NOT EXISTS target_roles TEXT[],
  ADD COLUMN IF NOT EXISTS tags TEXT[];

CREATE INDEX IF NOT EXISTS idx_engrams_company_id ON engrams(company_id);
CREATE INDEX IF NOT EXISTS idx_engrams_category ON engrams(category);
CREATE INDEX IF NOT EXISTS idx_engrams_target_roles ON engrams USING GIN(target_roles);

-- Tools
ALTER TABLE tools
  ADD COLUMN IF NOT EXISTS company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  ADD COLUMN IF NOT EXISTS category TEXT,  -- e.g. "calculator", "generator", "selector"
  ADD COLUMN IF NOT EXISTS target_roles TEXT[],
  ADD COLUMN IF NOT EXISTS tags TEXT[];

CREATE INDEX IF NOT EXISTS idx_tools_company_id ON tools(company_id);
CREATE INDEX IF NOT EXISTS idx_tools_category ON tools(category);
CREATE INDEX IF NOT EXISTS idx_tools_target_roles ON tools USING GIN(target_roles);

-- Resources
ALTER TABLE resources
  ADD COLUMN IF NOT EXISTS company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  ADD COLUMN IF NOT EXISTS category TEXT,  -- e.g. "battle_card", "spec_sheet", "script"
  ADD COLUMN IF NOT EXISTS target_roles TEXT[],
  ADD COLUMN IF NOT EXISTS tags TEXT[];

CREATE INDEX IF NOT EXISTS idx_resources_company_id ON resources(company_id);
CREATE INDEX IF NOT EXISTS idx_resources_category ON resources(category);
CREATE INDEX IF NOT EXISTS idx_resources_target_roles ON resources USING GIN(target_roles);

-- Drills
ALTER TABLE drills
  ADD COLUMN IF NOT EXISTS company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  ADD COLUMN IF NOT EXISTS category TEXT,  -- e.g. "roleplay", "scenario", "knowledge_check"
  ADD COLUMN IF NOT EXISTS target_roles TEXT[],
  ADD COLUMN IF NOT EXISTS tags TEXT[];

CREATE INDEX IF NOT EXISTS idx_drills_company_id ON drills(company_id);
CREATE INDEX IF NOT EXISTS idx_drills_category ON drills(category);
CREATE INDEX IF NOT EXISTS idx_drills_target_roles ON drills USING GIN(target_roles);

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check new columns exist
SELECT 
  column_name, 
  data_type,
  is_nullable
FROM information_schema.columns
WHERE table_name = 'lessons'
  AND column_name IN ('company_id', 'module', 'track', 'target_roles', 'tags')
ORDER BY column_name;

-- Expected result: 5 rows showing new columns
