'use client'

import { Rocket, Sparkles, Zap, Trophy, Heart } from 'lucide-react'

interface HeroCardProps {
    title: string
    subtitle?: string
    tagline?: string
    content?: string
    icon?: string
    theme?: string
    sections?: {
        title: string
        content?: string
        items?: string[]
    }[]
    callout?: {
        type: 'critical' | 'warning' | 'info'
        text: string
    }
}

const getIcon = (iconName: string) => {
    // If it's an emoji, return it directly
    if (iconName && iconName.length <= 2) {
        return <div style={{ fontSize: '5rem' }}>{iconName}</div>
    }

    switch (iconName) {
        case 'rocket': return <Rocket size={64} strokeWidth={1.5} />
        case 'sparkles': return <Sparkles size={64} strokeWidth={1.5} />
        case 'zap': return <Zap size={64} strokeWidth={1.5} />
        case 'trophy': return <Trophy size={64} strokeWidth={1.5} />
        case 'heart': return <Heart size={64} strokeWidth={1.5} />
        default: return <Rocket size={64} strokeWidth={1.5} />
    }
}

export default function HeroCard({ title, subtitle, tagline, content, icon = 'rocket', theme = 'default', sections, callout }: HeroCardProps) {
    const isSafetyTheme = theme === 'safety'

    return (
        <div style={{
            maxWidth: '900px',
            width: '100%'
        }}>
            <div style={{
                background: isSafetyTheme
                    ? 'linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(218, 41, 28, 0.15))'
                    : 'rgba(20, 20, 35, 0.7)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: isSafetyTheme
                    ? '2px solid rgba(239, 68, 68, 0.4)'
                    : '1px solid rgba(255, 255, 255, 0.08)',
                borderTop: isSafetyTheme ? '6px solid #DA291C' : '4px solid #DA291C',
                borderRadius: '24px',
                padding: '50px',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
                position: 'relative',
                overflow: 'hidden'
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
                    color: '#DA291C',
                    fontWeight: 600,
                    padding: '6px 12px',
                    background: 'rgba(218, 41, 28, 0.1)',
                    border: '1px solid rgba(218, 41, 28, 0.2)',
                    borderRadius: '20px',
                    zIndex: 10
                }}>
                    WSTĘP
                </div>
                {/* Badge */}
                {subtitle && (
                    <div style={{
                        display: 'inline-block',
                        background: 'rgba(218, 41, 28, 0.3)',
                        border: '1px solid #DA291C',
                        padding: '8px 20px',
                        borderRadius: '20px',
                        fontSize: '0.9rem',
                        fontWeight: 600,
                        color: '#DA291C',
                        marginBottom: '20px',
                        textTransform: 'uppercase',
                        letterSpacing: '1px'
                    }}>
                        {subtitle}
                    </div>
                )}

                {/* Icon */}
                <div style={{
                    textAlign: 'center',
                    marginBottom: '30px',
                    color: '#DA291C',
                    animation: 'pulse-warning 2s ease-in-out infinite'
                }}>
                    {getIcon(icon)}
                    <style jsx>{`
                        @keyframes pulse-warning {
                            0%, 100% { transform: scale(1); filter: drop-shadow(0 0 10px rgba(239, 68, 68, 0.5)); }
                            50% { transform: scale(1.05); filter: drop-shadow(0 0 20px rgba(239, 68, 68, 0.8)); }
                        }
                    `}</style>
                </div>

                {/* Title */}
                <h1 style={{
                    fontSize: '3rem',
                    fontWeight: 800,
                    background: 'linear-gradient(135deg, #DA291C, #ef4444)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text',
                    marginBottom: '20px',
                    textAlign: 'center'
                }}>
                    {title}
                </h1>

                {/* Tagline */}
                {tagline && (
                    <div style={{
                        textAlign: 'center',
                        fontSize: '1.3rem',
                        fontWeight: 700,
                        color: '#DA291C',
                        textTransform: 'uppercase',
                        letterSpacing: '2px',
                        marginBottom: '40px'
                    }}>
                        {tagline}
                    </div>
                )}

                {/* Sections Grid */}
                {sections && sections.length > 0 && (
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: sections.length > 1 ? 'repeat(2, 1fr)' : '1fr',
                        gap: '30px',
                        margin: '40px 0'
                    }}>
                        {sections.map((section, index) => (
                            <div
                                key={index}
                                style={{
                                    background: 'rgba(0, 0, 0, 0.3)',
                                    borderRadius: '16px',
                                    padding: '25px',
                                    border: '1px solid rgba(255, 255, 255, 0.1)'
                                }}
                            >
                                <h4 style={{
                                    fontSize: '1.2rem',
                                    color: '#DA291C',
                                    marginBottom: '15px',
                                    fontWeight: 700
                                }}>
                                    {section.title}
                                </h4>
                                {section.content && (
                                    <p style={{
                                        marginBottom: '15px',
                                        fontSize: '1rem',
                                        opacity: 0.9,
                                        lineHeight: 1.6
                                    }}>
                                        {section.content}
                                    </p>
                                )}
                                {section.items && (
                                    <ul style={{ listStyle: 'none', padding: 0 }}>
                                        {section.items.map((item, i) => (
                                            <li
                                                key={i}
                                                style={{
                                                    padding: '8px 0',
                                                    paddingLeft: '25px',
                                                    position: 'relative',
                                                    lineHeight: 1.6
                                                }}
                                            >
                                                <span style={{
                                                    position: 'absolute',
                                                    left: 0,
                                                    color: '#00ff87'
                                                }}>✔</span>
                                                <span dangerouslySetInnerHTML={{ __html: item.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }} />
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </div>
                        ))}
                    </div>
                )}

                {/* Simple content fallback */}
                {content && !sections && (
                    <div style={{
                        fontSize: '1.1rem',
                        lineHeight: 1.8,
                        marginBottom: '30px',
                        color: 'rgba(255, 255, 255, 0.9)',
                        textAlign: 'center'
                    }}>
                        {content}
                    </div>
                )}

                {/* Callout */}
                {callout && (
                    <div style={{
                        background: 'rgba(239, 68, 68, 0.2)',
                        border: '2px solid #ef4444',
                        borderRadius: '12px',
                        padding: '25px',
                        marginTop: '30px',
                        fontSize: '1.3rem',
                        lineHeight: 1.8,
                        fontStyle: 'italic',
                        textAlign: 'center'
                    }}
                        dangerouslySetInnerHTML={{ __html: callout.text.replace(/„/g, '"').replace(/"/g, '"') }}
                    />
                )}
            </div>
        </div>
    )
}
