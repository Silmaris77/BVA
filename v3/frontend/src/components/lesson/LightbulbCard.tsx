'use client'

import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Lightbulb } from 'lucide-react'

interface LightbulbCardProps {
    title: string
    content: string
    insight?: string
    accent_color?: string
    steps?: {
        number: number
        title: string
    }[]
}

export default function LightbulbCard({ title, content, insight, accent_color = 'yellow', steps }: LightbulbCardProps) {
    const accentColor = accent_color === 'yellow' ? '#ffd700' : '#00d4ff';
    const gradient = accent_color === 'yellow'
        ? 'linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 136, 0, 0.1))'
        : 'linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 100, 255, 0.1))';
    const borderColor = accent_color === 'yellow' ? 'rgba(255, 215, 0, 0.3)' : 'rgba(0, 212, 255, 0.3)';

    return (
        <div style={{
            maxWidth: '900px',
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
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
                color: accentColor,
                fontWeight: 600,
                padding: '6px 12px',
                background: `rgba(${accent_color === 'yellow' ? '255, 215, 0' : '0, 212, 255'}, 0.1)`,
                border: `1px solid ${borderColor}`,
                borderRadius: '20px',
                width: 'fit-content'
            }}>
                INSIGHT
            </div>

            <div style={{
                background: gradient,
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: `2px solid ${borderColor}`,
                borderRadius: '24px',
                padding: '60px 40px',
                textAlign: 'center',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.2)'
            }}>
                <div style={{
                    display: 'flex',
                    justifyContent: 'center',
                    marginBottom: '24px'
                }}>
                    <div style={{
                        padding: '20px',
                        background: 'rgba(255, 255, 255, 0.1)',
                        borderRadius: '50%',
                        color: accentColor
                    }}>
                        <Lightbulb size={60} strokeWidth={1.5} />
                    </div>
                </div>

                <h2 style={{
                    fontSize: '24px',
                    fontWeight: 300,
                    marginBottom: '24px',
                    color: 'rgba(255, 255, 255, 0.8)'
                }}>
                    {title}
                </h2>

                <div style={{
                    fontSize: '28px',
                    fontWeight: 700,
                    marginBottom: '40px',
                    color: '#fff',
                    maxWidth: '800px',
                    margin: '0 auto 40px auto'
                }}>
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {content}
                    </ReactMarkdown>
                </div>

                {/* Steps */}
                {steps && steps.length > 0 && (
                    <div style={{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '16px',
                        marginBottom: '40px',
                        maxWidth: '700px',
                        margin: '0 auto 40px auto'
                    }}>
                        {steps.map((step) => (
                            <div
                                key={step.number}
                                style={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '16px',
                                    padding: '16px 24px',
                                    background: 'rgba(0, 0, 0, 0.2)',
                                    borderRadius: '12px',
                                    textAlign: 'left'
                                }}
                            >
                                <div style={{
                                    width: '40px',
                                    height: '40px',
                                    borderRadius: '50%',
                                    background: accentColor,
                                    color: '#000',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    fontSize: '20px',
                                    fontWeight: 700,
                                    flexShrink: 0
                                }}>
                                    {step.number}
                                </div>
                                <div style={{
                                    fontSize: '18px',
                                    fontWeight: 600,
                                    color: '#fff'
                                }}>
                                    {step.title}
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {insight && (
                    <div style={{
                        background: 'rgba(0, 0, 0, 0.2)',
                        borderLeft: `4px solid ${accentColor}`,
                        padding: '24px 32px',
                        borderRadius: '12px',
                        maxWidth: '700px',
                        margin: '0 auto',
                        textAlign: 'left'
                    }}>
                        <strong style={{
                            color: accentColor,
                            display: 'block',
                            marginBottom: '8px',
                            fontSize: '14px',
                            textTransform: 'uppercase',
                            letterSpacing: '1px'
                        }}>
                            KLUCZOWY WNIOSEK
                        </strong>
                        <div style={{
                            fontSize: '18px',
                            lineHeight: '1.6',
                            color: 'rgba(255, 255, 255, 0.9)'
                        }}>
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                {insight}
                            </ReactMarkdown>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
