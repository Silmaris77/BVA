'use client'

import { useState } from 'react'
import { CheckCircle2, XCircle, HelpCircle } from 'lucide-react'
import confetti from 'canvas-confetti'
import MathRenderer from './MathRenderer'

type SignType = 'positive' | 'negative' | 'zero'

interface SignPredictorCardProps {
    title?: string
    question: string
    expression: string
    correctSign: SignType
    explanation?: string
}

export default function SignPredictorCard({
    title = 'Przewidź znak wyniku',
    question,
    expression,
    correctSign,
    explanation
}: SignPredictorCardProps) {
    const [selectedSign, setSelectedSign] = useState<SignType | null>(null)
    const [isAnswered, setIsAnswered] = useState(false)

    const handleSignSelect = (sign: SignType) => {
        if (isAnswered) return

        setSelectedSign(sign)
        setIsAnswered(true)

        if (sign === correctSign) {
            triggerConfetti()
        }
    }

    const triggerConfetti = () => {
        confetti({
            particleCount: 50,
            spread: 60,
            origin: { y: 0.7 },
            colors: ['#00ff88', '#ffd700']
        })
    }

    const getSignIcon = (sign: SignType) => {
        switch (sign) {
            case 'positive': return '➕'
            case 'negative': return '➖'
            case 'zero': return '⚖️'
        }
    }

    const getSignLabel = (sign: SignType) => {
        switch (sign) {
            case 'positive': return 'Dodatni'
            case 'negative': return 'Ujemny'
            case 'zero': return 'Zero'
        }
    }

    const getOptionClass = (sign: SignType) => {
        const baseClass = 'relative group cursor-pointer rounded-xl p-6 transition-all duration-300 border-2'

        if (!isAnswered) {
            return `${baseClass} bg-black/20 border-white/10 hover:border-purple-500 hover:bg-purple-500/10 hover:scale-105 text-gray-200`
        }

        if (sign === correctSign) {
            return `${baseClass} border-green-500 bg-green-500/20 text-green-400 scale-105`
        }

        if (sign === selectedSign && sign !== correctSign) {
            return `${baseClass} border-red-500 bg-red-500/10 text-red-400 opacity-60`
        }

        return `${baseClass} bg-black/10 border-white/5 text-gray-500 opacity-50`
    }

    return (
        <div style={{
            maxWidth: '900px',
            width: '100%',
            position: 'relative',
            background: 'rgba(20, 20, 35, 0.6)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            border: '1px solid rgba(168, 85, 247, 0.2)',
            borderRadius: '20px',
            padding: '40px',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
            borderLeft: '4px solid #a855f7'
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
                color: '#a855f7',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(168, 85, 247, 0.1)',
                border: '1px solid rgba(168, 85, 247, 0.2)',
                borderRadius: '20px'
            }}>
                PRZEWIDYWANIE ZNAKU
            </div>

            {/* Title */}
            <h2 style={{
                fontSize: '28px',
                fontWeight: 700,
                marginBottom: '12px',
                marginTop: '20px',
                color: '#a855f7',
                textAlign: 'center'
            }}>
                {title}
            </h2>
            
            {question && (
                <p className="text-gray-300 text-center mb-8">{question}</p>
            )}

            {/* Expression Display */}
            <div className="bg-black/30 rounded-xl p-8 mb-8 border border-white/10">
                <div className="text-center text-3xl font-bold text-white">
                    <MathRenderer content={expression} />
                </div>
            </div>

            {/* Sign Options */}
            <div className="grid grid-cols-3 gap-4 mb-8">
                {(['positive', 'negative', 'zero'] as SignType[]).map((sign) => (
                    <button
                        key={sign}
                        onClick={() => handleSignSelect(sign)}
                        disabled={isAnswered}
                        className={getOptionClass(sign)}
                    >
                        <div className="text-center">
                            <div className="text-5xl mb-3">
                                {getSignIcon(sign)}
                            </div>
                            <div className="text-lg font-semibold">
                                {getSignLabel(sign)}
                            </div>
                        </div>

                        {/* Checkmark for correct answer */}
                        {isAnswered && sign === correctSign && (
                            <div className="absolute top-3 right-3">
                                <CheckCircle2 className="w-8 h-8 text-green-400" />
                            </div>
                        )}

                        {/* X mark for wrong answer */}
                        {isAnswered && sign === selectedSign && sign !== correctSign && (
                            <div className="absolute top-3 right-3">
                                <XCircle className="w-8 h-8 text-red-400" />
                            </div>
                        )}
                    </button>
                ))}
            </div>

            {/* Explanation */}
            {isAnswered && explanation && (
                <div className="bg-purple-500/10 border-l-4 border-purple-500 rounded-xl p-6 animate-fade-in">
                    <div className="flex items-start gap-3">
                        <HelpCircle className="w-6 h-6 text-purple-400 flex-shrink-0 mt-1" />
                        <div>
                            <h3 className="font-bold text-purple-300 mb-2">
                                💡 Wyjaśnienie:
                            </h3>
                            <div className="text-gray-300 leading-relaxed">
                                <MathRenderer content={explanation} />
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
