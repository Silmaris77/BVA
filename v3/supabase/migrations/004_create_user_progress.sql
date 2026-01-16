-- Migration: 004_create_user_progress.sql
-- Description: User progress tracking tables
-- Author: BrainVenture V3
-- Date: 2026-01-16

-- ============================================
-- USER PROGRESS TRACKING
-- ============================================

-- Lesson Progress
CREATE TABLE IF NOT EXISTS user_lesson_progress (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  lesson_id TEXT NOT NULL, -- Stores TEXT lesson_id for queries
  lesson_uuid UUID REFERENCES lessons(id) ON DELETE CASCADE, -- Proper FK
  
  status TEXT DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed')),
  current_card INTEGER DEFAULT 0,
  quiz_score INTEGER,
  
  started_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE,
  xp_earned INTEGER DEFAULT 0,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  UNIQUE(user_id, lesson_id)
);

-- Engram Installs
CREATE TABLE IF NOT EXISTS user_engram_installs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  engram_id TEXT NOT NULL, -- Stores TEXT engram_id
  engram_uuid UUID REFERENCES engrams(id) ON DELETE CASCADE, -- Proper FK
  
  install_count INTEGER DEFAULT 0,
  refresh_count INTEGER DEFAULT 0,
  
  last_refreshed_at TIMESTAMP WITH TIME ZONE,
  decay_percentage INTEGER DEFAULT 100 CHECK (decay_percentage >= 0 AND decay_percentage <= 100),
  next_refresh_due TIMESTAMP WITH TIME ZONE,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  UNIQUE(user_id, engram_id)
);

-- Tool Usage
CREATE TABLE IF NOT EXISTS user_tool_usage (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  tool_id TEXT NOT NULL, -- Stores TEXT tool_id
  tool_uuid UUID REFERENCES tools(id) ON DELETE CASCADE, -- Proper FK
  
  usage_count INTEGER DEFAULT 0,
  last_used_at TIMESTAMP WITH TIME ZONE,
  total_xp_earned INTEGER DEFAULT 0,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  UNIQUE(user_id, tool_id)
);

-- Drill Attempts
CREATE TABLE IF NOT EXISTS user_drill_attempts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  drill_id TEXT NOT NULL, -- Stores TEXT drill_id
  drill_uuid UUID REFERENCES drills(id) ON DELETE CASCADE, -- Proper FK
  
  score_percentage INTEGER CHECK (score_percentage >= 0 AND score_percentage <= 100),
  time_taken_seconds INTEGER,
  xp_earned INTEGER DEFAULT 0,
  
  completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- XP Transactions Log
CREATE TABLE IF NOT EXISTS user_xp_transactions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  
  source_type TEXT NOT NULL CHECK (source_type IN ('lesson', 'engram', 'tool', 'drill', 'path', 'bonus', 'manual')),
  source_id TEXT, -- lesson_id, engram_id, tool_id, drill_id, path_slug
  xp_amount INTEGER NOT NULL,
  description TEXT,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_user_lesson_progress_user ON user_lesson_progress(user_id);
CREATE INDEX idx_user_lesson_progress_lesson ON user_lesson_progress(lesson_id);
CREATE INDEX idx_user_lesson_progress_status ON user_lesson_progress(status);

CREATE INDEX idx_user_engram_installs_user ON user_engram_installs(user_id);
CREATE INDEX idx_user_engram_installs_engram ON user_engram_installs(engram_id);
CREATE INDEX idx_user_engram_installs_decay ON user_engram_installs(decay_percentage);

CREATE INDEX idx_user_tool_usage_user ON user_tool_usage(user_id);
CREATE INDEX idx_user_tool_usage_tool ON user_tool_usage(tool_id);

CREATE INDEX idx_user_drill_attempts_user ON user_drill_attempts(user_id);
CREATE INDEX idx_user_drill_attempts_drill ON user_drill_attempts(drill_id);
CREATE INDEX idx_user_drill_attempts_completed ON user_drill_attempts(completed_at);

CREATE INDEX idx_user_xp_transactions_user ON user_xp_transactions(user_id);
CREATE INDEX idx_user_xp_transactions_source ON user_xp_transactions(source_type, source_id);
CREATE INDEX idx_user_xp_transactions_created ON user_xp_transactions(created_at);

-- Add updated_at triggers
CREATE TRIGGER update_user_lesson_progress_updated_at BEFORE UPDATE ON user_lesson_progress
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_engram_installs_updated_at BEFORE UPDATE ON user_engram_installs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_tool_usage_updated_at BEFORE UPDATE ON user_tool_usage
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add comments
COMMENT ON TABLE user_lesson_progress IS 'User progress through lessons (current card, completion)';
COMMENT ON TABLE user_engram_installs IS 'Engram installations with decay tracking';
COMMENT ON TABLE user_tool_usage IS 'Tool usage statistics';
COMMENT ON TABLE user_drill_attempts IS 'Drill completion history with scores';
COMMENT ON TABLE user_xp_transactions IS 'Complete XP transaction log for auditing';

-- Function to calculate total user XP
CREATE OR REPLACE FUNCTION get_user_total_xp(user_uuid UUID)
RETURNS INTEGER AS $$
  SELECT COALESCE(SUM(xp_amount), 0)::INTEGER
  FROM user_xp_transactions
  WHERE user_id = user_uuid;
$$ LANGUAGE SQL STABLE;

COMMENT ON FUNCTION get_user_total_xp IS 'Calculate total XP for a user from transaction log';
