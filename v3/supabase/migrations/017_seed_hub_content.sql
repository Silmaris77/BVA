-- ==========================================
-- Hub & Engagement System Migration
-- ==========================================

-- 1. Extend user_profiles for Streak Tracking
ALTER TABLE user_profiles 
ADD COLUMN IF NOT EXISTS current_streak INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS longest_streak INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS last_activity_date TIMESTAMP WITH TIME ZONE;

-- 2. Announcements table (News Feed)
CREATE TABLE IF NOT EXISTS announcements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  type TEXT CHECK (type IN ('info', 'alert', 'success', 'warning')) DEFAULT 'info',
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  expires_at TIMESTAMP WITH TIME ZONE
);

-- Enable RLS for announcements
ALTER TABLE announcements ENABLE ROW LEVEL SECURITY;

-- Policy: Everyone can read active announcements
CREATE POLICY "Announcements are viewable by everyone" 
ON announcements FOR SELECT 
USING (is_active = true);

-- 3. Daily Tips table (Pigułka wiedzy)
CREATE TABLE IF NOT EXISTS daily_tips (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  category TEXT DEFAULT 'general',
  author TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS for daily_tips
ALTER TABLE daily_tips ENABLE ROW LEVEL SECURITY;

-- Policy: Everyone can read tips
CREATE POLICY "Tips are viewable by everyone" 
ON daily_tips FOR SELECT 
USING (true);

-- ==========================================
-- SEED DATA
-- ==========================================

-- Seed Announcements
INSERT INTO announcements (title, content, type, expires_at) VALUES
(
  'Witaj w nowej wersji BVA! 🚀', 
  'Cieszymy się, że jesteś z nami. Sprawdź nowe lekcje o Milwaukee i system Engramów. Twoja opinia jest dla nas kluczowa!', 
  'success',
  NOW() + INTERVAL '30 days'
),
(
  'Nowy moduł: Techniki Sprzedaży', 
  'Już wkrótce udostępnimy zaawansowany moduł o technikach negocjacji. Bądź czujny!', 
  'info',
  NOW() + INTERVAL '14 days'
),
(
  'Przerwa techniczna', 
  'W najbliższy wtorek w godzinach 2:00 - 4:00 planujemy aktualizację bazy danych. Przepraszamy za utrudnienia.', 
  'warning',
  NOW() + INTERVAL '7 days'
);

-- Seed Daily Tips
INSERT INTO daily_tips (content, category, author) VALUES
('Klienci kupują korzyści, nie cechy. Zamiast mówić "bateria 5Ah", powiedz "pracujesz cały dzień na jednym ładowaniu".', 'sales', 'Brian Tracy'),
('Engramy najskuteczniej utrwalają się, gdy powtarzasz wiedzę tuż przed snem. Mózg konsoliduje pamięć w nocy.', 'neuroscience', 'Andrew Huberman'),
('System M18 jest w pełni kompatybilny wstecznie. Bateria z dzisiaj pasuje do narzędzia sprzed 10 lat.', 'product', 'Milwaukee Tech'),
('Zadawanie pytań otwartych zwiększa szansę na sprzedaż o 40%. Pozwól klientowi opowiedzieć o swoim problemie.', 'sales', 'SPIN Selling'),
('Milwaukee jako pierwsze wprowadziło technologię litowo-jonową do elektronarzędzi w 2005 roku.', 'history', 'BVA Facts');

-- ==========================================
-- VERIFICATION
-- ==========================================
SELECT count(*) as announcements_count FROM announcements;
SELECT count(*) as tips_count FROM daily_tips;
