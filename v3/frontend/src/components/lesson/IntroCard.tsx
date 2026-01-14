'use client'

import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface IntroCardProps {
    title: string
    subtitle?: string
    description: string
    icon?: string
}

export default function IntroCard({ title, subtitle, description, icon = '🎯' }: IntroCardProps) {
    return (
        <div style={{
            maxWidth: '800px',
            width: '100%',
            textAlign: 'center',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '24px'
        }}>
            {/* Type Badge */}
            <div style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                fontSize: '11px',
                textTransform: 'uppercase',
                letterSpacing: '1px',
                color: '#b000ff',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(176, 0, 255, 0.1)',
                border: '1px solid rgba(176, 0, 255, 0.2)',
                borderRadius: '20px'
            }}>
                INTRO
            </div>

            {/* Icon */}
            <div style={{
                fontSize: '80px',
                marginBottom: '8px',
                animation: 'float 3s ease-in-out infinite'
            }}>
                {icon}
            </div>

            <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-10px); }
        }
      `}</style>

            {/* Title */}
            <h1 style={{
                fontSize: '36px',
                fontWeight: 700,
                lineHeight: '1.2',
                marginBottom: '8px'
            }}>
                {title}
            </h1>

            {/* Subtitle */}
            {subtitle && (
                <p style={{
                    fontSize: '18px',
                    color: '#00d4ff',
                    fontWeight: 600
                }}>
                    {subtitle}
                </p>
            )}

            {/* Description */}
            <div style={{
                fontSize: '16px',
                color: 'rgba(255, 255, 255, 0.7)',
                lineHeight: '1.7',
                maxWidth: '600px'
            }}>
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {description}
                </ReactMarkdown>
            </div>

            {/* Decorative gradient line */}
            <div style={{
                width: '200px',
                height: '3px',
                background: 'linear-gradient(90deg, transparent, #00d4ff, #b000ff, transparent)',
                borderRadius: '2px',
                marginTop: '16px'
            }} />
        </div>
    )
}
