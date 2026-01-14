-- Day 9 Migration: RPG Mechanics Tables
-- Creates user_stats, user_classes, user_combos, and combo_definitions tables

-- 1. user_stats - Track category-level stats for each user
CREATE TABLE IF NOT EXISTS user_stats (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('Leadership', 'Sales', 'Strategy', 'Mindset', 'Technical', 'Communication')),
    points INTEGER DEFAULT 0 CHECK (points >= 0 AND points <= 100),
    level INTEGER DEFAULT 1 CHECK (level >= 1 AND level <= 5),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    UNIQUE(user_id, category)
);

CREATE INDEX IF NOT EXISTS idx_user_stats_user ON user_stats(user_id);
CREATE INDEX IF NOT EXISTS idx_user_stats_category ON user_stats(category);

-- 2. user_classes - Track unlocked classes for each user
CREATE TABLE IF NOT EXISTS user_classes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    class_name TEXT NOT NULL,
    unlocked_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(user_id, class_name)
);

CREATE INDEX IF NOT EXISTS idx_user_classes_user ON user_classes(user_id);

-- 3. user_combos - Track unlocked synergy combos
CREATE TABLE IF NOT EXISTS user_combos (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    combo_name TEXT NOT NULL,
    unlocked_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    bonus_active BOOLEAN DEFAULT TRUE,
    UNIQUE(user_id, combo_name)
);

CREATE INDEX IF NOT EXISTS idx_user_combos_user ON user_combos(user_id);

-- 4. combo_definitions - Define available combos
CREATE TABLE IF NOT EXISTS combo_definitions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    required_engrams JSONB NOT NULL, -- Array of engram IDs
    bonus_type TEXT NOT NULL CHECK (bonus_type IN ('xp_multiplier', 'resource_unlock', 'stat_boost')),
    bonus_value JSONB NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 5. Modify engrams table - add RPG metadata
ALTER TABLE engrams ADD COLUMN IF NOT EXISTS stat_category TEXT CHECK (stat_category IN ('Leadership', 'Sales', 'Strategy', 'Mindset', 'Technical', 'Communication'));
ALTER TABLE engrams ADD COLUMN IF NOT EXISTS stat_points INTEGER DEFAULT 10 CHECK (stat_points >= 0 AND stat_points <= 50);
ALTER TABLE engrams ADD COLUMN IF NOT EXISTS prerequisites JSONB DEFAULT '[]'::jsonb;

-- 6. RLS Policies
ALTER TABLE user_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_classes ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_combos ENABLE ROW LEVEL SECURITY;
ALTER TABLE combo_definitions ENABLE ROW LEVEL SECURITY;

-- Users can read their own stats/classes/combos
CREATE POLICY "Users can read own stats" ON user_stats FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own stats" ON user_stats FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own stats" ON user_stats FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can read own classes" ON user_classes FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own classes" ON user_classes FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own classes" ON user_classes FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can read own combos" ON user_combos FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own combos" ON user_combos FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own combos" ON user_combos FOR UPDATE USING (auth.uid() = user_id);

-- Everyone can read combo definitions
CREATE POLICY "Public read combo definitions" ON combo_definitions FOR SELECT USING (true);

-- Update existing sample engram with metadata
UPDATE engrams 
SET 
    stat_category = 'Sales',
    stat_points = 15,
    prerequisites = '[]'::jsonb
WHERE title = 'Szybkie Decyzje (OODA Loop)';
