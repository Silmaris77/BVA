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

        // Query the leaderboard_view
        // RLS automatically filters to user's company
        const { data, error } = await supabase
            .from('leaderboard_view')
            .select('*')
            .order('rank', { ascending: true })
            .limit(limit)

        if (error) {
            console.error('Leaderboard query error:', error)
            return NextResponse.json(
                { error: error.message },
                { status: 500 }
            )
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
