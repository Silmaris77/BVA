import { Gamepad2 } from 'lucide-react'

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

            <div style={{ textAlign: 'center', padding: '40px', color: 'rgba(255,255,255,0.4)' }}>
                Więcej scenariuszy wkrótce...
            </div>
        </div>
    )
}
