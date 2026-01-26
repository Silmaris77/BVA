import { createClient } from '@/lib/supabase/server';
import { NextRequest, NextResponse } from 'next/server';

interface RouteParams {
    params: Promise<{
        slug: string;
    }>;
}

export async function GET(
    request: NextRequest,
    { params }: RouteParams
) {
    try {
        const supabase = await createClient();
        const { slug } = await params;

        // Get path details
        const { data: path, error: pathError } = await supabase
            .from('learning_paths')
            .select('*')
            .eq('path_slug', slug)
            .single();

        if (pathError || !path) {
            return NextResponse.json({ error: 'Path not found' }, { status: 404 });
        }

        // Get lesson IDs from the path
        const lessonIds = path.lesson_sequence || [];

        // Fetch all lessons in the path
        const { data: lessons, error: lessonsError } = await supabase
            .from('lessons')
            .select(`
                lesson_id, 
                title, 
                description, 
                duration_minutes, 
                xp_reward, 
                difficulty, 
                category, 
                content,
                module_id,
                modules (
                    id,
                    title,
                    display_order
                )
            `)
            .in('lesson_id', lessonIds);

        if (lessonsError) {
            console.error('Lessons fetch error:', lessonsError);
            return NextResponse.json({ error: lessonsError.message }, { status: 500 });
        }

        // Sort lessons by the order in lesson_sequence
        const sortedLessons = lessonIds.map((id: string) =>
            lessons?.find(l => l.lesson_id === id)
        ).filter(Boolean);

        // Get user progress if authenticated
        const { data: { user } } = await supabase.auth.getUser();

        let lessonProgressMap: Record<string, any> = {};
        let pathProgress = null;

        if (user) {
            // Get lesson progress
            const { data: progressData } = await supabase
                .from('user_lesson_progress')
                .select('lesson_id, status, completed_at, current_card')
                .eq('user_id', user.id)
                .in('lesson_id', lessonIds);

            if (progressData) {
                lessonProgressMap = progressData.reduce((acc, p) => {
                    acc[p.lesson_id] = p;
                    return acc;
                }, {} as Record<string, any>);
            }

            // Get path progress
            const { data: pathProgressData } = await supabase
                .from('user_path_progress')
                .select('*')
                .eq('user_id', user.id)
                .eq('path_slug', slug)
                .single();

            pathProgress = pathProgressData;
        }

        // Calculate progress stats
        const completedLessons = Object.values(lessonProgressMap).filter(
            (p: any) => p.status === 'completed'
        ).length;
        const totalLessons = sortedLessons.length;
        const progressPercentage = totalLessons > 0
            ? Math.round((completedLessons / totalLessons) * 100)
            : 0;

        // Find current lesson (first not completed)
        const currentLessonIndex = sortedLessons.findIndex((lesson: any) => {
            const progress = lessonProgressMap[lesson.lesson_id];
            return !progress || progress.status !== 'completed';
        });

        return NextResponse.json({
            path: {
                ...path,
                lessons: sortedLessons,
                lessonProgress: lessonProgressMap,
                stats: {
                    totalLessons,
                    completedLessons,
                    progressPercentage,
                    currentLessonIndex: currentLessonIndex >= 0 ? currentLessonIndex : totalLessons - 1,
                    totalDuration: sortedLessons.reduce((sum: number, l: any) => sum + (l.duration_minutes || 0), 0),
                    totalXP: sortedLessons.reduce((sum: number, l: any) => sum + (l.xp_reward || 0), 0)
                }
            },
            userProgress: pathProgress
        });

    } catch (error) {
        console.error('API error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
