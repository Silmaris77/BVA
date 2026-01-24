'use client'

import { useAuth } from '@/contexts/AuthContext'
import { Zap, Bell, Flame } from 'lucide-react'
import { useEffect, useState } from 'react'

export default function TopBar() {
    const { user, profile } = useAuth()
    const [status, setStatus] = useState<{ streak: number, pending_missions: number } | null>(null)

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

    return (
        <div style={{
            background: 'rgba(0, 0, 0, 0.2)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
            padding: '16px 32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'flex-end',
            position: 'sticky',
            top: 0,
            zIndex: 50,
            marginBottom: '0'
        }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                {/* Streak Widget */}
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '6px 12px',
                    background: 'rgba(255, 68, 68, 0.1)',
                    border: '1px solid rgba(255, 68, 68, 0.2)',
                    borderRadius: '20px',
                    fontSize: '13px',
                    fontWeight: 700,
                    color: '#ff4444'
                }} title="Dni z rzędu">
                    <Flame size={16} fill="#ff4444" />
                    <span>{status?.streak || 0}</span>
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
                    position: 'relative'
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
                            justifyContent: 'center'
                        }}>
                            {status.pending_missions}
                        </div>
                    ) : null}
                </div>

                {/* XP Badge */}
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
                    cursor: 'pointer'
                }}>
                    {profile?.full_name?.substring(0, 2).toUpperCase() || 'U'}
                </div>
            </div>
        </div>
    )
}
