import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

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
            // Get user's engram progress
            const { data: userEngrams } = await supabase
                .from('user_engrams')
                .select('*')
                .eq('user_id', user.id);

            if (userEngrams) {
                userEngramsMap = userEngrams.reduce((acc, ue) => {
                    // Match by either engram_id or engram_uuid
                    const key = ue.engram_id || ue.engram_uuid;
                    acc[key] = ue;
                    return acc;
                }, {} as Record<string, any>);
            }
        }

        // Enrich engrams with user progress
        const enrichedEngrams = engrams?.map(engram => {
            const userProgress = userEngramsMap[engram.engram_id] || userEngramsMap[engram.id];
            return {
                ...engram,
                installed: !!userProgress,
                strength: userProgress?.strength || 0,
                last_refreshed_at: userProgress?.last_refreshed_at || null,
                install_count: userProgress?.install_count || 0
            };
        });

        return NextResponse.json({ engrams: enrichedEngrams });

    } catch (error) {
        console.error('API error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
