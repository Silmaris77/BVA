import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET() {
    try {
        const supabase = await createClient()

        const { data: resources, error } = await supabase
            .from('resources')
            .select('*')
            .order('resource_type', { ascending: true })
            .order('title', { ascending: true })

        if (error) {
            return NextResponse.json({ error: error.message }, { status: 500 })
        }

        let finalResources = resources || [];

        // Apply Whitelist Filtering (if applicable)
        const { data: { user } } = await supabase.auth.getUser();

        if (user) {
            try {
                // Fetch user profile to check access mode and role
                const { data: profile } = await supabase
                    .from('user_profiles')
                    .select('*, role:user_roles(role_slug)')
                    .eq('id', user.id)
                    .single();

                const accessMode = profile?.access_mode || 'standard';
                const userRole = Array.isArray(profile?.role)
                    ? (profile.role[0] as any)?.role_slug
                    : (profile?.role as any)?.role_slug || '';

                console.log('[RESOURCES FILTER] User:', user.email, 'AccessMode:', accessMode, 'Role:', userRole);

                if (accessMode === 'whitelist') {
                    // Fetch permissions configuration
                    const { data: permissionsConfig } = await supabase
                        .from('resource_permissions')
                        .select('resource_id, allowed_roles');

                    console.log('[RESOURCES FILTER] Permissions config:', permissionsConfig);

                    // Filter resources based on permissions
                    finalResources = finalResources.filter((resource: any) => {
                        const config = permissionsConfig?.find((p: any) => p.resource_id === resource.resource_id || p.resource_id === resource.id);

                        console.log('[RESOURCES FILTER] Checking resource:', resource.title, 'ID:', resource.resource_id || resource.id, 'Config found:', !!config);

                        // No config = HIDE in whitelist mode
                        if (!config) return false;

                        // Check if user role is allowed
                        const allowed = config.allowed_roles.includes(userRole) || config.allowed_roles.includes('all');

                        // SPECIAL DEBUG for reported issues
                        if (resource.resource_id === 'degen-atlas' || resource.id === 'degen-atlas') {
                            console.log('[DEBUG DEGEN ATLAS] ID:', resource.resource_id, 'Config roles:', config.allowed_roles, 'User Role:', userRole, 'Allowed:', allowed);
                        }

                        console.log('[RESOURCES FILTER] Resource allowed:', allowed, 'Config roles:', config.allowed_roles);
                        return allowed;
                    });

                    console.log('[RESOURCES FILTER] Final resources count:', finalResources.length, 'of', finalResources.length);
                }
            } catch (e) {
                console.error('Error applying resource permissions:', e);
            }
        }

        return NextResponse.json({ resources: finalResources })
    } catch (error) {
        console.error('Resources GET error:', error)
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
    }
}
