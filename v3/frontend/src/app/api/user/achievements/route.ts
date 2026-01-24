import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'
import { checkAchievements } from '@/lib/badges'

export async function GET(request: Request) {
    try {
        const supabase = await createClient()
        const { data: { user } } = await supabase.auth.getUser()

        if (!user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        // Trigger a check to ensure everything is up to date
        // In a real high-scale app, this would be async/queue-based, but for MVP it's fine
        // making sure user sees latest badges when visiting profile.
        // We wrap it in a non-blocking call or just await it if we want immediate consistency.
        // Let's await to be nice.
        await checkAchievements(user.id)

        // Fetch Definitions + User Status
        const { data: achievements } = await supabase
            .from('achievements')
            .select('*')
            .order('xp_reward', { ascending: true })

        const { data: unlocked } = await supabase
            .from('user_achievements')
            .select('achievement_id, unlocked_at')
            .eq('user_id', user.id)

        // Merge
        const result = achievements?.map(a => {
            const isUnlocked = unlocked?.find(u => u.achievement_id === a.id)
            return {
                ...a,
                unlocked: !!isUnlocked,
                unlocked_at: isUnlocked?.unlocked_at || null
            }
        })

        return NextResponse.json(result || [])

    } catch (error) {
        console.error('Achievements API Error:', error)
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
    }
}
