'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState, useRef } from 'react'
import { useParams, useRouter } from 'next/navigation'
import CardRenderer from '@/components/lesson/CardRenderer'
import LessonSidebar from '@/components/LessonSidebar'
import { X, ChevronLeft, ChevronRight, Menu } from 'lucide-react'
import Toast from '@/components/Toast'

interface Card {
    type: 'intro' | 'concept' | 'question' | 'summary'
    [key: string]: any
}

interface Lesson {
    lesson_id: string
    title: string
    subtitle?: string
    estimated_duration?: number
    xp_reward: number
    content: {
        cards: Card[]
    }
}

export default function LessonPlayerPage() {
    const { user, profile } = useAuth()
    const params = useParams()
    const router = useRouter()
    const lessonId = params.id as string

    const [lesson, setLesson] = useState<Lesson | null>(null)
    const [cards, setCards] = useState<Card[]>([])
    const [currentCardIndex, setCurrentCardIndex] = useState(0)
    const [completedCards, setCompletedCards] = useState<number[]>([])
    const [loading, setLoading] = useState(true)
    const [showExitModal, setShowExitModal] = useState(false)
    const [toast, setToast] = useState<string | null>(null)
    const [direction, setDirection] = useState<'left' | 'right'>('right')
    const [drawerOpen, setDrawerOpen] = useState(false)
    const contentAreaRef = useRef<HTMLDivElement>(null)

    // Scroll to top when card changes
    useEffect(() => {
        if (contentAreaRef.current) {
            contentAreaRef.current.scrollTo({ top: 0, behavior: 'smooth' })
        }
        // Also scroll window for mobile
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }, [currentCardIndex])

    useEffect(() => {
        async function loadLesson() {
            try {
                // Fetch from API endpoint
                const response = await fetch(`/api/lessons/${lessonId}`)
                const data = await response.json()

                if (data.lesson) {
                    setLesson(data.lesson)
                    setCards(data.lesson.content?.cards || [])

                    // Resume from saved progress if exists
                    if (data.progress && !data.progress.completed_at) {
                        setCurrentCardIndex(data.progress.current_card_index || 0)
                    } else if (!data.progress && user) {
                        // Auto-start lesson if not started yet
                        const startResponse = await fetch(`/api/lessons/${lessonId}`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ action: 'start' })
                        })
                        if (startResponse.ok) {
                            console.log('Lesson started automatically')
                        }
                    }
                }
            } catch (error) {
                console.error('Error loading lesson:', error)
            } finally {
                setLoading(false)
            }
        }

        if (user) {
            loadLesson()
        }
    }, [lessonId, user])


    const saveProgress = async (cardIndex: number) => {
        if (!user) return
        try {
            // Save current card progress to API
            await fetch(`/api/lessons/${lessonId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    action: 'progress',
                    current_card: cardIndex
                })
            })
        } catch (error) {
            console.error('Error saving progress:', error)
        }
    }

    const completeLesson = async () => {
        if (!user || !lesson) return

        try {
            // Complete lesson via API (awards XP automatically)
            const response = await fetch(`/api/lessons/${lessonId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'complete' })
            })

            const data = await response.json()

            if (data.success) {
                setToast(`Ukończono lekcję! +${lesson.xp_reward} XP`)
            }
        } catch (error) {
            console.error('Error completing lesson:', error)
        }
    }

    const handleNext = async () => {
        if (currentCardIndex < cards.length - 1) {
            setDirection('right')
            const newIndex = currentCardIndex + 1
            setCurrentCardIndex(newIndex)
            await saveProgress(newIndex)
        } else {
            // Last card - complete lesson
            await completeLesson()
            router.push('/lessons')
        }
    }

    const handlePrevious = () => {
        if (currentCardIndex > 0) {
            setDirection('left')
            setCurrentCardIndex(currentCardIndex - 1)
        }
    }

    const handleExit = async () => {
        await saveProgress(currentCardIndex)
        router.push('/lessons')
    }

    // Keyboard navigation
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            // Prevent if typing in input
            if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return

            switch (e.key) {
                case 'ArrowLeft':
                    e.preventDefault()
                    handlePrevious()
                    break
                case 'ArrowRight':
                    e.preventDefault()
                    handleNext()
                    break
                case 'Escape':
                    e.preventDefault()
                    setShowExitModal(true)
                    break
            }
        }

        window.addEventListener('keydown', handleKeyDown)
        return () => window.removeEventListener('keydown', handleKeyDown)
    }, [currentCardIndex, cards.length])

    if (!user) return null

    if (loading) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
            }}>
                Ładowanie lekcji...
            </div>
        )
    }

    if (!lesson || cards.length === 0) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '16px'
            }}>
                <p>Lekcja nie znaleziona lub brak zawartości</p>
                <button
                    onClick={() => router.push('/lessons')}
                    style={{
                        padding: '12px 24px',
                        background: '#00d4ff',
                        border: 'none',
                        borderRadius: '12px',
                        color: '#000',
                        fontWeight: 600,
                        cursor: 'pointer'
                    }}
                >
                    Wróć do lekcji
                </button>
            </div>
        )
    }

    const currentCard = cards[currentCardIndex]
    const progress = ((currentCardIndex + 1) / cards.length) * 100

    return (
        <div style={{
            height: '100vh',
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden'
        }}>
            {/* Top Bar - Full Width */}
            <div style={{
                background: 'rgba(0, 0, 0, 0.3)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
                padding: '16px 32px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                position: 'sticky',
                top: 0,
                zIndex: 100
            }}>
                {/* Hamburger Button (Mobile Only) */}
                <button
                    className="hamburger-btn"
                    onClick={() => setDrawerOpen(true)}
                >
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
                <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <div style={{
                        fontSize: '14px',
                        color: 'rgba(255, 255, 255, 0.6)',
                        marginBottom: '8px'
                    }}>
                        {lesson.title}
                    </div>
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px'
                    }}>
                        <div style={{
                            width: '400px',
                            height: '8px',
                            background: 'rgba(255, 255, 255, 0.1)',
                            borderRadius: '4px',
                            overflow: 'hidden'
                        }}>
                            <div style={{
                                height: '100%',
                                width: `${progress}%`,
                                background: 'linear-gradient(90deg, #00d4ff, #b000ff)',
                                transition: 'width 0.3s ease'
                            }} />
                        </div>
                        <span style={{
                            fontSize: '13px',
                            fontWeight: 600,
                            color: 'rgba(255, 255, 255, 0.8)'
                        }}>
                            {currentCardIndex + 1}/{cards.length}
                        </span>
                    </div>
                </div>

                <button
                    onClick={() => setShowExitModal(true)}
                    style={{
                        width: '40px',
                        height: '40px',
                        borderRadius: '12px',
                        background: 'rgba(255, 255, 255, 0.05)',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        cursor: 'pointer',
                        color: 'white',
                        transition: 'all 0.2s'
                    }}
                    onMouseOver={(e) => {
                        e.currentTarget.style.background = 'rgba(255, 68, 68, 0.2)'
                        e.currentTarget.style.borderColor = '#ef4444'
                    }}
                    onMouseOut={(e) => {
                        e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)'
                        e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.08)'
                    }}
                >
                    <X size={20} />
                </button>
            </div>

            {/* Mobile Drawer Overlay */}
            <div
                className={`lesson-drawer-overlay ${drawerOpen ? 'active' : ''}`}
                onClick={() => setDrawerOpen(false)}
            />

            {/* Mobile Drawer */}
            <div className={`lesson-drawer ${drawerOpen ? 'active' : ''}`}>
                <div style={{
                    padding: '20px',
                    borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between'
                }}>
                    <span style={{ fontWeight: 600 }}>📚 Struktura Lekcji</span>
                    <button
                        onClick={() => setDrawerOpen(false)}
                        style={{
                            width: '32px',
                            height: '32px',
                            borderRadius: '8px',
                            background: 'rgba(255, 255, 255, 0.05)',
                            border: '1px solid rgba(255, 255, 255, 0.1)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            cursor: 'pointer',
                            color: 'white'
                        }}
                    >
                        <X size={16} />
                    </button>
                </div>
                <LessonSidebar
                    cards={cards}
                    currentCardIndex={currentCardIndex}
                    completedCards={completedCards}
                    onSelectCard={(index) => {
                        if (index < currentCardIndex || completedCards.includes(index)) {
                            setCurrentCardIndex(index)
                            setDrawerOpen(false)
                        }
                    }}
                />
            </div>

            {/* Grid Layout - Sidebar + Content */}
            <div className="lesson-player-grid" style={{
                display: 'grid',
                gridTemplateColumns: '360px 1fr',
                flex: 1,
                overflow: 'hidden'
            }}>
                {/* Lesson Sidebar (Desktop Only) */}
                <div className="lesson-sidebar-desktop" style={{ height: '100%', overflow: 'auto' }}>
                    <LessonSidebar
                        cards={cards}
                        currentCardIndex={currentCardIndex}
                        completedCards={completedCards}
                        onSelectCard={(index) => {
                            if (index < currentCardIndex || completedCards.includes(index)) {
                                setCurrentCardIndex(index)
                            }
                        }}
                    />
                </div>

                {/* Main Content Column */}
                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    overflow: 'hidden'
                }}>
                    {/* Card Content Area */}
                    <div
                        ref={contentAreaRef}
                        className="lesson-content-area"
                        style={{
                            flex: 1,
                            padding: '24px 32px 100px 32px',
                            display: 'flex',
                            alignItems: 'flex-start',
                            justifyContent: 'center',
                            overflowY: 'auto',
                            overflowX: 'hidden'
                        }}
                    >
                        <div
                            key={currentCardIndex}
                            style={{
                                animation: direction === 'right'
                                    ? 'slideInRight 0.4s ease'
                                    : 'slideInLeft 0.4s ease',
                                width: '100%',
                                display: 'flex',
                                justifyContent: 'center'
                            }}
                        >
                            <style>{`
                        @keyframes slideInRight {
                            from {
                                opacity: 0;
                                transform: translateX(50px);
                            }
                            to {
                                opacity: 1;
                                transform: translateX(0);
                            }
                        }
                        @keyframes slideInLeft {
                            from {
                                opacity: 0;
                                transform: translateX(-50px);
                            }
                            to {
                                opacity: 1;
                                transform: translateX(0);
                            }
                        }
                    `}</style>
                            <CardRenderer
                                card={currentCard}
                                onAnswer={() => { }}
                            />
                        </div>
                    </div>

                    {/* Bottom Navigation - Fixed at bottom */}
                    <div style={{
                        position: 'fixed',
                        bottom: 0,
                        left: 0,
                        right: 0,
                        background: 'transparent',
                        borderTop: 'none',
                        padding: '16px 32px',
                        display: 'flex',
                        justifyContent: 'flex-end',
                        gap: '12px',
                        zIndex: 100
                    }}>
                        <button
                            onClick={handlePrevious}
                            disabled={currentCardIndex === 0}
                            style={{
                                padding: '12px 24px',
                                background: currentCardIndex === 0 ? 'rgba(255, 255, 255, 0.05)' : 'rgba(255, 255, 255, 0.1)',
                                border: '1px solid rgba(255, 255, 255, 0.1)',
                                borderRadius: '12px',
                                color: currentCardIndex === 0 ? 'rgba(255, 255, 255, 0.3)' : 'white',
                                fontWeight: 600,
                                cursor: currentCardIndex === 0 ? 'not-allowed' : 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '8px',
                                fontFamily: 'Outfit, sans-serif'
                            }}
                        >
                            <ChevronLeft size={20} />
                            Poprzednia
                        </button>

                        <button
                            onClick={handleNext}
                            style={{
                                padding: '12px 24px',
                                background: 'linear-gradient(135deg, #00d4ff, #b000ff)',
                                border: 'none',
                                borderRadius: '12px',
                                color: 'white',
                                fontWeight: 600,
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '8px',
                                fontFamily: 'Outfit, sans-serif',
                                boxShadow: '0 4px 20px rgba(0, 212, 255, 0.3)'
                            }}
                        >
                            {currentCardIndex === cards.length - 1 ? 'Zakończ' : 'Następna'}
                            <ChevronRight size={20} />
                        </button>
                    </div>

                    {/* Exit Confirmation Modal */}
                    {showExitModal && (
                        <div style={{
                            position: 'fixed',
                            top: 0,
                            left: 0,
                            right: 0,
                            bottom: 0,
                            background: 'rgba(0, 0, 0, 0.7)',
                            backdropFilter: 'blur(10px)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            zIndex: 1000
                        }}>
                            <div style={{
                                background: 'rgba(20, 20, 35, 0.9)',
                                backdropFilter: 'blur(20px)',
                                border: '1px solid rgba(255, 255, 255, 0.1)',
                                borderRadius: '20px',
                                padding: '32px',
                                maxWidth: '400px',
                                width: '90%'
                            }}>
                                <h2 style={{
                                    fontSize: '24px',
                                    fontWeight: 700,
                                    marginBottom: '12px'
                                }}>
                                    Opuścić lekcję?
                                </h2>
                                <p style={{
                                    fontSize: '15px',
                                    color: 'rgba(255, 255, 255, 0.7)',
                                    marginBottom: '24px'
                                }}>
                                    Twój postęp zostanie zapisany i będziesz mógł wrócić później.
                                </p>
                                <div style={{
                                    display: 'flex',
                                    gap: '12px'
                                }}>
                                    <button
                                        onClick={() => setShowExitModal(false)}
                                        style={{
                                            flex: 1,
                                            padding: '12px',
                                            background: 'rgba(255, 255, 255, 0.1)',
                                            border: '1px solid rgba(255, 255, 255, 0.1)',
                                            borderRadius: '12px',
                                            color: 'white',
                                            fontWeight: 600,
                                            cursor: 'pointer',
                                            fontFamily: 'Outfit, sans-serif'
                                        }}
                                    >
                                        Anuluj
                                    </button>
                                    <button
                                        onClick={handleExit}
                                        style={{
                                            flex: 1,
                                            padding: '12px',
                                            background: '#ef4444',
                                            border: 'none',
                                            borderRadius: '12px',
                                            color: 'white',
                                            fontWeight: 600,
                                            cursor: 'pointer',
                                            fontFamily: 'Outfit, sans-serif'
                                        }}
                                    >
                                        Opuść
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Toast Notification */}
                    {toast && <Toast message={toast} type="success" onClose={() => setToast(null)} />}
                </div>
            </div>
        </div>
    )
}


