'use client'

import { useState } from 'react'
import { Check } from 'lucide-react'

interface HabitAction {
    text?: string // for backwards compat
    id: string
    // New fields for OJT lessons
    icon?: string
    title?: string
    description?: string
    goal?: string
}

interface HabitBuilderCardProps {
    title: string
    description: string
    habits: HabitAction[]
    tip?: string // Overall tip for all habits
}

export default function HabitBuilderCard({ title, description, habits = [], tip }: HabitBuilderCardProps) {
    const [checkedState, setCheckedState] = useState<Record<string, boolean>>({})

    const toggleHabit = (id: string) => {
        setCheckedState(prev => ({
            ...prev,
            [id]: !prev[id]
        }))
    }

    return (
        <div style={{
            maxWidth: '600px',
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            gap: '24px'
        }}>
            <div style={{
                padding: '30px',
                border: '1px solid rgba(255, 255, 255, 0.05)',
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
                    color: '#00ff88',
                    fontWeight: 600,
                    padding: '6px 12px',
                    background: 'rgba(0, 255, 136, 0.1)',
                    border: '1px solid rgba(0, 255, 136, 0.2)',
                    borderRadius: '20px'
                }}>
                    ACTION PLAN
                </div>
                <div style={{
                    textAlign: 'center',
                    marginBottom: '30px'
                }}>
                    <div style={{
                        fontSize: '12px',
                        fontWeight: 700,
                        color: '#00ff88',
                        textTransform: 'uppercase',
                        letterSpacing: '1px',
                        marginBottom: '10px'
                    }}>
                        ACTION PLAN
                    </div>
                    <h2 style={{
                        fontSize: '24px',
                        fontWeight: 700,
                        color: '#fff',
                        marginBottom: '10px'
                    }}>
                        {title}
                    </h2>
                    <p style={{
                        color: 'rgba(255, 255, 255, 0.7)',
                        fontSize: '15px'
                    }}>
                        {description}
                    </p>
                </div>

                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '12px'
                }}>
                    {habits.map((habit) => {
                        const isChecked = checkedState[habit.id] || false
                        const hasRichContent = habit.icon || habit.title || habit.description
                        return (
                            <div
                                key={habit.id}
                                onClick={() => toggleHabit(habit.id)}
                                style={{
                                    background: isChecked ? 'rgba(0, 255, 136, 0.15)' : 'rgba(255, 255, 255, 0.05)',
                                    border: `2px solid ${isChecked ? '#00ff88' : 'rgba(255, 255, 255, 0.1)'}`,
                                    borderRadius: '12px',
                                    padding: '18px',
                                    cursor: 'pointer',
                                    transition: 'all 0.3s ease',
                                    display: 'flex',
                                    alignItems: hasRichContent ? 'flex-start' : 'center',
                                    gap: '15px'
                                }}
                            >
                                <div style={{
                                    width: '24px',
                                    height: '24px',
                                    border: `2px solid ${isChecked ? '#00ff88' : 'rgba(255, 255, 255, 0.3)'}`,
                                    borderRadius: '6px',
                                    background: isChecked ? 'linear-gradient(135deg, #00ff88, #00cc70)' : 'transparent',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    transition: 'all 0.2s',
                                    flexShrink: 0,
                                    marginTop: hasRichContent ? '4px' : '0'
                                }}>
                                    {isChecked && <Check size={16} color="#000" strokeWidth={3} />}
                                </div>

                                {/* Rich content (new format) */}
                                {hasRichContent ? (
                                    <div style={{ flex: 1 }}>
                                        <div style={{
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: '10px',
                                            marginBottom: '8px'
                                        }}>
                                            {habit.icon && (
                                                <span style={{ fontSize: '20px', flexShrink: 0 }}>
                                                    {habit.icon}
                                                </span>
                                            )}
                                            {habit.title && (
                                                <span style={{
                                                    fontSize: '17px',
                                                    fontWeight: 700,
                                                    color: isChecked ? '#fff' : 'rgba(255, 255, 255, 0.95)',
                                                    textDecoration: isChecked ? 'line-through' : 'none'
                                                }}>
                                                    {habit.title}
                                                </span>
                                            )}
                                        </div>
                                        {habit.description && (
                                            <p style={{
                                                fontSize: '15px',
                                                lineHeight: '1.6',
                                                color: isChecked ? 'rgba(255, 255, 255, 0.6)' : 'rgba(255, 255, 255, 0.7)',
                                                margin: '0 0 8px 0'
                                            }}>
                                                {habit.description}
                                            </p>
                                        )}
                                        {habit.goal && (
                                            <div style={{
                                                display: 'inline-block',
                                                padding: '4px 10px',
                                                background: 'rgba(0, 212, 255, 0.15)',
                                                borderRadius: '6px',
                                                fontSize: '13px',
                                                fontWeight: 600,
                                                color: '#00d4ff'
                                            }}>
                                                🎯 {habit.goal}
                                            </div>
                                        )}
                                    </div>
                                ) : (
                                    /* Simple text (old format) */
                                    <span style={{
                                        fontSize: '16px',
                                        color: isChecked ? '#fff' : 'rgba(255, 255, 255, 0.8)',
                                        fontWeight: isChecked ? 600 : 400,
                                        textDecoration: isChecked ? 'line-through' : 'none',
                                        opacity: isChecked ? 0.8 : 1,
                                        transition: 'all 0.2s'
                                    }}>
                                        {habit.text}
                                    </span>
                                )}
                            </div>
                        )
                    })}
                </div>

                {/* Tip (if present) */}
                {tip && (
                    <div style={{
                        marginTop: '20px',
                        padding: '16px',
                        background: 'rgba(255, 136, 0, 0.1)',
                        borderRadius: '8px',
                        borderLeft: '4px solid #ff8800'
                    }}>
                        <div style={{
                            fontSize: '13px',
                            fontWeight: 600,
                            color: '#ff8800',
                            marginBottom: '6px',
                            textTransform: 'uppercase',
                            letterSpacing: '0.5px'
                        }}>
                            💡 Wskazówka
                        </div>
                        <div style={{
                            fontSize: '14px',
                            lineHeight: '1.6',
                            color: 'rgba(255, 255, 255, 0.85)'
                        }}>
                            {tip}
                        </div>
                    </div>
                )}

                <div style={{
                    marginTop: '25px',
                    textAlign: 'center',
                    fontSize: '13px',
                    color: 'rgba(255, 255, 255, 0.4)',
                    fontStyle: 'italic'
                }}>
                    Zobowiązuję się wykonać te zadania w tym tygodniu.
                </div>
            </div>
        </div>
    )
}
