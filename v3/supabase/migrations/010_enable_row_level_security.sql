-- Migration: 010_enable_row_level_security.sql
-- Description: Enable Row Level Security on all user-related tables
-- Author: BrainVenture V3
-- Date: 2026-01-18

-- Note: user_profiles already has RLS enabled in migration 002

-- ============================================
-- ENABLE RLS ON USER PROGRESS TABLES
-- ============================================

-- User Lesson Progress
ALTER TABLE user_lesson_progress ENABLE ROW LEVEL SECURITY;

-- User Engrams
ALTER TABLE user_engrams ENABLE ROW LEVEL SECURITY;

-- User Path Progress
ALTER TABLE user_path_progress ENABLE ROW LEVEL SECURITY;

-- User XP Transactions
ALTER TABLE user_xp_transactions ENABLE ROW LEVEL SECURITY;

-- ============================================
-- RLS POLICIES FOR USER_LESSON_PROGRESS
-- ============================================

-- Users can only view their own progress
DROP POLICY IF EXISTS "Users can view own lesson progress" ON user_lesson_progress;
CREATE POLICY "Users can view own lesson progress"
ON user_lesson_progress FOR SELECT
USING (auth.uid() = user_id);

-- Users can insert their own progress
DROP POLICY IF EXISTS "Users can insert own lesson progress" ON user_lesson_progress;
CREATE POLICY "Users can insert own lesson progress"
ON user_lesson_progress FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can update their own progress
DROP POLICY IF EXISTS "Users can update own lesson progress" ON user_lesson_progress;
CREATE POLICY "Users can update own lesson progress"
ON user_lesson_progress FOR UPDATE
USING (auth.uid() = user_id);

-- ============================================
-- RLS POLICIES FOR USER_ENGRAMS
-- ============================================

DROP POLICY IF EXISTS "Users can view own engrams" ON user_engrams;
CREATE POLICY "Users can view own engrams"
ON user_engrams FOR SELECT
USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert own engrams" ON user_engrams;
CREATE POLICY "Users can insert own engrams"
ON user_engrams FOR INSERT
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update own engrams" ON user_engrams;
CREATE POLICY "Users can update own engrams"
ON user_engrams FOR UPDATE
USING (auth.uid() = user_id);

-- ============================================
-- RLS POLICIES FOR USER_PATH_PROGRESS
-- ============================================

DROP POLICY IF EXISTS "Users can view own path progress" ON user_path_progress;
CREATE POLICY "Users can view own path progress"
ON user_path_progress FOR SELECT
USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert own path progress" ON user_path_progress;
CREATE POLICY "Users can insert own path progress"
ON user_path_progress FOR INSERT
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update own path progress" ON user_path_progress;
CREATE POLICY "Users can update own path progress"
ON user_path_progress FOR UPDATE
USING (auth.uid() = user_id);

-- ============================================
-- RLS POLICIES FOR USER_XP_TRANSACTIONS
-- ============================================

DROP POLICY IF EXISTS "Users can view own xp transactions" ON user_xp_transactions;
CREATE POLICY "Users can view own xp transactions"
ON user_xp_transactions FOR SELECT
USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert own xp transactions" ON user_xp_transactions;
CREATE POLICY "Users can insert own xp transactions"
ON user_xp_transactions FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Note: Users typically cannot update XP transactions (immutable audit log)

-- ============================================
-- PUBLIC CONTENT TABLES (Read-only for all authenticated users)
-- ============================================

-- Lessons - public read
ALTER TABLE lessons ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Anyone can view lessons" ON lessons;
CREATE POLICY "Anyone can view lessons"
ON lessons FOR SELECT
TO authenticated
USING (true);

-- Engrams - public read
ALTER TABLE engrams ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Anyone can view engrams" ON engrams;
CREATE POLICY "Anyone can view engrams"
ON engrams FOR SELECT
TO authenticated
USING (true);

-- Tools - public read
ALTER TABLE tools ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Anyone can view tools" ON tools;
CREATE POLICY "Anyone can view tools"
ON tools FOR SELECT
TO authenticated
USING (true);

-- Learning Paths - public read
ALTER TABLE learning_paths ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Anyone can view learning paths" ON learning_paths;
CREATE POLICY "Anyone can view learning paths"
ON learning_paths FOR SELECT
TO authenticated
USING (true);

-- Resources - public read
ALTER TABLE resources ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Anyone can view resources" ON resources;
CREATE POLICY "Anyone can view resources"
ON resources FOR SELECT
TO authenticated
USING (true);

-- ============================================
-- VERIFICATION
-- ============================================

-- Check RLS is enabled
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN (
  'user_lesson_progress', 
  'user_engrams', 
  'user_path_progress',
  'user_xp_transactions',
  'user_profiles',
  'lessons',
  'engrams',
  'tools',
  'learning_paths'
);

