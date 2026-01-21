'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { Zap, Trophy, Target, Flame, BookOpen, Brain, ChevronRight, GraduationCap, Bell } from 'lucide-react'

export default function HomePage() {
  const { user, profile, loading } = useAuth()
  const router = useRouter()
  const [completedLessons, setCompletedLessons] = useState<number>(0)
  const [leaderboard, setLeaderboard] = useState<any[]>([])
  const [leaderboardLoading, setLeaderboardLoading] = useState(true)

  useEffect(() => {
    if (!loading && !user) {
      router.push('/auth/login')
    }
  }, [user, loading, router])

  useEffect(() => {
    async function fetchStats() {
      if (!user) return

      const { count } = await supabase
        .from('user_progress')
        .select('*', { count: 'exact', head: true })
        .eq('user_id', user.id)
        .not('completed_at', 'is', null)

      setCompletedLessons(count || 0)
    }

    fetchStats()
  }, [user])

  useEffect(() => {
    async function fetchLeaderboard() {
      if (!user) return

      try {
        setLeaderboardLoading(true)
        const response = await fetch('/api/leaderboard?limit=10')

        if (!response.ok) {
          console.error('Leaderboard fetch failed:', response.statusText)
          return
        }

        const data = await response.json()
        setLeaderboard(data)
      } catch (error) {
        console.error('Leaderboard error:', error)
      } finally {
        setLeaderboardLoading(false)
      }
    }

    fetchLeaderboard()
  }, [user])

  if (loading) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'rgba(255, 255, 255, 0.6)'
      }}>
        Ładowanie profilu...
      </div>
    )
  }

  if (!user) return null

  const levelName = (level: number) => {
    const names = ['Recruit', 'Analyst', 'Associate', 'Manager', 'Director', 'VP', 'SVP', 'Executive', 'Strategist', 'Master']
    return names[Math.min(level - 1, names.length - 1)] || 'Recruit'
  }

  // Main content area matching mockup structure
  return (
    <div style={{ minHeight: '100vh' }}>
      {/* Top Bar */}
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
        zIndex: 50
      }}>
        {/* Actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          {/* Notifications */}
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

      {/* Content with padding matching mockup */}
      <div style={{ padding: '48px 32px 32px 48px' }}>
        {/* Page Header */}
        <div style={{ marginBottom: '32px' }}>
          <h1 style={{
            fontSize: '28px',
            fontWeight: 700,
            marginBottom: ' 8px'
          }}>
            Witaj z powrotem, {profile?.full_name?.split(' ')[0] || 'Piotr'}! 👋
          </h1>
          <p style={{
            fontSize: '15px',
            color: 'rgba(255, 255, 255, 0.6)'
          }}>
            Kontynuuj swoją podróż. Dziś masz 3 aktywne misje do ukończenia.
          </p>
        </div>

        {/* Stats Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '16px',
          marginBottom: '32px'
        }}>
          <StatCard
            icon={<Trophy size={24} />}
            iconColor="purple"
            value="#8"
            label="Ranking"
          />
          <StatCard
            icon={<Target size={24} />}
            iconColor="blue"
            value="12"
            label="Odznaki"
          />
          <StatCard
            icon={<Target size={24} />}
            iconColor="gold"
            value={`${completedLessons}/15`}
            label="Ukończone lekcje"
          />
          <StatCard
            icon={<Flame size={24} />}
            iconColor="green"
            value="7 dni"
            label="Streak"
          />
        </div>

        {/* Content Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '2fr 1fr',
          gap: '24px',
          marginBottom: '32px'
        }}>
          {/* Missions */}
          <GlassCard>
            <CardHeader title="🎯 Aktywne Misje" action="Zobacz wszystkie" />
            <MissionItem
              icon={<GraduationCap size={18} />}
              title="Milwaukee Canvas - Krok 4/7"
              meta="🔥 3 karty do końca | ~12 min | +50 XP"
              progress={57}
            />
            <MissionItem
              icon={<Brain size={18} />}
              title="Neural Engram: Leadership Basics"
              meta="⏳ Pobrano | Aktywacja: 24h"
              progress={0}
            />
            <MissionItem
              icon={<Trophy size={18} />}
              title="Tygodniowe Wyzwanie: 5 lekcji"
              meta="🎯 Pozostało 3 dni | 3/5 ukończone"
              progress={60}
            />
          </GlassCard>

          {/* Leaderboard */}
          <GlassCard>
            <CardHeader title="🏆 Leaderboard" action="Top 100" />
            {leaderboardLoading ? (
              <div style={{
                padding: '20px',
                textAlign: 'center',
                color: 'rgba(255, 255, 255, 0.6)'
              }}>
                Ładowanie rankingu...
              </div>
            ) : leaderboard.length === 0 ? (
              <div style={{
                padding: '20px',
                textAlign: 'center',
                color: 'rgba(255, 255, 255, 0.6)'
              }}>
                Brak danych rankingu
              </div>
            ) : (
              <>
                {leaderboard.map((entry) => (
                  <LeaderboardItem
                    key={entry.user_id}
                    rank={entry.rank}
                    initials={entry.display_name?.substring(0, 2).toUpperCase() || 'U'}
                    name={entry.user_id === user?.id ? `${entry.display_name || 'Ty'} (Ty)` : (entry.display_name || 'User')}
                    level={entry.level}
                    title={levelName(entry.level)}
                    xp={entry.total_xp}
                    top={entry.rank <= 3}
                  />
                ))}
              </>
            )}
          </GlassCard>
        </div>

        {/* Radar Chart */}
        <GlassCard>
          <CardHeader title="📊 Mapa Kompetencji" action="Szczegóły" />
          <div style={{
            height: '300px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'rgba(255, 255, 255, 0.4)',
            fontSize: '14px'
          }}>
            <p>📊 Radar chart kompetencji (wymaga Chart.js - dodamy w następnym kroku)</p>
          </div>
        </GlassCard>
      </div>
    </div>
  )
}

