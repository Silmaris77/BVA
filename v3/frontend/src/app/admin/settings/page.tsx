'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Settings as SettingsIcon, ArrowLeft, Save, AlertTriangle } from 'lucide-react'

export default function AdminSettingsPage() {
    const { user, loading: authLoading } = useAuth()
    const router = useRouter()
    const [isAdmin, setIsAdmin] = useState(false)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function checkAdmin() {
            if (!user) return
            try {
                const response = await fetch('/api/admin/analytics')
                setIsAdmin(response.ok)
            } catch (error) {
                setIsAdmin(false)
            } finally {
                setLoading(false)
            }
        }
        if (!authLoading) checkAdmin()
    }, [user, authLoading])

    useEffect(() => {
        if (!authLoading && !loading && (!user || !isAdmin)) {
            router.push('/admin')
        }
    }, [user, isAdmin, authLoading, loading, router])

    if (authLoading || loading) {
        return <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'rgba(255, 255, 255, 0.6)' }}>Ładowanie...</div>
    }

    if (!user || !isAdmin) return null

    return (
        <div style={{ minHeight: '100vh', padding: '32px 48px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '32px' }}>
                <Link href="/admin" style={{ width: '40px', height: '40px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'rgba(255, 255, 255, 0.8)' }}>
                    <ArrowLeft size={20} />
                </Link>
                <div style={{ width: '48px', height: '48px', background: 'rgba(255, 136, 0, 0.2)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#ff8800' }}>
                    <SettingsIcon size={24} />
                </div>
                <div>
                    <h1 style={{ fontSize: '24px', fontWeight: 700 }}>Ustawienia Platformy</h1>
                    <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px' }}>Globalna konfiguracja BrainVenture</p>
                </div>
            </div>

            {/* Platform Info */}
            <div style={{ background: 'rgba(20, 20, 35, 0.4)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '16px', padding: '24px', marginBottom: '24px' }}>
                <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '16px' }}>Informacje o platformie</h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                    <div>
                        <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.5)', marginBottom: '4px' }}>Nazwa platformy</div>
                        <div style={{ fontSize: '14px', fontWeight: 600 }}>BrainVenture V3</div>
                    </div>
                    <div>
                        <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.5)', marginBottom: '4px' }}>Wersja</div>
                        <div style={{ fontSize: '14px', fontWeight: 600 }}>3.0.0</div>
                    </div>
                </div>
            </div>

            {/* XP Settings */}
            <div style={{ background: 'rgba(20, 20, 35, 0.4)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '16px', padding: '24px', marginBottom: '24px' }}>
                <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '16px' }}>Ustawienia XP</h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                    <div>
                        <label style={{ display: 'block', fontSize: '13px', color: 'rgba(255, 255, 255, 0.7)', marginBottom: '8px' }}>Domyślne XP za lekcję</label>
                        <input type="number" defaultValue={150} style={{ width: '100%', padding: '10px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }} />
                    </div>
                    <div>
                        <label style={{ display: 'block', fontSize: '13px', color: 'rgba(255, 255, 255, 0.7)', marginBottom: '8px' }}>Domyślne XP za engram (instalacja)</label>
                        <input type="number" defaultValue={50} style={{ width: '100%', padding: '10px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }} />
                    </div>
                    <div>
                        <label style={{ display: 'block', fontSize: '13px', color: 'rgba(255, 255, 255, 0.7)', marginBottom: '8px' }}>Domyślne XP za engram (refresh)</label>
                        <input type="number" defaultValue={25} style={{ width: '100%', padding: '10px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }} />
                    </div>
                    <div>
                        <label style={{ display: 'block', fontSize: '13px', color: 'rgba(255, 255, 255, 0.7)', marginBottom: '8px' }}>Domyślne XP za tool</label>
                        <input type="number" defaultValue={50} style={{ width: '100%', padding: '10px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }} />
                    </div>
                </div>
            </div>

            {/* Feature Flags */}
            <div style={{ background: 'rgba(20, 20, 35, 0.4)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '16px', padding: '24px', marginBottom: '24px' }}>
                <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '16px' }}>Funkcje platformy</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    {[
                        { label: 'Spaced Repetition dla engramów', enabled: true },
                        { label: 'System poziomów i odznak', enabled: false },
                        { label: 'Tryb praktyki', enabled: false },
                        { label: 'Text-to-Speech', enabled: false }
                    ].map((feature, i) => (
                        <div key={i} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px', background: 'rgba(255, 255, 255, 0.02)', borderRadius: '8px' }}>
                            <span style={{ fontSize: '14px' }}>{feature.label}</span>
                            <div style={{ width: '48px', height: '24px', background: feature.enabled ? '#00ff88' : 'rgba(255, 255, 255, 0.1)', borderRadius: '12px', position: 'relative', cursor: 'pointer' }}>
                                <div style={{ width: '20px', height: '20px', background: 'white', borderRadius: '50%', position: 'absolute', top: '2px', left: feature.enabled ? '26px' : '2px', transition: 'left 0.2s' }} />
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Save Button */}
            <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
                <button style={{ padding: '12px 24px', background: 'linear-gradient(135deg, #00ff88, #00cc66)', border: 'none', borderRadius: '12px', color: 'white', fontSize: '14px', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Save size={18} />
                    Zapisz zmiany
                </button>
            </div>

            {/* Warning */}
            <div style={{ marginTop: '24px', padding: '16px', background: 'rgba(255, 136, 0, 0.1)', border: '1px solid rgba(255, 136, 0, 0.3)', borderRadius: '12px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                <AlertTriangle size={20} style={{ color: '#ff8800' }} />
                <span style={{ fontSize: '13px', color: 'rgba(255, 255, 255, 0.8)' }}>
                    Zmiany w ustawieniach globalnych wpływają na całą platformę. Upewnij się przed zapisaniem.
                </span>
            </div>
        </div>
    )
}
