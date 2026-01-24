// Achievement System Logic
import { supabase } from './supabase'

/**
 * Check and award achievements for a user based on their stats
 * Should be called after significant events (lesson complete, xp gain, etc.)
 */
export async function checkAchievements(userId: string) {
    console.log('Checking achievements for:', userId)

    try {
        // 1. Fetch User Stats
        const { data: profile } = await supabase
            .from('user_profiles')
            .select('current_streak, level, xp')
            .eq('id', userId)
            .single()

        const { count: lessonsCompleted } = await supabase
            .from('user_progress')
            .select('*', { count: 'exact', head: true })
            .eq('user_id', userId)
            .not('completed_at', 'is', null)

        const { count: engramCount } = await supabase
            .from('user_engrams')
            .select('*', { count: 'exact', head: true })
            .eq('user_id', userId)
        const currentStreak = profile?.current_streak || 0
        const currentXp = profile?.xp || 0
        const currentEngrams = engramCount || 0

        // 2. Fetch All Achievements
        const { data: allAchievements } = await supabase
            .from('achievements')
            .select('*')

        if (!allAchievements) return

        // 3. Fetch User's Unlocked Achievements
        const { data: unlocked } = await supabase
            .from('user_achievements')
            .select('achievement_id')
            .eq('user_id', userId)

        const unlockedIds = new Set(unlocked?.map((u: { achievement_id: string }) => u.achievement_id))
        const newUnlocks: string[] = []

        // 4. Check Conditions
        for (const achievement of allAchievements) {
            if (unlockedIds.has(achievement.id)) continue

            let qualified = false
            const target = achievement.condition_value

            switch (achievement.condition_type) {
                case 'streak':
                    qualified = currentStreak >= target
                    break
                case 'lesson':
                    qualified = lessonsCompleted >= target
                    break
                case 'xp':
                    qualified = currentXp >= target
                    break
                case 'engram':
                    qualified = currentEngrams >= target
                    break
                // 'manual' type is skipped here, handled by specific events
            }

            if (qualified) {
                newUnlocks.push(achievement.id)
            }
        }

        // 5. Award New Achievements
        if (newUnlocks.length > 0) {
            console.log('🏆 Unlocking achievements:', newUnlocks)

            const insertData = newUnlocks.map(id => ({
                user_id: userId,
                achievement_id: id
            }))

            const { error } = await supabase
                .from('user_achievements')
                .insert(insertData)

            if (error) console.error('Error unlocking achievements:', error)

            // Optional: Send notification or XP reward here (if not handled by insert trigger)
            // For MVP we just insert.
        }

    } catch (error) {
        console.error('Error in checkAchievements:', error)
    }
}
