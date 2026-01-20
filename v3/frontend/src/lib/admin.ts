'use server'

import { createClient } from '@/lib/supabase/server'

export interface AdminUser {
    id: string
    email: string
    role_slug: string
    display_name: string | null
}

/**
 * Check if the current user has admin role
 */
export async function isAdmin(): Promise<boolean> {
    const supabase = await createClient()

    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return false

    const { data: profile } = await supabase
        .from('user_profiles')
        .select(`
            role_id,
            user_roles!inner (
                role_slug
            )
        `)
        .eq('id', user.id)
        .single()

    if (!profile) return false

    // @ts-ignore - nested select typing
    return profile.user_roles?.role_slug === 'admin'
}

/**
 * Get admin user data or null if not admin
 */
export async function getAdminUser(): Promise<AdminUser | null> {
    const supabase = await createClient()

    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return null

    const { data: profile } = await supabase
        .from('user_profiles')
        .select(`
            display_name,
            user_roles!inner (
                role_slug
            )
        `)
        .eq('id', user.id)
        .single()

    if (!profile) return null

    // @ts-ignore - nested select typing
    const roleSlug = profile.user_roles?.role_slug
    if (roleSlug !== 'admin') return null

    return {
        id: user.id,
        email: user.email || '',
        role_slug: roleSlug,
        display_name: profile.display_name
    }
}

/**
 * Require admin access - throws if not admin
 */
export async function requireAdmin(): Promise<AdminUser> {
    const admin = await getAdminUser()
    if (!admin) {
        throw new Error('Unauthorized: Admin access required')
    }
    return admin
}
