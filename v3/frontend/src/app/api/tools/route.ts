import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

export async function GET() {
    try {
        const supabase = await createClient();

        // Get all tools
        const { data: tools, error } = await supabase
            .from('tools')
            .select('*')
            .order('tier', { ascending: true })
            .order('created_at', { ascending: true });

        if (error) {
            console.error('Tools fetch error:', error);
            return NextResponse.json({ error: error.message }, { status: 500 });
        }

        // Get user if authenticated
        const { data: { user } } = await supabase.auth.getUser();

        let userToolsMap: Record<string, any> = {};

        if (user) {
            // Get user's tool usage from new table
            const { data: usageData } = await supabase
                .from('user_tool_usage')
                .select('tool_id, created_at')
                .eq('user_id', user.id);

            if (usageData) {
                // Aggregate usage by tool_id
                userToolsMap = usageData.reduce((acc, usage) => {
                    const tid = usage.tool_id;
                    if (!acc[tid]) {
                        acc[tid] = { usage_count: 0, last_used_at: null };
                    }
                    acc[tid].usage_count++;
                    if (!acc[tid].last_used_at || new Date(usage.created_at) > new Date(acc[tid].last_used_at)) {
                        acc[tid].last_used_at = usage.created_at;
                    }
                    return acc;
                }, {} as Record<string, any>);
            }
        }

        // Default tools (Fallback)
        const defaultTools = [
            {
                id: 'roi-calculator', // Placeholder UUID
                tool_id: 'roi-calculator',
                title: 'Kalkulator ROI',
                description: 'Interaktywne narzędzie do obliczania zwrotu z inwestycji (ROI) oraz progu rentowności (BEP). Idealne do pokazywania wartości finansowej klientowi.',
                tier: 1,
                default_xp: 50,
                config: {},
                created_at: new Date().toISOString()
            }
        ];

        // Combine DB tools with default tools (prefer DB if exists)
        const dbTools = tools || [];
        const mergedTools = [...dbTools];

        // Add defaults if they don't exist in DB
        defaultTools.forEach(dt => {
            if (!mergedTools.find(t => t.tool_id === dt.tool_id)) {
                mergedTools.push(dt);
            }
        });

        // Enrich tools with user progress
        const enrichedTools = mergedTools.map(tool => {
            const userProgress = userToolsMap[tool.tool_id] || userToolsMap[tool.id];
            return {
                ...tool,
                unlocked: !!userProgress,
                usage_count: userProgress?.usage_count || 0,
                last_used_at: userProgress?.last_used_at || null
            };
        });

        return NextResponse.json({ tools: enrichedTools });

    } catch (error) {
        console.error('API error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
