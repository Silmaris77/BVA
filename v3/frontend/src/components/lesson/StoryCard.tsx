'use client'

interface StoryCardProps {
    icon?: string
    badge?: string
    title: string
    scenario: {
        heading: string
        text: string
    }
    consequences: string[]
    lesson: {
        heading: string
        text: string
    }
}

export default function StoryCard({ icon = '⚠️', badge, title, scenario, consequences, lesson }: StoryCardProps) {
    return (
        <div style={{
            maxWidth: '900px',
            width: '100%',
            background: 'linear-gradient(135deg, rgba(218, 41, 28, 0.1), rgba(239, 68, 68, 0.05))',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            border: '2px solid rgba(218, 41, 28, 0.3)',
            borderRadius: '24px',
            padding: '40px',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)'
        }}>
            {/* Header */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '20px',
                marginBottom: '25px',
                paddingBottom: '20px',
                borderBottom: '2px solid rgba(218, 41, 28, 0.2)'
            }}>
                <div style={{ fontSize: '3rem', flexShrink: 0 }}>{icon}</div>
                <div style={{ flex: 1 }}>
                    {badge && (
                        <div style={{
                            display: 'inline-block',
                            background: 'rgba(218, 41, 28, 0.2)',
                            padding: '6px 15px',
                            borderRadius: '20px',
                            fontSize: '0.85rem',
                            color: '#ef4444',
                            marginBottom: '10px',
                            fontWeight: 600
                        }}>
                            {badge}
                        </div>
                    )}
                    <h3 style={{
                        fontSize: '1.5rem',
                        color: '#DA291C',
                        fontWeight: 700,
                        margin: 0
                    }}>
                        {title}
                    </h3>
                </div>
            </div>

            {/* Scenario */}
            <div style={{
                background: 'rgba(0, 0, 0, 0.3)',
                borderLeft: '4px solid #DA291C',
                padding: '25px',
                borderRadius: '12px',
                marginBottom: '20px'
            }}>
                <h4 style={{
                    color: '#DA291C',
                    marginBottom: '15px',
                    fontSize: '1.2rem',
                    fontWeight: 600
                }}>
                    {scenario.heading}
                </h4>
                <p style={{
                    fontSize: '1.1rem',
                    lineHeight: 1.8,
                    margin: 0,
                    color: 'rgba(255, 255, 255, 0.9)'
                }}>
                    {scenario.text}
                </p>
            </div>

            {/* Consequences */}
            <div style={{ marginBottom: '25px' }}>
                <h4 style={{
                    color: '#ef4444',
                    marginBottom: '15px',
                    fontSize: '1.2rem',
                    fontWeight: 600
                }}>
                    Skutki:
                </h4>
                {consequences.map((consequence, index) => (
                    <div
                        key={index}
                        style={{
                            display: 'flex',
                            alignItems: 'flex-start',
                            gap: '15px',
                            padding: '15px',
                            marginBottom: '12px',
                            background: 'rgba(239, 68, 68, 0.1)',
                            borderLeft: '3px solid #ef4444',
                            borderRadius: '8px'
                        }}
                    >
                        <span style={{ fontSize: '1.3rem', flexShrink: 0 }}>➡️</span>
                        <span style={{
                            fontSize: '1rem',
                            lineHeight: 1.6,
                            color: 'rgba(255, 255, 255, 0.9)'
                        }}>
                            {consequence}
                        </span>
                    </div>
                ))}
            </div>

            {/* Lesson */}
            <div style={{
                background: 'rgba(0, 255, 135, 0.1)',
                border: '2px solid rgba(0, 255, 135, 0.3)',
                borderRadius: '12px',
                padding: '25px'
            }}>
                <h4 style={{
                    color: '#00ff87',
                    marginBottom: '15px',
                    fontSize: '1.2rem',
                    fontWeight: 600
                }}>
                    {lesson.heading}
                </h4>
                <p style={{
                    fontSize: '1.1rem',
                    lineHeight: 1.8,
                    margin: 0,
                    color: 'rgba(255, 255, 255, 0.9)'
                }}
                    dangerouslySetInnerHTML={{ __html: lesson.text.replace(/\*\*(.*?)\*\*/g, '<strong style="color: #00ff87">$1</strong>') }}
                />
            </div>
        </div>
    )
}
