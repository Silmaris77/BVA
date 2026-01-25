import { createClient } from '@supabase/supabase-js';
import { NextResponse } from 'next/server';

export async function GET() {
    try {
        // Use standard supabase-js client for Admin/Service Role operations
        // This ensures no cookies/user session interferes with RLS bypass

        const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
        if (!serviceRoleKey) {
            return NextResponse.json({ error: 'Config Error: SUPABASE_SERVICE_ROLE_KEY is missing in .env.local' }, { status: 500 });
        }

        const supabase = createClient(
            process.env.NEXT_PUBLIC_SUPABASE_URL!,
            serviceRoleKey,
            {
                auth: {
                    persistSession: false,
                    autoRefreshToken: false,
                    detectSessionInUrl: false
                }
            }
        );

        // 1. Insert "Szkoła" Company
        const { data: company, error: companyError } = await supabase
            .from('companies')
            .upsert({
                company_slug: 'school',
                name: 'Szkoła',
                logo_url: null
            }, { onConflict: 'company_slug' })
            .select()
            .single();

        if (companyError) {
            console.error('Company insert error:', companyError);
            return NextResponse.json({ error: companyError.message }, { status: 500 });
        }

        // 2. Insert "student" Role if not exists
        const { data: role, error: roleError } = await supabase
            .from('user_roles')
            .upsert({
                role_slug: 'student',
                display_name: 'Uczeń'
            }, { onConflict: 'role_slug' })
            .select()
            .single();

        if (roleError) {
            console.error('Role insert error:', roleError);
        }

        return NextResponse.json({
            success: true,
            message: 'School company and Student role seeded successfully',
            company,
            role
        });

    } catch (error) {
        console.error('Setup error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
