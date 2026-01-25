-- 11. TOOLS (Interactive Toolkit)
CREATE TABLE IF NOT EXISTS tools (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  tool_id TEXT NOT NULL UNIQUE, -- e.g. 'roi-calculator'
  title TEXT NOT NULL,
  description TEXT,
  tier INTEGER DEFAULT 1,
  default_xp INTEGER DEFAULT 10,
  config JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- RLS for tools
ALTER TABLE tools ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read tools" ON tools FOR SELECT USING (true);

-- 12. USER TOOL USAGE (Tracking & Persistence)
CREATE TABLE IF NOT EXISTS user_tool_usage (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) NOT NULL,
  tool_id TEXT REFERENCES tools(tool_id) NOT NULL, -- references external_id
  input_data JSONB, -- Saved state (e.g. price=10000)
  output_data JSONB, -- Calculated result (e.g. roi=150)
  xp_awarded INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Index for fast lookup of user's tool usage
CREATE INDEX IF NOT EXISTS idx_user_tool_usage_user ON user_tool_usage(user_id);
CREATE INDEX IF NOT EXISTS idx_user_tool_usage_tool ON user_tool_usage(tool_id);

-- RLS for usage
ALTER TABLE user_tool_usage ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can insert own tool usage" ON user_tool_usage FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can read own tool usage" ON user_tool_usage FOR SELECT USING (auth.uid() = user_id);
