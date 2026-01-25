'use client'

import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { useState } from 'react'
import { ChevronDown, ChevronUp } from 'lucide-react'

interface PracticeCardProps {
    title: string
    content: string
    keyPoints?: string[]
    actionSteps?: string[]
    // New fields for OJT lessons
    scenario?: string
    instruction?: string
    inputs?: Array<{
        label: string
        placeholder: string
        type?: 'text' | 'textarea'
    }>
    sampleAnswers?: {
        title?: string
        answers: string[]
        tip?: string
    }
}

export default function PracticeCard({ title, content, keyPoints, actionSteps, scenario, instruction, inputs, sampleAnswers }: PracticeCardProps) {
    const [inputValues, setInputValues] = useState<Record<number, string>>({})
    const [showAnswers, setShowAnswers] = useState(false)

    const handleInputChange = (index: number, value: string) => {
        setInputValues(prev => ({ ...prev, [index]: value }))
    }

    return (
        <div style={{
            maxWidth: '900px',
            width: '100%'
        }}>
            {/* Main Content Card */}
            <div style={{
                position: 'relative',
                background: 'rgba(20, 20, 35, 0.6)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(0, 255, 136, 0.2)',
                borderRadius: '20px',
                padding: '40px',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
                borderLeft: '4px solid #00ff88'
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
                    color: '#00ff88',
                    fontWeight: 600,
                    padding: '6px 12px',
                    background: 'rgba(0, 255, 136, 0.1)',
                    border: '1px solid rgba(0, 255, 136, 0.2)',
                    borderRadius: '20px'
                }}>
                    PRACTICE
                </div>

                {/* Title */}
                <h2 style={{
                    fontSize: '28px',
                    fontWeight: 700,
                    marginBottom: '24px',
                    marginTop: '20px',
                    color: '#00ff88'
                }}>
                    {title}
                </h2>

                {/* Scenario (if present) */}
                {scenario && (
                    <div style={{
                        marginBottom: '20px',
                        padding: '20px',
                        background: 'rgba(255, 136, 0, 0.1)',
                        borderRadius: '12px',
                        borderLeft: '4px solid #ff8800'
                    }}>
                        <h4 style={{ color: '#ff8800', marginBottom: '10px', fontSize: '1rem', fontWeight: 600 }}>Scenariusz:</h4>
                        <div style={{ fontSize: '15px', lineHeight: '1.7', color: 'rgba(255, 255, 255, 0.9)' }}>
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>{scenario}</ReactMarkdown>
                        </div>
                    </div>
                )}

                {/* Instruction (if present) */}
                {instruction && (
                    <div style={{
                        marginBottom: '20px',
                        padding: '16px',
                        background: 'rgba(0, 212, 255, 0.1)',
                        borderRadius: '8px',
                        fontSize: '15px',
                        fontWeight: 600,
                        color: '#00d4ff'
                    }}>
                        {instruction}
                    </div>
                )}

                {/* Content */}
                <div style={{
                    fontSize: '16px',
                    lineHeight: '1.8',
                    color: 'rgba(255, 255, 255, 0.9)',
                    marginBottom: keyPoints || actionSteps || inputs ? '24px' : '0'
                }}>
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {content}
                    </ReactMarkdown>
                </div>

                {/* Interactive Inputs (if present) */}
                {inputs && inputs.length > 0 && (
                    <div style={{ marginTop: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        {inputs.map((input, index) => (
                            <div key={index}>
                                <label style={{
                                    display: 'block',
                                    marginBottom: '8px',
                                    fontSize: '14px',
                                    fontWeight: 600,
                                    color: '#00ff88'
                                }}>
                                    {input.label}
                                </label>
                                {input.type === 'textarea' ? (
                                    <textarea
                                        value={inputValues[index] || ''}
                                        onChange={(e) => handleInputChange(index, e.target.value)}
                                        placeholder={input.placeholder}
                                        style={{
                                            width: '100%',
                                            padding: '12px',
                                            background: 'rgba(0, 0, 0, 0.3)',
                                            border: '1px solid rgba(0, 255, 136, 0.3)',
                                            borderRadius: '8px',
                                            color: '#fff',
                                            fontSize: '15px',
                                            fontFamily: 'inherit',
                                            resize: 'vertical',
                                            minHeight: '80px'
                                        }}
                                    />
                                ) : (
                                    <input
                                        type="text"
                                        value={inputValues[index] || ''}
                                        onChange={(e) => handleInputChange(index, e.target.value)}
                                        placeholder={input.placeholder}
                                        style={{
                                            width: '100%',
                                            padding: '12px',
                                            background: 'rgba(0, 0, 0, 0.3)',
                                            border: '1px solid rgba(0, 255, 136, 0.3)',
                                            borderRadius: '8px',
                                            color: '#fff',
                                            fontSize: '15px',
                                            fontFamily: 'inherit'
                                        }}
                                    />
                                )}
                            </div>
                        ))}
                    </div>
                )}

                {/* Sample Answers (collapsible) */}
                {sampleAnswers && (
                    <div style={{ marginTop: '24px' }}>
                        <button
                            onClick={() => setShowAnswers(!showAnswers)}
                            style={{
                                width: '100%',
                                padding: '14px 20px',
                                background: 'rgba(176, 0, 255, 0.2)',
                                border: '1px solid rgba(176, 0, 255, 0.4)',
                                borderRadius: '8px',
                                color: '#b000ff',
                                fontSize: '15px',
                                fontWeight: 600,
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                gap: '8px',
                                transition: 'all 0.2s'
                            }}
                        >
                            {showAnswers ? (
                                <><ChevronUp size={20} /> Ukryj przykładowe odpowiedzi</>
                            ) : (
                                <><ChevronDown size={20} /> Pokaż przykładowe odpowiedzi</>
                            )}
                        </button>
                        {showAnswers && (
                            <div style={{
                                marginTop: '16px',
                                padding: '20px',
                                background: 'rgba(176, 0, 255, 0.1)',
                                borderRadius: '12px',
                                border: '1px solid rgba(176, 0, 255, 0.2)'
                            }}>
                                {sampleAnswers.title && (
                                    <h4 style={{ color: '#b000ff', marginBottom: '12px', fontSize: '1rem' }}>
                                        {sampleAnswers.title}
                                    </h4>
                                )}
                                <ol style={{ paddingLeft: '20px', margin: 0, display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                    {sampleAnswers.answers.map((answer, index) => (
                                        <li key={index} style={{
                                            fontSize: '15px',
                                            lineHeight: '1.7',
                                            color: 'rgba(255, 255, 255, 0.9)'
                                        }}>
                                            <ReactMarkdown remarkPlugins={[remarkGfm]}>{answer}</ReactMarkdown>
                                        </li>
                                    ))}
                                </ol>
                                {sampleAnswers.tip && (
                                    <div style={{
                                        marginTop: '16px',
                                        padding: '16px',
                                        background: 'rgba(0, 255, 136, 0.1)',
                                        borderRadius: '8px',
                                        borderLeft: '4px solid #00ff88'
                                    }}>
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{sampleAnswers.tip}</ReactMarkdown>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                )}

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
