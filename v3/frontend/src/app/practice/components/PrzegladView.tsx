import { Zap, Target, Brain, ArrowRight, Folder } from 'lucide-react'

export default function PrzegladView() {
    return (
        <div style={{ maxWidth: '1200px' }}>
            <div style={{ marginBottom: '32px' }}>
                <h1 style={{ fontSize: '32px', fontWeight: 700, marginBottom: '8px' }}>
                    Witaj w Centrum Praktyki
                </h1>
                <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px' }}>
                    Twój osobisty poligon doświadczalny. Trenuj, graj i wdrażaj.
                </p>
            </div>

            <div className="przeglad-grid">
                <style>{`
                    .przeglad-grid {
                        display: grid;
                        grid-template-columns: 2fr 1fr;
                        gap: 24px;
                    }
                    @media (max-width: 900px) {
                        .przeglad-grid {
                            display: flex;
                            flex-direction: column;
                        }
                    }
                `}</style>
                {/* --- LEFT COLUMN --- */}
                <div>
                    {/* Daily Drills Section */}
                    <div style={{
                        background: 'rgba(20, 20, 35, 0.6)',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        borderRadius: '20px',
                        padding: '24px',
                        marginBottom: '24px'
                    }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                            <h2 style={{ fontSize: '18px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '10px' }}>
                                🔥 Polecane na Dziś
                            </h2>
                            <span style={{ fontSize: '13px', color: '#00d4ff', cursor: 'pointer' }}>Wszystkie Drills &gt;</span>
                        </div>

                        {/* MOCK ITEM 1 */}
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            padding: '16px',
                            background: 'rgba(255,255,255,0.03)',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            borderRadius: '12px',
                            marginBottom: '12px',
                            cursor: 'pointer'
                        }}>
                            <div style={{
                                width: '40px', height: '40px', borderRadius: '8px',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                marginRight: '16px', fontSize: '20px', flexShrink: 0,
                                background: 'rgba(255, 68, 68, 0.15)', color: '#ff4444'
                            }}>
                                🛡️
                            </div>
                            <div style={{ flex: 1 }}>
                                <div style={{ fontSize: '15px', fontWeight: 600, marginBottom: '4px' }}>Szybka Reakcja: Obiekcje Cenowe</div>
                                <div style={{ fontSize: '12px', color: 'rgba(255,255,255,0.6)' }}>⏱️ 2 min • ⭐ +50 XP • Wymaga: Level 2</div>
                            </div>
                            <button style={{
                                padding: '6px 16px', borderRadius: '20px',
                                fontSize: '12px', fontWeight: 700,
                                background: '#ff4444', color: 'white', border: 'none', cursor: 'pointer'
                            }}>Start</button>
                        </div>

                        {/* MOCK ITEM 2 */}
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            padding: '16px',
                            background: 'rgba(255,255,255,0.03)',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            borderRadius: '12px',
                            cursor: 'pointer'
                        }}>
                            <div style={{
                                width: '40px', height: '40px', borderRadius: '8px',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                marginRight: '16px', fontSize: '20px', flexShrink: 0,
                                background: 'rgba(0, 212, 255, 0.15)', color: '#00d4ff'
                            }}>
                                🧠
                            </div>
                            <div style={{ flex: 1 }}>
                                <div style={{ fontSize: '15px', fontWeight: 600, marginBottom: '4px' }}>Typologia Klienta: Analiza Audio</div>
                                <div style={{ fontSize: '12px', color: 'rgba(255,255,255,0.6)' }}>⏱️ 3 min • ⭐ +30 XP • Codzienne Wyzwanie</div>
                            </div>
                            <button style={{
                                padding: '6px 16px', borderRadius: '20px',
                                fontSize: '12px', fontWeight: 700,
                                background: 'rgba(255,255,255,0.05)', color: 'rgba(255,255,255,0.6)',
                                border: '1px solid rgba(255,255,255,0.1)', cursor: 'pointer'
                            }}>Start</button>
                        </div>
                        {/* MATH LESSON ITEM */}
                        <div
                            onClick={() => window.location.href = '/lessons/math-g7-l1'}
                            style={{
                                display: 'flex',
                                alignItems: 'center',
                                padding: '16px',
                                background: 'rgba(59, 130, 246, 0.1)',
                                border: '1px solid rgba(59, 130, 246, 0.2)',
                                borderRadius: '12px',
                                marginBottom: '12px',
                                cursor: 'pointer'
                            }}>
                            <div style={{
                                width: '40px', height: '40px', borderRadius: '8px',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                marginRight: '16px', fontSize: '20px', flexShrink: 0,
                                background: 'rgba(59, 130, 246, 0.2)', color: '#60a5fa'
                            }}>
                                📐
                            </div>
                            <div style={{ flex: 1 }}>
                                <div style={{ fontSize: '15px', fontWeight: 600, marginBottom: '4px' }}>Matematyka: Liczby i Działania</div>
                                <div style={{ fontSize: '12px', color: 'rgba(255,255,255,0.6)' }}>⏱️ 15 min • ⭐ +50 XP • Klasa 7</div>
                            </div>
                            <button style={{
                                padding: '6px 16px', borderRadius: '20px',
                                fontSize: '12px', fontWeight: 700,
                                background: '#3b82f6', color: 'white', border: 'none', cursor: 'pointer'
                            }}>Start</button>
                        </div>
                    </div>

                    {/* Active Projects Section */}
                    <div style={{
                        background: 'rgba(20, 20, 35, 0.6)',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        borderRadius: '20px',
                        padding: '24px'
                    }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                            <h2 style={{ fontSize: '18px', fontWeight: 600 }}>🚀 Aktywne Projekty (Wdrożenia)</h2>
                            <span style={{ fontSize: '13px', color: '#00d4ff', cursor: 'pointer' }}>Tablica Projektów &gt;</span>
                        </div>

                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            padding: '16px',
                            background: 'rgba(255,255,255,0.03)',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            borderLeft: '3px solid #ffd700',
                            borderRadius: '12px',
                            cursor: 'pointer'
                        }}>
                            <div style={{
                                width: '40px', height: '40px', borderRadius: '8px',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                marginRight: '16px', fontSize: '20px', flexShrink: 0,
                                background: 'rgba(255, 215, 0, 0.15)', color: '#ffd700'
                            }}>
                                📂
                            </div>
                            <div style={{ flex: 1 }}>
                                <div style={{ fontSize: '15px', fontWeight: 600, marginBottom: '4px' }}>Budowa Lejka Sprzedaży B2B</div>
                                <div style={{ fontSize: '12px', color: 'rgba(255,255,255,0.6)' }}>📅 Deadline: Piątek • Status: W trakcie</div>
                            </div>
                            <div style={{ fontSize: '13px', fontWeight: 600, color: '#ffd700' }}>65%</div>
                        </div>
                    </div>
                </div>

                {/* --- RIGHT COLUMN --- */}
                <div>
                    {/* Stats */}
                    <div style={{
                        background: 'rgba(20, 20, 35, 0.6)',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        borderRadius: '20px',
                        padding: '24px',
                        marginBottom: '24px'
                    }}>
                        <div style={{ fontSize: '18px', fontWeight: 600, marginBottom: '20px' }}>Twój Postęp</div>

                        <div style={{
                            background: 'linear-gradient(135deg, rgba(176, 0, 255, 0.1), rgba(0, 0, 0, 0))',
                            border: '1px solid rgba(176, 0, 255, 0.2)',
                            borderRadius: '16px',
                            padding: '20px',
                            textAlign: 'center',
                            marginBottom: '16px'
                        }}>
                            <div style={{ fontSize: '32px', fontWeight: 700, color: '#fff', marginBottom: '4px' }}>12</div>
                            <div style={{ fontSize: '12px', color: '#b000ff', textTransform: 'uppercase', letterSpacing: '1px' }}>Ukończonych Symulacji</div>
                        </div>

                        <div style={{
                            background: 'linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0,0,0,0))',
                            border: '1px solid rgba(0, 212, 255, 0.2)',
                            borderRadius: '16px',
                            padding: '20px',
                            textAlign: 'center'
                        }}>
                            <div style={{ fontSize: '32px', fontWeight: 700, color: '#fff', marginBottom: '4px' }}>85%</div>
                            <div style={{ fontSize: '12px', color: '#00d4ff', textTransform: 'uppercase', letterSpacing: '1px' }}>Śr. Skuteczność</div>
                        </div>
                    </div>

                    {/* Game Teaser */}
                    <div style={{
                        background: 'url(\'https://images.unsplash.com/photo-1614728263952-84ea2563bc74?auto=format&fit=crop&q=80\')',
                        backgroundSize: 'cover',
                        backgroundPosition: 'center',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        borderRadius: '20px',
                        height: '200px',
                        position: 'relative',
                        overflow: 'hidden',
                        display: 'flex',
                        alignItems: 'flex-end'
                    }}>
                        <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', background: 'linear-gradient(to bottom, transparent, #0f0f13)' }}></div>
                        <div style={{ position: 'relative', zIndex: 2, padding: '24px' }}>
                            <div style={{ display: 'inline-block', padding: '4px 8px', borderRadius: '4px', background: 'rgba(0,0,0,0.8)', color: '#b000ff', fontSize: '11px', fontWeight: 800, marginBottom: '8px' }}>NOWA GRA</div>
                            <div style={{ fontSize: '16px', fontWeight: 700, marginBottom: '4px', color: 'white' }}>Negocjacje: Horyzont</div>
                            <div style={{ fontSize: '12px', color: 'rgba(255,255,255,0.7)' }}>Uratuj kontrakt roku.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
