'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { supabase } from '@/lib/supabase'
import Link from 'next/link'
import { Search, Bell, Zap, Brain, Library, BookOpen, Filter, Lock, ExternalLink, FileText, Table, Video, Book, TrendingUp, Mail, LayoutTemplate } from 'lucide-react'

export default function ResourcesPage() {
    const { user, profile, loading: authLoading } = useAuth()
    const router = useRouter()
    const [searchTerm, setSearchTerm] = useState('')

    useEffect(() => {
        if (!authLoading && !user) {
            router.push('/auth/login')
        }
    }, [user, authLoading, router])

    const [resources, setResources] = useState<any[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function loadResources() {
            if (!user) return

            try {
                const { data, error } = await supabase
                    .from('resources')
                    .select('*')

                if (error) throw error
                setResources(data || [])
            } catch (error) {
                console.error('Error loading resources:', error)
            } finally {
                setLoading(false)
            }
        }
        loadResources()
    }, [user])

    const filteredResources = resources.filter(resource =>
        resource.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (resource.description && resource.description.toLowerCase().includes(searchTerm.toLowerCase()))
    )

    const recommendedResources = filteredResources.slice(0, 3)
    const allResources = filteredResources.slice(3)

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
                            background: 'rgba(0, 255, 136, 0.2)',
                            border: '1px solid #00ff88',
                            color: '#00ff88',
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
                        Biblioteka Zasobów 📚
                    </h1>
                    <p style={{
                        fontSize: '16px',
                        color: 'rgba(255, 255, 255, 0.6)'
                    }}>
                        Szablony, artykuły, narzędzia i materiały wspierające Twój rozwój
                    </p>
                </div>

                {/* Recommended Section */}
                <div style={{ marginBottom: '48px' }}>
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        marginBottom: '20px'
                    }}>
                        <span style={{ fontSize: '20px' }}>⭐</span>
                        <h2 style={{
                            fontSize: '20px',
                            fontWeight: 600
                        }}>
                            Polecane dla Ciebie
                        </h2>
                    </div>

                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
                        gap: '20px'
                    }}>
                        {recommendedResources.map(resource => (
                            <ResourceCard key={resource.id} resource={resource} />
                        ))}
                    </div>
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
                            placeholder="Szukaj w bibliotece zasobów..."
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
                    <button style={{
                        padding: '10px 20px',
                        background: 'rgba(255, 255, 255, 0.05)',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        borderRadius: '12px',
                        color: 'white',
                        fontSize: '14px',
                        fontWeight: 600,
                        cursor: 'pointer',
                        fontFamily: 'Outfit, sans-serif',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px'
                    }}>
                        <Filter size={16} />
                        Filtry
                    </button>
                </div>

                {/* All Resources */}
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
                    gap: '20px'
                }}>
                    {allResources.map(resource => (
                        <ResourceCard key={resource.id} resource={resource} />
                    ))}
                </div>
            </div>
        </div>
    )
}

