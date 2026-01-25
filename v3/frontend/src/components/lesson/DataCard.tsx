'use client'

import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface DataCardProps {
    icon?: string
    title: string
    subtitle?: string
    content?: string
    stats: {
        value: string
        label: string
    }[]
    infoBoxes?: {
        icon?: string
        title: string
        content: string
        type?: 'warning' | 'info'
    }[]
    table?: {
        title?: string
        headers: string[]
        rows: string[][]
    }
    callout?: {
        type: 'warning' | 'success' | 'info'
        title?: string
        text: string
    }
    sources?: string
}

export default function DataCard({ icon = '📊', title, subtitle, content, stats, callout, infoBoxes, table, sources }: DataCardProps) {
    const calloutColors = {
        warning: { bg: 'rgba(245, 158, 11, 0.1)', border: 'rgba(245, 158, 11, 0.3)', text: '#f59e0b' },
        success: { bg: 'rgba(0, 255, 135, 0.1)', border: 'rgba(0, 255, 135, 0.3)', text: '#00ff87' },
        info: { bg: 'rgba(96, 239, 255, 0.1)', border: 'rgba(96, 239, 255, 0.3)', text: '#60efff' }
    }

    return (
        <div style={{
            maxWidth: '900px',
            width: '100%',
            background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(251, 146, 60, 0.1))',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            border: '2px solid rgba(245, 158, 11, 0.4)',
            borderRadius: '24px',
            padding: '50px',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
            position: 'relative'
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
                color: '#f59e0b',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(245, 158, 11, 0.1)',
                border: '1px solid rgba(245, 158, 11, 0.2)',
                borderRadius: '20px'
            }}>
                DANE
            </div>
            {/* Header */}
            <div style={{ textAlign: 'center', marginBottom: '40px' }}>
                <div style={{ fontSize: '4rem', marginBottom: '20px' }}>{icon}</div>
                <h2 style={{
                    fontSize: '2.2rem',
                    fontWeight: 700,
                    color: '#f59e0b',
                    marginBottom: '15px'
                }}>
                    {title}
                </h2>
                {subtitle && (
                    <p style={{ fontSize: '1.1rem', opacity: 0.9, color: 'rgba(255, 255, 255, 0.8)' }}>
                        {subtitle}
                    </p>
                )}
            </div>

            {/* Content */}
            {content && (
                <div style={{
                    fontSize: '1.1rem',
                    lineHeight: 1.8,
                    opacity: 0.9,
                    marginBottom: '40px',
                    textAlign: 'left',
                    whiteSpace: 'pre-line'
                }}>
                    {content}
                </div>
            )}

            {/* Stats Grid */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '25px',
                marginBottom: callout ? '40px' : '0'
            }}>
                {stats.map((stat, index) => (
                    <div
                        key={index}
                        style={{
                            textAlign: 'center',
                            padding: '30px',
                            background: 'rgba(0, 0, 0, 0.3)',
                            borderRadius: '16px',
                            border: '2px solid rgba(245, 158, 11, 0.3)',
                            transition: 'all 0.3s ease',
                            cursor: 'pointer'
                        }}
                        onMouseOver={(e) => {
                            e.currentTarget.style.transform = 'translateY(-5px)'
                            e.currentTarget.style.borderColor = '#f59e0b'
                        }}
                        onMouseOut={(e) => {
                            e.currentTarget.style.transform = 'translateY(0)'
                            e.currentTarget.style.borderColor = 'rgba(245, 158, 11, 0.3)'
                        }}
                    >
                        <div style={{
                            fontSize: '3.5rem',
                            fontWeight: 800,
                            color: '#f59e0b',
                            marginBottom: '12px'
                        }}>
                            {stat.value}
                        </div>
                        <div style={{
                            fontSize: '1rem',
                            opacity: 0.9,
                            lineHeight: 1.6,
                            color: 'rgba(255, 255, 255, 0.9)'
                        }}
                            dangerouslySetInnerHTML={{ __html: stat.label.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }}
                        />
                    </div>
                ))}
            </div>

            {/* Info Boxes */}
            {infoBoxes && infoBoxes.map((box, index) => (
                <div key={index} style={{
                    background: 'rgba(50, 40, 30, 0.4)',
                    border: '1px solid rgba(245, 158, 11, 0.2)',
                    borderRadius: '16px',
                    padding: '25px',
                    marginBottom: '20px'
                }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '15px' }}>
                        <span style={{ fontSize: '1.5rem' }}>{box.icon || (box.type === 'warning' ? '⚠️' : '🧱')}</span>
                        <h4 style={{ color: '#f59e0b', fontSize: '1.2rem', margin: 0 }}>{box.title}</h4>
                    </div>
                    <div style={{ 
                        fontSize: '1rem', 
                        lineHeight: '1.6', 
                        opacity: 0.9,
                        wordWrap: 'break-word',
                        overflowWrap: 'break-word'
                    }}>
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{box.content}</ReactMarkdown>
                    </div>
                </div>
            ))}

            {/* Data Table */}
            {table && (
                <div style={{ marginTop: '40px', marginBottom: '30px' }}>
                    {table.title && (
                        <h3 style={{ color: '#f59e0b', textAlign: 'center', marginBottom: '20px', fontSize: '1.4rem' }}>
                            {table.title}
                        </h3>
                    )}
                    <div style={{ overflowX: 'auto' }}>
                        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.95rem' }}>
                            <thead>
                                <tr>
                                    {table.headers.map((header, i) => (
                                        <th key={i} style={{
                                            textAlign: 'left',
                                            padding: '15px',
                                            borderBottom: '2px solid rgba(245, 158, 11, 0.3)',
                                            color: '#f59e0b',
                                            background: 'rgba(245, 158, 11, 0.05)'
                                        }}>
                                            {header}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {table.rows.map((row, i) => (
                                    <tr key={i} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
                                        {row.map((cell, j) => (
                                            <td key={j} style={{ padding: '15px', opacity: 0.9 }}>{cell}</td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}

            {/* Callout */}
            {callout && (
                <div style={{
                    background: calloutColors[callout.type].bg,
                    border: `2px solid ${calloutColors[callout.type].border}`,
                    borderRadius: '12px',
                    padding: '25px',
                    textAlign: 'center',
                    marginTop: '30px'
                }}>
                    {callout.title && (
                        <strong style={{
                            fontSize: '1.1rem',
                            color: calloutColors[callout.type].text,
                            display: 'block',
                            marginBottom: '10px'
                        }}>
                            {callout.title}
                        </strong>
                    )}
                    <p style={{
                        fontSize: '1.3rem',
                        lineHeight: 1.8,
                        fontWeight: 600,
                        color: 'rgba(255, 255, 255, 0.95)',
                        margin: 0
                    }}
                        dangerouslySetInnerHTML={{ __html: callout.text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }}
                    />
                </div>
            )}

            {/* Sources */}
            {sources && (
                <div style={{
                    marginTop: '30px',
                    padding: '15px 0',
                    borderTop: '1px solid rgba(245, 158, 11, 0.2)',
                    fontSize: '0.9rem',
                    opacity: 0.7,
                    textAlign: 'center',
                    fontStyle: 'italic'
                }}>
                    {sources}
                </div>
            )}
        </div>
    )
}
