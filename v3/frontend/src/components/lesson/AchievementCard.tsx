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
    stats?: { value: string; label: string }[]
    badge?: string
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

export default function AchievementCard({
    title,
    description,
    icon = 'trophy',
    level = 'Level 1',
    xp = 100,
    stats,
    badge
}: AchievementCardProps) {

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

    // New Layout for Lesson Completion (if stats are present)
    if (stats && stats.length > 0) {
        return (
            <div style={{
                maxWidth: '800px',
                width: '100%',
                display: 'flex',
                flexDirection: 'column',
                gap: '32px',
                alignItems: 'center',
                textAlign: 'center'
            }}>
                {/* Icon */}
                <div style={{
                    marginBottom: '10px',
                    filter: 'drop-shadow(0 0 20px rgba(255, 215, 0, 0.4))',
                    animation: 'float 3s ease-in-out infinite'
                }}>
                    <style jsx>{`
                        @keyframes float {
                            0%, 100% { transform: translateY(0); }
                            50% { transform: translateY(-10px); }
                        }
                    `}</style>
                    {getIcon(icon)}
                </div>

                {/* Title */}
                <div>
                    <h1 style={{
                        fontSize: '42px',
                        fontWeight: 900,
                        color: '#ffd700',
                        marginBottom: '16px',
                        textShadow: '0 0 20px rgba(255, 215, 0, 0.5)',
                        lineHeight: 1.2
                    }}>
                        {title}
                    </h1>
                    <p style={{
                        fontSize: '18px',
                        color: 'rgba(255, 255, 255, 0.9)',
                        maxWidth: '600px',
                        margin: '0 auto'
                    }}>
                        {description}
                    </p>
                </div>

                {/* Stats Grid */}
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(3, 1fr)',
                    gap: '20px',
                    width: '100%',
                    marginTop: '20px'
                }}>
                    {stats.map((stat, index) => (
                        <div key={index} style={{
                            background: 'rgba(20, 20, 30, 0.6)',
                            border: '1px solid rgba(255, 255, 255, 0.1)',
                            borderRadius: '16px',
                            padding: '30px 20px',
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            justifyContent: 'center',
                            gap: '10px'
                        }}>
                            <span style={{
                                fontSize: '48px',
                                fontWeight: 800,
                                color: '#ffd700',
                                lineHeight: 1
                            }}>
                                {stat.value}
                            </span>
                            <span style={{
                                fontSize: '14px',
                                color: 'rgba(255, 255, 255, 0.7)',
                                fontWeight: 500
                            }}>
                                {stat.label}
                            </span>
                        </div>
                    ))}
                </div>

                {/* Badge Footer */}
                {badge && (
                    <div style={{
                        marginTop: '20px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        fontSize: '18px',
                        fontWeight: 700,
                        color: '#ffd700'
                    }}>
                        <Award size={24} />
                        <span>{badge}</span>
                    </div>
                )}
            </div>
        )
    }

    // Default Layout (Backward Compatibility)
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
