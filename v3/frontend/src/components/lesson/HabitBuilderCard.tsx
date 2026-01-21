'use client'

import { useState } from 'react'
import { Check } from 'lucide-react'

interface HabitAction {
    text: string
    id: string
}

interface HabitBuilderCardProps {
    title: string
    description: string
    habits: HabitAction[]
}

export default function HabitBuilderCard({ title, description, habits = [] }: HabitBuilderCardProps) {
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
                background: 'rgba(255, 255, 255, 0.03)',
                borderRadius: '16px',
                padding: '30px',
                border: '1px solid rgba(255, 255, 255, 0.05)'
            }}>
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
                                    alignItems: 'center',
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
                                    flexShrink: 0
                                }}>
                                    {isChecked && <Check size={16} color="#000" strokeWidth={3} />}
                                </div>
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
                            </div>
                        )
                    })}
                </div>

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
