import { createClient } from '@/lib/supabase/server';
import { NextRequest, NextResponse } from 'next/server';
import { calculateEngramStrength, calculateNextRefreshDue, getRefreshUrgency, needsRefresh } from '@/lib/spaced-repetition';

interface RouteParams {
    params: Promise<{ id: string }>;
}

export async function GET(request: NextRequest, { params }: RouteParams) {
    try {
        const supabase = await createClient();
        const { id } = await params;

        // Fetch engram by id or engram_id
        const { data: engram, error } = await supabase
            .from('engrams')
            .select('*')
            .or(`id.eq.${id},engram_id.eq.${id}`)
            .single();

        if (error || !engram) {
            console.error('Engram fetch error:', error);
            return NextResponse.json({ error: 'Engram not found' }, { status: 404 });
        }

        // Get user if authenticated
        const { data: { user } } = await supabase.auth.getUser();

        let userProgress = null;
        if (user) {
            // Try user_engram_installs first (correct table name from migration)
            const { data: progress, error: installsError } = await supabase
                .from('user_engram_installs')
                .select('*')
                .eq('user_id', user.id)
                .or(`engram_id.eq.${engram.engram_id},engram_uuid.eq.${engram.id}`)
                .single();

            if (!installsError && progress) {
                userProgress = progress;
            } else {
                // Fallback to user_engrams
                const { data: fallbackProgress } = await supabase
                    .from('user_engrams')
                    .select('*')
                    .eq('user_id', user.id)
                    .or(`engram_id.eq.${engram.engram_id},engram_uuid.eq.${engram.id}`)
                    .single();
                userProgress = fallbackProgress;
            }
        }

        // Calculate SR data
        let strength = 0;
        let nextRefreshDue = null;
        let urgency = null;
        let needsRefreshNow = false;

        if (userProgress) {
            const lastRefreshed = userProgress.last_refreshed_at || userProgress.installed_at;
            strength = userProgress.decay_percentage !== undefined
                ? userProgress.decay_percentage
                : calculateEngramStrength(lastRefreshed);

            const refreshCount = userProgress.refresh_count || 0;
            nextRefreshDue = userProgress.next_refresh_due ||
                (lastRefreshed ? calculateNextRefreshDue(refreshCount, lastRefreshed).toISOString() : null);

            urgency = getRefreshUrgency(strength);
            needsRefreshNow = needsRefresh(strength);
        }

        // Enrich engram with user progress and SR data
        const enrichedEngram = {
            ...engram,
            installed: !!userProgress,
            strength,
            last_refreshed_at: userProgress?.last_refreshed_at || userProgress?.installed_at || null,
            next_refresh_due: nextRefreshDue,
            install_count: userProgress?.install_count || 0,
            refresh_count: userProgress?.refresh_count || 0,
            urgency,
            needs_refresh: needsRefreshNow
        };

        return NextResponse.json({ engram: enrichedEngram });

    } catch (error) {
        console.error('API error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}

export async function POST(request: NextRequest, { params }: RouteParams) {
    try {
        const supabase = await createClient();
        const { id } = await params;
        const body = await request.json();
        const { action, quiz_score } = body;

        // Get user
        const { data: { user } } = await supabase.auth.getUser();
        if (!user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        // Fetch engram
        const { data: engram, error: engramError } = await supabase
            .from('engrams')
            .select('*')
            .or(`id.eq.${id},engram_id.eq.${id}`)
            .single();

        if (engramError || !engram) {
            return NextResponse.json({ error: 'Engram not found' }, { status: 404 });
        }

        if (action === 'install') {
            const now = new Date().toISOString();

            // Try user_engram_installs first
            let existingProgress = null;
            let tableName = 'user_engram_installs';

            const { data: installProgress, error: installsError } = await supabase
                .from('user_engram_installs')
                .select('*')
                .eq('user_id', user.id)
                .or(`engram_id.eq.${engram.engram_id},engram_uuid.eq.${engram.id}`)
                .single();

            if (!installsError && installProgress) {
                existingProgress = installProgress;
            } else {
                // Fallback to user_engrams
                const { data: fallbackProgress } = await supabase
                    .from('user_engrams')
                    .select('*')
                    .eq('user_id', user.id)
                    .or(`engram_id.eq.${engram.engram_id},engram_uuid.eq.${engram.id}`)
                    .single();
                if (fallbackProgress) {
                    existingProgress = fallbackProgress;
                    tableName = 'user_engrams';
                }
            }

            if (existingProgress) {
                // Refresh - update decay_percentage and increment refresh_count
                const newRefreshCount = (existingProgress.refresh_count || 0) + 1;
                const nextRefreshDue = calculateNextRefreshDue(newRefreshCount, now).toISOString();

                await supabase
                    .from(tableName)
                    .update({
                        decay_percentage: 100,
                        last_refreshed_at: now,
                        next_refresh_due: nextRefreshDue,
                        refresh_count: newRefreshCount,
                        updated_at: now
                    })
                    .eq('id', existingProgress.id);

                // Award refresh XP
                await supabase.from('user_xp_transactions').insert({
                    user_id: user.id,
                    xp_amount: engram.refresh_xp || 25,
                    source_type: 'engram_refresh',
                    source_id: engram.id,
                    description: `Refreshed engram: ${engram.title}`
                });

                return NextResponse.json({
                    success: true,
                    type: 'refresh',
                    xp_earned: engram.refresh_xp || 25,
                    next_refresh_due: nextRefreshDue,
                    refresh_count: newRefreshCount
                });
            } else {
                // First install - calculate next refresh due (refresh_count = 0)
                const nextRefreshDue = calculateNextRefreshDue(0, now).toISOString();

                await supabase.from('user_engram_installs').insert({
                    user_id: user.id,
                    engram_id: engram.engram_id,
                    engram_uuid: engram.id,
                    installed_at: now,
                    last_refreshed_at: now,
                    decay_percentage: 100,
                    next_refresh_due: nextRefreshDue,
                    refresh_count: 0,
                    install_count: 1
                });

                // Award install XP
                await supabase.from('user_xp_transactions').insert({
                    user_id: user.id,
                    xp_amount: engram.install_xp || 50,
                    source_type: 'engram_install',
                    source_id: engram.id,
                    description: `Installed engram: ${engram.title}`
                });

                return NextResponse.json({
                    success: true,
                    type: 'install',
                    xp_earned: engram.install_xp || 50,
                    next_refresh_due: nextRefreshDue,
                    refresh_count: 0
                });
            }
        }

        return NextResponse.json({ error: 'Invalid action' }, { status: 400 });

    } catch (error) {
        console.error('API error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}

