-- Migration: 000_cleanup_existing_tables.sql
-- Description: Drop existing tables if migration failed midway
-- Author: BrainVenture V3
-- Date: 2026-01-16
-- Run this ONLY if you need to reset and start fresh

-- ============================================
-- CLEANUP - Run this first if re-running migrations
-- ============================================

-- Drop all tables in reverse dependency order
DROP TABLE IF EXISTS user_xp_transactions CASCADE;
DROP TABLE IF EXISTS user_drill_attempts CASCADE;
DROP TABLE IF EXISTS user_tool_usage CASCADE;
DROP TABLE IF EXISTS user_engram_installs CASCADE;
DROP TABLE IF EXISTS user_lesson_progress CASCADE;
DROP TABLE IF EXISTS user_path_progress CASCADE;
DROP TABLE IF EXISTS content_access_rules CASCADE;
DROP TABLE IF EXISTS learning_paths CASCADE;
DROP TABLE IF EXISTS drills CASCADE;
DROP TABLE IF EXISTS resources CASCADE;
DROP TABLE IF EXISTS tools CASCADE;
DROP TABLE IF EXISTS engrams CASCADE;
DROP TABLE IF EXISTS lessons CASCADE;
DROP TABLE IF EXISTS user_roles CASCADE;
DROP TABLE IF EXISTS companies CASCADE;

-- Drop functions
DROP FUNCTION IF EXISTS get_user_total_xp(UUID);
DROP FUNCTION IF EXISTS update_updated_at_column();

-- Note: This does NOT drop auth.users columns (company_id, role_id, department)
-- Those will remain and be reused
