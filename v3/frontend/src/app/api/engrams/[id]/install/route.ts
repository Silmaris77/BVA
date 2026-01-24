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

        // Check if already installed FIRST (before XP check)
        const { data: existing } = await supabase
            .from('user_engram_installs')
            .select('*')
            .eq('user_id', user.id)
            .eq('engram_id', engramId)
            .single();

        if (existing) {
            return NextResponse.json({ error: 'Already installed' }, { status: 400 });
        }

        // Get user profile to check XP
        const { data: profile, error: profileError } = await supabase
            .from('profiles')
            .select('xp, level')
            .eq('id', user.id)
            .single();

        if (profileError || !profile) {
            return NextResponse.json({ error: 'Profile not found' }, { status: 404 });
        }

        // Check if enough XP
        const installCost = engram.install_xp || 0;
        /* DEBUG: Disable XP check for testing
        if (profile.xp < installCost) {
            return NextResponse.json({
                error: 'Insufficient XP',
                required: installCost,
                current: profile.xp
            }, { status: 400 });
        }
        */

        // Deduct XP from profile
        /* DEBUG: Disable XP deduction for testing
        const { error: updateError } = await supabase
            .from('profiles')
            .update({ xp: profile.xp - installCost })
            .eq('id', user.id);

        if (updateError) {
            return NextResponse.json({ error: 'Failed to deduct XP' }, { status: 500 });
        }
        */

        // Create install record
        const { data: install, error: installError } = await supabase
            .from('user_engram_installs')
            .insert({
                user_id: user.id,
                engram_id: engramId,
                engram_uuid: engram.id,
                install_count: 1,
                refresh_count: 0,
                last_refreshed_at: new Date().toISOString(),
                decay_percentage: 100,
                next_refresh_due: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 1 day
            })
            .select()
            .single();

        if (installError) {
            console.error('Install Error Details:', {
                error: installError,
                code: installError.code,
                message: installError.message,
                details: installError.details,
                hint: installError.hint,
                userId: user.id,
                engramId: engramId,
                engramUUID: engram.id
            });

            // Rollback XP if install fails
            /* DEBUG: Disable XP rollback
            await supabase
                .from('profiles')
                .update({ xp: profile.xp })
                .eq('id', user.id);
            */

            return NextResponse.json({
                error: 'Installation failed',
                details: installError.message,
                code: installError.code
            }, { status: 500 });
        }

        // Log XP transaction
        await supabase
            .from('user_xp_transactions')
            .insert({
                user_id: user.id,
                source_type: 'engram',
                source_id: engramId,
                xp_amount: -installCost,
                description: `Installed engram: ${engram.title}`
            });

        return NextResponse.json({
            success: true,
            install,
            new_xp: profile.xp - installCost,
            engram: {
                id: engram.engram_id,
                title: engram.title,
                slides: engram.slides
            }
        });

    } catch (error) {
        console.error('Install engram error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
