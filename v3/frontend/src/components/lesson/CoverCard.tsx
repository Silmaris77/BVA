'use client'

import { Clock, Trophy, Play, BookOpen } from 'lucide-react'

interface CoverCardProps {
    title: string
    subtitle?: string
    description?: string
    category?: string
    durationMinutes?: number
    xpReward?: number
    image?: string
    onStart?: () => void
}

export default function CoverCard({
    title,
    subtitle,
    description,
    category = 'Moduł Edukacyjny',
    durationMinutes,
    xpReward,
    image,
    onStart
}: CoverCardProps) {

    // Logic to determine image: Prop > Title Match > Category Fallback
    const getFallbackImage = () => {
        // 1. Explicit Prop (Highest Priority)
        if (image) return image

        const t = title.toLowerCase()
        const c = category ? category.toLowerCase() : ''

        // 2. SPECIFIC TITLE OVERRIDES
        if (t.includes('historia') && t.includes('milwaukee')) {
            return '/lessons/milwaukee/history/oldtimesnewtimes.png'
        }

        if (t.includes('ojt') || t.includes('on the job') || t.includes('on-the-job')) {
            return '/lessons/ojt/cover.png'
        }

        if (t.includes('fundamenty') || t.includes('historia') || t.includes('dna')) {
            // User Choice: Specific Unsplash Image
            return 'https://images.unsplash.com/photo-1649908787172-7945c00fafa2?auto=format&fit=crop&w=1600&q=80'
        }

        // 3. Category Fallbacks
        if (t.includes('sprzedaż') || c.includes('sprzedaż') || t.includes('wizyta')) {
            // Dark Meeting Handshake
            return 'https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=1600&q=80'
        }
        if (t.includes('współpraca') || c.includes('współpraca')) {
            // Teamwork dark
            return 'https://images.unsplash.com/photo-1600880292203-757bb62b4baf?auto=format&fit=crop&w=1600&q=80'
        }
        if (t.includes('aplikacja') || t.includes('krok')) {
            // Construction / Engineering dark
            return 'https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1600&q=80'
        }

        // 4. Default Abstract
        return 'https://images.unsplash.com/photo-1614850523060-8da1d56ae167?auto=format&fit=crop&w=1600&q=80'
    }

    const bgImage = getFallbackImage()

    return (
        <div style={{
            maxWidth: '1000px',
            width: '100%',
            aspectRatio: '16/9',
            minHeight: '600px',
            display: 'flex',
            borderRadius: '24px',
            overflow: 'hidden',
            boxShadow: '0 30px 60px rgba(0,0,0,0.5)',
            border: '1px solid rgba(255,255,255,0.1)',
            position: 'relative',
            backgroundColor: '#0f0f13' // Base color
        }}>


            {/* Background Layer - Switched to IMG tag for stability */}
            <div style={{
                position: 'absolute',
                inset: 0,
            }}>
                <img
                    src={bgImage || ""}
                    alt="Background"
                    style={{
                        width: '100%',
                        height: '100%',
                        objectFit: 'cover',
                        opacity: 0.6 // Visible but allows text contrast
                    }}
                />
                {/* Lighter Gradient Overlay - Reduced Opacity */}
                <div style={{
                    position: 'absolute',
                    inset: 0,
                    background: 'linear-gradient(90deg, #0f0f13 0%, rgba(15,15,19,0.5) 50%, rgba(15,15,19,0) 100%)'
                }} />
            </div>
            {/* Content Layout */}
            <div style={{
                zIndex: 2,
                flex: 1,
                padding: '60px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                position: 'relative'
            }}>

                {/* Top Badge */}
                <div style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '8px 16px',
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '100px',
                    width: 'fit-content',
                    marginBottom: '32px',
                    backdropFilter: 'blur(10px)'
                }}>
                    <BookOpen size={14} color="#DA291C" />
                    <span style={{
                        fontSize: '12px',
                        fontWeight: 600,
                        letterSpacing: '1px',
                        textTransform: 'uppercase',
                        color: 'rgba(255,255,255,0.8)'
                    }}>
                        {category}
                    </span>
                </div>

                {/* Main Title */}
                <h1 style={{
                    fontSize: '3rem',
                    fontWeight: 800,
                    lineHeight: 1.1,
                    marginBottom: '16px',
                    background: 'linear-gradient(90deg, #FFFFFF 0%, #E0E0E0 100%)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    maxWidth: '800px'
                }}>
                    {title}
                </h1>

                {/* Subtitle / Description */}
                <p style={{
                    fontSize: '1.25rem',
                    lineHeight: 1.6,
                    color: 'rgba(255,255,255,0.7)',
                    maxWidth: '600px',
                    marginBottom: '48px',
                    fontWeight: 300
                }}>
                    {description || subtitle}
                </p>

                {/* Metadata Row */}
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '32px',
                    paddingTop: '32px',
                    borderTop: '1px solid rgba(255,255,255,0.08)'
                }}>
                    {durationMinutes && (
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                            <div style={{
                                width: '40px',
                                height: '40px',
                                borderRadius: '10px',
                                background: 'rgba(255,255,255,0.05)',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                color: '#00d4ff'
                            }}>
                                <Clock size={20} />
                            </div>
                            <div>
                                <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.5)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Czas</div>
                                <div style={{ fontWeight: 600, fontSize: '16px' }}>{durationMinutes} min</div>
                            </div>
                        </div>
                    )}

                    {xpReward && (
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                            <div style={{
                                width: '40px',
                                height: '40px',
                                borderRadius: '10px',
                                background: 'rgba(255,255,255,0.05)',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                color: '#ffd700'
                            }}>
                                <Trophy size={20} />
                            </div>
                            <div>
                                <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.5)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Nagroda</div>
                                <div style={{ fontWeight: 600, fontSize: '16px' }}>+{xpReward} XP</div>
                            </div>
                        </div>
                    )}

                    {/* Start Prompt (Visual only, as the whole card usually flows to next) */}
                    <div
                        onClick={onStart}
                        role="button"
                        tabIndex={0}
                        style={{
                            marginLeft: 'auto',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '12px',
                            color: 'rgba(255,255,255,0.8)', // Increased visibility
                            cursor: 'pointer', // Interactive cursor
                            pointerEvents: 'auto'
                        }}
                    >
                        <span style={{ fontSize: '14px', letterSpacing: '1px', textTransform: 'uppercase' }}>Rozpocznij</span>
                        <div style={{
                            width: '48px',
                            height: '48px',
                            borderRadius: '50%',
                            background: '#DA291C',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            boxShadow: '0 0 20px rgba(218, 41, 28, 0.4)',
                            animation: 'pulse 2s infinite',
                            transition: 'transform 0.2s'
                        }}
                            onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
                            onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
                        >
                            <Play fill="white" size={20} style={{ marginLeft: '2px' }} />
                        </div>
                    </div>
                </div>

            </div>

            <style jsx>{`
                @keyframes pulse {
                    0% { box-shadow: 0 0 0 0 rgba(218, 41, 28, 0.4); transform: scale(1); }
                    70% { box-shadow: 0 0 0 10px rgba(218, 41, 28, 0); transform: scale(1.05); }
                    100% { box-shadow: 0 0 0 0 rgba(218, 41, 28, 0); transform: scale(1); }
                }
             `}</style>
        </div>
    )
}
