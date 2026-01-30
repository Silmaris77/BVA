import { NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'
import { isAdmin } from '@/lib/admin'

export async function GET() {
    try {
        if (!(await isAdmin())) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        const supabase = await createClient()

        // Fetch all resource types
        const [lessonsRes, modulesRes, engramsRes, resourcesRes, toolsRes, pathsRes] = await Promise.all([
            supabase.from('lessons').select('lesson_id, title, category, module_id'),
            supabase.from('modules').select('id, title, track'),
            supabase.from('engrams').select('engram_id, title'),
            supabase.from('resources').select('resource_id, title, type'),
            supabase.from('tools').select('tool_id, title, category'),
            supabase.from('learning_paths').select('path_slug, title, description'),
        ])

        const resources = {
            nauka: {
                lekcje: lessonsRes.data?.map(l => ({
                    id: l.lesson_id,
                    title: l.title,
                    category: l.category,
                    type: 'lesson',
                    parentId: l.module_id // Link to Module
                })) || [],
                moduły: modulesRes.data?.map(m => ({
                    id: m.id,
                    title: m.title,
                    category: m.track || 'Moduł',
                    type: 'module',
                    parentId: m.track // Link to Track/Path
                })) || [],
                ścieżki: pathsRes.data?.map(p => ({
                    id: p.path_slug, // Using slug as ID for permission check
                    title: p.title,
                    category: 'Path',
                    type: 'path'
                })) || [],
                engramy: engramsRes.data?.map(e => ({
                    id: e.engram_id,
                    title: e.title,
                    type: 'engram'
                })) || [],
                zasoby: resourcesRes.data?.map(r => ({
                    id: r.resource_id,
                    title: r.title,
                    resourceType: r.type,
                    type: 'resource'
                })) || [],
            },
            praktyka: {
                narzędzia: toolsRes.data?.map(t => ({
                    id: t.tool_id,
                    title: t.title,
                    category: t.category,
                    type: 'tool'
                })) || [],
                // Trening, gry, projekty - will add if tables exist
            }
        }

        return NextResponse.json({ resources })

    } catch (error) {
        console.error('Resources scan error:', error)
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
    }
}
