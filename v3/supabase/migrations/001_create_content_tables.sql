-- Migration: 001_create_content_tables.sql
-- Description: Core content tables (lessons, engrams, tools)
-- Author: BrainVenture V3
-- Date: 2026-01-16

-- Enable UUID extension if not exists
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- CONTENT TABLES
-- ============================================

-- Lessons
CREATE TABLE IF NOT EXISTS lessons (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  lesson_id TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  duration_minutes INTEGER NOT NULL,
  xp_reward INTEGER NOT NULL DEFAULT 150,
  difficulty TEXT CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),
  content JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Engrams (micro-learning)
CREATE TABLE IF NOT EXISTS engrams (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  engram_id TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  lesson_id TEXT, -- Stores the lesson_id TEXT value
  lesson_uuid UUID REFERENCES lessons(id) ON DELETE SET NULL, -- Proper FK to lessons
  slides JSONB NOT NULL,
  quiz_pool JSONB NOT NULL,
  install_xp INTEGER DEFAULT 50,
  refresh_xp INTEGER DEFAULT 25,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tools
CREATE TABLE IF NOT EXISTS tools (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  tool_id TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  tier INTEGER CHECK (tier IN (1, 2, 3)),
  usage_xp INTEGER DEFAULT 50,
  config JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Resources (PDF-style references)
CREATE TABLE IF NOT EXISTS resources (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  resource_id TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  resource_type TEXT CHECK (resource_type IN ('pdf', 'table', 'guide', 'template')),
  content JSONB NOT NULL,
  download_xp INTEGER DEFAULT 10,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Drills (practice exercises)
CREATE TABLE IF NOT EXISTS drills (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  drill_id TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  drill_type TEXT CHECK (drill_type IN ('quiz', 'matching', 'scenario', 'sequencing')),
  questions JSONB NOT NULL,
  time_limit_seconds INTEGER,
  passing_score_percentage INTEGER DEFAULT 70,
  max_xp INTEGER DEFAULT 75,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_lessons_lesson_id ON lessons(lesson_id);
CREATE INDEX idx_engrams_engram_id ON engrams(engram_id);
CREATE INDEX idx_engrams_lesson_id ON engrams(lesson_id);
CREATE INDEX idx_engrams_lesson_uuid ON engrams(lesson_uuid); -- FK index
CREATE INDEX idx_tools_tool_id ON tools(tool_id);
CREATE INDEX idx_resources_resource_id ON resources(resource_id);
CREATE INDEX idx_drills_drill_id ON drills(drill_id);

-- Add updated_at triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_lessons_updated_at BEFORE UPDATE ON lessons
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_engrams_updated_at BEFORE UPDATE ON engrams
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tools_updated_at BEFORE UPDATE ON tools
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_resources_updated_at BEFORE UPDATE ON resources
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_drills_updated_at BEFORE UPDATE ON drills
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add comments
COMMENT ON TABLE lessons IS 'Main lesson content (multi-card structure)';
COMMENT ON TABLE engrams IS 'Micro-learning content with spaced repetition';
COMMENT ON TABLE tools IS 'Interactive tools (calculators, generators, simulators)';
COMMENT ON TABLE resources IS 'Reference materials (PDFs, tables, guides)';
COMMENT ON TABLE drills IS 'Practice exercises and quizzes';
