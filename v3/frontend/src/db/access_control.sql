-- Create resource_permissions table
CREATE TABLE IF NOT EXISTS resource_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource_id TEXT NOT NULL UNIQUE,
    allowed_roles TEXT[] DEFAULT '{}',
    allowed_companies TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE resource_permissions ENABLE ROW LEVEL SECURITY;

-- Allow read access to authenticated users
-- (Frontend needs to read permissions to decide whether to show content)
CREATE POLICY "Allow read access to authenticated users" ON resource_permissions
    FOR SELECT TO authenticated USING (true);

-- Allow full access to builders/admins (Adjust based on your admin check logic)
-- Example assuming user_roles table or metadata check
CREATE POLICY "Allow full access to admins" ON resource_permissions
    FOR ALL TO authenticated USING (
        EXISTS (
            SELECT 1 FROM user_profiles
            JOIN user_roles ON user_profiles.role_id = user_roles.id
            WHERE user_profiles.id = auth.uid()
            AND (user_roles.role_slug = 'admin' OR user_roles.role_slug = 'builder')
        )
    );

-- Initial Data for Degen Test & Atlas
INSERT INTO resource_permissions (resource_id, allowed_roles)
VALUES
    ('degen-test', ARRAY['admin', 'inwestor']),
    ('degen-atlas', ARRAY['admin', 'inwestor'])
ON CONFLICT (resource_id) DO UPDATE
SET allowed_roles = EXCLUDED.allowed_roles;
