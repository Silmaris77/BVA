'use client'

interface EndingCardProps {
    icon?: string
    title: string
    subtitle?: string
    checklist: {
        icon: string
        text: string
    }[]
    tagline?: string
    next_steps?: {
        text: string
        available: boolean
    }
}

export default function EndingCard({ icon = '✅', title, subtitle, checklist, tagline, next_steps }: EndingCardProps) {
    return (
        <div style={{
            maxWidth: '900px',
            width: '100%',
            background: 'linear-gradient(135deg, rgba(0, 255, 135, 0.15), rgba(96, 239, 255, 0.15))',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            border: '2px solid rgba(0, 255, 135, 0.4)',
            borderRadius: '24px',
            padding: '50px',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
            position: 'relative'
        }}>
            {/* Type Badge - Top Left Corner */}
            <div style={{
                position: 'absolute',
                top: '20px',
                left: '20px',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                fontSize: '11px',
                textTransform: 'uppercase',
                letterSpacing: '1px',
                color: '#00ff87',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(0, 255, 135, 0.1)',
                border: '1px solid rgba(0, 255, 135, 0.2)',
                borderRadius: '20px'
            }}>
                PODSUMOWANIE
            </div>
            {/* Header */}
            <div style={{ textAlign: 'center', marginBottom: '40px' }}>
                <div style={{ fontSize: '5rem', marginBottom: '20px' }}>{icon}</div>
                <h2 style={{
                    fontSize: '2.5rem',
                    fontWeight: 800,
                    marginBottom: '15px',
                    background: 'linear-gradient(135deg, #00ff87, #60efff)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text'
                }}>
                    {title}
                </h2>
                {subtitle && (
                    <p style={{
                        fontSize: '1.2rem',
                        color: 'rgba(255, 255, 255, 0.8)',
                        margin: 0
                    }}>
                        {subtitle}
                    </p>
                )}
            </div>

            {/* Checklist */}
            <div style={{ marginBottom: tagline ? '40px' : '0' }}>
                {checklist.map((item, index) => (
                    <div
                        key={index}
                        style={{
                            display: 'flex',
                            alignItems: 'flex-start',
                            gap: '15px',
                            padding: '20px',
                            marginBottom: '15px',
                            background: 'rgba(0, 255, 135, 0.05)',
                            border: '1px solid rgba(0, 255, 135, 0.2)',
                            borderRadius: '12px',
                            transition: 'all 0.3s ease',
                            cursor: 'default'
                        }}
                        onMouseOver={(e) => {
                            e.currentTarget.style.background = 'rgba(0, 255, 135, 0.1)'
                            e.currentTarget.style.transform = 'translateX(5px)'
                        }}
                        onMouseOut={(e) => {
                            e.currentTarget.style.background = 'rgba(0, 255, 135, 0.05)'
                            e.currentTarget.style.transform = 'translateX(0)'
                        }}
                    >
                        <span style={{
                            fontSize: '1.8rem',
                            color: '#00ff87',
                            flexShrink: 0
                        }}>
                            {item.icon}
                        </span>
                        <span style={{
                            fontSize: '1.1rem',
                            lineHeight: 1.6,
                            color: 'rgba(255, 255, 255, 0.9)',
                            flex: 1
                        }}
                            dangerouslySetInnerHTML={{ __html: item.text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }}
                        />
                    </div>
                ))}
            </div>

            {/* Tagline */}
            {tagline && (
                <div style={{
                    textAlign: 'center',
                    fontSize: '1.5rem',
                    fontWeight: 700,
                    color: '#DA291C',
                    textTransform: 'uppercase',
                    letterSpacing: '2px',
                    padding: '20px',
                    background: 'rgba(218, 41, 28, 0.1)',
                    border: '2px solid rgba(218, 41, 28, 0.3)',
                    borderRadius: '12px',
                    marginTop: '30px'
                }}>
                    {tagline}
                </div>
            )}

            {/* Next Steps */}
            {next_steps && (
                <div style={{
                    marginTop: '30px',
                    padding: '20px',
                    background: 'rgba(96, 239, 255, 0.1)',
                    border: '1px solid rgba(96, 239, 255, 0.2)',
                    borderRadius: '12px',
                    textAlign: 'center'
                }}>
                    <p style={{
                        fontSize: '1.1rem',
                        color: next_steps.available ? '#60efff' : 'rgba(255, 255, 255, 0.5)',
                        margin: 0
                    }}
                        dangerouslySetInnerHTML={{ __html: next_steps.text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }}
                    />
                    {!next_steps.available && (
                        <p style={{
                            fontSize: '0.9rem',
                            color: 'rgba(255, 255, 255, 0.4)',
                            marginTop: '10px',
                            fontStyle: 'italic'
                        }}>
                            (Wkrótce dostępne)
                        </p>
                    )}
                </div>
            )}
        </div>
    )
}
