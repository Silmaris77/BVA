'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Wrench, Zap, TrendingUp, Filter } from 'lucide-react'

interface Tool {
    id: string
    tool_id: string
    title: string
    description: string
    tier: number
    default_xp: number
    icon?: string
    config?: any
    unlocked?: boolean
    usage_count?: number
}

export default function ToolsPage() {
    const [tools, setTools] = useState<Tool[]>([])
    const [loading, setLoading] = useState(true)
    const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
    const [selectedTier, setSelectedTier] = useState<number | null>(null)

    useEffect(() => {
        async function loadTools() {
            try {
                const response = await fetch('/api/tools')
                const data = await response.json()
                setTools(data.tools || [])
            } catch (error) {
                console.error('Error loading tools:', error)
            } finally {
                setLoading(false)
            }
        }
        loadTools()
    }, [])

    const filteredTools = tools.filter(t => {
        if (selectedTier && t.tier !== selectedTier) return false
        if (selectedCategory && (t as any).category !== selectedCategory) return false
        return true
    })

    const getTierBadge = (tier: number) => {
        const tiers = {
            1: { label: 'Tier 1 - Podstawowy', color: '#00ff88', bg: 'rgba(0,255,136,0.2)' },
            2: { label: 'Tier 2 - Zaawansowany', color: '#ffd700', bg: 'rgba(255,215,0,0.2)' },
            3: { label: 'Tier 3 - Ekspert', color: '#ff4444', bg: 'rgba(255,68,68,0.2)' }
        }
        return tiers[tier as keyof typeof tiers] || tiers[1]
    }

    if (loading) {
        return (
            <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <div style={{ color: 'rgba(255,255,255,0.6)' }}>Ładowanie...</div>
            </div>
        )
    }

    return (
        <div className="page-content-wrapper" style={{ minHeight: '100vh' }}>
            {/* Header */}
            <div style={{ marginBottom: '48px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '12px' }}>
                    <div style={{ width: '56px', height: '56px', background: 'rgba(255,136,0,0.2)', borderRadius: '14px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <Wrench size={28} style={{ color: '#ff8800' }} />
                    </div>
                    <div>
                        <h1 style={{ fontSize: '36px', fontWeight: 700, margin: 0 }}>Narzędzia & Diagnostyka</h1>
                        <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: '16px', margin: '4px 0 0 0' }}>
                            Centrum narzędzi operacyjnych i testów kompetencji
                        </p>
                    </div>
                </div>
            </div>

            {/* Filters */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginBottom: '32px' }}>
                {/* Categories */}
                <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
                    <button
                        onClick={() => setSelectedCategory(null)}
                        style={{
                            padding: '10px 20px',
                            background: !selectedCategory ? 'white' : 'rgba(255,255,255,0.05)',
                            color: !selectedCategory ? 'black' : 'white',
                            border: `1px solid ${!selectedCategory ? 'white' : 'rgba(255,255,255,0.1)'}`,
                            borderRadius: '12px',
                            cursor: 'pointer',
                            fontSize: '14px',
                            fontWeight: 600
                        }}
                    >
                        Wszystkie
                    </button>
                    <button
                        onClick={() => setSelectedCategory('diagnosis')}
                        style={{
                            padding: '10px 20px',
                            background: selectedCategory === 'diagnosis' ? '#b000ff' : 'rgba(255,255,255,0.05)',
                            color: 'white',
                            border: `1px solid ${selectedCategory === 'diagnosis' ? '#b000ff' : 'rgba(255,255,255,0.1)'}`,
                            borderRadius: '12px',
                            cursor: 'pointer',
                            fontSize: '14px',
                            fontWeight: 600
                        }}
                    >
                        🧪 Diagnostyka
                    </button>
                    <button
                        onClick={() => setSelectedCategory('utility')}
                        style={{
                            padding: '10px 20px',
                            background: selectedCategory === 'utility' ? '#ff8800' : 'rgba(255,255,255,0.05)',
                            color: 'white',
                            border: `1px solid ${selectedCategory === 'utility' ? '#ff8800' : 'rgba(255,255,255,0.1)'}`,
                            borderRadius: '12px',
                            cursor: 'pointer',
                            fontSize: '14px',
                            fontWeight: 600
                        }}
                    >
                        🛠️ Narzędzia
                    </button>
                </div>

                {/* Tiers */}
                <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
                    <button
                        onClick={() => setSelectedTier(null)}
                        style={{
                            padding: '8px 16px',
                            background: 'transparent',
                            border: 'none',
                            color: !selectedTier ? 'white' : 'rgba(255,255,255,0.4)',
                            cursor: 'pointer',
                            fontSize: '13px',
                            fontWeight: 500
                        }}
                    >
                        Każdy poziom
                    </button>
                    {[1, 2, 3].map(tier => (
                        <button
                            key={tier}
                            onClick={() => setSelectedTier(tier)}
                            style={{
                                padding: '8px 16px',
                                background: selectedTier === tier ? 'rgba(255,255,255,0.1)' : 'transparent',
                                border: 'none',
                                borderRadius: '8px',
                                color: selectedTier === tier ? 'white' : 'rgba(255,255,255,0.4)',
                                cursor: 'pointer',
                                fontSize: '13px',
                                fontWeight: 500
                            }}
                        >
                            Tier {tier}
                        </button>
                    ))}
                </div>
            </div>

            {/* Tools Grid */}
            {filteredTools.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '80px 20px', color: 'rgba(255,255,255,0.5)' }}>
                    <Wrench size={64} style={{ opacity: 0.3, margin: '0 auto 20px' }} />
                    <p>Brak narzędzi</p>
                </div>
            ) : (
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fill, minmax(380px, 1fr))',
                    gap: '24px'
                }}>
                    {filteredTools.map(tool => {
                        const tierInfo = getTierBadge(tool.tier)
                        return (
                            <Link
                                key={tool.id}
                                href={`/tools/${tool.tool_id}`}
                                style={{
                                    background: 'rgba(20, 20, 35, 0.4)',
                                    backdropFilter: 'blur(15px)',
                                    border: '1px solid rgba(255,255,255,0.08)',
                                    borderRadius: '20px',
                                    padding: '24px',
                                    cursor: 'pointer',
                                    transition: 'all 0.3s',
                                    position: 'relative',
                                    overflow: 'hidden',
                                    textDecoration: 'none',
                                    color: 'white',
                                    display: 'block'
                                }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.transform = 'translateY(-5px)'
                                    e.currentTarget.style.borderColor = 'rgba(255,136,0,0.3)'
                                    e.currentTarget.style.boxShadow = '0 15px 40px rgba(0,0,0,0.4)'
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.transform = 'translateY(0)'
                                    e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)'
                                    e.currentTarget.style.boxShadow = 'none'
                                }}
                            >
                                {/* Top Border */}
                                <div style={{
                                    position: 'absolute',
                                    top: 0,
                                    left: 0,
                                    width: '100%',
                                    height: '4px',
                                    background: 'linear-gradient(90deg, #ff8800, #ffaa00)'
                                }} />

                                {/* Header */}
                                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px', marginBottom: '16px' }}>
                                    <div style={{
                                        width: '56px',
                                        height: '56px',
                                        background: 'rgba(255,136,0,0.2)',
                                        borderRadius: '14px',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        fontSize: '28px',
                                        flexShrink: 0
                                    }}>
                                        <Wrench size={28} style={{ color: '#ff8800' }} />
                                    </div>
                                    <div style={{ flex: 1 }}>
                                        <div style={{ fontSize: '18px', fontWeight: 600, marginBottom: '4px' }}>
                                            {tool.title}
                                        </div>
                                        <span style={{
                                            display: 'inline-block',
                                            padding: '4px 10px',
                                            background: tierInfo.bg,
                                            color: tierInfo.color,
                                            borderRadius: '12px',
                                            fontSize: '11px',
                                            fontWeight: 600,
                                            textTransform: 'uppercase'
                                        }}>
                                            {tierInfo.label}
                                        </span>
                                    </div>
                                </div>

                                {/* Description */}
                                <div style={{
                                    color: 'rgba(255,255,255,0.7)',
                                    fontSize: '14px',
                                    lineHeight: 1.6,
                                    marginBottom: '16px',
                                    minHeight: '60px'
                                }}>
                                    {tool.description}
                                </div>

                                {/* Footer */}
                                <div style={{
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    alignItems: 'center',
                                    paddingTop: '16px',
                                    borderTop: '1px solid rgba(255,255,255,0.05)'
                                }}>
                                    <div style={{ display: 'flex', gap: '16px', fontSize: '12px', color: 'rgba(255,255,255,0.5)' }}>
                                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                            <Zap size={14} /> +{tool.default_xp} XP
                                        </span>
                                        {tool.usage_count !== undefined && (
                                            <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                                <TrendingUp size={14} /> {tool.usage_count} użyć
                                            </span>
                                        )}
                                    </div>
                                    <div style={{
                                        padding: '8px 16px',
                                        background: 'linear-gradient(135deg, #ff8800, #cc6600)',
                                        borderRadius: '10px',
                                        fontSize: '13px',
                                        fontWeight: 600
                                    }}>
                                        Użyj
                                    </div>
                                </div>
                            </Link>
                        )
                    })}
                </div>
            )}
        </div>
    )
}
