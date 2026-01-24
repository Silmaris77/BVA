'use client'

import { useEffect, useState } from 'react'
import { Flame } from 'lucide-react'

interface ActivityDay {
    date: string
    count: number
    level: number
}

interface ActivityData {
    heatmap: ActivityDay[]
    total_xp_year: number
    active_days: number
}

export default function ActivityHeatmap() {
    const [data, setData] = useState<ActivityData | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function fetchData() {
            try {
                const res = await fetch('/api/user/activity')
                if (res.ok) {
                    const json = await res.json()
                    setData(json)
                }
            } catch (e) {
                console.error('Failed to load activity', e)
            } finally {
                setLoading(false)
            }
        }
        fetchData()
    }, [])

    if (loading) {
        return (
            <div style={{ padding: '20px', textAlign: 'center', color: 'rgba(255,255,255,0.4)' }}>
                Ładowanie mapy aktywności...
            </div>
        )
    }

    // Generate last 365 days grid
    const today = new Date()
    const days = []
    for (let i = 0; i < 365; i++) {
        const d = new Date()
        d.setDate(today.getDate() - (364 - i))
        days.push(d)
    }

    // Map data for fast lookup
    const dataMap = new Map((data?.heatmap || []).map(d => [d.date, d]))

    // Color logic
    const getColor = (level: number) => {
        switch (level) {
            case 1: return 'rgba(176, 0, 255, 0.3)' // Dim Purple
            case 2: return 'rgba(176, 0, 255, 0.6)' // Mid Purple
            case 3: return 'rgba(0, 212, 255, 0.6)' // Mid Cyan
            case 4: return '#00d4ff'                // Bright Cyan
            default: return 'rgba(255, 255, 255, 0.05)' // Inactive
        }
    }

    const getGlow = (level: number) => {
        if (level === 4) return '0 0 8px rgba(0, 212, 255, 0.5)'
        return 'none'
    }

    // Tooltip State
    const [hovered, setHovered] = useState<{ date: string; xp: number; x: number; y: number } | null>(null)

    // Helper for formatting date: "24 sty 2024"
    const formatDate = (dateStr: string) => {
        const d = new Date(dateStr)
        return d.toLocaleDateString('pl-PL', { day: 'numeric', month: 'short', year: 'numeric' })
    }

    return (
        <div style={{
            background: 'rgba(20, 20, 35, 0.4)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            borderRadius: '20px',
            padding: '24px',
            marginBottom: '32px',
            position: 'relative' // For tooltip context if needed, though we use fixed/absolute from page
        }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
                <h3 style={{ fontSize: '18px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Flame size={20} color="#ff8800" />
                    Aktywność (Ostatni Rok)
                </h3>
                <div style={{ fontSize: '13px', color: 'rgba(255, 255, 255, 0.6)' }}>
                    <span style={{ color: '#fff', fontWeight: 700 }}>{data?.total_xp_year.toLocaleString()} XP</span> w tym roku
                </div>
            </div>

            {/* Custom Tooltip Portal/Overlay */}
            {hovered && (
                <div style={{
                    position: 'fixed',
                    top: hovered.y - 45, // Above the cell
                    left: hovered.x,
                    transform: 'translateX(-50%)',
                    background: 'rgba(0, 0, 0, 0.9)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    padding: '8px 12px',
                    borderRadius: '8px',
                    fontSize: '12px',
                    color: 'white',
                    pointerEvents: 'none',
                    zIndex: 100,
                    whiteSpace: 'nowrap',
                    boxShadow: '0 4px 12px rgba(0,0,0,0.5)',
                    backdropFilter: 'blur(4px)'
                }}>
                    <div style={{ fontWeight: 700, color: '#ff8800' }}>{hovered.xp} XP</div>
                    <div style={{ color: 'rgba(255,255,255,0.7)', fontSize: '10px' }}>{formatDate(hovered.date)}</div>
                    {/* Tiny arrow */}
                    <div style={{
                        position: 'absolute',
                        bottom: '-4px',
                        left: '50%',
                        transform: 'translateX(-50%) rotate(45deg)',
                        width: '8px',
                        height: '8px',
                        background: 'rgba(0,0,0,0.9)',
                        borderRight: '1px solid rgba(255, 255, 255, 0.2)',
                        borderBottom: '1px solid rgba(255, 255, 255, 0.2)'
                    }} />
                </div>
            )}

            {/* Heatmap Grid */}
            <div style={{
                display: 'flex',
                gap: '4px',
                flexWrap: 'wrap',
                maxWidth: '100%',
                overflowX: 'auto',
                paddingBottom: '8px'
            }}>
                {/* 
                   We arrange in generic consecutive squares for simplicity
                   Real GitHub graph is column-major weeks, but simple row-major is easier to read on mobile 
                   Wait, GitHub style 7 rows is better.
                */}
                <div style={{
                    display: 'grid',
                    gridTemplateRows: 'repeat(7, 1fr)',
                    gridAutoFlow: 'column',
                    gap: '4px'
                }}>
                    {days.map((date, i) => {
                        const dateStr = date.toISOString().split('T')[0]
                        const activity = dataMap.get(dateStr)
                        const level = activity?.level || 0
                        const count = activity?.count || 0

                        return (
                            <div
                                key={dateStr}
                                onMouseEnter={(e) => {
                                    const rect = e.currentTarget.getBoundingClientRect()
                                    setHovered({
                                        date: dateStr,
                                        xp: count,
                                        x: rect.left + rect.width / 2,
                                        y: rect.top
                                    })
                                }}
                                onMouseLeave={() => setHovered(null)}
                                style={{
                                    width: '12px',
                                    height: '12px',
                                    borderRadius: '2px',
                                    background: getColor(level),
                                    boxShadow: getGlow(level),
                                    border: level > 0 ? `1px solid ${getColor(level)}` : 'none',
                                    cursor: 'pointer',
                                    transition: 'transform 0.1s'
                                }}
                            />
                        )
                    })}
                </div>
            </div>

            {/* Legend */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '11px', color: 'rgba(255,255,255,0.4)', marginTop: '16px', justifyContent: 'flex-end' }}>
                Less
                <div style={{ width: '10px', height: '10px', background: getColor(0), borderRadius: '2px' }} />
                <div style={{ width: '10px', height: '10px', background: getColor(1), borderRadius: '2px' }} />
                <div style={{ width: '10px', height: '10px', background: getColor(2), borderRadius: '2px' }} />
                <div style={{ width: '10px', height: '10px', background: getColor(3), borderRadius: '2px' }} />
                <div style={{ width: '10px', height: '10px', background: getColor(4), borderRadius: '2px', boxShadow: getGlow(4) }} />
                More
            </div>
        </div>
    )
}
