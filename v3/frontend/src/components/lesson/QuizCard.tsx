'use client'

import { useState } from 'react'
import { CheckCircle2, XCircle, Trophy, ArrowRight, RotateCcw } from 'lucide-react'
import confetti from 'canvas-confetti'
import MathRenderer from './math/MathRenderer'

interface QuizQuestion {
    question: string
    options: string[]
    correctAnswer: number
    explanation?: string
}

interface QuizCardProps {
    title: string
    questions: QuizQuestion[]
}

export default function QuizCard({ title, questions = [] }: QuizCardProps) {
    const [currentIndex, setCurrentIndex] = useState(0)
    const [score, setScore] = useState(0)
    const [showResult, setShowResult] = useState(false)
    const [selectedOption, setSelectedOption] = useState<number | null>(null)
    const [isAnswered, setIsAnswered] = useState(false)

    const currentQuestion = questions[currentIndex]
    const letters = ['A', 'B', 'C', 'D']

    // Debug: Log question data to find object in options
    console.log('QuizCard questions:', JSON.stringify(questions, null, 2))
    console.log('Current question correctAnswer:', currentQuestion?.correctAnswer, 'type:', typeof currentQuestion?.correctAnswer)

    const handleAnswer = (index: number) => {
        if (isAnswered) return

        setSelectedOption(index)
        setIsAnswered(true)

        // Compare with type coercion in case correctAnswer is string
        if (index === Number(currentQuestion.correctAnswer)) {
            setScore(prev => prev + 1)
            triggerConfetti()
        }
    }

    const handleNext = () => {
        if (currentIndex < questions.length - 1) {
            setCurrentIndex(prev => prev + 1)
            setSelectedOption(null)
            setIsAnswered(false)
        } else {
            setShowResult(true)
            triggerFinalConfetti()
        }
    }

    const handleRetry = () => {
        setCurrentIndex(0)
        setScore(0)
        setShowResult(false)
        setSelectedOption(null)
        setIsAnswered(false)
    }

    const triggerConfetti = () => {
        confetti({
            particleCount: 50,
            spread: 60,
            origin: { y: 0.7 },
            colors: ['#00ff88', '#ffd700']
        })
    }

    const triggerFinalConfetti = () => {
        const duration = 3000
        const end = Date.now() + duration

        const frame = () => {
            confetti({
                particleCount: 2,
                angle: 60,
                spread: 55,
                origin: { x: 0 },
                colors: ['#DA291C', '#00ff88', '#ffd700']
            })
            confetti({
                particleCount: 2,
                angle: 120,
                spread: 55,
                origin: { x: 1 },
                colors: ['#DA291C', '#00ff88', '#ffd700']
            })

            if (Date.now() < end) {
                requestAnimationFrame(frame)
            }
        }
        frame()
    }

    const getOptionStyle = (index: number) => {
        const correctIdx = Number(currentQuestion.correctAnswer);
        
        const baseStyle = {
            padding: '16px 20px',
            background: 'rgba(255, 255, 255, 0.05)',
            border: '2px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '12px',
            cursor: isAnswered ? 'default' : 'pointer',
            transition: 'all 0.2s',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            fontSize: '16px',
            color: 'white',
            width: '100%',
            textAlign: 'left' as const
        }

        if (!isAnswered) {
            // Hover effect handled via onMouseEnter/Leave in JSX
            return baseStyle
        }

        if (index === correctIdx) {
            return {
                ...baseStyle,
                background: 'rgba(0, 255, 136, 0.15)',
                border: '2px solid #00ff88',
                boxShadow: '0 0 15px rgba(0, 255, 136, 0.2)'
            }
        }

        if (index === selectedOption && index !== correctIdx) {
            return {
                ...baseStyle,
                background: 'rgba(239, 68, 68, 0.15)',
                border: '2px solid #ef4444'
            }
        }

        return {
            ...baseStyle,
            opacity: 0.5
        }
    }

    if (showResult) {
        return (
            <div style={{
                maxWidth: '800px',
                width: '100%',
                background: 'rgba(20, 20, 35, 0.8)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '24px',
                padding: '50px',
                textAlign: 'center',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)'
            }}>
                <div style={{
                    width: '100px',
                    height: '100px',
                    margin: '0 auto 30px',
                    background: 'linear-gradient(135deg, #ffd700, #ff8800)',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    boxShadow: '0 0 40px rgba(255, 215, 0, 0.4)'
                }}>
                    <Trophy size={48} color="#000" />
                </div>

                <h2 style={{
                    fontSize: '32px',
                    fontWeight: 700,
                    marginBottom: '10px',
                    color: '#fff'
                }}>
                    Quiz Zakończony!
                </h2>

                <div style={{
                    fontSize: '18px',
                    color: 'rgba(255, 255, 255, 0.6)',
                    marginBottom: '40px'
                }}>
                    Twój wynik: <span style={{ color: '#ffd700', fontWeight: 700, fontSize: '24px' }}>{score} / {questions.length}</span>
                </div>

                <div style={{
                    display: 'flex',
                    justifyContent: 'center',
                    gap: '20px'
                }}>
                    <button
                        onClick={handleRetry}
                        style={{
                            padding: '12px 24px',
                            background: 'rgba(255, 255, 255, 0.1)',
                            border: '1px solid rgba(255, 255, 255, 0.2)',
                            borderRadius: '12px',
                            color: '#fff',
                            fontSize: '16px',
                            fontWeight: 600,
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px'
                        }}
                    >
                        <RotateCcw size={20} />
                        Spróbuj Ponownie
                    </button>
                    {/* User would typically proceed automatically or via lesson nav, but this confirms completion */}
                </div>
            </div>
        )
    }

    if (!currentQuestion) return null

    return (
        <div style={{
            maxWidth: '800px',
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            gap: '24px'
        }}>
            {/* Header */}
            <div style={{
                display: 'flex',
                justifyContent: 'flex-end',
                alignItems: 'center'
            }}>
                <div style={{
                    fontSize: '14px',
                    color: 'rgba(255, 255, 255, 0.5)'
                }}>
                    Wynik: {score}
                </div>
            </div>

            {/* Question Card */}
            <div style={{
                background: 'rgba(20, 20, 35, 0.6)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '20px',
                padding: '40px',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
                position: 'relative',
                borderLeft: '4px solid #b000ff'
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
                    color: '#b000ff',
                    fontWeight: 600,
                    padding: '6px 12px',
                    background: 'rgba(176, 0, 255, 0.1)',
                    border: '1px solid rgba(176, 0, 255, 0.2)',
                    borderRadius: '20px'
                }}>
                    QUIZ
                </div>
                <h3 style={{
                    fontSize: '22px',
                    fontWeight: 600,
                    marginBottom: '30px',
                    marginTop: '20px', // Added top margin
                    color: '#fff',
                    lineHeight: '1.4'
                }}>
                    <MathRenderer content={currentQuestion.question} inline={true} />
                </h3>

                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '12px'
                }}>
                    {currentQuestion.options.map((option, index) => {
                        // Handle case where option might be an object instead of string
                        const optionText = typeof option === 'string' 
                            ? option 
                            : (option as any)?.text || (option as any)?.label || JSON.stringify(option);
                        
                        const correctIdx = Number(currentQuestion.correctAnswer);
                        
                        return (
                        <button
                            key={index}
                            onClick={() => handleAnswer(index)}
                            style={getOptionStyle(index)}
                            disabled={isAnswered}
                        >
                            <div style={{
                                width: '32px',
                                height: '32px',
                                borderRadius: '8px',
                                background: isAnswered && index === correctIdx
                                    ? 'rgba(0, 255, 136, 0.2)'
                                    : isAnswered && index === selectedOption
                                        ? 'rgba(239, 68, 68, 0.2)'
                                        : 'rgba(255, 255, 255, 0.1)',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontWeight: 700,
                                fontSize: '14px',
                                flexShrink: 0
                            }}>
                                {letters[index]}
                            </div>
                            <span style={{ flex: 1, textAlign: 'left' }}>
                                <MathRenderer content={optionText} inline={true} />
                            </span>
                            {isAnswered && index === correctIdx && (
                                <CheckCircle2 size={20} color="#00ff88" />
                            )}
                            {isAnswered && index === selectedOption && index !== correctIdx && (
                                <XCircle size={20} color="#ef4444" />
                            )}
                        </button>
                    )})}
                </div>

                {isAnswered && (
                    <div style={{
                        marginTop: '30px',
                        paddingTop: '20px',
                        borderTop: '1px solid rgba(255, 255, 255, 0.1)',
                        animation: 'fadeIn 0.3s ease'
                    }}>
                        <style>{`@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }`}</style>

                        {currentQuestion.explanation && (
                            <div style={{
                                fontSize: '14px',
                                color: 'rgba(255, 255, 255, 0.8)',
                                marginBottom: '20px',
                                lineHeight: '1.6',
                                background: 'rgba(255, 255, 255, 0.03)',
                                padding: '15px',
                                borderRadius: '12px'
                            }}>
                                <strong style={{ color: '#00d4ff', display: 'block', marginBottom: '5px' }}>Wyjaśnienie:</strong>
                                <MathRenderer content={currentQuestion.explanation} />
                            </div>
                        )}

                        <button
                            onClick={handleNext}
                            style={{
                                width: '100%',
                                padding: '14px',
                                background: 'linear-gradient(135deg, #b000ff, #00d4ff)',
                                border: 'none',
                                borderRadius: '12px',
                                color: '#fff',
                                fontWeight: 700,
                                fontSize: '16px',
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                gap: '8px',
                                boxShadow: '0 8px 20px rgba(176, 0, 255, 0.3)'
                            }}
                        >
                            {currentIndex < questions.length - 1 ? 'Następne Pytanie' : 'Zakończ Quiz'}
                            <ArrowRight size={20} />
                        </button>
                    </div>
                )}
            </div>
        </div>
    )
}
