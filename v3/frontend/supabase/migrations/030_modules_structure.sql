-- 1. Create modules table
CREATE TABLE IF NOT EXISTS modules (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    track TEXT NOT NULL, -- 'foundation', 'professional', 'expert'
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Add module_id to lessons
ALTER TABLE lessons ADD COLUMN IF NOT EXISTS module_id UUID REFERENCES modules(id);

-- 3. Enable RLS on modules
ALTER TABLE modules ENABLE ROW LEVEL SECURITY;

-- 4. RLS Policies for modules
-- Everyone can view
CREATE POLICY "Modules are viewable by everyone" 
ON modules FOR SELECT 
USING (true);

-- Only admins can insert/update/delete (assuming admin role check logic usually handled or service role)
-- For simplicity in this script we allow authenticated for now, or match existing patterns.
-- Let's mimic the lessons policy if it exists, simplified here:
CREATE POLICY "Admins can manage modules" 
ON modules FOR ALL 
USING (
  exists (
    select 1 from user_roles ur
    inner join user_profiles up on up.role_id = ur.id
    where up.id = auth.uid() and ur.role_slug = 'admin'
  )
);

-- 5. Seed Initial Modules (Milwaukee Structure)
INSERT INTO modules (title, description, track, display_order) VALUES
('Milwaukee Foundations', 'Historia, wartości i ekosystem Milwaukee.', 'foundation', 1),
('Standard Wizyty "One Milwaukee"', 'Przygotowanie, prowadzenie rozmowy i zamknięcie.', 'foundation', 2),
('Application First Canvas', '7 kroków metodologii Application First.', 'foundation', 3),
('Współpraca & One Milwaukee', 'Współpraca między działami i cross-sell.', 'foundation', 4);

-- 6. Seed Math Module (Test)
INSERT INTO modules (title, description, track, display_order) VALUES
('Matematyka: Liczby i Działania', 'Liczby całkowite, ułamki i działania.', 'math', 1);
