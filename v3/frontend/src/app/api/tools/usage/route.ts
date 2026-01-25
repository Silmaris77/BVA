import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function POST(request: Request) {
    const supabase = await createClient()

    // 1. Check Auth
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) {
        return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    try {
        const body = await request.json()
        const { tool_id, input_data, output_data } = body

        if (!tool_id) {
            return NextResponse.json({ error: 'Missing tool_id' }, { status: 400 })
        }

        // 2. Fetch Tool Info (to get default XP)
        const { data: tool, error: toolError } = await supabase
            .from('tools')
            .select('default_xp')
            .eq('tool_id', tool_id)
            .single()

        if (toolError) {
            // If tool not found in DB, fallback gracefully or error. 
            // We'll proceed with 0 XP or default if DB entry missing, 
            // but strictly we should expect it.
            console.error('Tool not found:', toolError)
        }

        const xpReward = tool?.default_xp || 0

        // 3. Record Usage
        const { error: usageError } = await supabase
            .from('user_tool_usage')
            .insert({
                user_id: user.id,
                tool_id: tool_id,
                input_data,
                output_data,
                xp_awarded: xpReward
            })

        if (usageError) {
            console.error('Usage Error:', usageError)
            return NextResponse.json({ error: 'Failed to record usage' }, { status: 500 })
        }

        // 4. Award XP (only if > 0)
        let newXpTotal = -1
        let levelUp = false

        if (xpReward > 0) {
            // Get current profile
            const { data: profile } = await supabase
                .from('profiles')
                .select('xp, level')
                .eq('id', user.id)
                .single()

            if (profile) {
                const currentXp = profile.xp || 0
                const nextXp = currentXp + xpReward

                // Simple level logic (e.g. 1000 XP per level) - keep consistent with other endpoints
                // Assuming levels are calculated on frontend or simple storage
                // For now just update XP
                const { error: updateError } = await supabase
                    .from('profiles')
                    .update({ xp: nextXp })
                    .eq('id', user.id)

                if (!updateError) {
                    newXpTotal = nextXp
                }
            }
        }

        return NextResponse.json({
            success: true,
            xp_awarded: xpReward,
            new_total_xp: newXpTotal
        })

    } catch (error) {
        console.error('API Error:', error)
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
    }
}
