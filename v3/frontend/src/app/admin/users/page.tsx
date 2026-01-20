'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Users as UsersIcon, ArrowLeft, Shield, RefreshCw, Building, Mail } from 'lucide-react'

interface User {
    id: string
    email: string
    display_name: string | null
    total_xp: number
    lessons_completed: number
    engrams_installed: number
    user_roles: { role_slug: string; display_name: string } | null
    companies: { company_slug: string; name: string } | null
    created_at: string
}

interface Role {
    role_slug: string
    display_name: string
}

interface Company {
    company_slug: string
    name: string
}

export default function AdminUsersPage() {
    const { user, loading: authLoading } = useAuth()
    const router = useRouter()
    const [users, setUsers] = useState<User[]>([])
    const [roles, setRoles] = useState<Role[]>([])
    const [companies, setCompanies] = useState<Company[]>([])
    const [loading, setLoading] = useState(true)
    const [isAdmin, setIsAdmin] = useState(false)
    const [updating, setUpdating] = useState<string | null>(null)

    useEffect(() => {
        async function loadData() {
            if (!user) return
            try {
                const [usersRes, rolesRes, companiesRes] = await Promise.all([
                    fetch('/api/admin/users'),
                    fetch('/api/admin/roles'),
                    fetch('/api/admin/companies')
                ])

                if (usersRes.ok) {
                    setIsAdmin(true)
                    const [usersData, rolesData, companiesData] = await Promise.all([
                        usersRes.json(),
                        rolesRes.json(),
                        companiesRes.json()
                    ])
                    setUsers(usersData.users || [])
                    setRoles(rolesData.roles || [])
                    setCompanies(companiesData.companies || [])
                } else {
                    setIsAdmin(false)
                }
            } catch (error) {
                console.error('Error loading data:', error)
            } finally {
                setLoading(false)
            }
        }
        if (!authLoading) loadData()
    }, [user, authLoading])

    useEffect(() => {
        if (!authLoading && !loading && (!user || !isAdmin)) {
            router.push('/admin')
        }
    }, [user, isAdmin, authLoading, loading, router])

    const handleUpdateRole = async (userId: string, roleSlug: string) => {
        setUpdating(userId)
        try {
            const response = await fetch('/api/admin/users', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, role_slug: roleSlug })
            })
            if (response.ok) {
                // Reload users
                const res = await fetch('/api/admin/users')
                const data = await res.json()
                setUsers(data.users || [])
            }
        } catch (error) {
            console.error('Error updating role:', error)
        } finally {
            setUpdating(null)
        }
    }

    const handleUpdateCompany = async (userId: string, companySlug: string) => {
        setUpdating(userId)
        try {
            const response = await fetch('/api/admin/users', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, company_slug: companySlug })
            })
            if (response.ok) {
                // Reload users
                const res = await fetch('/api/admin/users')
                const data = await res.json()
                setUsers(data.users || [])
            }
        } catch (error) {
            console.error('Error updating company:', error)
        } finally {
            setUpdating(null)
        }
    }

    if (authLoading || loading) {
        return <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'rgba(255, 255, 255, 0.6)' }}>Ładowanie...</div>
    }

    if (!user || !isAdmin) return null

    return (
        <div style={{ minHeight: '100vh', padding: '32px 48px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '32px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <Link href="/admin" style={{ width: '40px', height: '40px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'rgba(255, 255, 255, 0.8)' }}>
                        <ArrowLeft size={20} />
                    </Link>
                    <div style={{ width: '48px', height: '48px', background: 'rgba(0, 212, 255, 0.2)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#00d4ff' }}>
                        <UsersIcon size={24} />
                    </div>
                    <div>
                        <h1 style={{ fontSize: '24px', fontWeight: 700 }}>Zarządzanie Użytkownikami</h1>
                        <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px' }}>{users.length} użytkowników</p>
                    </div>
                </div>
            </div>

            <div style={{ background: 'rgba(20, 20, 35, 0.4)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '16px', overflow: 'hidden' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                        <tr style={{ background: 'rgba(0, 0, 0, 0.2)', borderBottom: '1px solid rgba(255, 255, 255, 0.08)' }}>
                            <th style={{ padding: '16px', textAlign: 'left', fontSize: '13px', fontWeight: 600, color: 'rgba(255, 255, 255, 0.7)' }}>Użytkownik</th>
                            <th style={{ padding: '16px', textAlign: 'left', fontSize: '13px', fontWeight: 600, color: 'rgba(255, 255, 255, 0.7)' }}>Rola</th>
                            <th style={{ padding: '16px', textAlign: 'left', fontSize: '13px', fontWeight: 600, color: 'rgba(255, 255, 255, 0.7)' }}>Firma</th>
                            <th style={{ padding: '16px', textAlign: 'right', fontSize: '13px', fontWeight: 600, color: 'rgba(255, 255, 255, 0.7)' }}>Statystyki</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map(u => (
                            <tr key={u.id} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
                                <td style={{ padding: '16px' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                        <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'linear-gradient(135deg, #b000ff, #00d4ff)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: '14px' }}>
                                            {u.display_name?.substring(0, 2).toUpperCase() || u.email.substring(0, 2).toUpperCase()}
                                        </div>
                                        <div>
                                            <div style={{ fontSize: '14px', fontWeight: 600 }}>{u.display_name || 'Bez nazwy'}</div>
                                            <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.5)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                                                <Mail size={12} /> {u.email}
                                            </div>
                                        </div>
                                    </div>
                                </td>
                                <td style={{ padding: '16px' }}>
                                    <select
                                        value={u.user_roles?.role_slug || ''}
                                        onChange={(e) => handleUpdateRole(u.id, e.target.value)}
                                        disabled={updating === u.id}
                                        style={{ padding: '6px 12px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '13px', cursor: 'pointer' }}
                                        className="admin-select"
                                    >
                                        {!u.user_roles && <option value="" style={{ background: '#1a1a2e', color: 'white' }}>Brak roli</option>}
                                        {roles.map(r => (
                                            <option key={r.role_slug} value={r.role_slug} style={{ background: '#1a1a2e', color: 'white' }}>{r.display_name}</option>
                                        ))}
                                    </select>
                                </td>
                                <td style={{ padding: '16px' }}>
                                    <select
                                        value={u.companies?.company_slug || ''}
                                        onChange={(e) => handleUpdateCompany(u.id, e.target.value)}
                                        disabled={updating === u.id}
                                        style={{ padding: '6px 12px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '13px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}
                                        className="admin-select"
                                    >
                                        {!u.companies && <option value="" style={{ background: '#1a1a2e', color: 'white' }}>Brak firmy</option>}
                                        {companies.map(c => (
                                            <option key={c.company_slug} value={c.company_slug} style={{ background: '#1a1a2e', color: 'white' }}>{c.name}</option>
                                        ))}
                                    </select>
                                </td>
                                <td style={{ padding: '16px', textAlign: 'right' }}>
                                    <div style={{ display: 'flex', gap: '16px', justifyContent: 'flex-end', fontSize: '12px' }}>
                                        <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>💪 {u.total_xp} XP</span>
                                        <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>📚 {u.lessons_completed}</span>
                                        <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>🧠 {u.engrams_installed}</span>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}
