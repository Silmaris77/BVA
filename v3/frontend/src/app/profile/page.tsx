'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useRouter, useSearchParams } from 'next/navigation'
import { useState, useEffect, Suspense } from 'react'
import { User, Bell, Zap, Trophy, Flame, Target, LogOut, TrendingUp, Award, Rocket, BookOpen, Sparkles, Star, Settings, Check, Layout } from 'lucide-react'
import { getUserStatsSummary } from '@/lib/rpg-stats'
import { useTheme } from '@/contexts/ThemeContext'
import ActivityHeatmap from '@/components/profile/ActivityHeatmap'
import AchievementsGrid from '@/components/profile/AchievementsGrid'
import CompetencyRadar from '@/components/profile/CompetencyRadar'
import EditProfileModal, { ARCHETYPES } from '@/components/profile/EditProfileModal'
import ThemeSelector from '@/components/profile/ThemeSelector'

function ProfileContent() {
    const { user, profile, signOut } = useAuth()
    const router = useRouter()
    const searchParams = useSearchParams()
    const activeTab = (searchParams.get('tab') as 'informacje' | 'postepy' | 'cele' | 'ustawienia') || 'informacje'
    const [isEditing, setIsEditing] = useState(false)
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




            {/* Content */}
            <div className="page-content-wrapper">
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
                                flexShrink: 0,
                                position: 'relative'
                            }}>
                                {(() => {
                                    const archetype = ARCHETYPES.find(a => a.id === profile?.avatar_url)
                                    if (archetype) {
                                        const Icon = archetype.icon
                                        return <Icon size={64} color="white" />
                                    }
                                    return profile?.full_name?.substring(0, 2).toUpperCase() || 'PK'
                                })()}
                            </div>

                            {/* Info */}
                            <div style={{ flex: 1 }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '4px' }}>
                                    <h1 style={{ fontSize: '32px', fontWeight: 700, margin: 0 }}>
                                        {profile?.display_name || profile?.full_name || 'Piotr Kowalski'}
                                    </h1>
                                    <button
                                        onClick={() => setIsEditing(true)}
                                        style={{
                                            background: 'rgba(255,255,255,0.1)',
                                            border: 'none',
                                            borderRadius: '8px',
                                            padding: '8px',
                                            cursor: 'pointer',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            transition: 'background 0.2s'
                                        }}
                                        title="Edytuj Profil"
                                    >
                                        <Settings size={16} color="rgba(255,255,255,0.7)" />
                                    </button>
                                </div>
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

                        {/* Edit Profile Modal */}
                        <EditProfileModal
                            isOpen={isEditing}
                            onClose={() => setIsEditing(false)}
                            currentName={profile?.display_name || profile?.full_name || ''}
                            currentAvatar={profile?.avatar_url || ''}
                            userId={user.id}
                        />

                        {/* Activity Heatmap */}
                        <ActivityHeatmap />

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
                        <AchievementsGrid />

                        {/* Moje Kompetencje (Preview) */}
                        <CompetencyRadar stats={userStats} />

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
                                {/* Dynamic Radar Chart */}
                                <CompetencyRadar stats={userStats} />

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

                        <div style={{ marginBottom: '32px' }}>
                            <label style={{ display: 'block', fontSize: '13px', color: 'rgba(255, 255, 255, 0.6)', marginBottom: '12px' }}>
                                Wygląd Aplikacji (Motyw)
                            </label>
                            <ThemeSelector />
                        </div>

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

export default function ProfilePage() {
    return (
        <Suspense fallback={
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'rgba(255, 255, 255, 0.6)'
            }}>
                Ładowanie...
            </div>
        }>
            <ProfileContent />
        </Suspense>
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
