'use client'

import { useState, useEffect } from 'react'
import { CheckCircle2, RotateCcw, Lightbulb, Target } from 'lucide-react'
import confetti from 'canvas-confetti'
import MathRenderer from './MathRenderer'

interface ExpressionBuilderCardProps {
    title?: string
    instruction?: string
    targetValue: number
    availableNumbers: number[]
    availableOperations: string[]
    sampleSolutions?: string[]
    explanation?: string
}

export default function ExpressionBuilderCard({
    title = 'Zbuduj wyrażenie',
    instruction = 'Użyj dostępnych liczb i operacji, aby uzyskać docelowy wynik',
    targetValue,
    availableNumbers,
    availableOperations,
    sampleSolutions = [],
    explanation
}: ExpressionBuilderCardProps) {
    const [expression, setExpression] = useState<string[]>([])
    const [usedNumbers, setUsedNumbers] = useState<Set<number>>(new Set())
    const [result, setResult] = useState<number | null>(null)
    const [isCorrect, setIsCorrect] = useState(false)
    const [showSamples, setShowSamples] = useState(false)
    const [showExplanation, setShowExplanation] = useState(false)

    useEffect(() => {
        evaluateExpression()
    }, [expression])

    const evaluateExpression = () => {
        if (expression.length === 0) {
            setResult(null)
            setIsCorrect(false)
            return
        }

        try {
            const exprString = expression.join(' ')
            // Simple eval (in production use proper parser)
            const calculated = eval(exprString)
            setResult(calculated)
            
            if (Math.abs(calculated - targetValue) < 0.001) {
                setIsCorrect(true)
                triggerConfetti()
            } else {
                setIsCorrect(false)
            }
        } catch (e) {
            setResult(null)
            setIsCorrect(false)
        }
    }

    const handleNumberClick = (num: number, index: number) => {
        if (usedNumbers.has(index)) return
        
        setExpression([...expression, num.toString()])
        setUsedNumbers(new Set([...usedNumbers, index]))
    }

    const handleOperationClick = (op: string) => {
        // Don't allow operation as first item or two operations in a row
        if (expression.length === 0) return
        const lastItem = expression[expression.length - 1]
        if (['+', '-', '*', '/'].includes(lastItem)) return
        
        setExpression([...expression, op])
    }

    const handleClear = () => {
        setExpression([])
        setUsedNumbers(new Set())
        setResult(null)
        setIsCorrect(false)
        setShowSamples(false)
        setShowExplanation(false)
    }

    const handleCheck = () => {
        if (!isCorrect) {
            setShowSamples(true)
        } else {
            setShowExplanation(true)
        }
    }

    const handleBackspace = () => {
        if (expression.length === 0) return
        
        const lastItem = expression[expression.length - 1]
        const newExpression = expression.slice(0, -1)
        
        // If it was a number, mark it as unused
        if (!['+', '-', '*', '/'].includes(lastItem)) {
            const numIndex = availableNumbers.findIndex((num, idx) => 
                num.toString() === lastItem && usedNumbers.has(idx)
            )
            if (numIndex !== -1) {
                const newUsed = new Set(usedNumbers)
                newUsed.delete(numIndex)
                setUsedNumbers(newUsed)
            }
        }
        
        setExpression(newExpression)
    }

    const triggerConfetti = () => {
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 }
        })
    }

    const formatExpression = (expr: string[]) => {
        return expr.map(item => {
            if (item === '*') return '×'
            if (item === '/') return '÷'
            return item
        }).join(' ')
    }

    return (
        <div style={{
            maxWidth: '900px',
            width: '100%',
            position: 'relative',
            background: 'rgba(20, 20, 35, 0.6)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            border: '1px solid rgba(251, 146, 60, 0.2)',
            borderRadius: '20px',
            padding: '40px',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
            borderLeft: '4px solid #fb923c'
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
                color: '#fb923c',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(251, 146, 60, 0.1)',
                border: '1px solid rgba(251, 146, 60, 0.2)',
                borderRadius: '20px'
            }}>
                BUDOWNICZY WYRAŻEŃ
            </div>

            {/* Title */}
            <h2 style={{
                fontSize: '28px',
                fontWeight: 700,
                marginBottom: '12px',
                marginTop: '20px',
                color: '#fb923c',
                textAlign: 'center'
            }}>
                {title}
            </h2>
            
            {instruction && (
                <p className="text-gray-300 text-center mb-8">{instruction}</p>
            )}

            {/* Target Display */}
            <div className="bg-orange-500/10 rounded-xl p-6 mb-8 border border-orange-500/20">
                <div className="flex items-center justify-center gap-3">
                    <Target className="w-8 h-8 text-orange-400" />
                    <div className="text-center">
                        <div className="text-sm text-orange-300 font-semibold mb-1">Docelowy wynik</div>
                        <div className="text-4xl font-bold text-orange-400">{targetValue}</div>
                    </div>
                </div>
            </div>

            {/* Expression Display */}
            <div className={`min-h-24 bg-black/30 rounded-xl p-6 mb-6 border-2 transition-all ${
                isCorrect ? 'border-green-500 bg-green-500/10' : 'border-white/10'
            }`}>
                <div className="text-center">
                    {expression.length === 0 ? (
                        <div className="text-gray-500 text-lg py-4">
                            Kliknij liczby i operacje poniżej...
                        </div>
                    ) : (
                        <div className="text-3xl font-semibold text-white py-2 font-mono">
                            {formatExpression(expression)}
                        </div>
                    )}
                    
                    {result !== null && (
                        <div className={`text-2xl font-bold mt-3 ${
                            isCorrect ? 'text-green-400' : 'text-gray-400'
                        }`}>
                            = {result}
                            {isCorrect && <CheckCircle2 className="inline-block ml-2 w-6 h-6" />}
                        </div>
                    )}
                </div>
            </div>

            {/* Available Numbers */}
            <div className="mb-6">
                <div className="text-sm font-semibold text-gray-400 mb-3">📊 Dostępne liczby:</div>
                <div className="grid grid-cols-4 gap-3">
                    {availableNumbers.map((num, index) => (
                        <button
                            key={index}
                            onClick={() => handleNumberClick(num, index)}
                            disabled={usedNumbers.has(index)}
                            className={`p-4 rounded-xl text-2xl font-bold transition-all ${
                                usedNumbers.has(index)
                                    ? 'bg-black/20 text-gray-600 cursor-not-allowed opacity-40'
                                    : 'bg-black/40 border-2 border-white/10 hover:border-orange-500 hover:bg-orange-500/10 hover:scale-105 active:scale-95 text-white'
                            }`}
                        >
                            {num}
                        </button>
                    ))}
                </div>
            </div>

            {/* Available Operations */}
            <div className="mb-8">
                <div className="text-sm font-semibold text-gray-400 mb-3">🔢 Dostępne operacje:</div>
                <div className="grid grid-cols-4 gap-3">
                    {availableOperations.map((op) => {
                        const displayOp = op === '*' ? '×' : op === '/' ? '÷' : op
                        return (
                            <button
                                key={op}
                                onClick={() => handleOperationClick(op)}
                                className="p-4 rounded-xl text-2xl font-bold bg-black/40 border-2 border-orange-500/20 hover:border-orange-500 hover:bg-orange-500/10 hover:scale-105 active:scale-95 text-orange-400 transition-all"
                            >
                                {displayOp}
                            </button>
                        )
                    })}
                </div>
            </div>

            {/* Action Buttons */}
            <div className="grid grid-cols-3 gap-3 mb-6">
                <button
                    onClick={handleBackspace}
                    disabled={expression.length === 0}
                    className="px-6 py-3 bg-black/40 border border-white/10 hover:bg-black/60 disabled:opacity-30 disabled:cursor-not-allowed rounded-xl font-semibold text-gray-300 transition-all"
                >
                    ⌫ Cofnij
                </button>
                <button
                    onClick={handleClear}
                    className="px-6 py-3 bg-black/40 border border-white/10 hover:bg-black/60 rounded-xl font-semibold text-gray-300 transition-all flex items-center justify-center gap-2"
                >
                    <RotateCcw className="w-5 h-5" />
                    Wyczyść
                </button>
                <button
                    onClick={handleCheck}
                    disabled={expression.length === 0}
                    className="px-6 py-3 bg-orange-500 hover:bg-orange-600 disabled:opacity-30 disabled:cursor-not-allowed text-black rounded-xl font-semibold transition-all flex items-center justify-center gap-2"
                >
                    <CheckCircle2 className="w-5 h-5" />
                    Sprawdź
                </button>
            </div>

            {/* Explanation */}
            {isCorrect && showExplanation && explanation && (
                <div className="bg-green-500/10 border-l-4 border-green-500 rounded-xl p-6 mb-6 animate-fade-in">
                    <div className="flex items-start gap-3">
                        <CheckCircle2 className="w-6 h-6 text-green-400 flex-shrink-0 mt-1" />
                        <div>
                            <h3 className="font-bold text-green-300 mb-2">✅ Świetnie!</h3>
                            <div className="text-gray-300 leading-relaxed">
                                <MathRenderer content={explanation} />
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Sample Solutions */}
            {showSamples && sampleSolutions.length > 0 && (
                <div className="bg-blue-500/10 border-l-4 border-blue-500 rounded-xl p-6 animate-fade-in">
                    <div className="flex items-start gap-3">
                        <Lightbulb className="w-6 h-6 text-blue-400 flex-shrink-0 mt-1" />
                        <div className="flex-1">
                            <h3 className="font-bold text-blue-300 mb-3">💡 Przykładowe rozwiązania:</h3>
                            <div className="space-y-2">
                                {sampleSolutions.map((solution, index) => (
                                    <div key={index} className="bg-black/30 rounded-lg p-3 border-l-3 border-blue-500/30 text-gray-300">
                                        <MathRenderer content={solution} />
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
