-- 018_achievements_system.sql

-- 1. Create Achievements Definition Table
CREATE TABLE IF NOT EXISTS public.achievements (
    id TEXT PRIMARY KEY, -- e.g., 'streak_7'
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    icon TEXT NOT NULL, -- Lucide icon name
    xp_reward INTEGER DEFAULT 0,
    condition_type TEXT NOT NULL, -- 'streak', 'lesson', 'xp', 'engram', 'manual'
    condition_value INTEGER DEFAULT 0,
    category TEXT NOT NULL DEFAULT 'general', -- 'learning', 'engagement', 'mastery'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Create User Achievements Table (Unlock tracking)
CREATE TABLE IF NOT EXISTS public.user_achievements (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    achievement_id TEXT REFERENCES public.achievements(id) ON DELETE CASCADE NOT NULL,
    unlocked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, achievement_id)
);

-- 3. Enable RLS
ALTER TABLE public.achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_achievements ENABLE ROW LEVEL SECURITY;

-- 4. RLS Policies
-- Achievements are readable by everyone (public definitions)
CREATE POLICY "Achievements are viewable by everyone" 
ON public.achievements FOR SELECT 
USING (true);

-- User Achievements are readable by the owner
CREATE POLICY "Users can view own achievements" 
ON public.user_achievements FOR SELECT 
USING (auth.uid() = user_id);

-- Only system/admin can insert achievements (or via backend function)
-- For now, we allow service role insert (implicit)

-- 5. Seed Data
INSERT INTO public.achievements (id, title, description, icon, xp_reward, condition_type, condition_value, category)
VALUES
    ('first_steps', 'Pierwsze Kroki', 'Ukończ swoją pierwszą lekcję', 'Rocket', 50, 'lesson', 1, 'learning'),
    ('knowledge_seeker', 'Głód Wiedzy', 'Ukończ 5 lekcji', 'BookOpen', 100, 'lesson', 5, 'learning'),
    ('fast_learner', 'Szybki Uczeń', 'Zdobądź 500 XP', 'Zap', 50, 'xp', 500, 'mastery'),
    ('streak_3', 'Rozgrzewka', 'Utrzymaj streak przez 3 dni', 'Flame', 100, 'streak', 3, 'engagement'),
    ('streak_7', 'Tydzień Ognia', 'Utrzymaj streak przez 7 dni', 'Flame', 250, 'streak', 7, 'engagement'),
    ('engram_novice', 'Kolekcjoner', 'Zainstaluj 3 engramy', 'Brain', 50, 'engram', 3, 'mastery'),
    ('engram_master', 'Architekt Umysłu', 'Zainstaluj 10 engramów', 'Brain', 200, 'engram', 10, 'mastery'),
    ('early_bird', 'Ranny Ptaszek', 'Ukończ lekcję przed 8:00 rano', 'Sun', 50, 'manual', 1, 'engagement'),
    ('night_owl', 'Nocny Marek', 'Ukończ lekcję po 22:00', 'Moon', 50, 'manual', 1, 'engagement')
ON CONFLICT (id) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    icon = EXCLUDED.icon,
    xp_reward = EXCLUDED.xp_reward;
