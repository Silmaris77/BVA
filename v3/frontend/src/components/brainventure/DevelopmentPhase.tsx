"use client"

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { useBrainVenture } from './BrainVentureContext'
import { Dices, TrendingUp, User, Users, ArrowRight, Brain } from 'lucide-react'

// Helper to roll dice
const rollDice = (count: number = 1): number[] => {
    return Array.from({ length: count }, () => Math.floor(Math.random() * 6) + 1)
}

export default function DevelopmentPhase() {
    const { state, dispatch } = useBrainVenture()
    const [selectedAction, setSelectedAction] = useState<'EMPLOYEE' | 'TEAM' | 'MANAGER' | null>(null)
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [targetId, setTargetId] = useState<string | null>(null) // For specific employee selection if needed logic expanded
    const [diceResult, setDiceResult] = useState<number[] | null>(null)
    const [success, setSuccess] = useState<boolean | null>(null)
    const [isRolling, setIsRolling] = useState(false)

    // Enable global navigation on mount
    React.useEffect(() => {
        dispatch({ type: 'SET_PHASE_READY', payload: true })
    }, [])

    // Simplified for MVP: Select action type -> Roll -> Apply effect
    // We assume 2 employees always exist for 'TEAM' action.

    const manager = state.team.find(c => c.role === 'MANAGER')
    // Start with 0 if no manager found? Should allow error handling but we hardcoded manager
    const managerEfficiency = manager?.efficiency || 0
    const managerAvailability = manager?.availability || 0

    const costs = {
        'EMPLOYEE': { label: 'Szkolenie Pracownika', costManager: 5, costEmployee: 5, target: '1 Pracownik' },
        'TEAM': { label: 'Szkolenie Zespołu', costManager: 5, costEmployee: 5, target: 'Wszyscy Pracownicy' }, // cost is per employee
        'MANAGER': { label: 'Szkolenie Siebie', costManager: 5, costEmployee: 0, target: 'Ty (Menedżer)' }
    }

    const canAfford = (action: 'EMPLOYEE' | 'TEAM' | 'MANAGER') => {
        if (action === 'MANAGER') {
            return managerAvailability >= 5
        }
        // Logic simplification for MVP: Check if manager has 5 PD and if at least one employee has 5 PD
        // For TEAM: Manager 5 PD and ALL employees 5 PD? Usually yes.
        const employees = state.team.filter(c => c.role === 'EMPLOYEE')
        const empWithPD = employees.filter(e => e.availability >= 5)

        if (action === 'EMPLOYEE') return managerAvailability >= 5 && empWithPD.length > 0
        if (action === 'TEAM') return managerAvailability >= 5 && empWithPD.length === employees.length // All must have PD? Or just subtract from those who have? Rules say "5 PD u obu" implies cost requirement.

        return false
    }

    const handleAction = (actionType: 'EMPLOYEE' | 'TEAM' | 'MANAGER') => {
        if (!canAfford(actionType)) return
        setSelectedAction(actionType)
        setDiceResult(null)
        setSuccess(null)
    }

    const handleRoll = () => {
        setIsRolling(true)
        setTimeout(() => {
            const rolls = rollDice(2)
            setDiceResult(rolls)
            const sum = rolls.reduce((a, b) => a + b, 0)
            const totalScore = sum + managerEfficiency
            const isSuccess = totalScore >= 12

            setSuccess(isSuccess)
            setIsRolling(false)

            if (isSuccess && selectedAction) {
                // Apply effects logic
                // Simplified application:
                // 1. Deduct costs
                // 2. Add efficiency

                // Deduct Manager PD
                dispatch({ type: 'UPDATE_AVAILABILITY', payload: { charId: 'manager', amount: -5 } })

                // Delay the gain animation to separate it from cost
                setTimeout(() => {
                    if (selectedAction === 'MANAGER') {
                        dispatch({ type: 'UPDATE_EFFICIENCY', payload: { charId: 'manager', amount: 1 } })
                    } else if (selectedAction === 'EMPLOYEE') {
                        // Pick the first available employee for MVP simplicity or logic to choose
                        const emp = state.team.find(c => c.role === 'EMPLOYEE' && c.availability >= 5)
                        if (emp) {
                            dispatch({ type: 'UPDATE_AVAILABILITY', payload: { charId: emp.id, amount: -5 } }) // This one is cost for employee, should it be delayed? 
                            // Actually cost should be immediate. The logic here: Manager pays 5, Employee pays 5.
                            // So both costs should be immediate.
                            // I will copy the cost part out.
                        }
                    } else if (selectedAction === 'TEAM') {
                        /* Logic split below */
                    }
                }, 1000)

                // Handling Employee/Team costs immediately
                if (selectedAction === 'EMPLOYEE') {
                    const emp = state.team.find(c => c.role === 'EMPLOYEE' && c.availability >= 5)
                    if (emp) dispatch({ type: 'UPDATE_AVAILABILITY', payload: { charId: emp.id, amount: -5 } })
                } else if (selectedAction === 'TEAM') {
                    const employees = state.team.filter(c => c.role === 'EMPLOYEE')
                    employees.forEach(emp => {
                        dispatch({ type: 'UPDATE_AVAILABILITY', payload: { charId: emp.id, amount: -5 } })
                    })
                }

                // Helper to find valid employee target (re-declared for clarity)
                const targetEmployee = state.team.find(c => c.role === 'EMPLOYEE' && c.availability >= 5)
                const allEmployees = state.team.filter(c => c.role === 'EMPLOYEE')

                // 2. Add Efficiency Gain Immediately (Simultaneous Animation in Panel)
                if (selectedAction === 'MANAGER') {
                    dispatch({ type: 'UPDATE_EFFICIENCY', payload: { charId: 'manager', amount: 1 } })
                } else if (selectedAction === 'EMPLOYEE' && targetEmployee) {
                    dispatch({ type: 'UPDATE_EFFICIENCY', payload: { charId: targetEmployee.id, amount: 1 } })
                } else if (selectedAction === 'TEAM') {
                    allEmployees.forEach(emp => {
                        dispatch({ type: 'UPDATE_EFFICIENCY', payload: { charId: emp.id, amount: 1 } })
                    })
                }
            } else {
                // Failure: Only deduct costs
                // Deduct Manager PD
                dispatch({ type: 'UPDATE_AVAILABILITY', payload: { charId: 'manager', amount: -5 } })

                if (selectedAction === 'EMPLOYEE') {
                    const emp = state.team.find(c => c.role === 'EMPLOYEE' && c.availability >= 5)
                    if (emp) dispatch({ type: 'UPDATE_AVAILABILITY', payload: { charId: emp.id, amount: -5 } })
                } else if (selectedAction === 'TEAM') {
                    const employees = state.team.filter(c => c.role === 'EMPLOYEE')
                    employees.forEach(emp => {
                        dispatch({ type: 'UPDATE_AVAILABILITY', payload: { charId: emp.id, amount: -5 } })
                    })
                }
            }

        }, 1000)
    }

    const handleNext = () => {
        dispatch({ type: 'NEXT_PHASE' })
    }

    return (
        <div className="h-full flex flex-col items-center max-w-5xl mx-auto w-full pt-4">
            <h2 className="text-3xl font-bold text-green-400 mb-2">Faza 4: Rozwój (Inwestycje)</h2>
            <p className="text-gray-400 mb-8">Zainwestuj Punkty Dostępności (PD) w Efektywność. Test Sukcesu: 2d6 + Efektywność Menedżera ({managerEfficiency}) {'>'}= 12.</p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mb-8">
                {/* Actions Cards */}
                {(['EMPLOYEE', 'TEAM', 'MANAGER'] as const).map((action) => (
                    <motion.div
                        key={action}
                        whileHover={{ scale: 1.02 }}
                        className={`bg-gray-800 border-2 rounded-xl p-6 cursor-pointer transition-colors relative overflow-hidden ${selectedAction === action ? 'border-green-500 bg-gray-700' : 'border-gray-700 hover:border-gray-500'} ${!canAfford(action) ? 'opacity-50 grayscale pointer-events-none' : ''}`}
                        onClick={() => handleAction(action)}
                    >
                        <div className="absolute top-0 right-0 p-2 bg-gray-900/50 rounded-bl-lg text-xs font-mono text-gray-400">
                            Koszt: {costs[action].costManager} PD (Ty) {costs[action].costEmployee > 0 ? `+ ${costs[action].costEmployee} PD (Prac.)` : ''}
                        </div>
                        <div className="flex items-center gap-3 mb-4">
                            <div className="p-3 bg-green-900/30 rounded-lg text-green-400">
                                {action === 'MANAGER' ? <User /> : <Users />}
                            </div>
                            <h3 className="font-bold text-lg text-white">{costs[action].label}</h3>
                        </div>
                        <p className="text-sm text-gray-400">Zwiększ efektywność: {costs[action].target}</p>
                    </motion.div>
                ))}
            </div>

            {/* Knowledge Academy Section */}
            <div className="w-full max-w-5xl mb-8 flex flex-col gap-4">
                <div className="flex items-center gap-3 mb-2">
                    <div className="p-2 bg-purple-900/30 rounded-lg text-purple-400">
                        <Brain size={24} />
                    </div>
                    <h3 className="text-2xl font-bold text-purple-400">Akademia Wiedzy (Inwestuj KW)</h3>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {state.team.map(char => {
                        const upgradeCost = char.role === 'MANAGER' ? 5 : 3
                        const canAfford = state.knowledgeCrystals >= upgradeCost

                        return (
                            <motion.div
                                key={char.id}
                                className="bg-gray-800/80 border border-purple-500/30 p-6 rounded-xl flex flex-col justify-between relative overflow-hidden group"
                            >
                                <div className="absolute top-0 right-0 p-3 opacity-10 group-hover:opacity-20 transition-opacity text-purple-500">
                                    <TrendingUp size={80} />
                                </div>

                                <div>
                                    <div className="flex justify-between items-center mb-2">
                                        <span className={`font-bold text-lg ${char.role === 'MANAGER' ? 'text-yellow-400' : 'text-blue-300'}`}>{char.name}</span>
                                        <span className="text-xs uppercase bg-gray-900 px-2 py-1 rounded text-gray-500">{char.role}</span>
                                    </div>
                                    <div className="flex items-center gap-2 mb-4">
                                        <span className="text-gray-400 text-sm">Obecne PE:</span>
                                        <span className="text-green-400 font-bold font-mono text-xl">{char.efficiency}</span>
                                    </div>
                                </div>

                                <button
                                    onClick={() => {
                                        if (canAfford) {
                                            dispatch({ type: 'UPDATE_KW', payload: -upgradeCost })
                                            dispatch({ type: 'UPDATE_EFFICIENCY', payload: { charId: char.id, amount: 1 } })
                                        } else {
                                            alert(`Za mało Kryształów Wiedzy (Wymagane: ${upgradeCost} KW)`)
                                        }
                                    }}
                                    disabled={!canAfford}
                                    className="w-full py-2 bg-purple-600 hover:bg-purple-500 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-lg text-white font-bold shadow-lg transition-all flex items-center justify-center gap-2"
                                >
                                    <span>Szkolenie (+1 PE)</span>
                                    <span className="text-xs bg-purple-800 px-2 py-0.5 rounded text-purple-200">-{upgradeCost} KW</span>
                                </button>
                            </motion.div>
                        )
                    })}
                </div>
            </div>

            {/* Results Area - Only show when action selected */}
            {selectedAction && (
                <div className="flex-1 w-full bg-gray-900/50 rounded-2xl border border-gray-700 p-8 flex flex-col items-center justify-center relative animate-fade-in">
                    <div className="text-center w-full max-w-md">
                        <h3 className="text-2xl font-bold text-white mb-6">Test Sukcesu</h3>

                        {!diceResult && !isRolling && (
                            <button
                                onClick={handleRoll}
                                className="bg-green-600 hover:bg-green-500 text-white px-12 py-4 rounded-full font-bold text-xl shadow-[0_0_30px_rgba(34,197,94,0.4)] flex items-center gap-3 mx-auto transition-transform hover:scale-105"
                            >
                                <Dices size={28} /> Rzuć Kośćmi (2d6)
                            </button>
                        )}

                        {/* Dice Animation placeholder */}
                        {isRolling && <div className="text-4xl animate-bounce text-green-400 font-mono">🎲 ...</div>}

                        {diceResult && (
                            <motion.div
                                initial={{ opacity: 0, scale: 0.5 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="bg-gray-800 rounded-xl p-6 border border-gray-600"
                            >
                                <div className="flex justify-center gap-4 text-4xl font-bold text-white mb-4">
                                    <div className="w-16 h-16 bg-black rounded flex items-center justify-center border border-gray-600">{diceResult[0]}</div>
                                    <div className="w-16 h-16 bg-black rounded flex items-center justify-center border border-gray-600">{diceResult[1]}</div>
                                </div>
                                <div className="text-xl text-gray-300 mb-2">
                                    Suma: {diceResult[0] + diceResult[1]} + {managerEfficiency} (Twój PE) = <span className="font-bold text-white">{diceResult[0] + diceResult[1] + managerEfficiency}</span>
                                </div>
                                <div className={`text-2xl font-bold ${success ? 'text-green-400' : 'text-red-400'} uppercase tracking-widest`}>
                                    {success ? 'SUKCES! (+1 PE)' : 'PORAŻKA'}
                                </div>
                            </motion.div>
                        )}
                    </div>
                </div>
            )}


        </div>
    )
}
