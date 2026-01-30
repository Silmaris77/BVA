-- Add allowed_users column to resource_permissions
ALTER TABLE resource_permissions 
ADD COLUMN IF NOT EXISTS allowed_users UUID[] DEFAULT '{}';

-- Update simple read policy is fine as structure changes but policy remains allow-read
-- Just in case we need to refresh schema cache in Supabase
