import { createClient } from '@/lib/supabase/server';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
    try {
        const supabase = await createClient();

        // Verify user is authenticated and is admin
        const { data: { user }, error: authError } = await supabase.auth.getUser();

        if (authError || !user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        // Check if user is admin
        const { data: profile } = await supabase
            .from('user_profiles')
            .select('role:user_roles(role_slug)')
            .eq('id', user.id)
            .single();

        if (!profile || profile.role?.role_slug !== 'admin') {
            return NextResponse.json({ error: 'Forbidden - Admin only' }, { status: 403 });
        }

        const body = await request.json();
        const { userId, companyId, roleId } = body;

        // Validate required fields
        if (!userId || !companyId || !roleId) {
            return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
        }

        // Update user profile
        const { data: updatedProfile, error: updateError } = await supabase
            .from('user_profiles')
            .update({
                company_id: companyId,
                role_id: roleId
            })
            .eq('id', userId)
            .select(`
        *,
        company:companies(id, company_slug, name),
        role:user_roles(id, role_slug, display_name)
      `)
            .single();

        if (updateError) {
            console.error('Profile update error:', updateError);
            return NextResponse.json({ error: updateError.message }, { status: 500 });
        }

        return NextResponse.json({ profile: updatedProfile });

    } catch (error) {
        console.error('API error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
