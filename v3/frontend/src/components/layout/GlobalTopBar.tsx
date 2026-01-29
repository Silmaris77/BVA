'use client'

import { useAuth } from '@/contexts/AuthContext'
import { Zap, Bell, Flame, BookOpen, Brain, Library, LayoutDashboard, Gamepad2, Folder, User, TrendingUp, Target, LogOut, Menu, Wrench } from 'lucide-react'
import { useEffect, useState } from 'react'
import { ARCHETYPES } from '@/components/profile/EditProfileModal'
import { usePathname, useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'

export default function TopBar() {
    const { user, profile } = useAuth()
    const pathname = usePathname()
    const router = useRouter()
    const searchParams = useSearchParams()

    // State
    const [status, setStatus] = useState<{ streak: number, pending_missions: number } | null>(null)
    const [isMobile, setIsMobile] = useState(false)
    const [hoveredTab, setHoveredTab] = useState<string | null>(null)

    // Determine Context
    const isHub = pathname === '/'
    const isScience = pathname?.startsWith('/lessons') || pathname?.startsWith('/engrams') || pathname?.startsWith('/resources') || pathname?.startsWith('/tools')
    const isPractice = pathname?.startsWith('/practice')
    const isProfile = pathname?.startsWith('/profile')

    // On mobile, we hide the right-side stats (XP, Bell, Profile) UNLESS we are on the Hub
    const showStats = !isMobile || isHub

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

    // Tab Configurations
    const SCIENCE_TABS = [
        { id: 'lessons', label: 'Lekcje', href: '/lessons', icon: BookOpen, active: pathname?.startsWith('/lessons') },
        { id: 'engrams', label: 'Engramy', href: '/engrams', icon: Brain, active: pathname?.startsWith('/engrams') },
        { id: 'resources', label: 'Zasoby', href: '/resources', icon: Library, active: pathname?.startsWith('/resources') },
        { id: 'tools', label: 'Narzędzia', href: '/tools', icon: Wrench, active: pathname?.startsWith('/tools') }
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
                <div className="flex gap-2 overflow-x-auto pb-0">
                    {SCIENCE_TABS.map(tab => (
                        <Link
                            key={tab.id}
                            href={tab.href}
                            className={`nav-item-link nav-item-compact ${tab.active ? 'active' : ''}`}
                        >
                            <div className="relative z-[2] flex items-center gap-2">
                                <tab.icon size={16} />
                                {!isMobile && tab.label}
                            </div>
                        </Link>
                    ))}
                </div>
            )
        }

        if (isPractice) {
            const currentView = searchParams.get('view') || 'przeglad'
            return (
                <div className="flex gap-2 overflow-x-auto pb-0">
                    {PRACTICE_TABS.map(tab => {
                        const isActive = currentView === tab.value
                        return (
                            <Link
                                key={tab.id}
                                href={`/practice?view=${tab.value}`}
                                className={`nav-item-link nav-item-compact variant-purple ${isActive ? 'active' : ''}`}
                            >
                                <div className="relative z-[2] flex items-center gap-2">
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
                <div className="flex gap-2 overflow-x-auto pb-0">
                    {PROFILE_TABS.map(tab => {
                        const isActive = currentTab === tab.value
                        return (
                            <Link
                                key={tab.id}
                                href={`/profile?tab=${tab.value}`}
                                className={`nav-item-link nav-item-compact variant-purple ${isActive ? 'active' : ''}`}
                            >
                                <div className="relative z-[2] flex items-center gap-2">
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
        <div className="global-topbar sticky top-0 z-50 flex h-[65px] items-center justify-between px-8">
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
