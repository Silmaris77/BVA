-- Migration: 003_create_learning_paths.sql
-- Description: Learning paths and user progress tracking
-- Author: BrainVenture V3
-- Date: 2026-01-16

-- ============================================
-- LEARNING PATHS
-- ============================================

-- Learning Paths
CREATE TABLE IF NOT EXISTS learning_paths (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  path_slug TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  
  -- Path metadata
  estimated_hours INTEGER,
  difficulty TEXT CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),
  total_xp_reward INTEGER NOT NULL DEFAULT 0,
  
  -- Lesson sequence
  lesson_sequence JSONB NOT NULL,
  
  -- Completion requirements
  requires_all_lessons BOOLEAN DEFAULT true,
  min_lessons_required INTEGER,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Path Progress
CREATE TABLE IF NOT EXISTS user_path_progress (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  path_slug TEXT REFERENCES learning_paths(path_slug) ON DELETE CASCADE,
  
  status TEXT DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed')),
  lessons_completed TEXT[] DEFAULT ARRAY[]::TEXT[],
  
  started_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  UNIQUE(user_id, path_slug)
);

-- Create indexes
CREATE INDEX idx_learning_paths_slug ON learning_paths(path_slug);
CREATE INDEX idx_user_path_progress_user ON user_path_progress(user_id);
CREATE INDEX idx_user_path_progress_path ON user_path_progress(path_slug);
CREATE INDEX idx_user_path_progress_status ON user_path_progress(status);

-- Add updated_at trigger
CREATE TRIGGER update_learning_paths_updated_at BEFORE UPDATE ON learning_paths
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_path_progress_updated_at BEFORE UPDATE ON user_path_progress
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add comments
COMMENT ON TABLE learning_paths IS 'Curated learning paths with multiple lessons';
COMMENT ON TABLE user_path_progress IS 'User progress through learning paths';
COMMENT ON COLUMN learning_paths.lesson_sequence IS 'JSON array of lesson_ids in recommended order';
COMMENT ON COLUMN learning_paths.requires_all_lessons IS 'If false, user must complete min_lessons_required';
COMMENT ON COLUMN user_path_progress.lessons_completed IS 'Array of completed lesson_ids (flexible order)';
