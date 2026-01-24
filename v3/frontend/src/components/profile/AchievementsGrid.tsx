'use client'

import { useEffect, useState } from 'react'
import { Trophy, Lock, Rocket, BookOpen, Zap, Flame, Brain, Sun, Moon, Award } from 'lucide-react'

// Icon mapping
const Icons: Record<string, any> = {
    Rocket, BookOpen, Zap, Flame, Brain, Sun, Moon, Trophy
}

interface Achievement {
    id: string
    title: string
    description: string
    icon: string
    xp_reward: number
    unlocked: boolean
    unlocked_at: string | null
    category: string
}

export default function AchievementsGrid() {
    const [achievements, setAchievements] = useState<Achievement[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function fetchAchievements() {
            try {
                const res = await fetch('/api/user/achievements')
                if (res.ok) {
                    const data = await res.json()
                    setAchievements(data)
                }
            } catch (error) {
                console.error('Failed to load achievements', error)
            } finally {
                setLoading(false)
            }
        }
        fetchAchievements()
    }, [])

    if (loading) {
        return <div style={{ color: 'rgba(255,255,255,0.4)', textAlign: 'center', padding: '20px' }}>Ładowanie odznak...</div>
    }

    // Helper: Sort unlocked first
    const sorted = [...achievements].sort((a, b) => {
        if (a.unlocked && !b.unlocked) return -1
        if (!a.unlocked && b.unlocked) return 1
        return 0
    })

    return (
        <div style={{
            background: 'rgba(20, 20, 35, 0.4)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            borderRadius: '20px',
            padding: '24px',
            marginBottom: '32px'
        }}>
            <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Award size={20} color="#ffd700" />
                Osiągnięcia ({achievements.filter(a => a.unlocked).length}/{achievements.length})
            </h3>

            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))',
                gap: '16px'
            }}>
                {sorted.map(achievement => {
                    const IconComponent = Icons[achievement.icon] || Trophy

                    return (
                        <div key={achievement.id} style={{
                            background: achievement.unlocked
                                ? 'linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03))'
                                : 'rgba(0, 0, 0, 0.2)',
                            border: achievement.unlocked
                                ? '1px solid rgba(255, 215, 0, 0.3)'
                                : '1px solid rgba(255, 255, 255, 0.05)',
                            borderRadius: '16px',
                            padding: '16px',
                            textAlign: 'center',
                            opacity: achievement.unlocked ? 1 : 0.5,
                            transition: 'all 0.3s',
                            position: 'relative',
                            overflow: 'hidden'
                        }}>
                            {/* Icon */}
                            <div style={{
                                width: '48px',
                                height: '48px',
                                borderRadius: '12px',
                                background: achievement.unlocked ? 'rgba(255, 215, 0, 0.1)' : 'rgba(255, 255, 255, 0.05)',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                margin: '0 auto 12px',
                                color: achievement.unlocked ? '#ffd700' : 'rgba(255, 255, 255, 0.3)'
                            }}>
                                <IconComponent size={24} />
                            </div>

                            {/* Badge Info */}
                            <div style={{ fontSize: '13px', fontWeight: 600, color: 'white', marginBottom: '4px' }}>
                                {achievement.title}
                            </div>
                            <div style={{ fontSize: '11px', color: 'rgba(255, 255, 255, 0.5)', lineHeight: '1.4' }}>
                                {achievement.description}
                            </div>

                            {/* Reward Pill */}
                            <div style={{
                                marginTop: '12px',
                                display: 'inline-block',
                                padding: '2px 8px',
                                borderRadius: '99px',
                                background: achievement.unlocked ? 'rgba(255, 215, 0, 0.2)' : 'rgba(255, 255, 255, 0.05)',
                                fontSize: '10px',
                                fontWeight: 700,
                                color: achievement.unlocked ? '#ffd700' : 'rgba(255, 255, 255, 0.3)'
                            }}>
                                +{achievement.xp_reward} XP
                            </div>

                            {/* Locked Overlay Icon */}
                            {!achievement.unlocked && (
                                <div style={{
                                    position: 'absolute',
                                    top: '8px',
                                    right: '8px',
                                    opacity: 0.3
                                }}>
                                    <Lock size={12} />
                                </div>
                            )}
                        </div>
                    )
                })}
            </div>
        </div>
    )
}
