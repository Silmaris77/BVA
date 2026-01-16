import { createClient } from '@/lib/supabase/server';
import { NextRequest, NextResponse } from 'next/server';

interface RouteParams {
    params: {
        id: string;
    };
}

export async function GET(
    request: NextRequest,
    { params }: RouteParams
) {
    try {
        const supabase = await createClient();
        const { id: lessonId } = await params; // Next.js 15: params is Promise

        // Get lesson details
        const { data: lesson, error: lessonError } = await supabase
            .from('lessons')
            .select('*')
            .eq('lesson_id', lessonId)
            .single();

        if (lessonError || !lesson) {
            return NextResponse.json({ error: 'Lesson not found' }, { status: 404 });
        }

        // Get user (if authenticated)
        const { data: { user } } = await supabase.auth.getUser();

        // If user is authenticated, check access and get progress
        if (user) {
            // TODO: Implement access control check using content_access_rules

            // Get user progress on this lesson
            const { data: progress } = await supabase
                .from('user_lesson_progress')
                .select('*')
                .eq('user_id', user.id)
                .eq('lesson_id', lessonId)
                .single();

            return NextResponse.json({
                lesson,
                progress: progress || null
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
            const { quiz_score, xp_earned } = body;

            // Mark lesson as completed
            const { data: progress, error: progressError } = await supabase
                .from('user_lesson_progress')
                .update({
                    status: 'completed',
                    completed_at: new Date().toISOString(),
                    quiz_score: quiz_score || null,
                    xp_earned: xp_earned || 0
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
                    xp_amount: xp_earned || 0,
                    description: `Completed lesson: ${lessonId}`
                });

            return NextResponse.json({ progress });
        }

        return NextResponse.json({ error: 'Invalid action' }, { status: 400 });

    } catch (error) {
        console.error('API error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
