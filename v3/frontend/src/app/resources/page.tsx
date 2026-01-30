'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { supabase } from '@/lib/supabase'
import Link from 'next/link'
import { Search, Bell, Zap, Brain, Library, BookOpen, Filter, Lock, ExternalLink, FileText, Table, Video, Book, TrendingUp, Mail, LayoutTemplate, Download } from 'lucide-react'

interface Resource {
    id: string
    title: string
    description: string
    resource_type: string
    category: string
    locked: boolean
    tier: number
    image_url?: string
    download_xp: number
    external_url?: string
}

export default function ResourcesPage() {
    const { user, profile, loading: authLoading } = useAuth()
    const router = useRouter()
    const [searchTerm, setSearchTerm] = useState('')
    const [hoveredTab, setHoveredTab] = useState<string | null>(null)

    useEffect(() => {
        if (!authLoading && !user) {
            router.push('/auth/login')
        }
    }, [user, authLoading, router])

    const [resources, setResources] = useState<Resource[]>([])
    const [loading, setLoading] = useState(true)
    const [downloadingId, setDownloadingId] = useState<string | null>(null)

    useEffect(() => {
        async function loadResources() {
            if (!user) return

            try {
                const { data, error } = await supabase
                    .from('resources')
                    .select('*')

                if (error) throw error

                // Inject Static Resources (e.g. Degen Atlas)
                const staticResources: Resource[] = [{
                    id: 'degen-atlas-static',
                    title: 'Atlas Degenów 🌍',
                    description: 'Kompendium 8 typów osobowości inwestycyjnych. Poznaj ich mocne i słabe strony, aby lepiej inwestować.',
                    resource_type: 'article',
                    category: 'Mindset',
                    locked: false,
                    tier: 1,
                    download_xp: 50,
                    external_url: '/learning/resources/degen-atlas'
                }]

                setResources([...staticResources, ...(data || [])])
            } catch (error) {
                console.error('Error loading resources:', error)
            } finally {
                setLoading(false)
            }
        }
        loadResources()
    }, [user])

    const handleDownload = async (resource: Resource) => {
        if (resource.locked) return { success: false, xp: 0 }

        // Handle External/Internal Links without downloading
        if (resource.external_url) {
            if (resource.external_url.startsWith('/')) {
                router.push(resource.external_url)
            } else {
                window.open(resource.external_url, '_blank')
            }
            return { success: true, xp: resource.download_xp || 0 }
        }

        setDownloadingId(resource.id)
        try {
            const response = await fetch(`/api/resources/${resource.id}/download`, {
                method: 'POST'
            })
            const data = await response.json()

            if (data.success) {
                if (data.url && data.url !== '#') {
                    // Small delay to let animation start
                    setTimeout(() => window.open(data.url, '_blank'), 500)
                } else {
                    // Demo fallback - silent
                    console.log('Demo link clicked')
                }
                return { success: true, xp: data.xp_awarded || 0 }
            } else {
                alert(data.error || 'Błąd pobierania')
                return { success: false, xp: 0 }
            }
        } catch (error) {
            console.error('Download error:', error)
            return { success: false, xp: 0 }
        } finally {
            setDownloadingId(null)
        }
    }

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


            {/* Content */}
            <div className="page-content-wrapper">
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
                            <ResourceCard
                                key={resource.id}
                                resource={resource}
                                onDownload={() => handleDownload(resource)}
                                isDownloading={downloadingId === resource.id}
                            />
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
                        <ResourceCard
                            key={resource.id}
                            resource={resource}
                            onDownload={() => handleDownload(resource)}
                            isDownloading={downloadingId === resource.id}
                        />
                    ))}
                </div>
            </div>
        </div >
    )
}

