import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'

export async function GET(
    request: NextRequest,
    { params }: { params: { id: string } }
) {
    try {
        const supabase = await createClient()
        const toolId = params.id

        const { data: tool, error } = await supabase
            .from('tools')
            .select('*')
            .eq('tool_id', toolId)
            .single()

        if (error || !tool) {
            return NextResponse.json({ error: 'Tool not found' }, { status: 404 })
        }

        return NextResponse.json({ tool })
    } catch (error) {
        console.error('Tool GET error:', error)
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
    }
}
