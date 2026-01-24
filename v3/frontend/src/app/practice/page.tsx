'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Bell, Zap, LayoutDashboard, Gamepad2, Wrench, Folder, Flame } from 'lucide-react'
import PrzegladView from './components/PrzegladView'
import GryView from './components/GryView'
import NarzedziaView from './components/NarzedziaView'
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

    const tabs = [
        { id: 'przeglad', name: 'Przegląd', icon: LayoutDashboard },
        { id: 'gry', name: 'Gry', icon: Gamepad2 },
        { id: 'narzedzia', name: 'Narzędzia', icon: Wrench },
        { id: 'projekty', name: 'Projekty', icon: Folder },
        { id: 'trening', name: 'Trening', icon: Flame }
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
        <div style={{ minHeight: '100vh' }}>
            {/* Sub-Nav Tabs */}
            <div style={{
                background: 'rgba(0, 0, 0, 0.2)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
                padding: '16px 32px 16px 48px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'flex-start', // Left align tabs
                position: 'sticky',
                top: '73px', // Below GlobalTopBar (approx 73px)
                zIndex: 49
            }}>
                {/* Main Tabs */}
                <div style={{
                    display: 'flex',
                    gap: isMobile ? '4px' : '8px',
                    overflowX: 'auto',
                    paddingBottom: isMobile ? '4px' : '0'
                }}>
                    {tabs.map(tab => {
                        const Icon = tab.icon
                        const isActive = activeTab === tab.id

                        return (
                            <div
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                style={{
                                    padding: isMobile ? '10px' : '8px 16px',
                                    borderRadius: '8px',
                                    background: isActive ? 'rgba(176, 0, 255, 0.2)' : 'transparent',
                                    border: isActive ? '1px solid #b000ff' : '1px solid transparent',
                                    color: isActive ? '#b000ff' : 'rgba(255, 255, 255, 0.6)',
                                    fontSize: '13px',
                                    fontWeight: 600,
                                    cursor: 'pointer',
                                    fontFamily: 'Outfit, sans-serif',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    gap: '6px',
                                    transition: 'all 0.2s',
                                    minWidth: isMobile ? '44px' : 'auto', // Touch-friendly on mobile
                                    minHeight: isMobile ? '44px' : 'auto',
                                    whiteSpace: 'nowrap'
                                }}
                            >
                                <Icon size={isMobile ? 20 : 16} />
                                {!isMobile && tab.name}
                            </div>
                        )
                    })}
                </div>
            </div>

            {/* Content Area */}
            <div>
                {activeTab === 'przeglad' && <PrzegladView />}
                {activeTab === 'gry' && <GryView />}
                {activeTab === 'narzedzia' && <NarzedziaView />}
                {activeTab === 'projekty' && <ProjektyView />}
                {activeTab === 'trening' && <TreningView />}
            </div>
        </div>
    )
}