function ResourceCard({
    resource,
    onDownload,
    isDownloading
}: {
    resource: Resource,
    onDownload: () => Promise<{ success: boolean, xp: number }>,
    isDownloading: boolean
}) {
    const [showAnim, setShowAnim] = useState(false)
    const [xpAmount, setXpAmount] = useState(0)

    const handleClick = async () => {
        if (!resource.locked && !isDownloading) {
            const result = await onDownload()
            if (result.success && result.xp > 0) {
                setXpAmount(result.xp)
                setShowAnim(true)
                setTimeout(() => setShowAnim(false), 2000)
            }
        }
    }

    const getIconForType = (type: string) => {
        switch (type) {
            case 'article': return FileText
            case 'template': return LayoutTemplate
            case 'video': return Video
            case 'ebook': return Book
            case 'case_study': return TrendingUp
            case 'tool': return Zap
            case 'pdf': return FileText
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
            'Wiedza produktowa': '#00d4ff',
            'Product': '#00d4ff',
            'Narzędzia': '#ffd700',
            'Organizacja': '#ff4757'
        }
        return colors[category] || '#00d4ff'
    }

    const Icon = getIconForType(resource.resource_type)
    const color = getCategoryColor(resource.category)

    return (
        <div
            style={{
                background: 'rgba(255, 255, 255, 0.03)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.08)',
                borderRadius: '16px',
                padding: '20px',
                cursor: resource.locked ? 'not-allowed' : 'pointer',
                transition: 'all 0.2s',
                position: 'relative',
                overflow: 'hidden',
                minHeight: '220px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
            }}
            onClick={handleClick}
            onMouseEnter={(e) => {
                if (resource.locked) return
                e.currentTarget.style.borderColor = color
                e.currentTarget.style.transform = 'translateY(-4px)'
                e.currentTarget.style.boxShadow = `0 12px 40px ${color}33`

                // Show download overlay
                const overlay = e.currentTarget.querySelector('.card-overlay') as HTMLElement
                if (overlay) overlay.style.opacity = '1'

                // Zoom image slightly
                const img = e.currentTarget.querySelector('.card-bg-image') as HTMLElement
                if (img) img.style.transform = 'scale(1.1)'
            }}
            onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.08)'
                e.currentTarget.style.transform = 'translateY(0)'
                e.currentTarget.style.boxShadow = 'none'

                const overlay = e.currentTarget.querySelector('.card-overlay') as HTMLElement
                if (overlay) overlay.style.opacity = '0'

                const img = e.currentTarget.querySelector('.card-bg-image') as HTMLElement
                if (img) img.style.transform = 'scale(1)'
            }}
        >
            {/* XP Floating Animation */}
            {showAnim && (
                <>
                    <div style={{
                        position: 'absolute',
                        top: '50%',
                        left: '50%',
                        transform: 'translate(-50%, -50%)',
                        color: '#ffd700',
                        fontSize: '32px',
                        fontWeight: 800,
                        textShadow: '0 4px 15px rgba(0,0,0,0.8)',
                        pointerEvents: 'none',
                        zIndex: 20,
                        animation: 'floatUp 1.5s ease-out forwards',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        width: '100%',
                        justifyContent: 'center'
                    }}>
                        <Zap size={32} fill="#ffd700" />
                        +{xpAmount} XP
                    </div>
                    <style jsx>{`
                    @keyframes floatUp {
                        0% { transform: translate(-50%, 0) scale(0.5); opacity: 0; }
                        20% { transform: translate(-50%, -20px) scale(1.2); opacity: 1; }
                        80% { transform: translate(-50%, -80px) scale(1); opacity: 1; }
                        100% { transform: translate(-50%, -100px) scale(0.8); opacity: 0; }
                    }
                `}</style>
                </>
            )}

            {/* Background Image */}
            {resource.image_url && (
                <>
                    <div
                        className="card-bg-image"
                        style={{
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            width: '100%',
                            height: '100%',
                            backgroundImage: `url(${resource.image_url})`,
                            backgroundSize: 'cover',
                            backgroundPosition: 'center',
                            opacity: 0.15,
                            transition: 'transform 0.4s ease',
                            zIndex: 0
                        }}
                    />
                    <div style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: '100%',
                        background: 'linear-gradient(to bottom, rgba(20,20,35,0.3), rgba(20,20,35,0.85))',
                        zIndex: 1
                    }} />
                </>
            )}

            {/* Content Container (z-index 2) */}
            <div style={{ position: 'relative', zIndex: 2 }}>

                {/* Lock Badge */}
                {resource.locked && (
                    <div style={{
                        position: 'absolute',
                        top: 0,
                        right: 0,
                        padding: '4px 8px',
                        background: 'rgba(0, 0, 0, 0.6)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '6px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px',
                        fontSize: '11px',
                        color: 'rgba(255, 255, 255, 0.6)',
                        backdropFilter: 'blur(4px)'
                    }}>
                        <Lock size={12} />
                        Zablokowane
                    </div>
                )}

                {/* Top Row: Icon + Type */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                    <div style={{
                        width: '48px',
                        height: '48px',
                        borderRadius: '12px',
                        background: `${color}20`,
                        border: `1px solid ${color}`,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: color,
                    }}>
                        <Icon size={24} />
                    </div>

                    {!resource.locked && resource.download_xp > 0 && (
                        <div style={{
                            padding: '4px 8px',
                            borderRadius: '12px',
                            background: 'rgba(255, 215, 0, 0.1)',
                            border: '1px solid rgba(255, 215, 0, 0.3)',
                            color: '#ffd700',
                            fontSize: '11px',
                            fontWeight: 700,
                            display: 'flex',
                            alignItems: 'center',
                            gap: '4px'
                        }}>
                            <Zap size={10} />
                            +{resource.download_xp} XP
                        </div>
                    )}
                </div>

                {/* Category */}
                <div style={{
                    fontSize: '11px',
                    color: color,
                    marginBottom: '4px',
                    fontWeight: 600,
                    textTransform: 'uppercase',
                    letterSpacing: '0.5px'
                }}>
                    {resource.category}
                </div>

                {/* Title */}
                <h3 style={{
                    fontSize: '18px',
                    fontWeight: 600,
                    marginBottom: '8px',
                    lineHeight: 1.3,
                    color: '#fff'
                }}>
                    {resource.title}
                </h3>

                {/* Description */}
                <p style={{
                    fontSize: '13px',
                    color: 'rgba(255, 255, 255, 0.6)',
                    lineHeight: 1.5,
                    marginBottom: '16px',
                    display: '-webkit-box',
                    WebkitLineClamp: 3,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden'
                }}>
                    {resource.description}
                </p>
            </div>

            {/* Action Button (Overlay) */}
            <div
                className="card-overlay"
                style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    background: `rgba(0,0,0,0.6)`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    opacity: 0,
                    transition: 'opacity 0.2s',
                    zIndex: 10,
                    pointerEvents: 'none' // allow click through to card
                }}
            >
                <div style={{
                    padding: '12px 24px',
                    background: color,
                    borderRadius: '30px',
                    color: '#000',
                    fontWeight: 700,
                    fontSize: '14px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    boxShadow: `0 4px 20px ${color}66`
                }}>
                    {isDownloading ? (
                        <>Pobieranie...</>
                    ) : (
                        <>
                            <Download size={18} />
                            Pobierz
                        </>
                    )}
                </div>
            </div>
        </div>
    )
}
