'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import { User, Bell, Zap, Trophy, Flame, Target, LogOut, TrendingUp, Award, Rocket, BookOpen, Sparkles, Star } from 'lucide-react'
import { getUserStatsSummary } from '@/lib/rpg-stats'

export default function ProfilePage() {
    const { user, profile, signOut } = useAuth()
    const router = useRouter()
    const [activeTab, setActiveTab] = useState<'informacje' | 'postepy' | 'cele' | 'ustawienia'>('informacje')
    const [userStats, setUserStats] = useState<any[]>([])
    const [userClasses, setUserClasses] = useState<any[]>([])
    const [userCombos, setUserCombos] = useState<any[]>([])

    // Load RPG stats
    useEffect(() => {
        async function loadRPGData() {
            if (!user) return
            const data = await getUserStatsSummary(user.id)
            setUserStats(data.stats)
            setUserClasses(data.classes)
            setUserCombos(data.combos)
        }
        loadRPGData()
    }, [user])

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
                justifyContent: 'flex-start',
                position: 'sticky',
                top: '73px', // Below GlobalTopBar
                zIndex: 49
            }}>
                {/* Tabs on Left */}
                <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '4px' }}>
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
                                transition: 'all 0.2s',
                                whiteSpace: 'nowrap'
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
                    <>
                        {/* Character Stats Radar + Bars */}
                        <div style={{
                            background: 'rgba(20, 20, 35, 0.4)',
                            backdropFilter: 'blur(20px)',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            borderRadius: '20px',
                            padding: '32px',
                            marginBottom: '32px'
                        }}>
                            <h3 style={{ fontSize: '20px', fontWeight: 700, marginBottom: '32px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                                📊 Character Stats
                            </h3>

                            <div style={{
                                display: 'grid',
                                gridTemplateColumns: 'repeat(auto-fit, minmax(450px, 1fr))',
                                gap: '48px'
                            }}>
                                {/* Radar Chart (SVG) */}
                                <div>
                                    <div style={{
                                        width: '100%',
                                        height: '400px',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center'
                                    }}>
                                        <svg viewBox="0 0 500 500" style={{ width: '100%', maxWidth: '400px', height: 'auto' }}>
                                            <defs>
                                                <linearGradient id="radarGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                                    <stop offset="0%" style={{ stopColor: '#b000ff', stopOpacity: 0.6 }} />
                                                    <stop offset="100%" style={{ stopColor: '#00d4ff', stopOpacity: 0.6 }} />
                                                </linearGradient>
                                            </defs>

                                            {/* Grid */}
                                            <circle cx="250" cy="250" r="200" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="1" />
                                            <circle cx="250" cy="250" r="150" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="1" />
                                            <circle cx="250" cy="250" r="100" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="1" />
                                            <circle cx="250" cy="250" r="50" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="1" />

                                            {/* Axis */}
                                            <line x1="250" y1="250" x2="250" y2="50" stroke="rgba(255,255,255,0.3)" strokeWidth="1" />
                                            <line x1="250" y1="250" x2="440" y2="155" stroke="rgba(255,255,255,0.3)" strokeWidth="1" />
                                            <line x1="250" y1="250" x2="440" y2="345" stroke="rgba(255,255,255,0.3)" strokeWidth="1" />
                                            <line x1="250" y1="250" x2="250" y2="450" stroke="rgba(255,255,255,0.3)" strokeWidth="1" />
                                            <line x1="250" y1="250" x2="60" y2="345" stroke="rgba(255,255,255,0.3)" strokeWidth="1" />
                                            <line x1="250" y1="250" x2="60" y2="155" stroke="rgba(255,255,255,0.3)" strokeWidth="1" />


                                            {/* Data Area - Dynamic from userStats */}
                                            {(() => {
                                                // Get stat values (0-100)
                                                const leadership = userStats.find(s => s.category === 'Leadership')?.points || 0
                                                const sales = userStats.find(s => s.category === 'Sales')?.points || 0
                                                const strategy = userStats.find(s => s.category === 'Strategy')?.points || 0
                                                const mindset = userStats.find(s => s.category === 'Mindset')?.points || 0
                                                const tech = userStats.find(s => s.category === 'Technical')?.points || 0
                                                const comm = userStats.find(s => s.category === 'Communication')?.points || 0

                                                // Convert to coordinates (center: 250,250, max radius: 200)
                                                const toCoord = (value: number, angle: number) => {
                                                    const radius = (value / 100) * 200
                                                    const x = 250 + radius * Math.sin((angle * Math.PI) / 180)
                                                    const y = 250 - radius * Math.cos((angle * Math.PI) / 180)
                                                    return { x, y }
                                                }

                                                const points = [
                                                    toCoord(leadership, 0),      // Top
                                                    toCoord(sales, 60),          // Top-right
                                                    toCoord(strategy, 120),      // Bottom-right
                                                    toCoord(mindset, 180),       // Bottom
                                                    toCoord(tech, 240),          // Bottom-left
                                                    toCoord(comm, 300)           // Top-left
                                                ]

                                                const pointsString = points.map(p => `${p.x},${p.y}`).join(' ')

                                                return (
                                                    <>
                                                        <polygon points={pointsString}
                                                            fill="url(#radarGradient)"
                                                            fillOpacity="0.5"
                                                            stroke="#b000ff"
                                                            strokeWidth="2" />

                                                        {/* Points */}
                                                        {points.map((p, i) => (
                                                            <circle key={i} cx={p.x} cy={p.y} r="5" fill="#00ff88" />
                                                        ))}
                                                    </>
                                                )
                                            })()}

                                            {/* Labels */}
                                            <text x="250" y="35" textAnchor="middle" fill="white" fontSize="14" fontWeight="600">Leadership</text>
                                            <text x="465" y="165" textAnchor="start" fill="white" fontSize="14" fontWeight="600">Sales</text>
                                            <text x="465" y="330" textAnchor="start" fill="white" fontSize="14" fontWeight="600">Strategy</text>
                                            <text x="250" y="480" textAnchor="middle" fill="white" fontSize="14" fontWeight="600">Mindset</text>
                                            <text x="35" y="330" textAnchor="end" fill="white" fontSize="14" fontWeight="600">Tech</text>
                                            <text x="35" y="165" textAnchor="end" fill="white" fontSize="14" fontWeight="600">Comm</text>
                                        </svg>
                                    </div>
                                </div>

                                {/* Progress Bars */}
                                <div>
                                    <CharacterStatBar
                                        category="Leadership"
                                        points={userStats.find(s => s.category === 'Leadership')?.points || 0}
                                        level={userStats.find(s => s.category === 'Leadership')?.level || 1}
                                        color="#b000ff"
                                    />
                                    <CharacterStatBar
                                        category="Sales"
                                        points={userStats.find(s => s.category === 'Sales')?.points || 0}
                                        level={userStats.find(s => s.category === 'Sales')?.level || 1}
                                        color="#00ff88"
                                    />
                                    <CharacterStatBar
                                        category="Strategy"
                                        points={userStats.find(s => s.category === 'Strategy')?.points || 0}
                                        level={userStats.find(s => s.category === 'Strategy')?.level || 1}
                                        color="#ffd700"
                                    />
                                    <CharacterStatBar
                                        category="Mindset"
                                        points={userStats.find(s => s.category === 'Mindset')?.points || 0}
                                        level={userStats.find(s => s.category === 'Mindset')?.level || 1}
                                        color="#00d4ff"
                                    />
                                    <CharacterStatBar
                                        category="Technical"
                                        points={userStats.find(s => s.category === 'Technical')?.points || 0}
                                        level={userStats.find(s => s.category === 'Technical')?.level || 1}
                                        color="#ff4757"
                                    />
                                    <CharacterStatBar
                                        category="Communication"
                                        points={userStats.find(s => s.category === 'Communication')?.points || 0}
                                        level={userStats.find(s => s.category === 'Communication')?.level || 1}
                                        color="#ff8800"
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Your Classes */}
                        <div style={{
                            background: 'rgba(20, 20, 35, 0.4)',
                            backdropFilter: 'blur(20px)',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            borderRadius: '20px',
                            padding: '32px',
                            marginBottom: '32px'
                        }}>
                            <h3 style={{ fontSize: '20px', fontWeight: 700, marginBottom: '24px' }}>
                                🏆 Your Classes
                            </h3>

                            {userClasses.length > 0 ? (
                                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
                                    {userClasses.map(cls => (
                                        <ClassBadge
                                            key={cls.id}
                                            icon={cls.class_name.includes('Sales') ? '🏆' : cls.class_name.includes('Versatile') ? '🎯' : cls.class_name.includes('Specialist') ? '🚀' : '🧠'}
                                            title={cls.class_name}
                                            bonus={cls.class_name.includes('Sales') ? '+50% XP from Sales' : cls.class_name.includes('Versatile') ? '+25% XP from all sources' : 'Special bonuses active'}
                                            color={cls.class_name.includes('Sales') ? '#b000ff' : cls.class_name.includes('Versatile') ? '#00ff88' : '#ffd700'}
                                        />
                                    ))}
                                </div>
                            ) : (
                                <div style={{
                                    padding: '32px',
                                    textAlign: 'center',
                                    color: 'rgba(255, 255, 255, 0.5)',
                                    background: 'rgba(255, 255, 255, 0.03)',
                                    borderRadius: '12px'
                                }}>
                                    🎯 Nie masz jeszcze żadnej klasy. Zainstaluj więcej engramów!
                                </div>
                            )}

                            <div style={{
                                marginTop: '20px',
                                padding: '16px',
                                background: 'rgba(255, 255, 255, 0.05)',
                                borderRadius: '12px',
                                fontSize: '13px',
                                color: 'rgba(255, 255, 255, 0.6)'
                            }}>
                                💡 Install more engrams to unlock new classes!
                            </div>
                        </div>

                        {/* Active Combos */}
                        <div style={{
                            background: 'rgba(20, 20, 35, 0.4)',
                            backdropFilter: 'blur(20px)',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            borderRadius: '20px',
                            padding: '32px'
                        }}>
                            <h3 style={{ fontSize: '20px', fontWeight: 700, marginBottom: '24px' }}>
                                🔥 Active Synergy Combos
                            </h3>

                            {userCombos.length > 0 ? (
                                userCombos.map(combo => (
                                    <SynergyCombo
                                        key={combo.combo_name}
                                        name={combo.combo_name}
                                        engrams={['Engram 1', 'Engram 2', 'Engram 3']} // TODO: fetch real engram names
                                        bonus="+50% XP bonus active"
                                    />
                                ))
                            ) : (
                                <div style={{
                                    padding: '32px',
                                    textAlign: 'center',
                                    color: 'rgba(255, 255, 255, 0.5)',
                                    background: 'rgba(255, 255, 255, 0.03)',
                                    borderRadius: '12px',
                                    marginBottom: '20px'
                                }}>
                                    🔥 Nie masz jeszcze żadnego combo. Ukończ więcej engramów!
                                </div>
                            )}

                            <div style={{
                                marginTop: '20px',
                                padding: '16px',
                                background: 'rgba(255, 255, 255, 0.05)',
                                borderRadius: '12px',
                                fontSize: '13px',
                                color: 'rgba(255, 255, 255, 0.6)',
                                textAlign: 'center'
                            }}>
                                🎮 Complete specific engram combinations to unlock powerful synergy bonuses!
                            </div>
                        </div>
                    </>
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

// RPG Components
function CharacterStatBar({ category, points, level, color }: {
    category: string
    points: number
    level: number
    color: string
}) {
    const levelNames = ['Novice', 'Apprentice', 'Practitioner', 'Expert', 'Master']
    const levelName = levelNames[Math.min(level - 1, 4)]

    return (
        <div style={{ marginBottom: '24px' }}>
            <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                marginBottom: '8px'
            }}>
                <span style={{ fontSize: '15px', fontWeight: 600 }}>{category}</span>
                <span style={{ fontSize: '13px', color: 'rgba(255, 255, 255, 0.7)' }}>
                    {points}/100
                </span>
            </div>
            <div style={{
                height: '12px',
                background: 'rgba(255, 255, 255, 0.1)',
                borderRadius: '6px',
                overflow: 'hidden',
                marginBottom: '8px'
            }}>
                <div style={{
                    height: '100%',
                    width: `${points}%`,
                    background: `linear-gradient(90deg, ${color}, ${color}dd)`,
                    borderRadius: '6px',
                    transition: 'width 0.6s ease'
                }} />
            </div>
            <span style={{
                display: 'inline-block',
                padding: '4px 12px',
                background: `${color}33`,
                border: `1px solid ${color}`,
                borderRadius: '12px',
                fontSize: '11px',
                fontWeight: 700,
                color: color
            }}>
                {levelName.toUpperCase()} (Level {level})
            </span>
        </div>
    )
}

