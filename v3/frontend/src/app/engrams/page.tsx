'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Search, Bell, Zap, Brain, Library, BookOpen, Clock, RefreshCw, Download } from 'lucide-react'

export default function EngramsPage() {
    const { user, profile } = useAuth()
    const [searchTerm, setSearchTerm] = useState('')
    const [selectedCategory, setSelectedCategory] = useState<string>('all')

    const categories = [
        { id: 'all', name: 'Wszystkie', color: '#00d4ff' },
        { id: 'Sales', name: 'Sprzedaż', color: '#00ff88' },
        { id: 'Leadership', name: 'Leadership', color: '#b000ff' },
        { id: 'Mindset', name: 'Mindset', color: '#ffd700' }
    ]

    // Mock engrams data
    const mockEngrams = [
        {
            id: '1',
            title: 'Szybkie Podejmowanie Decyzji',
            description: 'Techniki błyskawicznej analizy sytuacji i podejmowania trafnych decyzji pod presją czasu.',
            category: 'Leadership',
            strength: 95,
            installed: true,
            lastRefreshed: '2 dni temu'
        },
        {
            id: '2',
            title: 'Pitch 30-Sekundowy',
            description: 'Umiejętność zwięzłego przedstawienia wartości produktu w 30 sekund.',
            category: 'Sales',
            strength: 45,
            installed: true,
            lastRefreshed: '14 dni temu'
        },
        {
            id: '3',
            title: 'Aktywne Słuchanie',
            description: 'Techniki głębokiego słuchania i rozumienia potrzeb rozmówcy.',
            category: 'Sales',
            strength: 78,
            installed: true,
            lastRefreshed: '5 dni temu'
        },
        {
            id: '4',
            title: 'Growth Mindset Praktycznie',
            description: 'Przekształcanie porażek w lekcje i budowanie mentalności wzrostu.',
            category: 'Mindset',
            strength: 0,
            installed: false,
            lastRefreshed: null
        },
        {
            id: '5',
            title: 'AI-Powered Prospecting',
            description: 'Wykorzystanie AI do identyfikacji i kwalifikacji potencjalnych klientów.',
            category: 'Sales',
            strength: 0,
            installed: false,
            lastRefreshed: null
        }
    ]

    const filteredEngrams = mockEngrams.filter(engram => {
        const matchesCategory = selectedCategory === 'all' || engram.category === selectedCategory
        const matchesSearch = engram.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
            engram.description.toLowerCase().includes(searchTerm.toLowerCase())
        return matchesCategory && matchesSearch
    })

    const installedCount = mockEngrams.filter(e => e.installed).length
    const availableCount = mockEngrams.filter(e => !e.installed).length
    const completedCount = mockEngrams.filter(e => e.installed && e.strength === 100).length

    const getStrengthColor = (strength: number) => {
        if (strength >= 80) return '#00ff88' // Green - Stable
        if (strength >= 40) return '#ffd700' // Yellow - Fading
        return '#ff4757' // Red - Critical
    }

    const getStrengthLabel = (strength: number) => {
        if (strength >= 80) return 'Stable'
        if (strength >= 40) return 'Fading'
        return 'Critical'
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
                        const getCategoryColor = (category: string) => {
                            const colors: Record<string, string> = {
                                'Sales': '#00ff88',
                                'Leadership': '#b000ff',
                                'Mindset': '#ffd700'
                            }
                            return colors[category] || '#00d4ff'
                        }

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
                                        zIndex: 2
                                    }}>
                                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                            <Clock size={12} />
                                            {engram.lastRefreshed}
                                        </span>
                                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: strengthColor }}>
                                            {engram.strength}%
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
                                <button style={{
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
