'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation' // Add useSearchParams
import Link from 'next/link'
import { Bell, Zap, LayoutDashboard, Gamepad2, Folder, Flame } from 'lucide-react'
import PrzegladView from './components/PrzegladView'
import GryView from './components/GryView'
import ProjektyView from './components/ProjektyView'
import TreningView from './components/TreningView'

export default function PracticePage() {
    const { user, profile, loading: authLoading } = useAuth()
    const router = useRouter()
    const searchParams = useSearchParams() // Hook
    const activeTab = searchParams.get('view') || 'przeglad' // Get from URL
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
            {/* Content */}
            <div style={{ padding: '32px' }}>
                {activeTab === 'przeglad' && <PrzegladView />}
                {activeTab === 'trening' && <TreningView />}
                {activeTab === 'gry' && <GryView />}
                {activeTab === 'projekty' && <ProjektyView />}
            </div>
        </div>
    )
}