function ClassBadge({ icon, title, bonus, color }: {
    icon: string
    title: string
    bonus: string
    color: string
}) {
    return (
        <div style={{
            background: `linear-gradient(135deg, ${color}20, ${color}10)`,
            border: `2px solid ${color}`,
            borderRadius: '16px',
            padding: '20px',
            display: 'flex',
            alignItems: 'center',
            gap: '12px'
        }}>
            <span style={{ fontSize: '32px' }}>{icon}</span>
            <div>
                <div style={{ fontSize: '18px', fontWeight: 700, color: color, marginBottom: '4px' }}>
                    {title}
                </div>
                <div style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.8)' }}>
                    {bonus}
                </div>
            </div>
        </div>
    )
}

function SynergyCombo({ name, engrams, bonus }: {
    name: string
    engrams: string[]
    bonus: string
}) {
    return (
        <div style={{
            background: 'linear-gradient(135deg, rgba(255, 140, 0, 0.2), rgba(255, 215, 0, 0.2))',
            border: '2px solid #ff8800',
            borderRadius: '20px',
            padding: '24px'
        }}>
            <div style={{ textAlign: 'center', marginBottom: '16px' }}>
                <div style={{ fontSize: '32px', marginBottom: '8px' }}>🔥</div>
                <div style={{ fontSize: '20px', fontWeight: 700, color: '#ff8800', marginBottom: '8px' }}>
                    {name}
                </div>
            </div>

            <div style={{ marginBottom: '16px' }}>
                <div style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.8)', marginBottom: '8px' }}>
                    You've mastered:
                </div>
                {engrams.map(engram => (
                    <div key={engram} style={{
                        fontSize: '15px',
                        padding: '4px 0',
                        color: 'white'
                    }}>
                        ✓ {engram}
                    </div>
                ))}
            </div>

            <div style={{
                background: 'rgba(0, 0, 0, 0.3)',
                padding: '12px',
                borderRadius: '12px',
                textAlign: 'center',
                fontWeight: 600,
                color: '#ffd700'
            }}>
                🎁 Bonus: {bonus}
            </div>
        </div>
    )
}
