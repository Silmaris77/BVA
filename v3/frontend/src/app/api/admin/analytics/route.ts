import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'
import { isAdmin } from '@/lib/admin'

export async function GET() {
    try {
        if (!(await isAdmin())) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        const supabase = await createClient()

        // Total users
        const { count: totalUsers } = await supabase
            .from('user_profiles')
            .select('*', { count: 'exact', head: true })

        // Total XP awarded
        const { data: xpData } = await supabase
            .from('user_xp_transactions')
            .select('xp_amount')
        const totalXp = xpData?.reduce((sum, t) => sum + t.xp_amount, 0) || 0

        // Content stats
        const { count: totalLessons } = await supabase
            .from('lessons')
            .select('*', { count: 'exact', head: true })

        const { count: totalEngrams } = await supabase
            .from('engrams')
            .select('*', { count: 'exact', head: true })

        const { count: completedLessons } = await supabase
            .from('user_lesson_progress')
            .select('*', { count: 'exact', head: true })
            .eq('completed', true)

        const { count: installedEngrams } = await supabase
            .from('user_engram_installs')
            .select('*', { count: 'exact', head: true })

        // Top users by XP
        const { data: topUsers } = await supabase
            .from('user_xp_transactions')
            .select('user_id, xp_amount')
            .order('created_at', { ascending: false })
            .limit(100)

        const userXpMap = topUsers?.reduce((acc: any, t) => {
            acc[t.user_id] = (acc[t.user_id] || 0) + t.xp_amount
            return acc
        }, {}) || {}

        const topUsersList = Object.entries(userXpMap)
            .sort(([, a]: any, [, b]: any) => b - a)
            .slice(0, 10)
            .map(([userId, xp]) => ({ user_id: userId, total_xp: xp }))

        // Recent activity (last 7 days)
        const sevenDaysAgo = new Date()
        sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)

        const { data: recentActivity } = await supabase
            .from('user_xp_transactions')
            .select('created_at, xp_amount, source_type')
            .gte('created_at', sevenDaysAgo.toISOString())
            .order('created_at', { ascending: true })

        // Group by day
        const activityByDay = recentActivity?.reduce((acc: any, t) => {
            const day = new Date(t.created_at).toISOString().split('T')[0]
            if (!acc[day]) acc[day] = { lessons: 0, engrams: 0, total_xp: 0 }
            if (t.source_type === 'lesson') acc[day].lessons++
            if (t.source_type?.includes('engram')) acc[day].engrams++
            acc[day].total_xp += t.xp_amount
            return acc
        }, {}) || {}

        return NextResponse.json({
            overview: {
                total_users: totalUsers || 0,
                total_xp: totalXp,
                total_lessons: totalLessons || 0,
                total_engrams: totalEngrams || 0,
                completed_lessons: completedLessons || 0,
                installed_engrams: installedEngrams || 0
            },
            top_users: topUsersList,
            activity_by_day: activityByDay
        })
    } catch (error) {
        console.error('Admin analytics GET error:', error)
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
    }
}
