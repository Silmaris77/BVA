'use client'

import { useState } from 'react'
import { CheckCircle2, XCircle, Info } from 'lucide-react'

interface QuestionCardProps {
    question: string
    options: string[]
    correctAnswer: number
    explanation?: string
    onAnswer?: (correct: boolean) => void
}

export default function QuestionCard({
    question,
    options,
    correctAnswer,
    explanation,
    onAnswer
}: QuestionCardProps) {
    const [selectedOption, setSelectedOption] = useState<number | null>(null)
    const [answered, setAnswered] = useState(false)

    const handleSelect = (index: number) => {
        if (answered) return

        setSelectedOption(index)
        setAnswered(true)

        const isCorrect = index === correctAnswer
        if (onAnswer) {
            onAnswer(isCorrect)
        }
    }

    const getOptionStyle = (index: number) => {
        const baseStyle = {
            padding: '20px 24px',
            background: 'rgba(255, 255, 255, 0.05)',
            border: '2px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '16px',
            cursor: answered ? 'default' : 'pointer',
            transition: 'all 0.2s',
            display: 'flex',
            alignItems: 'center',
            gap: '16px',
            fontFamily: 'Outfit, sans-serif',
            fontSize: '16px'
        }

        if (!answered) {
            return baseStyle
        }

        if (index === correctAnswer) {
            return {
                ...baseStyle,
                background: 'rgba(0, 255, 136, 0.15)',
                borderColor: '#00ff88',
                boxShadow: '0 0 20px rgba(0, 255, 136, 0.2)'
            }
        }

        if (index === selectedOption && index !== correctAnswer) {
            return {
                ...baseStyle,
                background: 'rgba(239, 68, 68, 0.15)',
                borderColor: '#ef4444',
                boxShadow: '0 0 20px rgba(239, 68, 68, 0.2)'
            }
        }

        return {
            ...baseStyle,
            opacity: 0.5
        }
    }

    const letters = ['A', 'B', 'C', 'D']

    return (
        <div style={{
            maxWidth: '800px',
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            gap: '32px'
        }}>
            {/* Question */}
            <div style={{
                background: 'rgba(20, 20, 35, 0.6)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '20px',
                padding: '40px',
                textAlign: 'center'
            }}>
                <h2 style={{
                    fontSize: '24px',
                    fontWeight: 600,
                    lineHeight: '1.5'
                }}>
                    {question}
                </h2>
            </div>

            {/* Options */}
            <div style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '16px'
            }}>
                {options.map((option, index) => (
                    <button
                        key={index}
                        onClick={() => handleSelect(index)}
                        style={getOptionStyle(index)}
                        onMouseOver={(e) => {
                            if (!answered) {
                                e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)'
                                e.currentTarget.style.borderColor = '#00d4ff'
                            }
                        }}
                        onMouseOut={(e) => {
                            if (!answered) {
                                e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)'
                                e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)'
                            }
                        }}
                    >
                        {/* Letter Badge */}
                        <div style={{
                            width: '40px',
                            height: '40px',
                            borderRadius: '12px',
                            background: answered && index === correctAnswer
                                ? 'rgba(0, 255, 136, 0.2)'
                                : answered && index === selectedOption
                                    ? 'rgba(239, 68, 68, 0.2)'
                                    : 'rgba(255, 255, 255, 0.1)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontWeight: 700,
                            fontSize: '18px',
                            flexShrink: 0
                        }}>
                            {letters[index]}
                        </div>

                        {/* Option Text */}
                        <span style={{
                            flex: 1,
                            textAlign: 'left',
                            color: 'rgba(255, 255, 255, 0.9)'
                        }}>
                            {option}
                        </span>

                        {/* Status Icon */}
                        {answered && index === correctAnswer && (
                            <CheckCircle2 size={24} style={{ color: '#00ff88', flexShrink: 0 }} />
                        )}
                        {answered && index === selectedOption && index !== correctAnswer && (
                            <XCircle size={24} style={{ color: '#ef4444', flexShrink: 0 }} />
                        )}
                    </button>
                ))}
            </div>

            {/* Explanation */}
            {answered && explanation && (
                <div style={{
                    background: 'rgba(0, 212, 255, 0.1)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(0, 212, 255, 0.3)',
                    borderRadius: '16px',
                    padding: '20px 24px',
                    display: 'flex',
                    gap: '16px',
                    animation: 'slideIn 0.3s ease'
                }}>
                    <style>{`
            @keyframes slideIn {
              from {
                opacity: 0;
                transform: translateY(10px);
              }
              to {
                opacity: 1;
                transform: translateY(0);
              }
            }
          `}</style>
                    <Info size={24} style={{ color: '#00d4ff', flexShrink: 0 }} />
                    <div>
                        <div style={{
                            fontSize: '14px',
                            fontWeight: 600,
                            color: '#00d4ff',
                            marginBottom: '8px'
                        }}>
                            Wyjaśnienie:
                        </div>
                        <p style={{
                            fontSize: '15px',
                            lineHeight: '1.6',
                            color: 'rgba(255, 255, 255, 0.9)'
                        }}>
                            {explanation}
                        </p>
                    </div>
                </div>
            )}
        </div>
    )
}
