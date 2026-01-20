import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'
import { isAdmin } from '@/lib/admin'

export async function GET() {
    try {
        if (!(await isAdmin())) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        const supabase = await createClient()

        const { data: companies, error } = await supabase
            .from('companies')
            .select('company_slug, name')
            .order('name')

        if (error) {
            return NextResponse.json({ error: error.message }, { status: 500 })
        }

        return NextResponse.json({ companies: companies || [] })
    } catch (error) {
        console.error('Admin companies GET error:', error)
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
    }
}
