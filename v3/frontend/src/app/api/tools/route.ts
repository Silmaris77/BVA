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
            // Get user's tool usage
            const { data: userTools } = await supabase
                .from('user_tools')
                .select('*')
                .eq('user_id', user.id);

            if (userTools) {
                userToolsMap = userTools.reduce((acc, ut) => {
                    const key = ut.tool_id || ut.tool_uuid;
                    acc[key] = ut;
                    return acc;
                }, {} as Record<string, any>);
            }
        }

        // Enrich tools with user progress
        const enrichedTools = tools?.map(tool => {
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
