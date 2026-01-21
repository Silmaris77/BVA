'use client'

import { Trophy, Star, Shield, Award } from 'lucide-react'
import confetti from 'canvas-confetti'
import { useEffect } from 'react'

interface AchievementCardProps {
    title: string
    description: string
    icon: 'trophy' | 'star' | 'shield' | 'award'
    level?: string
    xp?: number
}

const getIcon = (iconName: string) => {
    switch (iconName) {
        case 'trophy': return <Trophy size={80} strokeWidth={1.5} />
        case 'star': return <Star size={80} strokeWidth={1.5} />
        case 'shield': return <Shield size={80} strokeWidth={1.5} />
        case 'award': return <Award size={80} strokeWidth={1.5} />
        default: return <Trophy size={80} strokeWidth={1.5} />
    }
}

export default function AchievementCard({ title, description, icon = 'trophy', level = 'Level 1', xp = 100 }: AchievementCardProps) {

    useEffect(() => {
        // Trigger confetti on mount
        const duration = 3000
        const end = Date.now() + duration

        const frame = () => {
            confetti({
                particleCount: 3,
                angle: 60,
                spread: 55,
                origin: { x: 0 },
                colors: ['#ffd700', '#ffa500', '#ffffff']
            })
            confetti({
                particleCount: 3,
                angle: 120,
                spread: 55,
                origin: { x: 1 },
                colors: ['#ffd700', '#ffa500', '#ffffff']
            })

            if (Date.now() < end) {
                requestAnimationFrame(frame)
            }
        }
        frame()
    }, [])

    return (
        <div style={{
            maxWidth: '600px',
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            gap: '24px',
            alignItems: 'center'
        }}>
            <div style={{
                background: 'rgba(255, 215, 0, 0.15)',
                border: '2px solid #ffd700',
                borderRadius: '24px',
                padding: '40px',
                textAlign: 'center',
                animation: 'pulseGlow 2s infinite',
                width: '100%',
                position: 'relative',
                overflow: 'hidden'
            }}>
                <style jsx>{`
                    @keyframes pulseGlow { 
                        0%, 100% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.2); } 
                        50% { box-shadow: 0 0 50px rgba(255, 215, 0, 0.5); } 
                    }
                `}</style>

                {/* Shine effect background */}
                <div style={{
                    position: 'absolute',
                    top: '-50%',
                    left: '-50%',
                    width: '200%',
                    height: '200%',
                    background: 'radial-gradient(circle, rgba(255,215,0,0.2) 0%, rgba(0,0,0,0) 70%)',
                    zIndex: 0
                }} />

                <div style={{
                    position: 'relative',
                    zIndex: 1,
                    color: '#ffd700',
                    marginBottom: '20px',
                    display: 'flex',
                    justifyContent: 'center'
                }}>
                    {getIcon(icon)}
                </div>

                <div style={{
                    position: 'relative',
                    zIndex: 1,
                    fontSize: '14px',
                    fontWeight: 700,
                    textTransform: 'uppercase',
                    letterSpacing: '2px',
                    color: '#ff8800',
                    marginBottom: '10px'
                }}>
                    ODBLOKOWANO OSIĄGNIĘCIE
                </div>

                <h2 style={{
                    position: 'relative',
                    zIndex: 1,
                    fontSize: '28px',
                    fontWeight: 800,
                    color: '#fff',
                    marginBottom: '15px',
                    textShadow: '0 2px 10px rgba(0,0,0,0.5)'
                }}>
                    {title}
                </h2>

                <p style={{
                    position: 'relative',
                    zIndex: 1,
                    fontSize: '16px',
                    color: 'rgba(255, 255, 255, 0.8)',
                    marginBottom: '30px',
                    lineHeight: '1.6'
                }}>
                    {description}
                </p>

                <div style={{
                    position: 'relative',
                    zIndex: 1,
                    display: 'inline-flex',
                    gap: '15px',
                    background: 'rgba(0,0,0,0.3)',
                    padding: '10px 20px',
                    borderRadius: '12px',
                    border: '1px solid rgba(255,215,0,0.3)'
                }}>
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <span style={{ fontSize: '12px', color: 'rgba(255,255,255,0.5)' }}>POZIOM</span>
                        <span style={{ fontSize: '16px', fontWeight: 700, color: '#fff' }}>{level}</span>
                    </div>
                    <div style={{ width: '1px', background: 'rgba(255,255,255,0.2)' }} />
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <span style={{ fontSize: '12px', color: 'rgba(255,255,255,0.5)' }}>XP</span>
                        <span style={{ fontSize: '16px', fontWeight: 700, color: '#ffd700' }}>+{xp}</span>
                    </div>
                </div>
            </div>
        </div>
    )
}
