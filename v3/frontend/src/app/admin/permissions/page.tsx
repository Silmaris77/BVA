'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Shield, ArrowLeft, Search, ChevronRight, ChevronDown, User, Users } from 'lucide-react'

interface Permission {
    id: string
    resource_id: string
    allowed_roles: string[]
}

interface Role {
    role_slug: string
    display_name: string
}

interface Company {
    id: string
    company_slug: string
    name: string
}

interface TreeNode {
    id: string
    title: string
    type: 'track' | 'module' | 'lesson' | 'engram' | 'resource' | 'tool'
    category?: string
    children?: TreeNode[]
    parentId?: string
}

interface ResourcesByCategory {
    nauka: {
        lekcje: any[]
        moduły: any[]
        ścieżki: any[]
        engramy: any[]
        zasoby: any[]
    }
    praktyka: {
        narzędzia: any[]
    }
}

export default function PermissionsPage() {
    const { user, loading: authLoading } = useAuth()
    const router = useRouter()

    const [permissions, setPermissions] = useState<Permission[]>([])
    const [roles, setRoles] = useState<Role[]>([])
    const [companies, setCompanies] = useState<Company[]>([])
    const [resources, setResources] = useState<ResourcesByCategory | null>(null)
    const [loading, setLoading] = useState(true)
    const [selectedRole, setSelectedRole] = useState<string>('')
    const [selectedCompany, setSelectedCompany] = useState<string>('')
    const [searchTerm, setSearchTerm] = useState('')
    const [activeTab, setActiveTab] = useState<'nauka' | 'praktyka'>('nauka')
    const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set())

    useEffect(() => {
        if (!authLoading && !user) {
            router.push('/auth/login')
        }
    }, [user, authLoading, router])

    useEffect(() => {
        fetchData()
    }, [])

    async function fetchData() {
        try {
            const [rolesRes, resourcesRes, permissionsRes, companiesRes] = await Promise.all([
                fetch('/api/admin/roles'),
                fetch('/api/admin/resources-scan'),
                fetch('/api/admin/permissions'),
                fetch('/api/admin/companies')
            ])

            const rolesData = await rolesRes.json()
            const resourcesData = await resourcesRes.json()
            const permissionsData = await permissionsRes.json()
            const companiesData = await companiesRes.json()

            if (rolesData.roles) {
                setRoles(rolesData.roles)
                if (rolesData.roles.length > 0 && !selectedRole) {
                    setSelectedRole(rolesData.roles[0].role_slug)
                }
            }

            if (companiesData.companies) {
                setCompanies(companiesData.companies)
                if (companiesData.companies.length > 0 && !selectedCompany) {
                    setSelectedCompany(companiesData.companies[0].company_slug)
                }
            }

            if (resourcesData.resources) {
                setResources(resourcesData.resources)
            }

            if (permissionsData.permissions) {
                setPermissions(permissionsData.permissions)
            }
        } catch (error) {
            console.error('Error fetching data:', error)
        } finally {
            setLoading(false)
        }
    }

    // Build tree structure from flat resources
    function buildTree(): TreeNode[] {
        if (!resources) return []

        const tree: TreeNode[] = []

        if (activeTab === 'nauka') {
            // Tracks -> Modules -> Lessons
            const tracksNode: TreeNode = {
                id: '_tracks',
                title: 'Ścieżki',
                type: 'track',
                children: resources.nauka.ścieżki.map(track => {
                    const trackModules = resources.nauka.moduły
                        .filter(m => m.parentId === track.id)
                        .map(mod => ({
                            id: mod.id,
                            title: mod.title,
                            type: 'module' as const,
                            children: resources.nauka.lekcje
                                .filter(l => l.parentId === mod.id)
                                .map(lesson => ({
                                    id: lesson.id,
                                    title: lesson.title,
                                    type: 'lesson' as const
                                }))
                        }))

                    return {
                        id: track.id,
                        title: track.title,
                        type: 'track' as const,
                        children: trackModules
                    }
                })
            }

            tree.push(tracksNode)

            // Engrams (flat)
            if (resources.nauka.engramy.length > 0) {
                tree.push({
                    id: '_engrams',
                    title: 'Engramy',
                    type: 'engram',
                    children: resources.nauka.engramy.map(e => ({
                        id: e.id,
                        title: e.title,
                        type: 'engram' as const
                    }))
                })
            }

            // Resources (flat)
            if (resources.nauka.zasoby.length > 0) {
                tree.push({
                    id: '_resources',
                    title: 'Zasoby',
                    type: 'resource',
                    children: resources.nauka.zasoby.map(r => ({
                        id: r.id,
                        title: r.title,
                        type: 'resource' as const
                    }))
                })
            }
        } else {
            // Tools (flat)
            if (resources.praktyka.narzędzia.length > 0) {
                tree.push({
                    id: '_tools',
                    title: 'Narzędzia',
                    type: 'tool',
                    children: resources.praktyka.narzędzia.map(t => ({
                        id: t.id,
                        title: t.title,
                        type: 'tool' as const
                    }))
                })
            }
        }

        return tree
    }

    // Check if role has access to resource
    function hasAccess(resourceId: string, roleSlug: string): boolean {
        const config = permissions.find(p => p.resource_id === resourceId)
        if (!config) return false
        return config.allowed_roles.includes(roleSlug) || config.allowed_roles.includes('all')
    }

    // Collect all descendant IDs from a node
    function collectDescendantIds(node: TreeNode): string[] {
        const ids: string[] = []
        if (!node.id.startsWith('_')) {
            ids.push(node.id)
        }
        if (node.children) {
            node.children.forEach(child => {
                ids.push(...collectDescendantIds(child))
            })
        }
        return ids
    }

    // Toggle access for a resource and all its children (cascading)
    async function toggleAccess(node: TreeNode, roleSlug: string, currentAccess: boolean) {
        try {
            // Collect all IDs to update (current node + descendants)
            const idsToUpdate = collectDescendantIds(node)

            // Filter out category headers
            const realIds = idsToUpdate.filter(id => !id.startsWith('_'))

            // Batch update all permissions
            const updates = realIds.map(async (resourceId) => {
                const config = permissions.find(p => p.resource_id === resourceId)
                let updatedRoles: string[] = []

                if (config) {
                    updatedRoles = currentAccess
                        ? config.allowed_roles.filter(r => r !== roleSlug)
                        : [...config.allowed_roles, roleSlug]
                } else {
                    updatedRoles = [roleSlug]
                }

                await fetch('/api/admin/permissions', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        resource_id: resourceId,
                        allowed_roles: updatedRoles
                    })
                })

                return { resourceId, updatedRoles }
            })

            const results = await Promise.all(updates)

            // Optimistically update local state
            setPermissions(prev => {
                let updated = [...prev]
                results.forEach(({ resourceId, updatedRoles }) => {
                    const existingIndex = updated.findIndex(p => p.resource_id === resourceId)
                    if (existingIndex >= 0) {
                        updated[existingIndex] = {
                            ...updated[existingIndex],
                            allowed_roles: updatedRoles
                        }
                    } else {
                        updated.push({
                            id: resourceId,
                            resource_id: resourceId,
                            allowed_roles: updatedRoles
                        })
                    }
                })
                return updated
            })
        } catch (error) {
            console.error('Error toggling access:', error)
        }
    }

    // Recursive tree component
    function TreeNodeComponent({ node, depth = 0 }: { node: TreeNode; depth?: number }) {
        const isExpanded = expandedNodes.has(node.id)
        const hasChildren = node.children && node.children.length > 0
        const isChecked = selectedRole ? hasAccess(node.id, selectedRole) : false

        // Filter children by search
        const filteredChildren = node.children?.filter(child =>
            child.title.toLowerCase().includes(searchTerm.toLowerCase())
        )

        // Hide if doesn't match search and no children match
        if (searchTerm && !node.title.toLowerCase().includes(searchTerm.toLowerCase()) && (!filteredChildren || filteredChildren.length === 0)) {
            return null
        }

        return (
            <div style={{ marginLeft: depth > 0 ? '24px' : '0' }}>
                <div
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        padding: '8px 12px',
                        borderRadius: '8px',
                        background: isChecked ? 'rgba(0, 212, 255, 0.1)' : 'transparent',
                        border: isChecked ? '1px solid rgba(0, 212, 255, 0.3)' : '1px solid transparent',
                        cursor: 'pointer',
                        transition: 'all 0.2s',
                        marginBottom: '4px'
                    }}
                    onMouseEnter={(e) => {
                        if (!isChecked) {
                            e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)'
                        }
                    }}
                    onMouseLeave={(e) => {
                        if (!isChecked) {
                            e.currentTarget.style.background = 'transparent'
                        }
                    }}
                >
                    {hasChildren && (
                        <button
                            onClick={(e) => {
                                e.stopPropagation()
                                setExpandedNodes(prev => {
                                    const next = new Set(prev)
                                    if (next.has(node.id)) {
                                        next.delete(node.id)
                                    } else {
                                        next.add(node.id)
                                    }
                                    return next
                                })
                            }}
                            style={{
                                background: 'transparent',
                                border: 'none',
                                cursor: 'pointer',
                                padding: '4px',
                                marginRight: '8px',
                                color: 'rgba(255, 255, 255, 0.6)'
                            }}
                        >
                            {isExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                        </button>
                    )}

                    <input
                        type="checkbox"
                        checked={isChecked}
                        onChange={() => {
                            if (selectedRole && !node.id.startsWith('_')) {
                                toggleAccess(node, selectedRole, isChecked)
                            }
                        }}
                        disabled={!selectedRole || node.id.startsWith('_')}
                        style={{
                            marginRight: '12px',
                            cursor: selectedRole ? 'pointer' : 'not-allowed'
                        }}
                    />

                    <span style={{
                        flex: 1,
                        color: node.id.startsWith('_') ? 'rgba(255, 255, 255, 0.9)' : 'rgba(255, 255, 255, 0.7)',
                        fontSize: node.id.startsWith('_') ? '15px' : '14px',
                        fontWeight: node.id.startsWith('_') ? 600 : 400
                    }}>
                        {node.title}
                    </span>
                </div>

                {isExpanded && hasChildren && (
                    <div>
                        {filteredChildren?.map(child => (
                            <TreeNodeComponent key={child.id} node={child} depth={depth + 1} />
                        ))}
                    </div>
                )}
            </div>
        )
    }

    if (authLoading || loading) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'rgba(255, 255, 255, 0.6)'
            }}>
                Ładowanie...
            </div>
        )
    }

    if (!user) return null

    const tree = buildTree()

    return (
        <div style={{ minHeight: '100vh', background: '#0f0f1e' }}>
            {/* Header */}
            <div style={{
                padding: '24px',
                borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
            }}>
                <Link href="/admin" style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '8px',
                    color: 'rgba(255, 255, 255, 0.6)',
                    textDecoration: 'none',
                    marginBottom: '16px',
                    fontSize: '14px'
                }}>
                    <ArrowLeft size={16} />
                    Panel Admina
                </Link>

                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <Shield size={32} style={{ color: '#00d4ff' }} />
                    <h1 style={{
                        fontSize: '28px',
                        fontWeight: 700,
                        color: 'white',
                        margin: 0
                    }}>
                        Zarządzanie Dostępem
                    </h1>
                </div>
            </div>

            {/* Split Pane */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: '280px 1fr',
                height: 'calc(100vh - 120px)'
            }}>
                {/* Left Sidebar: Companies & Roles */}
                <div style={{
                    borderRight: '1px solid rgba(255, 255, 255, 0.1)',
                    padding: '24px',
                    overflowY: 'auto'
                }}>
                    {/* Companies Section */}
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        marginBottom: '12px',
                        color: 'rgba(255, 255, 255, 0.6)',
                        fontSize: '12px',
                        textTransform: 'uppercase',
                        fontWeight: 600
                    }}>
                        <Shield size={14} />
                        Firma ({companies.length})
                    </div>

                    {companies.map(company => (
                        <button
                            key={company.company_slug}
                            onClick={() => setSelectedCompany(company.company_slug)}
                            style={{
                                width: '100%',
                                padding: '10px 14px',
                                background: selectedCompany === company.company_slug
                                    ? 'rgba(176, 0, 255, 0.15)'
                                    : 'transparent',
                                border: selectedCompany === company.company_slug
                                    ? '1px solid rgba(176, 0, 255, 0.5)'
                                    : '1px solid rgba(255, 255, 255, 0.08)',
                                borderRadius: '8px',
                                color: selectedCompany === company.company_slug
                                    ? '#b000ff'
                                    : 'rgba(255, 255, 255, 0.6)',
                                fontSize: '13px',
                                fontWeight: selectedCompany === company.company_slug ? 600 : 400,
                                cursor: 'pointer',
                                marginBottom: '6px',
                                textAlign: 'left',
                                fontFamily: 'Outfit, sans-serif',
                                transition: 'all 0.2s'
                            }}
                        >
                            {company.name}
                        </button>
                    ))}

                    {/* Divider */}
                    <div style={{
                        height: '1px',
                        background: 'rgba(255, 255, 255, 0.1)',
                        margin: '20px 0'
                    }} />
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        marginBottom: '16px',
                        color: 'rgba(255, 255, 255, 0.6)',
                        fontSize: '12px',
                        textTransform: 'uppercase',
                        fontWeight: 600
                    }}>
                        <Users size={14} />
                        Role ({roles.length})
                    </div>

                    {roles.map(role => (
                        <button
                            key={role.role_slug}
                            onClick={() => setSelectedRole(role.role_slug)}
                            style={{
                                width: '100%',
                                padding: '12px 16px',
                                background: selectedRole === role.role_slug
                                    ? 'rgba(0, 212, 255, 0.15)'
                                    : 'transparent',
                                border: selectedRole === role.role_slug
                                    ? '1px solid rgba(0, 212, 255, 0.5)'
                                    : '1px solid rgba(255, 255, 255, 0.1)',
                                borderRadius: '10px',
                                color: selectedRole === role.role_slug
                                    ? '#00d4ff'
                                    : 'rgba(255, 255, 255, 0.7)',
                                fontSize: '14px',
                                fontWeight: selectedRole === role.role_slug ? 600 : 400,
                                cursor: 'pointer',
                                marginBottom: '8px',
                                textAlign: 'left',
                                fontFamily: 'Outfit, sans-serif',
                                transition: 'all 0.2s',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '8px'
                            }}
                        >
                            <User size={16} />
                            {role.display_name}
                        </button>
                    ))}
                </div>

                {/* Main Panel: Tree View */}
                <div style={{ padding: '24px', overflowY: 'auto' }}>
                    {selectedRole ? (
                        <>
                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '16px',
                                marginBottom: '24px'
                            }}>
                                {/* Tabs */}
                                <button
                                    onClick={() => setActiveTab('nauka')}
                                    style={{
                                        padding: '10px 20px',
                                        background: activeTab === 'nauka'
                                            ? 'rgba(0, 212, 255, 0.15)'
                                            : 'transparent',
                                        border: activeTab === 'nauka'
                                            ? '1px solid #00d4ff'
                                            : '1px solid rgba(255, 255, 255, 0.1)',
                                        borderRadius: '10px',
                                        color: activeTab === 'nauka' ? '#00d4ff' : 'rgba(255, 255, 255, 0.6)',
                                        fontSize: '14px',
                                        fontWeight: 600,
                                        cursor: 'pointer',
                                        fontFamily: 'Outfit, sans-serif'
                                    }}
                                >
                                    Nauka
                                </button>
                                <button
                                    onClick={() => setActiveTab('praktyka')}
                                    style={{
                                        padding: '10px 20px',
                                        background: activeTab === 'praktyka'
                                            ? 'rgba(255, 215, 0, 0.15)'
                                            : 'transparent',
                                        border: activeTab === 'praktyka'
                                            ? '1px solid #ffd700'
                                            : '1px solid rgba(255, 255, 255, 0.1)',
                                        borderRadius: '10px',
                                        color: activeTab === 'praktyka' ? '#ffd700' : 'rgba(255, 255, 255, 0.6)',
                                        fontSize: '14px',
                                        fontWeight: 600,
                                        cursor: 'pointer',
                                        fontFamily: 'Outfit, sans-serif'
                                    }}
                                >
                                    Praktyka
                                </button>

                                {/* Search */}
                                <div style={{
                                    position: 'relative',
                                    flex: 1,
                                    maxWidth: '400px'
                                }}>
                                    <Search size={16} style={{
                                        position: 'absolute',
                                        left: '12px',
                                        top: '50%',
                                        transform: 'translateY(-50%)',
                                        color: 'rgba(255, 255, 255, 0.4)'
                                    }} />
                                    <input
                                        type="text"
                                        placeholder="Szukaj zasobów..."
                                        value={searchTerm}
                                        onChange={(e) => setSearchTerm(e.target.value)}
                                        style={{
                                            width: '100%',
                                            padding: '10px 16px 10px 40px',
                                            background: 'rgba(255, 255, 255, 0.05)',
                                            border: '1px solid rgba(255, 255, 255, 0.1)',
                                            borderRadius: '10px',
                                            color: 'white',
                                            fontSize: '14px',
                                            fontFamily: 'Outfit, sans-serif',
                                            outline: 'none'
                                        }}
                                    />
                                </div>
                            </div>

                            {/* Tree */}
                            <div>
                                {tree.map(node => (
                                    <TreeNodeComponent key={node.id} node={node} />
                                ))}
                            </div>
                        </>
                    ) : (
                        <div style={{
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            justifyContent: 'center',
                            height: '100%',
                            color: 'rgba(255, 255, 255, 0.4)',
                            gap: '12px'
                        }}>
                            <User size={48} />
                            <p>Wybierz rolę, aby zarządzać uprawnieniami</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
