// RPG Stats Management System
// Handles automatic updates of user stats, class unlocks, and combo detection

import { supabase } from './supabase'

// ============================================
// MAIN FUNCTION: Update User Stats
// ============================================
export async function updateUserStats(
    userId: string,
    engramId: string
): Promise<void> {
    try {
        // 1. Get engram metadata
        const { data: engram, error: engramError } = await supabase
            .from('engrams')
            .select('stat_category, stat_points, title')
            .eq('id', engramId)
            .single()

        if (engramError) throw engramError
        if (!engram?.stat_category) {
            console.log('Engram has no stat_category, skipping stat update')
            return
        }

        // 2. Get current user stat for this category
        const { data: currentStat } = await supabase
            .from('user_stats')
            .select('points, level')
            .eq('user_id', userId)
            .eq('category', engram.stat_category)
            .single()

        // 3. Calculate new points and level
        const currentPoints = currentStat?.points || 0
        const newPoints = Math.min(100, currentPoints + engram.stat_points)
        const newLevel = Math.floor(newPoints / 20) + 1 // Level 1-5 (0-20: L1, 21-40: L2, etc.)

        // 4. Upsert user_stats
        const { error: upsertError } = await supabase
            .from('user_stats')
            .upsert({
                user_id: userId,
                category: engram.stat_category,
                points: newPoints,
                level: Math.min(5, newLevel),
                updated_at: new Date().toISOString()
            })

        if (upsertError) throw upsertError

        console.log(`✅ Updated ${engram.stat_category}: ${currentPoints} → ${newPoints} (Level ${newLevel})`)

        // 5. Check for class unlocks
        await checkClassUnlocks(userId)

        // 6. Check for combo unlocks
        await checkComboUnlocks(userId)

    } catch (error) {
        console.error('Error updating user stats:', error)
        throw error
    }
}

// ============================================
// CLASS DETECTION
// ============================================
async function checkClassUnlocks(userId: string): Promise<void> {
    try {
        // Get all user stats
        const { data: stats } = await supabase
            .from('user_stats')
            .select('category, points')
            .eq('user_id', userId)

        // Get all user engrams with categories
        const { data: userEngrams } = await supabase
            .from('user_engrams')
            .select('engram_id, engrams(stat_category)')
            .eq('user_id', userId)

        if (!userEngrams) return

        // Count engrams per category
        const engramsByCategory: Record<string, number> = {}
        userEngrams.forEach((ue: { engrams: { stat_category: string } | { stat_category: string }[] | null }) => {
            // Handle array or single object from Supabase join
            const engramData = Array.isArray(ue.engrams) ? ue.engrams[0] : ue.engrams
            const category = engramData?.stat_category

            if (category) {
                engramsByCategory[category] = (engramsByCategory[category] || 0) + 1
            }
        })

        // CLASS 1: Sales Strategist (5+ Sales + 3+ Mindset)
        if ((engramsByCategory['Sales'] || 0) >= 5 && (engramsByCategory['Mindset'] || 0) >= 3) {
            await unlockClass(userId, 'Sales Strategist')
        }

        // CLASS 2: Versatile Professional (2+ engrams in ALL 6 categories)
        const categories = ['Leadership', 'Sales', 'Strategy', 'Mindset', 'Technical', 'Communication']
        const hasAllCategories = categories.every(cat => (engramsByCategory[cat] || 0) >= 2)
        if (hasAllCategories) {
            await unlockClass(userId, 'Versatile Professional')
        }

        // CLASS 3: Specialist (10+ engrams in ONE category)
        for (const [category, count] of Object.entries(engramsByCategory)) {
            if (count >= 10) {
                await unlockClass(userId, `${category} Specialist`)
            }
        }

        // CLASS 4: Learning Architect (5+ Leadership + 3+ Technical)
        if ((engramsByCategory['Leadership'] || 0) >= 5 && (engramsByCategory['Technical'] || 0) >= 3) {
            await unlockClass(userId, 'Learning Architect')
        }

    } catch (error) {
        console.error('Error checking class unlocks:', error)
    }
}

async function unlockClass(userId: string, className: string): Promise<void> {
    try {
        // Check if already unlocked
        const { data: existing } = await supabase
            .from('user_classes')
            .select('id')
            .eq('user_id', userId)
            .eq('class_name', className)
            .single()

        if (existing) {
            console.log(`Class "${className}" already unlocked`)
            return
        }

        // Unlock new class
        const { error } = await supabase
            .from('user_classes')
            .insert({
                user_id: userId,
                class_name: className,
                is_active: true
            })

        if (error) throw error
        console.log(`🏆 CLASS UNLOCKED: ${className}`)

    } catch (error) {
        console.error('Error unlocking class:', error)
    }
}

// ============================================
// COMBO DETECTION
// ============================================
async function checkComboUnlocks(userId: string): Promise<void> {
    try {
        // Get all user engrams
        const { data: userEngrams } = await supabase
            .from('user_engrams')
            .select('engram_id')
            .eq('user_id', userId)

        if (!userEngrams) return

        const userEngramIds = userEngrams.map((ue: { engram_id: string }) => ue.engram_id)

        // Get all combo definitions
        const { data: combos } = await supabase
            .from('combo_definitions')
            .select('*')

        if (!combos) return

        // Check each combo
        for (const combo of combos) {
            const requiredEngrams: string[] = combo.required_engrams as string[] || []

            // Check if user has ALL required engrams
            const hasAll = requiredEngrams.every(reqId => userEngramIds.includes(reqId))

            if (hasAll) {
                await unlockCombo(userId, combo.name)
            }
        }

    } catch (error) {
        console.error('Error checking combo unlocks:', error)
    }
}

async function unlockCombo(userId: string, comboName: string): Promise<void> {
    try {
        // Check if already unlocked
        const { data: existing } = await supabase
            .from('user_combos')
            .select('id')
            .eq('user_id', userId)
            .eq('combo_name', comboName)
            .single()

        if (existing) {
            console.log(`Combo "${comboName}" already unlocked`)
            return
        }

        // Unlock new combo
        const { error } = await supabase
            .from('user_combos')
            .insert({
                user_id: userId,
                combo_name: comboName,
                bonus_active: true
            })

        if (error) throw error
        console.log(`🔥 COMBO UNLOCKED: ${comboName}`)

    } catch (error) {
        console.error('Error unlocking combo:', error)
    }
}

// ============================================
// HELPER: Get User Stats Summary
// ============================================
export async function getUserStatsSummary(userId: string) {
    try {
        const { data: stats } = await supabase
            .from('user_stats')
            .select('*')
            .eq('user_id', userId)
            .order('category')

        const { data: classes } = await supabase
            .from('user_classes')
            .select('*')
            .eq('user_id', userId)
            .eq('is_active', true)

        const { data: combos } = await supabase
            .from('user_combos')
            .select('combo_name, unlocked_at, bonus_active')
            .eq('user_id', userId)
            .eq('bonus_active', true)

        return {
            stats: stats || [],
            classes: classes || [],
            combos: combos || []
        }
    } catch (error) {
        console.error('Error getting user stats summary:', error)
        return { stats: [], classes: [], combos: [] }
    }
}
