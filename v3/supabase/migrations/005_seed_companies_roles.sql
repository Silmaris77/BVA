-- Migration: 005_seed_companies_roles.sql
-- Description: Seed initial companies (Milwaukee, Warta) and role types
-- Author: BrainVenture V3
-- Date: 2026-01-16
-- Run this after migrations 001-004 are complete

-- ============================================
-- SEED COMPANIES
-- ============================================

-- Note: 'general' company already exists from migration 002

-- Milwaukee Tool
INSERT INTO companies (company_slug, name, logo_url, is_general_group) 
VALUES (
  'milwaukee',
  'Milwaukee Tool',
  'https://www.milwaukeetool.com/logo.png', -- Update with real logo URL
  false
)
ON CONFLICT (company_slug) DO NOTHING;

-- Warta
INSERT INTO companies (company_slug, name, logo_url, is_general_group) 
VALUES (
  'warta',
  'Warta',
  NULL, -- Add logo URL when available
  false
)
ON CONFLICT (company_slug) DO NOTHING;

-- ============================================
-- SEED USER ROLES
-- ============================================

-- Note: 'learner' role already exists from migration 002

-- Sales Representative
INSERT INTO user_roles (role_slug, display_name, description)
VALUES (
  'sales-rep',
  'Sales Representative',
  'Field sales representative role for product sales'
)
ON CONFLICT (role_slug) DO NOTHING;

-- Manager
INSERT INTO user_roles (role_slug, display_name, description)
VALUES (
  'manager',
  'Manager',
  'Team manager with access to analytics and team management'
)
ON CONFLICT (role_slug) DO NOTHING;

-- Technician
INSERT INTO user_roles (role_slug, display_name, description)
VALUES (
  'technician',
  'Technician',
  'Technical support and product specialist'
)
ON CONFLICT (role_slug) DO NOTHING;

-- Admin
INSERT INTO user_roles (role_slug, display_name, description)
VALUES (
  'admin',
  'Administrator',
  'Platform administrator with full access'
)
ON CONFLICT (role_slug) DO NOTHING;

-- ============================================
-- VERIFICATION
-- ============================================

-- View all companies
SELECT 
  company_slug,
  name,
  is_general_group,
  created_at
FROM companies
ORDER BY 
  CASE WHEN is_general_group THEN 0 ELSE 1 END,
  name;

-- View all roles
SELECT 
  role_slug,
  display_name,
  description,
  created_at
FROM user_roles
ORDER BY role_slug;

-- Expected results:
-- COMPANIES (3 total):
--   - general (is_general_group = true)
--   - milwaukee
--   - warta
--
-- ROLES (5 total):
--   - admin
--   - learner
--   - manager
--   - sales-rep
--   - technician
