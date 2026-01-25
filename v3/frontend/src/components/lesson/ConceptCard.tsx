'use client'

import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import 'katex/dist/katex.min.css'
import { CheckCircle2, Lightbulb, AlertTriangle } from 'lucide-react'

interface ConceptCardProps {
    title: string
    content?: string
    keyPoints?: string[]
    visual?: {
        type: 'image' | 'diagram'
        src: string
    }
    sections?: {
        title?: string
        heading?: string  // backward compatibility
        content?: string
        items?: string[]
    }[]
    callout?: {
        type: 'critical' | 'warning' | 'info'
        text: string
    }
    remember?: {
        title?: string
        items?: string[]
        // backward compatibility
        icon?: string
        text?: string
    }
}

export default function ConceptCard({
    title,
    content,
    keyPoints,
    visual,
    sections,
    callout,
    remember
}: ConceptCardProps) {
    return (
        <div style={{
            maxWidth: '900px',
            width: '100%'
        }}>
            {/* Glass Card Container */}
            <div style={{
                position: 'relative',
                background: 'rgba(20, 20, 35, 0.6)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '20px',
                padding: '40px',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)'
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
                    color: '#00d4ff',
                    fontWeight: 600,
                    padding: '6px 12px',
                    background: 'rgba(0, 212, 255, 0.1)',
                    border: '1px solid rgba(0, 212, 255, 0.2)',
                    borderRadius: '20px'
                }}>
                    CONCEPT
                </div>

                {/* Title */}
                <h2 style={{
                    fontSize: '28px',
                    fontWeight: 700,
                    marginBottom: '24px',
                    marginTop: '20px',
                    background: 'linear-gradient(135deg, #00d4ff, #b000ff)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent'
                }}>
                    {title}
                </h2>

                {/* Simple Content (fallback) */}
                {content && !sections && (
                    <div style={{
                        fontSize: '16px',
                        lineHeight: '1.8',
                        color: 'rgba(255, 255, 255, 0.9)',
                        marginBottom: visual ? '32px' : '0'
                    }}>
                        <ReactMarkdown 
                            remarkPlugins={[remarkGfm, remarkMath]}
                            rehypePlugins={[rehypeKatex]}
                        >
                            {content.replace(/\\n/g, '\n')}
                        </ReactMarkdown>
                    </div>
                )}

                {/* Sections */}
                {sections && sections.length > 0 && (
                    <div style={{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '30px',
                        marginBottom: '30px'
                    }}>
                        {sections.map((section, index) => (
                            <div key={index}>
                                <h3 style={{
                                    fontSize: '1.3rem',
                                    color: '#00d4ff',
                                    marginBottom: '15px',
                                    fontWeight: 700
                                }}>
                                    {section.title || section.heading}
                                </h3>
                                {section.content && (
                                    <p style={{
                                        marginBottom: '15px',
                                        fontSize: '1rem',
                                        opacity: 0.9,
                                        lineHeight: 1.8
                                    }}>
                                        {section.content}
                                    </p>
                                )}
                                {section.items && (
                                    <ul style={{
                                        listStyle: 'none',
                                        padding: 0,
                                        display: 'flex',
                                        flexDirection: 'column',
                                        gap: '10px'
                                    }}>
                                        {section.items.map((item, i) => (
                                            <li
                                                key={i}
                                                style={{
                                                    padding: '12px 0',
                                                    paddingLeft: '30px',
                                                    position: 'relative',
                                                    lineHeight: 1.7,
                                                    fontSize: '1rem'
                                                }}
                                            >
                                                <span style={{
                                                    position: 'absolute',
                                                    left: 0,
                                                    color: '#00ff87',
                                                    fontSize: '1.2rem'
                                                }}>✔</span>
                                                <span dangerouslySetInnerHTML={{
                                                    __html: item.replace(/\*\*(.*?)\*\*/g, '<strong style="color: #00d4ff;">$1</strong>')
                                                }} />
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </div>
                        ))}
                    </div>
                )}

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

                {/* Callout */}
                {callout && (
                    <div style={{
                        background: callout.type === 'critical'
                            ? 'rgba(239, 68, 68, 0.2)'
                            : callout.type === 'warning'
                                ? 'rgba(251, 191, 36, 0.2)'
                                : 'rgba(59, 130, 246, 0.2)',
                        border: `2px solid ${callout.type === 'critical'
                            ? '#ef4444'
                            : callout.type === 'warning'
                                ? '#fbbf24'
                                : '#3b82f6'
                            }`,
                        borderRadius: '12px',
                        padding: '20px',
                        marginTop: '30px',
                        display: 'flex',
                        alignItems: 'flex-start',
                        gap: '15px'
                    }}>
                        {callout.type === 'critical' && <AlertTriangle size={24} color="#ef4444" style={{ flexShrink: 0 }} />}
                        {callout.type === 'warning' && <AlertTriangle size={24} color="#fbbf24" style={{ flexShrink: 0 }} />}
                        {callout.type === 'info' && <Lightbulb size={24} color="#3b82f6" style={{ flexShrink: 0 }} />}
                        <div
                            style={{
                                fontSize: '1.05rem',
                                lineHeight: 1.7
                            }}
                            dangerouslySetInnerHTML={{
                                __html: callout.text
                                    .replace(/„/g, '"')
                                    .replace(/"/g, '"')
                                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                            }}
                        />
                    </div>
                )}
            </div>

            {/* Remember Box */}
            {remember && (
                <div style={{
                    background: 'rgba(0, 255, 135, 0.1)',
                    backdropFilter: 'blur(20px)',
                    WebkitBackdropFilter: 'blur(20px)',
                    border: '2px solid rgba(0, 255, 135, 0.4)',
                    borderRadius: '16px',
                    padding: '30px'
                }}>
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        marginBottom: '20px'
                    }}>
                        <Lightbulb size={28} color="#00ff87" />
                        <h3 style={{
                            fontSize: '1.4rem',
                            fontWeight: 700,
                            color: '#00ff87',
                            margin: 0
                        }}>
                            {remember.title || 'Zapamiętaj'}
                        </h3>
                    </div>
                    {/* New structure with items array */}
                    {remember.items && remember.items.length > 0 && (
                        <ul style={{
                            listStyle: 'none',
                            padding: 0,
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '12px'
                        }}>
                            {remember.items.map((item, i) => (
                                <li
                                    key={i}
                                    style={{
                                        padding: '10px 0',
                                        paddingLeft: '30px',
                                        position: 'relative',
                                        lineHeight: 1.7,
                                        fontSize: '1.05rem'
                                    }}
                                >
                                    <span style={{
                                        position: 'absolute',
                                        left: 0,
                                        color: '#00ff87',
                                        fontSize: '1.2rem'
                                    }}>✔</span>
                                    <span dangerouslySetInnerHTML={{
                                        __html: item.replace(/\*\*(.*?)\*\*/g, '<strong style="color: #00ff87;">$1</strong>')
                                    }} />
                                </li>
                            ))}
                        </ul>
                    )}
                    {/* Old structure with text field - backward compatibility */}
                    {remember.text && !remember.items && (
                        <div style={{
                            fontSize: '1.05rem',
                            lineHeight: 1.7,
                            paddingLeft: '30px',
                            position: 'relative'
                        }}>
                            <span style={{
                                position: 'absolute',
                                left: 0,
                                color: '#00ff87',
                                fontSize: '1.2rem'
                            }}>✔</span>
                            <span dangerouslySetInnerHTML={{
                                __html: remember.text.replace(/\*\*(.*?)\*\*/g, '<strong style="color: #00ff87;">$1</strong>')
                            }} />
                        </div>
                    )}
                </div>
            )}

            {/* Key Points (legacy support) */}
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
