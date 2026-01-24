import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
    const supabase = await createClient()

    try {
        const { data: { user } } = await supabase.auth.getUser()
        if (!user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        const today = new Date().toISOString().split('T')[0]

        // Fetch parallel basic stats
        const [profileRes, pendingEngramsRes, newsRes] = await Promise.all([
            // 1. Profile (Streak, XP handled by trigger/view usually but here raw)
            supabase
                .from('user_profiles')
                .select('current_streak')
                .eq('user_id', user.id)
                .single(),

            // 2. Pending Engrams (for mission logic approximation)
            supabase
                .from('user_engrams')
                .select('count', { count: 'exact', head: true })
                .eq('user_id', user.id)
                .lte('next_review_at', new Date().toISOString()),

            // 3. News count (for now used in bell logic)
            supabase
                .from('announcements')
                .select('count', { count: 'exact', head: true })
                .eq('is_active', true)
        ])

        // Calculate Pending Missions Count (Approximated logic to match Hub)
        // Ideally this logic should be shared, but for speed replicating basics:
        // 1. Engrams > 0 = 1 mission
        // 2. Daily XP < 100 = 1 mission (need XP query)
        // 3. Lesson = 1 mission
        // For lightness, let's return just engrams and streak for now or do 1 more query.

        // Let's add XP query to be precise
        const { data: xpData } = await supabase
            .from('xp_transactions')
            .select('amount')
            .eq('user_id', user.id)
            .gte('created_at', today)

        const currentDailyXp = xpData?.reduce((sum, tx) => sum + (tx.amount || 0), 0) || 0

        // Count pending
        let pendingMissions = 0
        if ((pendingEngramsRes.count || 0) > 0) pendingMissions++
        if (currentDailyXp < 100) pendingMissions++
        pendingMissions++ // Always have lesson mission active unless completed all (rare)

        return NextResponse.json({
            streak: profileRes.data?.current_streak || 0,
            pending_missions: pendingMissions,
            // xp: profileRes.data?.xp || 0 // Profile XP usually cached in auth session or separate
        })

    } catch (error) {
        console.error('Status API Error:', error)
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
    }
}
