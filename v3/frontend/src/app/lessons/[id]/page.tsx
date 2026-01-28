'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState, useRef } from 'react'
import { useParams, useRouter } from 'next/navigation'
import CardRenderer from '@/components/lesson/CardRenderer'
import LessonSidebar from '@/components/LessonSidebar'
import { X, ChevronLeft, ChevronRight, Menu } from 'lucide-react'
import Toast from '@/components/Toast'

interface Card {
    type: 'intro' | 'concept' | 'question' | 'summary' | 'test' | 'cover'
    [key: string]: any
}

interface Lesson {
    lesson_id: string
    title: string
    subtitle?: string
    estimated_duration?: number
    xp_reward: number
    track?: string
    category?: string // Allow category in interface
    content: {
        cards: Card[]
    }
}

const TRACK_TITLES: Record<string, string> = {
    'sales-manager': 'Akademia Menedżera',
    'sales': 'Akademia B2B',
    'math': 'Matematyka'
}

export default function LessonPlayerPage() {
    const { user, profile, refreshProfile } = useAuth()
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
    const [navBlocked, setNavBlocked] = useState(false)

    // Swipe State
    const touchStart = useRef<{ x: number, y: number } | null>(null)
    const touchEnd = useRef<{ x: number, y: number } | null>(null)

    // Touch Handlers for Swipe
    const handleTouchStart = (e: React.TouchEvent) => {
        touchEnd.current = null
        touchStart.current = {
            x: e.targetTouches[0].clientX,
            y: e.targetTouches[0].clientY
        }
    }

    const handleTouchMove = (e: React.TouchEvent) => {
        touchEnd.current = {
            x: e.targetTouches[0].clientX,
            y: e.targetTouches[0].clientY
        }
    }

    const handleTouchEnd = () => {
        if (!touchStart.current || !touchEnd.current) return

        const xDiff = touchStart.current.x - touchEnd.current.x
        const yDiff = touchStart.current.y - touchEnd.current.y
        const absX = Math.abs(xDiff)
        const absY = Math.abs(yDiff)

        // Minimum swipe distance (px)
        const minSwipeDistance = 50

        // Check if it's horizontal swipe (X diff significantly larger than Y diff)
        if (absX > absY && absX > minSwipeDistance) {
            if (xDiff > 0) {
                // Swiped Left -> Next Card
                if (!navBlocked) handleNext()
            } else {
                // Swiped Right -> Previous Card
                handlePrevious()
            }
        }
    }

    // Scroll to top when card changes
    useEffect(() => {
        if (contentAreaRef.current) {
            contentAreaRef.current.scrollTo({ top: 0, behavior: 'smooth' })
        }
        // Also scroll window for mobile
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }, [currentCardIndex])

    // Update navBlocked based on card type
    useEffect(() => {
        const currentCard = cards[currentCardIndex]
        if (currentCard?.type === 'test') {
            setNavBlocked(true)
        } else {
            setNavBlocked(false)
        }
    }, [currentCardIndex, cards])

    useEffect(() => {
        async function loadLesson() {
            try {
                // Fetch from API endpoint
                const response = await fetch(`/api/lessons/${lessonId}`)
                const data = await response.json()

                if (data.lesson) {
                    setLesson(data.lesson)

                    const originalCards = data.lesson.content?.cards || []

                    // Check if content already starts with a cover card (e.g. from custom JSON)
                    if (originalCards.length > 0 && originalCards[0].type === 'cover') {
                        setCards(originalCards)
                    } else {
                        // Create Cover Card automatically
                        // Determine Category: Explicit DB category > Track Title Mapping > Default
                        let categoryDisplay = 'Moduł Edukacyjny';
                        if (data.lesson.category) {
                            categoryDisplay = data.lesson.category; // DB override
                        } else if (data.lesson.track && TRACK_TITLES[data.lesson.track]) {
                            categoryDisplay = TRACK_TITLES[data.lesson.track];
                        } else if (data.lesson.track === 'sales-manager') {
                            // Fallback for sales-manager if key is slightly diff
                            categoryDisplay = 'Akademia Menedżera';
                        }

                        const coverCard: Card = {
                            type: 'cover',
                            title: data.lesson.title,
                            subtitle: data.lesson.subtitle,
                            description: data.lesson.description,
                            category: categoryDisplay,
                            durationMinutes: data.lesson.duration_minutes,
                            xpReward: data.lesson.xp_reward
                        }

                        // Prepend cover card
                        setCards([coverCard, ...originalCards])
                    }

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
                await refreshProfile()
            }
        } catch (error) {
            console.error('Error completing lesson:', error)
        }
    }



    const handleResetLesson = async () => {
        try {
            const response = await fetch(`/api/lessons/${lessonId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'reset' })
            })

            if (response.ok) {
                setToast('Postęp zresetowany. Powodzenia!')
                setCurrentCardIndex(0)
                setNavBlocked(false)
                // Reload lesson to be safe or just reset stats
                setCompletedCards([])
            }
        } catch (error) {
            console.error('Error resetting lesson:', error)
        }
    }

    const handleNext = async () => {
        if (navBlocked) return
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
                    if (!navBlocked) handleNext()
                    break
                case 'Escape':
                    e.preventDefault()
                    setShowExitModal(true)
                    break
            }
        }

        window.addEventListener('keydown', handleKeyDown)
        return () => window.removeEventListener('keydown', handleKeyDown)
    }, [currentCardIndex, cards.length, navBlocked])

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

    // Safety check if card is missing (e.g. index out of bounds or empty cards)
    if (!currentCard) {
        return (
            <div style={{
                height: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white'
            }}>
                Wczytywanie karty...
            </div>
        )
    }

    const progress = ((currentCardIndex + 1) / cards.length) * 100
    const isTestCard = currentCard.type === 'test'


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
                <style>{`
                    .hamburger-btn { display: flex; }
                    .desktop-header-spacer { display: none; }
                    
                    @media (min-width: 769px) {
                        .hamburger-btn { display: none; }
                        .desktop-header-spacer { display: block; width: 360px; flex-shrink: 0; }
                    }
                `}</style>
                <div className="desktop-header-spacer" />
                <button
                    className="hamburger-btn"
                    onClick={() => setDrawerOpen(true)}
                >
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
                <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', minWidth: 0, padding: '0 12px' }}>
                    <div style={{
                        fontSize: '14px',
                        color: 'rgba(255, 255, 255, 0.6)',
                        marginBottom: '8px',
                        whiteSpace: 'nowrap',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        maxWidth: '100%'
                    }}>
                        {lesson.title}
                    </div>
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        width: '100%',
                        justifyContent: 'center'
                    }}>
                        <div style={{
                            width: '100%',
                            maxWidth: '400px',
                            height: '8px',
                            background: 'rgba(255, 255, 255, 0.1)',
                            borderRadius: '4px',
                            overflow: 'hidden',
                            flexShrink: 1
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
                            color: 'rgba(255, 255, 255, 0.8)',
                            flexShrink: 0
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
                    flexDirection: 'column',
                    overflow: 'hidden',
                    position: 'relative', // Needed for absolute positioning of nav
                    height: '100%',     // Ensure full height
                    display: 'flex'
                }}>
                    {/* Navigation Buttons - Floating Side Chevrons (Desktop) / Bottom Corners (Mobile) */}
                    <style>{`
                        .nav-btn {
                            position: absolute;
                            top: 50%;
                            transform: translateY(-50%);
                            z-index: 50;
                            transition: all 0.2s ease;
                            opacity: 0.3; /* Ghost style on desktop by default */
                        }
                        .nav-btn:hover {
                            opacity: 1; /* Fully visible on hover */
                            transform: translateY(-50%) scale(1.1);
                        }
                        .nav-btn-prev {
                            left: 32px;
                        }
                        .nav-btn-next {
                            right: 32px;
                        }

                        @media (max-width: 768px) {
                            .nav-btn {
                                position: fixed;
                                top: auto !important;
                                bottom: 24px !important;
                                transform: none !important;
                                opacity: 0.15 !important; /* Even more subtle on mobile */
                                background: rgba(255, 255, 255, 0.1) !important;
                            }
                            /* Make it slightly more visible when actually touching/using it */
                            .nav-btn:active {
                                opacity: 0.8 !important;
                                transform: scale(0.95) !important;
                            }
                            /* Remove hover effect on mobile to prevent sticky states */
                            .nav-btn:hover {
                                opacity: 0.15; 
                                transform: none;
                            }
                            .nav-btn-prev {
                                left: 24px;
                            }
                            .nav-btn-next {
                                right: 24px;
                            }
                        }
                    `}</style>

                    {/* Previous Button */}
                    <button
                        onClick={handlePrevious}
                        className="nav-btn nav-btn-prev"
                        disabled={currentCardIndex === 0}
                        style={{
                            width: '56px',
                            height: '56px',
                            borderRadius: '50%',
                            background: 'rgba(255, 255, 255, 0.05)',
                            border: '1px solid rgba(255, 255, 255, 0.1)',
                            backdropFilter: 'blur(10px)',
                            color: 'white',
                            display: currentCardIndex === 0 ? 'none' : 'flex', // Hide if disabled
                            alignItems: 'center',
                            justifyContent: 'center',
                            cursor: 'pointer',
                            boxShadow: '0 4px 20px rgba(0,0,0,0.2)'
                        }}
                    >
                        <ChevronLeft size={28} />
                    </button>

                    {/* Next Button */}
                    <button
                        onClick={handleNext}
                        disabled={navBlocked}
                        className="nav-btn nav-btn-next"
                        style={{
                            width: currentCardIndex === cards.length - 1 ? 'auto' : '56px',
                            padding: currentCardIndex === cards.length - 1 ? '0 32px' : '0',
                            height: '56px',
                            borderRadius: '50px', // Capsule or Circle
                            background: navBlocked ? 'rgba(255,255,255,0.1)' : 'linear-gradient(135deg, #00d4ff, #b000ff)',
                            border: 'none',
                            color: navBlocked ? 'rgba(255,255,255,0.3)' : 'white',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            cursor: navBlocked ? 'not-allowed' : 'pointer',
                            boxShadow: navBlocked ? 'none' : '0 4px 20px rgba(0, 212, 255, 0.3)'
                        }}
                    >
                        {currentCardIndex === cards.length - 1 ? (
                            <span style={{ fontFamily: 'Outfit, sans-serif', fontWeight: 600, fontSize: '16px' }}>Zakończ</span>
                        ) : (
                            <ChevronRight size={28} />
                        )}
                    </button>

                    {/* Card Content Area - With Swipe Handlers */}
                    <div
                        ref={contentAreaRef}
                        className="lesson-content-area"
                        onTouchStart={handleTouchStart}
                        onTouchMove={handleTouchMove}
                        onTouchEnd={handleTouchEnd}
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
                                onReset={handleResetLesson}
                                onNext={handleNext}
                                onTestResult={async (score, passed) => {
                                    if (passed) {
                                        setNavBlocked(false)
                                        // Optional: Save score or status via API if needed
                                    } else {
                                        setNavBlocked(true)
                                    }
                                }}
                            />
                        </div>
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


