'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import {
    Shield, BookOpen, Brain, Wrench, FileText, Users,
    Settings, BarChart3, Plus, AlertTriangle
} from 'lucide-react'

interface ContentStats {
    lessons: number
    engrams: number
    tools: number
    resources: number
}

export default function AdminDashboard() {
    const { user, profile, loading: authLoading } = useAuth()
    const router = useRouter()
    const [isAdmin, setIsAdmin] = useState(false)
    const [checkingRole, setCheckingRole] = useState(true)
    const [stats, setStats] = useState<ContentStats>({ lessons: 0, engrams: 0, tools: 0, resources: 0 })

    // Check admin role
    useEffect(() => {
        async function checkAdminAccess() {
            if (!user) {
                setCheckingRole(false)
                return
            }

            try {
                // Try to fetch admin content - if it works, we're admin
                const response = await fetch('/api/admin/lessons')
                if (response.ok) {
                    setIsAdmin(true)
                    // Fetch all stats
                    const [lessonsRes, engramsRes, toolsRes, resourcesRes] = await Promise.all([
                        fetch('/api/admin/lessons'),
                        fetch('/api/admin/engrams'),
                        fetch('/api/admin/tools'),
                        fetch('/api/admin/resources')
                    ])

                    const [lessonsData, engramsData, toolsData, resourcesData] = await Promise.all([
                        lessonsRes.json(),
                        engramsRes.json(),
                        toolsRes.json(),
                        resourcesRes.json()
                    ])

                    setStats({
                        lessons: lessonsData.lessons?.length || 0,
                        engrams: engramsData.engrams?.length || 0,
                        tools: toolsData.tools?.length || 0,
                        resources: resourcesData.resources?.length || 0
                    })
                } else {
                    setIsAdmin(false)
                }
            } catch (error) {
                console.error('Admin check error:', error)
                setIsAdmin(false)
            } finally {
                setCheckingRole(false)
            }
        }

        if (!authLoading) {
            checkAdminAccess()
        }
    }, [user, authLoading])

    // Redirect to login if not authenticated
    useEffect(() => {
        if (!authLoading && !checkingRole && !user) {
            router.push('/auth/login')
        }
    }, [user, authLoading, checkingRole, router])

    if (authLoading || checkingRole) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'rgba(255, 255, 255, 0.6)'
            }}>
                Weryfikacja uprawnień...
            </div>
        )
    }

    if (!user) {
        return null
    }

    if (!isAdmin) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '24px',
                padding: '32px'
            }}>
                <div style={{
                    width: '80px',
                    height: '80px',
                    background: 'rgba(255, 68, 68, 0.2)',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                }}>
                    <AlertTriangle size={40} style={{ color: '#ff4444' }} />
                </div>
                <h1 style={{ fontSize: '28px', fontWeight: 700 }}>Brak dostępu</h1>
                <p style={{ color: 'rgba(255, 255, 255, 0.6)', textAlign: 'center', maxWidth: '400px' }}>
                    Ta sekcja jest dostępna tylko dla administratorów.
                    Jeśli uważasz, że powinieneś mieć dostęp, skontaktuj się z administratorem systemu.
                </p>
                <Link
                    href="/"
                    style={{
                        padding: '12px 24px',
                        background: 'linear-gradient(135deg, #b000ff, #00d4ff)',
                        borderRadius: '12px',
                        color: 'white',
                        textDecoration: 'none',
                        fontWeight: 600
                    }}
                >
                    Wróć do strony głównej
                </Link>
            </div>
        )
    }

    const contentSections = [
        {
            title: 'Lekcje',
            icon: BookOpen,
            count: stats.lessons,
            color: '#00d4ff',
            href: '/admin/lessons',
            description: 'Zarządzaj lekcjami i ich kartami'
        },
        {
            title: 'Engramy',
            icon: Brain,
            count: stats.engrams,
            color: '#b000ff',
            href: '/admin/engrams',
            description: 'Mikro-lekcje z quizami'
        },
        {
            title: 'Narzędzia',
            icon: Wrench,
            count: stats.tools,
            color: '#ff8800',
            href: '/admin/tools',
            description: 'Kalkulatory i generatory'
        },
        {
            title: 'Zasoby',
            icon: FileText,
            count: stats.resources,
            color: '#00ff88',
            href: '/admin/resources',
            description: 'Materiały referencyjne'
        }
    ]

    return (
        <div style={{ minHeight: '100vh', padding: '32px 48px' }}>
            {/* Header */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: '48px'
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <div style={{
                        width: '56px',
                        height: '56px',
                        background: 'linear-gradient(135deg, #ff0055, #b000ff)',
                        borderRadius: '16px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                    }}>
                        <Shield size={28} />
                    </div>
                    <div>
                        <h1 style={{ fontSize: '28px', fontWeight: 700, marginBottom: '4px' }}>
                            Panel Administratora
                        </h1>
                        <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px' }}>
                            Zarządzaj contentem platformy BrainVenture
                        </p>
                    </div>
                </div>

                <Link
                    href="/"
                    style={{
                        padding: '10px 20px',
                        background: 'rgba(255, 255, 255, 0.05)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '10px',
                        color: 'rgba(255, 255, 255, 0.8)',
                        textDecoration: 'none',
                        fontSize: '14px',
                        fontWeight: 500
                    }}
                >
                    ← Wróć do aplikacji
                </Link>
            </div>

            {/* Stats Overview */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(4, 1fr)',
                gap: '24px',
                marginBottom: '48px'
            }}>
                {contentSections.map(section => (
                    <div
                        key={section.title}
                        style={{
                            background: 'rgba(20, 20, 35, 0.4)',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            borderRadius: '16px',
                            padding: '24px',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '16px'
                        }}
                    >
                        <div style={{
                            width: '48px',
                            height: '48px',
                            background: `${section.color}20`,
                            borderRadius: '12px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: section.color
                        }}>
                            <section.icon size={24} />
                        </div>
                        <div>
                            <div style={{ fontSize: '28px', fontWeight: 700 }}>{section.count}</div>
                            <div style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '13px' }}>
                                {section.title}
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Content Management Cards */}
            <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '24px' }}>
                Zarządzanie contentem
            </h2>

            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(2, 1fr)',
                gap: '24px'
            }}>
                {contentSections.map(section => (
                    <Link
                        key={section.title}
                        href={section.href}
                        style={{
                            background: 'rgba(20, 20, 35, 0.4)',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            borderRadius: '16px',
                            padding: '24px',
                            textDecoration: 'none',
                            color: 'white',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            transition: 'all 0.2s'
                        }}
                        onMouseEnter={(e) => {
                            e.currentTarget.style.borderColor = section.color
                            e.currentTarget.style.transform = 'translateY(-2px)'
                        }}
                        onMouseLeave={(e) => {
                            e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.08)'
                            e.currentTarget.style.transform = 'translateY(0)'
                        }}
                    >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                            <div style={{
                                width: '56px',
                                height: '56px',
                                background: `${section.color}20`,
                                borderRadius: '14px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                color: section.color
                            }}>
                                <section.icon size={28} />
                            </div>
                            <div>
                                <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '4px' }}>
                                    {section.title}
                                </h3>
                                <p style={{ color: 'rgba(255, 255, 255, 0.5)', fontSize: '13px' }}>
                                    {section.description}
                                </p>
                            </div>
                        </div>

                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <span style={{
                                padding: '6px 12px',
                                background: `${section.color}20`,
                                borderRadius: '20px',
                                fontSize: '13px',
                                fontWeight: 600,
                                color: section.color
                            }}>
                                {section.count} elementów
                            </span>
                            <div style={{
                                width: '36px',
                                height: '36px',
                                background: section.color,
                                borderRadius: '10px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center'
                            }}>
                                <Plus size={20} style={{ color: 'white' }} />
                            </div>
                        </div>
                    </Link>
                ))}
            </div>

            {/* Quick Actions */}
            <h2 style={{ fontSize: '20px', fontWeight: 600, margin: '48px 0 24px' }}>
                Szybkie akcje
            </h2>

            <div style={{
                display: 'flex',
                gap: '16px',
                flexWrap: 'wrap'
            }}>
                <Link
                    href="/admin/users"
                    style={{
                        padding: '16px 24px',
                        background: 'rgba(255, 255, 255, 0.05)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '12px',
                        color: 'rgba(255, 255, 255, 0.8)',
                        textDecoration: 'none',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        fontSize: '14px',
                        fontWeight: 500,
                        transition: 'all 0.2s'
                    }}
                >
                    <Users size={20} />
                    Użytkownicy
                </Link>
                <Link
                    href="/admin/analytics"
                    style={{
                        padding: '16px 24px',
                        background: 'rgba(255, 255, 255, 0.05)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '12px',
                        color: 'rgba(255, 255, 255, 0.8)',
                        textDecoration: 'none',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        fontSize: '14px',
                        fontWeight: 500
                    }}
                >
                    <BarChart3 size={20} />
                    Analityka
                </Link>
                <Link
                    href="/admin/settings"
                    style={{
                        padding: '16px 24px',
                        background: 'rgba(255, 255, 255, 0.05)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '12px',
                        color: 'rgba(255, 255, 255, 0.8)',
                        textDecoration: 'none',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        fontSize: '14px',
                        fontWeight: 500
                    }}
                >
                    <Settings size={20} />
                    Ustawienia
                </Link>
            </div>
        </div>
    )
}