function GlassCard({ children }: { children: React.ReactNode }) {
  return (
    <div style={{
      background: 'rgba(20, 20, 35, 0.4)',
      backdropFilter: 'blur(20px)',
      WebkitBackdropFilter: 'blur(20px)',
      border: '1px solid rgba(255, 255, 255, 0.08)',
      borderRadius: '20px',
      padding: '24px',
      boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)'
    }}>
      {children}
    </div>
  )
}

function CardHeader({ title, action }: { title: string; action: string }) {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginBottom: '20px'
    }}>
      <h3 style={{ fontSize: '16px', fontWeight: 600 }}>{title}</h3>
      <span style={{
        fontSize: '13px',
        color: '#00d4ff',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        gap: '4px'
      }}>
        {action}
        <ChevronRight size={16} />
      </span>
    </div>
  )
}

function StatCard({ icon, iconColor, value, label }: {
  icon: React.ReactNode
  iconColor: 'purple' | 'blue' | 'gold' | 'green'
  value: string
  label: string
}) {
  const iconBgMap = {
    purple: 'rgba(176, 0, 255, 0.2)',
    blue: 'rgba(0, 212, 255, 0.2)',
    gold: 'rgba(255, 215, 0, 0.2)',
    green: 'rgba(0, 255, 136, 0.2)'
  }

  const iconColorMap = {
    purple: '#b000ff',
    blue: '#00d4ff',
    gold: '#ffd700',
    green: '#00ff88'
  }

  return (
    <div
      style={{
        background: 'rgba(20, 20, 35, 0.4)',
        backdropFilter: 'blur(20px)',
        WebkitBackdropFilter: 'blur(20px)',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        borderRadius: '16px',
        padding: '5px 16px 5px 16px',
        display: 'flex',
        alignItems: 'center',
        gap: '16px',
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        position: 'relative',
        overflow: 'hidden'
      }}
      onMouseOver={(e) => {
        e.currentTarget.style.background = 'rgba(255, 255, 255, 0.08)'
        e.currentTarget.style.transform = 'translateY(-2px)'
        e.currentTarget.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.4)'
        const shine = e.currentTarget.querySelector('.shine-stat') as HTMLElement
        if (shine) shine.style.left = '100%'
      }}
      onMouseOut={(e) => {
        e.currentTarget.style.background = 'rgba(20, 20, 35, 0.4)'
        e.currentTarget.style.transform = 'translateY(0)'
        e.currentTarget.style.boxShadow = 'none'
        const shine = e.currentTarget.querySelector('.shine-stat') as HTMLElement
        if (shine) shine.style.left = '-100%'
      }}
    >
      <div
        className="shine-stat"
        style={{
          position: 'absolute',
          top: 0,
          left: '-100%',
          width: '100%',
          height: '100%',
          background: 'linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent)',
          transition: 'left 0.6s ease',
          pointerEvents: 'none',
          zIndex: 1
        }}
      />
      <div style={{
        width: '48px',
        height: '48px',
        borderRadius: '12px',
        background: iconBgMap[iconColor],
        color: iconColorMap[iconColor],
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexShrink: 0
      }}>
        {icon}
      </div>
      <div>
        <h3 style={{
          fontSize: '24px',
          fontWeight: 700,
          marginBottom: '4px'
        }}>{value}</h3>
        <p style={{
          fontSize: '13px',
          color: 'rgba(255, 255, 255, 0.6)'
        }}>{label}</p>
      </div>
    </div>
  )
}

