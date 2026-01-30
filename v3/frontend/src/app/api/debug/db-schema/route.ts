import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET() {
    const supabase = await createClient()
    try {
        // Inspect the columns of user_tool_usage
        // Since we can't run raw SQL easily via client, we'll try to insert a dummy record with JUST required fields
        // and see what error we get, OR we try to select * and see the returned keys if any data exists.

        // Better yet, let's try to just select the definition from information_schema if we have permissions, 
        // but often we don't.

        // Let's try to insert without input_data and see if it works.
        const { data, error } = await supabase
            .from('resources')
            .select('*')

        return NextResponse.json({
            count: data?.length || 0,
            data,
            error
        })
    } catch (e: any) {
        return NextResponse.json({ status: 'exception', message: e.message })
    }
}
