import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'

export async function GET(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const supabase = await createClient()
        const { id: resourceId } = await params

        const { data: resource, error } = await supabase
            .from('resources')
            .select('*')
            .eq('resource_id', resourceId)
            .single()

        if (error || !resource) {
            return NextResponse.json({ error: 'Resource not found' }, { status: 404 })
        }

        return NextResponse.json({ resource })
    } catch (error) {
        console.error('Resource GET error:', error)
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
    }
}
