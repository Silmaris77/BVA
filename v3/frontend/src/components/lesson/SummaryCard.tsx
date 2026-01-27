'use client'

import MathRenderer from './math/MathRenderer'
import { Trophy, CheckCircle2, Sparkles } from 'lucide-react'
import { useEffect, useState } from 'react'
import confetti from 'canvas-confetti'

interface SummaryCardProps {
    title?: string
    recap: string[]
    nextSteps?: string
    badge?: {
        xp: number
        title: string
    }
}

export default function SummaryCard({
    title = 'Gratulacje!',
    recap,
    nextSteps,
    badge
}: SummaryCardProps) {
    const [xpCount, setXpCount] = useState(0)
    const targetXP = badge?.xp || 0

    // Animated XP counter
    useEffect(() => {
        if (!badge) return

        const duration = 1500
        const steps = 30
        const increment = targetXP / steps
        const stepDuration = duration / steps

        let current = 0
        const interval = setInterval(() => {
            current += increment
            if (current >= targetXP) {
                setXpCount(targetXP)
                clearInterval(interval)
            } else {
                setXpCount(Math.floor(current))
            }
        }, stepDuration)

        return () => clearInterval(interval)
    }, [targetXP, badge])

    // Confetti celebration
    useEffect(() => {
        // Initial burst
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 }
        })

        // Second burst from left
        setTimeout(() => {
            confetti({
                particleCount: 50,
                angle: 60,
                spread: 55,
                origin: { x: 0 }
            })
        }, 250)

        // Third burst from right
        setTimeout(() => {
            confetti({
                particleCount: 50,
                angle: 120,
                spread: 55,
                origin: { x: 1 }
            })
        }, 400)
    }, [])

    return (
        <div style={{
            maxWidth: '800px',
            width: '100%',
            position: 'relative',
            background: 'rgba(20, 20, 35, 0.6)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 215, 0, 0.2)', // Gold
            borderRadius: '20px',
            padding: '24px',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
            borderLeft: '4px solid #ffd700',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '16px',
            textAlign: 'center'
        }}>
            {/* Badge */}
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
                color: '#ffd700',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(255, 215, 0, 0.1)',
                border: '1px solid rgba(255, 215, 0, 0.2)',
                borderRadius: '20px'
            }}>
                PODSUMOWANIE
            </div>

            {/* Success Icon */}
            <div style={{
                width: '80px',
                height: '80px',
                borderRadius: '50%',
                background: 'linear-gradient(135deg, #00ff88, #00d4ff)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 0 40px rgba(0, 255, 136, 0.4)',
                animation: 'pulse 2s ease-in-out infinite',
                marginTop: '10px'
            }}>
                <style>{`
          @keyframes pulse {
            0%, 100% { transform: scale(1); box-shadow: 0 0 40px rgba(0, 255, 136, 0.4); }
            50% { transform: scale(1.05); box-shadow: 0 0 60px rgba(0, 255, 136, 0.6); }
          }
          @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
          }
          @keyframes fadeInUp {
            from {
              opacity: 0;
              transform: translateY(20px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
        `}</style>
                <Trophy size={40} style={{ color: '#000' }} />
            </div>

            {/* Title */}
            <h1 style={{
                fontSize: '28px',
                fontWeight: 700,
                background: 'linear-gradient(135deg, #00ff88, #00d4ff)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                animation: 'fadeInUp 0.6s ease 0.2s both'
            }}>
                {title}
            </h1>

            {/* XP Badge */}
            {badge && (
                <div style={{
                    background: 'linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 140, 0, 0.2))',
                    backdropFilter: 'blur(20px)',
                    border: '2px solid #ffd700',
                    borderRadius: '20px',
                    padding: '16px 32px',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '4px',
                    boxShadow: '0 0 30px rgba(255, 215, 0, 0.3)',
                    animation: 'fadeInUp 0.6s ease 0.4s both'
                }}>
                    <Sparkles size={24} style={{ color: '#ffd700' }} />
                    <div style={{
                        fontSize: '40px',
                        fontWeight: 800,
                        color: '#ffd700',
                        lineHeight: '1'
                    }}>
                        +{xpCount} XP
                    </div>
                    {badge.title && (
                        <div style={{
                            fontSize: '14px',
                            fontWeight: 600,
                            color: 'rgba(255, 215, 0, 0.8)'
                        }}>
                            {badge.title}
                        </div>
                    )}
                </div>
            )}

            {/* Recap */}
            <div style={{
                background: 'rgba(255, 255, 255, 0.03)',
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '20px',
                padding: '20px',
                width: '100%',
                animation: 'fadeInUp 0.6s ease 0.6s both'
            }}>
                <h3 style={{
                    fontSize: '18px',
                    fontWeight: 600,
                    marginBottom: '12px',
                    color: '#00d4ff',
                    textAlign: 'left'
                }}>
                    Czego się nauczyłeś:
                </h3>
                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '10px',
                    textAlign: 'left'
                }}>
                    {recap?.map((item, index) => (
                        <div
                            key={index}
                            style={{
                                display: 'flex',
                                alignItems: 'flex-start',
                                gap: '12px',
                                animation: `fadeInUp 0.4s ease ${0.8 + index * 0.1}s both`
                            }}
                        >
                            <CheckCircle2
                                size={20}
                                style={{
                                    color: '#00ff88',
                                    flexShrink: 0,
                                    marginTop: '2px'
                                }}
                            />
                            <span style={{
                                fontSize: '16px',
                                lineHeight: '1.6',
                                color: 'rgba(255, 255, 255, 0.9)'
                            }}>
                                <MathRenderer content={item} inline={true} />
                            </span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Next Steps */}
            {nextSteps && (
                <div style={{
                    padding: '20px 24px',
                    background: 'rgba(0, 212, 255, 0.1)',
                    border: '1px solid rgba(0, 212, 255, 0.3)',
                    borderRadius: '16px',
                    fontSize: '15px',
                    lineHeight: '1.6',
                    color: 'rgba(255, 255, 255, 0.8)',
                    animation: 'fadeInUp 0.6s ease 1.2s both',
                    width: '100%',
                    textAlign: 'left'
                }}>
                    💡 <strong>Dalsze kroki:</strong> {nextSteps}
                </div>
            )}
        </div>
    )
}
