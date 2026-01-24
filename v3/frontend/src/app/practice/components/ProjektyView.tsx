import { Folder, CheckCircle, Clock, Search } from 'lucide-react'

export default function ProjektyView() {
    return (
        <div style={{ maxWidth: '1200px' }}>
            <div style={{ marginBottom: '32px' }}>
                <h1 style={{ fontSize: '32px', fontWeight: 700, marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <Folder size={32} color="#ffd700" />
                    Projekty Wdrożeniowe (OJT)
                </h1>
                <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px' }}>
                    Realizuj zadania w świecie rzeczywistym. Planuj, wykonuj i raportuj wyniki.
                </p>
            </div>

            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
                gap: '24px'
            }}>
                {/* Project Card 1 */}
                <div style={{
                    background: 'rgba(20, 20, 35, 0.6)',
                    border: '1px solid rgba(255, 255, 255, 0.08)',
                    borderLeft: '4px solid #ffd700',
                    borderRadius: '20px',
                    padding: '24px',
                    cursor: 'pointer',
                    display: 'flex', flexDirection: 'column'
                }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                        <span style={{ fontSize: '11px', fontWeight: 700, padding: '4px 8px', borderRadius: '6px', background: 'rgba(255, 215, 0, 0.1)', color: '#ffd700', textTransform: 'uppercase' }}>
                            W Toku
                        </span>
                        <div style={{ width: '40px', height: '40px', background: 'rgba(255, 215, 0, 0.1)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#ffd700', fontSize: '20px' }}>
                            📝
                        </div>
                    </div>

                    <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '8px' }}>Budowa Lejka Sprzedaży</h3>
                    <p style={{ fontSize: '13px', color: 'rgba(255,255,255,0.6)', lineHeight: 1.5, marginBottom: '24px', flex: 1 }}>
                        Zadanie z lekcji "Strategia Sprzedaży". Zmapuj proces decyzyjny u klienta kluczowego i załącz plik z analizą interesariuszy.
                    </p>

                    <div style={{ marginTop: 'auto' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: 'rgba(255,255,255,0.5)', marginBottom: '8px' }}>
                            <span>Postęp</span>
                            <span>65%</span>
                        </div>
                        <div style={{ height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                            <div style={{ width: '65%', height: '100%', background: '#ffd700', borderRadius: '3px' }}></div>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '16px', fontSize: '12px', color: '#ffd700', fontWeight: 600 }}>
                            +500 XP
                        </div>
                    </div>
                </div>

                {/* Project Card 2 */}
                <div style={{
                    background: 'rgba(20, 20, 35, 0.6)',
                    border: '1px solid rgba(255, 255, 255, 0.08)',
                    borderLeft: '4px solid #00ff88',
                    borderRadius: '20px',
                    padding: '24px',
                    cursor: 'pointer',
                    display: 'flex', flexDirection: 'column',
                    opacity: 0.8
                }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                        <span style={{ fontSize: '11px', fontWeight: 700, padding: '4px 8px', borderRadius: '6px', background: 'rgba(0, 255, 136, 0.1)', color: '#00ff88', textTransform: 'uppercase' }}>
                            Nowe
                        </span>
                        <div style={{ width: '40px', height: '40px', background: 'rgba(0, 255, 136, 0.1)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#00ff88', fontSize: '20px' }}>
                            🤝
                        </div>
                    </div>

                    <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '8px' }}>Shadowing: Obserwacja</h3>
                    <p style={{ fontSize: '13px', color: 'rgba(255,255,255,0.6)', lineHeight: 1.5, marginBottom: '24px', flex: 1 }}>
                        Udaj się na spotkanie z Senior Managerem i wypełnij kartę obserwacji z jego negocjacji.
                    </p>

                    <div style={{ marginTop: 'auto' }}>
                        <button style={{
                            width: '100%', padding: '10px', borderRadius: '12px',
                            border: '1px solid rgba(255,255,255,0.2)', background: 'transparent',
                            color: 'white', fontSize: '13px', cursor: 'pointer'
                        }}>
                            Rozpocznij Projekt
                        </button>
                    </div>
                </div>

            </div>
        </div>
    )
}
