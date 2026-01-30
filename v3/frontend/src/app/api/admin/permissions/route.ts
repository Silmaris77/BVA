import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'
import { isAdmin } from '@/lib/admin'

export async function GET() {
    try {
        if (!(await isAdmin())) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        const supabase = await createClient()
        const { data, error } = await supabase
            .from('resource_permissions')
            .select('*')
            .order('resource_id')

        if (error) throw error

        return NextResponse.json({ permissions: data })
    } catch (error: any) {
        return NextResponse.json({ error: error.message }, { status: 500 })
    }
}

export async function POST(request: NextRequest) {
    try {
        if (!(await isAdmin())) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        const body = await request.json()
        const { resource_id, allowed_roles } = body

        if (!resource_id) {
            return NextResponse.json({ error: 'Missing resource_id' }, { status: 400 })
        }

        const supabase = await createClient()

        // Upsert permission
        const { data, error } = await supabase
            .from('resource_permissions')
            .upsert({
                resource_id,
                allowed_roles,
                updated_at: new Date().toISOString()
            }, { onConflict: 'resource_id' })
            .select()
            .single()

        if (error) throw error

        return NextResponse.json({ permission: data })
    } catch (error: any) {
        return NextResponse.json({ error: error.message }, { status: 500 })
    }
}
