'use client'

import { useEffect } from 'react'
import { useTheme } from '@/contexts/ThemeContext'
import { Zap, Battery, Gauge, Power, CircuitBoard, Plug, Activity, AlertTriangle, CheckCircle, XCircle, Wifi, WifiOff } from 'lucide-react'
import Link from 'next/link'

export default function VoltageDemoPage() {
    const { setTheme } = useTheme()
    
    // Automatycznie przełącz na motyw Voltage
    useEffect(() => {
        setTheme('voltage')
    }, [setTheme])

    return (
        <div style={{ padding: '32px', maxWidth: '1200px', margin: '0 auto' }}>
            {/* Header */}
            <div style={{ marginBottom: '48px', textAlign: 'center' }}>
                <h1 style={{ 
                    fontSize: '36px', 
                    fontWeight: 900,
                    fontFamily: "'JetBrains Mono', monospace",
                    textTransform: 'uppercase',
                    letterSpacing: '4px',
                    marginBottom: '16px'
                }}>
                    ⚡ VOLTAGE THEME DEMO ⚡
                </h1>
                <p style={{ color: 'var(--t-text-muted)', fontSize: '14px' }}>
                    Mockup wszystkich proponowanych efektów dla motywu elektrycznego
                </p>
            </div>

            {/* 1. HAZARD STRIPES */}
            <section style={{ marginBottom: '48px' }}>
                <h2 style={{ 
                    fontSize: '18px', 
                    fontFamily: "'JetBrains Mono', monospace",
                    marginBottom: '16px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                }}>
                    <AlertTriangle size={20} color="#ffcc00" />
                    1. Hazard Stripes (Paski ostrzegawcze)
                </h2>
                
                {/* Hazard Bar */}
                <div style={{
                    background: 'repeating-linear-gradient(-45deg, #ffcc00 0px, #ffcc00 10px, #1a1a1a 10px, #1a1a1a 20px)',
                    height: '8px',
                    width: '100%',
                    marginBottom: '16px',
                    borderRadius: '2px'
                }} />
                
                <div className="glass-card" style={{ padding: '20px' }}>
                    <p>Separator sekcji lub element dekoracyjny dla ważnych obszarów</p>
                </div>
                
                {/* Hazard Bar Bottom */}
                <div style={{
                    background: 'repeating-linear-gradient(-45deg, #ffcc00 0px, #ffcc00 10px, #1a1a1a 10px, #1a1a1a 20px)',
                    height: '8px',
                    width: '100%',
                    marginTop: '16px',
                    borderRadius: '2px'
                }} />
            </section>

            {/* 2. LCD DISPLAY */}
            <section style={{ marginBottom: '48px' }}>
                <h2 style={{ 
                    fontSize: '18px', 
                    fontFamily: "'JetBrains Mono', monospace",
                    marginBottom: '16px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                }}>
                    <Gauge size={20} color="#00e5ff" />
                    2. LCD Display (Wyświetlacz)
                </h2>
                
                <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
                    {/* LCD Style Stat */}
                    <div style={{
                        background: '#080a0f',
                        border: '2px solid rgba(0, 229, 255, 0.3)',
                        borderRadius: '4px',
                        padding: '16px 24px',
                        boxShadow: 'inset 0 2px 10px rgba(0, 0, 0, 0.8)',
                        minWidth: '150px'
                    }}>
                        <div style={{ 
                            fontSize: '12px', 
                            color: '#8a8d9b',
                            textTransform: 'uppercase',
                            letterSpacing: '1px',
                            marginBottom: '4px'
                        }}>XP Points</div>
                        <div style={{
                            fontFamily: "'Share Tech Mono', 'JetBrains Mono', monospace",
                            fontSize: '32px',
                            fontWeight: 700,
                            color: '#00e5ff',
                            textShadow: '0 0 15px rgba(0, 229, 255, 0.8)',
                            letterSpacing: '2px'
                        }}>21,285</div>
                    </div>
                    
                    {/* Green LCD */}
                    <div style={{
                        background: '#080a0f',
                        border: '2px solid rgba(0, 255, 136, 0.3)',
                        borderRadius: '4px',
                        padding: '16px 24px',
                        boxShadow: 'inset 0 2px 10px rgba(0, 0, 0, 0.8)',
                        minWidth: '150px'
                    }}>
                        <div style={{ 
                            fontSize: '12px', 
                            color: '#8a8d9b',
                            textTransform: 'uppercase',
                            letterSpacing: '1px',
                            marginBottom: '4px'
                        }}>Streak</div>
                        <div style={{
                            fontFamily: "'Share Tech Mono', 'JetBrains Mono', monospace",
                            fontSize: '32px',
                            fontWeight: 700,
                            color: '#00ff88',
                            textShadow: '0 0 15px rgba(0, 255, 136, 0.8)',
                            letterSpacing: '2px'
                        }}>7 DNI</div>
                    </div>

                    {/* Warning LCD */}
                    <div style={{
                        background: '#080a0f',
                        border: '2px solid rgba(255, 204, 0, 0.3)',
                        borderRadius: '4px',
                        padding: '16px 24px',
                        boxShadow: 'inset 0 2px 10px rgba(0, 0, 0, 0.8)',
                        minWidth: '150px'
                    }}>
                        <div style={{ 
                            fontSize: '12px', 
                            color: '#8a8d9b',
                            textTransform: 'uppercase',
                            letterSpacing: '1px',
                            marginBottom: '4px'
                        }}>Voltage</div>
                        <div style={{
                            fontFamily: "'Share Tech Mono', 'JetBrains Mono', monospace",
                            fontSize: '32px',
                            fontWeight: 700,
                            color: '#ffcc00',
                            textShadow: '0 0 15px rgba(255, 204, 0, 0.8)',
                            letterSpacing: '2px'
                        }}>230V</div>
                    </div>
                </div>
            </section>

            {/* 3. PULSE ANIMATION */}
            <section style={{ marginBottom: '48px' }}>
                <h2 style={{ 
                    fontSize: '18px', 
                    fontFamily: "'JetBrains Mono', monospace",
                    marginBottom: '16px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                }}>
                    <Activity size={20} color="#00e5ff" />
                    3. Efekt "Zasilania" (Pulse Animation)
                </h2>
                
                <style dangerouslySetInnerHTML={{ __html: `
                    @keyframes powerPulse {
                        0%, 100% { box-shadow: 0 0 5px rgba(0, 229, 255, 0.3), inset 0 0 5px rgba(0, 229, 255, 0.1); }
                        50% { box-shadow: 0 0 20px rgba(0, 229, 255, 0.6), inset 0 0 10px rgba(0, 229, 255, 0.2); }
                    }
                    .power-pulse {
                        animation: powerPulse 3s ease-in-out infinite;
                    }
                    @keyframes ledBlink {
                        0%, 90%, 100% { opacity: 1; }
                        95% { opacity: 0.5; }
                    }
                    .led-active {
                        animation: ledBlink 2s ease-in-out infinite;
                    }
                `}} />
                
                <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
                    <div 
                        className="glass-card power-pulse" 
                        style={{ 
                            padding: '24px', 
                            display: 'flex', 
                            alignItems: 'center', 
                            gap: '12px',
                            borderColor: 'rgba(0, 229, 255, 0.4)'
                        }}
                    >
                        <Power size={24} color="#00e5ff" />
                        <span>Aktywny element z pulsującym glow</span>
                    </div>
                </div>
            </section>

            {/* 4. ELECTRIC ICONS */}
            <section style={{ marginBottom: '48px' }}>
                <h2 style={{ 
                    fontSize: '18px', 
                    fontFamily: "'JetBrains Mono', monospace",
                    marginBottom: '16px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                }}>
                    <CircuitBoard size={20} color="#00e5ff" />
                    4. Ikony Elektryczne
                </h2>
                
                <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap' }}>
                    {[
                        { icon: Zap, label: 'XP', color: '#ffcc00' },
                        { icon: Battery, label: 'Energia', color: '#00ff88' },
                        { icon: Gauge, label: 'Poziom', color: '#00e5ff' },
                        { icon: Power, label: 'Status', color: '#00e5ff' },
                        { icon: CircuitBoard, label: 'Moduły', color: '#00e5ff' },
                        { icon: Plug, label: 'Połączenie', color: '#00e5ff' },
                        { icon: Activity, label: 'Aktywność', color: '#00ff88' },
                    ].map((item, i) => (
                        <div key={i} style={{
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            gap: '8px',
                            padding: '16px',
                            background: 'rgba(0, 229, 255, 0.05)',
                            borderRadius: '8px',
                            border: '1px solid rgba(0, 229, 255, 0.1)'
                        }}>
                            <item.icon size={32} color={item.color} />
                            <span style={{ fontSize: '12px', color: '#8a8d9b' }}>{item.label}</span>
                        </div>
                    ))}
                </div>
            </section>

            {/* 5. GLOW ON HOVER */}
            <section style={{ marginBottom: '48px' }}>
                <h2 style={{ 
                    fontSize: '18px', 
                    fontFamily: "'JetBrains Mono', monospace",
                    marginBottom: '16px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                }}>
                    <Zap size={20} color="#00e5ff" />
                    5. Glow na Hover
                </h2>
                
                <style dangerouslySetInnerHTML={{ __html: `
                    .voltage-btn {
                        background: #ffcc00;
                        color: #000;
                        font-family: 'JetBrains Mono', monospace;
                        font-weight: 900;
                        text-transform: uppercase;
                        letter-spacing: 1px;
                        border: none;
                        border-radius: 4px;
                        padding: 14px 28px;
                        cursor: pointer;
                        box-shadow: 0 4px 0 #997a00, 0 8px 20px rgba(0, 0, 0, 0.3);
                        transition: all 0.15s ease;
                    }
                    .voltage-btn:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 6px 0 #997a00, 0 12px 30px rgba(255, 204, 0, 0.4);
                    }
                    .voltage-btn:active {
                        transform: translateY(2px);
                        box-shadow: 0 2px 0 #997a00;
                    }
                    .voltage-btn-cyan {
                        background: linear-gradient(180deg, #00e5ff 0%, #00b8cc 100%);
                        box-shadow: 0 4px 0 #007a8a, 0 8px 20px rgba(0, 0, 0, 0.3);
                    }
                    .voltage-btn-cyan:hover {
                        box-shadow: 0 6px 0 #007a8a, 0 12px 30px rgba(0, 229, 255, 0.4);
                    }
                    .voltage-btn-cyan:active {
                        box-shadow: 0 2px 0 #007a8a;
                    }
                    .voltage-link {
                        color: #00e5ff;
                        text-decoration: none;
                        transition: all 0.2s ease;
                        padding: 4px 8px;
                        border-radius: 4px;
                    }
                    .voltage-link:hover {
                        background: rgba(0, 229, 255, 0.1);
                        text-shadow: 0 0 10px rgba(0, 229, 255, 0.8);
                    }
                `}} />
                
                <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', alignItems: 'center' }}>
                    <button className="voltage-btn">⚡ Akcja główna</button>
                    <button className="voltage-btn voltage-btn-cyan">Akcja drugorzędna</button>
                    <a href="#" className="voltage-link">Link z glow →</a>
                </div>
            </section>

            {/* 6. TERMINAL/CONSOLE LOOK */}
            <section style={{ marginBottom: '48px' }}>
                <h2 style={{ 
                    fontSize: '18px', 
                    fontFamily: "'JetBrains Mono', monospace",
                    marginBottom: '16px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                }}>
                    <CircuitBoard size={20} color="#00e5ff" />
                    6. Terminal/Konsola Look
                </h2>
                
                <div style={{
                    background: '#0a0e14',
                    border: '1px solid rgba(0, 229, 255, 0.2)',
                    borderRadius: '8px',
                    padding: '20px',
                    fontFamily: "'JetBrains Mono', monospace",
                    fontSize: '14px'
                }}>
                    <div style={{ color: '#8a8d9b', marginBottom: '8px' }}>// System Status</div>
                    <div style={{ marginBottom: '4px' }}>
                        <span style={{ color: '#00e5ff' }}>USER:</span> 
                        <span style={{ color: '#e8eef5', marginLeft: '8px' }}>admin@brainventure</span>
                    </div>
                    <div style={{ marginBottom: '4px' }}>
                        <span style={{ color: '#00ff88' }}>STATUS:</span> 
                        <span style={{ color: '#00ff88', marginLeft: '8px' }}>● ONLINE</span>
                    </div>
                    <div style={{ marginBottom: '4px' }}>
                        <span style={{ color: '#ffcc00' }}>POWER:</span> 
                        <span style={{ color: '#ffcc00', marginLeft: '8px' }}>230V / 50Hz</span>
                    </div>
                    <div style={{ marginBottom: '4px' }}>
                        <span style={{ color: '#00e5ff' }}>UPTIME:</span> 
                        <span style={{ color: '#e8eef5', marginLeft: '8px' }}>7d 14h 32m</span>
                    </div>
                    <div style={{ marginTop: '12px', color: '#00e5ff' }}>
                        &gt; Ready for input_
                        <span style={{ animation: 'blink 1s infinite' }}>▌</span>
                    </div>
                </div>
                
                <style dangerouslySetInnerHTML={{ __html: `
                    @keyframes blink {
                        0%, 50% { opacity: 1; }
                        51%, 100% { opacity: 0; }
                    }
                `}} />
            </section>

            {/* 9. STATUS INDICATORS (LED) */}
            <section style={{ marginBottom: '48px' }}>
                <h2 style={{ 
                    fontSize: '18px', 
                    fontFamily: "'JetBrains Mono', monospace",
                    marginBottom: '16px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                }}>
                    <Power size={20} color="#00e5ff" />
                    9. Status Indicators (LED)
                </h2>
                
                <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap' }}>
                    {/* Online */}
                    <div className="glass-card" style={{ padding: '16px 24px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <div className="led-active" style={{
                            width: '12px',
                            height: '12px',
                            borderRadius: '50%',
                            background: '#00ff88',
                            boxShadow: '0 0 10px #00ff88, 0 0 20px rgba(0, 255, 136, 0.5)'
                        }} />
                        <span>System Online</span>
                        <Wifi size={16} color="#00ff88" />
                    </div>
                    
                    {/* Warning */}
                    <div className="glass-card" style={{ padding: '16px 24px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <div style={{
                            width: '12px',
                            height: '12px',
                            borderRadius: '50%',
                            background: '#ffcc00',
                            boxShadow: '0 0 10px #ffcc00, 0 0 20px rgba(255, 204, 0, 0.5)',
                            animation: 'ledBlink 0.5s ease-in-out infinite'
                        }} />
                        <span>High Voltage Warning</span>
                        <AlertTriangle size={16} color="#ffcc00" />
                    </div>
                    
                    {/* Offline */}
                    <div className="glass-card" style={{ padding: '16px 24px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <div style={{
                            width: '12px',
                            height: '12px',
                            borderRadius: '50%',
                            background: '#ff4444',
                            boxShadow: '0 0 10px #ff4444, 0 0 20px rgba(255, 68, 68, 0.5)'
                        }} />
                        <span>Connection Lost</span>
                        <WifiOff size={16} color="#ff4444" />
                    </div>
                </div>
            </section>

            {/* 10. BREADCRUMB WITH POWER FLOW */}
            <section style={{ marginBottom: '48px' }}>
                <h2 style={{ 
                    fontSize: '18px', 
                    fontFamily: "'JetBrains Mono', monospace",
                    marginBottom: '16px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                }}>
                    <Zap size={20} color="#00e5ff" />
                    10. Breadcrumb z "przepływem prądu"
                </h2>
                
                <style dangerouslySetInnerHTML={{ __html: `
                    @keyframes powerFlow {
                        0% { background-position: 0% 50%; }
                        100% { background-position: 200% 50%; }
                    }
                    .power-line {
                        height: 2px;
                        background: linear-gradient(90deg, 
                            transparent 0%, 
                            #00e5ff 25%, 
                            #00ffff 50%, 
                            #00e5ff 75%, 
                            transparent 100%
                        );
                        background-size: 200% 100%;
                        animation: powerFlow 2s linear infinite;
                    }
                `}} />
                
                <div style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: '0',
                    padding: '16px 24px',
                    background: 'rgba(0, 229, 255, 0.05)',
                    borderRadius: '8px',
                    border: '1px solid rgba(0, 229, 255, 0.1)'
                }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Power size={16} color="#00ff88" />
                        <span style={{ color: '#00e5ff' }}>Hub</span>
                    </div>
                    
                    <div className="power-line" style={{ width: '40px', margin: '0 12px' }} />
                    
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <CircuitBoard size={16} color="#00e5ff" />
                        <span style={{ color: '#00e5ff' }}>Nauka</span>
                    </div>
                    
                    <div className="power-line" style={{ width: '40px', margin: '0 12px' }} />
                    
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Zap size={16} color="#ffcc00" />
                        <span style={{ color: '#e8eef5', fontWeight: 700 }}>Lekcja: Podstawy Elektryki</span>
                    </div>
                </div>
            </section>

            {/* CARD SHOWCASE */}
            <section style={{ marginBottom: '48px' }}>
                <h2 style={{ 
                    fontSize: '18px', 
                    fontFamily: "'JetBrains Mono', monospace",
                    marginBottom: '16px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                }}>
                    <CircuitBoard size={20} color="#00e5ff" />
                    Karty z efektami
                </h2>
                
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
                    {/* Standard Card */}
                    <div className="glass-card" style={{ padding: '24px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                            <div className="led-active" style={{
                                width: '8px',
                                height: '8px',
                                borderRadius: '50%',
                                background: '#00ff88',
                                boxShadow: '0 0 8px #00ff88'
                            }} />
                            <h3 style={{ fontSize: '16px', fontWeight: 700 }}>Moduł Aktywny</h3>
                        </div>
                        <p style={{ color: '#8a8d9b', fontSize: '14px', marginBottom: '16px' }}>
                            Standardowa karta z lewą cyan ramką i narożnikami w stylu blueprint.
                        </p>
                        <button className="voltage-btn" style={{ width: '100%' }}>
                            <Zap size={16} style={{ marginRight: '8px' }} />
                            Uruchom
                        </button>
                    </div>
                    
                    {/* Warning Card */}
                    <div className="glass-card" style={{ 
                        padding: '24px',
                        borderLeftColor: '#ffcc00'
                    }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                            <div style={{
                                width: '8px',
                                height: '8px',
                                borderRadius: '50%',
                                background: '#ffcc00',
                                boxShadow: '0 0 8px #ffcc00',
                                animation: 'ledBlink 0.5s ease-in-out infinite'
                            }} />
                            <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#ffcc00' }}>⚠ Uwaga</h3>
                        </div>
                        <p style={{ color: '#8a8d9b', fontSize: '14px', marginBottom: '16px' }}>
                            Karta ostrzegawcza z żółtą ramką i pulsującą diodą LED.
                        </p>
                        <div style={{
                            background: 'repeating-linear-gradient(-45deg, #ffcc00 0px, #ffcc00 10px, #1a1a1a 10px, #1a1a1a 20px)',
                            height: '6px',
                            width: '100%',
                            borderRadius: '2px'
                        }} />
                    </div>
                    
                    {/* Disabled Card */}
                    <div className="glass-card" style={{ 
                        padding: '24px',
                        opacity: 0.5,
                        borderLeftColor: '#ff4444'
                    }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                            <div style={{
                                width: '8px',
                                height: '8px',
                                borderRadius: '50%',
                                background: '#ff4444',
                                boxShadow: '0 0 8px #ff4444'
                            }} />
                            <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#ff4444' }}>Offline</h3>
                        </div>
                        <p style={{ color: '#8a8d9b', fontSize: '14px', marginBottom: '16px' }}>
                            Nieaktywny moduł - brak zasilania.
                        </p>
                        <button disabled style={{ 
                            width: '100%',
                            padding: '14px 28px',
                            background: '#333',
                            color: '#666',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'not-allowed',
                            fontFamily: "'JetBrains Mono', monospace",
                            textTransform: 'uppercase'
                        }}>
                            Niedostępne
                        </button>
                    </div>
                </div>
            </section>

            {/* Back Link */}
            <div style={{ textAlign: 'center', marginTop: '48px' }}>
                <Link href="/" className="voltage-link" style={{ fontSize: '16px' }}>
                    ← Powrót do Hub
                </Link>
            </div>
        </div>
    )
}
