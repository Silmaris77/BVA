'use client'

import { useState, useEffect } from 'react'
import { Check, X, RotateCcw } from 'lucide-react'

// Helper for class names
function classNames(...classes: (string | undefined | null | false)[]) {
    return classes.filter(Boolean).join(' ')
}

interface FractionVisualCardProps {
    title?: string
    question: string
    numerator: number
    denominator: number
    visualType?: 'pie' | 'bar'
    interactive?: boolean
    onComplete?: (correct: boolean) => void
}

export default function FractionVisualCard({
    title,
    question,
    numerator,
    denominator,
    visualType = 'pie',
    interactive = true,
    onComplete
}: FractionVisualCardProps) {
    const [selectedSegments, setSelectedSegments] = useState<number[]>([])
    const [isSubmitted, setIsSubmitted] = useState(false)
    const [isCorrect, setIsCorrect] = useState(false)

    // Reset when props change
    useEffect(() => {
        setSelectedSegments([])
        setIsSubmitted(false)
        setIsCorrect(false)
    }, [numerator, denominator])

    const toggleSegment = (index: number) => {
        if (!interactive || isSubmitted) return

        setSelectedSegments(prev => {
            if (prev.includes(index)) {
                return prev.filter(i => i !== index)
            } else {
                return [...prev, index]
            }
        })
    }

    const handleSubmit = () => {
        const correct = selectedSegments.length === numerator
        setIsCorrect(correct)
        setIsSubmitted(true)
        if (onComplete) onComplete(correct)
    }

    const handleReset = () => {
        setSelectedSegments([])
        setIsSubmitted(false)
        setIsCorrect(false)
    }

    // Pie Chart Generation Logic
    const renderPieChart = () => {
        const radius = 100
        const center = 100
        const size = 200

        return (
            <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="transform -rotate-90">
                {Array.from({ length: denominator }).map((_, i) => {
                    const startAngle = (i * 360) / denominator
                    const endAngle = ((i + 1) * 360) / denominator

                    // Specific logic for drawing SVG arcs
                    // Convert polar to cartesian
                    const x1 = center + radius * Math.cos((Math.PI * startAngle) / 180)
                    const y1 = center + radius * Math.sin((Math.PI * startAngle) / 180)
                    const x2 = center + radius * Math.cos((Math.PI * endAngle) / 180)
                    const y2 = center + radius * Math.sin((Math.PI * endAngle) / 180)

                    const largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1"

                    const d = [
                        "M", center, center,
                        "L", x1, y1,
                        "A", radius, radius, 0, largeArcFlag, 1, x2, y2,
                        "Z"
                    ].join(" ")

                    const isSelected = selectedSegments.includes(i)

                    return (
                        <path
                            key={i}
                            d={d}
                            onClick={() => toggleSegment(i)}
                            fill={isSelected ? 'var(--accent-purple)' : 'rgba(255, 255, 255, 0.1)'}
                            stroke="rgba(20, 20, 35, 1)"
                            strokeWidth="2"
                            className={classNames(
                                "transition-all duration-300",
                                interactive && !isSubmitted ? "cursor-pointer hover:opacity-80" : ""
                            )}
                        />
                    )
                })}
                {/* Center circle overlay for donut effect if desired, or just keep pie */}
            </svg>
        )
    }

    // Bar Chart Generation Logic
    const renderBarChart = () => {
        return (
            <div className="flex w-full h-16 rounded-xl overflow-hidden border border-white/10 gap-1 bg-black/20 p-1">
                {Array.from({ length: denominator }).map((_, i) => {
                    const isSelected = selectedSegments.includes(i)
                    return (
                        <div
                            key={i}
                            onClick={() => toggleSegment(i)}
                            className={classNames(
                                "flex-1 rounded-md transition-all duration-300 h-full",
                                isSelected ? "bg-[var(--accent-purple)]" : "bg-white/10",
                                interactive && !isSubmitted ? "cursor-pointer hover:bg-white/20" : ""
                            )}
                        />
                    )
                })}
            </div>
        )
    }

    return (
        <div className="w-full max-w-2xl mx-auto glass-card p-8 rounded-2xl border border-white/10 relative overflow-hidden">
            {/* Header Badge */}
            <div className="absolute top-4 left-4">
                <span className="bg-purple-500/10 text-purple-300 px-2 py-0.5 rounded text-[10px] font-bold uppercase border border-purple-500/20 tracking-wider">
                    Wizualizacja
                </span>
            </div>

            <div className="mt-6 mb-8 text-center">
                {title && <h3 className="text-gray-400 uppercase text-xs font-bold tracking-widest mb-2">{title}</h3>}
                <h2 className="text-xl md:text-2xl font-medium text-white">
                    {question}
                </h2>
                <div className="mt-2 text-gray-400 flex items-center justify-center gap-2">
                    Zaznaczono:
                    <span className={classNames("font-bold font-mono text-lg", selectedSegments.length === numerator && isSubmitted ? "text-green-400" : "text-white")}>
                        {selectedSegments.length}
                    </span>
                    /
                    <span className="font-bold font-mono text-lg text-white">
                        {denominator}
                    </span>
                </div>
            </div>

            {/* Visual Area */}
            <div className="flex justify-center mb-8">
                {visualType === 'pie' ? renderPieChart() : renderBarChart()}
            </div>

            {/* Controls */}
            {interactive && (
                <div className="flex justify-center">
                    {!isSubmitted ? (
                        <button
                            onClick={handleSubmit}
                            disabled={selectedSegments.length === 0}
                            className="bg-[var(--accent-blue)] text-black font-bold px-8 py-3 rounded-xl hover:brightness-110 transition disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_20px_rgba(0,212,255,0.3)]"
                        >
                            Sprawdź
                        </button>
                    ) : (
                        <div className="flex flex-col items-center gap-4 animate-in fade-in slide-in-from-bottom-2">
                            {isCorrect ? (
                                <div className="flex items-center gap-2 text-green-400 font-bold bg-green-500/10 px-6 py-3 rounded-xl border border-green-500/20">
                                    <Check size={24} /> Świetnie! To jest ułamek {numerator}/{denominator}.
                                </div>
                            ) : (
                                <div className="flex flex-col items-center gap-2">
                                    <div className="flex items-center gap-2 text-red-400 font-bold bg-red-500/10 px-6 py-3 rounded-xl border border-red-500/20">
                                        <X size={24} /> Niestety, zaznaczono {selectedSegments.length}/{denominator}.
                                    </div>
                                    <button
                                        onClick={handleReset}
                                        className="flex items-center gap-2 text-gray-400 hover:text-white transition text-sm underline mt-2"
                                    >
                                        <RotateCcw size={14} /> Spróbuj ponownie
                                    </button>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}
