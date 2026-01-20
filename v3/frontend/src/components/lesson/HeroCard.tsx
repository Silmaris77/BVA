'use client'

import { LucideIcon, Rocket, Sparkles, Zap, Trophy, Heart } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface HeroCardProps {
    title: string
    subtitle?: string
    content: string
    icon?: string
}

const getIcon = (iconName: string) => {
    switch (iconName) {
        case 'rocket': return <Rocket size={64} strokeWidth={1.5} />
        case 'sparkles': return <Sparkles size={64} strokeWidth={1.5} />
        case 'zap': return <Zap size={64} strokeWidth={1.5} />
        case 'trophy': return <Trophy size={64} strokeWidth={1.5} />
        case 'heart': return <Heart size={64} strokeWidth={1.5} />
        default: return <Rocket size={64} strokeWidth={1.5} />
    }
}

export default function HeroCard({ title, subtitle, content, icon = 'rocket' }: HeroCardProps) {
    return (
        <div style={{
            maxWidth: '800px',
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            gap: '24px'
        }}>
            {/* Card Container - Emotional Variant */}
            <div style={{
                background: 'rgba(20, 20, 35, 0.7)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                borderTop: '4px solid #DA291C', // Milwaukee Red Top Border
                borderRight: '1px solid rgba(255, 255, 255, 0.08)',
                borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
                borderLeft: '1px solid rgba(255, 255, 255, 0.08)',
                borderRadius: '24px',
                padding: '50px',
                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
                position: 'relative',
                overflow: 'hidden',
                textAlign: 'center'
            }}>
                {/* HERO TAG */}
                <div style={{
                    position: 'absolute',
                    top: '20px',
                    right: '20px',
                    background: 'rgba(218, 41, 28, 0.2)',
                    border: '1px solid rgba(218, 41, 28, 0.4)',
                    padding: '6px 14px',
                    borderRadius: '8px',
                    fontSize: '12px',
                    fontWeight: 700,
                    textTransform: 'uppercase',
                    letterSpacing: '1px',
                    color: '#ff6b6b'
                }}>
                    WSTĘP
                </div>

                {/* Animated Icon */}
                <div style={{
                    marginBottom: '25px',
                    color: '#DA291C',
                    display: 'flex',
                    justifyContent: 'center'
                }}>
                    <div style={{
                        animation: 'pulse-glow 2s ease-in-out infinite'
                    }}>
                        {getIcon(icon)}
                        <style jsx>{`
                            @keyframes pulse-glow {
                                0%, 100% { 
                                    transform: scale(1);
                                    filter: drop-shadow(0 0 10px rgba(218, 41, 28, 0.5));
                                }
                                50% { 
                                    transform: scale(1.1);
                                    filter: drop-shadow(0 0 20px rgba(218, 41, 28, 0.8));
                                }
                            }
                        `}</style>
                    </div>
                </div>

                {/* Typography */}
                <h1 style={{
                    fontSize: '2.5rem',
                    fontWeight: 800,
                    marginBottom: '15px',
                    lineHeight: '1.2',
                    background: 'linear-gradient(135deg, #DA291C, #ff6b6b)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text'
                }}>
                    {title}
                </h1>

                {subtitle && (
                    <div style={{
                        fontSize: '1.1rem',
                        fontWeight: 600,
                        opacity: 0.9,
                        marginBottom: '30px',
                        color: '#60efff'
                    }}>
                        {subtitle}
                    </div>
                )}

                <div style={{
                    fontSize: '1.1rem',
                    lineHeight: '1.8',
                    marginBottom: '30px',
                    color: 'rgba(255, 255, 255, 0.9)'
                }}>
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {content}
                    </ReactMarkdown>
                </div>

            </div>
        </div>
    )
}
