-- Naprawa widoku Leaderboard:
-- 1. Użycie kolumny 'xp' z user_profiles (szybciej i dokładniej po naszej naprawie).
-- 2. Usunięcie 'PARTITION BY company_id' w rankingu, aby lista była spójna (brak wielu miejsc #1).

DROP VIEW IF EXISTS leaderboard_view;

CREATE VIEW leaderboard_view AS
SELECT 
  up.id as user_id,
  up.display_name,
  up.company_id,
  up.avatar_url,
  -- Używamy bezpośrednio nowej kolumny XP
  COALESCE(up.xp, 0) as total_xp,
  -- Poziom = XP / 100
  FLOOR(COALESCE(up.xp, 0) / 100.0) as level,
  -- Ranking globalny (bez podziału na grupy wewnątrz widoku)
  RANK() OVER (
    ORDER BY COALESCE(up.xp, 0) DESC
  ) as rank
FROM user_profiles up;

-- Uprawnienia dla widoku
GRANT SELECT ON leaderboard_view TO authenticated;

-- Weryfikacja
SELECT * FROM leaderboard_view ORDER BY rank LIMIT 10;
