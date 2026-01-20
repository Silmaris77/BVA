'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { ChevronLeft, ChevronRight, CheckCircle2, Sparkles, Trophy, ArrowLeft } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface EngramSlide {
    id?: number
    title?: string
    content?: string
    question?: string
    options?: string[]
    correctAnswer?: number
    explanation?: string
    image_url?: string
}

interface QuizItem {
    // Support both full names and shorthand keys
    question?: string
    q?: string
    options?: string[]
    a?: string
    wrong?: string[]
    correctAnswer?: number
    explanation?: string
}

// Helper function to normalize quiz item
function normalizeQuiz(item: QuizItem): { question: string; options: string[]; correctAnswer: number; explanation?: string } {
    const question = item.question || item.q || '';
    let options: string[] = [];
    let correctAnswer = 0;

    if (item.options && typeof item.correctAnswer === 'number') {
        // Full format: options array with correctAnswer index
        options = item.options;
        correctAnswer = item.correctAnswer;
    } else if (item.a && item.wrong) {
        // Shorthand format: a (correct answer) and wrong (array of wrong answers)
        // Randomize position of correct answer
        const wrongAnswers = item.wrong;
        correctAnswer = Math.floor(Math.random() * (wrongAnswers.length + 1));
        options = [...wrongAnswers];
        options.splice(correctAnswer, 0, item.a);
    }

    return { question, options, correctAnswer, explanation: item.explanation };
}

interface EngramData {
    id: string
    engram_id: string
    title: string
    category?: string
    slides: EngramSlide[]
    quiz_pool: QuizItem[]
    install_xp: number
    refresh_xp: number
    installed?: boolean
    strength?: number
}

