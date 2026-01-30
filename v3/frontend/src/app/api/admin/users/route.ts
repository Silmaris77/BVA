import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'
import { isAdmin } from '@/lib/admin'

// GET - List all users with their roles and stats
export async function GET() {
    try {
        console.log('1. Admin users API called')

        if (!(await isAdmin())) {
            console.log('2. Not admin - unauthorized')
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        console.log('3. Admin check passed')
        const supabase = await createClient()
        console.log('4. Supabase client created')

        // Direct query - note: email is in auth.users, not user_profiles
        const { data: profiles, error: profilesError } = await supabase
            .from('user_profiles')
            .select(`
                id, display_name, avatar_url, created_at, access_mode,
                user_roles(role_slug, display_name),
                companies(company_slug, name)
            `)
            .order('created_at', { ascending: false })

        console.log('5. Profiles query executed', { profilesCount: profiles?.length, error: profilesError })

        if (profilesError) {
            console.error('Profiles query error:', profilesError)
            return NextResponse.json({ error: profilesError.message }, { status: 500 })
        }

        // Fetch emails from auth.users using Service Role
        const { createClient: createSupabaseClient } = await import('@supabase/supabase-js');
        const supabaseAdmin = createSupabaseClient(
            process.env.NEXT_PUBLIC_SUPABASE_URL!,
            process.env.SUPABASE_SERVICE_ROLE_KEY!,
            {
                auth: {
                    persistSession: false,
                    autoRefreshToken: false,
                    detectSessionInUrl: false
                }
            }
        );

        const { data: { users: authUsers }, error: authError } = await supabaseAdmin.auth.admin.listUsers()

        console.log('6. Auth users fetched', { count: authUsers?.length, error: authError })

        const emailMap = new Map(authUsers?.map(u => [u.id, u.email]) || [])

        // Transform to expected format
        const transformedUsers = profiles?.map((profile: any) => ({
            id: profile.id,
            email: emailMap.get(profile.id) || 'unknown@example.com',
            display_name: profile.display_name,
            avatar_url: profile.avatar_url,
            created_at: profile.created_at,
            total_xp: 0,
            lessons_completed: 0,
            engrams_installed: 0,
            user_roles: profile.user_roles || null,
            companies: profile.companies || null,
            access_mode: profile.access_mode || 'standard'
        })) || []

        console.log('6. Returning', transformedUsers.length, 'users')
        return NextResponse.json({ users: transformedUsers })
    } catch (error) {
        console.error('Admin users GET error:', error)
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
    }
}

// PUT - Update user role or company
export async function PUT(request: NextRequest) {
    try {
        if (!(await isAdmin())) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        // Use Service Role to bypass RLS for updating other users
        const { createClient: createSupabaseClient } = await import('@supabase/supabase-js');
        const supabaseAdmin = createSupabaseClient(
            process.env.NEXT_PUBLIC_SUPABASE_URL!,
            process.env.SUPABASE_SERVICE_ROLE_KEY!,
            {
                auth: {
                    persistSession: false,
                    autoRefreshToken: false,
                    detectSessionInUrl: false
                }
            }
        );

        const body = await request.json()
        const { user_id, role_slug, company_slug, access_mode } = body

        if (!user_id) {
            return NextResponse.json({ error: 'Missing user_id' }, { status: 400 })
        }

        const updates: any = {}

        // Handle Role
        if (role_slug === "") {
            updates.role_id = null;
        } else if (role_slug) {
            const { data: role } = await supabaseAdmin
                .from('user_roles')
                .select('id')
                .eq('role_slug', role_slug)
                .single()

            if (role) updates.role_id = role.id
        }

        // Handle Company
        if (company_slug === "") {
            updates.company_id = null;
        } else if (company_slug) {
            const { data: company } = await supabaseAdmin
                .from('companies')
                .select('id')
                .eq('company_slug', company_slug)
                .single()

            if (company) updates.company_id = company.id
        }

        // Handle Access Mode
        if (access_mode && ['standard', 'whitelist'].includes(access_mode)) {
            updates.access_mode = access_mode;
        }

        const { data, error } = await supabaseAdmin
            .from('user_profiles')
            .update(updates)
            .eq('id', user_id)
            .select()
            .single()

        if (error) {
            console.error('Update error:', error);
            return NextResponse.json({ error: error.message }, { status: 500 })
        }

        return NextResponse.json({ user: data })
    } catch (error) {
        console.error('Admin users PUT error:', error)
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
    }
}
