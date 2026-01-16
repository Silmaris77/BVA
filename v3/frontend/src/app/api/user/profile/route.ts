import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

export async function GET() {
    try {
        const supabase = await createClient();

        // Get current user
        const { data: { user }, error: authError } = await supabase.auth.getUser();

        if (authError || !user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        // Get user profile with company and role
        const { data: profile, error: profileError } = await supabase
            .from('user_profiles')
            .select(`
        *,
        company:companies(id, company_slug, name, logo_url),
        role:user_roles(id, role_slug, display_name)
      `)
            .eq('id', user.id)
            .single();

        if (profileError) {
            console.error('Profile fetch error:', profileError);
            return NextResponse.json({ error: profileError.message }, { status: 500 });
        }

        // Get total XP
        const { data: xpData } = await supabase
            .rpc('get_user_total_xp', { user_uuid: user.id });

        const totalXp = xpData || 0;

        return NextResponse.json({
            user: {
                id: user.id,
                email: user.email,
                profile: {
                    ...profile,
                    totalXp
                }
            }
        });

    } catch (error) {
        console.error('API error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
