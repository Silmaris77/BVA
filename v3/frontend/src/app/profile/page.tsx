'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useRouter } from 'next/navigation'
import { useState } from 'react'
import { User, Bell, Zap, Trophy, Flame, Target, LogOut, TrendingUp, Award, Rocket, BookOpen, Sparkles, Star } from 'lucide-react'

export default function ProfilePage() {
    const { user, profile, signOut } = useAuth()
    const router = useRouter()
    const [activeTab, setActiveTab] = useState<'informacje' | 'postepy' | 'cele' | 'ustawienia'>('informacje')

    if (!user) return null

    const handleSignOut = async () => {
        await signOut()
        router.push('/auth/login')
    }

    const levelName = (level: number) => {
        const names = ['Recruit', 'Analyst', 'Associate', 'Manager', 'Director', 'VP', 'SVP', 'Executive', 'Strategist', 'Master']
        return names[Math.min(level - 1, names.length - 1)] || 'Recruit'
    }

    return (
        <div style={{ minHeight: '100vh' }}>
            {/* Top Bar with Tabs */}
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
                {/* Tabs on Left */}
                <div style={{ display: 'flex', gap: '8px', flex: 1 }}>
                    {(['informacje', 'postepy', 'cele', 'ustawienia'] as const).map(tab => (
                        <button
                            key={tab}
                            onClick={() => setActiveTab(tab)}
                            style={{
                                padding: '8px 16px',
                                borderRadius: '8px',
                                background: activeTab === tab ? 'rgba(176, 0, 255, 0.2)' : 'transparent',
                                border: activeTab === tab ? '1px solid #b000ff' : '1px solid transparent',
                                color: activeTab === tab ? '#b000ff' : 'rgba(255, 255, 255, 0.6)',
                                fontSize: '13px',
                                fontWeight: 600,
                                cursor: 'pointer',
                                fontFamily: 'Outfit, sans-serif',
                                textTransform: 'capitalize',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '6px',
                                transition: 'all 0.2s'
                            }}
                        >
                            {tab === 'informacje' && <User size={16} />}
                            {tab === 'postepy' && <TrendingUp size={16} />}
                            {tab === 'cele' && <Target size={16} />}
                            {tab === 'ustawienia' && <LogOut size={16} />}
                            {tab}
                        </button>
                    ))}
                </div>

                {/* Actions on Right */}
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
                </div>
            </div>

            {/* Content */}
            <div style={{ padding: '48px 32px 32px 48px' }}>
                {activeTab === 'informacje' && (
                    <>
                        {/* Enhanced Profile Header */}
                        <div style={{
                            background: 'rgba(20, 20, 35, 0.4)',
                            backdropFilter: 'blur(20px)',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            borderRadius: '20px',
                            padding: '32px',
                            marginBottom: '32px',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '32px'
                        }}>
                            {/* Avatar */}
                            <div style={{
                                width: '120px',
                                height: '120px',
                                borderRadius: '50%',
                                background: 'linear-gradient(135deg, #b000ff, #00d4ff)',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontSize: '48px',
                                fontWeight: 700,
                                border: '4px solid rgba(176, 0, 255, 0.3)',
                                boxShadow: '0 0 40px rgba(176, 0, 255, 0.4)',
                                flexShrink: 0
                            }}>
                                {profile?.full_name?.substring(0, 2).toUpperCase() || 'PK'}
                            </div>

                            {/* Info */}
                            <div style={{ flex: 1 }}>
                                <h1 style={{ fontSize: '32px', fontWeight: 700, marginBottom: '4px' }}>
                                    {profile?.full_name || 'Piotr Kowalski'}
                                </h1>
                                <p style={{ fontSize: '15px', color: 'rgba(255, 255, 255, 0.6)', marginBottom: '16px' }}>
                                    {levelName(profile?.level || 1)} • Członek od stycznia 2024
                                </p>

                                <div style={{
                                    display: 'inline-flex',
                                    alignItems: 'center',
                                    gap: '8px',
                                    padding: '8px 20px',
                                    background: 'linear-gradient(135deg, #ffd700, #ff8800)',
                                    borderRadius: '24px',
                                    fontSize: '15px',
                                    fontWeight: 700,
                                    color: '#000'
                                }}>
                                    <Trophy size={18} />
                                    Level {profile?.level || 8} • {(profile?.xp || 2450).toLocaleString()} XP
                                </div>
                            </div>
                        </div>

                        {/* 4 Mini Stats Cards */}
                        <div style={{
                            display: 'grid',
                            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                            gap: '16px',
                            marginBottom: '32px'
                        }}>
                            <MiniStatCard icon={<BookOpen size={20} />} value="12" label="Ukończone lekcje" color="purple" />
                            <MiniStatCard icon={<Flame size={20} />} value="7 dni" label="Streak" color="orange" />
                            <MiniStatCard icon={<Award size={20} />} value="8" label="Odznaki" color="cyan" />
                            <MiniStatCard icon={<Trophy size={20} />} value="#8" label="Ranking" color="gold" />
                        </div>

                        {/* Zdobyte Odznaki */}
                        <div style={{
                            background: 'rgba(20, 20, 35, 0.4)',
                            backdropFilter: 'blur(20px)',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            borderRadius: '20px',
                            padding: '24px',
                            marginBottom: '32px'
                        }}>
                            <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                                🏆 Zdobyte Odznaki
                            </h3>
                            <div style={{
                                display: 'grid',
                                gridTemplateColumns: 'repeat(auto-fill, minmax(80px, 1fr))',
                                gap: '16px'
                            }}>
                                <BadgeItem icon={<Rocket />} label="First Steps" color="#00d4ff" />
                                <BadgeItem icon={<BookOpen />} label="Knowledge Seeker" color="#b000ff" />
                                <BadgeItem icon={<Flame />} label="7-Day Streak" color="#ff8800" />
                                <BadgeItem icon={<Zap />} label="Fast Learner" color="#ffd700" />
                                <BadgeItem icon={<Sparkles />} label="Premium Member" color="#00d4ff" />
                                <BadgeItem icon={<Target />} label="Graduate" color="#00ff88" />
                                <BadgeItem icon={<Trophy />} label="Achiever" color="#ffd700" />
                                <BadgeItem icon={<Star />} label="All-Star" color="#ff8800" />
                            </div>
                        </div>

                        {/* Moje Kompetencje (Placeholder for Radar Chart) */}
                        <div style={{
                            background: 'rgba(20, 20, 35, 0.4)',
                            backdropFilter: 'blur(20px)',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            borderRadius: '20px',
                            padding: '24px',
                            marginBottom: '32px'
                        }}>
                            <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                                📊 Moje Kompetencje
                            </h3>
                            <div style={{
                                height: '300px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                color: 'rgba(255, 255, 255, 0.4)',
                                fontSize: '14px'
                            }}>
                                📊 Radar chart kompetencji (wymaga Chart.js - Day 8)
                            </div>
                        </div>

                        {/* Aktywne Cele */}
                        <div style={{
                            background: 'rgba(20, 20, 35, 0.4)',
                            backdropFilter: 'blur(20px)',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            borderRadius: '20px',
                            padding: '24px'
                        }}>
                            <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                                🎯 Aktywne Cele
                            </h3>
                            <GoalItem title="Ukończ 15 lekcji w styczniu" progress={80} current={12} target={15} />
                            <GoalItem title="Osiągnij Level 10" progress={48} current={2450} target={5000} unit="XP" />
                            <GoalItem title="30-dniowy streak nauki" progress={23} current={7} target={30} />
                        </div>
                    </>
                )}

                {activeTab === 'postepy' && (
                    <div style={{
                        background: 'rgba(20, 20, 35, 0.4)',
                        backdropFilter: 'blur(20px)',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        borderRadius: '20px',
                        padding: '32px',
                        textAlign: 'center',
                        color: 'rgba(255, 255, 255, 0.6)'
                    }}>
                        <p>📊 Szczegółowe wykresy postępów będą dostępne wkrótce</p>
                    </div>
                )}

                {activeTab === 'cele' && (
                    <div style={{
                        background: 'rgba(20, 20, 35, 0.4)',
                        backdropFilter: 'blur(20px)',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        borderRadius: '20px',
                        padding: '32px',
                        textAlign: 'center',
                        color: 'rgba(255, 255, 255, 0.6)'
                    }}>
                        <p>🎯 System celów będzie dostępny wkrótce</p>
                    </div>
                )}

                {activeTab === 'ustawienia' && (
                    <div style={{
                        background: 'rgba(20, 20, 35, 0.4)',
                        backdropFilter: 'blur(20px)',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        borderRadius: '20px',
                        padding: '32px'
                    }}>
                        <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '24px' }}>Ustawienia konta</h3>

                        <div style={{ marginBottom: '24px' }}>
                            <label style={{ display: 'block', fontSize: '13px', color: 'rgba(255, 255, 255, 0.6)', marginBottom: '8px' }}>
                                Email
                            </label>
                            <input
                                type="email"
                                value={user.email || ''}
                                disabled
                                style={{
                                    width: '100%',
                                    padding: '12px 16px',
                                    background: 'rgba(255, 255, 255, 0.03)',
                                    border: '1px solid rgba(255, 255, 255, 0.08)',
                                    borderRadius: '12px',
                                    color: 'rgba(255, 255, 255, 0.5)',
                                    fontFamily: 'Outfit, sans-serif',
                                    fontSize: '14px'
                                }}
                            />
                        </div>

                        <div style={{ marginBottom: '32px' }}>
                            <label style={{ display: 'block', fontSize: '13px', color: 'rgba(255, 255, 255, 0.6)', marginBottom: '8px' }}>
                                Imię i nazwisko
                            </label>
                            <input
                                type="text"
                                value={profile?.full_name || ''}
                                disabled
                                style={{
                                    width: '100%',
                                    padding: '12px 16px',
                                    background: 'rgba(255, 255, 255, 0.05)',
                                    border: '1px solid rgba(255, 255, 255, 0.08)',
                                    borderRadius: '12px',
                                    color: 'white',
                                    fontFamily: 'Outfit, sans-serif',
                                    fontSize: '14px'
                                }}
                            />
                        </div>

                        <button
                            onClick={handleSignOut}
                            style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '12px',
                                padding: '12px 24px',
                                background: 'rgba(239, 68, 68, 0.15)',
                                border: '1px solid #ef4444',
                                borderRadius: '12px',
                                color: '#ef4444',
                                fontSize: '14px',
                                fontWeight: 600,
                                cursor: 'pointer',
                                fontFamily: 'Outfit, sans-serif',
                                transition: 'all 0.2s'
                            }}
                            onMouseOver={(e) => {
                                e.currentTarget.style.background = 'rgba(239, 68, 68, 0.25)'
                            }}
                            onMouseOut={(e) => {
                                e.currentTarget.style.background = 'rgba(239, 68, 68, 0.15)'
                            }}
                        >
                            <LogOut size={18} />
                            Wyloguj się
                        </button>
                    </div>
                )}
            </div>
        </div>
    )
}

