export default function GryView() {
    return (
        <div style={{ padding: '32px 48px' }}>
            <h1 style={{ fontSize: '32px', fontWeight: 700, marginBottom: '8px' }}>
                🎮 Gry Biznesowe
            </h1>
            <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px', marginBottom: '32px' }}>
                Zarządzaj wirtualnymi firmami, realizuj kontrakty, buduj reputację
            </p>

            <div style={{
                background: 'rgba(20, 20, 35, 0.6)',
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '20px',
                padding: '48px 32px',
                textAlign: 'center'
            }}>
                <p style={{
                    color: 'rgba(255, 255, 255, 0.5)',
                    fontSize: '16px'
                }}>
                    Zawartość w przygotowaniu...
                </p>
            </div>
        </div>
    )
}
