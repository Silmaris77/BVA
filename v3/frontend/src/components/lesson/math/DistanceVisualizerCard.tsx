'use client'

import { useState, useEffect } from 'react'
import { CheckCircle2, Ruler, ArrowLeftRight } from 'lucide-react'
import confetti from 'canvas-confetti'
import MathRenderer from './MathRenderer'

interface DistanceVisualizerCardProps {
    title?: string
    question: string
    numbers: number[]
    correctDistance: number
    showSymmetry?: boolean
    compareMode?: boolean
    explanation?: string
}

export default function DistanceVisualizerCard({
    title = 'Wizualizacja odległości',
    question,
    numbers,
    correctDistance,
    showSymmetry = false,
    compareMode = false,
    explanation
}: DistanceVisualizerCardProps) {
    const [selectedNumber, setSelectedNumber] = useState<number | null>(null)
    const [isAnswered, setIsAnswered] = useState(showSymmetry || compareMode) // Auto-answer in display modes
    const [showAnswer, setShowAnswer] = useState(false)

    // Auto-show visualization after 1 second
    useEffect(() => {
        const timer = setTimeout(() => {
            setShowAnswer(true)
            if (showSymmetry || compareMode) {
                setIsAnswered(true) // Ensure answered state for display modes
            }
        }, 800)
        return () => clearTimeout(timer)
    }, [showSymmetry, compareMode])

    const handleNumberClick = (number: number) => {
        if (isAnswered) return
        
        setSelectedNumber(number)
        setIsAnswered(true)

        if (Math.abs(number) === correctDistance) {
            triggerConfetti()
        }
    }

    const triggerConfetti = () => {
        confetti({
            particleCount: 60,
            spread: 70,
            origin: { y: 0.6 },
            colors: ['#00d4ff', '#00ff88', '#ffd700']
        })
    }

    // Calculate scale for axis
    const maxAbs = Math.max(...numbers.map(Math.abs), 10)
    const scale = 100 / maxAbs // Scale to fit in 100% width

    const getPositionPercent = (num: number) => {
        return 50 + (num * scale * 0.4) // Center at 50%, scale by 40% of container
    }

    const getDistanceColor = (num: number) => {
        const distance = Math.abs(num)
        if (distance === correctDistance) {
            return '#00ff88' // Green for correct
        }
        return '#00d4ff' // Blue for others
    }

    return (
        <div style={{
            maxWidth: '900px',
            width: '100%',
            position: 'relative',
            background: 'rgba(20, 20, 35, 0.6)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            border: '1px solid rgba(0, 212, 255, 0.2)',
            borderRadius: '20px',
            padding: '40px',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
            borderLeft: '4px solid #00d4ff'
        }}>
            {/* Badge */}
            <div style={{
                position: 'absolute',
                top: '20px',
                left: '20px',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                fontSize: '11px',
                textTransform: 'uppercase',
                letterSpacing: '1px',
                color: '#00d4ff',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(0, 212, 255, 0.1)',
                border: '1px solid rgba(0, 212, 255, 0.2)',
                borderRadius: '20px'
            }}>
                <Ruler size={12} />
                WIZUALIZACJA ODLEGŁOŚCI
            </div>

            {/* Title */}
            <h2 style={{
                fontSize: '28px',
                fontWeight: 700,
                marginBottom: '12px',
                marginTop: '20px',
                color: '#00d4ff',
                textAlign: 'center'
            }}>
                {title}
            </h2>
            
            {question && (
                <div className="text-gray-300 text-center mb-8 text-lg">
                    <MathRenderer content={question} />
                </div>
            )}

            {/* Interactive Number Line Visualization */}
            <div className="bg-black/30 rounded-xl p-10 mb-6 border border-white/10 overflow-hidden">
                <div className="relative" style={{ height: '280px' }}>
                    {/* Number Line */}
                    <div className="absolute top-1/2 left-0 right-0 h-1 bg-gradient-to-r from-purple-500/30 via-white/50 to-purple-500/30 transform -translate-y-1/2" />
                    
                    {/* Zero Point */}
                    <div 
                        className="absolute top-1/2 transform -translate-x-1/2 -translate-y-1/2"
                        style={{ left: '50%' }}
                    >
                        <div className="w-4 h-4 bg-white rounded-full shadow-lg shadow-white/50" />
                        <div className="text-white text-sm font-bold mt-2 text-center">0</div>
                    </div>

                    {/* Distance Lines and Numbers */}
                    {showAnswer && numbers.map((num, index) => {
                        const position = getPositionPercent(num)
                        const distance = Math.abs(num)
                        const color = getDistanceColor(num)
                        const isSelected = selectedNumber === num
                        const isCorrect = distance === correctDistance

                        return (
                            <div key={index}>
                                {/* Solid Distance Line from zero to number */}
                                <div 
                                    className="absolute top-1/2 transform -translate-y-1/2 transition-all duration-700"
                                    style={{
                                        left: num >= 0 ? '50%' : `${position}%`,
                                        width: `${Math.abs(position - 50)}%`,
                                        height: '4px',
                                        background: color,
                                        opacity: 0.6,
                                        borderRadius: '2px'
                                    }}
                                />

                                {/* Number Point */}
                                <button
                                    onClick={() => !compareMode && handleNumberClick(num)}
                                    disabled={compareMode || isAnswered}
                                    className={`absolute transform -translate-x-1/2 transition-all duration-500 ${!compareMode && !isAnswered ? 'cursor-pointer hover:scale-125' : ''}`}
                                    style={{
                                        left: `${position}%`,
                                        top: '50%',
                                        marginTop: '-10px'
                                    }}
                                >
                                    <div 
                                        className={`w-6 h-6 rounded-full transition-all duration-300 ${
                                            isSelected && isCorrect ? 'ring-4 ring-green-400' :
                                            isSelected && !isCorrect ? 'ring-4 ring-red-400' :
                                            isCorrect && isAnswered ? 'ring-4 ring-green-400/50' : ''
                                        }`}
                                        style={{
                                            background: color,
                                            boxShadow: `0 0 20px ${color}80`,
                                            transform: isSelected ? 'scale(1.3)' : 'scale(1)'
                                        }}
                                    />
                                    <div 
                                        className="text-white font-bold text-center text-xl absolute"
                                        style={{ 
                                            color,
                                            top: num >= 0 ? '-35px' : '35px',
                                            left: '50%',
                                            transform: 'translateX(-50%)',
                                            whiteSpace: 'nowrap'
                                        }}
                                    >
                                        {num}
                                    </div>
                                    
                                    {/* Distance Label */}
                                    {isAnswered && (
                                        <div 
                                            className="text-xs font-semibold text-center px-2 py-1 rounded-full animate-fadeIn absolute"
                                            style={{
                                                background: `${color}20`,
                                                color: color,
                                                border: `1px solid ${color}40`,
                                                top: num >= 0 ? '40px' : '-50px',
                                                left: '50%',
                                                transform: 'translateX(-50%)',
                                                whiteSpace: 'nowrap'
                                            }}
                                        >
                                            {distance} {distance === 1 ? 'jednostka' : distance < 5 ? 'jednostki' : 'jednostek'}
                                        </div>
                                    )}
                                </button>
                            </div>
                        )
                    })}
                </div>

                {/* Comparison Result */}
                {compareMode && isAnswered && (
                    <div className="mt-6 text-center">
                        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/20 border border-blue-500/30">
                            <CheckCircle2 size={20} className="text-blue-400" />
                            <span className="text-blue-400 font-semibold">
                                Liczba {numbers.find(n => Math.abs(n) === correctDistance)} jest dalej od zera
                            </span>
                        </div>
                    </div>
                )}
            </div>

            {/* Value Display */}
            {isAnswered && (
                <div className="bg-gradient-to-r from-blue-500/10 to-green-500/10 rounded-xl p-6 mb-6 border border-white/10 animate-fadeIn">
                    <div className="text-center">
                        <div className="text-sm text-gray-400 mb-2">Wartości bezwzględne:</div>
                        <div className="flex justify-center gap-6 text-xl font-bold">
                            {numbers.map((num, idx) => (
                                <div key={idx} className="flex items-center gap-2">
                                    <MathRenderer content={`$|${num}| = ${Math.abs(num)}$`} />
                                    {Math.abs(num) === correctDistance && (
                                        <CheckCircle2 size={20} className="text-green-400" />
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {/* Explanation */}
            {explanation && isAnswered && (
                <div style={{
                    background: 'rgba(0, 212, 255, 0.1)',
                    border: '1px solid rgba(0, 212, 255, 0.2)',
                    borderRadius: '12px',
                    padding: '20px',
                    marginTop: '24px'
                }} className="animate-fadeIn">
                    <div className="flex items-start gap-3">
                        <CheckCircle2 size={24} className="text-blue-400 flex-shrink-0 mt-1" />
                        <div>
                            <div className="font-semibold text-blue-400 mb-2">Wyjaśnienie</div>
                            <div className="text-gray-300 leading-relaxed">
                                <MathRenderer content={explanation} />
                            </div>
                        </div>
                    </div>
                </div>
            )}

            <style jsx>{`
                @keyframes fadeIn {
                    from {
                        opacity: 0;
                        transform: translateY(10px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                .animate-fadeIn {
                    animation: fadeIn 0.5s ease-out;
                }
            `}</style>
        </div>
    )
}
