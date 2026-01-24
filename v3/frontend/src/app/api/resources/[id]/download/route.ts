import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function POST(
    request: Request,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const { id: resourceId } = await params
        const supabase = await createClient()

        // 1. Authenticate
        const { data: { user }, error: authError } = await supabase.auth.getUser()
        if (authError || !user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        // 2. Get Resource
        const { data: resource, error: resError } = await supabase
            .from('resources')
            .select('*')
            .eq('id', resourceId)
            .single()

        if (resError || !resource) {
            return NextResponse.json({ error: 'Resource not found' }, { status: 404 })
        }

        if (resource.locked) {
            // Check if user satisfies unlock condition (e.g. tier) - for now just block
            return NextResponse.json({ error: 'Resource is locked' }, { status: 403 })
        }

        // 3. Award XP (if eligible)
        // Check if recently downloaded/awarded to prevent spamming XP
        // specific 'resource_download' log in xp_transactions
        const { data: recentLog } = await supabase
            .from('user_xp_transactions')
            .select('*')
            .eq('user_id', user.id)
            .eq('source_id', resourceId)
            .eq('source_type', 'resource_download')
            .single()

        let xpAwarded = 0

        if (!recentLog && resource.download_xp > 0) {
            xpAwarded = resource.download_xp

            // Update Profile XP
            const { data: profile } = await supabase
                .from('profiles')
                .select('xp')
                .eq('id', user.id)
                .single()

            if (profile) {
                await supabase
                    .from('profiles')
                    .update({ xp: profile.xp + xpAwarded })
                    .eq('id', user.id)
            }

            // Log Transaction
            await supabase.from('user_xp_transactions').insert({
                user_id: user.id,
                source_type: 'resource_download',
                source_id: resourceId,
                xp_amount: xpAwarded,
                description: `Pobrano zasób: ${resource.title}`
            })
        }

        return NextResponse.json({
            success: true,
            url: resource.external_url || '#',
            xp_awarded: xpAwarded
        })

    } catch (error) {
        console.error('Download error:', error)
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
    }
}
