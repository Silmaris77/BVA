import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const supabase = await createClient()
        const { id: toolId } = await params

        // Get authenticated user
        const { data: { user }, error: authError } = await supabase.auth.getUser()
        if (authError || !user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        const body = await request.json()
        const { input_data, output_data, xp_awarded = 0 } = body

        if (!output_data) {
            return NextResponse.json({ error: 'Missing output_data' }, { status: 400 })
        }

        // Update user metadata to store result
        // We use a specific structure: { tool_history: { [toolId]: { last_result: ..., timestamp: ... } } }

        const currentMeta = user.user_metadata || {};
        const toolHistory = currentMeta.tool_history || {};

        // Update specific tool data
        toolHistory[toolId] = {
            last_result: output_data,
            timestamp: new Date().toISOString(),
            xp_config: xp_awarded
        };

        const { data: userData, error: updateError } = await supabase.auth.updateUser({
            data: {
                ...currentMeta,
                tool_history: toolHistory
            }
        });

        if (updateError) {
            console.error('Error updating user metadata:', updateError)
            return NextResponse.json({ error: updateError.message }, { status: 500 })
        }

        // Return structure compatible with frontend expectation
        return NextResponse.json({
            success: true,
            usage: {
                // Mocking the DB record structure so frontend doesn't break
                output_data: output_data,
                created_at: new Date().toISOString()
            }
        })

    } catch (error) {
        console.error('Tool completion error:', error)
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
    }
}
