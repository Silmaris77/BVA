'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Bell, Zap, LayoutDashboard, Gamepad2, Folder, Flame } from 'lucide-react'
import PrzegladView from './components/PrzegladView'
import GryView from './components/GryView'
import ProjektyView from './components/ProjektyView'
import TreningView from './components/TreningView'

export default function PracticePage() {
    const { user, profile, loading: authLoading } = useAuth()
    const router = useRouter()
    const [activeTab, setActiveTab] = useState('przeglad')
    const [isMobile, setIsMobile] = useState(false)

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
        if (!authLoading && !user) {
            router.push('/auth/login')
        }
    }, [user, authLoading, router])

    const [hoveredTab, setHoveredTab] = useState<string | null>(null)

    const tabs = [
        { id: 'przeglad', name: 'Przegląd', icon: LayoutDashboard },
        { id: 'trening', name: 'Trening', icon: Flame },
        { id: 'gry', name: 'Gry', icon: Gamepad2 },
        { id: 'projekty', name: 'Projekty', icon: Folder }
    ]

    if (authLoading) {
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

    return (
        <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
            {/* Sub-Nav Tabs */}
            <div style={{
                background: 'transparent',
                backdropFilter: 'blur(10px)',
                WebkitBackdropFilter: 'blur(10px)',
                borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
                padding: '16px 48px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'flex-start',
                position: 'sticky',
                top: '73px', // Below GlobalTopBar
                zIndex: 49
            }}>
                <div style={{
                    display: 'flex',
                    gap: isMobile ? '4px' : '8px',
                    overflowX: 'auto',
                    paddingBottom: isMobile ? '4px' : '0'
                }}>
                    {tabs.map(tab => {
                        const Icon = tab.icon
                        const isActive = activeTab === tab.id
                        const isHovered = hoveredTab === tab.id

                        return (
                            <div
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                onMouseEnter={() => setHoveredTab(tab.id)}
                                onMouseLeave={() => setHoveredTab(null)}
                                style={{
                                    padding: isMobile ? '10px' : '8px 16px',
                                    borderRadius: '8px',
                                    background: isActive
                                        ? 'rgba(176, 0, 255, 0.2)'
                                        : isHovered
                                            ? 'rgba(255, 255, 255, 0.05)'
                                            : 'transparent',
                                    border: isActive
                                        ? '1px solid #b000ff'
                                        : isHovered
                                            ? '1px solid rgba(255, 255, 255, 0.2)'
                                            : '1px solid transparent',
                                    color: isActive
                                        ? '#b000ff'
                                        : isHovered
                                            ? 'rgba(255, 255, 255, 0.9)'
                                            : 'rgba(255, 255, 255, 0.6)',
                                    fontSize: '13px',
                                    fontWeight: 600,
                                    cursor: 'pointer',
                                    fontFamily: 'Outfit, sans-serif',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
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
                                    <Icon size={isMobile ? 20 : 16} />
                                    {!isMobile && tab.name}
                                </div>
                            </div>
                        )
                    })}
                </div>
            </div>

            {/* Content Area */}
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                {activeTab === 'przeglad' && <PrzegladView />}
                {activeTab === 'trening' && <TreningView />}
                {activeTab === 'gry' && <GryView />}
                {activeTab === 'projekty' && <ProjektyView />}
            </div>
        </div>
    )
}
