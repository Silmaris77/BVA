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
    // New fields for OJT lessons
    comparison?: {
        headers: [string, string]
        rows: Array<{
            wrong: string
            right: string
        }>
    }
    whenToTell?: {
        title: string
        cases: string[]
    }
    caseStudy?: {
        title: string
        company: string
        investment: string[]
        results: string[]
        roi: string
    }
    quote?: string
    quoteAuthor?: string
    highlight?: string
    footnote?: string
    icon?: string
}

export default function LightbulbCard({ 
    title, 
    content, 
    insight, 
    accent_color = 'yellow', 
    steps,
    comparison,
    whenToTell,
    caseStudy,
    quote,
    quoteAuthor,
    highlight,
    footnote,
    icon
}: LightbulbCardProps) {
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
            <div style={{
                background: gradient,
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: `2px solid ${borderColor}`,
                borderRadius: '24px',
                padding: '60px 40px',
                textAlign: 'center',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.2)',
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
                    color: accentColor,
                    fontWeight: 600,
                    padding: '6px 12px',
                    background: `rgba(${accent_color === 'yellow' ? '255, 215, 0' : '0, 212, 255'}, 0.1)`,
                    border: `1px solid ${borderColor}`,
                    borderRadius: '20px'
                }}>
                    INSIGHT
                </div>

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

                {/* Comparison Table */}
                {comparison && (
                    <div style={{ marginBottom: '40px', maxWidth: '800px', margin: '0 auto 40px auto' }}>
                        <div style={{
                            display: 'grid',
                            gridTemplateColumns: '1fr 1fr',
                            gap: '16px',
                            background: 'rgba(0, 0, 0, 0.2)',
                            borderRadius: '12px',
                            padding: '24px',
                            textAlign: 'left'
                        }}>
                            {/* Headers */}
                            <div style={{
                                padding: '12px',
                                background: 'rgba(255, 0, 0, 0.1)',
                                borderRadius: '8px',
                                border: '1px solid rgba(255, 0, 0, 0.3)',
                                fontWeight: 700,
                                fontSize: '15px',
                                color: '#ff6b6b',
                                textAlign: 'center'
                            }}>
                                {comparison.headers[0]}
                            </div>
                            <div style={{
                                padding: '12px',
                                background: 'rgba(0, 255, 136, 0.1)',
                                borderRadius: '8px',
                                border: '1px solid rgba(0, 255, 136, 0.3)',
                                fontWeight: 700,
                                fontSize: '15px',
                                color: '#00ff88',
                                textAlign: 'center'
                            }}>
                                {comparison.headers[1]}
                            </div>
                            {/* Rows */}
                            {comparison.rows.map((row, index) => (
                                <>
                                    <div key={`wrong-${index}`} style={{
                                        padding: '14px',
                                        background: 'rgba(255, 255, 255, 0.03)',
                                        borderRadius: '8px',
                                        fontSize: '15px',
                                        lineHeight: '1.6',
                                        color: 'rgba(255, 255, 255, 0.85)'
                                    }}>
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{row.wrong}</ReactMarkdown>
                                    </div>
                                    <div key={`right-${index}`} style={{
                                        padding: '14px',
                                        background: 'rgba(255, 255, 255, 0.03)',
                                        borderRadius: '8px',
                                        fontSize: '15px',
                                        lineHeight: '1.6',
                                        color: 'rgba(255, 255, 255, 0.85)'
                                    }}>
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{row.right}</ReactMarkdown>
                                    </div>
                                </>
                            ))}
                        </div>
                    </div>
                )}

                {/* When to Tell */}
                {whenToTell && (
                    <div style={{
                        marginBottom: '40px',
                        maxWidth: '700px',
                        margin: '0 auto 40px auto',
                        textAlign: 'left'
                    }}>
                        <h3 style={{
                            fontSize: '18px',
                            fontWeight: 700,
                            color: accentColor,
                            marginBottom: '16px',
                            textAlign: 'center'
                        }}>
                            {whenToTell.title}
                        </h3>
                        <ul style={{
                            listStyle: 'none',
                            padding: 0,
                            margin: 0,
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '12px'
                        }}>
                            {whenToTell.cases.map((caseItem, index) => (
                                <li key={index} style={{
                                    padding: '14px 18px',
                                    background: 'rgba(0, 0, 0, 0.2)',
                                    borderRadius: '8px',
                                    borderLeft: `4px solid ${accentColor}`,
                                    fontSize: '15px',
                                    lineHeight: '1.6',
                                    color: 'rgba(255, 255, 255, 0.9)'
                                }}>
                                    {caseItem}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}

                {/* Case Study */}
                {caseStudy && (
                    <div style={{
                        marginBottom: '40px',
                        maxWidth: '800px',
                        margin: '0 auto 40px auto',
                        padding: '28px',
                        background: 'rgba(0, 0, 0, 0.3)',
                        borderRadius: '16px',
                        border: `2px solid ${accentColor}`,
                        textAlign: 'left'
                    }}>
                        <h3 style={{
                            fontSize: '19px',
                            fontWeight: 700,
                            color: accentColor,
                            marginBottom: '16px'
                        }}>
                            {caseStudy.title}
                        </h3>
                        <div style={{
                            fontSize: '16px',
                            color: 'rgba(255, 255, 255, 0.8)',
                            marginBottom: '18px',
                            fontStyle: 'italic'
                        }}>
                            {caseStudy.company}
                        </div>
                        <div style={{ marginBottom: '18px' }}>
                            <div style={{
                                fontSize: '14px',
                                fontWeight: 600,
                                color: '#ff8800',
                                marginBottom: '8px',
                                textTransform: 'uppercase',
                                letterSpacing: '0.5px'
                            }}>
                                Inwestycja:
                            </div>
                            <ul style={{ margin: 0, paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                                {caseStudy.investment.map((item, index) => (
                                    <li key={index} style={{ fontSize: '15px', lineHeight: '1.6', color: 'rgba(255, 255, 255, 0.85)' }}>
                                        {item}
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <div style={{ marginBottom: '18px' }}>
                            <div style={{
                                fontSize: '14px',
                                fontWeight: 600,
                                color: '#00ff88',
                                marginBottom: '8px',
                                textTransform: 'uppercase',
                                letterSpacing: '0.5px'
                            }}>
                                Wyniki:
                            </div>
                            <ul style={{ margin: 0, paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                                {caseStudy.results.map((item, index) => (
                                    <li key={index} style={{ fontSize: '15px', lineHeight: '1.6', color: 'rgba(255, 255, 255, 0.85)' }}>
                                        {item}
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <div style={{
                            padding: '16px',
                            background: `rgba(${accent_color === 'yellow' ? '255, 215, 0' : '0, 212, 255'}, 0.15)`,
                            borderRadius: '8px',
                            fontSize: '17px',
                            fontWeight: 700,
                            color: accentColor,
                            textAlign: 'center'
                        }}>
                            ROI: {caseStudy.roi}
                        </div>
                    </div>
                )}

                {/* Highlight */}
                {highlight && (
                    <div style={{
                        marginBottom: '30px',
                        padding: '20px 30px',
                        background: 'rgba(0, 0, 0, 0.3)',
                        borderRadius: '12px',
                        borderLeft: `4px solid ${accentColor}`,
                        fontSize: '20px',
                        fontWeight: 600,
                        fontStyle: 'italic',
                        color: '#fff',
                        maxWidth: '700px',
                        margin: '0 auto 30px auto'
                    }}>
                        {highlight}
                    </div>
                )}

                {/* Quote */}
                {quote && (
                    <div style={{
                        marginBottom: '30px',
                        padding: '24px',
                        background: 'rgba(0, 0, 0, 0.2)',
                        borderRadius: '12px',
                        maxWidth: '700px',
                        margin: '0 auto 30px auto',
                        textAlign: 'center'
                    }}>
                        <div style={{
                            fontSize: '19px',
                            fontStyle: 'italic',
                            lineHeight: '1.6',
                            color: 'rgba(255, 255, 255, 0.95)',
                            marginBottom: '12px'
                        }}>
                            "{quote}"
                        </div>
                        {quoteAuthor && (
                            <div style={{
                                fontSize: '14px',
                                color: accentColor,
                                fontWeight: 600
                            }}>
                                — {quoteAuthor}
                            </div>
                        )}
                    </div>
                )}

                {/* Footnote */}
                {footnote && (
                    <div style={{
                        marginTop: '30px',
                        padding: '16px',
                        background: 'rgba(0, 0, 0, 0.2)',
                        borderRadius: '8px',
                        fontSize: '14px',
                        lineHeight: '1.6',
                        color: 'rgba(255, 255, 255, 0.6)',
                        fontStyle: 'italic',
                        maxWidth: '700px',
                        margin: '30px auto 0 auto',
                        textAlign: 'center'
                    }}>
                        {footnote}
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
