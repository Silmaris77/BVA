import { Gamepad2, Brain } from 'lucide-react'
import Link from 'next/link'

export default function GryView() {
    return (
        <div style={{ maxWidth: '1200px' }}>
            <h1 style={{ fontSize: '32px', fontWeight: 700, marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                <Gamepad2 size={32} color="#b000ff" />
                Gry Biznesowe (Symulacje)
            </h1>
            <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px', marginBottom: '32px' }}>
                Złożone scenariusze fabularne, w których Twoje decyzje mają realne konsekwencje.
            </p>

            {/* Featured Game Banner */}
            <div style={{
                background: 'linear-gradient(135deg, rgba(80, 20, 100, 0.8), rgba(20, 20, 35, 0.9)), url(\'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&q=80\')',
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                borderRadius: '20px',
                padding: '48px',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                position: 'relative',
                overflow: 'hidden',
                marginBottom: '48px'
            }}>
                <div style={{ position: 'relative', zIndex: 2, maxWidth: '500px' }}>
                    <span style={{
                        background: '#00d4ff', color: '#000', fontSize: '12px', fontWeight: 800,
                        padding: '6px 12px', borderRadius: '6px', display: 'inline-block', marginBottom: '16px'
                    }}>
                        PREMIERA SEZONU 1
                    </span>
                    <h2 style={{ fontSize: '36px', fontWeight: 800, margin: '0 0 16px 0', lineHeight: 1.2 }}>
                        Projekt "Horyzont"
                    </h2>
                    <p style={{ color: 'rgba(255, 255, 255, 0.8)', fontSize: '16px', lineHeight: 1.6, marginBottom: '32px' }}>
                        Wciel się w rolę Key Account Managera. Czeka Cię trudna rozmowa z Dyrektorem Zakupów, który chce zerwać kontrakt. Czy uratujesz umowę i utrzymasz marżę?
                    </p>
                    <button style={{
                        background: 'white', color: 'black', padding: '14px 32px', borderRadius: '30px',
                        fontSize: '16px', fontWeight: 700, border: 'none', cursor: 'pointer',
                        display: 'inline-flex', alignItems: 'center', gap: '8px',
                        boxShadow: '0 10px 20px rgba(0,0,0,0.3)'
                    }}>
                        ▶ Rozpocznij Symulację
                    </button>
                </div>
            </div>

            {/* Game Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '24px' }}>

                {/* BrainVenture Card */}
                <Link href="/brainventure" style={{ textDecoration: 'none' }}>
                    <div className="group" style={{
                        background: 'rgba(255, 255, 255, 0.05)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '16px',
                        overflow: 'hidden',
                        transition: 'transform 0.3s ease, border-color 0.3s ease',
                        cursor: 'pointer',
                        height: '100%',
                        display: 'flex',
                        flexDirection: 'column'
                    }}>
                        <div style={{
                            height: '180px',
                            background: 'linear-gradient(to bottom, transparent, rgba(0,0,0,0.8)), url(\'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&q=80\') center/cover',
                            position: 'relative'
                        }}>
                            <div style={{ position: 'absolute', top: 12, right: 12, background: 'rgba(0,0,0,0.6)', padding: '4px 8px', borderRadius: '4px', fontSize: '10px', fontWeight: 700, color: '#a855f7', border: '1px solid #a855f7' }}>
                                NEW
                            </div>
                        </div>
                        <div style={{ padding: '24px', flex: 1, display: 'flex', flexDirection: 'column' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                                <Brain size={16} color="#a855f7" />
                                <span style={{ fontSize: '12px', fontWeight: 700, color: '#a855f7', letterSpacing: '0.05em' }}>NEURO-ZARZĄDZANIE</span>
                            </div>
                            <h3 style={{ fontSize: '20px', fontWeight: 700, margin: '0 0 8px 0', color: 'white' }}>BrainVenture</h3>
                            <p style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.6)', lineHeight: 1.5, marginBottom: '24px', flex: 1 }}>
                                Zarządzaj zespołem w oparciu o wiedzę o mózgu. Dbaj o zasoby poznawcze, efektywność i realizuj kontrakty w neuro-futurystycznym otoczeniu.
                            </p>
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 'auto' }}>
                                <span style={{ fontSize: '12px', color: 'rgba(255,255,255,0.4)' }}>Czas gry: ~15 min</span>
                                <span style={{ color: 'white', fontWeight: 600, fontSize: '14px' }}>Zagraj <i className="fa-solid fa-arrow-right" style={{ marginLeft: '4px' }}></i></span>
                            </div>
                        </div>
                    </div>
                </Link>

                {/* Dream Team Consulting Card */}
                <Link href="/practice/games/consulting" style={{ textDecoration: 'none' }}>
                    <div className="group" style={{
                        background: 'rgba(255, 255, 255, 0.05)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '16px',
                        overflow: 'hidden',
                        transition: 'transform 0.3s ease, border-color 0.3s ease',
                        cursor: 'pointer',
                        height: '100%',
                        display: 'flex',
                        flexDirection: 'column'
                    }}>
                        <div style={{
                            height: '180px',
                            background: 'linear-gradient(to bottom, transparent, rgba(0,0,0,0.8)), url(\'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&q=80\') center/cover',
                            position: 'relative'
                        }}>
                        </div>
                        <div style={{ padding: '24px', flex: 1, display: 'flex', flexDirection: 'column' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                                <i className="fa-solid fa-briefcase" style={{ color: '#00d4ff' }}></i>
                                <span style={{ fontSize: '12px', fontWeight: 700, color: '#00d4ff', letterSpacing: '0.05em' }}>STRATEGIA & ZARZĄDZANIE</span>
                            </div>
                            <h3 style={{ fontSize: '20px', fontWeight: 700, margin: '0 0 8px 0', color: 'white' }}>Dream Team Consulting</h3>
                            <p style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.6)', lineHeight: 1.5, marginBottom: '24px', flex: 1 }}>
                                Buduj własną firmę doradczą. Rekrutuj konsultantów, negocjuj kontrakty i zarządzaj biurem w dynamicznym świecie biznesu.
                            </p>
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 'auto' }}>
                                <span style={{ fontSize: '12px', color: 'rgba(255,255,255,0.4)' }}>Czas gry: ~20 min</span>
                                <span style={{ color: 'white', fontWeight: 600, fontSize: '14px' }}>Zagraj <i className="fa-solid fa-arrow-right" style={{ marginLeft: '4px' }}></i></span>
                            </div>
                        </div>
                    </div>
                </Link>


                {/* Placeholder Card */}
                <div style={{ opacity: 0.5, pointerEvents: 'none', filter: 'grayscale(1)' }}>
                    <div style={{
                        background: 'rgba(255, 255, 255, 0.02)',
                        border: '1px solid rgba(255, 255, 255, 0.05)',
                        borderRadius: '16px',
                        overflow: 'hidden',
                        height: '100%'
                    }}>
                        <div style={{ height: '180px', background: 'rgba(0,0,0,0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <span style={{ fontSize: '48px', color: 'rgba(255,255,255,0.1)' }}>?</span>
                        </div>
                        <div style={{ padding: '24px' }}>
                            <h3 style={{ fontSize: '20px', fontWeight: 700, margin: '0 0 8px 0', color: 'rgba(255,255,255,0.3)' }}>Wkrótce...</h3>
                            <p style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.2)' }}>Więcej symulacji w przygotowaniu.</p>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    )
}
