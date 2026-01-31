'use client'

import MathRenderer from './math/MathRenderer'

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
            position: 'relative',
            background: 'rgba(20, 20, 35, 0.6)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            border: '1px solid rgba(176, 0, 255, 0.2)', // Purple
            borderRadius: '20px',
            padding: '40px',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
            borderLeft: '4px solid #b000ff',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '24px'
        }}>
            {/* Type Badge */}
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
                marginTop: '16px',
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
                marginBottom: '8px',
                textAlign: 'center'
            }}>
                {title}
            </h1>

            {/* Subtitle */}
            {subtitle && (
                <p style={{
                    fontSize: '18px',
                    color: '#00d4ff',
                    fontWeight: 600,
                    textAlign: 'center'
                }}>
                    {subtitle}
                </p>
            )}

            {/* Description */}
            <div style={{
                fontSize: '16px',
                color: 'rgba(255, 255, 255, 0.7)',
                lineHeight: '1.7',
                maxWidth: '600px',
                textAlign: 'center'
            }}>
                <MathRenderer content={description} />
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
