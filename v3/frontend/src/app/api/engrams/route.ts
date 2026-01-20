import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';
import { calculateEngramStrength, calculateNextRefreshDue, getRefreshUrgency, needsRefresh } from '@/lib/spaced-repetition';

export async function GET() {
    try {
        const supabase = await createClient();

        // Get all engrams
        const { data: engrams, error } = await supabase
            .from('engrams')
            .select('*')
            .order('created_at', { ascending: true });

        if (error) {
            console.error('Engrams fetch error:', error);
            return NextResponse.json({ error: error.message }, { status: 500 });
        }

        // Get user if authenticated
        const { data: { user } } = await supabase.auth.getUser();

        let userEngramsMap: Record<string, any> = {};

        if (user) {
            // Try user_engram_installs first (correct table name from migration)
            const { data: userEngrams, error: installsError } = await supabase
                .from('user_engram_installs')
                .select('*')
                .eq('user_id', user.id);

            // Fallback to user_engrams if user_engram_installs doesn't exist
            if (installsError) {
                const { data: fallbackEngrams } = await supabase
                    .from('user_engrams')
                    .select('*')
                    .eq('user_id', user.id);

                if (fallbackEngrams) {
                    userEngramsMap = fallbackEngrams.reduce((acc, ue) => {
                        const key = ue.engram_id || ue.engram_uuid;
                        acc[key] = ue;
                        return acc;
                    }, {} as Record<string, any>);
                }
            } else if (userEngrams) {
                userEngramsMap = userEngrams.reduce((acc, ue) => {
                    const key = ue.engram_id || ue.engram_uuid;
                    acc[key] = ue;
                    return acc;
                }, {} as Record<string, any>);
            }
        }

        // Enrich engrams with user progress and spaced repetition data
        const enrichedEngrams = engrams?.map(engram => {
            const userProgress = userEngramsMap[engram.engram_id] || userEngramsMap[engram.id];

            if (!userProgress) {
                // Not installed
                return {
                    ...engram,
                    installed: false,
                    strength: 0,
                    last_refreshed_at: null,
                    next_refresh_due: null,
                    install_count: 0,
                    refresh_count: 0,
                    urgency: null,
                    needs_refresh: false
                };
            }

            // Calculate current strength based on decay
            const lastRefreshed = userProgress.last_refreshed_at || userProgress.installed_at;
            const strength = userProgress.decay_percentage !== undefined
                ? userProgress.decay_percentage
                : calculateEngramStrength(lastRefreshed);

            const refreshCount = userProgress.refresh_count || 0;
            const nextRefreshDue = userProgress.next_refresh_due ||
                (lastRefreshed ? calculateNextRefreshDue(refreshCount, lastRefreshed).toISOString() : null);

            return {
                ...engram,
                installed: true,
                strength,
                last_refreshed_at: lastRefreshed,
                next_refresh_due: nextRefreshDue,
                install_count: userProgress.install_count || 1,
                refresh_count: refreshCount,
                urgency: getRefreshUrgency(strength),
                needs_refresh: needsRefresh(strength)
            };
        });

        // Sort: urgent refreshes first, then by strength
        const sortedEngrams = enrichedEngrams?.sort((a, b) => {
            // Installed engrams needing refresh first
            if (a.needs_refresh && !b.needs_refresh) return -1;
            if (!a.needs_refresh && b.needs_refresh) return 1;
            // Then by strength (lower = more urgent)
            if (a.installed && b.installed) {
                return a.strength - b.strength;
            }
            // Installed before non-installed
            if (a.installed && !b.installed) return -1;
            if (!a.installed && b.installed) return 1;
            return 0;
        });

        return NextResponse.json({ engrams: sortedEngrams });

    } catch (error) {
        console.error('API error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}

