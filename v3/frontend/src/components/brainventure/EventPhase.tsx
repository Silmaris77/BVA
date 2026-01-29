import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useBrainVenture } from './BrainVentureContext'
import EVENTS_DATA from '@/data/brainventure/events.json'
import { EventCard, EventOption, EventEffect, EventRisk } from '@/types/brainventure'
import { Disc, PlayCircle, Dices, ChevronRight, Gem, Zap, Clock, DollarSign, TrendingUp } from 'lucide-react'

// Simple dice roll helper
const rollDice = (count: number = 1): number[] => {
    return Array.from({ length: count }, () => Math.floor(Math.random() * 6) + 1)
}

// Helper to calculate probability for display
const calculateProbability = (risk: EventRisk, modifierValue: number = 0): number => {
    // Simplified probability calc for 1d6 and 2d6
    const totalOutcomes = Math.pow(6, risk.diceCount)
    let successCount = 0

    // Ultra-simplistic simulation for complex rules (robust enough for UI display)
    if (risk.diceCount === 1) {
        for (let i = 1; i <= 6; i++) {
            const val = i + modifierValue
            if (risk.rule === 'SUM_GE' && val >= risk.targetValue) successCount++
            if (risk.rule === 'SUM_LE' && val <= risk.targetValue) successCount++
            if (risk.rule === 'CONTAINS' && i === risk.targetValue) successCount++
        }
    } else if (risk.diceCount === 2) {
        for (let i = 1; i <= 6; i++) {
            for (let j = 1; j <= 6; j++) {
                const sum = i + j + modifierValue
                if (risk.rule === 'SUM_GE' && sum >= risk.targetValue) successCount++
                if (risk.rule === 'SUM_LE' && sum <= risk.targetValue) successCount++
                if (risk.rule === 'CONTAINS' && (i === risk.targetValue || j === risk.targetValue)) successCount++
            }
        }
    }

    return Math.round((successCount / totalOutcomes) * 100)
}

