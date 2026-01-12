'use client'

import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { CheckCircle2 } from 'lucide-react'

interface ConceptCardProps {
    title: string
    content: string
    keyPoints?: string[]
    visual?: {
        type: 'image' | 'diagram'
        src: string
    }
}

export default function ConceptCard({ title, content, keyPoints, visual }: ConceptCardProps) {
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
                color: '#00d4ff',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(0, 212, 255, 0.1)',
                border: '1px solid rgba(0, 212, 255, 0.2)',
                borderRadius: '20px',
                width: 'fit-content'
            }}>
                CONCEPT
            </div>

            {/* Glass Card Container */}
            <div style={{
                background: 'rgba(20, 20, 35, 0.6)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '20px',
                padding: '40px',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)'
            }}>
                {/* Title */}
                <h2 style={{
                    fontSize: '28px',
                    fontWeight: 700,
                    marginBottom: '24px',
                    background: 'linear-gradient(135deg, #00d4ff, #b000ff)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent'
                }}>
                    {title}
                </h2>

                {/* Content */}
                <div style={{
                    fontSize: '16px',
                    lineHeight: '1.8',
                    color: 'rgba(255, 255, 255, 0.9)',
                    marginBottom: visual ? '32px' : '0'
                }}>
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {content}
                    </ReactMarkdown>
                </div>

                {/* Visual (if provided) */}
                {visual && (
                    <div style={{
                        marginTop: '32px',
                        borderRadius: '12px',
                        overflow: 'hidden',
                        border: '1px solid rgba(255, 255, 255, 0.1)'
                    }}>
                        <img
                            src={visual.src}
                            alt="Concept visual"
                            style={{
                                width: '100%',
                                height: 'auto',
                                display: 'block'
                            }}
                        />
                    </div>
                )}
            </div>

            {/* Key Points */}
            {keyPoints && keyPoints.length > 0 && (
                <div style={{
                    background: 'rgba(0, 212, 255, 0.1)',
                    backdropFilter: 'blur(20px)',
                    WebkitBackdropFilter: 'blur(20px)',
                    border: '1px solid rgba(0, 212, 255, 0.3)',
                    borderRadius: '16px',
                    padding: '24px'
                }}>
                    <h3 style={{
                        fontSize: '18px',
                        fontWeight: 600,
                        marginBottom: '16px',
                        color: '#00d4ff'
                    }}>
                        Kluczowe punkty:
                    </h3>
                    <div style={{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '12px'
                    }}>
                        {keyPoints.map((point, index) => (
                            <div
                                key={index}
                                style={{
                                    display: 'flex',
                                    alignItems: 'flex-start',
                                    gap: '12px'
                                }}
                            >
                                <CheckCircle2
                                    size={20}
                                    style={{
                                        color: '#00d4ff',
                                        flexShrink: 0,
                                        marginTop: '2px'
                                    }}
                                />
                                <span style={{
                                    fontSize: '15px',
                                    lineHeight: '1.6',
                                    color: 'rgba(255, 255, 255, 0.9)'
                                }}>
                                    {point}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    )
}
