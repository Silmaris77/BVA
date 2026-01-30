import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

export async function GET() {
    try {
        const supabase = await createClient();

        // Get all learning paths
        const { data: paths, error } = await supabase
            .from('learning_paths')
            .select('*')
            .order('created_at', { ascending: true });

        if (error) {
            console.error('Learning paths fetch error:', error);
            return NextResponse.json({ error: error.message }, { status: 500 });
        }

        // Get user progress and profile if authenticated
        const { data: { user } } = await supabase.auth.getUser();

        let pathProgressMap: Record<string, any> = {};
        let lessonProgressMap: Record<string, any> = {};
        let accessMode = 'standard';
        let userRole = '';
        let permissionsConfig: any[] = [];

        if (user) {
            // Get user's path progress
            const { data: pathProgressData } = await supabase
                .from('user_path_progress')
                .select('*')
                .eq('user_id', user.id);

            if (pathProgressData) {
                pathProgressMap = pathProgressData.reduce((acc, p) => {
                    acc[p.path_slug] = p;
                    return acc;
                }, {} as Record<string, any>);
            }

            // Get user's lesson progress to calculate path completion
            const { data: lessonProgressData } = await supabase
                .from('user_lesson_progress')
                .select('lesson_id, status')
                .eq('user_id', user.id);

            if (lessonProgressData) {
                lessonProgressMap = lessonProgressData.reduce((acc, p) => {
                    acc[p.lesson_id] = p;
                    return acc;
                }, {} as Record<string, any>);
            }

            // Get user profile for access mode and role
            try {
                const { data: profile } = await supabase
                    .from('user_profiles')
                    .select('*, role:user_roles(role_slug)')
                    .eq('id', user.id)
                    .single();

                if (profile) {
                    accessMode = profile.access_mode || 'standard';
                    userRole = profile.role?.role_slug || '';
                }

                // Get permissions config
                const { data: perms } = await supabase.from('resource_permissions').select('*');
                permissionsConfig = perms || [];

            } catch (e) {
                console.error('Error fetching profile/permissions:', e);
            }
        }

        // Enrich paths with progress data AND apply filtering
        let enrichedPaths = paths?.map(path => {
            const lessonSequence = path.lesson_sequence as string[];
            const completedLessons = lessonSequence.filter(
                lessonId => lessonProgressMap[lessonId]?.status === 'completed'
            );
            const inProgressLessons = lessonSequence.filter(
                lessonId => lessonProgressMap[lessonId]?.status === 'in_progress'
            );

            const totalLessons = lessonSequence.length;
            const completedCount = completedLessons.length;
            const progressPercent = totalLessons > 0
                ? Math.round((completedCount / totalLessons) * 100)
                : 0;

            // Determine status
            let status: 'not_started' | 'in_progress' | 'completed' = 'not_started';
            if (completedCount === totalLessons && totalLessons > 0) {
                status = 'completed';
            } else if (completedCount > 0 || inProgressLessons.length > 0) {
                status = 'in_progress';
            }

            return {
                ...path,
                lesson_count: totalLessons,
                completed_lessons: completedCount,
                progress_percent: progressPercent,
                status,
                user_progress: pathProgressMap[path.path_slug] || null
            };
        }) || [];

        // INJECT LOCAL MATH PATH
        const mathLessonId = 'math-g7-l1';
        const mathPathSlug = 'math-grade-7';

        const mathLessonSequence = [mathLessonId];
        const mathCompletedLessons = mathLessonSequence.filter(id => lessonProgressMap[id]?.status === 'completed');
        const mathInProgressLessons = mathLessonSequence.filter(id => lessonProgressMap[id]?.status === 'in_progress');
        const mathTotalLessons = mathLessonSequence.length;
        const mathCompletedCount = mathCompletedLessons.length;
        const mathProgressPercent = mathTotalLessons > 0 ? Math.round((mathCompletedCount / mathTotalLessons) * 100) : 0;

        let mathStatus: 'not_started' | 'in_progress' | 'completed' = 'not_started';
        if (mathCompletedCount === mathTotalLessons && mathTotalLessons > 0) {
            mathStatus = 'completed';
        } else if (mathCompletedCount > 0 || mathInProgressLessons.length > 0) {
            mathStatus = 'in_progress';
        }

        const localMathPath = {
            id: 'math-path-001',
            path_slug: mathPathSlug,
            title: 'Matematyka (Klasa 7)',
            description: 'Kompleksowa ścieżka edukacyjna z matematyki dla klasy 7, zgodna z podstawą programową.',
            estimated_hours: 40,
            total_xp_reward: 2000,
            difficulty: 'beginner',
            lesson_sequence: mathLessonSequence,
            lesson_count: mathTotalLessons,
            completed_lessons: mathCompletedCount,
            progress_percent: mathProgressPercent,
            status: mathStatus,
            user_progress: pathProgressMap[mathPathSlug] || null,
            is_local: true
        };

        if (!enrichedPaths.some(p => p.path_slug === mathPathSlug)) {
            enrichedPaths.unshift(localMathPath);
        }

        // Apply Access Mode Filtering
        if (accessMode === 'whitelist') {
            enrichedPaths = enrichedPaths.filter(path => {
                // Local Math path is always allowed
                if (path.path_slug === 'math-grade-7') return true;

                const config = permissionsConfig.find(p => p.resource_id === path.path_slug); // Using slug as ID

                // No config = HIDE in whitelist mode
                if (!config) return false;

                // Check role
                return config.allowed_roles.includes(userRole) || config.allowed_roles.includes('all');
            });
        }

        return NextResponse.json({ paths: enrichedPaths });

    } catch (error) {
        console.error('API error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
