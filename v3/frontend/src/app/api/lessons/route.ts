import { createClient } from '@/lib/supabase/server';
import { NextRequest, NextResponse } from 'next/server';

export async function GET() {
    try {
        const supabase = await createClient();

        // Get all modules
        const { data: modules, error: modulesError } = await supabase
            .from('modules')
            .select('id, title, description, track, display_order')
            .order('display_order');

        // Get all lessons (RLS auto-filters by company)
        const { data: lessons, error } = await supabase
            .from('lessons')
            .select('lesson_id, title, description, duration_minutes, xp_reward, difficulty, category, content, status, release_date, display_order, module, track, module_id')
            .order('display_order', { ascending: true });

        if (error || modulesError) {
            console.error('Data fetch error:', error || modulesError);
            return NextResponse.json({ error: (error || modulesError)?.message }, { status: 500 });
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

        if (isAuthorizedForMath) {
            try {
                const fs = await import('fs');
                const path = await import('path');
                const filePath = path.join(process.cwd(), 'src/data/math/grade7/lesson1.json');

                if (fs.existsSync(filePath)) {
                    const fileContent = fs.readFileSync(filePath, 'utf-8');
                    const localLesson = JSON.parse(fileContent);

                    // Add metadata required for list view
                    const mathLesson = {
                        lesson_id: localLesson.lesson_id,
                        title: localLesson.title,
                        description: localLesson.subtitle || "Lekcja matematyki",
                        duration_minutes: 15,
                        xp_reward: localLesson.xp_reward || 50,
                        difficulty: 'beginner',
                        category: 'Matematyka',
                        status: 'published',
                        display_order: 0,
                        release_date: null,
                        module: 'math-grade7',
                        track: 'math',
                        content: localLesson.content, // Include content or not depending on payload size
                        module_id: mathModuleId
                    };

                    // Add to beginning or end
                    lessons?.unshift(mathLesson);
                }
            } catch (err) {
                console.error('Failed to inject local lesson:', err);
            }
        }

        // INJECT LOCAL OJT LESSON (for all users - demo/public access)
        try {
            const fs = await import('fs');
            const path = await import('path');
            const filePath = path.join(process.cwd(), 'src/data/sales/lesson_ojt.json');

            if (fs.existsSync(filePath)) {
                const fileContent = fs.readFileSync(filePath, 'utf-8');
                const localLesson = JSON.parse(fileContent);

                const ojtLesson = {
                    lesson_id: localLesson.lesson_id,
                    title: localLesson.title,
                    description: localLesson.subtitle || "On-the-Job Training",
                    duration_minutes: 25,
                    xp_reward: localLesson.xp_reward || 300,
                    difficulty: 'intermediate',
                    category: 'Sprzedaż',
                    status: 'published',
                    display_order: 1,
                    release_date: null,
                    module: 'sales-training',
                    track: 'sales',
                    content: localLesson.content,
                    module_id: null // Will be assigned when sales module exists
                };

                lessons?.unshift(ojtLesson);
            }
        } catch (err) {
            console.error('Failed to inject OJT lesson:', err);
        }

        // INJECT FUNDAMENTALS LESSON
        try {
            const fs = await import('fs');
            const path = await import('path');
            const filePath = path.join(process.cwd(), 'src/data/sales/lesson_fundamentals.json');

            if (fs.existsSync(filePath)) {
                const fileContent = fs.readFileSync(filePath, 'utf-8');
                const localLesson = JSON.parse(fileContent);

                // Use the status from the file or default to published
                localLesson.status = 'published';
                localLesson.category = 'Przywództwo'; // Override category if needed

                lessons?.unshift(localLesson);
            }
        } catch (err) {
            console.error('Failed to inject Fundamentals lesson:', err);
        }

        return NextResponse.json({ lessons, modules, progress: progressMap });

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
