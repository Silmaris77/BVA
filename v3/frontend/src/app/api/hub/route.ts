import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
    const supabase = await createClient()

    try {
        const { data: { user } } = await supabase.auth.getUser()
        if (!user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        // 1. Streak Logic
        const today = new Date().toISOString().split('T')[0] // YYYY-MM-DD

        // Fetch current profile
        const { data: profile } = await supabase
            .from('user_profiles')
            .select('current_streak, last_activity_date, longest_streak')
            .eq('user_id', user.id)
            .single()

        let newStreak = profile?.current_streak || 0
        let lastActivity = profile?.last_activity_date ? new Date(profile.last_activity_date).toISOString().split('T')[0] : null
        let updatedNeeded = false

        if (lastActivity === today) {
            // Already active today, do nothing to streak
        } else {
            updatedNeeded = true
            // Check if yesterday
            const yesterday = new Date()
            yesterday.setDate(yesterday.getDate() - 1)
            const yesterdayStr = yesterday.toISOString().split('T')[0]

            if (lastActivity === yesterdayStr) {
                // Consecutive day
                newStreak++
            } else {
                // Missed a day (or first time)
                newStreak = 1
            }
        }

        // Update profile if needed (async, don't await blocking)
        if (updatedNeeded) {
            const { error: updateError } = await supabase
                .from('user_profiles')
                .update({
                    current_streak: newStreak,
                    last_activity_date: new Date().toISOString(),
                    longest_streak: Math.max(newStreak, profile?.longest_streak || 0)
                })
                .eq('user_id', user.id)

            if (updateError) console.error('Streak update failed:', updateError)
        }

        // 2. Fetch Aggregated Data in Parallel
        const [newsRes, tipsRes, progressRes, xpRes, engramsRes, installedEngramsRes] = await Promise.all([
            // A. Announcements (Active, newest first, limit 3)
            supabase
                .from('announcements')
                .select('*')
                .eq('is_active', true)
                .order('created_at', { ascending: false })
                .limit(3),

            // B. Daily Tip
            supabase
                .from('daily_tips')
                .select('*')
                .limit(10),

            // C. Last Active Lesson (Resume)
            supabase
                .from('user_progress')
                .select('lesson_id, current_card_index, updated_at, lessons(title)')
                .eq('user_id', user.id)
                .is('completed_at', null)
                .order('updated_at', { ascending: false })
                .limit(1)
                .maybeSingle(),

            // D. Today's XP (for Daily Goal)
            supabase
                .from('xp_transactions')
                .select('amount')
                .eq('user_id', user.id)
                .gte('created_at', today),

            // E. Pending Engrams (Review)
            supabase
                .from('user_engrams')
                .select('count', { count: 'exact', head: true })
                .eq('user_id', user.id)
                .lte('next_review_at', new Date().toISOString()),

            // F. Total Installed Engrams (Mastered/Learned count)
            supabase
                .from('user_engram_installs')
                .select('count', { count: 'exact', head: true })
                .eq('user_id', user.id)
        ])

        // Process Tip
        const tips = tipsRes.data || []
        const randomTip = tips.length > 0 ? tips[Math.floor(Math.random() * tips.length)] : null

        // Process Missions
        const dailyXpGoal = 100
        const currentDailyXp = xpRes.data?.reduce((sum, tx) => sum + (tx.amount || 0), 0) || 0
        const engramsCount = engramsRes.count || 0
        const totalEngrams = installedEngramsRes.count || 0

        // Slot 1: Next Lesson
        let lessonMission = null
        if (progressRes.data) {
            lessonMission = {
                id: 'lesson',
                icon: 'GraduationCap',
                title: `Kontynuuj: ${progressRes.data.lessons?.title || 'Lekcja'}`,
                meta: 'Dokończ rozpoczętą lekcję (+50 XP)',
                progress: 50 // TODO: Calculate accurate progress percentage if possible
            }
        } else {
            // Find next available lesson? For now generic fallback
            lessonMission = {
                id: 'lesson_new',
                icon: 'GraduationCap',
                title: 'Rozpocznij nową lekcję',
                meta: 'Wybierz dowolną z katalogu (+100 XP)',
                progress: 0
            }
        }

        const missions = [
            lessonMission,
            {
                id: 'daily_xp',
                icon: 'Trophy',
                title: 'Cel Dnia: Zdobądź XP',
                meta: `${currentDailyXp}/${dailyXpGoal} XP zdobyte dzisiaj`,
                progress: Math.min((currentDailyXp / dailyXpGoal) * 100, 100)
            },
            {
                id: 'engrams',
                icon: 'Brain',
                title: 'Powtórki Engramów',
                meta: engramsCount > 0 ? `${engramsCount} do powtórki` : 'Wszystko zaliczone! (+20 XP)',
                progress: engramsCount > 0 ? 0 : 100
            }
        ]

        // Response structure
        return NextResponse.json({
            streak: {
                current: newStreak,
                updated: updatedNeeded
            },
            news: newsRes.data || [],
            daily_tip: randomTip,
            resume_lesson: progressRes.data ? {
                lesson_id: progressRes.data.lesson_id,
                title: progressRes.data.lessons?.title || 'Lekcja',
                progress_index: progressRes.data.current_card_index
            } : null,
            messages: [], // messages removed? Wait, no messages here.
            missions: missions,
            total_engrams: totalEngrams
        })

    } catch (error) {
        console.error('Hub API Error:', error)
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
    }
}
