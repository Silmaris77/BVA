import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'
import { isAdmin } from '@/lib/admin'

export async function GET() {
    try {
        if (!(await isAdmin())) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        const supabase = await createClient()

        const { data: roles, error } = await supabase
            .from('user_roles')
            .select('role_slug, display_name, description')
            .order('display_name')

        if (error) {
            return NextResponse.json({ error: error.message }, { status: 500 })
        }

        return NextResponse.json({ roles: roles || [] })
    } catch (error) {
        console.error('Admin roles GET error:', error)
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
    }
}
