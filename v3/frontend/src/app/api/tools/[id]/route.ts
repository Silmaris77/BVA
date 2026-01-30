import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'

export async function GET(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const supabase = await createClient();
        const { id: toolId } = await params;
        console.log('Received tool request for ID:', toolId);

        // Check for user's last usage FIRST (before tool lookup)
        let lastUsage = null;
        const { data: { user } } = await supabase.auth.getUser();

        if (user) {
            const meta = user.user_metadata || {};

            if (meta.tool_history && meta.tool_history[toolId]) {
                const saved = meta.tool_history[toolId];
                lastUsage = {
                    output_data: saved.last_result,
                    created_at: saved.timestamp
                };
            }
        }

        const { data: tool, error } = await supabase
            .from('tools')
            .select('*')
            .eq('tool_id', toolId)
            .single();

        if (error || !tool) {
            console.log('Force fallback for ID:', toolId);

            let fallbackTool;

            if (toolId === 'kolb-test') {
                fallbackTool = {
                    id: 'kolb-test-01',
                    tool_id: 'kolb-test',
                    title: 'Test Stylu Uczenia (Kolb)',
                    description: 'Zdiagnozuj swój naturalny styl przyswajania wiedzy.',
                    tier: 1,
                    default_xp: 100,
                    config: {},
                    created_at: new Date().toISOString()
                };
            } else if (toolId === 'degen-test') {
                fallbackTool = {
                    id: 'degen-test-01',
                    tool_id: 'degen-test',
                    title: 'Test Typu Degena',
                    description: 'Sprawdź, jakim typem inwestora jesteś naprawdę. Czy kierujesz się zimną kalkulacją, emocjami, czy może intuicją?',
                    tier: 1,
                    default_xp: 150,
                    config: {},
                    created_at: new Date().toISOString()
                };
            } else if (toolId === 'neuroleader-test') {
                fallbackTool = {
                    id: 'neuroleader-test-01',
                    tool_id: 'neuroleader-test',
                    title: 'Profil Neuroleadera',
                    description: 'Odkryj swój dominujący styl przywództwa.',
                    tier: 2,
                    default_xp: 150,
                    config: {},
                    created_at: new Date().toISOString()
                };
            } else {
                fallbackTool = {
                    id: 'roi-calculator',
                    tool_id: 'roi-calculator',
                    title: 'Kalkulator ROI',
                    description: 'Interaktywne narzędzie do obliczania zwrotu z inwestycji (ROI).',
                    tier: 1,
                    default_xp: 50,
                    config: {},
                    created_at: new Date().toISOString()
                };
            }

            return NextResponse.json({
                tool: fallbackTool,
                lastUsage,
                debug_id: toolId
            });
        }

        return NextResponse.json({ tool, lastUsage });
    } catch (error) {
        console.error('Tool GET error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
