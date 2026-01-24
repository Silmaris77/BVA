import { useEffect, useState } from 'react'
import { Flame, Zap, Brain, Shield, Loader } from 'lucide-react'
import { createClient } from '@/lib/supabase/client'
import { awardXP } from '@/lib/access-control'
import DrillRunnerModal, { DrillData } from './DrillRunnerModal'

export default function TreningView() {
    const supabase = createClient()
    const [drills, setDrills] = useState<DrillData[]>([])
    const [loading, setLoading] = useState(true)
    const [activeDrill, setActiveDrill] = useState<DrillData | null>(null)

    useEffect(() => {
        fetchDrills()
    }, [])

    const fetchDrills = async () => {
        try {
            const { data, error } = await supabase
                .from('drills')
                .select('*')
                .order('created_at', { ascending: false })

            if (error) throw error
            if (data) setDrills(data)
        } catch (e) {
            console.error('Error fetching drills:', e)
        } finally {
            setLoading(false)
        }
    }

    const handleStartDrill = (drill: DrillData) => {
        setActiveDrill(drill)
    }

    const handleCloseDrill = () => {
        setActiveDrill(null)
    }

    const handleCompleteDrill = async (xp: number, score: number) => {
        if (!activeDrill) return

        try {
            const { data: { user } } = await supabase.auth.getUser()
            if (!user) return

            // Record attempt
            await supabase.from('user_drill_attempts').insert({
                user_id: user.id,
                drill_id: activeDrill.drill_id,
                drill_uuid: activeDrill.id,
                score_percentage: score,
                xp_earned: xp
            })

            // Award XP
            if (xp > 0) {
                await awardXP({
                    userId: user.id,
                    sourceType: 'drill',
                    sourceId: activeDrill.drill_id,
                    xpAmount: xp,
                    description: `Drill: ${activeDrill.title} (${score}%)`
                })
            }

            console.log(`Earned ${xp} XP!`)
            // Ideally refresh global stats here (e.g. via context or triggering a re-fetch)
            handleCloseDrill()
        } catch (e) {
            console.error('Error recording drill result:', e)
            handleCloseDrill()
        }
    }

    // Colors mapping
    const getDrillColor = (type: string) => {
        switch (type) {
            case 'speed_run': return { color: '#ff4444', icon: <Shield size={24} color="#b000ff" /> }
            case 'analysis': return { color: '#00d4ff', icon: <Brain size={24} color="#00d4ff" /> }
            case 'daily': return { color: '#ffd700', icon: <Zap size={24} color="#ffd700" /> }
            default: return { color: '#ffffff', icon: <Flame size={24} color="#ffffff" /> }
        }
    }

    if (loading) {
        return (
            <div style={{ padding: '48px', textAlign: 'center', color: 'rgba(255,255,255,0.4)', display: 'flex', justifyContent: 'center', gap: '10px' }}>
                <Loader className="animate-spin" /> Ładowanie drillów...
            </div>
        )
    }

    return (
        <div style={{ padding: '32px 48px', maxWidth: '1200px' }}>
            <div style={{ marginBottom: '32px' }}>
                <h1 style={{ fontSize: '32px', fontWeight: 700, marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <Flame size={32} color="#ff4444" />
                    Centrum Treningowe (Drills)
                </h1>
                <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px' }}>
                    Szybkie, intensywne ćwiczenia budujące nawyki i automatyzmy.
                </p>
            </div>

            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                gap: '24px'
            }}>
                {drills.map((drill) => {
                    const { color, icon } = getDrillColor(drill.drill_type)
                    return (
                        <div
                            key={drill.id}
                            onClick={() => handleStartDrill(drill)}
                            style={{
                                background: 'rgba(20, 20, 35, 0.6)',
                                border: '1px solid rgba(255, 255, 255, 0.08)',
                                borderRadius: '20px',
                                padding: '24px',
                                cursor: 'pointer',
                                transition: 'transform 0.2s',
                                position: 'relative',
                                overflow: 'hidden'
                            }}
                            onMouseEnter={(e) => { e.currentTarget.style.transform = 'translateY(-4px)'; e.currentTarget.style.borderColor = 'rgba(255,255,255,0.2)'; }}
                            onMouseLeave={(e) => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)'; }}
                        >
                            <div style={{ position: 'absolute', top: '20px', right: '20px', fontSize: '11px', fontWeight: 700, padding: '4px 10px', borderRadius: '12px', background: `${color}33`, color: color, textTransform: 'uppercase' }}>
                                {drill.drill_type.replace('_', ' ')}
                            </div>
                            <div style={{
                                width: '48px', height: '48px', borderRadius: '12px',
                                background: 'rgba(255, 255, 255, 0.05)',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                fontSize: '24px', marginBottom: '16px'
                            }}>
                                {icon}
                            </div>
                            <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '8px' }}>{drill.title}</h3>
                            <p style={{ fontSize: '13px', color: 'rgba(255,255,255,0.6)', lineHeight: 1.5, marginBottom: '20px' }}>
                                {drill.description}
                            </p>
                            <div style={{ display: 'flex', gap: '16px', fontSize: '12px', color: 'rgba(255,255,255,0.6)', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '16px' }}>
                                <span>⏱️ {Math.floor(drill.time_limit_seconds / 60) > 0 ? `${Math.floor(drill.time_limit_seconds / 60)} min` : `${drill.time_limit_seconds}s`}</span>
                                <span>⭐ +{drill.max_xp} XP</span>
                            </div>
                        </div>
                    )
                })}
            </div>

            {activeDrill && (
                <DrillRunnerModal
                    drill={activeDrill}
                    onClose={handleCloseDrill}
                    onComplete={handleCompleteDrill}
                />
            )}
        </div>
    )
}
