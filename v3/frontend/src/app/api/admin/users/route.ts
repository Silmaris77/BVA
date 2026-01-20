import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'
import { isAdmin } from '@/lib/admin'

// GET - List all users with their roles and stats
export async function GET() {
    try {
        if (!(await isAdmin())) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        const supabase = await createClient()

        // Get all users using RPC function
        const { data: users, error } = await supabase.rpc('get_admin_users_list')

        if (error) {
            console.error('RPC error:', error)
            return NextResponse.json({ error: error.message }, { status: 500 })
        }

        // Transform flat RPC data to nested structure for UI
        const transformedUsers = users?.map((user: any) => ({
            id: user.id,
            email: user.email,
            display_name: user.display_name,
            avatar_url: user.avatar_url,
            created_at: user.created_at,
            total_xp: Number(user.total_xp),
            lessons_completed: Number(user.lessons_completed),
            engrams_installed: Number(user.engrams_installed),
            user_roles: user.role_slug ? {
                role_slug: user.role_slug,
                display_name: user.role_display_name
            } : null,
            companies: user.company_slug ? {
                company_slug: user.company_slug,
                name: user.company_name
            } : null
        })) || []

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

        const supabase = await createClient()
        const body = await request.json()
        const { user_id, role_slug, company_slug } = body

        if (!user_id) {
            return NextResponse.json({ error: 'Missing user_id' }, { status: 400 })
        }

        const updates: any = {}

        if (role_slug) {
            const { data: role } = await supabase
                .from('user_roles')
                .select('id')
                .eq('role_slug', role_slug)
                .single()

            if (role) updates.role_id = role.id
        }

        if (company_slug) {
            const { data: company } = await supabase
                .from('companies')
                .select('id')
                .eq('company_slug', company_slug)
                .single()

            if (company) updates.company_id = company.id
        }

        const { data, error } = await supabase
            .from('user_profiles')
            .update(updates)
            .eq('id', user_id)
            .select()
            .single()

        if (error) {
            return NextResponse.json({ error: error.message }, { status: 500 })
        }

        return NextResponse.json({ user: data })
    } catch (error) {
        console.error('Admin users PUT error:', error)
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
    }
}