function ResourceCard({ resource }: { resource: any }) {
    const getIconForType = (type: string) => {
        switch (type) {
            case 'article': return FileText
            case 'template': return Table
            case 'video': return Video
            case 'ebook': return Book
            case 'case_study': return TrendingUp
            default: return FileText
        }
    }

    const getCategoryColor = (category: string) => {
        const colors: Record<string, string> = {
            'Sales': '#00ff88',
            'Sprzedaż': '#00ff88',
            'Leadership': '#b000ff',
            'Communication': '#ffd700',
            'Komunikacja': '#ffd700',
            'Mindset': '#ff4757',
            'Strategy': '#00d4ff',
            'Management': '#b000ff',
            'Technology': '#00d4ff',
            'Tools': '#ffd700',
            'Skills': '#ff4757'
        }
        return colors[category] || '#00d4ff'
    }

    const Icon = getIconForType(resource.type)
    const color = getCategoryColor(resource.category)

    return (
        <div
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
                e.currentTarget.style.borderColor = resource.locked ? 'rgba(255, 255, 255, 0.15)' : 'rgba(0, 255, 136, 0.3)'
                e.currentTarget.style.transform = 'translateY(-4px)'
                if (!resource.locked) {
                    e.currentTarget.style.borderColor = color
                    e.currentTarget.style.boxShadow = `0 12px 40px ${color}33`
                }
                const shine = e.currentTarget.querySelector('.shine-resource') as HTMLElement
                if (shine) shine.style.left = '100%'
            }}
            onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.08)'
                e.currentTarget.style.transform = 'translateY(0)'
                e.currentTarget.style.boxShadow = 'none'
                const shine = e.currentTarget.querySelector('.shine-resource') as HTMLElement
                if (shine) shine.style.left = '-100%'
            }}
        >
            {/* Shine overlay */}
            <div
                className="shine-resource"
                style={{
                    position: 'absolute',
                    top: 0,
                    left: '-100%',
                    width: '100%',
                    height: '100%',
                    background: `linear-gradient(90deg, transparent, ${color}40, transparent)`,
                    transition: 'left 0.6s ease',
                    pointerEvents: 'none',
                    zIndex: 1
                }}
            />

            {/* Lock Badge */}
            {resource.locked && (
                <div style={{
                    position: 'absolute',
                    top: '16px',
                    right: '16px',
                    padding: '4px 8px',
                    background: 'rgba(255, 255, 255, 0.1)',
                    borderRadius: '6px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                    fontSize: '11px',
                    color: 'rgba(255, 255, 255, 0.6)',
                    zIndex: 2
                }}>
                    <Lock size={12} />
                    Zablokowane
                </div>
            )}

            {/* Icon */}
            <div style={{
                width: '56px',
                height: '56px',
                borderRadius: '12px',
                background: `${color}20`,
                border: `1px solid ${color}`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '16px',
                color: color,
                position: 'relative',
                zIndex: 2
            }}>
                <Icon size={24} />
            </div>

            {/* Type Badge */}
            <div style={{
                display: 'inline-block',
                padding: '4px 10px',
                background: `${color}20`,
                border: `1px solid ${color}`,
                borderRadius: '6px',
                fontSize: '10px',
                fontWeight: 700,
                color: color,
                marginBottom: '12px',
                textTransform: 'uppercase',
                letterSpacing: '0.5px',
                position: 'relative',
                zIndex: 2
            }}>
                {resource.type}
            </div>

            {/* Category */}
            <div style={{
                fontSize: '11px',
                color: 'rgba(255, 255, 255, 0.5)',
                marginBottom: '8px',
                position: 'relative',
                zIndex: 2
            }}>
                {resource.category}
            </div>

            {/* Title */}
            <h3 style={{
                fontSize: '16px',
                fontWeight: 600,
                marginBottom: '8px',
                lineHeight: 1.3,
                position: 'relative',
                zIndex: 2
            }}>
                {resource.title}
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
                {resource.description}
            </p>

            {/* Action Button */}
            <button style={{
                width: '100%',
                padding: '10px',
                background: resource.locked
                    ? 'rgba(255, 255, 255, 0.05)'
                    : `${color}20`,
                border: resource.locked
                    ? '1px solid rgba(255, 255, 255, 0.1)'
                    : `1px solid ${color}`,
                borderRadius: '8px',
                color: resource.locked ? 'rgba(255, 255, 255, 0.4)' : color,
                fontSize: '14px',
                fontWeight: 600,
                cursor: resource.locked ? 'not-allowed' : 'pointer',
                fontFamily: 'Outfit, sans-serif',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                position: 'relative',
                zIndex: 2
            }}>
                {resource.locked ? (
                    <>
                        <Lock size={14} />
                        Odblokuj
                    </>
                ) : (
                    <>
                        <ExternalLink size={14} />
                        Otwórz
                    </>
                )}
            </button>
        </div>
    )
}
