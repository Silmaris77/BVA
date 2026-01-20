-- Create admin function to get all users with their profiles
CREATE OR REPLACE FUNCTION get_admin_users_list()
RETURNS TABLE (
    id UUID,
    email TEXT,
    display_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ,
    role_slug TEXT,
    role_display_name TEXT,
    company_slug TEXT,
    company_name TEXT,
    total_xp INTEGER,
    lessons_completed INTEGER,
    engrams_installed INTEGER
)
SECURITY DEFINER
SET search_path = public
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        au.id,
        au.email,
        up.display_name,
        up.avatar_url,
        au.created_at,
        ur.role_slug,
        ur.display_name as role_display_name,
        c.company_slug,
        c.name as company_name,
        COALESCE(
            (SELECT SUM(xp_amount) FROM user_xp_transactions WHERE user_id = au.id),
            0
        ) as total_xp,
        COALESCE(
            (SELECT COUNT(*) FROM user_lesson_progress WHERE user_id = au.id AND status = 'completed'),
            0
        ) as lessons_completed,
        COALESCE(
            (SELECT COUNT(*) FROM user_engram_installs WHERE user_id = au.id),
            0
        ) as engrams_installed
    FROM auth.users au
    LEFT JOIN user_profiles up ON au.id = up.id
    LEFT JOIN user_roles ur ON up.role_id = ur.id
    LEFT JOIN companies c ON up.company_id = c.id
    ORDER BY au.created_at DESC;
END;
$$;

-- Grant execute permission to authenticated users
GRANT EXECUTE ON FUNCTION get_admin_users_list() TO authenticated;
