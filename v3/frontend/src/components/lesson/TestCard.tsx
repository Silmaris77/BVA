'use client'

import { useState, useEffect, useRef } from 'react'
import { CheckCircle2, XCircle, Trophy, ArrowRight, RotateCcw, Timer, AlertCircle } from 'lucide-react'
import confetti from 'canvas-confetti'

interface QuizQuestion {
    question: string
    options: string[]
    correctAnswer: number
    explanation?: string
}

interface TestCardProps {
    title: string
    questions: QuizQuestion[]
    onTestResult: (score: number, passed: boolean) => void
    onReset?: () => void
}

export default function TestCard({ title, questions = [], onTestResult, onReset }: TestCardProps) {
    // Mode: 'start' | 'test' | 'result'
    const [mode, setMode] = useState<'start' | 'test' | 'result'>('start')

    // Test State
    const [currentIndex, setCurrentIndex] = useState(0)
    const [score, setScore] = useState(0)
    const [userAnswers, setUserAnswers] = useState<(number | null)[]>([])
    const [isAnswered, setIsAnswered] = useState(false)
    const [selectedOption, setSelectedOption] = useState<number | null>(null)

    // Timer State
    const SECONDS_PER_QUESTION = 15
    const totalTime = questions.length * SECONDS_PER_QUESTION
    const [timeLeft, setTimeLeft] = useState(totalTime)
    const timerRef = useRef<NodeJS.Timeout | null>(null)

    const PASS_THRESHOLD = 0.8 // 80%

    // Start Timer when entering test mode
    useEffect(() => {
        if (mode === 'test') {
            timerRef.current = setInterval(() => {
                setTimeLeft((prev) => {
                    if (prev <= 1) {
                        finishTest(true) // Timeout
                        return 0
                    }
                    return prev - 1
                })
            }, 1000)
        }
        return () => {
            if (timerRef.current) clearInterval(timerRef.current)
        }
    }, [mode])

    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60)
        const secs = seconds % 60
        return `${mins}:${secs.toString().padStart(2, '0')}`
    }

    const finishTest = (isTimeout: boolean = false) => {
        if (timerRef.current) clearInterval(timerRef.current)

        // Calculate final score
        // We need to account for the current question if it wasn't answered
        let finalScore = score

        // If timed out, current and remaining questions are wrong (score doesn't increase)

        const passedRate = finalScore / questions.length
        const passed = passedRate >= PASS_THRESHOLD

        setMode('result')

        if (passed) {
            triggerConfetti()
        }

        // Report result to parent
        onTestResult(finalScore, passed)
    }

    const handleStart = () => {
        setMode('test')
        setTimeLeft(totalTime)
        setCurrentIndex(0)
        setScore(0)
        setUserAnswers(new Array(questions.length).fill(null))
    }

    const handleAnswer = (index: number) => {
        if (isAnswered) return

        setSelectedOption(index)
        setIsAnswered(true)

        // Store answer
        const newAnswers = [...userAnswers]
        newAnswers[currentIndex] = index
        setUserAnswers(newAnswers)

        const currentQuestion = questions[currentIndex]
        if (index === currentQuestion.correctAnswer) {
            setScore(prev => prev + 1)
        }
    }

    const handleNext = () => {
        if (currentIndex < questions.length - 1) {
            setCurrentIndex(prev => prev + 1)
            setSelectedOption(null)
            setIsAnswered(false)
        } else {
            finishTest(false)
        }
    }

    const triggerConfetti = () => {
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

    // --- RENDERERS ---

    if (mode === 'start') {
        return (
            <div style={{
                maxWidth: '600px',
                width: '100%',
                background: 'rgba(20, 20, 35, 0.8)',
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '24px',
                padding: '40px',
                textAlign: 'center',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)'
            }}>
                <div style={{
                    width: '80px',
                    height: '80px',
                    margin: '0 auto 24px',
                    background: 'rgba(176, 0, 255, 0.1)',
                    borderRadius: '20px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    border: '1px solid rgba(176, 0, 255, 0.2)'
                }}>
                    <Trophy size={40} color="#b000ff" />
                </div>

                <h2 style={{ fontSize: '28px', fontWeight: 700, marginBottom: '12px', color: 'white' }}>
                    Sprawdź Wiedzę: {title}
                </h2>

                <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '16px', marginBottom: '32px', lineHeight: '1.6' }}>
                    To jest test zaliczający lekcję. Musisz uzyskać minimum <strong style={{ color: '#00ff88' }}>80%</strong> poprawnych odpowiedzi, aby kontynuować.<br />
                    Masz ograniczony czas!
                </p>

                <div style={{
                    display: 'flex',
                    justifyContent: 'center',
                    gap: '24px',
                    marginBottom: '32px'
                }}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                        <span style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.4)', textTransform: 'uppercase' }}>Pytania</span>
                        <span style={{ fontSize: '20px', fontWeight: 700, color: 'white' }}>{questions.length}</span>
                    </div>
                    <div style={{ width: '1px', background: 'rgba(255, 255, 255, 0.1)' }} />
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                        <span style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.4)', textTransform: 'uppercase' }}>Czas</span>
                        <span style={{ fontSize: '20px', fontWeight: 700, color: 'white' }}>{formatTime(totalTime)}</span>
                    </div>
                    <div style={{ width: '1px', background: 'rgba(255, 255, 255, 0.1)' }} />
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                        <span style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.4)', textTransform: 'uppercase' }}>Próg</span>
                        <span style={{ fontSize: '20px', fontWeight: 700, color: '#00ff88' }}>80%</span>
                    </div>
                </div>

                <button
                    onClick={handleStart}
                    style={{
                        padding: '16px 32px',
                        background: 'linear-gradient(135deg, #b000ff, #00d4ff)',
                        border: 'none',
                        borderRadius: '12px',
                        color: 'white',
                        fontSize: '16px',
                        fontWeight: 700,
                        cursor: 'pointer',
                        boxShadow: '0 8px 20px rgba(176, 0, 255, 0.3)',
                        transition: 'transform 0.2s',
                        width: '100%'
                    }}
                    onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.02)'}
                    onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}
                >
                    Rozpocznij Test
                </button>
            </div>
        )
    }

    const currentQuestion = questions[currentIndex]
    const letters = ['A', 'B', 'C', 'D']

    if (mode === 'test') {
        const progress = ((currentIndex) / questions.length) * 100

        return (
            <div style={{
                maxWidth: '800px',
                width: '100%',
                display: 'flex',
                flexDirection: 'column',
                gap: '24px'
            }}>
                {/* Header Bar */}
                <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    background: 'rgba(20, 20, 35, 0.4)',
                    padding: '12px 20px',
                    borderRadius: '16px',
                    border: '1px solid rgba(255, 255, 255, 0.05)'
                }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <div style={{
                            fontSize: '12px',
                            fontWeight: 700,
                            color: '#b000ff',
                            textTransform: 'uppercase',
                            background: 'rgba(176, 0, 255, 0.1)',
                            padding: '4px 8px',
                            borderRadius: '6px'
                        }}>
                            PYTANIE {currentIndex + 1} / {questions.length}
                        </div>
                        <div style={{
                            width: '100px',
                            height: '6px',
                            background: 'rgba(255, 255, 255, 0.1)',
                            borderRadius: '3px',
                            overflow: 'hidden'
                        }}>
                            <div style={{
                                width: `${progress}%`,
                                height: '100%',
                                background: '#b000ff',
                                transition: 'width 0.3s'
                            }} />
                        </div>
                    </div>

                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        color: timeLeft < 30 ? '#ef4444' : 'white',
                        fontWeight: 700,
                        fontVariantNumeric: 'tabular-nums'
                    }}>
                        <Timer size={18} />
                        {formatTime(timeLeft)}
                    </div>
                </div>

                {/* Question Card */}
                <div style={{
                    background: 'rgba(20, 20, 35, 0.6)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '20px',
                    padding: '40px',
                    boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)'
                }}>
                    <h3 style={{
                        fontSize: '22px',
                        fontWeight: 600,
                        marginBottom: '30px',
                        color: '#fff',
                        lineHeight: '1.4'
                    }}>
                        {currentQuestion.question}
                    </h3>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                        {currentQuestion.options.map((option, index) => (
                            <button
                                key={index}
                                onClick={() => handleAnswer(index)}
                                disabled={isAnswered}
                                style={{
                                    padding: '16px 20px',
                                    background: isAnswered && index === selectedOption
                                        ? (index === currentQuestion.correctAnswer ? 'rgba(0, 255, 136, 0.15)' : 'rgba(239, 68, 68, 0.15)')
                                        : 'rgba(255, 255, 255, 0.05)',
                                    border: isAnswered && index === selectedOption
                                        ? (index === currentQuestion.correctAnswer ? '2px solid #00ff88' : '2px solid #ef4444')
                                        : '2px solid rgba(255, 255, 255, 0.1)',
                                    borderRadius: '12px',
                                    cursor: isAnswered ? 'default' : 'pointer',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '12px',
                                    fontSize: '16px',
                                    color: isAnswered && index !== selectedOption ? 'rgba(255,255,255,0.4)' : 'white',
                                    opacity: isAnswered && index !== selectedOption ? 0.6 : 1,
                                    width: '100%',
                                    textAlign: 'left',
                                    transition: 'all 0.2s'
                                }}
                            >
                                <div style={{
                                    width: '32px', height: '32px', borderRadius: '8px',
                                    background: 'rgba(255, 255, 255, 0.1)',
                                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                                    fontWeight: 700, fontSize: '14px', flexShrink: 0
                                }}>
                                    {letters[index]}
                                </div>
                                <span style={{ flex: 1 }}>{option}</span>
                                {isAnswered && index === selectedOption && (
                                    index === currentQuestion.correctAnswer
                                        ? <CheckCircle2 size={20} color="#00ff88" />
                                        : <XCircle size={20} color="#ef4444" />
                                )}
                            </button>
                        ))}
                    </div>

                    {isAnswered && (
                        <div style={{ marginTop: '30px', paddingTop: '20px', borderTop: '1px solid rgba(255, 255, 255, 0.1)', animation: 'fadeIn 0.3s ease' }}>
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
                                    gap: '8px'
                                }}
                            >
                                {currentIndex < questions.length - 1 ? 'Następne Pytanie' : 'Zakończ Test'}
                                <ArrowRight size={20} />
                            </button>
                        </div>
                    )}
                </div>
            </div>
        )
    }

    // Result Mode
    const passed = score / questions.length >= PASS_THRESHOLD

    return (
        <div style={{
            maxWidth: '600px',
            width: '100%',
            background: 'rgba(20, 20, 35, 0.8)',
            backdropFilter: 'blur(20px)',
            border: passed ? '1px solid #00ff88' : '1px solid #ef4444',
            borderRadius: '24px',
            padding: '50px',
            textAlign: 'center',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)'
        }}>
            <div style={{
                width: '100px',
                height: '100px',
                margin: '0 auto 30px',
                background: passed ? 'rgba(0, 255, 136, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: passed ? '0 0 40px rgba(0, 255, 136, 0.2)' : '0 0 40px rgba(239, 68, 68, 0.2)'
            }}>
                {passed ? <Trophy size={48} color="#00ff88" /> : <AlertCircle size={48} color="#ef4444" />}
            </div>

            <h2 style={{ fontSize: '32px', fontWeight: 700, marginBottom: '10px', color: 'white' }}>
                {passed ? 'Gratulacje!' : 'Test Niezaliczony'}
            </h2>

            <div style={{ fontSize: '18px', color: 'rgba(255, 255, 255, 0.6)', marginBottom: '40px' }}>
                Twój wynik: <span style={{ color: passed ? '#00ff88' : '#ef4444', fontWeight: 700, fontSize: '24px' }}>
                    {Math.round((score / questions.length) * 100)}%
                </span>
                <div style={{ fontSize: '14px', marginTop: '8px' }}>
                    Wymagane: 80%
                </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'center', gap: '20px' }}>
                {!passed && (
                    <button
                        className='nav-btn-fail'
                        onClick={() => onReset && onReset()}
                        style={{
                            padding: '12px 24px',
                            background: '#ef4444',
                            border: 'none',
                            borderRadius: '12px',
                            color: 'white',
                            fontWeight: 600,
                            cursor: onReset ? 'pointer' : 'default',
                            opacity: 0.8,
                            pointerEvents: onReset ? 'auto' : 'none'
                        }}
                    >
                        Musisz powtórzyć lekcję
                    </button>
                )}
                {passed && (
                    <div style={{ color: '#00ff88', fontWeight: 600 }}>
                        Lekcja odblokowana. Kliknij "Zakończ" na dole ekranu.
                    </div>
                )}
            </div>
        </div>
    )
}
