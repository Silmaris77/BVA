import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useBrainVenture } from './BrainVentureContext'
import EVENTS_DATA from '@/data/brainventure/events.json'
import { EventCard, EventOption, EventEffect, EventRisk } from '@/types/brainventure'
import { Disc, PlayCircle, Dices, ChevronRight } from 'lucide-react'

// Simple dice roll helper
const rollDice = (count: number = 1): number[] => {
    return Array.from({ length: count }, () => Math.floor(Math.random() * 6) + 1)
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

    // Draw card on mount
    useEffect(() => {
        if (state.currentEvent) {
            setCard(state.currentEvent)
            return
        }

        // FOR TESTING: Force the new test event
        const testEvent = EVENTS_DATA.find(e => e.id === 'event_test_loss') || EVENTS_DATA[0]
        setCard(testEvent as unknown as EventCard)
        dispatch({ type: 'LOG_EVENT', payload: testEvent.id })
        dispatch({ type: 'SET_CURRENT_EVENT', payload: testEvent as unknown as EventCard }) // [NEW] Save immediately
    }, [])

    const handleReveal = () => {
        setIsRevealed(true)
        // Auto-apply immediate effects if no options
        if (card && !card.options && card.immediateEffects) {
            applyEffects(card.immediateEffects)
            setProcessed(true)
            dispatch({ type: 'SET_PHASE_READY', payload: true }) // [NEW]
        }
        // If no interaction needed (info only)
        if (card && !card.options && !card.immediateEffects) {
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
                }
                // Simplified employee targeting
            }

            if (effect.type === 'AVAILABILITY') {
                if (effect.target === 'MANAGER') {
                    dispatch({ type: 'UPDATE_AVAILABILITY', payload: { charId: 'manager', amount: effect.amount } })
                } else if (effect.target === 'EMPLOYEE') {
                    // MVP: Hit the first employee or all? Assuming first for now or random
                    // Better: "target" could be specific ID, but we used generic roles.
                    const emp = state.team.find(c => c.role === 'EMPLOYEE')
                    if (emp) dispatch({ type: 'UPDATE_AVAILABILITY', payload: { charId: emp.id, amount: effect.amount } })
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
            // Wait for roll
        } else {
            setProcessed(true)
            dispatch({ type: 'SET_PHASE_READY', payload: true }) // [NEW]
        }
    }

    const handleRiskRoll = () => {
        if (!activeRisk) return

        const results = rollDice(activeRisk.diceCount)
        setDiceResult(results)
        const sum = results.reduce((a, b) => a + b, 0)

        let success = false
        if (activeRisk.rule === 'SUM_GE') success = sum >= activeRisk.targetValue
        if (activeRisk.rule === 'CONTAINS') success = results.includes(activeRisk.targetValue)
        // ... other rules

        if (success) {
            setRiskMessage('SUKCES!')
            if (activeRisk.successEffect) applyEffects(activeRisk.successEffect)
        } else {
            setRiskMessage('PORAŻKA...')
            if (activeRisk.failureEffect) applyEffects(activeRisk.failureEffect)
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
                    <div className="absolute inset-0 backface-hidden bg-gradient-to-br from-blue-900 to-slate-900 rounded-2xl border-2 border-blue-500/30 flex flex-col items-center justify-center shadow-[0_0_50px_rgba(59,130,246,0.2)] hover:shadow-blue-500/40 transition-shadow">
                        <Disc size={64} className="text-blue-400/50 animate-spin-slow" />
                        <span className="mt-4 text-xl font-bold text-blue-300 uppercase tracking-widest">Karta Zdarzenia</span>
                        <span className="text-sm text-blue-400/60 mt-2">Kliknij, aby odkryć</span>
                    </div>

                    {/* Card Front */}
                    <div
                        className="absolute inset-0 backface-hidden bg-slate-800 rounded-2xl border border-gray-600 p-8 flex flex-col items-center text-center shadow-2xl overflow-y-auto custom-scrollbar"
                        style={{ transform: 'rotateY(180deg)' }}
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

                        {/* Risk / Dice Interface */}
                        {activeRisk && !processed && (
                            <div className="mt-auto">
                                <p className="text-yellow-400 font-bold mb-4">Wymagany rzut kostką!</p>
                                <button
                                    onClick={(e) => { e.stopPropagation(); handleRiskRoll() }}
                                    className="py-3 px-8 bg-yellow-600 hover:bg-yellow-500 rounded-full font-bold text-black shadow-lg animate-pulse"
                                >
                                    <Dices size={24} className="inline mr-2" /> Rzuć ({activeRisk.diceCount}d6)
                                </button>
                            </div>
                        )}

                        {/* Result Display */}
                        {diceResult && (
                            <div className="mt-4 p-4 bg-gray-900/50 rounded-xl border border-gray-700 w-full">
                                <div className="text-2xl font-mono mb-2">🎲 {diceResult.join(' + ')} = {diceResult.reduce((a, b) => a + b, 0)}</div>
                                <div className={`text-xl font-bold ${riskMessage === 'SUKCES!' ? 'text-green-400' : 'text-red-400'}`}>
                                    {riskMessage}
                                </div>
                            </div>
                        )}


                    </div>
                </motion.div>
            </div>


        </div>
    )
}
