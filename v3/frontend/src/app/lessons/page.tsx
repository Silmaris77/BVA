'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState, useMemo } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { supabase } from '@/lib/supabase'
import LessonCard from '@/components/LessonCard'
import { Search, Bell, Zap, Filter, Brain, Library, BookOpen } from 'lucide-react'

interface Lesson {
    id: string
    title: string
    description: string
    category: string
    difficulty: 'beginner' | 'intermediate' | 'advanced'
    duration_minutes: number
    xp_reward: number
    card_count: number
    created_at: string
}

interface UserProgress {
    lesson_id: string
    completed_at: Date | null
    current_card_index: number
}

export default function LessonsPage() {
    const { user, profile } = useAuth()
    const router = useRouter()
    const [lessons, setLessons] = useState<Lesson[]>([])
    const [progress, setProgress] = useState<Record<string, UserProgress>>({})
    const [loading, setLoading] = useState(true)
    const [selectedCategory, setSelectedCategory] = useState<string>('all')
    const [searchTerm, setSearchTerm] = useState('')
    const [sortBy, setSortBy] = useState<'newest' | 'duration' | 'xp' | 'difficulty'>('newest')

    const categories = [
        { id: 'all', name: 'Wszystkie', color: '#00d4ff' },
        { id: 'Komunikacja', name: 'Komunikacja', color: '#00d4ff' },
        { id: 'Leadership', name: 'Leadership', color: '#b000ff' },
        { id: 'Strategy', name: 'Strategia', color: '#ffd700' },
        { id: 'Sales', name: 'Sprzedaż', color: '#00ff88' }
    ]

    useEffect(() => {
        async function fetchLessons() {
            if (!user) return

            try {
                console.log('Fetching lessons for user:', user.id)

                // Fetch all lessons
                const { data: lessonsData, error: lessonsError } = await supabase
                    .from('lessons')
                    .select('*')
                    .order('created_at', { ascending: false })

                if (lessonsError) {
                    console.error('Error fetching lessons:', lessonsError)
                    throw lessonsError
                }

                console.log('Fetched lessons:', lessonsData)

                // Fetch user progress
                const { data: progressData, error: progressError } = await supabase
                    .from('user_progress')
                    .select('*')
                    .eq('user_id', user.id)

                if (progressError) {
                    console.error('Error fetching progress:', progressError)
                    // Don't throw - progress is optional
                }

                console.log('Fetched progress:', progressData)

                // Create progress map
                const progressMap: Record<string, UserProgress> = {}
                progressData?.forEach((p: any) => {
                    progressMap[p.lesson_id] = {
                        lesson_id: p.lesson_id,
                        completed_at: p.completed_at,
                        current_card_index: p.current_card_index
                    }
                })

                setLessons(lessonsData || [])
                setProgress(progressMap)

                // Artificial delay to show skeleton loaders (REMOVE IN PRODUCTION)
                await new Promise(resolve => setTimeout(resolve, 1500))
            } catch (error) {
                console.error('Error fetching lessons:', error)
            } finally {
                setLoading(false)
            }
        }

        fetchLessons()
    }, [user])

    // Filter lessons
    const filteredLessons = lessons.filter(lesson => {
        const matchesCategory = selectedCategory === 'all' || lesson.category === selectedCategory
        const matchesSearch = lesson.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
            lesson.description.toLowerCase().includes(searchTerm.toLowerCase())
        return matchesCategory && matchesSearch
    })

    // Sort lessons
    const sortedLessons = useMemo(() => {
        const sorted = [...filteredLessons]
        switch (sortBy) {
            case 'newest':
                return sorted.sort((a, b) =>
                    new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
                )
            case 'duration':
                return sorted.sort((a, b) => a.duration_minutes - b.duration_minutes)
            case 'xp':
                return sorted.sort((a, b) => b.xp_reward - a.xp_reward)
            case 'difficulty':
                const order = { beginner: 1, intermediate: 2, advanced: 3 }
                return sorted.sort((a, b) =>
                    (order[a.difficulty] || 0) - (order[b.difficulty] || 0)
                )
            default:
                return sorted
        }
    }, [filteredLessons, sortBy])

    if (!user) return null

    return (
        <div style={{ minHeight: '100vh' }}>
            {/* Top Bar */}
            <div style={{
                background: 'rgba(0, 0, 0, 0.2)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
                padding: '16px 32px 16px 48px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                position: 'sticky',
                top: 0,
                zIndex: 50
            }}>
                {/* Main Tabs (Lekcje / Engramy / Zasoby) */}
                <div style={{
                    display: 'flex',
                    gap: '8px',
                    flex: 1
                }}>
                    <Link
                        href="/lessons"
                        style={{
                            padding: '8px 16px',
                            borderRadius: '8px',
                            background: 'rgba(0, 212, 255, 0.2)',
                            border: '1px solid #00d4ff',
                            color: '#00d4ff',
                            fontSize: '13px',
                            fontWeight: 600,
                            cursor: 'pointer',
                            fontFamily: 'Outfit, sans-serif',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '6px',
                            transition: 'all 0.2s',
                            textDecoration: 'none'
                        }}
                    >
                        <BookOpen size={16} />
                        Lekcje
                    </Link>
                    <Link
                        href="/engrams"
                        style={{
                            padding: '8px 16px',
                            borderRadius: '8px',
                            background: 'transparent',
                            border: '1px solid transparent',
                            color: 'rgba(255, 255, 255, 0.6)',
                            fontSize: '13px',
                            fontWeight: 600,
                            cursor: 'pointer',
                            fontFamily: 'Outfit, sans-serif',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '6px',
                            transition: 'all 0.2s',
                            textDecoration: 'none'
                        }}
                    >
                        <Brain size={16} />
                        Engramy
                    </Link>
                    <Link
                        href="/resources"
                        style={{
                            padding: '8px 16px',
                            borderRadius: '8px',
                            background: 'transparent',
                            border: '1px solid transparent',
                            color: 'rgba(255, 255, 255, 0.6)',
                            fontSize: '13px',
                            fontWeight: 600,
                            cursor: 'pointer',
                            fontFamily: 'Outfit, sans-serif',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '6px',
                            transition: 'all 0.2s',
                            textDecoration: 'none'
                        }}
                    >
                        <Library size={16} />
                        Zasoby
                    </Link>
                </div>

                {/* Actions */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <div style={{
                        width: '40px',
                        height: '40px',
                        borderRadius: '12px',
                        background: 'rgba(255, 255, 255, 0.05)',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        cursor: 'pointer',
                        position: 'relative'
                    }}>
                        <Bell size={20} />
                        <div style={{
                            position: 'absolute',
                            top: '-4px',
                            right: '-4px',
                            width: '18px',
                            height: '18px',
                            background: '#ff0055',
                            borderRadius: '50%',
                            fontSize: '10px',
                            fontWeight: 700,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                        }}>3</div>
                    </div>

                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '6px 12px',
                        background: 'linear-gradient(135deg, #ffd700, #ff8800)',
                        borderRadius: '20px',
                        fontSize: '13px',
                        fontWeight: 700,
                        color: '#000'
                    }}>
                        <Zap size={16} />
                        <span>{profile?.xp || 0} XP</span>
                    </div>

                    <div style={{
                        width: '40px',
                        height: '40px',
                        borderRadius: '50%',
                        background: 'linear-gradient(135deg, #b000ff, #00d4ff)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontWeight: 700,
                        cursor: 'pointer'
                    }}>
                        {profile?.full_name?.substring(0, 2).toUpperCase() || 'U'}
                    </div>
                </div>
            </div>

            {/* Content */}
            <div style={{ padding: '48px 32px 32px 48px' }}>
                {/* Page Header */}
                <div style={{ marginBottom: '32px' }}>
                    <h1 style={{
                        fontSize: '32px',
                        fontWeight: 700,
                        marginBottom: '8px'
                    }}>
                        Nauka
                    </h1>
                    <p style={{
                        fontSize: '16px',
                        color: 'rgba(255, 255, 255, 0.6)'
                    }}>
                        Rozwijaj swoje umiejętności z interaktywnymi lekcjami i mikro-szkoleniami
                    </p>
                </div>

                {/* Search and Sort */}
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '16px',
                    marginBottom: '32px'
                }}>
                    {/* Search */}
                    <div style={{ position: 'relative', width: '76%' }}>
                        <input
                            type="text"
                            placeholder="Szukaj lekcji..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            style={{
                                width: '100%',
                                padding: '10px 16px 10px 40px',
                                background: 'rgba(255, 255, 255, 0.05)',
                                border: '1px solid rgba(255, 255, 255, 0.08)',
                                borderRadius: '12px',
                                color: 'white',
                                fontFamily: 'Outfit, sans-serif',
                                fontSize: '14px',
                                outline: 'none'
                            }}
                        />
                        <Search size={18} style={{
                            position: 'absolute',
                            left: '12px',
                            top: '50%',
                            transform: 'translateY(-50%)',
                            color: 'rgba(255, 255, 255, 0.6)'
                        }} />
                    </div>

                    {/* Sort */}
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px'
                    }}>
                        <span style={{
                            fontSize: '14px',
                            color: 'rgba(255, 255, 255, 0.6)',
                            fontWeight: 500
                        }}>
                            Sortuj:
                        </span>
                        <select
                            value={sortBy}
                            onChange={(e) => setSortBy(e.target.value as any)}
                            style={{
                                padding: '10px 16px',
                                background: 'rgba(255, 255, 255, 0.05)',
                                border: '1px solid rgba(255, 255, 255, 0.1)',
                                borderRadius: '10px',
                                color: 'white',
                                cursor: 'pointer',
                                fontFamily: 'Outfit, sans-serif',
                                fontSize: '14px',
                                fontWeight: 500,
                                outline: 'none'
                            }}
                        >
                            <option value="newest" style={{ background: '#1a1a2e' }}>Najnowsze</option>
                            <option value="duration" style={{ background: '#1a1a2e' }}>Czas trwania</option>
                            <option value="xp" style={{ background: '#1a1a2e' }}>Nagroda XP</option>
                            <option value="difficulty" style={{ background: '#1a1a2e' }}>Poziom trudności</option>
                        </select>
                    </div>
                </div>

                {/* Statistics Bar */}
                {!loading && (
                    <div style={{
                        display: 'flex',
                        gap: '24px',
                        padding: '16px 24px',
                        background: 'rgba(255, 255, 255, 0.03)',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        borderRadius: '12px',
                        marginBottom: '24px',
                        fontSize: '14px'
                    }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <span>📊</span>
                            <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
                                <strong style={{ color: 'white' }}>{lessons.length}</strong> lekcji dostępnych
                            </span>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <span>✅</span>
                            <span style={{ color: '#00ff88' }}>
                                <strong style={{ color: '#00ff88' }}>
                                    {Object.values(progress).filter(p => p.completed_at).length}
                                </strong> ukończone
                            </span>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <span>🔥</span>
                            <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
                                <strong style={{ color: '#00d4ff' }}>
                                    {Object.values(progress).filter(p => p.current_card_index > 0 && !p.completed_at).length}
                                </strong> w trakcie
                            </span>
                        </div>
                    </div>
                )}

                {/* Category Tabs */}
                <div style={{
                    display: 'flex',
                    gap: '12px',
                    marginBottom: '32px',
                    overflowX: 'auto',
                    paddingBottom: '8px'
                }}>
                    {categories.map(cat => (
                        <button
                            key={cat.id}
                            onClick={() => setSelectedCategory(cat.id)}
                            style={{
                                padding: '10px 20px',
                                background: selectedCategory === cat.id ? `${cat.color}20` : 'rgba(255, 255, 255, 0.05)',
                                border: selectedCategory === cat.id ? `1px solid ${cat.color}` : '1px solid rgba(255, 255, 255, 0.08)',
                                borderRadius: '12px',
                                color: selectedCategory === cat.id ? cat.color : 'rgba(255, 255, 255, 0.7)',
                                fontSize: '14px',
                                fontWeight: 600,
                                cursor: 'pointer',
                                transition: 'all 0.2s',
                                whiteSpace: 'nowrap',
                                fontFamily: 'Outfit, sans-serif'
                            }}
                        >
                            {cat.name}
                        </button>
                    ))}
                </div>

                {/* Lessons Grid */}
                {loading ? (
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
                        gap: '24px'
                    }}>
                        {[1, 2, 3, 4, 5, 6].map(i => (
                            <SkeletonCard key={i} delay={i * 0.05} />
                        ))}
                    </div>
                ) : sortedLessons.length === 0 ? (
                    <div style={{
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '400px',
                        gap: '16px'
                    }}>
                        <Filter size={48} style={{ color: 'rgba(255, 255, 255, 0.3)' }} />
                        <p style={{ fontSize: '16px', color: 'rgba(255, 255, 255, 0.6)' }}>
                            Nie znaleziono lekcji spełniających kryteria
                        </p>
                    </div>
                ) : (
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
                        gap: '24px'
                    }}>
                        {sortedLessons.map(lesson => (
                            <LessonCard
                                key={lesson.id}
                                lesson={lesson}
                                progress={progress[lesson.id]}
                                onClick={() => router.push(`/lessons/${lesson.id}`)}
                            />
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}

// Skeleton loader for lesson cards
function SkeletonCard({ delay }: { delay: number }) {
    return (
        <div
            style={{
                background: 'rgba(20, 20, 35, 0.4)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.08)',
                borderRadius: '16px',
                padding: '20px',
                animation: `fadeIn 0.5s ease-in ${delay}s both`
            }}
        >
            <style>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        @keyframes shimmer {
          0% {
            background-position: -1000px 0;
          }
          100% {
            background-position: 1000px 0;
          }
        }
      `}</style>

            {/* Icon skeleton */}
            <div style={{
                width: '56px',
                height: '56px',
                borderRadius: '12px',
                background: 'linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%)',
                backgroundSize: '1000px 100%',
                animation: 'shimmer 2s infinite',
                marginBottom: '16px'
            }} />

            {/* Title skeleton */}
            <div style={{
                height: '20px',
                width: '80%',
                borderRadius: '4px',
                background: 'linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%)',
                backgroundSize: '1000px 100%',
                animation: 'shimmer 2s infinite',
                marginBottom: '8px'
            }} />

            {/* Description skeleton */}
            <div style={{
                height: '14px',
                width: '100%',
                borderRadius: '4px',
                background: 'linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%)',
                backgroundSize: '1000px 100%',
                animation: 'shimmer 2s infinite',
                marginBottom: '6px'
            }} />
            <div style={{
                height: '14px',
                width: '70%',
                borderRadius: '4px',
                background: 'linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%)',
                backgroundSize: '1000px 100%',
                animation: 'shimmer 2s infinite',
                marginBottom: '16px'
            }} />

            {/* Meta skeleton */}
            <div style={{
                display: 'flex',
                gap: '16px',
                marginBottom: '12px'
            }}>
                <div style={{
                    height: '12px',
                    width: '60px',
                    borderRadius: '4px',
                    background: 'linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%)',
                    backgroundSize: '1000px 100%',
                    animation: 'shimmer 2s infinite'
                }} />
                <div style={{
                    height: '12px',
                    width: '60px',
                    borderRadius: '4px',
                    background: 'linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%)',
                    backgroundSize: '1000px 100%',
                    animation: 'shimmer 2s infinite'
                }} />
                <div style={{
                    height: '12px',
                    width: '60px',
                    borderRadius: '4px',
                    background: 'linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%)',
                    backgroundSize: '1000px 100%',
                    animation: 'shimmer 2s infinite'
                }} />
            </div>

            {/* Progress bar skeleton */}
            <div style={{
                height: '6px',
                width: '100%',
                borderRadius: '3px',
                background: 'linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%)',
                backgroundSize: '1000px 100%',
                animation: 'shimmer 2s infinite'
            }} />
        </div>
    )
}
