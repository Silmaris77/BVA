'use client'

import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface PracticeCardProps {
    title: string
    content: string
    keyPoints?: string[]
    actionSteps?: string[]
}

export default function PracticeCard({ title, content, keyPoints, actionSteps }: PracticeCardProps) {
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
                color: '#00ff88',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(0, 255, 136, 0.1)',
                border: '1px solid rgba(0, 255, 136, 0.2)',
                borderRadius: '20px',
                width: 'fit-content'
            }}>
                PRACTICE
            </div>

            {/* Main Content Card */}
            <div style={{
                background: 'rgba(20, 20, 35, 0.6)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(0, 255, 136, 0.2)',
                borderRadius: '20px',
                padding: '40px',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
                borderLeft: '4px solid #00ff88'
            }}>
                {/* Title */}
                <h2 style={{
                    fontSize: '28px',
                    fontWeight: 700,
                    marginBottom: '24px',
                    color: '#00ff88'
                }}>
                    {title}
                </h2>

                {/* Content */}
                <div style={{
                    fontSize: '16px',
                    lineHeight: '1.8',
                    color: 'rgba(255, 255, 255, 0.9)',
                    marginBottom: keyPoints || actionSteps ? '24px' : '0'
                }}>
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {content}
                    </ReactMarkdown>
                </div>

                {/* Key Points */}
                {keyPoints && keyPoints.length > 0 && (
                    <div style={{
                        marginTop: '24px',
                        padding: '20px',
                        background: 'rgba(0, 255, 136, 0.05)',
                        borderRadius: '12px',
                        border: '1px solid rgba(0, 255, 136, 0.1)'
                    }}>
                        <h4 style={{
                            fontSize: '14px',
                            fontWeight: 600,
                            marginBottom: '12px',
                            color: '#00ff88',
                            textTransform: 'uppercase',
                            letterSpacing: '0.5px'
                        }}>
                            💡 Kluczowe praktyki:
                        </h4>
                        <ul style={{
                            listStyle: 'none',
                            padding: 0,
                            margin: 0,
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '8px'
                        }}>
                            {keyPoints.map((point, index) => (
                                <li key={index} style={{
                                    display: 'flex',
                                    alignItems: 'flex-start',
                                    gap: '12px',
                                    fontSize: '15px',
                                    lineHeight: '1.6'
                                }}>
                                    <span style={{ color: '#00ff88', fontSize: '18px' }}>✓</span>
                                    <span>{point}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}

                {/* Action Steps */}
                {actionSteps && actionSteps.length > 0 && (
                    <div style={{
                        marginTop: '24px',
                        padding: '20px',
                        background: 'rgba(0, 212, 255, 0.05)',
                        borderRadius: '12px',
                        border: '1px solid rgba(0, 212, 255, 0.15)'
                    }}>
                        <h4 style={{
                            fontSize: '14px',
                            fontWeight: 600,
                            marginBottom: '12px',
                            color: '#00d4ff',
                            textTransform: 'uppercase',
                            letterSpacing: '0.5px'
                        }}>
                            🎯 Do zrobienia:
                        </h4>
                        <ol style={{
                            paddingLeft: '24px',
                            margin: 0,
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '8px'
                        }}>
                            {actionSteps.map((step, index) => (
                                <li key={index} style={{
                                    fontSize: '15px',
                                    lineHeight: '1.6',
                                    color: 'rgba(255, 255, 255, 0.9)'
                                }}>
                                    {step}
                                </li>
                            ))}
                        </ol>
                    </div>
                )}
            </div>
        </div>
    )
}
