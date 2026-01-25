import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'

export async function GET(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const supabase = await createClient()
        const { id: toolId } = await params
        console.log('Received tool request for ID:', toolId)

        const { data: tool, error } = await supabase
            .from('tools')
            .select('*')
            .eq('tool_id', toolId)
            .single()

        if (error || !tool) {
            // FORCE FALLBACK for debugging
            console.log('Force fallback for ID:', toolId)

            return NextResponse.json({
                tool: {
                    id: 'roi-calculator',
                    tool_id: 'roi-calculator',
                    title: 'Kalkulator ROI',
                    description: 'Interaktywne narzędzie do obliczania zwrotu z inwestycji (ROI).',
                    tier: 1,
                    default_xp: 50,
                    config: {},
                    created_at: new Date().toISOString()
                },
                debug_id: toolId
            })
        }

        return NextResponse.json({ tool })
    } catch (error) {
        console.error('Tool GET error:', error)
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
    }
}
