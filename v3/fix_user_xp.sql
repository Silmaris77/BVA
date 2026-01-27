-- Skrypt naprawczy: Synchronizacja XP użytkownika z historią transakcji
-- Cel: Naprawienie błędnego stanu XP (0 XP) + DODANIE brakującej kolumny 'xp' w user_profiles.

BEGIN;

-- 0. Dodaj brakującą kolumnę 'xp' do user_profiles (jeśli nie istnieje)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user_profiles' AND column_name = 'xp') THEN
        ALTER TABLE user_profiles ADD COLUMN xp INTEGER DEFAULT 0;
    END IF;
END $$;

-- 1. Upewnij się, że ukończone lekcje mają wpis w transakcjach
-- Jeśli brakuje transakcji dla ukończonej lekcji, dodaj ją (naprawa wsteczna)
INSERT INTO user_xp_transactions (user_id, source_type, source_id, xp_amount, description, created_at)
SELECT 
    ulp.user_id,
    'lesson',
    ulp.lesson_id,
    COALESCE(ulp.xp_earned, l.xp_reward, 0), -- Użyj xp_earned z progresu lub domyślnego z lekcji
    'Ukończono lekcję (naprawa): ' || COALESCE(l.title, ulp.lesson_id),
    ulp.completed_at
FROM 
    user_lesson_progress ulp
LEFT JOIN 
    lessons l ON ulp.lesson_id = l.lesson_id
WHERE 
    ulp.status = 'completed'
    AND NOT EXISTS (
        SELECT 1 FROM user_xp_transactions uxt 
        WHERE uxt.user_id = ulp.user_id 
        AND uxt.source_id = ulp.lesson_id
        AND uxt.source_type = 'lesson'
    );

-- 2. Przelicz całkowite XP dla każdego użytkownika na podstawie transakcji
WITH CalculatedXP AS (
    SELECT 
        user_id, 
        COALESCE(SUM(xp_amount), 0) as total_xp
    FROM 
        user_xp_transactions
    GROUP BY 
        user_id
)
UPDATE user_profiles
SET xp = CalculatedXP.total_xp
FROM CalculatedXP
WHERE user_profiles.id = CalculatedXP.user_id;

COMMIT;

-- Weryfikacja
SELECT id, display_name, xp FROM user_profiles;
