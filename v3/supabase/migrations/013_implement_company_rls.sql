-- Migration: 013_implement_company_rls.sql
-- Description: Company-based Row Level Security for multi-tenant content isolation
-- Author: BrainVenture V3
-- Date: 2026-01-21

-- ============================================
-- PHASE 1: SCHEMA UPDATES
-- ============================================

-- Add company_id to content tables
ALTER TABLE engrams ADD COLUMN IF NOT EXISTS company_id UUID REFERENCES companies(id);
ALTER TABLE tools ADD COLUMN IF NOT EXISTS company_id UUID REFERENCES companies(id);
ALTER TABLE resources ADD COLUMN IF NOT EXISTS company_id UUID REFERENCES companies(id);

-- Add admin flag to user_profiles
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT false;

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_engrams_company ON engrams(company_id);
CREATE INDEX IF NOT EXISTS idx_tools_company ON tools(company_id);
CREATE INDEX IF NOT EXISTS idx_resources_company ON resources(company_id);
CREATE INDEX IF NOT EXISTS idx_user_profiles_admin ON user_profiles(is_admin) WHERE is_admin = true;

-- ============================================
-- PHASE 2: BACKFILL EXISTING DATA
-- ============================================

-- Get general company ID
DO $$
DECLARE
  general_company_id UUID;
BEGIN
  SELECT id INTO general_company_id FROM companies WHERE company_slug = 'general';
  
  -- Backfill company_id for existing content (set to general)
  UPDATE lessons SET company_id = general_company_id WHERE company_id IS NULL;
  UPDATE learning_paths SET company_id = general_company_id WHERE company_id IS NULL;
  UPDATE engrams SET company_id = general_company_id WHERE company_id IS NULL;
  UPDATE tools SET company_id = general_company_id WHERE company_id IS NULL;
  UPDATE resources SET company_id = general_company_id WHERE company_id IS NULL;
END $$;

-- ============================================
-- PHASE 3: UPDATE RLS POLICIES
-- ============================================

-- Helper function to get user's company_id
CREATE OR REPLACE FUNCTION public.user_company_id()
RETURNS UUID AS $$
  SELECT company_id FROM public.user_profiles WHERE id = auth.uid();
$$ LANGUAGE SQL SECURITY DEFINER STABLE;

-- Helper function to check if user is admin
CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS BOOLEAN AS $$
  SELECT COALESCE((SELECT is_admin FROM public.user_profiles WHERE id = auth.uid()), false);
$$ LANGUAGE SQL SECURITY DEFINER STABLE;

-- ============================================
-- LESSONS TABLE
-- ============================================

DROP POLICY IF EXISTS "Anyone can view lessons" ON lessons;

CREATE POLICY "Users can view company lessons or admins see all"
ON lessons FOR SELECT TO authenticated
USING (
  company_id = public.user_company_id()
  OR
  public.is_admin() = true
);

-- ============================================
-- LEARNING PATHS TABLE
-- ============================================

DROP POLICY IF EXISTS "Anyone can view learning paths" ON learning_paths;

CREATE POLICY "Users can view company learning paths or admins see all"
ON learning_paths FOR SELECT TO authenticated
USING (
  company_id = public.user_company_id()
  OR
  public.is_admin() = true
);

-- ============================================
-- ENGRAMS TABLE
-- ============================================

DROP POLICY IF EXISTS "Anyone can view engrams" ON engrams;

CREATE POLICY "Users can view company engrams or admins see all"
ON engrams FOR SELECT TO authenticated
USING (
  company_id = public.user_company_id()
  OR
  public.is_admin() = true
);

-- ============================================
-- TOOLS TABLE
-- ============================================

DROP POLICY IF EXISTS "Anyone can view tools" ON tools;

CREATE POLICY "Users can view company tools or admins see all"
ON tools FOR SELECT TO authenticated
USING (
  company_id = public.user_company_id()
  OR
  public.is_admin() = true
);

-- ============================================
-- RESOURCES TABLE
-- ============================================

DROP POLICY IF EXISTS "Anyone can view resources" ON resources;

