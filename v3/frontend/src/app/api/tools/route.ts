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
                category: 'utility',
                default_xp: 50,
                config: {},
                created_at: new Date().toISOString()
            },
            {
                id: 'kolb-test-01',
                tool_id: 'kolb-test',
                title: 'Test Stylu Uczenia (Kolb)',
                description: 'Zdiagnozuj swój naturalny styl przyswajania wiedzy. Czy jesteś Aktywistą, Refleksyjnym Obserwatorem, Teoretykiem czy Pragmatykiem?',
                tier: 1,
                category: 'diagnosis',
                default_xp: 100,
                config: {},
                created_at: new Date().toISOString()
            },
            {
                id: 'degen-test',
                tool_id: 'degen-test',
                title: 'Test Typu Degena',
                description: 'Sprawdź, jakim typem inwestora jesteś naprawdę. Czy kierujesz się zimną kalkulacją, emocjami, czy może intuicją?',
                tier: 1,
                category: 'diagnosis',
                default_xp: 150,
                config: {},
                created_at: new Date().toISOString()
            },
            {
                id: 'neuroleader-test-01',
                tool_id: 'neuroleader-test',
                title: 'Profil Neuroleadera',
                description: 'Odkryj swój dominujący styl przywództwa w oparciu o neurobiologię. Poznaj swoje mocne strony w zarządzaniu zespołem.',
                tier: 2,
                category: 'diagnosis',
                default_xp: 150,
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

        // Apply Whitelist Filtering (if applicable)
        let finalTools = enrichedTools;

        if (user) {
            try {
                // Fetch user profile to check access mode and role
                const { data: profile } = await supabase
                    .from('user_profiles')
                    .select('*, role:user_roles(role_slug)')
                    .eq('id', user.id)
                    .single();

                const accessMode = profile?.access_mode || 'standard';
                const userRole = Array.isArray(profile?.role)
                    ? (profile.role[0] as any)?.role_slug
                    : (profile?.role as any)?.role_slug || '';

                console.log('[TOOLS FILTER] User:', user.email, 'AccessMode:', accessMode, 'Role:', userRole);

                if (accessMode === 'whitelist') {
                    // Fetch permissions configuration
                    const { data: permissionsConfig } = await supabase
                        .from('resource_permissions')
                        .select('resource_id, allowed_roles');

                    console.log('[TOOLS FILTER] Permissions config:', permissionsConfig);

                    // Filter tools based on permissions
                    finalTools = enrichedTools.filter((tool: any) => {
                        const config = permissionsConfig?.find((p: any) => p.resource_id === tool.tool_id || p.resource_id === tool.id);

                        console.log('[TOOLS FILTER] Checking tool:', tool.title, 'ID:', tool.tool_id || tool.id, 'Config found:', !!config);

                        // No config = HIDE in whitelist mode
                        if (!config) return false;

                        // Check if user role is allowed
                        const allowed = config.allowed_roles.includes(userRole) || config.allowed_roles.includes('all');
                        console.log('[TOOLS FILTER] Tool allowed:', allowed, 'Config roles:', config.allowed_roles);

                        // SPECIAL DEBUG for reported issues
                        if (tool.tool_id === 'degen-test' || tool.id === 'degen-test') {
                            console.log('[DEBUG DEGEN TEST] Tool ID:', tool.tool_id, 'Config roles:', config.allowed_roles, 'User Role:', userRole, 'Allowed:', allowed);
                        }

                        return allowed;
                    });

                    console.log('[TOOLS FILTER] Final tools count:', finalTools.length, 'of', enrichedTools.length);
                }
            } catch (e) {
                console.error('Error applying tool permissions:', e);
            }
        }

        return NextResponse.json({ tools: finalTools });

    } catch (error) {
        console.error('API error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
