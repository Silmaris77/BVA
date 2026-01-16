-- Migration: 002_create_multi_tenancy.sql
-- Description: Multi-tenancy tables (companies, roles, access control)
-- Author: BrainVenture V3
-- Date: 2026-01-16

-- ============================================
-- MULTI-TENANCY & ACCESS CONTROL
-- ============================================

-- Companies
CREATE TABLE IF NOT EXISTS companies (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  company_slug TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  logo_url TEXT,
  is_general_group BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Roles
CREATE TABLE IF NOT EXISTS user_roles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  role_slug TEXT UNIQUE NOT NULL,
  display_name TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Seed default company and role
INSERT INTO companies (company_slug, name, is_general_group) 
VALUES ('general', 'General Access', true)
ON CONFLICT (company_slug) DO NOTHING;

INSERT INTO user_roles (role_slug, display_name, description)
VALUES ('learner', 'Learner', 'Default role for new users')
ON CONFLICT (role_slug) DO NOTHING;

-- User Profiles (instead of modifying auth.users)
-- This table extends user data with company/role info
CREATE TABLE IF NOT EXISTS user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  company_id UUID REFERENCES companies(id),
  role_id UUID REFERENCES user_roles(id),
  department TEXT,
  
  -- Additional profile fields
  display_name TEXT,
  avatar_url TEXT,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create trigger to auto-create profile on user signup
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
DROP FUNCTION IF EXISTS create_user_profile();

CREATE OR REPLACE FUNCTION create_user_profile()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.user_profiles (id, company_id, role_id)
  VALUES (
    NEW.id,
    (SELECT id FROM public.companies WHERE company_slug = 'general'),
    (SELECT id FROM public.user_roles WHERE role_slug = 'learner')
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION create_user_profile();

-- Content Access Rules
CREATE TABLE IF NOT EXISTS content_access_rules (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  content_type TEXT NOT NULL CHECK (content_type IN ('lesson', 'engram', 'tool', 'resource', 'drill', 'path')),
  content_id TEXT NOT NULL,
  
  -- Access filters (ALL must match, NULL = no restriction)
  allowed_companies UUID[],
  allowed_roles UUID[],
  required_departments TEXT[],
  
  min_xp_required INTEGER DEFAULT 0,
  prerequisite_lessons TEXT[],
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Ensure unique rule per content
  UNIQUE(content_type, content_id)
);

-- Create indexes
CREATE INDEX idx_companies_slug ON companies(company_slug);
CREATE INDEX idx_user_roles_slug ON user_roles(role_slug);
CREATE INDEX idx_user_profiles_company ON user_profiles(company_id);
CREATE INDEX idx_user_profiles_role ON user_profiles(role_id);
CREATE INDEX idx_access_rules_content ON content_access_rules(content_type, content_id);
CREATE INDEX idx_access_rules_companies ON content_access_rules USING GIN(allowed_companies);
CREATE INDEX idx_access_rules_roles ON content_access_rules USING GIN(allowed_roles);

-- Enable RLS on user_profiles
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Users can view their own profile
CREATE POLICY "Users can view own profile"
  ON user_profiles FOR SELECT
  USING (auth.uid() = id);

-- Users can update their own display_name and avatar
CREATE POLICY "Users can update own profile"
  ON user_profiles FOR UPDATE
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- Add updated_at trigger for user_profiles
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add comments
COMMENT ON TABLE companies IS 'Organizations using the platform (Milwaukee, Ryobi, etc.)';
COMMENT ON TABLE user_roles IS 'User roles (sales-rep, manager, technician, learner)';
COMMENT ON TABLE user_profiles IS 'User profile data including company and role assignments';
COMMENT ON TABLE content_access_rules IS 'Content access control (company/role/xp/prerequisites)';
COMMENT ON COLUMN companies.is_general_group IS 'TRUE for the default general access company';
COMMENT ON COLUMN user_profiles.company_id IS 'User company assignment (defaults to general)';
COMMENT ON COLUMN user_profiles.role_id IS 'User role assignment (defaults to learner)';
