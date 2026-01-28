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
        <div style={{ maxWidth: '1200px' }}>
            <div style={{ marginBottom: '32px' }}>
                <h1 style={{ fontSize: '32px', fontWeight: 700, marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <Flame size={32} color="#ff4444" />
                    Centrum Treningowe (Drills)
                </h1>
                <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px' }}>
                    Szybkie, intensywne ćwiczenia budujące nawyki i automatyzmy.
                </p>
            </div>

            {/* Sekcja: Drille (Istniejące) */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                gap: '24px',
                marginBottom: '48px'
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

            {/* MOCKUP: Zbiory Zadań */}
            <div style={{ marginBottom: '32px' }}>
                <h2 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <Brain size={28} color="#00d4ff" />
                    Zbiory Zadań (Problem Sets)
                </h2>
                <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px' }}>
                    Tematyczne zestawy zadań utrwalających wiedzę.
                </p>
            </div>

            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                gap: '24px'
            }}>
                {[
                    {
                        id: 'mock-1', drill_id: 'math-ps-1', title: 'Liczby - Poziom Podstawowy',
                        description: 'Trening rozpoznawania typów liczb i podstawowych działań na ułamkach.',
                        drill_type: 'problem_set', time_limit_seconds: 600, max_xp: 50,
                        questions: [
                            { id: 'q1', question: 'Która liczba jest całkowita?', options: ['3.5', '-2', '1/2', '0.1'], correctIndex: 1, feedback: '-2 jest liczbą całkowitą.' },
                            { id: 'q2', question: 'Zamień 1/4 na ułamek dziesiętny', options: ['0.2', '0.25', '0.4', '0.5'], correctIndex: 1, feedback: '1/4 = 0.25' },
                            { id: 'q3', question: 'Liczba przeciwna do 5 to:', options: ['1/5', '5', '-5', '0'], correctIndex: 2, feedback: 'Przeciwna do 5 to -5.' }
                        ]
                    },
                    {
                        id: 'mock-2', drill_id: 'math-ps-2', title: 'Zaokrąglanie - Poziom Średni',
                        description: 'Ćwiczenia z zaokrąglania do dziesiątek, setek i części dziesiętnych.',
                        drill_type: 'problem_set', time_limit_seconds: 900, max_xp: 100,
                        questions: [
                            { id: 'q1', question: 'Zaokrąglij 149 do setek', options: ['100', '150', '200', '140'], correctIndex: 0, feedback: '4 < 5, więc w dół do 100.' },
                            { id: 'q2', question: 'Zaokrąglij 3.85 do części dziesiętnych', options: ['3.8', '3.9', '4.0', '3.85'], correctIndex: 1, feedback: '5 podnosi cyfrę 8 do 9.' }
                        ]
                    },
                    {
                        id: 'mock-3', drill_id: 'math-ps-3', title: 'Szacowanie - Poziom Ekspert',
                        description: 'Szybkie szacowanie wyników skomplikowanych działań w pamięci.',
                        drill_type: 'problem_set', time_limit_seconds: 300, max_xp: 150,
                        questions: [
                            { id: 'q1', question: 'Oszacuj 49 * 21', options: ['800', '1000', '1200', '1500'], correctIndex: 1, feedback: '50 * 20 = 1000' }
                        ]
                    }
                ].map((drill: any) => {
                    const color = '#00d4ff' // Niebieski dla Problem Sets
                    const icon = <Brain size={24} color="#00d4ff" />

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
                            <div style={{ position: 'absolute', top: '0', left: '0', width: '100%', height: '4px', background: 'linear-gradient(90deg, #00d4ff 0%, #0055ff 100%)' }}></div>

                            <div style={{ position: 'absolute', top: '20px', right: '20px', fontSize: '11px', fontWeight: 700, padding: '4px 10px', borderRadius: '12px', background: `${color}33`, color: color, textTransform: 'uppercase' }}>
                                PROBLEM SET
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
