'use client'

import { Check, Lock } from 'lucide-react'
import 'katex/dist/katex.min.css'
import { InlineMath } from 'react-katex'

// Helper function to render text with inline LaTeX
function renderMathText(text: string) {
    // Split by $ signs for inline math
    const parts = text.split(/\$([^$]+)\$/g)
    return parts.map((part, i) => 
        i % 2 === 1 
            ? <InlineMath key={i} math={part} />
            : <span key={i}>{part}</span>
    )
}

interface LessonSidebarProps {
    cards: Array<{
        type: string
        title?: string
        question?: string
        [key: string]: any
    }>
    currentCardIndex: number
    completedCards: number[]
    onSelectCard: (index: number) => void
}

export default function LessonSidebar({
    cards,
    currentCardIndex,
    completedCards,
    onSelectCard
}: LessonSidebarProps) {

    const getCardTitle = (card: any, index: number) => {
        if (card.title) return card.title
        if (card.question) return card.question.substring(0, 60) + '...'
        return `Karta ${index + 1}`
    }

    const getCardStatus = (index: number) => {
        if (completedCards.includes(index)) return 'completed'
        if (index === currentCardIndex) return 'current'
        if (index < currentCardIndex) return 'unlocked'
        return 'locked'
    }

    return (
        <div className="no-scrollbar" style={{
            background: 'rgba(0, 0, 0, 0.2)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            borderRight: '1px solid rgba(255, 255, 255, 0.08)',
            height: '100%',
            overflowY: 'auto',
            padding: '20px'
        } as React.CSSProperties}>
            <div style={{ marginBottom: '32px' }}>
                <h3 style={{
                    fontSize: '12px',
                    textTransform: 'uppercase',
                    letterSpacing: '1px',
                    color: 'rgba(255, 255, 255, 0.6)',
                    marginBottom: '16px',
                    paddingLeft: '12px'
                }}>
                    Struktura lekcji
                </h3>

                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '12px'
                }}>
                    {cards.map((card, index) => {
                        const status = getCardStatus(index)
                        const isActive = index === currentCardIndex
                        const isCompleted = completedCards.includes(index)
                        const isLocked = index > currentCardIndex && !isCompleted

                        return (
                            <div
                                key={index}
                                onClick={() => !isLocked && onSelectCard(index)}
                                style={{
                                    padding: '16px',
                                    borderRadius: '16px',
                                    cursor: isLocked ? 'not-allowed' : 'pointer',
                                    transition: 'all 0.2s',
                                    border: '1px solid transparent',
                                    background: isActive
                                        ? 'rgba(0, 212, 255, 0.15)'
                                        : 'transparent',
                                    borderColor: isActive
                                        ? '#00d4ff'
                                        : 'transparent',
                                    boxShadow: isActive
                                        ? '0 0 20px rgba(0, 212, 255, 0.2)'
                                        : 'none',
                                    opacity: isLocked ? 0.4 : (isCompleted ? 0.6 : 1),
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '12px'
                                }}
                                onMouseEnter={(e) => {
                                    if (!isLocked && !isActive) {
                                        e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)'
                                        e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)'
                                    }
                                }}
                                onMouseLeave={(e) => {
                                    if (!isActive) {
                                        e.currentTarget.style.background = 'transparent'
                                        e.currentTarget.style.borderColor = 'transparent'
                                    }
                                }}
                            >
                                {/* Card Number */}
                                <div style={{
                                    width: '32px',
                                    height: '32px',
                                    borderRadius: '8px',
                                    background: isActive
                                        ? '#00d4ff'
                                        : isCompleted
                                            ? '#00ff88'
                                            : 'rgba(0, 0, 0, 0.3)',
                                    color: (isActive || isCompleted) ? '#000' : '#fff',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    fontSize: '14px',
                                    fontWeight: 700,
                                    flexShrink: 0
                                }}>
                                    {index + 1}
                                </div>

                                {/* Card Info */}
                                <div style={{ flex: 1, minWidth: 0 }}>
                                    <div style={{
                                        fontSize: '14px',
                                        fontWeight: 600,
                                        marginBottom: '4px',
                                        lineHeight: '1.4',
                                        wordBreak: 'break-word'
                                    }}>
                                        {renderMathText(getCardTitle(card, index))}
                                    </div>
                                    <div style={{
                                        fontSize: '12px',
                                        color: isActive
                                            ? '#00d4ff'
                                            : isCompleted
                                                ? '#00ff88'
                                                : 'rgba(255, 255, 255, 0.6)'
                                    }}>
                                        {isCompleted ? 'Ukończone' : isActive ? 'Aktualnie' : isLocked ? 'Zablokowane' : 'Do zrobienia'}
                                    </div>
                                </div>

                                {/* Status Icon */}
                                {isCompleted && (
                                    <Check size={16} style={{ color: '#00ff88', flexShrink: 0 }} />
                                )}
                                {isLocked && (
                                    <Lock size={16} style={{ color: 'rgba(255, 255, 255, 0.4)', flexShrink: 0 }} />
                                )}
                            </div>
                        )
                    })}
                </div>
            </div>
        </div>
    )
}
