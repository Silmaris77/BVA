import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
    try {
        const supabase = await createClient()
        const { searchParams } = new URL(request.url)
        const limit = parseInt(searchParams.get('limit') || '100')

        // Get current user to verify authentication
        const { data: { user }, error: userError } = await supabase.auth.getUser()

        if (userError || !user) {
            return NextResponse.json(
                { error: 'Unauthorized' },
                { status: 401 }
            )
        }

        // Get current user's profile to determine their company and role
        const { data: profile } = await supabase
            .from('user_profiles')
            .select('company_id, role:user_roles(role_slug)')
            .eq('id', user.id)
            .single()

        if (!profile) {
            return NextResponse.json(
                { error: 'Profile not found' },
                { status: 404 }
            )
        }

        const userCompanyId = profile.company_id
        const userRoleSlug = Array.isArray(profile.role)
            ? (profile.role[0] as any)?.role_slug
            : (profile.role as any)?.role_slug;

        console.log('[LEADERBOARD DEBUG] User:', user.email, 'Company:', userCompanyId, 'Role:', userRoleSlug);

        // Query the leaderboard_view
        let query = supabase
            .from('leaderboard_view')
            .select('*')
            .order('rank', { ascending: true })
            .limit(limit)

        // Add filters ONLY if we have values and columns exist (standard safety)
        if (userCompanyId) {
            query = query.eq('company_id', userCompanyId)
        }

        if (userRoleSlug) {
            query = query.eq('role_slug', userRoleSlug)
        }

        const { data, error: queryError } = await query

        if (queryError) {
            console.error('[LEADERBOARD ERROR] Query failed:', queryError.message, queryError.details, queryError.hint);

            // Fallback: If filtered query fails (maybe columns missing), try unfiltered but order only
            console.log('[LEADERBOARD] Attempting fallback query without filters...');
            const { data: fallbackData, error: fallbackError } = await supabase
                .from('leaderboard_view')
                .select('*')
                .order('rank', { ascending: true })
                .limit(limit);

            if (fallbackError) {
                return NextResponse.json({ error: fallbackError.message }, { status: 500 });
            }
            return NextResponse.json(fallbackData || []);
        }

        return NextResponse.json(data || [])
    } catch (error) {
        console.error('Leaderboard API error:', error)
        return NextResponse.json(
            { error: 'Internal server error' },
            { status: 500 }
        )
    }
}
