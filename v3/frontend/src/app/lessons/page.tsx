'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState, useMemo } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import LessonCard from '@/components/LessonCard'
import PathCard from '@/components/PathCard'
import { Search, Bell, Zap, Filter, Brain, Library, BookOpen, Trophy } from 'lucide-react'
import { CONTENT_CATEGORIES } from '@/lib/categories'

interface Lesson {
    lesson_id: string
    title: string
    description: string
    duration_minutes: number
    xp_reward: number
    difficulty: 'beginner' | 'intermediate' | 'advanced'
    category?: string
    content?: {
        cards: any[]
    }
}

interface UserProgress {
    lesson_id: string
    status: 'not_started' | 'in_progress' | 'completed'
    started_at: string | null
    completed_at: string | null
    current_card_index: number
}

export default function LessonsPage() {
    const { user, profile, loading: authLoading } = useAuth()
    const router = useRouter()
    const [lessons, setLessons] = useState<Lesson[]>([])
    const [userProgress, setUserProgress] = useState<Record<string, UserProgress>>({})
    const [loading, setLoading] = useState(true)
    const [searchTerm, setSearchTerm] = useState('')
    const [sortBy, setSortBy] = useState<'newest' | 'duration' | 'xp' | 'difficulty'>('newest')
    const [selectedCategory, setSelectedCategory] = useState<string>('all')
    const [paths, setPaths] = useState<any[]>([])
    const [pathsLoading, setPathsLoading] = useState(true)
    const [activeTab, setActiveTab] = useState<'lessons' | 'paths'>('lessons')

    const categories = CONTENT_CATEGORIES

    useEffect(() => {
        if (!authLoading && !user) {
            router.push('/auth/login')
        }
    }, [user, authLoading, router])

    useEffect(() => {
        async function fetchLessonsAndProgress() {
            if (!user) return

            try {
                // Fetch lessons and progress from single API endpoint
                const response = await fetch('/api/lessons')
                const data = await response.json()

                if (data.lessons) {
                    setLessons(data.lessons)
                }

                if (data.progress) {
                    setUserProgress(data.progress)
                }
            } catch (error) {
                console.error('Error fetching lessons:', error)
            } finally {
                setLoading(false)
            }
        }

        fetchLessonsAndProgress()
    }, [user])

    // Fetch learning paths
    useEffect(() => {
        async function fetchPaths() {
            if (!user) return
            try {
                const response = await fetch('/api/paths')
                const data = await response.json()
                if (data.paths) {
                    setPaths(data.paths)
                }
            } catch (error) {
                console.error('Error fetching paths:', error)
            } finally {
                setPathsLoading(false)
            }
        }
        fetchPaths()
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

    if (authLoading) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'rgba(255, 255, 255, 0.6)'
            }}>
                Ładowanie...
            </div>
        )
    }

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
                {/* Main Tabs */}
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
                        Rozwijaj swoje umiejętności z interaktywnymi lekcjami
                    </p>
                </div>

                {/* Sub-tabs */}
                <div style={{
                    display: 'flex',
                    gap: '8px',
                    marginBottom: '24px',
                    borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
                    paddingBottom: '16px'
                }}>
                    <button
                        onClick={() => setActiveTab('lessons')}
                        style={{
                            padding: '10px 20px',
                            background: activeTab === 'lessons' ? 'rgba(0, 212, 255, 0.15)' : 'transparent',
                            border: activeTab === 'lessons' ? '1px solid #00d4ff' : '1px solid transparent',
                            borderRadius: '10px',
                            color: activeTab === 'lessons' ? '#00d4ff' : 'rgba(255, 255, 255, 0.6)',
                            fontSize: '14px',
                            fontWeight: 600,
                            cursor: 'pointer',
                            fontFamily: 'Outfit, sans-serif',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            transition: 'all 0.2s'
                        }}
                    >
                        <BookOpen size={16} />
                        Pojedyncze lekcje
                    </button>
                    <button
                        onClick={() => setActiveTab('paths')}
                        style={{
                            padding: '10px 20px',
                            background: activeTab === 'paths' ? 'rgba(176, 0, 255, 0.15)' : 'transparent',
                            border: activeTab === 'paths' ? '1px solid #b000ff' : '1px solid transparent',
                            borderRadius: '10px',
                            color: activeTab === 'paths' ? '#b000ff' : 'rgba(255, 255, 255, 0.6)',
                            fontSize: '14px',
                            fontWeight: 600,
                            cursor: 'pointer',
                            fontFamily: 'Outfit, sans-serif',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            transition: 'all 0.2s'
                        }}
                    >
                        <Trophy size={16} />
                        Ścieżki edukacyjne
                        {!pathsLoading && paths.length > 0 && (
                            <span style={{
                                padding: '2px 8px',
                                background: 'rgba(176, 0, 255, 0.3)',
                                borderRadius: '10px',
                                fontSize: '11px'
                            }}>
                                {paths.length}
                            </span>
                        )}
                    </button>
                </div>

                {/* LESSONS TAB */}
                {activeTab === 'lessons' && (
                    <>
                        {/* Search and Sort */}
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '16px',
                            marginBottom: '24px'
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

                        {/* Category Filters */}
                        <div style={{
                            display: 'flex',
                            gap: '12px',
                            marginBottom: '24px',
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
                            </div>
                        )}

                        {/* Lessons Grid */}
                        {loading ? (
                            <div style={{
                                display: 'grid',
                                gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
                                gap: '24px'
                            }}>
                                {[1, 2, 3].map(i => (
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
                                    Nie znaleziono lekcji
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
                                        key={lesson.lesson_id}
                                        lesson={{
                                            id: lesson.lesson_id,
                                            title: lesson.title,
                                            description: lesson.description,
                                            category: lesson.category || 'Sprzedaż',
                                            difficulty: lesson.difficulty,
                                            duration_minutes: lesson.duration_minutes,
                                            xp_reward: lesson.xp_reward,
                                            card_count: lesson.content?.cards?.length || 0
                                        }}
                                        progress={userProgress[lesson.lesson_id]}
                                        onClick={() => router.push(`/lessons/${lesson.lesson_id}`)}
                                    />
                                ))}
                            </div>
                        )}
                    </>
                )}

                {/* PATHS TAB */}
                {activeTab === 'paths' && (
                    <div>
                        {pathsLoading ? (
                            <div style={{
                                display: 'flex',
                                justifyContent: 'center',
                                alignItems: 'center',
                                height: '200px',
                                color: 'rgba(255, 255, 255, 0.6)'
                            }}>
                                Ładowanie ścieżek...
                            </div>
                        ) : paths.length === 0 ? (
                            <div style={{
                                display: 'flex',
                                flexDirection: 'column',
                                justifyContent: 'center',
                                alignItems: 'center',
                                height: '300px',
                                gap: '16px'
                            }}>
                                <Trophy size={48} style={{ color: 'rgba(255, 255, 255, 0.3)' }} />
                                <p style={{ fontSize: '16px', color: 'rgba(255, 255, 255, 0.6)' }}>
                                    Brak dostępnych ścieżek edukacyjnych
                                </p>
                            </div>
                        ) : (
                            <>
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
                                        <span>🎯</span>
                                        <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
                                            <strong style={{ color: 'white' }}>{paths.length}</strong> ścieżek dostępnych
                                        </span>
                                    </div>
                                </div>
                                <div style={{
                                    display: 'grid',
                                    gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))',
                                    gap: '24px'
                                }}>
                                    {paths.map(path => (
                                        <PathCard key={path.path_slug} path={path} />
                                    ))}
                                </div>
                            </>
                        )}
                    </div>
                )}
            </div>
        </div>
    )
}

// Skeleton loader
function SkeletonCard({ delay }: { delay: number }) {
    return (
        <div style={{
            background: 'rgba(20, 20, 35, 0.4)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            borderRadius: '16px',
            padding: '20px',
            animation: `fadeIn 0.5s ease-in ${delay}s both`
        }}>
            <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes shimmer {
          0% { background-position: -1000px 0; }
          100% { background-position: 1000px 0; }
        }
      `}</style>

            <div style={{
                width: '56px',
                height: '56px',
                borderRadius: '12px',
                background: 'linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%)',
                backgroundSize: '1000px 100%',
                animation: 'shimmer 2s infinite',
                marginBottom: '16px'
            }} />

            <div style={{
                height: '20px',
                width: '80%',
                borderRadius: '4px',
                background: 'linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%)',
                backgroundSize: '1000px 100%',
                animation: 'shimmer 2s infinite',
                marginBottom: '8px'
            }} />

            <div style={{
                height: '14px',
                width: '100%',
                borderRadius: '4px',
                background: 'linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%)',
                backgroundSize: '1000px 100%',
                animation: 'shimmer 2s infinite',
                marginBottom: '6px'
            }} />
        </div>
    )
}
