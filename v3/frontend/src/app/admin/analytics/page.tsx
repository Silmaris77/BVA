'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { BarChart3, ArrowLeft, Users, Zap, BookOpen, Brain, TrendingUp } from 'lucide-react'

interface Analytics {
    overview: {
        total_users: number
        total_xp: number
        total_lessons: number
        total_engrams: number
        completed_lessons: number
        installed_engrams: number
    }
    top_users: Array<{ user_id: string; total_xp: number }>
    activity_by_day: Record<string, { lessons: number; engrams: number; total_xp: number }>
}

export default function AdminAnalyticsPage() {
    const { user, loading: authLoading } = useAuth()
    const router = useRouter()
    const [analytics, setAnalytics] = useState<Analytics | null>(null)
    const [loading, setLoading] = useState(true)
    const [isAdmin, setIsAdmin] = useState(false)

    useEffect(() => {
        async function loadAnalytics() {
            if (!user) return
            try {
                const response = await fetch('/api/admin/analytics')
                if (response.ok) {
                    setIsAdmin(true)
                    const data = await response.json()
                    setAnalytics(data)
                } else {
                    setIsAdmin(false)
                }
            } catch (error) {
                console.error('Error loading analytics:', error)
            } finally {
                setLoading(false)
            }
        }
        if (!authLoading) loadAnalytics()
    }, [user, authLoading])

    useEffect(() => {
        if (!authLoading && !loading && (!user || !isAdmin)) {
            router.push('/admin')
        }
    }, [user, isAdmin, authLoading, loading, router])

    if (authLoading || loading) {
        return <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'rgba(255, 255, 255, 0.6)' }}>Ładowanie...</div>
    }

    if (!user || !isAdmin || !analytics) return null

    const { overview, activity_by_day } = analytics
    const completionRate = overview.total_lessons > 0 ? ((overview.completed_lessons / overview.total_lessons) * 100).toFixed(1) : '0'
    const avgXpPerUser = overview.total_users > 0 ? Math.round(overview.total_xp / overview.total_users) : 0

    return (
        <div style={{ minHeight: '100vh', padding: '32px 48px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '32px' }}>
                <Link href="/admin" style={{ width: '40px', height: '40px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'rgba(255, 255, 255, 0.8)' }}>
                    <ArrowLeft size={20} />
                </Link>
                <div style={{ width: '48px', height: '48px', background: 'rgba(0, 255, 136, 0.2)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#00ff88' }}>
                    <BarChart3 size={24} />
                </div>
                <div>
                    <h1 style={{ fontSize: '24px', fontWeight: 700 }}>Analityka Platformy</h1>
                    <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px' }}>Statystyki i aktywność użytkowników</p>
                </div>
            </div>

            {/* Overview Stats */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '24px', marginBottom: '32px' }}>
                {[
                    { icon: Users, label: 'Użytkownicy', value: overview.total_users, color: '#00d4ff' },
                    { icon: Zap, label: 'Całkowite XP', value: overview.total_xp.toLocaleString(), color: '#ffd700' },
                    { icon: BookOpen, label: 'Ukończone lekcje', value: overview.completed_lessons, color: '#00ff88' },
                    { icon: Brain, label: 'Zainstalowane engramy', value: overview.installed_engrams, color: '#b000ff' }
                ].map((stat, i) => (
                    <div key={i} style={{ background: 'rgba(20, 20, 35, 0.4)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '16px', padding: '20px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
                            <div style={{ width: '40px', height: '40px', background: `${stat.color}20`, borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: stat.color }}>
                                <stat.icon size={20} />
                            </div>
                            <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.6)' }}>{stat.label}</div>
                        </div>
                        <div style={{ fontSize: '28px', fontWeight: 700 }}>{stat.value}</div>
                    </div>
                ))}
            </div>

            {/* Metrics */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '32px' }}>
                <div style={{ background: 'rgba(20, 20, 35, 0.4)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '16px', padding: '24px' }}>
                    <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '16px' }}>Wskaźniki zaangażowania</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <span style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.7)' }}>Wskaźnik ukończenia lekcji</span>
                            <span style={{ fontSize: '18px', fontWeight: 700, color: '#00ff88' }}>{completionRate}%</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <span style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.7)' }}>Średnie XP na użytkownika</span>
                            <span style={{ fontSize: '18px', fontWeight: 700, color: '#ffd700' }}>{avgXpPerUser}</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <span style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.7)' }}>Engramy na użytkownika</span>
                            <span style={{ fontSize: '18px', fontWeight: 700, color: '#b000ff' }}>{overview.total_users > 0 ? (overview.installed_engrams / overview.total_users).toFixed(1) : '0'}</span>
                        </div>
                    </div>
                </div>

                <div style={{ background: 'rgba(20, 20, 35, 0.4)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '16px', padding: '24px' }}>
                    <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '16px' }}>Aktywność (ostatnie 7 dni)</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {Object.entries(activity_by_day).slice(-7).map(([day, data]) => (
                            <div key={day} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px', background: 'rgba(255, 255, 255, 0.02)', borderRadius: '8px' }}>
                                <span style={{ fontSize: '13px', color: 'rgba(255, 255, 255, 0.6)' }}>{new Date(day).toLocaleDateString('pl-PL', { month: 'short', day: 'numeric' })}</span>
                                <div style={{ display: 'flex', gap: '12px', fontSize: '12px' }}>
                                    <span style={{ color: '#00d4ff' }}>📚 {data.lessons}</span>
                                    <span style={{ color: '#b000ff' }}>🧠 {data.engrams}</span>
                                    <span style={{ color: '#ffd700' }}>💪 {data.total_xp}XP</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Content Overview */}
            <div style={{ background: 'rgba(20, 20, 35, 0.4)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '16px', padding: '24px' }}>
                <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '16px' }}>Przegląd contentu</h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
                    <div style={{ padding: '16px', background: 'rgba(0, 212, 255, 0.05)', borderRadius: '12px', border: '1px solid rgba(0, 212, 255, 0.2)' }}>
                        <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.6)', marginBottom: '8px' }}>Lekcje</div>
                        <div style={{ fontSize: '24px', fontWeight: 700, color: '#00d4ff' }}>{overview.total_lessons}</div>
                        <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.5)', marginTop: '4px' }}>{overview.completed_lessons} ukończonych</div>
                    </div>
                    <div style={{ padding: '16px', background: 'rgba(176, 0, 255, 0.05)', borderRadius: '12px', border: '1px solid rgba(176, 0, 255, 0.2)' }}>
                        <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.6)', marginBottom: '8px' }}>Engramy</div>
                        <div style={{ fontSize: '24px', fontWeight: 700, color: '#b000ff' }}>{overview.total_engrams}</div>
                        <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.5)', marginTop: '4px' }}>{overview.installed_engrams} zainstalowanych</div>
                    </div>
                </div>
            </div>
        </div>
    )
}
