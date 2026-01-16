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
            {/* Top Bar */}
            <div style={{
                background: 'rgba(0, 0, 0, 0.2)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
                padding: '16px 32px 16px 48px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                position: 'sticky',
                top: 0,
                zIndex: 50
            }}>
                {/* Main Tabs */}
                <div style={{
                    display: 'flex',
                    gap: isMobile ? '4px' : '8px',
                    flex: 1
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
                                    minHeight: isMobile ? '44px' : 'auto'
                                }}
                            >
                                <Icon size={isMobile ? 20 : 16} />
                                {!isMobile && tab.name}
                            </div>
                        )
                    })}
                </div>

                {/* Actions */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
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
                        position: 'relative'
                    }}>
                        <Bell size={20} />
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
                            justifyContent: 'center'
                        }}>3</div>
                    </div>

                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '6px 12px',
                        background: 'linear-gradient(135deg, #ffd700, #ff8800)',
                        borderRadius: '20px',
                        fontSize: '13px',
                        fontWeight: 700,
                        color: '#000'
                    }}>
                        <Zap size={16} />
                        <span>{profile?.xp || 0} XP</span>
                    </div>

                    <Link href="/profile" style={{
                        width: '40px',
                        height: '40px',
                        borderRadius: '50%',
                        background: 'linear-gradient(135deg, #667eea, #764ba2)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontWeight: 700,
                        fontSize: '14px',
                        cursor: 'pointer',
                        textDecoration: 'none',
                        color: 'white'
                    }}>
                        {profile?.full_name?.substring(0, 2).toUpperCase() || 'PA'}
                    </Link>
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
