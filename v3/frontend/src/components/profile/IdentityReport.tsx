'use client'

import { Brain, Star, Target, Compass, Sparkles, BookOpen, User, Lock } from 'lucide-react'
import { useState } from 'react'

// Mock Data (jako fallback)
const MOCK_IDENTITY_DATA = {
    synthesis: {
        archetype: "Strategiczny Wizjoner",
        description: "Twoje wyniki wskazują na unikalne połączenie analitycznego myślenia z intuicją strategiczną.",
    },
    strengths: [
        { title: "Strategiczne planowanie", desc: "Potrafisz przewidywać konsekwencje długofalowe." },
        { title: "Szybka adaptacja", desc: "Błyskawicznie uczysz się nowych systemów." }
    ],
    tests: {
        kolb: { name: "Styl Kolba", result: "Refleksyjny Obserwator", color: "#667eea" },
        neuroleader: { name: "Neuroleader", result: "Visionary", color: "#b000ff" },
        mi: { name: "Inteligencje", result: "Logiczno-Matematyczna", color: "#00d4ff" }
    },
    recommendations: [
        { title: "Rozwiń Delegowanie", desc: "Twoja potrzeba kontroli może hamować zespół.", priority: "high" }
    ]
}

interface IdentityReportData {
    synthesis: {
        archetype: string
        description: string
    }
    strengths: Array<{ title: string; desc: string }>
    blind_spots: Array<{ title: string; desc: string }>
    energy_profile: { type: string; tips: string }
    communication_style: string
    tests: Record<string, { name: string; result: string; color: string }>
    recommendations: Array<{ title: string; desc: string; priority: string }>
    motivational_message?: string
}

