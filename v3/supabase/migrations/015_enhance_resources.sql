-- Migration: 015_enhance_resources.sql
-- Description: Add category, image, and access control to resources
-- Author: BrainVenture V3
-- Date: 2026-01-23

-- Add new columns to resources table
ALTER TABLE resources 
ADD COLUMN IF NOT EXISTS category TEXT,
ADD COLUMN IF NOT EXISTS image_url TEXT,
ADD COLUMN IF NOT EXISTS tier INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS locked BOOLEAN DEFAULT false,
ADD COLUMN IF NOT EXISTS external_url TEXT; -- For linking to external tools/docs

-- Extend resource_type constraint to include 'ebook' and 'tool'
ALTER TABLE resources 
DROP CONSTRAINT IF EXISTS resources_resource_type_check;

ALTER TABLE resources 
ADD CONSTRAINT resources_resource_type_check 
CHECK (resource_type IN ('pdf', 'table', 'guide', 'template', 'ebook', 'tool'));

-- Create index for category filtering
CREATE INDEX IF NOT EXISTS idx_resources_category ON resources(category);

-- Add comment
COMMENT ON COLUMN resources.category IS 'Resource category (Sales, Product, Leadership)';
COMMENT ON COLUMN resources.tier IS 'Access tier level (1=Basic, 2=Advanced, 3=Expert)';
