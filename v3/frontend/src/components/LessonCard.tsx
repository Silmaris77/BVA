import { Clock, Trophy, BookOpen, Layers, Calendar, Lock } from 'lucide-react'

interface LessonCardProps {
    lesson: {
        id: string
        title: string
        description: string
        category: string
        difficulty: 'beginner' | 'intermediate' | 'advanced'
        duration_minutes: number
        xp_reward: number
        card_count: number
        status?: 'published' | 'coming_soon' | 'draft' | 'archived'
        release_date?: string
        track?: string
        is_locked?: boolean
    }
    progress?: {
        status: 'not_started' | 'in_progress' | 'completed'
        started_at: string | null
        completed_at: string | null
        current_card_index: number
    }
    onClick: () => void
}

export default function LessonCard({ lesson, progress, onClick }: LessonCardProps) {
    const isCompleted = progress?.status === 'completed'
    const isInProgress = progress?.status === 'in_progress'
    const isComingSoon = lesson.status === 'coming_soon'
    const isLocked = lesson.is_locked

    // Format release date if present
    const formattedDate = lesson.release_date
        ? new Date(lesson.release_date).toLocaleDateString('pl-PL', { day: 'numeric', month: 'long', year: 'numeric' })
        : null

    // Completed = 100%, In Progress = calculate, Not Started = 0
    const progressPercentage = isCompleted
        ? 100
        : (progress && lesson.card_count > 0
            ? Math.round(((progress.current_card_index || 0) / lesson.card_count) * 100)
            : 0)

    // Category colors
    const categoryColors: Record<string, string> = {
        'Komunikacja': '#00d4ff',
        'Leadership': '#b000ff',
        'Strategy': '#ffd700',
        'Sales': '#00ff88',
        'Sales Skills': '#00ff88',
        'Sales Methodology': '#ff0055',
        'Product Knowledge': '#ff8800',
        'Account Management': '#b000ff'
    }

    const categoryColor = isComingSoon ? '#888888' : (categoryColors[lesson.category] || '#00d4ff')

    // Badge text
    let badgeText = ''
    let badgeColor = categoryColor

    if (isComingSoon) {
        badgeText = '🚧 W przygotowaniu'
        badgeColor = '#888888'
    } else if (isLocked) {
        badgeText = '🔒 Dostęp zablokowany'
        badgeColor = '#ff4444'
    } else if (isCompleted) {
        badgeText = '✓ Ukończone'
        badgeColor = '#ffd700'
    } else if (isInProgress) {
        badgeText = 'W trakcie'
        badgeColor = '#00d4ff'
    }

    return (
        <div
            onClick={(isComingSoon || isLocked) ? undefined : onClick}
            style={{
                background: 'rgba(20, 20, 35, 0.4)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.08)',
                borderRadius: '16px',
                padding: '20px',
                cursor: (isComingSoon || isLocked) ? 'not-allowed' : 'pointer',
                transition: 'all 0.2s',
                position: 'relative',
                overflow: 'hidden',
                opacity: (isComingSoon || isLocked) ? 0.7 : 1
            }}
            onMouseOver={(e) => {
                if (isComingSoon) return
                e.currentTarget.style.borderColor = categoryColor
                e.currentTarget.style.transform = 'translateY(-4px)'
                e.currentTarget.style.boxShadow = `0 12px 40px ${categoryColor}33`
                const shine = e.currentTarget.querySelector('.shine-lesson') as HTMLElement
                if (shine) shine.style.left = '100%'
            }}
            onMouseOut={(e) => {
                if (isComingSoon) return
                e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.08)'
                e.currentTarget.style.transform = 'translateY(0)'
                e.currentTarget.style.boxShadow = 'none'
                const shine = e.currentTarget.querySelector('.shine-lesson') as HTMLElement
                if (shine) shine.style.left = '-100%'
            }}
        >
            {/* Shine overlay */}
            <div
                className="shine-lesson"
                style={{
                    position: 'absolute',
                    top: 0,
                    left: '-100%',
                    width: '100%',
                    height: '100%',
                    background: `linear-gradient(90deg, transparent, ${categoryColor}40, transparent)`,
                    transition: 'left 0.6s ease',
                    pointerEvents: 'none',
                    zIndex: 1
                }}
            />

            {/* Badge (top right) */}
            {badgeText && (
                <div style={{
                    position: 'absolute',
                    top: '16px',
                    right: '16px',
                    padding: '4px 12px',
                    background: `${badgeColor}33`,
                    border: `1px solid ${badgeColor}`,
                    borderRadius: '20px',
                    fontSize: '11px',
                    fontWeight: 600,
                    color: badgeColor,
                    zIndex: 2,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                }}>
                    {isComingSoon && <Lock size={10} />}
                    {badgeText}
                </div>
            )}

            {/* Track Info (if belongs to track) */}
            {lesson.track && !isComingSoon && (
                <div style={{
                    position: 'absolute',
                    top: '16px',
                    left: '16px', // Wait, icon is here? No icon is below relative
                    padding: '2px 8px',
                    background: 'rgba(255, 255, 255, 0.1)',
                    borderRadius: '4px',
                    fontSize: '10px',
                    color: 'rgba(255, 255, 255, 0.6)',
                    zIndex: 2,
                    display: 'none' // Hidden for now to verify layout
                }}>
                    {lesson.track}
                </div>
            )}

            {/* Icon */}
            <div style={{
                width: '56px',
                height: '56px',
                background: `${categoryColor}33`,
                borderRadius: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '16px',
                color: categoryColor,
                position: 'relative',
                zIndex: 2
            }}>
                <BookOpen size={28} />
            </div>

            {/* Title */}
            <h3 style={{
                fontSize: '16px',
                fontWeight: 600,
                marginBottom: '8px',
                position: 'relative',
                zIndex: 2
            }}>
                {lesson.title}
            </h3>

            {/* Description */}
            <p style={{
                fontSize: '13px',
                color: 'rgba(255, 255, 255, 0.6)',
                marginBottom: '16px',
                lineHeight: '1.5',
                position: 'relative',
                zIndex: 2,
                display: '-webkit-box',
                WebkitLineClamp: 2,
                WebkitBoxOrient: 'vertical',
                overflow: 'hidden'
            }}>
                {lesson.description}
            </p>

            {/* Meta info */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                fontSize: '12px',
                color: 'rgba(255, 255, 255, 0.6)',
                marginBottom: '12px',
                position: 'relative',
                zIndex: 2,
                flexWrap: 'wrap'
            }}>
                {isComingSoon && formattedDate ? (
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: '#ff8800' }}>
                        <Calendar size={12} />
                        Dostępne: {formattedDate}
                    </span>
                ) : (
                    <>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                            <Clock size={12} />
                            {lesson.duration_minutes} min
                        </span>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                            <Layers size={12} />
                            {lesson.card_count} kart
                        </span>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                            <Trophy size={12} />
                            +{lesson.xp_reward} XP
                        </span>
                    </>
                )}
            </div>

            {/* Track Label (Bottom) */}
            {lesson.track && (
                <div style={{
                    fontSize: '11px',
                    color: 'rgba(255, 255, 255, 0.4)',
                    marginBottom: '12px',
                    textTransform: 'uppercase',
                    letterSpacing: '0.5px'
                }}>
                    {lesson.track} Track
                </div>
            )}

            {/* Progress bar - only show if started AND NOT coming soon */}
            {!isComingSoon && (
                <div style={{
                    height: '6px',
                    background: 'rgba(255, 255, 255, 0.1)',
                    borderRadius: '3px',
                    overflow: 'hidden',
                    position: 'relative',
                    zIndex: 2
                }}>
                    <div style={{
                        height: '100%',
                        width: `${progressPercentage}%`,
                        background: isCompleted
                            ? 'linear-gradient(90deg, #00ff88, #00d4ff)' // Green for completed
                            : `linear-gradient(90deg, ${categoryColor}, #b000ff)`, // Category color for in progress
                        borderRadius: '3px',
                        transition: 'width 0.4s ease'
                    }} />
                </div>
            )}
        </div>
    )
}
