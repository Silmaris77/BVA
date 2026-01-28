'use client'

import { useState, useEffect } from 'react'
import { Check, HelpCircle, RotateCcw } from 'lucide-react'

// Helper for class names
function classNames(...classes: (string | undefined | null | false)[]) {
    return classes.filter(Boolean).join(' ')
}

interface DigitSelectorCardProps {
    title?: string
    question: string
    number: string | number
    correctIndex: number // 0-based index of the digit in the string representation
    explanation?: string
    onComplete?: (correct: boolean) => void
}

export default function DigitSelectorCard({
    title,
    question,
    number,
    correctIndex,
    explanation,
    onComplete
}: DigitSelectorCardProps) {
    const [selectedindex, setSelectedIndex] = useState<number | null>(null)
    const [isCorrect, setIsCorrect] = useState<boolean | null>(null)
    const [showExplanation, setShowExplanation] = useState(false)

    const numberStr = String(number)
    const digits = numberStr.split('')

    const handleDigitClick = (index: number) => {
        if (isCorrect === true) return // Prevent clicking after success

        // Skip non-digit characters if we want strictly digits, but sometimes we might want to select the comma/dot?
        // usually we select digits. For now let's allow clicking anything that is a character in the string.

        setSelectedIndex(index)

        const correct = index === correctIndex
        setIsCorrect(correct)

        if (correct) {
            setShowExplanation(true)
            if (onComplete) onComplete(true)
        } else {
            // Maybe auto-hide error after delay? 
            // For now keep it red until they try again.
        }
    }

    const reset = () => {
        setSelectedIndex(null)
        setIsCorrect(null)
        setShowExplanation(false)
    }

    return (
        <div style={{
            maxWidth: '900px',
            width: '100%',
            position: 'relative',
            background: 'rgba(20, 20, 35, 0.6)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            border: '1px solid rgba(59, 130, 246, 0.2)', // Blue
            borderRadius: '20px',
            padding: '40px',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
            borderLeft: '4px solid #3b82f6',
            display: 'flex',
            flexDirection: 'column',
            minHeight: '300px'
        }}>
            {/* Header Badge */}
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
                color: '#3b82f6',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(59, 130, 246, 0.1)',
                border: '1px solid rgba(59, 130, 246, 0.2)',
                borderRadius: '20px'
            }}>
                WARTOŚĆ POZYCYJNA
            </div>

            <div className="mt-6 mb-8 text-center">
                {title && <h3 className="text-gray-400 uppercase text-xs font-bold tracking-widest mb-2">{title}</h3>}
                <h2 className="text-xl md:text-2xl font-medium text-white mb-6">
                    {question}
                </h2>

                {/* Number Display */}
                <div className="flex justify-center items-center gap-2 flex-wrap">
                    {digits.map((char, index) => {
                        const isSelected = selectedindex === index
                        const isRight = isSelected && isCorrect
                        const isWrong = isSelected && isCorrect === false

                        return (
                            <button
                                key={`digit-${index}`}
                                onClick={() => handleDigitClick(index)}
                                className={classNames(
                                    "text-4xl md:text-6xl font-mono font-bold px-3 py-2 rounded-xl transition-all duration-200 border-2 select-none",
                                    isSelected
                                        ? (isRight ? "bg-green-500/20 text-green-400 border-green-500 scale-110" : "bg-red-500/20 text-red-400 border-red-500")
                                        : "bg-black/20 text-white border-transparent hover:bg-white/10 hover:border-white/20 hover:scale-105"
                                )}
                            >
                                {char}
                            </button>
                        )
                    })}
                </div>
            </div>

            {/* Explanation Area */}
            {(showExplanation && explanation) && (
                <div className="mt-4 p-4 rounded-xl bg-blue-500/10 border border-blue-500/20 animate-in fade-in slide-in-from-bottom-2">
                    <div className="flex items-start gap-3">
                        <HelpCircle className="w-5 h-5 text-blue-400 mt-1 flex-shrink-0" />
                        <p className="text-blue-100/90 leading-relaxed text-sm">
                            {explanation}
                        </p>
                    </div>
                </div>
            )}

            {/* Success Overlay if needed, or just visual feedback on digits */}
            {isCorrect && (
                <div className="flex flex-col items-center mt-6 animate-in fade-in">
                    <div className="flex items-center gap-2 text-green-400 font-bold mb-2">
                        <Check size={20} />
                        <span>Dokładnie tak!</span>
                    </div>
                    <button
                        onClick={reset}
                        className="text-xs text-gray-500 hover:text-white transition uppercase tracking-wider font-bold flex items-center gap-1"
                    >
                        <RotateCcw size={12} /> Powtórz
                    </button>
                </div>
            )}
        </div>
    )
}
