'use client'

import { AlertTriangle } from 'lucide-react'

interface WarningCardProps {
    title: string
    content: string
    warnings?: string[]
    example?: string
}

export default function WarningCard({ title, content, warnings, example }: WarningCardProps) {
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
                color: '#ff0055',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(255, 0, 85, 0.1)',
                border: '1px solid rgba(255, 0, 85, 0.2)',
                borderRadius: '20px',
                width: 'fit-content'
            }}>
                WARNING
            </div>

            {/* Main Content Card */}
            <div style={{
                background: 'rgba(20, 20, 35, 0.6)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 0, 85, 0.2)',
                borderRadius: '20px',
                padding: '40px',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
                borderLeft: '4px solid #ff0055'
            }}>
                {/* Icon + Title */}
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '16px',
                    marginBottom: '24px'
                }}>
                    <div style={{
                        width: '48px',
                        height: '48px',
                        borderRadius: '12px',
                        background: 'rgba(255, 0, 85, 0.2)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                    }}>
                        <AlertTriangle size={28} style={{ color: '#ff0055' }} />
                    </div>
                    <h2 style={{
                        fontSize: '28px',
                        fontWeight: 700,
                        color: '#ff0055',
                        flex: 1
                    }}>
                        {title}
                    </h2>
                </div>

                {/* Content */}
                <div style={{
                    fontSize: '16px',
                    lineHeight: '1.8',
                    color: 'rgba(255, 255, 255, 0.9)',
                    marginBottom: warnings || example ? '24px' : '0'
                }}>
                    {content}
                </div>

                {/* Warnings List */}
                {warnings && warnings.length > 0 && (
                    <div style={{
                        marginTop: '24px',
                        padding: '20px',
                        background: 'rgba(255, 0, 85, 0.1)',
                        borderRadius: '12px',
                        border: '1px solid rgba(255, 0, 85, 0.2)'
                    }}>
                        <h4 style={{
                            fontSize: '14px',
                            fontWeight: 600,
                            marginBottom: '12px',
                            color: '#ff0055',
                            textTransform: 'uppercase',
                            letterSpacing: '0.5px'
                        }}>
                            ⚠️ Uważaj na:
                        </h4>
                        <ul style={{
                            listStyle: 'none',
                            padding: 0,
                            margin: 0,
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '12px'
                        }}>
                            {warnings.map((warning, index) => (
                                <li key={index} style={{
                                    display: 'flex',
                                    alignItems: 'flex-start',
                                    gap: '12px',
                                    fontSize: '15px',
                                    lineHeight: '1.6',
                                    padding: '12px',
                                    background: 'rgba(0, 0, 0, 0.2)',
                                    borderRadius: '8px'
                                }}>
                                    <span style={{
                                        color: '#ff0055',
                                        fontSize: '18px',
                                        fontWeight: 700,
                                        flexShrink: 0
                                    }}>
                                        ×
                                    </span>
                                    <span>{warning}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}

                {/* Example */}
                {example && (
                    <div style={{
                        marginTop: '24px',
                        padding: '20px',
                        background: 'rgba(255, 215, 0, 0.05)',
                        borderRadius: '12px',
                        border: '1px solid rgba(255, 215, 0, 0.2)'
                    }}>
                        <h4 style={{
                            fontSize: '14px',
                            fontWeight: 600,
                            marginBottom: '12px',
                            color: '#ffd700',
                            textTransform: 'uppercase',
                            letterSpacing: '0.5px'
                        }}>
                            📖 Przykład z życia:
                        </h4>
                        <p style={{
                            fontSize: '15px',
                            lineHeight: '1.7',
                            color: 'rgba(255, 255, 255, 0.9)',
                            fontStyle: 'italic',
                            margin: 0
                        }}>
                            {example}
                        </p>
                    </div>
                )}
            </div>
        </div>
    )
}
