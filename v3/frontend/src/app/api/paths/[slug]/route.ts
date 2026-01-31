import { createClient } from '@/lib/supabase/server';
import { NextRequest, NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

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
        let path: any = null;
        let pathError: any = null;

        // Always fetch from database (no hardcoded fallback)
        const { data, error } = await supabase
            .from('learning_paths')
            .select('*')
            .eq('path_slug', slug)
            .single();

        path = data;
        pathError = error;

        if (pathError || !path) {
            return NextResponse.json({ error: 'Path not found' }, { status: 404 });
        }

        // Parse lesson sequence to get IDs (handle both flat strings and module objects)
        const sequence = path.lesson_sequence || [];
        let lessonIds: string[] = [];
        const moduleMap = new Map<string, any>(); // Map lesson_id -> module info from JSON

        if (Array.isArray(sequence)) {
            sequence.forEach((item: any) => {
                if (typeof item === 'string') {
                    lessonIds.push(item);
                } else if (item.type === 'module' && Array.isArray(item.lessons)) {
                    item.lessons.forEach((lId: string) => {
                        lessonIds.push(lId);
                        // Store module info to attach to lesson later
                        moduleMap.set(lId, {
                            id: item.id,
                            title: item.title,
                            display_order: 0 // Default or from JSON if available
                        });
                    });
                }
            });
        }

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
                track,
                module_id,
                modules (
                    id,
                    title,
                    track,
                    display_order
                )
            `)
            .in('lesson_id', lessonIds);

        if (lessonsError) {
            console.error('Lessons fetch error:', lessonsError);
            return NextResponse.json({ error: lessonsError.message }, { status: 500 });
        }

        const allLessons = (lessons || []).map(lesson => {
            let cardCount = 0;
            try {
                if (typeof lesson.content === 'string') {
                    const parsed = JSON.parse(lesson.content);
                    cardCount = parsed.cards?.length || 0;
                } else if (lesson.content && typeof lesson.content === 'object') {
                    cardCount = (lesson.content as any).cards?.length || 0;
                }
            } catch (e) {
                console.error(`Error parsing content for lesson ${lesson.lesson_id}:`, e);
            }

            // Enrich track from module if missing
            const track = lesson.track || (lesson.modules as any)?.track || null;

            return {
                ...lesson,
                card_count: cardCount,
                track: track
            };
        });

        // DYNAMICALLY INJECT ALL LOCAL MATH LESSONS FOR MATH PATH
        if (slug === 'math-grade-7') {
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
                                track: 'Matematyka',
                                content: localLesson.content,
                                card_count: localLesson.content?.cards?.length || 0,
                                modules: [],
                                module_id: null
                            };

                            if (!allLessons.some(l => l.lesson_id === mathLesson.lesson_id)) {
                                (allLessons as any).push(mathLesson);
                            }

                            if (!lessonIds.includes(mathLesson.lesson_id)) {
                                lessonIds.push(mathLesson.lesson_id);
                            }
                        } catch (innerErr) {
                            console.error(`Error processing math file ${fileName}:`, innerErr);
                        }
                    }

                    // Maintain sort based on lesson ID number
                    lessonIds.sort((a, b) => {
                        const aNum = parseInt(a.match(/l(\d+)$/)?.[1] || '0');
                        const bNum = parseInt(b.match(/l(\d+)$/)?.[1] || '0');
                        return aNum - bNum;
                    });
                }
            } catch (err) {
                console.error('Failed to inject local math lessons for path:', err);
            }
        }

        // Sort lessons by the order in lesson_sequence
        const sortedLessons = lessonIds.map((id: string) => {
            const lesson = allLessons?.find(l => l.lesson_id === id);
            if (!lesson) return null;

            // If lesson doesn't have a module from DB relation, but we have it in JSON structure, attach it
            if (!lesson.modules && moduleMap.has(id)) {
                return {
                    ...lesson,
                    modules: moduleMap.get(id)
                };
            }
            return lesson;
        }).filter(Boolean);

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
