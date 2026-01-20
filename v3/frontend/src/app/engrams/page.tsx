'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { supabase } from '@/lib/supabase'
import Link from 'next/link'
import { Search, Bell, Zap, Brain, Library, BookOpen, Clock, RefreshCw, Download, AlertTriangle } from 'lucide-react'
import { CONTENT_CATEGORIES, getCategoryColor } from '@/lib/categories'
import { getStrengthColor, getStrengthLabel, formatTimeUntilRefresh, getRefreshUrgency } from '@/lib/spaced-repetition'

export default function EngramsPage() {
    const { user, profile, loading: authLoading } = useAuth()
    const router = useRouter()
    const [searchTerm, setSearchTerm] = useState('')
    const [selectedCategory, setSelectedCategory] = useState<string>('all')

    useEffect(() => {
        if (!authLoading && !user) {
            router.push('/auth/login')
        }
    }, [user, authLoading, router])

    // Use shared categories from config
    const categories = CONTENT_CATEGORIES

    const [engrams, setEngrams] = useState<any[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function loadData() {
            if (!user) return

            try {
                // Use API endpoint instead of direct Supabase query
                const response = await fetch('/api/engrams')
                const data = await response.json()

                if (data.engrams) {
                    // Format data for display
                    const formattedEngrams = data.engrams.map((engram: any) => ({
                        ...engram,
                        lastRefreshed: engram.last_refreshed_at
                            ? new Date(engram.last_refreshed_at).toLocaleDateString()
                            : null
                    }))
                    setEngrams(formattedEngrams)
                }
            } catch (error) {
                console.error('Error loading engrams:', error)
            } finally {
                setLoading(false)
            }
        }

        loadData()
    }, [user])

    const filteredEngrams = engrams.filter(engram => {
        const matchesCategory = selectedCategory === 'all' || engram.category === selectedCategory
        const matchesSearch = engram.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
            (engram.description && engram.description.toLowerCase().includes(searchTerm.toLowerCase()))
        return matchesCategory && matchesSearch
    })

    const installedCount = engrams.filter(e => e.installed).length
    const availableCount = engrams.filter(e => !e.installed).length
    const completedCount = engrams.filter(e => e.installed && e.strength === 100).length

    const needsRefreshCount = engrams.filter(e => e.installed && e.needs_refresh).length

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
                        <BookOpen size={16} />
                        Lekcje
                    </Link>
                    <Link
                        href="/engrams"
                        style={{
                            padding: '8px 16px',
                            borderRadius: '8px',
                            background: 'rgba(176, 0, 255, 0.2)',
                            border: '1px solid #b000ff',
                            color: '#b000ff',
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
                        Katalog Engramów 🧠
                    </h1>
                    <p style={{
                        fontSize: '16px',
                        color: 'rgba(255, 255, 255, 0.6)'
                    }}>
                        Mikro-umiejętności gotowe do instalacji w Twojej pamięci podręcznej
                    </p>
                </div>

                {/* Search */}
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '16px',
                    marginBottom: '32px'
                }}>
                    <div style={{ position: 'relative', flex: 1 }}>
                        <input
                            type="text"
                            placeholder="Szukaj engramów..."
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
                </div>

                {/* Statistics */}
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
                        <span>💾</span>
                        <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
                            <strong style={{ color: '#b000ff' }}>{installedCount}</strong> zainstalowanych
                        </span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span>📦</span>
                        <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
                            <strong style={{ color: '#00d4ff' }}>{availableCount}</strong> dostępnych
                        </span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span>✅</span>
                        <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
                            <strong style={{ color: '#00ff88' }}>{completedCount}</strong> ukończonych
                        </span>
                    </div>
                    {needsRefreshCount > 0 && (
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <AlertTriangle size={14} style={{ color: '#ff8800' }} />
                            <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
                                <strong style={{ color: '#ff8800' }}>{needsRefreshCount}</strong> do powtórki
                            </span>
                        </div>
                    )}
                </div>

                {/* Category Filters */}
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

                {/* Engrams Grid */}
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
                    gap: '24px'
                }}>
                    {filteredEngrams.map(engram => {
                        // Use shared category color function
                        const categoryColor = getCategoryColor(engram.category)
                        const strengthColor = getStrengthColor(engram.strength)

                        return (
                            <div
                                key={engram.id}
                                style={{
                                    background: 'rgba(20, 20, 35, 0.4)',
                                    backdropFilter: 'blur(20px)',
                                    WebkitBackdropFilter: 'blur(20px)',
                                    border: '1px solid rgba(255, 255, 255, 0.08)',
                                    borderRadius: '16px',
                                    padding: '20px',
                                    cursor: 'pointer',
                                    transition: 'all 0.2s',
                                    position: 'relative',
                                    overflow: 'hidden'
                                }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.borderColor = categoryColor
                                    e.currentTarget.style.transform = 'translateY(-4px)'
                                    e.currentTarget.style.boxShadow = `0 12px 40px ${categoryColor}33`
                                    const shine = e.currentTarget.querySelector('.shine-engram') as HTMLElement
                                    if (shine) shine.style.left = '100%'
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.08)'
                                    e.currentTarget.style.transform = 'translateY(0)'
                                    e.currentTarget.style.boxShadow = 'none'
                                    const shine = e.currentTarget.querySelector('.shine-engram') as HTMLElement
                                    if (shine) shine.style.left = '-100%'
                                }}
                            >
                                {/* Shine overlay */}
                                <div
                                    className="shine-engram"
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

                                {/* Status Badge (top right) */}
                                {engram.installed && (
                                    <div style={{
                                        position: 'absolute',
                                        top: '16px',
                                        right: '16px',
                                        padding: '4px 12px',
                                        background: `${strengthColor}33`,
                                        border: `1px solid ${strengthColor}`,
                                        borderRadius: '20px',
                                        fontSize: '11px',
                                        fontWeight: 600,
                                        color: strengthColor,
                                        zIndex: 2
                                    }}>
                                        {getStrengthLabel(engram.strength)}
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
                                    <Brain size={28} />
                                </div>

                                {/* Title */}
                                <h3 style={{
                                    fontSize: '16px',
                                    fontWeight: 600,
                                    marginBottom: '8px',
                                    position: 'relative',
                                    zIndex: 2
                                }}>
                                    {engram.title}
                                </h3>

                                {/* Description */}
                                <p style={{
                                    fontSize: '13px',
                                    color: 'rgba(255, 255, 255, 0.6)',
                                    lineHeight: 1.5,
                                    marginBottom: '16px',
                                    position: 'relative',
                                    zIndex: 2
                                }}>
                                    {engram.description}
                                </p>

                                {/* Meta info (if installed) */}
                                {engram.installed && (
                                    <div style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '16px',
                                        fontSize: '12px',
                                        color: 'rgba(255, 255, 255, 0.6)',
                                        marginBottom: '12px',
                                        position: 'relative',
                                        zIndex: 2,
                                        flexWrap: 'wrap'
                                    }}>
                                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: strengthColor }}>
                                            💪 {engram.strength}%
                                        </span>
                                        {engram.next_refresh_due && (
                                            <span style={{
                                                display: 'flex',
                                                alignItems: 'center',
                                                gap: '4px',
                                                color: engram.needs_refresh ? '#ff8800' : 'rgba(255, 255, 255, 0.6)'
                                            }}>
                                                <RefreshCw size={12} />
                                                {formatTimeUntilRefresh(engram.next_refresh_due)}
                                            </span>
                                        )}
                                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                            🔄 {engram.refresh_count || 0}x
                                        </span>
                                    </div>
                                )}

                                {/* Progress bar (if installed) */}
                                {engram.installed && (
                                    <div style={{
                                        height: '6px',
                                        background: 'rgba(255, 255, 255, 0.1)',
                                        borderRadius: '3px',
                                        overflow: 'hidden',
                                        marginBottom: '12px',
                                        position: 'relative',
                                        zIndex: 2
                                    }}>
                                        <div style={{
                                            height: '100%',
                                            width: `${engram.strength}%`,
                                            background: `linear-gradient(90deg, ${strengthColor}, ${categoryColor})`,
                                            borderRadius: '3px',
                                            transition: 'width 0.4s ease'
                                        }} />
                                    </div>
                                )}

                                {/* Action Button */}
                                <button
                                    onClick={(e) => {
                                        e.stopPropagation()
                                        router.push(`/engrams/${engram.id}`)
                                    }}
                                    style={{
                                        width: '100%',
                                        padding: '10px',
                                        background: engram.installed
                                            ? `${categoryColor}20`
                                            : `linear-gradient(135deg, ${categoryColor}, #b000ff)`,
                                        border: engram.installed ? `1px solid ${categoryColor}` : 'none',
                                        borderRadius: '8px',
                                        color: 'white',
                                        fontSize: '14px',
                                        fontWeight: 600,
                                        cursor: 'pointer',
                                        fontFamily: 'Outfit, sans-serif',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        gap: '8px',
                                        position: 'relative',
                                        zIndex: 2
                                    }}>
                                    {engram.installed ? (
                                        <>
                                            <RefreshCw size={14} />
                                            Odśwież
                                        </>
                                    ) : (
                                        <>
                                            <Download size={14} />
                                            Instaluj
                                        </>
                                    )}
                                </button>
                            </div>
                        )
                    })}
                </div>
            </div>
        </div>
    )
}
