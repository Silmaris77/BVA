import { createClient } from '@/lib/supabase/server';
import { NextRequest, NextResponse } from 'next/server';

interface RouteParams {
    params: Promise<{
        id: string;
    }>;
}

export async function GET(
    request: NextRequest,
    { params }: RouteParams
) {
    try {
        const supabase = await createClient();
        const { id: lessonId } = await params; // Next.js 15: params is Promise

        // Get user (if authenticated)
        const { data: { user: currentUser } } = await supabase.auth.getUser();

        // Get lesson details
        const { data: lesson, error: lessonError } = await supabase
            .from('lessons')
            .select('*')
            .eq('lesson_id', lessonId)
            .single();

        if (lessonError || !lesson) {
            // FALLBACK FILE SYSTEM LOADING FOR MATH LESSONS
            if (lessonId.startsWith('math-')) {
                try {
                    const fs = await import('fs');
                    const path = await import('path');
                    // math-g7-l1 -> lesson1.json
                    const filePath = path.join(process.cwd(), 'src/data/math/grade7/lesson1.json');

                    if (fs.existsSync(filePath)) {
                        const fileContent = fs.readFileSync(filePath, 'utf-8');
                        const localLesson = JSON.parse(fileContent);

                        return NextResponse.json({
                            lesson: localLesson,
                            // Dummy progress for local file
                            progress: currentUser ? {
                                status: 'not_started',
                                current_card: 0,
                                current_card_index: 0
                            } : null
                        });
                    }
                } catch (err) {
                    console.error('Local file load error:', err);
                }
            }

            // FALLBACK FILE SYSTEM LOADING FOR FUNDAMENTALS LESSON
            if (lessonId === 'sales-fundamentals-1') {
                try {
                    const fs = await import('fs');
                    const path = await import('path');
                    const filePath = path.join(process.cwd(), 'src/data/sales/lesson_fundamentals.json');

                    if (fs.existsSync(filePath)) {
                        const fileContent = fs.readFileSync(filePath, 'utf-8');
                        const localLesson = JSON.parse(fileContent);

                        return NextResponse.json({
                            lesson: localLesson,
                            progress: currentUser ? {
                                status: 'not_started',
                                current_card: 0,
                                current_card_index: 0
                            } : null
                        });
                    }
                } catch (err) {
                    console.error('Local file load error:', err);
                }
            }

            return NextResponse.json({ error: 'Lesson not found' }, { status: 404 });
        }

        // If user is authenticated, check access and get progress
        if (currentUser) {
            // TODO: Implement access control check using content_access_rules

            // Get user progress on this lesson
            const { data: progress } = await supabase
                .from('user_lesson_progress')
                .select('*')
                .eq('user_id', currentUser.id)
                .eq('lesson_id', lessonId)
                .single();

            return NextResponse.json({
                lesson,
                progress: progress ? {
                    ...progress,
                    current_card_index: progress.current_card // Map for frontend
                } : null
            });
        }

        // If not authenticated, return lesson only
        return NextResponse.json({ lesson });

    } catch (error) {
        console.error('API error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}

export async function POST(
    request: NextRequest,
    { params }: RouteParams
) {
    try {
        const supabase = await createClient();
        const { id: lessonId } = await params; // Next.js 15: params is Promise

        // Verify user is authenticated
        const { data: { user }, error: authError } = await supabase.auth.getUser();

        if (authError || !user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const body = await request.json();
        const { action } = body;

        if (action === 'start') {
            // Start lesson - create/update progress
            const { data: progress, error: progressError } = await supabase
                .from('user_lesson_progress')
                .upsert({
                    user_id: user.id,
                    lesson_id: lessonId,
                    status: 'in_progress',
                    started_at: new Date().toISOString()
                }, {
                    onConflict: 'user_id,lesson_id'
                })
                .select()
                .single();

            if (progressError) {
                console.error('Progress create error:', progressError);
                return NextResponse.json({ error: progressError.message }, { status: 500 });
            }

            return NextResponse.json({ progress });
        }

        if (action === 'complete') {
            // Get lesson to fetch XP reward
            const { data: lesson } = await supabase
                .from('lessons')
                .select('xp_reward')
                .eq('lesson_id', lessonId)
                .single();

            const xpAmount = lesson?.xp_reward || 100;

            // Mark lesson as completed
            const { data: progress, error: progressError } = await supabase
                .from('user_lesson_progress')
                .update({
                    status: 'completed',
                    completed_at: new Date().toISOString(),
                    xp_earned: xpAmount
                })
                .eq('user_id', user.id)
                .eq('lesson_id', lessonId)
                .select()
                .single();

            if (progressError) {
                console.error('Progress update error:', progressError);
                return NextResponse.json({ error: progressError.message }, { status: 500 });
            }

            // Award XP
            await supabase
                .from('user_xp_transactions')
                .insert({
                    user_id: user.id,
                    source_type: 'lesson',
                    source_id: lessonId,
                    xp_amount: xpAmount,
                    description: `Completed lesson: ${lessonId}`
                });

            // Update User Profile XP Cache
            const { data: profile } = await supabase
                .from('user_profiles')
                .select('xp')
                .eq('id', user.id)
                .single();

            const currentXp = profile?.xp || 0;

            await supabase
                .from('user_profiles')
                .update({ xp: currentXp + xpAmount })
                .eq('id', user.id);

            return NextResponse.json({ success: true, xpEarned: xpAmount, progress });
        }

        if (action === 'progress') {
            // Update current card progress
            const { current_card } = body;

            const { data: progress, error: progressError } = await supabase
                .from('user_lesson_progress')
                .update({
                    current_card: current_card,
                    status: 'in_progress'
                })
                .eq('user_id', user.id)
                .eq('lesson_id', lessonId)
                .select()
                .single();

            if (progressError) {
                console.error('Progress update error:', progressError);
                return NextResponse.json({ error: progressError.message }, { status: 500 });
            }

            return NextResponse.json({ success: true, progress });
        }

        if (action === 'reset') {
            // Reset lesson progress to not_started (or just in_progress with card 0)
            const { data: progress, error: progressError } = await supabase
                .from('user_lesson_progress')
                .update({
                    status: 'in_progress',
                    current_card: 0,
                    completed_at: null,
                    xp_earned: 0
                })
                .eq('user_id', user.id)
                .eq('lesson_id', lessonId)
                .select()
                .single();

            if (progressError) {
                console.error('Progress reset error:', progressError);
                return NextResponse.json({ error: progressError.message }, { status: 500 });
            }

            return NextResponse.json({ success: true, progress });
        }

        return NextResponse.json({ error: 'Invalid action' }, { status: 400 });

    } catch (error) {
        console.error('API error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
