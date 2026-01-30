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

        // Apply Access Mode Filtering
        if (accessMode === 'whitelist') {
            enrichedPaths = enrichedPaths.filter(path => {
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
