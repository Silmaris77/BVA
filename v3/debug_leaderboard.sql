-- Sprawdź dane użytkowników i ich firmy/XP
SELECT 
    id, 
    display_name, 
    company_id, 
    xp 
FROM user_profiles 
ORDER BY xp DESC;

-- Sprawdź definicję widoku (opcjonalnie, ale widzę ją w pliku)
-- Sprawdź co zwraca widok obecnie
SELECT * FROM leaderboard_view ORDER BY total_xp DESC;
