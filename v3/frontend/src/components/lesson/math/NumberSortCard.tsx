'use client'

import { useState, useEffect } from 'react'
import { Check, ArrowRight, RotateCcw } from 'lucide-react'

// Helper for class names
function classNames(...classes: (string | undefined | null | false)[]) {
    return classes.filter(Boolean).join(' ')
}

interface NumberSortCardProps {
    title?: string
    question: string
    numbers: number[] // Expected sorted order is calculated from this if needed, or expected logic handled internally
    order?: 'asc' | 'desc'
    onComplete?: (correct: boolean) => void
}

export default function NumberSortCard({
    title,
    question,
    numbers,
    order = 'asc',
    onComplete
}: NumberSortCardProps) {
    const [shuffledNumbers, setShuffledNumbers] = useState<number[]>([])
    const [sortedSoFar, setSortedSoFar] = useState<number[]>([])
    const [isCompleted, setIsCompleted] = useState(false)
    const [wrongIndex, setWrongIndex] = useState<number | null>(null)

    // Calculate correct sequence based on props
    const correctSequence = [...numbers].sort((a, b) => order === 'asc' ? a - b : b - a)

    useEffect(() => {
        // Shuffle on mount
        const shuffled = [...numbers].sort(() => Math.random() - 0.5)
        // Ensure it's not already sorted by accident (rare but possible)
        // For small arrays it might happen often, but it's fine for simple tasks.
        setShuffledNumbers(shuffled)
        setSortedSoFar([])
        setIsCompleted(false)
        setWrongIndex(null)
    }, [numbers, order])

    const handleNumberClick = (num: number, index: number) => {
        if (isCompleted) return

        const nextExpectedIndex = sortedSoFar.length
        const nextExpectedNumber = correctSequence[nextExpectedIndex]

        if (num === nextExpectedNumber) {
            // Correct!
            setSortedSoFar(prev => [...prev, num])
            // Remove from clickable pool (or just mark as used visually logic needs to track which specific instance if duplicates exist)
            // To handle duplicates properly, we should track by index in original shuffled array or similar.
            // Let's use index in shuffledNumbers to identify the exact button clicked.
            setShuffledNumbers(prev => prev.map((n, i) => i === index ? -999999 : n)) // Mark as taken with a sentinel or handle differently

            // Check completion
            if (sortedSoFar.length + 1 === numbers.length) {
                setIsCompleted(true)
                if (onComplete) onComplete(true)
            }
        } else {
            // Wrong!
            setWrongIndex(index)
            setTimeout(() => setWrongIndex(null), 500)
        }
    }

    const reset = () => {
        const shuffled = [...numbers].sort(() => Math.random() - 0.5)
        setShuffledNumbers(shuffled)
        setSortedSoFar([])
        setIsCompleted(false)
    }

    return (
        <div className="w-full max-w-2xl mx-auto glass-card p-8 rounded-2xl border border-white/10 relative overflow-hidden flex flex-col min-h-[400px]">
            {/* Header Badge */}
            <div className="absolute top-4 left-4">
                <span className="bg-blue-500/10 text-blue-300 px-2 py-0.5 rounded text-[10px] font-bold uppercase border border-blue-500/20 tracking-wider">
                    Sortowanie
                </span>
            </div>

            <div className="mt-6 mb-8 text-center">
                {title && <h3 className="text-gray-400 uppercase text-xs font-bold tracking-widest mb-2">{title}</h3>}
                <h2 className="text-xl md:text-2xl font-medium text-white">
                    {question}
                </h2>
                <p className="text-sm text-gray-500 mt-2">
                    {order === 'asc' ? 'Od najmniejszej do największej (Rosnąco)' : 'Od największej do najmniejszej (Malejąco)'}
                </p>
            </div>

            {/* Content Area */}
            <div className="flex-1 flex flex-col gap-8">

                {/* Sorted Drop Zone */}
                <div className="flex flex-wrap gap-3 min-h-[80px] p-4 rounded-xl bg-black/20 border border-white/5 items-center justify-start">
                    {sortedSoFar.length === 0 && !isCompleted && (
                        <span className="text-gray-600 text-sm italic w-full text-center">
                            Wybieraj liczby w odpowiedniej kolejności...
                        </span>
                    )}
                    {sortedSoFar.map((num, i) => (
                        <div
                            key={`sorted-${i}`}
                            className="w-12 h-12 flex items-center justify-center rounded-lg bg-green-500/20 border border-green-500/30 text-green-400 font-bold font-mono text-lg animate-in zoom-in spin-in-12 duration-300"
                        >
                            {num}
                        </div>
                    ))}
                    {sortedSoFar.length > 0 && !isCompleted && (
                        <div className="w-8 h-8 flex items-center justify-center text-gray-600">
                            <ArrowRight size={16} />
                        </div>
                    )}
                </div>

                {/* Available Numbers */}
                <div className="flex flex-wrap gap-4 justify-center py-4">
                    {shuffledNumbers.map((num, i) => {
                        if (num === -999999) return null // Hidden/Taken

                        const isWrong = wrongIndex === i
                        return (
                            <button
                                key={`available-${i}`}
                                onClick={() => handleNumberClick(num, i)}
                                className={classNames(
                                    "w-16 h-16 flex items-center justify-center rounded-xl font-bold font-mono text-xl transition-all duration-200 border-b-4 active:scale-95 active:border-b-0",
                                    isWrong
                                        ? "bg-red-500 text-white border-red-700 animate-shake"
                                        : "bg-white text-black border-gray-300 hover:bg-gray-100 hover:scale-105"
                                )}
                            >
                                {num}
                            </button>
                        )
                    })}
                </div>

            </div>

            {/* Success Message */}
            {isCompleted && (
                <div className="absolute inset-0 bg-black/80 backdrop-blur-sm flex flex-col items-center justify-center z-10 animate-in fade-in">
                    <div className="bg-[#0f0c29] border border-[var(--accent-green)] p-8 rounded-2xl flex flex-col items-center gap-4 shadow-[0_0_50px_rgba(0,255,157,0.2)]">
                        <div className="w-16 h-16 rounded-full bg-green-500/20 flex items-center justify-center text-green-400 mb-2">
                            <Check size={32} strokeWidth={3} />
                        </div>
                        <h3 className="text-2xl font-bold text-white">Zadanie wykonane!</h3>
                        <p className="text-gray-400 text-center max-w-xs">
                            Liczby zostały posortowane poprawnie.
                        </p>
                        <button
                            onClick={reset}
                            className="mt-4 flex items-center gap-2 text-sm text-gray-500 hover:text-white transition uppercase tracking-wider font-bold"
                        >
                            <RotateCcw size={14} /> Powtórz
                        </button>
                    </div>
                    <style>{`
                        @keyframes shake {
                            0%, 100% { transform: translateX(0); }
                            25% { transform: translateX(-5px); }
                            75% { transform: translateX(5px); }
                        }
                        .animate-shake {
                            animation: shake 0.3s ease-in-out;
                        }
                    `}</style>
                </div>
            )}
        </div>
    )
}
