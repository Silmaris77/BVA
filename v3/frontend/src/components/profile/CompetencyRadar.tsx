'use client'

import { useState, useMemo, useEffect } from 'react'
import { Target, Check } from 'lucide-react'

interface StatPoint {
    category: string
    points: number
    level: number
}

interface CompetencyRadarProps {
    stats: StatPoint[]
}

const ALL_CATEGORIES = ['Leadership', 'Sales', 'Strategy', 'Mindset', 'Technical', 'Communication']

export default function CompetencyRadar({ stats }: CompetencyRadarProps) {
    // Default to all categories active
    const [activeCategories, setActiveCategories] = useState<string[]>(ALL_CATEGORIES)
    const [hoveredStat, setHoveredStat] = useState<StatPoint | null>(null)

    // Helper to toggle categories
    const toggleCategory = (cat: string) => {
        if (activeCategories.includes(cat)) {
            // Prevent removing if only 3 left (triangle is min polygon)
            if (activeCategories.length <= 3) return
            setActiveCategories(prev => prev.filter(c => c !== cat))
        } else {
            setActiveCategories(prev => [...prev, cat])
        }
    }

    // Animation State
    const [animationProgress, setAnimationProgress] = useState(0)

    // Mount Animation
    useEffect(() => {
        let startTime: number
        let animationFrame: number

        const animate = (time: number) => {
            if (!startTime) startTime = time
            const progress = (time - startTime) / 1000 // 1 second duration

            // Ease out cubic
            const easeOutPromise = 1 - Math.pow(1 - Math.min(progress, 1), 3)

            setAnimationProgress(easeOutPromise)

            if (progress < 1) {
                animationFrame = requestAnimationFrame(animate)
            }
        }

        animationFrame = requestAnimationFrame(animate)

        return () => cancelAnimationFrame(animationFrame)
    }, []) // Run once on mount

    // Calculations
    const { points, polygonString, axisLines } = useMemo(() => {
        // Filter stats based on active categories
        // We preserve the order from ALL_CATEGORIES to keep the shape stable
        const currentStats = ALL_CATEGORIES
            .filter(cat => activeCategories.includes(cat))
            .map(cat => {
                const found = stats.find(s => s.category === cat)
                return found || { category: cat, points: 0, level: 1 }
            })

        const count = currentStats.length
        const radius = 150
        const centerX = 200
        const centerY = 200

        const calculatedPoints = currentStats.map((stat, i) => {
            const angle = (Math.PI * 2 * i) / count - Math.PI / 2 // Start from top

            // Apply animation progress to the value
            const finalValueRatio = Math.max(0.1, stat.points / 100)
            const animatedValueRatio = finalValueRatio * animationProgress

            const x = centerX + Math.cos(angle) * (radius * animatedValueRatio)
            const y = centerY + Math.sin(angle) * (radius * animatedValueRatio)

            const labelX = centerX + Math.cos(angle) * (radius + 30)
            const labelY = centerY + Math.sin(angle) * (radius + 30)

            return { x, y, labelX, labelY, stat }
        })

        const polygonString = calculatedPoints.map(p => `${p.x},${p.y}`).join(' ')

        // Axis lines (spider web)
        const axisLines = calculatedPoints.map(p => {
            // End of axis
            const endX = centerX + Math.cos(Math.atan2(p.y - centerY, p.x - centerX)) * radius
            const endY = centerY + Math.sin(Math.atan2(p.y - centerY, p.x - centerX)) * radius
            return { x1: centerX, y1: centerY, x2: endX, y2: endY }
        })

        return { points: calculatedPoints, polygonString, axisLines }
    }, [activeCategories, stats, animationProgress])


    return (
        <div style={{
            background: 'rgba(20, 20, 35, 0.4)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            borderRadius: '20px',
            padding: '32px',
            marginBottom: '32px'
        }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
                <h3 style={{ fontSize: '18px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Target size={20} color="#00ff88" />
                    Radar Kompetencji
                </h3>
            </div>

            {/* Configurator */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '32px' }}>
                {ALL_CATEGORIES.map(cat => {
                    const isActive = activeCategories.includes(cat)
                    const isDisabled = isActive && activeCategories.length <= 3

                    return (
                        <button
                            key={cat}
                            onClick={() => toggleCategory(cat)}
                            disabled={isDisabled}
                            style={{
                                padding: '6px 12px',
                                borderRadius: '20px',
                                background: isActive ? 'rgba(0, 255, 136, 0.15)' : 'rgba(255, 255, 255, 0.05)',
                                border: isActive ? '1px solid #00ff88' : '1px solid transparent',
                                color: isActive ? '#00ff88' : 'rgba(255, 255, 255, 0.4)',
                                fontSize: '11px',
                                fontWeight: 600,
                                cursor: isDisabled ? 'not-allowed' : 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '6px',
                                transition: 'all 0.2s',
                                opacity: isDisabled ? 0.5 : 1
                            }}
                        >
                            {isActive && <Check size={12} />}
                            {cat}
                        </button>
                    )
                })}
            </div>

            {/* Chart Area */}
            <div style={{ position: 'relative', height: '400px', display: 'flex', justifyContent: 'center' }}>
                <svg width="400" height="400" viewBox="0 0 400 400">
                    <defs>
                        <radialGradient id="radarGradient" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
                            <stop offset="0%" stopColor="#00ff88" stopOpacity="0.4" />
                            <stop offset="100%" stopColor="#00d4ff" stopOpacity="0.1" />
                        </radialGradient>
                    </defs>

                    {/* Background Grid Circles */}
                    {[1, 0.75, 0.5, 0.25].map((r, i) => (
                        <circle
                            key={i}
                            cx="200"
                            cy="200"
                            r={150 * r}
                            fill={i === 0 ? 'rgba(0,0,0,0.2)' : 'none'}
                            stroke="rgba(255,255,255,0.05)"
                            strokeWidth="1"
                        />
                    ))}

                    {/* Axes */}
                    {axisLines.map((line, i) => (
                        <line
                            key={i}
                            x1={line.x1}
                            y1={line.y1}
                            x2={line.x2}
                            y2={line.y2}
                            stroke="rgba(255,255,255,0.1)"
                            strokeWidth="1"
                        />
                    ))}

                    {/* The Data Polygon */}
                    <polygon
                        points={polygonString}
                        fill="url(#radarGradient)"
                        stroke="#00ff88"
                        strokeWidth="2"
                        style={{ filter: 'drop-shadow(0 0 8px rgba(0, 255, 136, 0.3))' }}
                    />

                    {/* Data Points */}
                    {points.map((p, i) => (
                        <g key={i}>
                            {/* Interactive Hit Area */}
                            <circle
                                cx={p.x}
                                cy={p.y}
                                r="8"
                                fill="transparent"
                                onMouseEnter={() => setHoveredStat(p.stat)}
                                onMouseLeave={() => setHoveredStat(null)}
                                style={{ cursor: 'pointer' }}
                            />
                            {/* Visible Dot */}
                            <circle
                                cx={p.x}
                                cy={p.y}
                                r="4"
                                fill="#fff"
                                stroke="#00ff88"
                                strokeWidth="2"
                                style={{ pointerEvents: 'none' }}
                            />
                            {/* Labels */}
                            <text
                                x={p.labelX}
                                y={p.labelY}
                                textAnchor="middle"
                                alignmentBaseline="middle"
                                fill={activeCategories.includes(p.stat.category) ? 'white' : 'rgba(255,255,255,0.3)'}
                                fontSize="12"
                                fontWeight="600"
                                onClick={() => toggleCategory(p.stat.category)}
                                style={{ cursor: 'pointer', transition: 'fill 0.2s' }}
                            >
                                {p.stat.category}
                            </text>
                        </g>
                    ))}
                </svg>

                {/* Hover Tooltip Overlay */}
                {hoveredStat && (
                    <div style={{
                        position: 'absolute',
                        top: '50%',
                        left: '50%',
                        transform: 'translate(-50%, -50%)',
                        background: 'rgba(0, 0, 0, 0.8)',
                        backdropFilter: 'blur(8px)',
                        border: '1px solid #00ff88',
                        padding: '12px 20px',
                        borderRadius: '12px',
                        textAlign: 'center',
                        pointerEvents: 'none',
                        boxShadow: '0 0 20px rgba(0, 255, 136, 0.2)'
                    }}>
                        <div style={{ fontSize: '12px', color: 'rgba(255,255,255,0.6)', marginBottom: '4px' }}>
                            {hoveredStat.category}
                        </div>
                        <div style={{ fontSize: '24px', fontWeight: 700, color: '#00ff88' }}>
                            {hoveredStat.points}
                        </div>
                        <div style={{ fontSize: '10px', color: '#00ff88', textTransform: 'uppercase', letterSpacing: '1px' }}>
                            XP Points
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
