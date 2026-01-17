import { createClient } from '@/lib/supabase/server';
import { NextRequest, NextResponse } from 'next/server';

export async function GET() {
    try {
        const supabase = await createClient();

        // Get all lessons (public endpoint - access control done on individual lesson view)
        const { data: lessons, error } = await supabase
            .from('lessons')
            .select('lesson_id, title, description, duration_minutes, xp_reward, difficulty, content')
            .order('created_at', { ascending: true });

        if (error) {
            console.error('Lessons fetch error:', error);
            return NextResponse.json({ error: error.message }, { status: 500 });
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

        return NextResponse.json({ lessons, progress: progressMap });

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
