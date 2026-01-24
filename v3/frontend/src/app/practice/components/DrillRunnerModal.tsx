import { useState, useEffect } from 'react'
import { X, CheckCircle, AlertCircle, ArrowRight, Play } from 'lucide-react'
import DrillTimer from './DrillTimer'

interface DrillQuestion {
    id: string
    question: string
    options: string[]
    correctIndex: number
    feedback: string
}

export interface DrillData {
    id: string
    drill_id: string
    title: string
    description: string
    drill_type: 'speed_run' | 'analysis' | 'daily'
    questions: DrillQuestion[]
    time_limit_seconds: number
    max_xp: number
}

interface DrillRunnerProps {
    drill: DrillData
    onClose: () => void
    onComplete: (xp: number, score: number) => void
}

type DrillState = 'intro' | 'running' | 'feedback' | 'summary'

export default function DrillRunnerModal({ drill, onClose, onComplete }: DrillRunnerProps) {
    const [state, setState] = useState<DrillState>('intro')
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
    const [selectedOption, setSelectedOption] = useState<number | null>(null)
    const [correctCount, setCorrectCount] = useState(0)
    const [isCorrect, setIsCorrect] = useState(false)
    const [timeUp, setTimeUp] = useState(false)

    const question = drill.questions[currentQuestionIndex]
    const isLastQuestion = currentQuestionIndex === drill.questions.length - 1

    const handleStart = () => {
        setState('running')
    }

    const handleTimeUp = () => {
        setTimeUp(true)
        setState('summary')
    }

    const handleAnswer = (index: number) => {
        if (state !== 'running') return

        setSelectedOption(index)
        const correct = index === question.correctIndex
        setIsCorrect(correct)

        if (correct) {
            setCorrectCount(prev => prev + 1)
        }

        setState('feedback')
    }

    const handleNext = () => {
        if (isLastQuestion) {
            setState('summary')
        } else {
            setCurrentQuestionIndex(prev => prev + 1)
            setSelectedOption(null)
            setState('running')
        }
    }

    const calculateScore = () => {
        if (drill.questions.length === 0) return 0
        return Math.round((correctCount / drill.questions.length) * 100)
    }

    const handleFinish = () => {
        const score = calculateScore()
        const xpEarned = Math.round((score / 100) * drill.max_xp)
        onComplete(xpEarned, score)
    }

    return (
        <div style={{
            position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh',
            background: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(10px)',
            zIndex: 100, display: 'flex', alignItems: 'center', justifyContent: 'center'
        }}>
            <div style={{
                width: '90%', maxWidth: '600px',
                background: '#141423', border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '24px', padding: '32px', position: 'relative',
                boxShadow: '0 20px 50px rgba(0,0,0,0.5)'
            }}>
                <button onClick={onClose} style={{
                    position: 'absolute', top: '24px', right: '24px',
                    background: 'transparent', border: 'none', color: 'rgba(255,255,255,0.4)',
                    cursor: 'pointer'
                }}>
                    <X size={24} />
                </button>

                {state === 'intro' && (
                    <div style={{ textAlign: 'center', padding: '24px 0' }}>
                        <div style={{ width: '80px', height: '80px', background: 'rgba(176, 0, 255, 0.1)', borderRadius: '20px', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 24px auto', color: '#b000ff' }}>
                            <Play size={40} fill="#b000ff" />
                        </div>
                        <h2 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '16px' }}>{drill.title}</h2>
                        <p style={{ color: 'rgba(255,255,255,0.6)', lineHeight: 1.6, marginBottom: '32px' }}>
                            {drill.questions.length} pytań • {drill.time_limit_seconds} sekund na całość.<br />
                            Przygotuj się na szybkie decyzje!
                        </p>
                        <button onClick={handleStart} style={{
                            background: '#b000ff', color: 'white', border: 'none',
                            padding: '16px 48px', borderRadius: '30px', fontSize: '16px', fontWeight: 700,
                            cursor: 'pointer', boxShadow: '0 0 20px rgba(176, 0, 255, 0.4)'
                        }}>
                            Rozpocznij Drill
                        </button>
                    </div>
                )}

                {(state === 'running' || state === 'feedback') && (
                    <div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '24px' }}>
                            <span style={{ fontSize: '12px', fontWeight: 700, color: 'rgba(255,255,255,0.4)', textTransform: 'uppercase' }}>
                                Pytanie {currentQuestionIndex + 1} / {drill.questions.length}
                            </span>
                        </div>

                        <DrillTimer
                            durationSeconds={drill.time_limit_seconds}
                            onTimeUp={handleTimeUp}
                            isActive={state === 'running'}
                        />

                        <h3 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '24px', lineHeight: 1.4 }}>
                            {question ? question.question : 'Błąd ładowania pytania'}
                        </h3>

                        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                            {question && question.options.map((opt, idx) => {
                                let bgColor = 'rgba(255,255,255,0.05)'
                                let borderColor = 'transparent'
                                if (state === 'feedback') {
                                    if (idx === question.correctIndex) {
                                        bgColor = 'rgba(0, 255, 136, 0.15)'
                                        borderColor = '#00ff88'
                                    } else if (idx === selectedOption && idx !== question.correctIndex) {
                                        bgColor = 'rgba(255, 68, 68, 0.15)'
                                        borderColor = '#ff4444'
                                    }
                                }

                                return (
                                    <button
                                        key={idx}
                                        onClick={() => handleAnswer(idx)}
                                        disabled={state === 'feedback'}
                                        style={{
                                            padding: '16px 20px', textAlign: 'left',
                                            background: bgColor,
                                            border: `1px solid ${borderColor === 'transparent' ? 'rgba(255,255,255,0.1)' : borderColor}`,
                                            borderRadius: '12px',
                                            color: 'white', fontSize: '15px',
                                            cursor: state === 'running' ? 'pointer' : 'default',
                                            transition: 'all 0.2s',
                                            display: 'flex', alignItems: 'center', justifyContent: 'space-between'
                                        }}
                                    >
                                        {opt}
                                        {state === 'feedback' && idx === question.correctIndex && <CheckCircle size={20} color="#00ff88" />}
                                        {state === 'feedback' && idx === selectedOption && idx !== question.correctIndex && <X size={20} color="#ff4444" />}
                                    </button>
                                )
                            })}
                        </div>

                        {state === 'feedback' && (
                            <div style={{ marginTop: '24px', padding: '16px', borderRadius: '12px', background: isCorrect ? 'rgba(0, 255, 136, 0.05)' : 'rgba(255, 68, 68, 0.05)', border: `1px solid ${isCorrect ? 'rgba(0, 255, 136, 0.2)' : 'rgba(255, 68, 68, 0.2)'}` }}>
                                <div style={{ fontSize: '13px', fontWeight: 700, color: isCorrect ? '#00ff88' : '#ff4444', marginBottom: '4px' }}>
                                    {isCorrect ? 'Dobrze!' : 'Niepoprawnie'}
                                </div>
                                <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.8)', lineHeight: 1.5, marginBottom: '16px' }}>
                                    {question.feedback}
                                </div>
                                <button onClick={handleNext} style={{
                                    background: 'white', color: 'black', border: 'none',
                                    padding: '10px 24px', borderRadius: '20px', fontWeight: 600, cursor: 'pointer',
                                    display: 'flex', alignItems: 'center', gap: '8px'
                                }}>
                                    {isLastQuestion ? 'Zakończ' : 'Następne'} <ArrowRight size={16} />
                                </button>
                            </div>
                        )}
                    </div>
                )}

                {state === 'summary' && (
                    <div style={{ textAlign: 'center', padding: '24px 0' }}>
                        <div style={{ fontSize: '64px', marginBottom: '16px' }}>
                            {calculateScore() >= 70 ? '🎉' : '🤔'}
                        </div>
                        <h2 style={{ fontSize: '28px', fontWeight: 700, marginBottom: '8px' }}>
                            {timeUp ? 'Czas minął!' : 'Drill Zakończony!'}
                        </h2>
                        <div style={{ fontSize: '48px', fontWeight: 800, color: calculateScore() >= 70 ? '#00ff88' : '#ffd700', marginBottom: '24px' }}>
                            {calculateScore()}%
                        </div>
                        <p style={{ color: 'rgba(255,255,255,0.6)', marginBottom: '32px' }}>
                            Poprawne odpowiedzi: {correctCount} / {drill.questions.length}<br />
                            XP Zdobyte: <span style={{ color: '#ffd700', fontWeight: 700 }}>+{Math.round((calculateScore() / 100) * drill.max_xp)} XP</span>
                        </p>
                        <button onClick={handleFinish} style={{
                            background: '#b000ff', color: 'white', border: 'none',
                            padding: '16px 48px', borderRadius: '30px', fontSize: '16px', fontWeight: 700,
                            cursor: 'pointer'
                        }}>
                            Odbierz Nagrodę i Zamknij
                        </button>
                    </div>
                )}
            </div>
        </div>
    )
}
