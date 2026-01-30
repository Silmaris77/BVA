-- ROLLBACK: Restore original RPC function without access_mode
DROP FUNCTION IF EXISTS get_admin_users_list();

CREATE OR REPLACE FUNCTION get_admin_users_list()
RETURNS TABLE (
    id UUID,
    email TEXT,
    display_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ,
    total_xp BIGINT,
    lessons_completed BIGINT,
    engrams_installed BIGINT,
    role_slug TEXT,
    role_display_name TEXT,
    company_slug TEXT,
    company_name TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        up.id,
        up.email,
        up.display_name,
        up.avatar_url,
        up.created_at,
        up.total_xp,
        up.lessons_completed,
        up.engrams_installed,
        ur.role_slug,
        ur.display_name AS role_display_name,
        c.company_slug,
        c.name AS company_name
    FROM user_profiles up
    LEFT JOIN user_roles ur ON up.role_id = ur.id
    LEFT JOIN companies c ON up.company_id = c.id
    ORDER BY up.created_at DESC;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
