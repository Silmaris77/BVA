'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { ArrowLeft, Clock, BookOpen, Trophy, ChevronRight, CheckCircle, PlayCircle } from 'lucide-react'
import { getCategoryColor } from '@/lib/categories'

interface Lesson {
    lesson_id: string
    title: string
    description: string
    duration_minutes: number
    xp_reward: number
    difficulty: string
    category: string
    content?: { cards?: any[] }
    module_id?: string
    modules?: {
        id: string
        title: string
        display_order: number
    }
    card_count?: number
}

interface PathData {
    id: string
    path_slug: string
    title: string
    description: string
    lessons: Lesson[]
    lessonProgress: Record<string, { status: string; completed_at: string; current_card: number }>
    stats: {
        totalLessons: number
        completedLessons: number
        progressPercentage: number
        currentLessonIndex: number
        totalDuration: number
        totalXP: number
    }
}

export default function PathDetailPage() {
    const { user } = useAuth()
    const params = useParams()
    const router = useRouter()
    const slug = params.slug as string

    const [path, setPath] = useState<PathData | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function loadPath() {
            try {
                const response = await fetch(`/api/paths/${slug}`)
                const data = await response.json()

                if (data.path) {
                    setPath(data.path)
                }
            } catch (error) {
                console.error('Error loading path:', error)
            } finally {
                setLoading(false)
            }
        }

        loadPath()
    }, [slug])

    const handleLessonClick = (lessonId: string) => {
        router.push(`/lessons/${lessonId}`)
    }

    const handleContinue = () => {
        if (path && path.stats.currentLessonIndex >= 0) {
            const currentLesson = path.lessons[path.stats.currentLessonIndex]
            if (currentLesson) {
                router.push(`/lessons/${currentLesson.lesson_id}`)
            }
        }
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
                Zaloguj się, aby zobaczyć ścieżkę
            </div>
        )
    }

    if (loading) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'rgba(255, 255, 255, 0.6)'
            }}>
                Ładowanie ścieżki...
            </div>
        )
    }

    if (!path) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '16px'
            }}>
                <p>Ścieżka nie znaleziona</p>
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

    const getStatusForLesson = (lesson: Lesson, index: number) => {
        const progress = path.lessonProgress[lesson.lesson_id]
        if (progress?.status === 'completed') return 'completed'
        if (index === path.stats.currentLessonIndex) return 'current'
        if (progress?.status === 'in_progress') return 'in_progress'
        return 'not_started'
    }

    return (
        <div style={{
            minHeight: '100vh',
            padding: '24px',
            maxWidth: '900px',
            margin: '0 auto'
        }}>
            {/* Back Button */}
            <button
                onClick={() => router.push('/lessons')}
                style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    background: 'none',
                    border: 'none',
                    color: 'rgba(255, 255, 255, 0.6)',
                    cursor: 'pointer',
                    marginBottom: '24px',
                    fontSize: '14px',
                    fontFamily: 'Outfit, sans-serif'
                }}
            >
                <ArrowLeft size={18} />
                Wróć do lekcji
            </button>

            {/* Path Header */}
            <div style={{
                background: 'rgba(255, 255, 255, 0.03)',
                border: '1px solid rgba(255, 255, 255, 0.08)',
                borderRadius: '20px',
                padding: '32px',
                marginBottom: '24px'
            }}>
                <span style={{
                    display: 'inline-block',
                    padding: '6px 14px',
                    background: 'rgba(0, 212, 255, 0.15)',
                    border: '1px solid rgba(0, 212, 255, 0.3)',
                    borderRadius: '20px',
                    fontSize: '12px',
                    fontWeight: 600,
                    color: '#00d4ff',
                    marginBottom: '16px'
                }}>
                    🎓 Ścieżka edukacyjna
                </span>

                <h1 style={{
                    fontSize: '32px',
                    fontWeight: 700,
                    marginBottom: '12px'
                }}>
                    {path.title}
                </h1>

                <p style={{
                    fontSize: '16px',
                    color: 'rgba(255, 255, 255, 0.6)',
                    lineHeight: 1.6,
                    marginBottom: '20px'
                }}>
                    {path.description}
                </p>

                <div style={{
                    display: 'flex',
                    gap: '24px',
                    fontSize: '14px',
                    color: 'rgba(255, 255, 255, 0.5)',
                    marginBottom: '20px'
                }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <BookOpen size={16} />
                        {path.stats.totalLessons} lekcji
                    </span>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Clock size={16} />
                        ~{path.stats.totalDuration} min
                    </span>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Trophy size={16} />
                        +{path.stats.totalXP} XP
                    </span>
                </div>

                {/* Progress Bar */}
                <div style={{
                    background: 'rgba(255, 255, 255, 0.1)',
                    borderRadius: '8px',
                    height: '12px',
                    overflow: 'hidden',
                    marginBottom: '12px'
                }}>
                    <div style={{
                        height: '100%',
                        width: `${path.stats.progressPercentage}%`,
                        background: 'linear-gradient(90deg, #00d4ff, #00ff88)',
                        borderRadius: '8px',
                        transition: 'width 0.4s ease'
                    }} />
                </div>
                <span style={{
                    fontSize: '14px',
                    color: 'rgba(255, 255, 255, 0.6)'
                }}>
                    {path.stats.completedLessons} z {path.stats.totalLessons} lekcji ukończone ({path.stats.progressPercentage}%)
                </span>

                {/* Continue Button */}
                {path.stats.progressPercentage < 100 && (
                    <button
                        onClick={handleContinue}
                        style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            padding: '14px 32px',
                            background: 'linear-gradient(135deg, #00d4ff, #b000ff)',
                            border: 'none',
                            borderRadius: '12px',
                            color: 'white',
                            fontSize: '16px',
                            fontWeight: 600,
                            cursor: 'pointer',
                            marginTop: '20px',
                            fontFamily: 'Outfit, sans-serif',
                            transition: 'transform 0.2s, box-shadow 0.2s'
                        }}
                        onMouseOver={(e) => {
                            e.currentTarget.style.transform = 'translateY(-2px)'
                            e.currentTarget.style.boxShadow = '0 8px 25px rgba(0, 212, 255, 0.3)'
                        }}
                        onMouseOut={(e) => {
                            e.currentTarget.style.transform = 'translateY(0)'
                            e.currentTarget.style.boxShadow = 'none'
                        }}
                    >
                        <PlayCircle size={20} />
                        {path.stats.completedLessons > 0 ? 'Kontynuuj ścieżkę' : 'Rozpocznij ścieżkę'}
                    </button>
                )}
            </div>

            {/* Lessons List (Variant B - Cards) */}
            <div style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '16px'
            }}>
                {path.lessons.map((lesson, index) => {
                    const status = getStatusForLesson(lesson, index)
                    const isCompleted = status === 'completed'
                    const isCurrent = status === 'current'
                    const categoryColor = getCategoryColor(lesson.category)

                    // Logic to check if we should show a module header
                    const prevLesson = index > 0 ? path.lessons[index - 1] : null;
                    const isNewModule = lesson.modules && (!prevLesson || prevLesson.modules?.id !== lesson.modules.id);

                    return (
                        <div key={lesson.lesson_id}>
                            {/* Module Header */}
                            {isNewModule && (
                                <div style={{
                                    margin: '32px 0 16px',
                                    paddingBottom: '8px',
                                    borderBottom: '1px solid rgba(255,255,255,0.1)',
                                    color: 'rgba(255,255,255,0.8)',
                                    fontWeight: 600,
                                    fontSize: '18px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '12px'
                                }}>
                                    <span style={{
                                        color: '#00d4ff',
                                        fontSize: '14px',
                                        fontWeight: 800,
                                        opacity: 0.8,
                                        textTransform: 'uppercase',
                                        letterSpacing: '1px'
                                    }}>
                                        Moduł
                                    </span>
                                    {lesson.modules?.title}
                                </div>
                            )}

                            <div
                                onClick={() => handleLessonClick(lesson.lesson_id)}
                                style={{
                                    background: 'rgba(255, 255, 255, 0.03)',
                                    border: `1px solid ${isCompleted ? 'rgba(0, 255, 136, 0.3)' :
                                        isCurrent ? '#00d4ff' :
                                            'rgba(255, 255, 255, 0.08)'
                                        }`,
                                    borderRadius: '16px',
                                    padding: '24px',
                                    display: 'flex',
                                    gap: '20px',
                                    cursor: 'pointer',
                                    transition: 'all 0.3s',
                                    position: 'relative',
                                    boxShadow: isCurrent ? '0 0 20px rgba(0, 212, 255, 0.15)' : 'none'
                                }}
                                onMouseOver={(e) => {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)'
                                    e.currentTarget.style.transform = 'translateX(4px)'
                                }}
                                onMouseOut={(e) => {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.03)'
                                    e.currentTarget.style.transform = 'translateX(0)'
                                }}
                            >
                                {/* Lesson Number */}
                                <div style={{
                                    width: '48px',
                                    height: '48px',
                                    borderRadius: '12px',
                                    background: isCompleted
                                        ? 'rgba(0, 255, 136, 0.15)'
                                        : `${categoryColor}20`,
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    fontSize: '20px',
                                    fontWeight: 700,
                                    color: isCompleted ? '#00ff88' : categoryColor,
                                    flexShrink: 0
                                }}>
                                    {isCompleted ? <CheckCircle size={24} /> : index + 1}
                                </div>

                                {/* Lesson Content */}
                                <div style={{ flex: 1 }}>
                                    <h3 style={{
                                        fontSize: '18px',
                                        fontWeight: 600,
                                        marginBottom: '8px'
                                    }}>
                                        {lesson.title}
                                    </h3>
                                    <p style={{
                                        fontSize: '14px',
                                        color: 'rgba(255, 255, 255, 0.5)',
                                        lineHeight: 1.5,
                                        marginBottom: '12px'
                                    }}>
                                        {lesson.description}
                                    </p>
                                    <div style={{
                                        display: 'flex',
                                        gap: '16px',
                                        fontSize: '13px',
                                        color: 'rgba(255, 255, 255, 0.4)'
                                    }}>
                                        <span>⏱️ {lesson.duration_minutes} min</span>
                                        <span>📄 {lesson.card_count || 0} kart</span>
                                        <span>⭐ +{lesson.xp_reward} XP</span>
                                    </div>
                                </div>

                                {/* Status Badge */}
                                <span style={{
                                    position: 'absolute',
                                    top: '16px',
                                    right: '16px',
                                    padding: '6px 12px',
                                    borderRadius: '20px',
                                    fontSize: '12px',
                                    fontWeight: 600,
                                    background: isCompleted
                                        ? 'rgba(0, 255, 136, 0.15)'
                                        : isCurrent
                                            ? 'rgba(0, 212, 255, 0.15)'
                                            : 'rgba(255, 255, 255, 0.05)',
                                    color: isCompleted ? '#00ff88' : isCurrent ? '#00d4ff' : 'rgba(255, 255, 255, 0.4)',
                                    border: `1px solid ${isCompleted ? '#00ff88' : isCurrent ? '#00d4ff' : 'rgba(255, 255, 255, 0.1)'}`
                                }}>
                                    {isCompleted ? '✅ Ukończone' : isCurrent ? '🔵 W trakcie' : '⚪ Nierozpoczęte'}
                                </span>

                                {/* Arrow */}
                                <ChevronRight
                                    size={24}
                                    style={{
                                        color: 'rgba(255, 255, 255, 0.3)',
                                        alignSelf: 'center'
                                    }}
                                />
                            </div>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}