export default function EngramPlayerPage() {
    const { user } = useAuth()
    const params = useParams()
    const router = useRouter()
    const engramId = params.id as string

    const [engram, setEngram] = useState<EngramData | null>(null)
    const [currentSlide, setCurrentSlide] = useState(0)
    const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
    const [answered, setAnswered] = useState(false)
    const [completed, setCompleted] = useState(false)
    const [loading, setLoading] = useState(true)
    const [correctAnswers, setCorrectAnswers] = useState(0)
    const [totalQuizzes, setTotalQuizzes] = useState(0)
    const [failed, setFailed] = useState(false)
    const [mode, setMode] = useState<'slides' | 'quiz'>('slides')
    const [quizIndex, setQuizIndex] = useState(0)

    const PASS_THRESHOLD = 0.7 // 70% required to pass

    useEffect(() => {
        loadEngram()
    }, [engramId])

    // Keyboard shortcuts
    useEffect(() => {
        const handleKeyPress = (e: KeyboardEvent) => {
            if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return
            if (completed || failed) return

            switch (e.key) {
                case 'ArrowLeft':
                    handlePrevious()
                    break
                case 'ArrowRight':
                    if (mode === 'slides') {
                        handleNext()
                    } else if (answered) {
                        handleNextQuiz()
                    }
                    break
                case 'Escape':
                    router.push('/engrams')
                    break
            }
        }

        window.addEventListener('keydown', handleKeyPress)
        return () => window.removeEventListener('keydown', handleKeyPress)
    }, [currentSlide, answered, completed, failed, engram, mode, quizIndex])

    async function loadEngram() {
        try {
            const response = await fetch(`/api/engrams/${engramId}`)
            const data = await response.json()

            if (data.error) {
                console.error('Error loading engram:', data.error)
                return
            }

            setEngram(data.engram)
        } catch (error) {
            console.error('Error loading engram:', error)
        } finally {
            setLoading(false)
        }
    }

    const handleComplete = async () => {
        // Check if passed quiz
        if (totalQuizzes > 0) {
            const score = correctAnswers / totalQuizzes
            if (score < PASS_THRESHOLD) {
                setFailed(true)
                return
            }
        }

        try {
            const response = await fetch(`/api/engrams/${engramId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    action: 'install',
                    quiz_score: totalQuizzes > 0 ? Math.round((correctAnswers / totalQuizzes) * 100) : 100
                })
            })

            if (response.ok) {
                setCompleted(true)
            }
        } catch (error) {
            console.error('Error completing engram:', error)
        }
    }

    const handleNext = () => {
        if (!engram) return

        if (currentSlide < engram.slides.length - 1) {
            setCurrentSlide(currentSlide + 1)
        } else {
            // Switch to quiz mode if there's a quiz pool
            if (engram.quiz_pool && engram.quiz_pool.length > 0) {
                setMode('quiz')
                setQuizIndex(0)
            } else {
                handleComplete()
            }
        }
    }

    const handlePrevious = () => {
        if (mode === 'quiz') {
            if (quizIndex > 0) {
                setQuizIndex(quizIndex - 1)
                setSelectedAnswer(null)
                setAnswered(false)
            } else {
                setMode('slides')
                setCurrentSlide(engram?.slides.length ? engram.slides.length - 1 : 0)
            }
        } else if (currentSlide > 0) {
            setCurrentSlide(currentSlide - 1)
        }
    }

    const handleAnswerSelect = (index: number) => {
        if (!engram || answered) return
        const currentQuiz = normalizeQuiz(engram.quiz_pool[quizIndex])

        setSelectedAnswer(index)
        setAnswered(true)

        if (index === currentQuiz.correctAnswer) {
            setCorrectAnswers(prev => prev + 1)
        }
        setTotalQuizzes(prev => prev + 1)
    }

    const handleNextQuiz = () => {
        if (!engram) return

        if (quizIndex < engram.quiz_pool.length - 1) {
            setQuizIndex(quizIndex + 1)
            setSelectedAnswer(null)
            setAnswered(false)
        } else {
            handleComplete()
        }
    }

    const handleRetry = () => {
        setCurrentSlide(0)
        setSelectedAnswer(null)
        setAnswered(false)
        setCompleted(false)
        setFailed(false)
        setCorrectAnswers(0)
        setTotalQuizzes(0)
        setMode('slides')
        setQuizIndex(0)
    }

    if (!user) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'rgba(255, 255, 255, 0.6)'
            }}>
                Zaloguj się, aby uczyć się engramów
            </div>
        )
    }

    if (loading) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
            }}>
                <div style={{ color: '#b000ff', fontSize: '18px' }}>Ładowanie...</div>
            </div>
        )
    }

    if (!engram) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexDirection: 'column',
                gap: '16px'
            }}>
                <div style={{ fontSize: '48px' }}>❌</div>
                <div style={{ fontSize: '18px', color: 'rgba(255, 255, 255, 0.7)' }}>
                    Engram nie znaleziony
                </div>
                <button
                    onClick={() => router.push('/engrams')}
                    style={{
                        marginTop: '16px',
                        padding: '12px 24px',
                        background: 'linear-gradient(135deg, #b000ff, #00d4ff)',
                        border: 'none',
                        borderRadius: '12px',
                        color: '#fff',
                        fontSize: '14px',
                        fontWeight: 600,
                        cursor: 'pointer'
                    }}
                >
                    Wróć do katalogu
                </button>
            </div>
        )
    }

    // Check if slides exist
    if (!engram.slides || engram.slides.length === 0) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexDirection: 'column',
                gap: '16px',
                padding: '32px'
            }}>
                <div style={{
                    width: '100px',
                    height: '100px',
                    borderRadius: '50%',
                    background: 'rgba(255, 136, 0, 0.2)',
                    border: '3px solid #ff8800',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '48px'
                }}>
                    🚧
                </div>
                <h2 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '8px' }}>
                    Treść w przygotowaniu
                </h2>
                <p style={{ fontSize: '16px', color: 'rgba(255, 255, 255, 0.7)', textAlign: 'center', maxWidth: '500px' }}>
                    Ten engram jest obecnie w trakcie tworzenia.
                    Sprawdź ponownie wkrótce!
                </p>
                <button
                    onClick={() => router.push('/engrams')}
                    style={{
                        marginTop: '16px',
                        padding: '12px 24px',
                        background: 'linear-gradient(135deg, #b000ff, #00d4ff)',
                        border: 'none',
                        borderRadius: '12px',
                        color: '#fff',
                        fontSize: '14px',
                        fontWeight: 600,
                        cursor: 'pointer',
                        fontFamily: 'Outfit, sans-serif'
                    }}
                >
                    Wróć do katalogu
                </button>
            </div>
        )
    }

    const slides = engram.slides
    const quizPool = engram.quiz_pool || []
    const totalSteps = slides.length + quizPool.length
    const currentStep = mode === 'slides' ? currentSlide + 1 : slides.length + quizIndex + 1
    const progress = (currentStep / totalSteps) * 100
    const scorePercentage = totalQuizzes > 0 ? Math.round((correctAnswers / totalQuizzes) * 100) : 0

    // Failed screen
    if (failed) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '32px'
            }}>
                <div style={{
                    maxWidth: '600px',
                    width: '100%',
                    textAlign: 'center',
                    background: 'rgba(20, 20, 35, 0.6)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255, 136, 0, 0.3)',
                    borderRadius: '24px',
                    padding: '48px 32px'
                }}>
                    <div style={{
                        width: '100px',
                        height: '100px',
                        borderRadius: '50%',
                        background: 'rgba(255, 136, 0, 0.2)',
                        border: '3px solid #ff8800',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        margin: '0 auto 24px',
                        fontSize: '48px'
                    }}>
                        📚
                    </div>

                    <h1 style={{
                        fontSize: '32px',
                        fontWeight: 700,
                        marginBottom: '16px',
                        color: '#ff8800'
                    }}>
                        Powtórz materiał
                    </h1>

                    <p style={{
                        fontSize: '16px',
                        color: 'rgba(255, 255, 255, 0.7)',
                        marginBottom: '24px'
                    }}>
                        Twój wynik to <strong style={{ color: '#ff8800' }}>{scorePercentage}%</strong>.
                        Potrzebujesz minimum <strong>70%</strong> żeby zainstalować engram.
                    </p>

                    <div style={{
                        display: 'flex',
                        gap: '16px',
                        justifyContent: 'center'
                    }}>
                        <button
                            onClick={() => router.push('/engrams')}
                            style={{
                                padding: '14px 32px',
                                background: 'rgba(255, 255, 255, 0.08)',
                                border: '1px solid rgba(255, 255, 255, 0.2)',
                                borderRadius: '12px',
                                color: 'white',
                                fontSize: '15px',
                                fontWeight: 600,
                                cursor: 'pointer',
                                fontFamily: 'Outfit, sans-serif'
                            }}
                        >
                            Wróć do listy
                        </button>
                        <button
                            onClick={handleRetry}
                            style={{
                                padding: '14px 32px',
                                background: 'linear-gradient(135deg, #ff8800, #ffd700)',
                                border: 'none',
                                borderRadius: '12px',
                                color: '#000',
                                fontSize: '15px',
                                fontWeight: 700,
                                cursor: 'pointer',
                                fontFamily: 'Outfit, sans-serif'
                            }}
                        >
                            Spróbuj ponownie
                        </button>
                    </div>
                </div>
            </div>
        )
    }

    // Completed screen
    if (completed) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '32px'
            }}>
                <div style={{
                    maxWidth: '600px',
                    width: '100%',
                    textAlign: 'center',
                    background: 'rgba(20, 20, 35, 0.6)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(0, 255, 136, 0.3)',
                    borderRadius: '24px',
                    padding: '48px 32px'
                }}>
                    <div style={{
                        width: '100px',
                        height: '100px',
                        borderRadius: '50%',
                        background: 'linear-gradient(135deg, #00ff88, #00d4ff)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        margin: '0 auto 24px',
                        boxShadow: '0 0 40px rgba(0, 255, 136, 0.4)'
                    }}>
                        <Trophy size={50} style={{ color: '#000' }} />
                    </div>

                    <h1 style={{
                        fontSize: '32px',
                        fontWeight: 700,
                        marginBottom: '16px',
                        background: 'linear-gradient(135deg, #00ff88, #00d4ff)',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent'
                    }}>
                        Engram zainstalowany!
                    </h1>

                    <p style={{
                        fontSize: '16px',
                        color: 'rgba(255, 255, 255, 0.7)',
                        marginBottom: totalQuizzes > 0 ? '16px' : '32px'
                    }}>
                        {engram.title} został pomyślnie zainstalowany.
                    </p>

                    {totalQuizzes > 0 && (
                        <div style={{
                            fontSize: '15px',
                            color: 'rgba(255, 255, 255, 0.8)',
                            marginBottom: '32px',
                            padding: '12px 20px',
                            background: correctAnswers === totalQuizzes
                                ? 'rgba(0, 255, 136, 0.15)'
                                : 'rgba(255, 136, 0, 0.15)',
                            border: correctAnswers === totalQuizzes
                                ? '1px solid #00ff88'
                                : '1px solid #ff8800',
                            borderRadius: '12px'
                        }}>
                            <strong>Wynik testu:</strong> {correctAnswers}/{totalQuizzes} poprawnych
                            {correctAnswers === totalQuizzes && ' 🎯 Perfekcyjnie!'}
                        </div>
                    )}

                    <div style={{
                        background: 'linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 140, 0, 0.2))',
                        border: '2px solid #ffd700',
                        borderRadius: '16px',
                        padding: '16px 24px',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '12px',
                        marginBottom: '32px'
                    }}>
                        <Sparkles size={24} style={{ color: '#ffd700' }} />
                        <div style={{
                            fontSize: '28px',
                            fontWeight: 800,
                            color: '#ffd700'
                        }}>
                            +{engram.install_xp} XP
                        </div>
                    </div>

                    <div>
                        <button
                            onClick={() => router.push('/engrams')}
                            style={{
                                padding: '14px 32px',
                                background: 'linear-gradient(135deg, #00ff88, #00d4ff)',
                                border: 'none',
                                borderRadius: '12px',
                                color: '#000',
                                fontSize: '15px',
                                fontWeight: 700,
                                cursor: 'pointer',
                                fontFamily: 'Outfit, sans-serif',
                                transition: 'transform 0.2s'
                            }}
                            onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
                            onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
                        >
                            Wróć do engramów
                        </button>
                    </div>
                </div>
            </div>
        )
    }

    // Slide view
    const slide = mode === 'slides' ? slides[currentSlide] : null
    const quiz = mode === 'quiz' && quizPool[quizIndex] ? normalizeQuiz(quizPool[quizIndex]) : null

    return (
        <div style={{
            minHeight: '100vh',
            display: 'flex',
            flexDirection: 'column'
        }}>
            {/* Header with Progress */}
            <div style={{
                background: 'rgba(0, 0, 0, 0.2)',
                backdropFilter: 'blur(20px)',
                borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
                padding: '20px 48px',
                position: 'sticky',
                top: 0,
                zIndex: 50
            }}>
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    marginBottom: '12px'
                }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                        <button
                            onClick={() => router.push('/engrams')}
                            style={{
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                width: '40px',
                                height: '40px',
                                background: 'rgba(255, 255, 255, 0.08)',
                                border: '1px solid rgba(255, 255, 255, 0.1)',
                                borderRadius: '12px',
                                color: 'white',
                                cursor: 'pointer'
                            }}
                        >
                            <ArrowLeft size={20} />
                        </button>
                        <div>
                            <h1 style={{ fontSize: '20px', fontWeight: 700, marginBottom: '4px' }}>
                                {engram.title}
                            </h1>
                            <div style={{ fontSize: '13px', color: 'rgba(255, 255, 255, 0.6)' }}>
                                {mode === 'slides' ? `Slajd ${currentSlide + 1} z ${slides.length}` : `Quiz ${quizIndex + 1} z ${quizPool.length}`}
                            </div>
                        </div>
                    </div>
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        padding: '8px 16px',
                        background: 'rgba(176, 0, 255, 0.15)',
                        border: '1px solid #b000ff',
                        borderRadius: '20px',
                        fontSize: '13px',
                        fontWeight: 600,
                        color: '#b000ff'
                    }}>
                        <Sparkles size={16} />
                        {engram.install_xp} XP
                    </div>
                </div>

                {/* Progress Bar */}
                <div style={{
                    height: '6px',
                    background: 'rgba(255, 255, 255, 0.1)',
                    borderRadius: '3px',
                    overflow: 'hidden'
                }}>
                    <div style={{
                        height: '100%',
                        width: `${progress}%`,
                        background: 'linear-gradient(90deg, #b000ff, #00d4ff)',
                        borderRadius: '3px',
                        transition: 'width 0.3s ease'
                    }} />
                </div>
            </div>

            {/* Content */}
            <div style={{
                flex: 1,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '48px 32px'
            }}>
                <div style={{
                    maxWidth: '800px',
                    width: '100%',
                    background: 'rgba(20, 20, 35, 0.6)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255, 255, 255, 0.08)',
                    borderRadius: '24px',
                    padding: '48px',
                    animation: 'slideIn 0.3s ease'
                }}>
                    <style>{`
                        @keyframes slideIn {
                            from { opacity: 0; transform: translateY(20px); }
                            to { opacity: 1; transform: translateY(0); }
                        }
                    `}</style>

                    {mode === 'slides' && slide && (
                        <>
                            {slide.title && (
                                <h2 style={{
                                    fontSize: '28px',
                                    fontWeight: 700,
                                    marginBottom: '24px',
                                    color: '#00d4ff'
                                }}>
                                    {slide.title}
                                </h2>
                            )}

                            {slide.image_url && (
                                <img
                                    src={slide.image_url}
                                    alt=""
                                    style={{
                                        width: '100%',
                                        maxHeight: '300px',
                                        objectFit: 'contain',
                                        borderRadius: '12px',
                                        marginBottom: '24px'
                                    }}
                                />
                            )}

                            {slide.content && (
                                <div style={{
                                    fontSize: '16px',
                                    lineHeight: '1.8',
                                    color: 'rgba(255, 255, 255, 0.9)'
                                }}>
                                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                        {slide.content}
                                    </ReactMarkdown>
                                </div>
                            )}
                        </>
                    )}

                    {mode === 'quiz' && quiz && (
                        <>
                            <div style={{
                                display: 'inline-block',
                                padding: '6px 14px',
                                background: 'rgba(176, 0, 255, 0.15)',
                                border: '1px solid #b000ff',
                                borderRadius: '20px',
                                fontSize: '12px',
                                fontWeight: 600,
                                color: '#b000ff',
                                marginBottom: '24px'
                            }}>
                                📝 Quiz
                            </div>

                            <div style={{
                                fontSize: '20px',
                                fontWeight: 600,
                                marginBottom: '24px',
                                color: 'white'
                            }}>
                                {quiz.question}
                            </div>

                            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                {quiz.options?.map((option, index) => {
                                    const isCorrect = index === quiz.correctAnswer
                                    const isSelected = index === selectedAnswer

                                    return (
                                        <button
                                            key={index}
                                            onClick={() => handleAnswerSelect(index)}
                                            disabled={answered}
                                            style={{
                                                padding: '16px 20px',
                                                background: answered
                                                    ? isCorrect
                                                        ? 'rgba(0, 255, 136, 0.15)'
                                                        : isSelected
                                                            ? 'rgba(239, 68, 68, 0.15)'
                                                            : 'rgba(255, 255, 255, 0.05)'
                                                    : 'rgba(255, 255, 255, 0.05)',
                                                border: answered
                                                    ? isCorrect
                                                        ? '2px solid #00ff88'
                                                        : isSelected
                                                            ? '2px solid #ef4444'
                                                            : '2px solid rgba(255, 255, 255, 0.1)'
                                                    : '2px solid rgba(255, 255, 255, 0.1)',
                                                borderRadius: '12px',
                                                cursor: answered ? 'default' : 'pointer',
                                                textAlign: 'left',
                                                fontSize: '15px',
                                                color: 'rgba(255, 255, 255, 0.9)',
                                                fontFamily: 'Outfit, sans-serif',
                                                transition: 'all 0.2s',
                                                display: 'flex',
                                                alignItems: 'center',
                                                justifyContent: 'space-between'
                                            }}
                                        >
                                            <span>{option}</span>
                                            {answered && isCorrect && (
                                                <CheckCircle2 size={20} style={{ color: '#00ff88' }} />
                                            )}
                                        </button>
                                    )
                                })}
                            </div>

                            {answered && quiz.explanation && (
                                <div style={{
                                    marginTop: '20px',
                                    padding: '16px 20px',
                                    background: 'rgba(0, 212, 255, 0.1)',
                                    border: '1px solid rgba(0, 212, 255, 0.3)',
                                    borderRadius: '12px',
                                    fontSize: '14px',
                                    lineHeight: '1.6',
                                    color: 'rgba(255, 255, 255, 0.8)'
                                }}>
                                    <strong style={{ color: '#00d4ff' }}>Wyjaśnienie:</strong> {quiz.explanation}
                                </div>
                            )}
                        </>
                    )}
                </div>
            </div>

            {/* Navigation */}
            <div style={{
                background: 'rgba(0, 0, 0, 0.2)',
                backdropFilter: 'blur(20px)',
                borderTop: '1px solid rgba(255, 255, 255, 0.08)',
                padding: '20px 48px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
            }}>
                <button
                    onClick={handlePrevious}
                    disabled={currentSlide === 0 && mode === 'slides'}
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '12px 24px',
                        background: (currentSlide === 0 && mode === 'slides') ? 'rgba(255, 255, 255, 0.03)' : 'rgba(255, 255, 255, 0.08)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '12px',
                        color: (currentSlide === 0 && mode === 'slides') ? 'rgba(255, 255, 255, 0.3)' : 'white',
                        fontSize: '14px',
                        fontWeight: 600,
                        cursor: (currentSlide === 0 && mode === 'slides') ? 'not-allowed' : 'pointer',
                        fontFamily: 'Outfit, sans-serif'
                    }}
                >
                    <ChevronLeft size={20} />
                    Wstecz
                </button>

                <button
                    onClick={mode === 'slides' ? handleNext : handleNextQuiz}
                    disabled={mode === 'quiz' && !answered}
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '12px 24px',
                        background: (mode === 'quiz' && !answered)
                            ? 'rgba(176, 0, 255, 0.1)'
                            : 'linear-gradient(135deg, #b000ff, #00d4ff)',
                        border: 'none',
                        borderRadius: '12px',
                        color: (mode === 'quiz' && !answered) ? 'rgba(255, 255, 255, 0.3)' : '#000',
                        fontSize: '14px',
                        fontWeight: 700,
                        cursor: (mode === 'quiz' && !answered) ? 'not-allowed' : 'pointer',
                        fontFamily: 'Outfit, sans-serif'
                    }}
                >
                    {(mode === 'quiz' && quizIndex === quizPool.length - 1) || (mode === 'slides' && currentSlide === slides.length - 1 && quizPool.length === 0) ? 'Zakończ' : 'Dalej'}
                    <ChevronRight size={20} />
                </button>
            </div>
        </div>
    )
}
