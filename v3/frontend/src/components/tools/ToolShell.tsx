'use client'

import { ArrowLeft, Wrench, Zap, TrendingUp, BookOpen, Brain, FileText } from 'lucide-react'
import Link from 'next/link'
import { ReactNode } from 'react'

interface ToolShellProps {
    tool: {
        id: string
        title: string
        description: string
        tier: number
        default_xp: number
        usage_count?: number // Optional since it might be enriched later
    }
    children: ReactNode
    stats?: { label: string; value: string | number }[]
    tips?: string[]
}

export default function ToolShell({ tool, children, stats, tips }: ToolShellProps) {
    const getTierBadge = (tier: number) => {
        const tiers = {
            1: { label: 'Tier 1 - Podstawowy', color: '#00ff88', bg: 'rgba(0,255,136,0.2)' },
            2: { label: 'Tier 2 - Zaawansowany', color: '#ffd700', bg: 'rgba(255,215,0,0.2)' },
            3: { label: 'Tier 3 - Ekspert', color: '#ff4444', bg: 'rgba(255,68,68,0.2)' }
        }
        return tiers[tier as keyof typeof tiers] || tiers[1]
    }

    const tierInfo = getTierBadge(tool.tier)

    return (
        <div style={{ minHeight: '100vh', padding: '40px 48px' }}>
            {/* Back Button */}
            <Link
                href="/tools"
                style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '10px 16px',
                    background: 'rgba(255,255,255,0.05)',
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: '10px',
                    color: 'rgba(255,255,255,0.8)',
                    textDecoration: 'none',
                    marginBottom: '32px',
                    transition: 'all 0.3s'
                }}
            >
                <ArrowLeft size={16} />
                Powrót do narzędzi
            </Link>

            {/* Tool Header */}
            <div style={{
                background: 'rgba(20, 20, 35, 0.4)',
                backdropFilter: 'blur(15px)',
                border: '1px solid rgba(255,255,255,0.08)',
                borderRadius: '20px',
                padding: '32px',
                marginBottom: '32px',
                position: 'relative',
                overflow: 'hidden'
            }}>
                {/* Top Border */}
                <div style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '4px',
                    background: 'linear-gradient(90deg, #ff8800, #ffaa00)'
                }} />

                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '20px', marginBottom: '16px' }}>
                    <div style={{
                        width: '72px',
                        height: '72px',
                        background: 'rgba(255,136,0,0.2)',
                        borderRadius: '18px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        flexShrink: 0
                    }}>
                        <Wrench size={36} style={{ color: '#ff8800' }} />
                    </div>
                    <div style={{ flex: 1 }}>
                        <h1 style={{ fontSize: '32px', fontWeight: 700, marginBottom: '8px', color: '#fff' }}>
                            {tool.title}
                        </h1>
                        <span style={{
                            display: 'inline-block',
                            padding: '6px 14px',
                            background: tierInfo.bg,
                            color: tierInfo.color,
                            borderRadius: '16px',
                            fontSize: '12px',
                            fontWeight: 600,
                            textTransform: 'uppercase'
                        }}>
                            {tierInfo.label}
                        </span>
                    </div>
                </div>
                <p style={{ color: 'rgba(255,255,255,0.7)', fontSize: '16px', lineHeight: 1.6, marginTop: '16px' }}>
                    {tool.description}
                </p>
            </div>

            {/* Body */}
            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
                {/* Main Content */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                    {children}

                    {/* Tips (if provided) */}
                    {tips && tips.length > 0 && (
                        <div style={{
                            background: 'rgba(20, 20, 35, 0.4)',
                            backdropFilter: 'blur(15px)',
                            border: '1px solid rgba(255,255,255,0.08)',
                            borderRadius: '20px',
                            padding: '24px'
                        }}>
                            <h4 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '12px', color: '#ff8800' }}>
                                💡 Wskazówki
                            </h4>
                            <ul style={{ margin: 0, paddingLeft: '20px', color: 'rgba(255,255,255,0.7)', fontSize: '14px', lineHeight: 1.6 }}>
                                {tips.map((tip, idx) => (
                                    <li key={idx} style={{ marginBottom: '4px' }}>{tip}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>

                {/* Sidebar */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                    {/* Stats */}
                    <div style={{
                        background: 'rgba(20, 20, 35, 0.4)',
                        backdropFilter: 'blur(15px)',
                        border: '1px solid rgba(255,255,255,0.08)',
                        borderRadius: '16px',
                        padding: '24px'
                    }}>
                        <h4 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '12px', color: '#ff8800' }}>
                            📊 Statystyki
                        </h4>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                            <div style={{ background: 'rgba(0,0,0,0.2)', padding: '12px', borderRadius: '10px', textAlign: 'center' }}>
                                <div style={{ fontSize: '20px', fontWeight: 700, color: '#ff8800' }}>+{tool.default_xp}</div>
                                <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.5)', marginTop: '4px' }}>XP za użycie</div>
                            </div>
                            <div style={{ background: 'rgba(0,0,0,0.2)', padding: '12px', borderRadius: '10px', textAlign: 'center' }}>
                                <div style={{ fontSize: '20px', fontWeight: 700, color: '#ff8800' }}>
                                    {tool.usage_count || 0}
                                </div>
                                <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.5)', marginTop: '4px' }}>Twoje użycia</div>
                            </div>
                        </div>
                    </div>

                    {/* Related Content (Static for now) */}
                    <div style={{
                        background: 'rgba(20, 20, 35, 0.4)',
                        backdropFilter: 'blur(15px)',
                        border: '1px solid rgba(255,255,255,0.08)',
                        borderRadius: '16px',
                        padding: '24px'
                    }}>
                        <h4 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '12px', color: '#ff8800' }}>
                            📚 Zasoby
                        </h4>
                        <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.7)' }}>
                            <div style={{ padding: '8px 0', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                <FileText size={14} style={{ display: 'inline', marginRight: '8px' }} />
                                Tabele i dokumenty
                            </div>
                            <div style={{ padding: '8px 0' }}>
                                <BookOpen size={14} style={{ display: 'inline', marginRight: '8px' }} />
                                Poradniki
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
