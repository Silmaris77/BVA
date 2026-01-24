import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

export async function POST(
    request: Request,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const { id: engramId } = await params;
        const supabase = await createClient();

        // Get authenticated user
        const { data: { user }, error: authError } = await supabase.auth.getUser();
        if (authError || !user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        // Get engram details
        const { data: engram, error: engramError } = await supabase
            .from('engrams')
            .select('*')
            .eq('engram_id', engramId)
            .single();

        if (engramError || !engram) {
            return NextResponse.json({ error: 'Engram not found' }, { status: 404 });
        }

        // Get user install record
        const { data: install, error: installError } = await supabase
            .from('user_engram_installs')
            .select('*')
            .eq('user_id', user.id)
            .eq('engram_id', engramId)
            .single();

        if (installError || !install) {
            return NextResponse.json({ error: 'Engram not installed' }, { status: 404 });
        }

        // Get body (score from frontend)
        const body = await request.json();
        const { score: scorePercentage = 100 } = body; // Score percentage from frontend quiz

        // Validate score
        if (typeof scorePercentage !== 'number' || scorePercentage < 0 || scorePercentage > 100) {
            return NextResponse.json({ error: 'Invalid score' }, { status: 400 });
        }

        // Calculate XP reward based on performance and time since last refresh
        const baseXP = engram.refresh_xp || 25;
        const performanceMultiplier = scorePercentage / 100;

        // Time decay bonus (more XP if refreshed on time)
        const daysSinceRefresh = install.last_refreshed_at
            ? (Date.now() - new Date(install.last_refreshed_at).getTime()) / (1000 * 60 * 60 * 24)
            : 1;
        const timeMultiplier = Math.min(1.5, 1 + (daysSinceRefresh / 30)); // Up to 1.5x if waited 30+ days

        const xpReward = Math.round(baseXP * performanceMultiplier * timeMultiplier);

        // Calculate new decay based on refresh count (spaced repetition)
        const refreshCount = (install.refresh_count || 0) + 1;
        const intervals = [1, 3, 7, 14, 30, 60]; // days
        const nextInterval = intervals[Math.min(refreshCount, intervals.length - 1)];
        const nextRefreshDue = new Date(Date.now() + nextInterval * 24 * 60 * 60 * 1000);

        // Update install record
        const { error: updateError } = await supabase
            .from('user_engram_installs')
            .update({
                last_refreshed_at: new Date().toISOString(),
                refresh_count: refreshCount,
                decay_percentage: scorePercentage,
                next_refresh_due: nextRefreshDue.toISOString()
            })
            .eq('id', install.id);

        if (updateError) {
            return NextResponse.json({ error: 'Failed to update progress' }, { status: 500 });
        }

        // Award XP to profile
        const { data: profile } = await supabase
            .from('profiles')
            .select('xp')
            .eq('id', user.id)
            .single();

        if (profile) {
            await supabase
                .from('profiles')
                .update({ xp: profile.xp + xpReward })
                .eq('id', user.id);
        }

        // Log XP transaction
        await supabase
            .from('user_xp_transactions')
            .insert({
                user_id: user.id,
                source_type: 'engram',
                source_id: engramId,
                xp_amount: xpReward,
                description: `Refreshed engram: ${engram.title} (${scorePercentage}%)`
            });

        return NextResponse.json({
            success: true,
            score: scorePercentage,
            xp_earned: xpReward,
            new_xp: (profile?.xp || 0) + xpReward,
            next_refresh: nextRefreshDue.toISOString(),
            refresh_count: refreshCount
        });

    } catch (error) {
        console.error('Refresh engram error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
