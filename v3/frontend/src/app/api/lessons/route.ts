import { createClient } from '@/lib/supabase/server';
import { NextRequest, NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

export async function GET() {
    try {
        const supabase = await createClient();

        // Get all modules
        const { data: modules, error: modulesError } = await supabase
            .from('modules')
            .select('id, title, description, track, display_order')
            .order('display_order');

        // Get all lessons (RLS auto-filters by company)
        let { data: lessons, error } = await supabase
            .from('lessons')
            .select('lesson_id, title, description, duration_minutes, xp_reward, difficulty, category, content, status, release_date, display_order, module, track, module_id')
            .order('display_order', { ascending: true });

        if (error || modulesError) {
            console.error('Data fetch error:', error || modulesError);
            return NextResponse.json({ error: (error || modulesError)?.message }, { status: 500 });
        }

        // Parse content and calculate card_count for each lesson
        if (lessons) {
            for (const lesson of lessons) {
                if (lesson.content && typeof lesson.content === 'string') {
                    try {
                        lesson.content = JSON.parse(lesson.content);
                    } catch (e) {
                        console.error(`Failed to parse content for lesson ${lesson.lesson_id}:`, e);
                    }
                }

                // Add card_count helper for frontend
                (lesson as any).card_count = lesson.content?.cards?.length || 0;
            }
        }

        // Get user progress if authenticated
        const { data: { user } } = await supabase.auth.getUser();

        let progressMap: Record<string, any> = {};

        if (user) {
            const { data: progressData } = await supabase
                .from('user_lesson_progress')
                .select('lesson_id, status, started_at, completed_at, current_card')
                .eq('user_id', user.id);

            if (progressData) {
                progressMap = progressData.reduce((acc, p) => {
                    acc[p.lesson_id] = {
                        ...p,
                        current_card_index: p.current_card // Map to expected frontend name
                    };
                    return acc;
                }, {} as Record<string, any>);
            }
        }

        let isAuthorizedForMath = false;
        let mathModuleId: string | null = null;

        // Find Math module ID
        const mathModule = modules?.find(m => m.title.includes('Matematyka'));
        if (mathModule) mathModuleId = mathModule.id;

        // INJECT LOCAL MATH LESSON
        // Check access control: Admin OR (Company="Szkoła" AND Role="Uczeń")
        if (user) {
            try {
                const { data: profile } = await supabase
                    .from('user_profiles')
                    .select(`
                        *,
                        company:companies(name),
                        role:user_roles(role_slug, display_name)
                    `)
                    .eq('id', user.id)
                    .single();

                if (profile) {
                    const isAdmin = profile.role?.role_slug === 'admin';
                    const isStudent = profile.company?.name === 'Szkoła' && profile.role?.display_name === 'Uczeń';

                    // Allow simple 'student' slug check too just in case
                    const isStudentSlug = profile.role?.role_slug === 'student';

                    isAuthorizedForMath = isAdmin || isStudent || (profile.company?.name === 'Szkoła' && isStudentSlug);
                }
            } catch (err) {
                console.error('Profile check error:', err);
            }
        }

        // DYNAMICALLY INJECT ALL LOCAL MATH LESSONS
        try {
            const fs = await import('fs');
            const pathTool = await import('path');
            const mathDir = pathTool.join(process.cwd(), 'src/data/math/grade7');

            if (fs.existsSync(mathDir)) {
                const files = fs.readdirSync(mathDir).filter(f => f.endsWith('.json'));

                for (const fileName of files) {
                    try {
                        const filePath = pathTool.join(mathDir, fileName);
                        const fileContent = fs.readFileSync(filePath, 'utf-8');
                        const localLesson = JSON.parse(fileContent);

                        const mathLesson = {
                            lesson_id: localLesson.lesson_id,
                            title: localLesson.title,
                            subtitle: localLesson.subtitle,
                            description: localLesson.description || "Lekcja matematyki",
                            duration_minutes: localLesson.duration_minutes || 20,
                            xp_reward: localLesson.xp_reward || 100,
                            difficulty: localLesson.difficulty || 'beginner',
                            category: 'Matematyka',
                            status: 'published',
                            display_order: parseInt(localLesson.lesson_id.match(/l(\d+)$/)?.[1] || '0'),
                            release_date: null,
                            module: 'math-grade7',
                            track: 'Matematyka',
                            content: localLesson.content,
                            module_id: mathModuleId,
                            card_count: localLesson.content?.cards?.length || 0
                        };

                        // Add to list if not already present
                        if (!lessons || !lessons.some(l => l.lesson_id === mathLesson.lesson_id)) {
                            if (lessons) {
                                (lessons as any).push(mathLesson);
                            } else {
                                (lessons as any) = [mathLesson];
                            }
                        }
                    } catch (innerErr) {
                        console.error(`Error processing math file ${fileName}:`, innerErr);
                    }
                }

                // Sort by display_order
                if (lessons) {
                    lessons.sort((a, b) => (a.display_order || 0) - (b.display_order || 0));
                }
            }
        } catch (err) {
            console.error('Failed to inject local math lessons:', err);
        }

        // ENRICH LESSONS WITH MODULE TRACK IF MISSING
        if (lessons && modules) {
            const moduleTrackMap = modules.reduce((acc, m) => {
                if (m.track) acc[m.id] = m.track;
                return acc;
            }, {} as Record<string, string>);

            for (const lesson of lessons) {
                if (!lesson.track && lesson.module_id && moduleTrackMap[lesson.module_id]) {
                    lesson.track = moduleTrackMap[lesson.module_id];
                }
            }
        }

        // Fetch dynamic permissions
        const { data: permissionsConfig } = await supabase
            .from('resource_permissions')
            .select('resource_id, allowed_roles');

        // Determine user access context + access mode
        let userRole = '';
        let accessMode = 'standard';

        if (user) {
            try {
                const { data: profile } = await supabase
                    .from('user_profiles')
                    .select('*, role:user_roles(role_slug)')
                    .eq('id', user.id)
                    .single();

                if (profile && profile.role) {
                    userRole = profile.role.role_slug;
                }

                // Get access mode (whitelist vs standard)
                accessMode = profile?.access_mode || 'standard';
            } catch (e) { /* ignore */ }
        }

        // Apply permissions based on access mode
        let finalLessons = [];
        let finalModules = modules;

        if (accessMode === 'whitelist') {
            console.log('🔒 WHITELIST MODE ACTIVE for user:', user?.id)
            console.log('User role:', userRole)
            console.log('Total lessons before filter:', lessons?.length)
            console.log('Permissions config:', permissionsConfig)

            // WHITELIST MODE: Show ONLY explicitly allowed content
            finalLessons = lessons?.filter((lesson: any) => {
                // Local Math lesson is always allowed
                if (lesson.lesson_id === 'math-g7-l1') return true;

                const config = permissionsConfig?.find((p: any) => p.resource_id === lesson.lesson_id);

                // No config = HIDE
                if (!config) {
                    console.log(`❌ No config for ${lesson.lesson_id} - HIDING`)
                    return false;
                }

                // Has config, check if user role is allowed
                const isAllowed = config.allowed_roles.includes(userRole) || config.allowed_roles.includes('all');
                console.log(`Lesson ${lesson.lesson_id}: allowed_roles=${JSON.stringify(config.allowed_roles)}, userRole=${userRole}, isAllowed=${isAllowed}`)
                return isAllowed;
            }).map((lesson: any) => ({ ...lesson, is_locked: false })) || [];

            console.log('✅ Final lessons count:', finalLessons.length)

            // WHITELIST MODE: Filter modules too
            // WHITELIST MODE: Filter modules too
            finalModules = modules?.filter((module: any) => {
                // Check direct module permission
                const moduleConfig = permissionsConfig?.find((p: any) => p.resource_id === module.id);
                // Check parent track permission (fallback)
                const trackConfig = module.track ? permissionsConfig?.find((p: any) => p.resource_id === module.track) : null;

                const config = moduleConfig || trackConfig;

                // No config = HIDE
                if (!config) return false;

                // Has config, check if user role is allowed
                const isAllowed = config.allowed_roles.includes(userRole) || config.allowed_roles.includes('all');
                return isAllowed;
            }) || [];

        } else {
            // STANDARD MODE: Show all, lock restricted content
            finalLessons = lessons?.map((lesson: any) => {
                // Local Math lesson is always allowed
                if (lesson.lesson_id === 'math-g7-l1') return { ...lesson, is_locked: false };

                const config = permissionsConfig?.find((p: any) => p.resource_id === lesson.lesson_id);

                // No config = ALLOW
                if (!config) return { ...lesson, is_locked: false };

                const isAllowed = config.allowed_roles.includes(userRole) || config.allowed_roles.includes('admin');

                if (!isAllowed) {
                    // Return locked lesson without content
                    const { content, ...safeLesson } = lesson;
                    return { ...safeLesson, is_locked: true, content: null };
                }

                return { ...lesson, is_locked: false };
            }) || [];
        }

        // Also process injected Math lesson (if applicable)
        // ... (existing math logic or skipping) ...

        return NextResponse.json({ lessons: finalLessons, modules: finalModules, progress: progressMap });

    } catch (error) {
        console.error('API error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}

export async function POST(request: NextRequest) {
    try {
        const supabase = await createClient();

        // Verify user is authenticated (only admins should create lessons)
        const { data: { user }, error: authError } = await supabase.auth.getUser();

        if (authError || !user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        // TODO: Check if user is admin
        // For now, allow any authenticated user

        const body = await request.json();
        const { lesson_id, title, description, duration_minutes, xp_reward, difficulty, content } = body;

        // Validate required fields
        if (!lesson_id || !title || !content) {
            return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
        }

        // Insert lesson
        const { data: lesson, error: insertError } = await supabase
            .from('lessons')
            .insert({
                lesson_id,
                title,
                description,
                duration_minutes: duration_minutes || 30,
                xp_reward: xp_reward || 150,
                difficulty: difficulty || 'beginner',
                content
            })
            .select()
            .single();

        if (insertError) {
            console.error('Lesson insert error:', insertError);
            return NextResponse.json({ error: insertError.message }, { status: 500 });
        }

        return NextResponse.json({ lesson }, { status: 201 });

    } catch (error) {
        console.error('API error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
