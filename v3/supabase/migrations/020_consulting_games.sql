-- Migration: 020_consulting_games.sql
-- Description: Sets up tables for "Dream Team Consulting" game (V3 Port)
-- Includes: Game State (JSONB), Global Market, Auctions, Shared Talent Pool.

-- 1. Game State (Player's Save Data)
CREATE TABLE IF NOT EXISTS public.consulting_games (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE UNIQUE,
    state JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS: Users can only see/edit their own game
ALTER TABLE public.consulting_games ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own game"
    ON public.consulting_games FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own game"
    ON public.consulting_games FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own game"
    ON public.consulting_games FOR INSERT
    WITH CHECK (auth.uid() = user_id);


-- 2. Global Contracts (The Market & Templates)
CREATE TABLE IF NOT EXISTS public.consulting_contracts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    is_global BOOLEAN DEFAULT FALSE, -- TRUE = Competitive Market, FALSE = Template/Personal
    
    title TEXT NOT NULL,
    description TEXT,
    difficulty TEXT DEFAULT 'Easy', -- Easy, Medium, Hard, Expert
    topic TEXT, -- Strategy, IT, HR, Finance
    
    requirements JSONB DEFAULT '{}'::jsonb, -- { "min_reputation": 50, "required_skills": ["analysis"] }
    reward JSONB DEFAULT '{}'::jsonb, -- { "coins": 1000, "reputation": 5 }
    
    -- Real-time mechanics
    expires_at TIMESTAMPTZ, -- When the contract disappears from market
    claimed_by UUID REFERENCES auth.users(id), -- If taken by a user
    
    -- Auction mechanics
    auction_end TIMESTAMPTZ, -- If NOT NULL, this is an active auction
    current_high_bid INT DEFAULT 0,
    high_bidder UUID REFERENCES auth.users(id),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS: Public can view, but only System/Admin (or Server Action) can insert/update generally
-- For now, we allow read-all for authenticated users
ALTER TABLE public.consulting_contracts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Authenticated users can view contracts"
    ON public.consulting_contracts FOR SELECT
    TO authenticated
    USING (true);


-- 3. Bids (Live Auctions History)
CREATE TABLE IF NOT EXISTS public.consulting_bids (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_id UUID NOT NULL REFERENCES public.consulting_contracts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    amount INT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS: Users see their own bids, maybe all bids for transparency?
-- Let's allow viewing all bids for "Live Ticker" feature
ALTER TABLE public.consulting_bids ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Authenticated users can view bids"
    ON public.consulting_bids FOR SELECT
    TO authenticated
    USING (true);


-- 4. Shared Talent Pool (Global Employees)
CREATE TABLE IF NOT EXISTS public.consulting_employees_market (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    avatar_url TEXT,
    
    role TEXT NOT NULL, -- Analyst, Manager, Expert
    specialty TEXT NOT NULL, -- Strategy, Finance, IT, etc.
    
    skills JSONB DEFAULT '{}'::jsonb, -- { "analysis": 5, "negotiation": 2 }
    salary_req INT NOT NULL, -- Daily cost
    
    hired_by UUID REFERENCES auth.users(id), -- NULL = Available on market
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS: Market valid
ALTER TABLE public.consulting_employees_market ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Authenticated users can view employees"
    ON public.consulting_employees_market FOR SELECT
    TO authenticated
    USING (true);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_consulting_games_user ON public.consulting_games(user_id);
CREATE INDEX IF NOT EXISTS idx_contracts_claimed ON public.consulting_contracts(claimed_by);
CREATE INDEX IF NOT EXISTS idx_contracts_global ON public.consulting_contracts(is_global);
CREATE INDEX IF NOT EXISTS idx_employees_hired ON public.consulting_employees_market(hired_by);
