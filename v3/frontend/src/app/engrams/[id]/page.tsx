'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { supabase } from '@/lib/supabase'
import { ChevronLeft, ChevronRight, CheckCircle2, Sparkles, Trophy } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { updateUserStats } from '@/lib/rpg-stats'

interface EngramSlide {
    id: number
    type: 'intro' | 'content' | 'quiz' | 'summary'
    title?: string
    content?: string
    question?: string
    options?: string[]
    correctAnswer?: number
    explanation?: string
}

interface EngramData {
    id: string
    title: string
    category: string
    description: string
    xp_reward: number
    estimated_minutes: number
    content_json: {
        slides: EngramSlide[]
    }
}

export default function EngramPlayerPage() {
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

    const PASS_THRESHOLD = 0.7 // 70% required to pass

    useEffect(() => {
        loadEngram()
    }, [engramId])

    // Keyboard shortcuts (Arrow Left/Right, Escape)
    useEffect(() => {
        const handleKeyPress = (e: KeyboardEvent) => {
            // Don't trigger if user is typing
            if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
                return
            }

            // Don't allow navigation on completion screens
            if (completed || failed) return

            switch (e.key) {
                case 'ArrowLeft':
                    handlePrevious()
                    break
                case 'ArrowRight':
                    // Only allow next if answered quiz or not on quiz slide
                    if (answered || !engram?.content_json.slides[currentSlide]?.question) {
                        handleNext()
                    }
                    break
                case 'Escape':
                    router.push('/engrams')
                    break
            }
        }

        window.addEventListener('keydown', handleKeyPress)
        return () => window.removeEventListener('keydown', handleKeyPress)
    }, [currentSlide, answered, completed, failed, engram])

    async function loadEngram() {
        try {
            const { data, error } = await supabase
                .from('engrams')
                .select('*')
                .eq('id', engramId)
                .single()

            if (error) throw error
            setEngram(data)
        } catch (error) {
            console.error('Error loading engram:', error)
        } finally {
            setLoading(false)
        }
    }

    const handleComplete = async () => {
        // Check if passed
        if (totalQuizzes > 0) {
            const score = correctAnswers / totalQuizzes
            if (score < PASS_THRESHOLD) {
                setFailed(true)
                return
            }
        }

        try {
            const { data: { user } } = await supabase.auth.getUser()
            if (!user) return


            // Save to user_engrams
            await supabase.from('user_engrams').upsert({
                user_id: user.id,
                engram_id: engramId,
                installed_at: new Date().toISOString(),
                strength: 100,
                status: 'active'
            })

            // 🎮 Update RPG stats (points, classes, combos)
            await updateUserStats(user.id, engramId)

            setCompleted(true)
        } catch (error) {
            console.error('Error completing engram:', error)
        }
    }

    const handleNext = () => {
        if (!engram) return
        const slides = engram.content_json.slides

        if (currentSlide < slides.length - 1) {
            setCurrentSlide(currentSlide + 1)
            setSelectedAnswer(null)
            setAnswered(false)
        } else {
            handleComplete()
        }
    }

    const handlePrevious = () => {
        if (currentSlide > 0) {
            setCurrentSlide(currentSlide - 1)
            setSelectedAnswer(null)
            setAnswered(false)
        }
    }

    const handleAnswerSelect = (index: number) => {
        if (!engram) return
        const slides = engram.content_json.slides
        const currentQuiz = slides[currentSlide]

        setSelectedAnswer(index)
        setAnswered(true)

        // Track correct answer
        if (index === currentQuiz.correctAnswer) {
            setCorrectAnswers(prev => prev + 1)
        }
        setTotalQuizzes(prev => prev + 1)
    }

    const handleRetry = () => {
        setCurrentSlide(0)
        setSelectedAnswer(null)
        setAnswered(false)
        setCompleted(false)
        setFailed(false)
        setCorrectAnswers(0)
        setTotalQuizzes(0)
    }

    if (loading) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
            }}>
                <div style={{ color: '#b000ff', fontSize: '18px' }}>Loading...</div>
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
                    Engram not found
                </div>
            </div>
        )
    }

    // Check if slides exist and are not empty
    if (!engram.content_json?.slides || engram.content_json.slides.length === 0) {
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
                    Content Not Available
                </h2>
                <p style={{ fontSize: '16px', color: 'rgba(255, 255, 255, 0.7)', textAlign: 'center', maxWidth: '500px' }}>
                    This engram is currently a placeholder and doesn't have content yet.
                    Check back soon!
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
                    Back to Catalog
                </button>
            </div>
        )
    }

    const slides = engram.content_json.slides
    const slide = slides[currentSlide]
    const progress = ((currentSlide + 1) / slides.length) * 100
    const scorePercentage = totalQuizzes > 0 ? Math.round((correctAnswers / totalQuizzes) * 100) : 0

    // Failed screen - didn't meet pass threshold
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
                        Review Required
                    </h1>

                    <p style={{
                        fontSize: '16px',
                        color: 'rgba(255, 255, 255, 0.7)',
                        marginBottom: '24px'
                    }}>
                        Your quiz score was <strong style={{ color: '#ff8800' }}>{scorePercentage}%</strong>.
                        You need at least <strong>70%</strong> to install this engram.
                    </p>

                    <div style={{
                        background: 'rgba(0, 212, 255, 0.1)',
                        border: '1px solid rgba(0, 212, 255, 0.3)',
                        borderRadius: '16px',
                        padding: '20px',
                        marginBottom: '32px',
                        textAlign: 'left'
                    }}>
                        <div style={{
                            fontSize: '14px',
                            fontWeight: 600,
                            color: '#00d4ff',
                            marginBottom: '12px'
                        }}>
                            💡 Recommendation:
                        </div>
                        <ul style={{
                            margin: 0,
                            paddingLeft: '20px',
                            fontSize: '14px',
                            lineHeight: '1.6',
                            color: 'rgba(255, 255, 255, 0.8)'
                        }}>
                            <li>Review the content slides again carefully</li>
                            <li>Pay special attention to key concepts</li>
                            <li>Take your time with quiz questions</li>
                            <li>Try the engram again when ready</li>
                        </ul>
                    </div>

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
                                fontFamily: 'Outfit, sans-serif',
                                transition: 'all 0.2s'
                            }}
                            onMouseOver={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.12)'}
                            onMouseOut={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.08)'}
                        >
                            Back to List
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
                                fontFamily: 'Outfit, sans-serif',
                                transition: 'transform 0.2s'
                            }}
                            onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
                            onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
                        >
                            Review & Try Again
                        </button>
                    </div>
                </div>
            </div>
        )
    }

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
                        Engram Installed!
                    </h1>

                    <p style={{
                        fontSize: '16px',
                        color: 'rgba(255, 255, 255, 0.7)',
                        marginBottom: totalQuizzes > 0 ? '16px' : '32px'
                    }}>
                        {engram.title} has been successfully installed to your neural matrix.
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
                            <strong>Quiz Score:</strong> {correctAnswers}/{totalQuizzes} correct
                            {correctAnswers === totalQuizzes && ' 🎯 Perfect!'}
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
                            +{engram.xp_reward} XP
                        </div>
                    </div>

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
                        Back to Engrams
                    </button>
                </div>
            </div>
        )
    }

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
                    <div>
                        <h1 style={{ fontSize: '20px', fontWeight: 700, marginBottom: '4px' }}>
                            {engram.title}
                        </h1>
                        <div style={{ fontSize: '13px', color: 'rgba(255, 255, 255, 0.6)' }}>
                            Slide {currentSlide + 1} of {slides.length}
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
                        {engram.xp_reward} XP
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

                {/* Progress Dots */}
                <div style={{
                    display: 'flex',
                    gap: '8px',
                    marginTop: '16px',
                    justifyContent: 'center'
                }}>
                    {slides.map((_, index) => (
                        <div
                            key={index}
                            style={{
                                width: '8px',
                                height: '8px',
                                borderRadius: '50%',
                                background: index <= currentSlide
                                    ? 'linear-gradient(135deg, #b000ff, #00d4ff)'
                                    : 'rgba(255, 255, 255, 0.2)',
                                transition: 'all 0.3s'
                            }}
                        />
                    ))}
                </div>
            </div>

            {/* Slide Content */}
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
                            from {
                                opacity: 0;
                                transform: translateY(20px);
                            }
                            to {
                                opacity: 1;
                                transform: translateY(0);
                            }
                        }
                    `}</style>

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

                    {slide.content && (
                        <div style={{
                            fontSize: '16px',
                            lineHeight: '1.8',
                            color: 'rgba(255, 255, 255, 0.9)',
                            marginBottom: slide.question ? '32px' : '0'
                        }}>
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                {slide.content}
                            </ReactMarkdown>
                        </div>
                    )}

                    {slide.question && (
                        <div>
                            <div style={{
                                fontSize: '18px',
                                fontWeight: 600,
                                marginBottom: '20px',
                                color: 'white'
                            }}>
                                {slide.question}
                            </div>

                            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                {slide.options?.map((option, index) => {
                                    const isCorrect = index === slide.correctAnswer
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

                            {answered && slide.explanation && (
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
                                    <strong style={{ color: '#00d4ff' }}>Explanation:</strong> {slide.explanation}
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>

            {/* Navigation Controls */}
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
                    disabled={currentSlide === 0}
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '12px 24px',
                        background: currentSlide === 0 ? 'rgba(255, 255, 255, 0.03)' : 'rgba(255, 255, 255, 0.08)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '12px',
                        color: currentSlide === 0 ? 'rgba(255, 255, 255, 0.3)' : 'white',
                        fontSize: '14px',
                        fontWeight: 600,
                        cursor: currentSlide === 0 ? 'not-allowed' : 'pointer',
                        fontFamily: 'Outfit, sans-serif',
                        transition: 'all 0.2s'
                    }}
                >
                    <ChevronLeft size={20} />
                    Previous
                </button>

                <button
                    onClick={handleNext}
                    disabled={slide.type === 'quiz' && !answered}
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '12px 24px',
                        background: (slide.type === 'quiz' && !answered)
                            ? 'rgba(176, 0, 255, 0.1)'
                            : 'linear-gradient(135deg, #b000ff, #00d4ff)',
                        border: 'none',
                        borderRadius: '12px',
                        color: (slide.type === 'quiz' && !answered) ? 'rgba(255, 255, 255, 0.3)' : '#000',
                        fontSize: '14px',
                        fontWeight: 700,
                        cursor: (slide.type === 'quiz' && !answered) ? 'not-allowed' : 'pointer',
                        fontFamily: 'Outfit, sans-serif',
                        transition: 'all 0.2s'
                    }}
                >
                    {currentSlide === slides.length - 1 ? 'Complete' : 'Next'}
                    <ChevronRight size={20} />
                </button>
            </div>
        </div>
    )
}
