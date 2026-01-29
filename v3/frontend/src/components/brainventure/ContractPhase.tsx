"use client"

import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useBrainVenture } from './BrainVentureContext'
import CONTRACTS_DATA from '@/data/brainventure/contracts.json'
import { ContractCard, ActiveContract } from '@/types/brainventure'
import { Briefcase, ArrowRight, CheckCircle, Clock } from 'lucide-react'

export default function ContractPhase() {
    const { state, dispatch, formatMoney, getTeamProductivity } = useBrainVenture()
    const [availableContracts, setAvailableContracts] = useState<ContractCard[]>([])

    const handleFinishContract = (contract: ActiveContract) => {
        dispatch({ type: 'COMPLETE_CONTRACT', payload: contract.id })
    }

    React.useEffect(() => {
        // Just pick 5 random for display demo
        const shuffled = [...CONTRACTS_DATA].sort(() => 0.5 - Math.random())
        setAvailableContracts(shuffled.slice(0, 5) as unknown as ContractCard[])

        // Enable Global Navigation
        dispatch({ type: 'SET_PHASE_READY', payload: true })
    }, [])

    const handleTakeContract = (contract: ContractCard) => {
        dispatch({ type: 'ADD_CONTRACT', payload: { ...contract, startedRound: state.round, currentProductivity: 0 } })
        setAvailableContracts(prev => prev.filter(c => c.id !== contract.id))
    }

    const teamProductivity = getTeamProductivity()

    return (
        <div className="h-full flex flex-col items-center max-w-6xl mx-auto w-full pt-4 relative">

            <h2 className="text-3xl font-bold text-orange-400 mb-2">Faza 5: Kontrakty</h2>
            <p className="text-gray-400 mb-6">Wybierz nowe zlecenia i realizuj aktywne. Twoja moc przerobowa (Wydajność): <span className="text-blue-300 font-bold">{teamProductivity}</span></p>

            <div className="flex gap-8 w-full flex-1 overflow-hidden">
                {/* Active Contracts Panel */}
                {/* Active Contracts Panel */}
                <div className="w-1/3 bg-gray-900/50 rounded-2xl border border-gray-700 p-6 flex flex-col">
                    <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2 border-b border-gray-700 pb-2">
                        Twoje Aktywne Kontrakty
                    </h3>

                    <div className="flex-1 overflow-y-auto custom-scrollbar flex flex-col gap-4 pr-1">
                        {state.activeContracts.length === 0 && <div className="text-gray-500 italic mt-8 text-center">Brak aktywnych kontraktów.</div>}

                        {state.activeContracts.map(contract => (
                            <motion.div
                                key={contract.id}
                                initial={{ x: -20, opacity: 0 }}
                                animate={{ x: 0, opacity: 1 }}
                                className="bg-gray-800 rounded-lg p-4 border border-blue-500 shadow-md flex-shrink-0"
                            >
                                <div className="flex justify-between items-start mb-2">
                                    <span className="font-bold text-blue-200">{contract.title}</span>
                                    <span className="text-green-400 font-mono">{formatMoney(contract.value)}</span>
                                </div>
                                <div className="text-xs text-gray-400 mb-3">{contract.description}</div>

                                <ContractProgressControl
                                    contract={contract}
                                    team={state.team}
                                    onAssign={(costMap, totalEff) => {
                                        Object.entries(costMap).forEach(([id, cost]) => {
                                            dispatch({ type: 'UPDATE_AVAILABILITY', payload: { charId: id, amount: -cost } })
                                        })
                                        dispatch({ type: 'UPDATE_CONTRACT_PROGRESS', payload: { contractId: contract.id, amount: totalEff } })
                                    }}
                                    onComplete={() => {
                                        dispatch({ type: 'COMPLETE_CONTRACT', payload: contract.id })
                                        dispatch({ type: 'UPDATE_CASH', payload: contract.value })
                                    }}
                                />
                            </motion.div>
                        ))}
                    </div>
                </div>

                {/* Market Panel */}
                <div className="w-2/3 bg-gray-900/50 rounded-2xl border border-gray-700 p-6 flex flex-col">
                    <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2 border-b border-gray-700 pb-2">
                        <Briefcase className="text-orange-400" /> Giełda Kontraktów (Dostępne)
                    </h3>

                    <div className="grid grid-cols-2 gap-4 overflow-y-auto custom-scrollbar flex-1 content-start">
                        {availableContracts.map(contract => (
                            <motion.div
                                key={contract.id}
                                whileHover={{ scale: 1.02 }}
                                className="bg-gray-800 rounded-lg p-4 border border-gray-600 hover:border-orange-500 cursor-pointer flex flex-col justify-between"
                            >
                                <div>
                                    <div className="flex justify-between items-start mb-2">
                                        <h4 className="font-bold text-gray-200">{contract.title}</h4>
                                        <span className="text-green-400 font-mono font-bold bg-green-900/30 px-2 py-1 rounded text-sm">{formatMoney(contract.value)}</span>
                                    </div>
                                    <div className="flex gap-4 text-xs text-gray-400 mb-3">
                                        <span className="flex items-center gap-1"><Clock size={12} /> Max {contract.duration} rundy</span>
                                        <span className="flex items-center gap-1"><ArrowRight size={12} /> Wymaga {contract.requiredProductivity} W</span>
                                    </div>
                                    <p className="text-sm text-gray-500 line-clamp-3">{contract.description}</p>
                                </div>
                                <button
                                    onClick={() => handleTakeContract(contract)}
                                    className="mt-4 w-full border border-orange-500/50 text-orange-400 hover:bg-orange-500 hover:text-white py-2 rounded transition-colors text-sm font-bold uppercase tracking-wider"
                                >
                                    Pobierz Kontrakt
                                </button>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </div>


        </div>
    )
}

function ContractProgressControl({ contract, team, onAssign, onComplete }: { contract: ActiveContract, team: any[], onAssign: (costMap: Record<string, number>, totalEff: number) => void, onComplete: () => void }) {
    const [sliderValue, setSliderValue] = useState(0)

    const remainingNeeded = contract.requiredProductivity - (contract.currentProductivity || 0)
    const maxPotential = team.reduce((sum: number, char: any) => sum + (char.efficiency * char.availability), 0)
    const maxSlider = Math.min(remainingNeeded, maxPotential)

    const calculateCost = (target: number) => {
        let needed = target
        let totalEff = 0
        const costMap: Record<string, number> = {}
        const sortedTeam = [...team].sort((a: any, b: any) => b.efficiency - a.efficiency)

        for (const char of sortedTeam) {
            if (needed <= 0) break
            if (char.availability <= 0) continue

            const maxPD = char.availability
            const pdForNeed = Math.ceil(needed / char.efficiency)
            const pdToTake = Math.min(maxPD, pdForNeed)

            if (pdToTake > 0) {
                costMap[char.id] = pdToTake
                const contribution = pdToTake * char.efficiency
                totalEff += contribution
                needed -= contribution
            }
        }
        return { costMap, totalEff }
    }

    const { costMap, totalEff } = calculateCost(sliderValue)

    const handleBarClick = (e: React.MouseEvent<HTMLDivElement>) => {
        if (contract.currentProductivity >= contract.requiredProductivity) return

        const rect = e.currentTarget.getBoundingClientRect()
        const clickX = e.clientX - rect.left
        const percent = clickX / rect.width

        // Snap to end if close (UX fix)
        let targetTotal = percent * contract.requiredProductivity
        if (percent > 0.95) targetTotal = contract.requiredProductivity

        let internalTarget = targetTotal - (contract.currentProductivity || 0)

        if (internalTarget < 0) internalTarget = 0
        if (internalTarget < 3) internalTarget = 0 // Snap to 0 if very small (fixes "stuck at 5W" issue)
        if (internalTarget > maxSlider) internalTarget = maxSlider

        setSliderValue(Math.ceil(internalTarget))
    }

    const handleAssignClick = () => {
        onAssign(costMap, totalEff)
        setSliderValue(0)
    }

    if (contract.currentProductivity >= contract.requiredProductivity) {
        return (
            <button
                onClick={onComplete}
                className="w-full py-2 bg-gradient-to-r from-yellow-500 to-amber-600 hover:from-yellow-400 hover:to-amber-500 rounded text-sm text-black font-bold uppercase tracking-wider shadow-[0_0_15px_rgba(251,191,36,0.5)] animate-pulse hover:scale-105 transition-transform"
            >
                Zakończ i Odbierz {contract.value} PLN
            </button>
        )
    }

    return (
        <div className="flex flex-col gap-2">
            <div className="relative h-8 bg-gray-700 rounded-lg overflow-hidden cursor-pointer group select-none shadow-inner"
                onClick={handleBarClick}
                onMouseMove={(e) => {
                    if (e.buttons === 1) handleBarClick(e)
                }}
                title="Kliknij lub przeciągnij, aby ustawić cel"
            >
                {/* Explicit Clickable MIN Handle (Thick Vertical Line) */}
                <div
                    className="absolute top-0 bottom-0 left-0 w-4 z-30 flex items-center justify-center cursor-pointer group/min"
                    onClick={(e) => {
                        e.stopPropagation()
                        setSliderValue(0)
                    }}
                    title="Reset (0)"
                >
                    <div className="w-1 h-2/3 bg-gray-500 group-hover/min:bg-red-400 group-hover/min:w-1.5 transition-all rounded-full" />
                </div>

                {/* Explicit Clickable MAX Handle (Thick Vertical Line) */}
                <div
                    className="absolute top-0 bottom-0 right-0 w-4 z-30 flex items-center justify-center cursor-pointer group/max"
                    onClick={(e) => {
                        e.stopPropagation()
                        setSliderValue(maxSlider)
                    }}
                    title="Max (Full)"
                >
                    <div className="w-1 h-2/3 bg-gray-500 group-hover/max:bg-green-400 group-hover/max:w-1.5 transition-all rounded-full" />
                </div>

                <div
                    className="absolute top-0 left-0 h-full bg-blue-600/80 border-r border-blue-400/50"
                    style={{ width: `${Math.min(100, ((contract.currentProductivity || 0) / contract.requiredProductivity) * 100)}%` }}
                />
                <div
                    className="absolute top-0 left-0 h-full bg-green-500/60 transition-all duration-100"
                    style={{
                        left: `${((contract.currentProductivity || 0) / contract.requiredProductivity) * 100}%`,
                        width: `${Math.min(100 - ((contract.currentProductivity || 0) / contract.requiredProductivity) * 100, (totalEff / contract.requiredProductivity) * 100)}%`,
                        opacity: totalEff > 0 ? 1 : 0
                    }}
                />
                {totalEff > 0 && (
                    <div
                        className="absolute top-0 bottom-0 w-1 bg-white shadow-[0_0_10px_white] z-10 pointer-events-none transition-all duration-100"
                        style={{ left: `${Math.min(100, (((contract.currentProductivity || 0) + totalEff) / contract.requiredProductivity) * 100)}%` }}
                    />
                )}
                <div className="absolute inset-0 flex items-center justify-center text-[10px] font-bold text-white drop-shadow-[0_1px_1px_rgba(0,0,0,0.8)] pointer-events-none">
                    <span className="z-20">
                        {Math.min(contract.requiredProductivity, (contract.currentProductivity || 0) + totalEff)} / {contract.requiredProductivity} W
                    </span>
                </div>
            </div>

            <div className="flex justify-end items-center text-[10px] min-h-[20px]">
                {sliderValue > 0 && (
                    <button
                        onClick={handleAssignClick}
                        className="px-4 py-0.5 bg-green-600 hover:bg-green-500 text-white rounded text-xs font-bold transition-colors animate-pulse"
                    >
                        Zatwierdź
                    </button>
                )}
            </div>
        </div >
    )
}