CREATE POLICY "Users can view company resources or admins see all"
ON resources FOR SELECT TO authenticated
USING (
  company_id = public.user_company_id()
  OR
  public.is_admin() = true
);

-- ============================================
-- COMPANIES TABLE (for reference/lookups)
-- ============================================

ALTER TABLE companies ENABLE ROW LEVEL SECURITY;

-- Users can view their own company
CREATE POLICY "Users can view own company"
ON companies FOR SELECT TO authenticated
USING (
  id = public.user_company_id()
  OR
  public.is_admin() = true
);

-- ============================================
-- USER_PROFILES TABLE (update for leaderboard)
-- ============================================

-- Drop old policy
DROP POLICY IF EXISTS "Users can view own profile" ON user_profiles;

-- New policy: Users can view profiles from their company (for leaderboard)
CREATE POLICY "Users can view company profiles for leaderboard"
ON user_profiles FOR SELECT TO authenticated
USING (
  company_id = public.user_company_id()
  OR
  public.is_admin() = true
);

-- Users can still only update their own profile
-- (keeping existing update policy)

-- ============================================
-- LEADERBOARD VIEW
-- ============================================

-- Create a view for leaderboard that auto-filters by company
DROP VIEW IF EXISTS leaderboard_view;

CREATE VIEW leaderboard_view AS
SELECT 
  up.id as user_id,
  up.display_name,
  up.company_id,
  up.avatar_url,
  -- Calculate total XP from transactions
  COALESCE(SUM(xpt.xp_amount), 0) as total_xp,
  -- Calculate level (simple: 100 XP per level)
  FLOOR(COALESCE(SUM(xpt.xp_amount), 0) / 100.0) as level,
  -- Rank within company
  RANK() OVER (
    PARTITION BY up.company_id 
    ORDER BY COALESCE(SUM(xpt.xp_amount), 0) DESC
  ) as rank
FROM user_profiles up
LEFT JOIN user_xp_transactions xpt ON xpt.user_id = up.id
GROUP BY up.id, up.display_name, up.company_id, up.avatar_url;

-- Enable RLS on the view
ALTER VIEW leaderboard_view SET (security_barrier = true);

-- Grant access to authenticated users
GRANT SELECT ON leaderboard_view TO authenticated;

-- ============================================
-- COMMENTS
-- ============================================

COMMENT ON FUNCTION public.user_company_id() IS 'Returns the company_id of the authenticated user';
COMMENT ON FUNCTION public.is_admin() IS 'Returns true if the authenticated user has admin privileges';
COMMENT ON VIEW leaderboard_view IS 'Company-scoped leaderboard with automatic RLS filtering';

COMMENT ON COLUMN engrams.company_id IS 'Company ownership for multi-tenant isolation';
COMMENT ON COLUMN tools.company_id IS 'Company ownership for multi-tenant isolation';
COMMENT ON COLUMN resources.company_id IS 'Company ownership for multi-tenant isolation';
COMMENT ON COLUMN user_profiles.is_admin IS 'Admin flag for unrestricted content access';

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check RLS is enabled on all tables
SELECT 
  schemaname,
  tablename, 
  rowsecurity as rls_enabled
FROM pg_tables 
WHERE schemaname = 'public' 
  AND tablename IN (
    'lessons', 
    'learning_paths', 
    'engrams', 
    'tools', 
    'resources',
    'companies',
    'user_profiles'
  )
ORDER BY tablename;

-- Check policies exist
SELECT 
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename IN (
    'lessons', 
    'learning_paths', 
    'engrams', 
    'tools', 
    'resources',
    'companies',
    'user_profiles'
  )
ORDER BY tablename, policyname;

-- Verify company_id columns exist
SELECT 
  table_name,
  column_name,
  data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND column_name = 'company_id'
  AND table_name IN ('lessons', 'learning_paths', 'engrams', 'tools', 'resources')
ORDER BY table_name;

-- Check admin flag
SELECT 
  id,
  display_name,
  is_admin,
  company_id
FROM user_profiles
WHERE is_admin = true;

-- Sample leaderboard query (as authenticated user)
-- This would be filtered by RLS to show only company users
SELECT * FROM leaderboard_view ORDER BY rank LIMIT 10;
