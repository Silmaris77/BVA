import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
    try {
        const supabase = await createClient()

        // 1. Authenticate
        const { data: { user } } = await supabase.auth.getUser()
        if (!user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        // 2. Define Range (Last 365 days)
        const endDate = new Date()
        const startDate = new Date()
        startDate.setDate(startDate.getDate() - 365)

        // 3. Fetch Transactions
        const { data: transactions, error } = await supabase
            .from('user_xp_transactions') // using standard table name from previous context
            .select('created_at, xp_amount')
            .eq('user_id', user.id)
            .gte('created_at', startDate.toISOString())
            .lte('created_at', endDate.toISOString())

        if (error) throw error

        // 4. Aggregate Data
        const dailyMap = new Map<string, number>()
        let totalXpYear = 0

        transactions?.forEach(tx => {
            const date = new Date(tx.created_at).toISOString().split('T')[0]
            const amount = tx.xp_amount || 0

            if (amount > 0) { // Only count positive XP gain
                dailyMap.set(date, (dailyMap.get(date) || 0) + amount)
                totalXpYear += amount
            }
        })

        // 5. Format for Frontend
        // We will return a sparse array, frontend fills the gaps
        const heatmap = Array.from(dailyMap.entries()).map(([date, count]) => {
            // Determine intensity level (0-4)
            // 0 = 0 XP
            // 1 = 1-50 XP
            // 2 = 51-150 XP
            // 3 = 151-300 XP
            // 4 = 300+ XP
            let level = 0
            if (count > 300) level = 4
            else if (count > 150) level = 3
            else if (count > 50) level = 2
            else if (count > 0) level = 1

            return { date, count, level }
        })

        return NextResponse.json({
            heatmap,
            total_xp_year: totalXpYear,
            active_days: heatmap.length
        })

    } catch (error) {
        console.error('Activity API Error:', error)
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
    }
}