function MiniStatCard({ icon, value, label, color }: {
    icon: React.ReactNode
    value: string
    label: string
    color: 'purple' | 'orange' | 'cyan' | 'gold'
}) {
    const colorMap = {
        purple: { bg: 'rgba(176, 0, 255, 0.15)', border: '#b000ff', text: '#b000ff' },
        orange: { bg: 'rgba(255, 136, 0, 0.15)', border: '#ff8800', text: '#ff8800' },
        cyan: { bg: 'rgba(0, 212, 255, 0.15)', border: '#00d4ff', text: '#00d4ff' },
        gold: { bg: 'rgba(255, 215, 0, 0.15)', border: '#ffd700', text: '#ffd700' }
    }

    return (
        <div style={{
            background: 'rgba(20, 20, 35, 0.4)',
            backdropFilter: 'blur(20px)',
            border: `1px solid ${colorMap[color].border}`,
            borderRadius: '16px',
            padding: '20px',
            textAlign: 'center'
        }}>
            <div style={{ fontSize: '28px', fontWeight: 700, marginBottom: '4px', color: colorMap[color].text }}>
                {value}
            </div>
            <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.6)' }}>{label}</div>
        </div>
    )
}

function BadgeItem({ icon, label, color }: { icon: React.ReactNode; label: string; color: string }) {
    return (
        <div style={{ textAlign: 'center' }}>
            <div style={{
                width: '64px',
                height: '64px',
                borderRadius: '12px',
                background: `${color}20`,
                border: `1px solid ${color}`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 8px',
                color: color
            }}>
                {icon}
            </div>
            <div style={{ fontSize: '11px', color: 'rgba(255, 255, 255, 0.6)' }}>{label}</div>
        </div>
    )
}

function GoalItem({ title, progress, current, target, unit }: {
    title: string
    progress: number
    current: number
    target: number
    unit?: string
}) {
    return (
        <div style={{ marginBottom: '20px' }}>
            <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                marginBottom: '8px',
                fontSize: '13px'
            }}>
                <span style={{ color: 'rgba(255, 255, 255, 0.8)' }}>{title}</span>
                <span style={{ color: '#00ff88', fontWeight: 600 }}>
                    {current}/{target}{unit && ` ${unit}`}
                </span>
            </div>
            <div style={{
                height: '8px',
                background: 'rgba(255, 255, 255, 0.1)',
                borderRadius: '4px',
                overflow: 'hidden'
            }}>
                <div style={{
                    height: '100%',
                    width: `${progress}%`,
                    background: 'linear-gradient(90deg, #ffd700, #00ff88)',
                    borderRadius: '4px',
                    transition: 'width 0.4s ease'
                }} />
            </div>
        </div>
    )
}