function MissionItem({ icon, title, meta, progress }: {
  icon: React.ReactNode
  title: string
  meta: string
  progress: number
}) {
  return (
    <div
      style={{
        padding: '16px',
        background: 'rgba(255, 255, 255, 0.03)',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        borderRadius: '12px',
        marginBottom: '12px',
        cursor: 'pointer',
        transition: 'all 0.2s',
        position: 'relative',
        overflow: 'hidden'
      }}
      onMouseOver={(e) => {
        e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)'
        e.currentTarget.style.borderColor = '#00d4ff'
        const shine = e.currentTarget.querySelector('.shine-mission') as HTMLElement
        if (shine) shine.style.left = '100%'
      }}
      onMouseOut={(e) => {
        e.currentTarget.style.background = 'rgba(255, 255, 255, 0.03)'
        e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.08)'
        const shine = e.currentTarget.querySelector('.shine-mission') as HTMLElement
        if (shine) shine.style.left = '-100%'
      }}
    >
      <div
        className="shine-mission"
        style={{
          position: 'absolute',
          top: 0,
          left: '-100%',
          width: '100%',
          height: '100%',
          background: 'linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.4), transparent)',
          transition: 'left 0.6s ease',
          pointerEvents: 'none',
          zIndex: 1
        }}
      />
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        marginBottom: '12px'
      }}>
        <div style={{
          width: '36px',
          height: '36px',
          borderRadius: '8px',
          background: 'rgba(0, 212, 255, 0.2)',
          color: '#00d4ff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          {icon}
        </div>
        <div style={{ flex: 1 }}>
          <h4 style={{
            fontSize: '14px',
            fontWeight: 600,
            marginBottom: '4px'
          }}>{title}</h4>
          <p style={{
            fontSize: '12px',
            color: 'rgba(255, 255, 255, 0.6)'
          }}>{meta}</p>
        </div>
      </div>
      <div style={{
        height: '6px',
        background: 'rgba(255, 255, 255, 0.1)',
        borderRadius: '3px',
        overflow: 'hidden'
      }}>
        <div style={{
          height: '100%',
          width: `${progress}%`,
          background: 'linear-gradient(90deg, #00d4ff, #b000ff)',
          borderRadius: '3px',
          transition: 'width 0.4s ease'
        }} />
      </div>
    </div>
  )
}

function LeaderboardItem({ rank, initials, name, level, title, xp, top }: {
  rank: number
  initials: string
  name: string
  level: number
  title: string
  xp: number
  top?: boolean
}) {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        padding: '12px',
        background: 'rgba(255, 255, 255, 0.03)',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        borderRadius: '12px',
        marginBottom: '8px',
        cursor: 'pointer',
        transition: 'all 0.2s'
      }}
      onMouseOver={(e) => {
        e.currentTarget.style.background = 'rgba(255, 255, 255, 0.06)'
      }}
      onMouseOut={(e) => {
        e.currentTarget.style.background = 'rgba(255, 255, 255, 0.03)'
      }}
    >
      <div style={{
        width: '32px',
        height: '32px',
        borderRadius: '8px',
        background: top ? 'linear-gradient(135deg, #ffd700, #ff8800)' : 'rgba(255, 215, 0, 0.2)',
        color: top ? '#000' : '#ffd700',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontWeight: 700,
        fontSize: '14px',
        flexShrink: 0
      }}>
        {rank}
      </div>
      <div style={{
        width: '36px',
        height: '36px',
        borderRadius: '50%',
        background: 'linear-gradient(135deg, #b000ff, #00d4ff)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontWeight: 700,
        fontSize: '14px'
      }}>
        {initials}
      </div>
      <div style={{ flex: 1 }}>
        <h4 style={{
          fontSize: '13px',
          fontWeight: 600,
          marginBottom: '2px'
        }}>{name}</h4>
        <p style={{
          fontSize: '11px',
          color: 'rgba(255, 255, 255, 0.6)'
        }}>Level {level} • {title}</p>
      </div>
      <div style={{
        fontSize: '14px',
        fontWeight: 700,
        color: '#ffd700'
      }}>
        {xp.toLocaleString()}
      </div>
    </div>
  )
}
