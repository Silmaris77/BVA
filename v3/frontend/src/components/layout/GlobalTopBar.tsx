'use client'

import { useAuth } from '@/contexts/AuthContext'
import { Zap, Bell, Flame, BookOpen, Brain, Library, LayoutDashboard, Gamepad2, Folder, User, TrendingUp, Target, LogOut, Menu } from 'lucide-react'
import { useEffect, useState } from 'react'
import { ARCHETYPES } from '@/components/profile/EditProfileModal'
import { usePathname, useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'

export default function TopBar() {
    const { user, profile } = useAuth()
    const pathname = usePathname()
    const router = useRouter()
    const searchParams = useSearchParams()
    const [status, setStatus] = useState<{ streak: number, pending_missions: number } | null>(null)
    const [isMobile, setIsMobile] = useState(false)
    const [hoveredTab, setHoveredTab] = useState<string | null>(null)

    // Detect mobile screen size
    useEffect(() => {
        const checkMobile = () => {
            setIsMobile(window.innerWidth <= 768)
        }
        checkMobile()
        window.addEventListener('resize', checkMobile)
        return () => window.removeEventListener('resize', checkMobile)
    }, [])

    useEffect(() => {
        if (!user) return

        const fetchStatus = async () => {
            try {
                const res = await fetch('/api/status')
                if (res.ok) {
                    setStatus(await res.json())
                }
            } catch (e) {
                console.error('TopBar status fetch error', e)
            }
        }

        fetchStatus()
        // Optional: Poll every minute
        const interval = setInterval(fetchStatus, 60000)
        return () => clearInterval(interval)
    }, [user])

    if (!user) return null

    // Determine Context
    const isHub = pathname === '/'
    const isScience = pathname?.startsWith('/lessons') || pathname?.startsWith('/engrams') || pathname?.startsWith('/resources')
    const isPractice = pathname?.startsWith('/practice')
    const isProfile = pathname?.startsWith('/profile')

    // On mobile, we hide the right-side stats (XP, Bell, Profile) UNLESS we are on the Hub
    const showStats = !isMobile || isHub

    // Tab Configurations
    const SCIENCE_TABS = [
        { id: 'lessons', label: 'Lekcje', href: '/lessons', icon: BookOpen, active: pathname?.startsWith('/lessons') },
        { id: 'engrams', label: 'Engramy', href: '/engrams', icon: Brain, active: pathname?.startsWith('/engrams') },
        { id: 'resources', label: 'Zasoby', href: '/resources', icon: Library, active: pathname?.startsWith('/resources') }
    ]

    const PRACTICE_TABS = [
        { id: 'przeglad', label: 'Przegląd', value: 'przeglad', icon: LayoutDashboard },
        { id: 'trening', label: 'Trening', value: 'trening', icon: Flame },
        { id: 'gry', label: 'Gry', value: 'gry', icon: Gamepad2 },
        { id: 'projekty', label: 'Projekty', value: 'projekty', icon: Folder }
    ]

    const PROFILE_TABS = [
        { id: 'informacje', label: 'Informacje', value: 'informacje', icon: User },
        { id: 'postepy', label: 'Postępy', value: 'postepy', icon: TrendingUp },
        { id: 'cele', label: 'Cele', value: 'cele', icon: Target },
        { id: 'ustawienia', label: 'Ustawienia', value: 'ustawienia', icon: LogOut }
    ]

    // Render Tabs Helper
    const renderTabs = () => {
        if (isScience) {
            return (
                <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '0px' }}>
                    {SCIENCE_TABS.map(tab => {
                        const isHovered = hoveredTab === tab.id
                        return (
                            <Link
                                key={tab.id}
                                href={tab.href}
                                onMouseEnter={() => setHoveredTab(tab.id)}
                                onMouseLeave={() => setHoveredTab(null)}
                                style={{
                                    padding: isMobile ? '8px' : '8px 16px',
                                    borderRadius: '8px',
                                    background: tab.active ? 'rgba(0, 212, 255, 0.15)' : isHovered ? 'rgba(255, 255, 255, 0.05)' : 'transparent',
                                    border: tab.active ? '1px solid #00d4ff' : isHovered ? '1px solid rgba(255, 255, 255, 0.2)' : '1px solid transparent',
                                    color: tab.active ? '#00d4ff' : isHovered ? 'rgba(255, 255, 255, 0.9)' : 'rgba(255, 255, 255, 0.6)',
                                    boxShadow: tab.active ? '0 0 20px rgba(0, 212, 255, 0.2)' : 'none',
                                    fontSize: '13px',
                                    fontWeight: 600,
                                    textDecoration: 'none',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '6px',
                                    transition: 'all 0.2s',
                                    whiteSpace: 'nowrap',
                                    position: 'relative',
                                    overflow: 'hidden'
                                }}
                            >
                                <div
                                    style={{
                                        position: 'absolute',
                                        top: 0,
                                        left: isHovered && !tab.active ? '100%' : '-100%',
                                        width: '100%',
                                        height: '100%',
                                        background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent)',
                                        transition: isHovered && !tab.active ? 'left 0.5s ease' : 'none',
                                        pointerEvents: 'none',
                                        zIndex: 1
                                    }}
                                />
                                <div style={{ position: 'relative', zIndex: 2, display: 'flex', alignItems: 'center', gap: '6px' }}>
                                    <tab.icon size={16} />
                                    {!isMobile && tab.label}
                                </div>
                            </Link>
                        )
                    })}
                </div>
            )
        }

        if (isPractice) {
            const currentView = searchParams.get('view') || 'przeglad'
            return (
                <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '0px' }}>
                    {PRACTICE_TABS.map(tab => {
                        const isActive = currentView === tab.value
                        const isHovered = hoveredTab === tab.id
                        return (
                            <Link
                                key={tab.id}
                                href={`/practice?view=${tab.value}`}
                                onMouseEnter={() => setHoveredTab(tab.id)}
                                onMouseLeave={() => setHoveredTab(null)}
                                style={{
                                    padding: isMobile ? '8px' : '8px 16px',
                                    borderRadius: '8px',
                                    background: isActive ? 'rgba(176, 0, 255, 0.15)' : isHovered ? 'rgba(255, 255, 255, 0.05)' : 'transparent',
                                    border: isActive ? '1px solid #b000ff' : isHovered ? '1px solid rgba(255, 255, 255, 0.2)' : '1px solid transparent',
                                    color: isActive ? '#b000ff' : isHovered ? 'rgba(255, 255, 255, 0.9)' : 'rgba(255, 255, 255, 0.6)',
                                    boxShadow: isActive ? '0 0 20px rgba(176, 0, 255, 0.2)' : 'none',
                                    fontSize: '13px',
                                    fontWeight: 600,
                                    textDecoration: 'none',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '6px',
                                    transition: 'all 0.2s',
                                    whiteSpace: 'nowrap',
                                    position: 'relative',
                                    overflow: 'hidden'
                                }}
                            >
                                <div
                                    style={{
                                        position: 'absolute',
                                        top: 0,
                                        left: isHovered && !isActive ? '100%' : '-100%',
                                        width: '100%',
                                        height: '100%',
                                        background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent)',
                                        transition: isHovered && !isActive ? 'left 0.5s ease' : 'none',
                                        pointerEvents: 'none',
                                        zIndex: 1
                                    }}
                                />
                                <div style={{ position: 'relative', zIndex: 2, display: 'flex', alignItems: 'center', gap: '6px' }}>
                                    <tab.icon size={16} />
                                    {!isMobile && tab.label}
                                </div>
                            </Link>
                        )
                    })}
                </div>
            )
        }

        if (isProfile) {
            const currentTab = searchParams.get('tab') || 'informacje'
            return (
                <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '0px' }}>
                    {PROFILE_TABS.map(tab => {
                        const isActive = currentTab === tab.value
                        const isHovered = hoveredTab === tab.id
                        return (
                            <Link
                                key={tab.id}
                                href={`/profile?tab=${tab.value}`}
                                onMouseEnter={() => setHoveredTab(tab.id)}
                                onMouseLeave={() => setHoveredTab(null)}
                                style={{
                                    padding: isMobile ? '8px' : '8px 16px',
                                    borderRadius: '8px',
                                    background: isActive ? 'rgba(176, 0, 255, 0.15)' : isHovered ? 'rgba(255, 255, 255, 0.05)' : 'transparent',
                                    border: isActive ? '1px solid #b000ff' : isHovered ? '1px solid rgba(255, 255, 255, 0.2)' : '1px solid transparent',
                                    color: isActive ? '#b000ff' : isHovered ? 'rgba(255, 255, 255, 0.9)' : 'rgba(255, 255, 255, 0.6)',
                                    boxShadow: isActive ? '0 0 20px rgba(176, 0, 255, 0.2)' : 'none',
                                    fontSize: '13px',
                                    fontWeight: 600,
                                    textDecoration: 'none',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '6px',
                                    transition: 'all 0.2s',
                                    whiteSpace: 'nowrap',
                                    position: 'relative',
                                    overflow: 'hidden'
                                }}
                            >
                                <div
                                    style={{
                                        position: 'absolute',
                                        top: 0,
                                        left: isHovered && !isActive ? '100%' : '-100%',
                                        width: '100%',
                                        height: '100%',
                                        background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent)',
                                        transition: isHovered && !isActive ? 'left 0.5s ease' : 'none',
                                        pointerEvents: 'none',
                                        zIndex: 1
                                    }}
                                />
                                <div style={{ position: 'relative', zIndex: 2, display: 'flex', alignItems: 'center', gap: '6px' }}>
                                    <tab.icon size={16} />
                                    {!isMobile && tab.label}
                                </div>
                            </Link>
                        )
                    })}
                </div>
            )
        }

        return null
    }

    return (
        <div style={{
            background: 'rgba(0, 0, 0, 0.2)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
            padding: '0 32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between', // Changed to space-between
            position: 'sticky',
            top: 0,
            zIndex: 50,
            marginBottom: '0',
            height: '65px' // Enforce height for alignment
        }}>
            {/* LEFT SIDE: Navigation Tabs */}
            <div style={{ flex: 1, overflow: 'hidden', marginLeft: '16px' }}>
                {renderTabs()}
            </div>

            {/* RIGHT SIDE: Stats & Profile (Conditional on Mobile) */}
            {showStats && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginLeft: '16px' }}>
                    {/* Streak Widget */}
                    <div style={{
                        height: '40px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '0 16px',
                        background: 'rgba(255, 68, 68, 0.1)',
                        border: '1px solid rgba(255, 68, 68, 0.2)',
                        borderRadius: '20px',
                        fontSize: '13px',
                        fontWeight: 700,
                        color: '#ff4444',
                        whiteSpace: 'nowrap'
                    }} title="Dni z rzędu">
                        <Flame size={16} fill="#ff4444" />
                        <span>{status?.streak || 0}</span>
                    </div>

                    {/* XP Badge */}
                    <div style={{
                        height: '40px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '0 16px',
                        background: 'linear-gradient(135deg, #ffd700, #ff8800)',
                        borderRadius: '20px',
                        fontSize: '13px',
                        fontWeight: 700,
                        color: '#000',
                        whiteSpace: 'nowrap'
                    }}>
                        <Zap size={16} />
                        <span>{profile?.xp || 0} XP</span>
                    </div>

                    {/* Notifications (Pending Missions) */}
                    <div style={{
                        width: '40px',
                        height: '40px',
                        borderRadius: '12px',
                        background: 'rgba(255, 255, 255, 0.05)',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        cursor: 'pointer',
                        position: 'relative',
                        flexShrink: 0
                    }}>
                        <Bell size={20} />
                        {status?.pending_missions && status.pending_missions > 0 ? (
                            <div style={{
                                position: 'absolute',
                                top: '-4px',
                                right: '-4px',
                                width: '18px',
                                height: '18px',
                                background: '#ff0055',
                                borderRadius: '50%',
                                fontSize: '10px',
                                fontWeight: 700,
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                border: '2px solid #13131f'
                            }}>
                                {status.pending_missions}
                            </div>
                        ) : null}
                    </div>

                    {/* Profile */}
                    <div style={{
                        width: '40px',
                        height: '40px',
                        borderRadius: '50%',
                        background: 'linear-gradient(135deg, #b000ff, #00d4ff)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontWeight: 700,
                        cursor: 'pointer',
                        border: '2px solid rgba(255,255,255,0.2)',
                        overflow: 'hidden',
                        flexShrink: 0
                    }}>
                        {(() => {
                            const archetype = ARCHETYPES.find(a => a.id === profile?.avatar_url)
                            if (archetype) {
                                const Icon = archetype.icon
                                return <Icon size={24} color="white" />
                            }
                            return profile?.full_name?.substring(0, 2).toUpperCase() || 'U'
                        })()}
                    </div>
                </div>
            )}
        </div>
    )
}
