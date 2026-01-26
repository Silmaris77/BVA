'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { Zap, Trophy, Target, Flame, BookOpen, Brain, ChevronRight, GraduationCap, Bell } from 'lucide-react'
import ResumeLessonCard from '@/components/hub/ResumeLessonCard'
import NewsFeed from '@/components/hub/NewsFeed'
import DailyTip from '@/components/hub/DailyTip'
import { ARCHETYPES } from '@/components/profile/EditProfileModal'

export default function HomePage() {
  const { user, profile, loading } = useAuth()
  const router = useRouter()
  const [completedLessons, setCompletedLessons] = useState<number>(0)
  const [leaderboard, setLeaderboard] = useState<any[]>([])
  const [hubData, setHubData] = useState<any>(null)
  const [loadingHub, setLoadingHub] = useState(true)

  useEffect(() => {
    if (!loading && !user) {
      router.push('/auth/login')
    }
  }, [user, loading, router])

  useEffect(() => {
    async function fetchData() {
      if (!user) return

      // 1. Fetch Stats
      const { count } = await supabase
        .from('user_progress')
        .select('*', { count: 'exact', head: true })
        .eq('user_id', user.id)
        .not('completed_at', 'is', null)

      setCompletedLessons(count || 0)

      // 2. Fetch Leaderboard
      const lbRes = await fetch('/api/leaderboard?limit=5') // Limit 5 for widget
      if (lbRes.ok) setLeaderboard(await lbRes.json())

      // 3. Fetch Hub Data (News, Tips, Resume, Streak)
      try {
        const hubRes = await fetch('/api/hub')
        if (hubRes.ok) setHubData(await hubRes.json())
      } catch (e) {
        console.error('Hub fetch error', e)
      } finally {
        setLoadingHub(false)
      }
    }

    if (user) fetchData()
  }, [user])

  if (loading || loadingHub) {
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

  // Derived Streak
  const streak = hubData?.streak?.current || 0

  return (
    <div style={{ minHeight: '100vh' }}>

      {/* Content with padding matching mockup */}
      <div className="page-content-wrapper">
        {/* Page Header */}
        <div style={{ marginBottom: '32px' }}>
          <h1 style={{
            fontSize: '28px',
            fontWeight: 700,
            marginBottom: ' 8px'
          }}>
            Witaj z powrotem, {profile?.display_name || profile?.full_name?.split(' ')[0] || 'User'}! 👋
          </h1>
          <p style={{
            fontSize: '15px',
            color: 'rgba(255, 255, 255, 0.6)'
          }}>
            Kontynuuj swoją podróż. Dziś masz {hubData?.missions?.filter((m: any) => m.progress < 100).length || 0} aktywne misje do ukończenia.
          </p>
        </div>

        {/* Dynamic Resume Lesson Card */}
        {hubData?.resume_lesson && (
          <ResumeLessonCard lesson={hubData.resume_lesson} />
        )}

        {/* Stats Grid */}
        <div className="stats-grid">
          <style>{`
                .stats-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 16px;
                    margin-bottom: 32px;
                }
                @media (max-width: 768px) {
                    .stats-grid {
                        grid-template-columns: 1fr 1fr; /* Force 2 columns Grid 2x2 */
                    }
                    /* Reduce padding in cards to fit */
                    .stats-grid > div {
                        flex-direction: column;
                        align-items: flex-start;
                        gap: 8px;
                        padding: 12px !important;
                    }
                    /* Adjust Icon Size */
                    .stats-grid .stat-icon {
                        width: 36px;
                        height: 36px;
                    }
                }
            `}</style>
          <StatCard
            icon={<Trophy size={24} />}
            iconColor="purple"
            value={`#${hubData?.leaderboard_rank || '-'}`} // TODO: Get rank from API
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
            value={`${completedLessons}`}
            label="Ukończone lekcje"
          />
          <StatCard
            icon={<Brain size={24} />}
            iconColor="green"
            value={`${hubData?.total_engrams || 0}`}
            label="Opanowane pojęcia"
          />
        </div>

        {/* Content Grid */}
        <div className="dashboard-content-grid">
          <style>{`
                .dashboard-content-grid {
                    display: grid;
                    grid-template-columns: 2fr 1fr;
                    gap: 24px;
                    margin-bottom: 32px;
                }
                @media (max-width: 900px) {
                    .dashboard-content-grid {
                        display: flex;
                        flex-direction: column;
                    }
                }
            `}</style>
          {/* Left Column: News & Missions */}
          <div>
            <NewsFeed news={hubData?.news || []} />

            {/* Missions */}
            <GlassCard>
              <CardHeader title="🎯 Aktywne Misje" action="Zobacz wszystkie" />

              {hubData?.missions?.map((mission: any, index: number) => {
                const getIcon = (name: string) => {
                  switch (name) {
                    case 'GraduationCap': return <GraduationCap size={18} />
                    case 'Trophy': return <Trophy size={18} />
                    case 'Brain': return <Brain size={18} />
                    default: return <Target size={18} />
                  }
                }

                return (
                  <MissionItem
                    key={mission.id || index}
                    icon={getIcon(mission.icon)}
                    title={mission.title}
                    meta={mission.meta}
                    progress={mission.progress}
                  />
                )
              })}

              {!hubData?.missions && (
                <div style={{ textAlign: 'center', padding: '20px', color: 'rgba(255,255,255,0.5)' }}>
                  Ładowanie misji...
                </div>
              )}
            </GlassCard>
          </div>

          {/* Right Column: Tips & Leaderboard */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <DailyTip tip={hubData?.daily_tip} />

            {/* Leaderboard */}
            <GlassCard>
              <CardHeader title="🏆 Leaderboard Top 5" action="Pełny Ranking" />
              {leaderboard.length === 0 ? (
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
        </div>
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
      }} className="stat-icon">
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
