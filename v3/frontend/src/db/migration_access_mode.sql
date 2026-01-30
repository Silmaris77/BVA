-- Add access_mode column to user_profiles
-- 'standard' = Default mode (see all content unless explicitly locked)
-- 'whitelist' = Restrictive mode (see ONLY content with explicit permission)

ALTER TABLE user_profiles 
ADD COLUMN IF NOT EXISTS access_mode TEXT DEFAULT 'standard' CHECK (access_mode IN ('standard', 'whitelist'));

-- Update existing users to standard mode (safety)
UPDATE user_profiles SET access_mode = 'standard' WHERE access_mode IS NULL;
