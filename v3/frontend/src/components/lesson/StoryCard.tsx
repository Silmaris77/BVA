'use client'

import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface StoryCardProps {
    icon?: string
    badge?: string
    title: string
    // Old format (backwards compatible)
    scenario?: {
        heading: string
        text: string
    }
    consequences?: (string | { heading: string; text: string })[]
    lesson?: {
        heading: string
        text: string
    } | string
    // New format (for OJT lessons)
    situation?: string
    scenarios?: Array<{
        type: 'bad' | 'good'
        title: string
        dialogue?: Array<{ speaker: string; text: string }>
        consequences?: string[]
    }>
    phases?: Array<{
        title: string
        type?: string
        dialogue?: Array<{ speaker: string; text: string; isThought?: boolean }>
        content?: string
    }>
    outcome?: string
}

export default function StoryCard({ icon = '⚠️', badge, title, scenario, consequences, lesson, situation, scenarios, phases, outcome }: StoryCardProps) {
    // NEW FORMAT: Multi-scenario with dialogue
    if (scenarios && scenarios.length > 0) {
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
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
                position: 'relative'
            }}>
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
                    color: '#ef4444',
                    fontWeight: 600,
                    padding: '6px 12px',
                    background: 'rgba(239, 68, 68, 0.1)',
                    border: '1px solid rgba(239, 68, 68, 0.2)',
                    borderRadius: '20px'
                }}>
                    HISTORIA
                </div>
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

                {situation && (
                    <div style={{
                        marginBottom: '24px',
                        padding: '20px',
                        background: 'rgba(255, 136, 0, 0.1)',
                        borderRadius: '12px',
                        borderLeft: '4px solid #ff8800'
                    }}>
                        <h4 style={{ color: '#ff8800', marginBottom: '10px', fontSize: '1.1rem' }}>Sytuacja:</h4>
                        <p style={{ margin: 0, lineHeight: 1.6, color: 'rgba(255, 255, 255, 0.9)' }}>{situation}</p>
                    </div>
                )}

                {scenarios.map((sc, idx) => (
                    <div key={idx} style={{ marginBottom: '24px' }}>
                        <div style={{
                            padding: '20px',
                            background: sc.type === 'bad' ? 'rgba(239, 68, 68, 0.1)' : 'rgba(0, 255, 136, 0.1)',
                            borderRadius: '12px',
                            border: `2px solid ${sc.type === 'bad' ? '#ef4444' : '#00ff88'}`
                        }}>
                            <h4 style={{
                                color: sc.type === 'bad' ? '#ef4444' : '#00ff88',
                                marginBottom: '16px',
                                fontSize: '1.2rem',
                                fontWeight: 700
                            }}>
                                {sc.title}
                            </h4>
                            {sc.dialogue && sc.dialogue.map((line, i) => (
                                <div key={i} style={{
                                    marginBottom: '12px',
                                    paddingLeft: '16px',
                                    borderLeft: '2px solid rgba(255, 255, 255, 0.2)'
                                }}>
                                    <div style={{ fontWeight: 600, color: '#00d4ff', marginBottom: '4px' }}>{line.speaker}:</div>
                                    <div style={{ color: 'rgba(255, 255, 255, 0.9)', lineHeight: 1.6 }}>{line.text}</div>
                                </div>
                            ))}
                            {sc.consequences && sc.consequences.length > 0 && (
                                <div style={{ marginTop: '16px', paddingTop: '16px', borderTop: '1px solid rgba(255, 255, 255, 0.1)' }}>
                                    <strong style={{ color: sc.type === 'bad' ? '#ef4444' : '#00ff88' }}>Efekt:</strong>
                                    <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
                                        {sc.consequences.map((c, ci) => (
                                            <li key={ci} style={{ marginBottom: '6px', color: 'rgba(255, 255, 255, 0.9)' }}>{c}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    </div>
                ))}

                {typeof lesson === 'string' && (
                    <div style={{
                        background: 'rgba(0, 255, 135, 0.1)',
                        border: '2px solid rgba(0, 255, 135, 0.3)',
                        borderRadius: '12px',
                        padding: '20px'
                    }}>
                        <strong style={{ color: '#00ff87', fontSize: '1.1rem' }}>Kluczowa lekcja:</strong>
                        <p style={{ margin: '8px 0 0 0', lineHeight: 1.7, color: 'rgba(255, 255, 255, 0.9)' }}>{lesson}</p>
                    </div>
                )}

                {outcome && (
                    <div style={{
                        marginTop: '20px',
                        background: 'rgba(0, 255, 135, 0.1)',
                        border: '2px solid rgba(0, 255, 135, 0.3)',
                        borderRadius: '12px',
                        padding: '20px'
                    }}>
                        <h4 style={{ color: '#00ff87', marginBottom: '10px', fontSize: '1.1rem' }}>Efekt:</h4>
                        <p style={{ margin: 0, lineHeight: 1.6, color: 'rgba(255, 255, 255, 0.9)' }}>{outcome}</p>
                    </div>
                )}
            </div>
        )
    }

    // NEW FORMAT: Phases-based story (for multi-step scenarios)
    if (phases && phases.length > 0) {
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
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
                position: 'relative'
            }}>
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
                    color: '#ef4444',
                    fontWeight: 600,
                    padding: '6px 12px',
                    background: 'rgba(239, 68, 68, 0.1)',
                    border: '1px solid rgba(239, 68, 68, 0.2)',
                    borderRadius: '20px'
                }}>
                    HISTORIA
                </div>
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
                        <h3 style={{ fontSize: '1.5rem', color: '#DA291C', fontWeight: 700, margin: 0 }}>{title}</h3>
                    </div>
                </div>

                {situation && (
                    <div style={{
                        marginBottom: '24px',
                        padding: '20px',
                        background: 'rgba(255, 136, 0, 0.1)',
                        borderRadius: '12px',
                        borderLeft: '4px solid #ff8800'
                    }}>
                        <h4 style={{ color: '#ff8800', marginBottom: '10px', fontSize: '1.1rem' }}>Sytuacja:</h4>
                        <p style={{ margin: 0, lineHeight: 1.6, color: 'rgba(255, 255, 255, 0.9)' }}>{situation}</p>
                    </div>
                )}

                {phases.map((phase, idx) => (
                    <div key={idx} style={{ marginBottom: '24px' }}>
                        <div style={{
                            padding: '20px',
                            background: phase.type === 'demonstration' ? 'rgba(0, 255, 136, 0.1)' : 'rgba(0, 212, 255, 0.1)',
                            borderRadius: '12px',
                            borderLeft: `4px solid ${phase.type === 'demonstration' ? '#00ff88' : '#00d4ff'}`
                        }}>
                            <h4 style={{
                                color: phase.type === 'demonstration' ? '#00ff88' : '#00d4ff',
                                marginBottom: '16px',
                                fontSize: '1.2rem',
                                fontWeight: 700
                            }}>
                                {phase.title}
                            </h4>
                            {phase.dialogue ? (
                                phase.dialogue.map((line, i) => (
                                    <div key={i} style={{
                                        marginBottom: '12px',
                                        paddingLeft: '16px',
                                        borderLeft: '2px solid rgba(255, 255, 255, 0.2)'
                                    }}>
                                        <div style={{ fontWeight: 600, color: '#00d4ff', marginBottom: '4px' }}>{line.speaker}:</div>
                                        <div style={{ color: 'rgba(255, 255, 255, 0.9)', lineHeight: 1.6 }}>{line.text}</div>
                                    </div>
                                ))
                            ) : phase.content ? (
                                <div style={{ 
                                    color: 'rgba(255, 255, 255, 0.9)', 
                                    lineHeight: 1.7,
                                    marginTop: '12px'
                                }}>
                                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{phase.content}</ReactMarkdown>
                                </div>
                            ) : null}
                        </div>
                    </div>
                ))}

                {outcome && (
                    <div style={{
                        background: 'rgba(0, 255, 135, 0.1)',
                        border: '2px solid rgba(0, 255, 135, 0.3)',
                        borderRadius: '12px',
                        padding: '20px'
                    }}>
                        <h4 style={{ color: '#00ff87', marginBottom: '10px', fontSize: '1.1rem' }}>Efekt:</h4>
                        <p style={{ margin: 0, lineHeight: 1.6, color: 'rgba(255, 255, 255, 0.9)' }} dangerouslySetInnerHTML={{ __html: outcome.replace(/\*\*(.*?)\*\*/g, '<strong style="color: #00ff87">$1</strong>') }} />
                    </div>
                )}

                {typeof lesson === 'string' && (
                    <div style={{
                        marginTop: '16px',
                        background: 'rgba(176, 0, 255, 0.1)',
                        border: '2px solid rgba(176, 0, 255, 0.3)',
                        borderRadius: '12px',
                        padding: '20px'
                    }}>
                        <strong style={{ color: '#b000ff', fontSize: '1.1rem' }}>Kluczowa lekcja:</strong>
                        <p style={{ margin: '8px 0 0 0', lineHeight: 1.7, color: 'rgba(255, 255, 255, 0.9)' }}>{lesson}</p>
                    </div>
                )}
            </div>
        )
    }

    // OLD FORMAT (backwards compatible)
    if (!scenario) return null

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
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
            position: 'relative' // Ensure relative positioning
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
                color: '#ef4444',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(239, 68, 68, 0.1)',
                border: '1px solid rgba(239, 68, 68, 0.2)',
                borderRadius: '20px'
            }}>
                HISTORIA
            </div>
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
                        {typeof consequence === 'string' ? (
                            <>
                                <span style={{ fontSize: '1.3rem', flexShrink: 0 }}>➡️</span>
                                <span style={{
                                    fontSize: '1rem',
                                    lineHeight: 1.6,
                                    color: 'rgba(255, 255, 255, 0.9)'
                                }}>
                                    {consequence}
                                </span>
                            </>
                        ) : (
                            <div style={{ width: '100%' }}>
                                <div style={{
                                    fontSize: '1.1rem',
                                    fontWeight: 700,
                                    color: '#ff8888',
                                    marginBottom: '4px'
                                }}>
                                    {consequence.heading}
                                </div>
                                <div style={{
                                    fontSize: '1rem',
                                    lineHeight: 1.6,
                                    color: 'rgba(255, 255, 255, 0.9)'
                                }}>
                                    {consequence.text}
                                </div>
                            </div>
                        )}
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
                    {typeof lesson === 'object' ? lesson.heading : '💡 Wniosek'}
                </h4>
                <p style={{
                    fontSize: '1.1rem',
                    lineHeight: 1.8,
                    margin: 0,
                    color: 'rgba(255, 255, 255, 0.9)'
                }}
                    dangerouslySetInnerHTML={{ __html: (typeof lesson === 'string' ? lesson : lesson.text).replace(/\*\*(.*?)\*\*/g, '<strong style="color: #00ff87">$1</strong>') }}
                />
            </div>
        </div>
    )
}
