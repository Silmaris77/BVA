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

        return NextResponse.json({ resources: resources || [] })
    } catch (error) {
        console.error('Resources GET error:', error)
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
    }
}
