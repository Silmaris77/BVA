-- Migration: 012_add_learning_path_organization.sql
-- Description: Add company and role fields to learning_paths table
-- Author: BrainVenture V3
-- Date: 2026-01-20

-- ============================================
-- ADD ORGANIZATION FIELDS TO LEARNING PATHS
-- ============================================

ALTER TABLE learning_paths
  ADD COLUMN IF NOT EXISTS company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  ADD COLUMN IF NOT EXISTS target_roles TEXT[],
  ADD COLUMN IF NOT EXISTS tags TEXT[];

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_learning_paths_company_id ON learning_paths(company_id);
CREATE INDEX IF NOT EXISTS idx_learning_paths_target_roles ON learning_paths USING GIN(target_roles);

-- Add comments
COMMENT ON COLUMN learning_paths.company_id IS 'FK to companies - null means available to all companies (e.g. general paths)';
COMMENT ON COLUMN learning_paths.target_roles IS 'Roles this path is intended for';
