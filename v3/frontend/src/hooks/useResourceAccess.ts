import { useEffect, useState } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { supabase } from '@/lib/supabase'

export function useResourceAccess(resourceId: string) {
    const { user, profile, loading: authLoading } = useAuth()
    const [permissions, setPermissions] = useState<{ allowed_roles: string[] } | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function fetchPermissions() {
            if (!resourceId) return

            try {
                const { data, error } = await supabase
                    .from('resource_permissions')
                    .select('allowed_roles')
                    .eq('resource_id', resourceId)
                    .single()

                if (data) {
                    setPermissions(data)
                } else {
                    // Resource not configured - fail safe logic
                    console.log(`Resource ${resourceId} permissions not found.`)
                    setPermissions(null)
                }
            } catch (err) {
                console.error('Error fetching permissions:', err)
            } finally {
                setLoading(false)
            }
        }

        fetchPermissions()
    }, [resourceId])

    if (authLoading || loading) {
        return { hasAccess: false, loading: true }
    }

    if (!user || !profile) {
        return { hasAccess: false, loading: false, reason: 'unauthenticated' }
    }

    // If no permissions found in DB, default to ALLOW or BLOCK?
    // Safe approach: if explicitly configured, check. If not, maybe allow? 
    // Usually dynamic RBAC assumes if IT EXISTS in table, check it. If not, default fallback.
    // For now, if no record, we return false (Block) to be safe, or we manually handle "Access Denied" if permissions loaded and check failed.

    if (!permissions) {
        // Fallback: if not in DB, assume it's public? Or block?
        // Let's assume block for 'degen-test' since it WAS protected.
        // But for other tools?
        // Let's return loading=false, hasAccess=false (Closed by default)
        return { hasAccess: false, loading: false, reason: 'not_configured' }
    }

    const userRole = profile.role || '' // role is slug now
    const hasAccess = permissions.allowed_roles.includes(userRole)

    return { hasAccess, loading: false }
}
