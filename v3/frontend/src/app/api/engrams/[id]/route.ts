import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

export async function GET(
    request: Request,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const { id: engramId } = await params;
        const supabase = await createClient();

        // Get engram details
        const { data: engram, error: engramError } = await supabase
            .from('engrams')
            .select('*')
            .eq('engram_id', engramId)
            .single();

        if (engramError || !engram) {
            return NextResponse.json({ error: 'Engram not found' }, { status: 404 });
        }

        // Get user if authenticated
        const { data: { user } } = await supabase.auth.getUser();

        let installed = false;
        let strength = 0;
        let userProgress = null;

        if (user) {
            // Check if user has installed this engram
            const { data: install } = await supabase
                .from('user_engram_installs')
                .select('*')
                .eq('user_id', user.id)
                .eq('engram_id', engramId)
                .single();

            if (install) {
                installed = true;
                strength = install.decay_percentage || 100;
                userProgress = install;
            }
        }

        return NextResponse.json({
            engram: {
                ...engram,
                installed,
                strength,
                userProgress
            }
        });

    } catch (error) {
        console.error('Get engram error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