export default function IdentityReport() {
    const [isUnlocked, setIsUnlocked] = useState(true)
    const [loading, setLoading] = useState(false)
    const [reportData, setReportData] = useState<IdentityReportData | null>(null)
    const [error, setError] = useState<string | null>(null)

    // Symulacja pobierania / generowania raportu
    const generateReport = async () => {
        setLoading(true)
        setError(null)
        try {
            const res = await fetch('/api/ai/reports/identity', { method: 'POST' })

            // Try to parse JSON, but handle if it fails (e.g. 500 html page)
            let data;
            const text = await res.text();
            try {
                data = JSON.parse(text);
            } catch (e) {
                console.error('Failed to parse response JSON:', text);
                throw new Error(`Server returned non-JSON response: ${text.substring(0, 100)}...`);
            }

            if (res.ok) {
                setReportData(data)
            } else {
                console.error('API Error:', data);
                setError(data.details || data.error || 'Wystąpił nieznany błąd podczas generowania raportu.');
            }
        } catch (e: any) {
            console.error('Fetch Error:', e)
            setError(e.message || 'Błąd połączenia z serwerem.')
        } finally {
            setLoading(false)
        }
    }

    if (!isUnlocked) {
        return (
            <div style={{
                background: 'rgba(20, 20, 35, 0.4)',
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.08)',
                borderRadius: '24px',
                padding: '64px',
                textAlign: 'center',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '24px'
            }}>
                <div style={{
                    padding: '24px',
                    background: 'rgba(176, 0, 255, 0.1)',
                    borderRadius: '50%',
                    border: '1px solid rgba(176, 0, 255, 0.3)',
                    color: '#b000ff'
                }}>
                    <Lock size={48} />
                </div>
                <div>
                    <h2 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '8px' }}>
                        Raport Tożsamości Zablokowany
                    </h2>
                    <p style={{ fontSize: '16px', color: 'rgba(255, 255, 255, 0.6)', maxWidth: '500px' }}>
                        Aby AI mogło wygenerować Twój Profil Potencjału, musisz ukończyć minimum 3 testy diagnostyczne w sekcji Narzędzia.
                    </p>
                </div>
                <button
                    style={{
                        padding: '12px 32px',
                        background: 'linear-gradient(135deg, #b000ff, #00d4ff)',
                        border: 'none',
                        borderRadius: '12px',
                        color: 'white',
                        fontWeight: 600,
                        cursor: 'pointer',
                        fontSize: '16px'
                    }}
                >
                    Przejdź do Testów
                </button>
            </div>
        )
    }

    if (!reportData && !loading) {
        return (
            <div style={{
                background: 'rgba(20, 20, 35, 0.4)',
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.08)',
                borderRadius: '24px',
                padding: '48px 32px',
                textAlign: 'center',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '24px',
                marginBottom: '100px' // Extra space for BottomNav on mobile
            }}>
                <div style={{
                    padding: '24px',
                    background: 'rgba(0, 212, 255, 0.1)',
                    borderRadius: '50%',
                    border: '1px solid rgba(0, 212, 255, 0.3)',
                    color: '#00d4ff'
                }}>
                    <Brain size={48} />
                </div>
                <div>
                    <h2 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '8px' }}>
                        Twój Raport jest Gotowy
                    </h2>
                    <p style={{ fontSize: '16px', color: 'rgba(255, 255, 255, 0.6)', maxWidth: '500px' }}>
                        Daj mi chwilę...
                    </p>
                </div>
                {error && (
                    <div style={{
                        marginTop: '16px',
                        padding: '12px',
                        background: 'rgba(255, 68, 68, 0.1)',
                        border: '1px solid #ff4444',
                        borderRadius: '8px',
                        color: '#ff4444',
                        maxWidth: '400px',
                        textAlign: 'left',
                        fontSize: '13px',
                        fontFamily: 'monospace'
                    }}>
                        <strong>Błąd:</strong> {error}
                    </div>
                )}
                <button
                    onClick={generateReport}
                    style={{
                        padding: '16px 48px',
                        background: 'linear-gradient(135deg, #b000ff, #00d4ff)',
                        border: 'none',
                        borderRadius: '16px',
                        color: 'white',
                        fontWeight: 700,
                        cursor: 'pointer',
                        fontSize: '18px',
                        boxShadow: '0 0 30px rgba(0, 212, 255, 0.3)',
                        transition: 'transform 0.2s, box-shadow 0.2s',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        WebkitTapHighlightColor: 'transparent',
                        touchAction: 'manipulation',
                        userSelect: 'none',
                        position: 'relative',
                        zIndex: 10
                    }}
                    onTouchStart={(e) => {
                        const target = e.currentTarget as HTMLButtonElement;
                        target.style.transform = 'scale(0.95)';
                    }}
                    onTouchEnd={(e) => {
                        const target = e.currentTarget as HTMLButtonElement;
                        target.style.transform = 'scale(1)';
                    }}
                >
                    <Sparkles size={20} />
                    Generuj Analizę AI
                </button>
            </div>
        )
    }

    if (loading) {
        return (
            <div style={{
                minHeight: '400px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '24px'
            }}>
                <div className="animate-spin" style={{
                    width: '64px',
                    height: '64px',
                    border: '4px solid rgba(255,255,255,0.1)',
                    borderTop: '4px solid #00d4ff',
                    borderRadius: '50%'
                }} />
                <div style={{ textAlign: 'center' }}>
                    <h3 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '8px' }}>
                        AI łączy fakty...
                    </h3>
                    <p style={{ color: 'rgba(255,255,255,0.6)' }}>
                        Konfrontuję Twoje wyniki testów z rzeczywistą aktywnością.
                    </p>
                </div>
            </div>
        )
    }

    if (!reportData) return null
    const data = reportData

    return (
        <div style={{ animation: 'fadeIn 0.5s ease-out' }}>
            <style>{`
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
            `}</style>

            {/* Header Section */}
            <div style={{
                background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
                borderRadius: '24px',
                padding: '48px',
                marginBottom: '32px',
                border: '1px solid rgba(255, 255, 255, 0.08)',
                position: 'relative',
                overflow: 'hidden'
            }}>
                <div style={{ position: 'relative', zIndex: 2, display: 'flex', gap: '48px', alignItems: 'center' }}>
                    <div style={{ flex: 1 }}>
                        <div style={{
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '8px',
                            background: 'rgba(176, 0, 255, 0.15)',
                            color: '#e0aaff',
                            padding: '6px 16px',
                            borderRadius: '20px',
                            fontSize: '13px',
                            fontWeight: 600,
                            marginBottom: '16px',
                            border: '1px solid rgba(176, 0, 255, 0.3)'
                        }}>
                            <Sparkles size={14} />
                            RAPORT TOŻSAMOŚCI AI
                        </div>
                        <h1 style={{ fontSize: '42px', fontWeight: 800, marginBottom: '16px', lineHeight: 1.1 }}>
                            {data.synthesis.archetype}
                        </h1>
                        <p style={{ fontSize: '18px', color: 'rgba(255, 255, 255, 0.8)', lineHeight: 1.6 }}>
                            {data.synthesis.description}
                        </p>
                    </div>
                    {/* Visual DNA Circle (Abstract) */}
                    <div style={{
                        width: '200px',
                        height: '200px',
                        borderRadius: '50%',
                        background: 'conic-gradient(from 0deg, #b000ff, #00d4ff, #b000ff)',
                        filter: 'blur(40px)',
                        opacity: 0.3,
                        position: 'absolute',
                        right: '0',
                        top: '50%',
                        transform: 'translateY(-50%)'
                    }} />
                </div>
            </div>

            {/* Main Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '24px' }}>

                {/* 1. Diagnostic Results */}
                <div style={{
                    background: 'rgba(20, 20, 35, 0.4)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255, 255, 255, 0.08)',
                    borderRadius: '20px',
                    padding: '32px'
                }}>
                    <h3 style={{ fontSize: '20px', fontWeight: 700, marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <Compass size={24} color="#00d4ff" />
                        Fundamenty Diagnostyczne
                    </h3>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        {data.tests && Object.values(data.tests).map((test: { name: string; result: string; color: string }) => (
                            <div key={test.name} style={{
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'space-between',
                                padding: '16px',
                                background: 'rgba(255, 255, 255, 0.03)',
                                borderRadius: '12px',
                                borderLeft: `4px solid ${test.color}`
                            }}>
                                <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>{test.name}</span>
                                <span style={{ fontWeight: 600, color: 'white' }}>{test.result}</span>
                            </div>
                        ))}
                    </div>

                    <div style={{ marginTop: '24px', padding: '16px', background: 'rgba(0, 212, 255, 0.05)', borderRadius: '12px', fontSize: '13px', color: '#00d4ff', lineHeight: 1.5 }}>
                        💡 <strong>Insight:</strong> Twoja kombinacja {data.tests.kolb.result} i {data.tests.neuroleader.result} jest rzadka (występuje u 4% liderów). Oznacza to, że potrafisz łączyć teorię z wizjonerską praktyką.
                    </div>
                </div>

                {/* 2. Top 5 Strengths */}
                <div style={{
                    background: 'rgba(20, 20, 35, 0.4)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255, 255, 255, 0.08)',
                    borderRadius: '20px',
                    padding: '32px'
                }}>
                    <h3 style={{ fontSize: '20px', fontWeight: 700, marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <Star size={24} color="#ffd700" />
                        Twoje Supermoce
                    </h3>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                        {data.strengths.map((str: { title: string; desc: string }, i: number) => (
                            <div key={i} style={{
                                display: 'flex',
                                gap: '16px',
                                padding: '12px',
                                borderBottom: i < data.strengths.length - 1 ? '1px solid rgba(255, 255, 255, 0.05)' : 'none'
                            }}>
                                <span style={{ color: '#ffd700', fontWeight: 700, opacity: 0.5 }}>0{i + 1}</span>
                                <div>
                                    <div style={{ fontWeight: 600, marginBottom: '4px', color: 'white' }}>{str.title}</div>
                                    <div style={{ fontSize: '13px', color: 'rgba(255, 255, 255, 0.6)' }}>{str.desc}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* 2.5 New Sections: Blind Spots & Energy */}
                {data.blind_spots && (
                    <div style={{
                        background: 'rgba(30, 10, 20, 0.4)',
                        backdropFilter: 'blur(20px)',
                        border: '1px solid rgba(255, 80, 80, 0.1)',
                        borderRadius: '20px',
                        padding: '32px'
                    }}>
                        <h3 style={{ fontSize: '20px', fontWeight: 700, marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '10px', color: '#ff6b6b' }}>
                            <Lock size={24} />
                            Ślepe Plamki (Shadow Work)
                        </h3>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                            {data.blind_spots.map((spot: { title: string; desc: string }, i: number) => (
                                <div key={i} style={{ padding: '12px', background: 'rgba(255,0,0,0.05)', borderRadius: '8px' }}>
                                    <div style={{ fontWeight: 600, color: '#ffaaaa', marginBottom: '4px' }}>⚠️ {spot.title}</div>
                                    <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>{spot.desc}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {data.energy_profile && (
                    <div style={{
                        background: 'rgba(20, 20, 35, 0.4)',
                        backdropFilter: 'blur(20px)',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        borderRadius: '20px',
                        padding: '32px'
                    }}>
                        <h3 style={{ fontSize: '20px', fontWeight: 700, marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                            <Brain size={24} color="#b000ff" />
                            Twój Profil Energetyczny
                        </h3>
                        <div style={{ padding: '16px', background: 'rgba(176, 0, 255, 0.05)', borderRadius: '12px', marginBottom: '16px' }}>
                            <div style={{ fontWeight: 600, color: '#e0aaff', marginBottom: '4px' }}>📆 Typ: {data.energy_profile.type}</div>
                            <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>{data.energy_profile.tips}</div>
                        </div>
                        {data.communication_style && (
                            <div style={{ marginTop: '20px' }}>
                                <h4 style={{ fontSize: '14px', fontWeight: 600, color: 'rgba(255,255,255,0.5)', textTransform: 'uppercase', marginBottom: '8px' }}>
                                    Styl Komunikacji
                                </h4>
                                <p style={{ fontSize: '14px', lineHeight: 1.6, color: 'rgba(255,255,255,0.8)' }}>
                                    {data.communication_style}
                                </p>
                            </div>
                        )}
                    </div>
                )}

                {/* 3. Action Plan / Recommendations (Full Width) */}
                <div style={{
                    gridColumn: '1 / -1',
                    background: 'linear-gradient(135deg, rgba(30, 20, 50, 0.6) 0%, rgba(20, 20, 35, 0.6) 100%)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(176, 0, 255, 0.2)',
                    borderRadius: '20px',
                    padding: '32px'
                }}>
                    <h3 style={{ fontSize: '20px', fontWeight: 700, marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <Target size={24} color="#b000ff" />
                        Rekomendacje Rozwojowe
                    </h3>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginBottom: '32px' }}>
                        {data.recommendations.map((rec: { title: string; desc: string; priority: string }, i: number) => {
                            const priorityColors = {
                                high: { bg: 'rgba(255, 68, 68, 0.1)', border: '#ff4444', text: '#ff4444' },
                                medium: { bg: 'rgba(255, 136, 0, 0.1)', border: '#ff8800', text: '#ff8800' },
                                low: { bg: 'rgba(0, 212, 255, 0.1)', border: '#00d4ff', text: '#00d4ff' }
                            }
                            const style = priorityColors[rec.priority as keyof typeof priorityColors] || priorityColors.medium

                            return (
                                <div key={i} style={{
                                    background: 'rgba(255, 255, 255, 0.03)',
                                    borderRadius: '16px',
                                    padding: '24px',
                                    border: '1px solid rgba(255, 255, 255, 0.05)',
                                    position: 'relative',
                                    overflow: 'hidden'
                                }}>
                                    <div style={{
                                        position: 'absolute',
                                        top: 0,
                                        left: 0,
                                        height: '100%',
                                        width: '4px',
                                        background: style.border
                                    }} />

                                    <div style={{
                                        display: 'inline-block',
                                        fontSize: '11px',
                                        fontWeight: 700,
                                        textTransform: 'uppercase',
                                        color: style.text,
                                        marginBottom: '12px',
                                        letterSpacing: '0.5px'
                                    }}>
                                        Priorytet: {rec.priority}
                                    </div>

                                    <h4 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '8px', color: 'white' }}>
                                        {rec.title}
                                    </h4>
                                    <p style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.7)', lineHeight: 1.5 }}>
                                        {rec.desc}
                                    </p>
                                </div>
                            )
                        })}
                    </div>

                    {data.motivational_message && (
                        <div style={{
                            textAlign: 'center',
                            padding: '32px',
                            background: 'rgba(255, 255, 255, 0.03)',
                            borderRadius: '16px',
                            border: '1px dashed rgba(255, 255, 255, 0.1)'
                        }}>
                            <div style={{ fontSize: '24px', marginBottom: '16px' }}>❝</div>
                            <p style={{ fontSize: '18px', fontStyle: 'italic', fontWeight: 500, color: '#e0aaff', maxWidth: '600px', margin: '0 auto', lineHeight: 1.6 }}>
                                {data.motivational_message}
                            </p>
                        </div>
                    )}
                </div>

            </div>
        </div>
    )
}