export default function EventPhase() {
    const { state, dispatch } = useBrainVenture()
    const [card, setCard] = useState<EventCard | null>(null)
    const [isRevealed, setIsRevealed] = useState(false)
    const [processed, setProcessed] = useState(false)

    // Risk/Dice State
    const [activeRisk, setActiveRisk] = useState<EventRisk | null>(null)
    const [diceResult, setDiceResult] = useState<number[] | null>(null)
    const [riskMessage, setRiskMessage] = useState<string>('')
    const [isRolling, setIsRolling] = useState(false)

    // Draw card on mount
    useEffect(() => {
        if (state.currentEvent) {
            setCard(state.currentEvent)
            setIsRevealed(true) // If loaded from state, it's already "active", assume revealed or reveal it
            return
        }

        // Draw a random event if none is set
        const randomEvent = EVENTS_DATA[Math.floor(Math.random() * EVENTS_DATA.length)]
        setCard(randomEvent as unknown as EventCard)
        // Delay dispatch until reveal to prevent sidebar spoilers
    }, [])

    const handleReveal = () => {
        if (!card) return

        setIsRevealed(true)
        // Reveal to global state now
        dispatch({ type: 'LOG_EVENT', payload: card.id })
        dispatch({ type: 'SET_CURRENT_EVENT', payload: card })

        // Auto-apply immediate effects if no options
        if (!card.options && card.immediateEffects) {
            applyEffects(card.immediateEffects)
            setProcessed(true)
            dispatch({ type: 'SET_PHASE_READY', payload: true }) // [NEW]
        }
        // If no interaction needed (info only)
        if (!card.options && !card.immediateEffects) {
            dispatch({ type: 'SET_PHASE_READY', payload: true })
        }
    }

    const applyEffects = (effects: EventEffect[]) => {
        if (!effects) return

        effects.forEach(effect => {
            if (effect.type === 'KW') dispatch({ type: 'UPDATE_KW', payload: effect.amount })
            if (effect.type === 'CASH') dispatch({ type: 'UPDATE_CASH', payload: effect.amount })

            if (effect.type === 'EFFICIENCY') {
                if (effect.target === 'TEAM' || effect.target === 'ALL') {
                    state.team.forEach(c => dispatch({ type: 'UPDATE_EFFICIENCY', payload: { charId: c.id, amount: effect.amount } }))
                } else if (effect.target === 'MANAGER') {
                    dispatch({ type: 'UPDATE_EFFICIENCY', payload: { charId: 'manager', amount: effect.amount } })
                } else if (effect.target === 'EMPLOYEES') {
                    state.team.filter(c => c.role === 'EMPLOYEE').forEach(emp => {
                        dispatch({ type: 'UPDATE_EFFICIENCY', payload: { charId: emp.id, amount: effect.amount } })
                    })
                } else if (effect.target === 'EMPLOYEE') {
                    const emp = state.team.find(c => c.role === 'EMPLOYEE')
                    if (emp) dispatch({ type: 'UPDATE_EFFICIENCY', payload: { charId: emp.id, amount: effect.amount } })
                }
            }

            if (effect.type === 'AVAILABILITY') {
                if (effect.target === 'MANAGER') {
                    dispatch({ type: 'UPDATE_AVAILABILITY', payload: { charId: 'manager', amount: effect.amount } })
                } else if (effect.target === 'EMPLOYEE') {
                    // Random employee or first found
                    const emp = state.team.find(c => c.role === 'EMPLOYEE')
                    if (emp) dispatch({ type: 'UPDATE_AVAILABILITY', payload: { charId: emp.id, amount: effect.amount } })
                } else if (effect.target === 'EMPLOYEES') {
                    state.team.filter(c => c.role === 'EMPLOYEE').forEach(emp => {
                        dispatch({ type: 'UPDATE_AVAILABILITY', payload: { charId: emp.id, amount: effect.amount } })
                    })
                }
            }
        })
    }

    const handleOptionClick = (option: EventOption) => {
        if (option.immediateEffects) {
            applyEffects(option.immediateEffects)
        }

        if (option.risk) {
            setActiveRisk(option.risk)
            setIsRolling(true)

            // Auto-roll after delay for effect
            setTimeout(() => {
                executeRiskRoll(option.risk!)
            }, 1000)
        } else {
            setProcessed(true)
            dispatch({ type: 'SET_PHASE_READY', payload: true })
        }
    }

    const executeRiskRoll = (risk: EventRisk) => {
        const results = rollDice(risk.diceCount)
        setDiceResult(results)
        setIsRolling(false)

        let modifierVal = 0
        if (risk.modifier === 'MANAGER_EFFICIENCY') {
            const manager = state.team.find(c => c.role === 'MANAGER')
            if (manager) modifierVal = manager.efficiency
        }

        const sum = results.reduce((a, b) => a + b, 0) + modifierVal

        let success = false
        if (risk.rule === 'SUM_GE') success = sum >= risk.targetValue
        if (risk.rule === 'CONTAINS') success = results.includes(risk.targetValue)
        // ...

        if (success) {
            setRiskMessage(risk.successMessage || 'POZYTYWNY EFEKT')
            if (risk.successEffect) applyEffects(risk.successEffect)
        } else {
            setRiskMessage(risk.failureMessage || 'BRAK ZMIAN')
            if (risk.failureEffect) applyEffects(risk.failureEffect)
        }

        setProcessed(true)
        dispatch({ type: 'SET_PHASE_READY', payload: true }) // [NEW]
    }

    if (!card) return <div>Losowanie zdarzenia...</div>

    return (
        <div className="h-full flex flex-col items-center justify-center max-w-4xl mx-auto w-full">
            <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="mb-8 text-center"
            >
                <h2 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-300 mb-2">
                    Faza 1: Zdarzenia
                </h2>
                <p className="text-blue-200/60">Co przyniesie nowy dzień w firmie?</p>
            </motion.div>

            <div className={`relative w-full max-w-2xl aspect-[3/2] perspective-1000 ${isRevealed ? '' : 'cursor-pointer'}`}>
                <motion.div
                    className="w-full h-full relative preserve-3d transition-transform duration-700"
                    style={{ transformStyle: 'preserve-3d', transform: isRevealed ? 'rotateY(180deg)' : 'rotateY(0deg)' }}
                    onClick={!isRevealed ? handleReveal : undefined}
                >
                    {/* Card Back */}
                    <div
                        className="absolute inset-0 backface-hidden bg-gradient-to-br from-blue-900 to-slate-900 rounded-2xl border-2 border-blue-500/30 flex flex-col items-center justify-center shadow-[0_0_50px_rgba(59,130,246,0.2)] hover:shadow-blue-500/40 transition-shadow"
                        style={{ backfaceVisibility: 'hidden', WebkitBackfaceVisibility: 'hidden' }}
                    >
                        <Disc size={64} className="text-blue-400/50 animate-spin-slow" />
                        <span className="mt-4 text-xl font-bold text-blue-300 uppercase tracking-widest">Karta Zdarzenia</span>
                        <span className="text-sm text-blue-400/60 mt-2">Kliknij, aby odkryć</span>
                    </div>

                    {/* Card Front */}
                    <div
                        className="absolute inset-0 backface-hidden bg-slate-800 rounded-2xl border border-gray-600 p-8 flex flex-col items-center text-center shadow-2xl overflow-y-auto custom-scrollbar"
                        style={{ transform: 'rotateY(180deg)', backfaceVisibility: 'hidden', WebkitBackfaceVisibility: 'hidden' }}
                    >
                        <div className={`w-full h-2 rounded-full mb-6 flex-shrink-0 ${card.type === 'POSITIVE' ? 'bg-green-500' :
                            card.type === 'NEGATIVE' ? 'bg-red-500' : 'bg-yellow-500'
                            }`} />

                        <h3 className="text-2xl font-bold text-white mb-4 uppercase tracking-wide">{card.title}</h3>

                        <div className="mb-6">
                            <p className="text-lg text-gray-300 leading-relaxed">
                                {card.description}
                            </p>
                        </div>

                        {/* Visual Effect Display */}
                        {card.immediateEffects && card.immediateEffects.length > 0 && (
                            <div className="mb-6 w-full bg-gray-900/40 rounded-xl p-4 border border-gray-700">
                                <h4 className="text-xs uppercase text-gray-500 font-bold mb-3 tracking-wider text-left">Efekt</h4>
                                <div className="flex flex-col gap-2">
                                    {card.immediateEffects.map((effect, idx) => (
                                        <div key={idx} className="flex items-center gap-3 text-left">
                                            {effect.type === 'KW' && <div className="p-2 bg-blue-500/20 rounded-lg text-blue-400"><Gem size={18} /></div>}
                                            {effect.type === 'EFFICIENCY' && <div className="p-2 bg-green-500/20 rounded-lg text-green-400"><TrendingUp size={18} /></div>}
                                            {effect.type === 'AVAILABILITY' && <div className="p-2 bg-orange-500/20 rounded-lg text-orange-400"><Clock size={18} /></div>}
                                            {effect.type === 'CASH' && <div className="p-2 bg-yellow-500/20 rounded-lg text-yellow-400"><DollarSign size={18} /></div>}

                                            <span className="font-bold text-gray-200">{effect.description}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Options / Interactions */}
                        {!processed && !activeRisk && card.options && (
                            <div className="flex flex-col gap-3 w-full max-w-sm mt-auto">
                                {card.options.map(opt => (
                                    <button
                                        key={opt.id}
                                        onClick={(e) => { e.stopPropagation(); handleOptionClick(opt) }}
                                        className="py-3 px-6 bg-blue-600 hover:bg-blue-500 rounded-xl font-bold text-white transition-colors flex items-center justify-center gap-2"
                                    >
                                        <PlayCircle size={18} /> {opt.label}
                                    </button>
                                ))}
                            </div>
                        )}

                        {/* Pending Risk Roll (Animation) */}
                        {isRolling && (
                            <div className="flex flex-col items-center gap-4 animate-in fade-in zoom-in duration-300 py-8">
                                <div className="relative">
                                    <div className="absolute inset-0 bg-blue-500 blur-xl opacity-20 animate-pulse"></div>
                                    <Dices size={64} className="text-blue-400 animate-bounce" />
                                </div>
                                <p className="text-blue-200 font-bold uppercase tracking-wider animate-pulse">
                                    Weryfikacja...
                                </p>
                            </div>
                        )}

                        {/* Result Display */}
                        {diceResult && activeRisk && (
                            <div className="mt-4 w-full bg-gray-900/40 rounded-xl p-4 border border-gray-700 animate-in fade-in slide-in-from-bottom-4">
                                <h4 className="text-xs uppercase text-gray-500 font-bold mb-3 tracking-wider text-left">
                                    {activeRisk.successEffect && (riskMessage === activeRisk.successMessage || riskMessage === 'POZYTYWNY EFEKT') ? 'SUKCES' : 'REZULTAT'}
                                </h4>

                                <div className={`text-lg leading-relaxed font-bold mb-4 ${activeRisk.successEffect && (riskMessage === activeRisk.successMessage || riskMessage === 'POZYTYWNY EFEKT') ? 'text-green-400' : 'text-gray-300'}`}>
                                    {riskMessage}
                                </div>

                                {/* Render Result Effects if any */}
                                <div className="flex flex-col gap-2">
                                    {((riskMessage === activeRisk.successMessage || riskMessage === 'POZYTYWNY EFEKT')
                                        ? activeRisk.successEffect
                                        : activeRisk.failureEffect)?.map((effect, idx) => (
                                            <div key={idx} className="flex items-center gap-3 text-left">
                                                {effect.type === 'KW' && <div className="p-2 bg-blue-500/20 rounded-lg text-blue-400"><Gem size={18} /></div>}
                                                {effect.type === 'EFFICIENCY' && <div className="p-2 bg-green-500/20 rounded-lg text-green-400"><TrendingUp size={18} /></div>}
                                                {effect.type === 'AVAILABILITY' && <div className="p-2 bg-orange-500/20 rounded-lg text-orange-400"><Clock size={18} /></div>}
                                                {effect.type === 'CASH' && <div className="p-2 bg-yellow-500/20 rounded-lg text-yellow-400"><DollarSign size={18} /></div>}

                                                <span className="font-bold text-gray-200">{effect.description}</span>
                                            </div>
                                        ))}
                                </div>

                                {(riskMessage === 'BRAK ZMIAN' && !activeRisk.failureMessage) && (
                                    <div className="mt-2 text-sm text-gray-500 italic">Bez dodatkowego wpływu na firmę.</div>
                                )}
                            </div>
                        )}

                        {/* DEBUG TOOL */}
                        {processed && (
                            <button
                                onClick={(e) => {
                                    e.stopPropagation();
                                    setProcessed(false);
                                    setActiveRisk(null);
                                    setDiceResult(null);
                                    setRiskMessage('');
                                    setIsRevealed(false);
                                    dispatch({ type: 'SET_PHASE_READY', payload: false });

                                    // Cycle next
                                    const currentIndex = EVENTS_DATA.findIndex(e => e.id === card.id);
                                    const nextIndex = (currentIndex + 1) % EVENTS_DATA.length;
                                    setCard(EVENTS_DATA[nextIndex] as unknown as EventCard);
                                }}
                                className="mt-6 py-2 px-4 bg-gray-800/80 hover:bg-gray-700 text-gray-400 text-xs font-mono border border-gray-700 rounded w-full flex items-center justify-center gap-2 transition-colors z-50"
                            >
                                <ChevronRight size={12} /> [DEBUG] Następna karta ({EVENTS_DATA.findIndex(e => e.id === card.id) + 1}/{EVENTS_DATA.length})
                            </button>
                        )}


                    </div>
                </motion.div>
            </div>


        </div>
    )
}
