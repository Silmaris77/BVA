"use client"

import React from 'react'
import { useBrainVenture } from './BrainVentureContext'
import { motion, AnimatePresence } from 'framer-motion'
import { Users, Zap, Clock, Disc } from 'lucide-react'

export default function GameContextPanel() {
    const { state } = useBrainVenture()
    const { currentEvent, team } = state

    return (
        <div className="w-80 h-full bg-[var(--bg-deep)] border-r border-gray-800 flex flex-col overflow-hidden">
            {/* 1. Active Event Widget */}
            <div className="p-4 border-b border-gray-800">
                <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-3">Aktywne Zdarzenie</h3>

                {currentEvent ? (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className={`rounded-xl p-4 border relative overflow-hidden ${currentEvent.type === 'POSITIVE' ? 'bg-green-900/20 border-green-500/30' :
                            currentEvent.type === 'NEGATIVE' ? 'bg-red-900/20 border-red-500/30' :
                                'bg-yellow-900/20 border-yellow-500/30'
                            }`}
                    >
                        <div className={`absolute left-0 top-0 bottom-0 w-1 ${currentEvent.type === 'POSITIVE' ? 'bg-green-500' :
                            currentEvent.type === 'NEGATIVE' ? 'bg-red-500' :
                                'bg-yellow-500'
                            }`} />

                        <div className="flex items-start gap-3">
                            <Disc className={`w-5 h-5 flex-shrink-0 mt-0.5 ${currentEvent.type === 'POSITIVE' ? 'text-green-400' :
                                currentEvent.type === 'NEGATIVE' ? 'text-red-400' :
                                    'text-yellow-400'
                                }`} />
                            <div>
                                <h4 className="text-sm font-bold text-white leading-tight mb-1">{currentEvent.title}</h4>
                                <p className="text-xs text-gray-400 line-clamp-3">{currentEvent.description}</p>
                            </div>
                        </div>
                    </motion.div>
                ) : (
                    <div className="rounded-xl p-4 border border-gray-800 bg-gray-900/50 flex flex-col items-center justify-center text-gray-600 gap-2 py-8">
                        <Disc className="w-8 h-8 opacity-20" />
                        <span className="text-xs">Brak aktywnego zdarzenia</span>
                    </div>
                )}
            </div>

            {/* 2. Team Status Widget */}
            <div className="flex-1 overflow-y-auto custom-scrollbar p-4">
                <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-3 flex items-center gap-2">
                    <Users size={14} /> Zespół ({team.length})
                </h3>

                <div className="flex flex-col gap-3">
                    {team.map(char => (
                        <CharacterStatusCard key={char.id} char={char} />
                    ))}
                </div>
            </div>
        </div>
    )
}

function CharacterStatusCard({ char }: { char: any }) {
    const { state } = useBrainVenture()
    const prevEff = React.useRef(char.efficiency)
    const prevAvail = React.useRef(char.availability)
    const [effChange, setEffChange] = React.useState<number | null>(null)
    const [availChange, setAvailChange] = React.useState<number | null>(null)

    React.useEffect(() => {
        if (char.efficiency !== prevEff.current) {
            const diff = char.efficiency - prevEff.current
            setEffChange(diff)
            prevEff.current = char.efficiency
            const timer = setTimeout(() => setEffChange(null), 3000)
            return () => clearTimeout(timer)
        }
    }, [char.efficiency])

    React.useEffect(() => {
        if (char.availability !== prevAvail.current) {
            const diff = char.availability - prevAvail.current
            setAvailChange(diff)
            prevAvail.current = char.availability
            const timer = setTimeout(() => setAvailChange(null), 3000)
            return () => clearTimeout(timer)
        }
    }, [char.availability])

    return (
        <div className="bg-gray-800/50 rounded-lg p-3 border border-gray-700 relative overflow-hidden">
            <div className="flex justify-between items-center mb-2">
                <span className={`text-sm font-bold ${char.role === 'MANAGER' ? 'text-blue-300' : 'text-gray-300'}`}>
                    {char.name}
                </span>
                <span className="text-[10px] bg-gray-700 px-1.5 py-0.5 rounded text-gray-400">
                    {char.role === 'MANAGER' ? 'LIDER' : 'PRACOWNIK'}
                </span>
            </div>

            {/* Efficiency Bar */}
            <div className="mb-2 relative">
                <div className="flex justify-between text-[10px] text-gray-400 mb-0.5">
                    <span className="flex items-center gap-1"><Zap size={10} /> Efektywność (PE)</span>
                    <span className={`transition-colors duration-300 ${effChange ? (effChange > 0 ? 'text-green-400 scale-125' : 'text-red-400 scale-125') : 'text-white'}`}>
                        {char.efficiency}
                    </span>
                </div>
                <div className="h-1.5 bg-gray-900 rounded-full overflow-hidden">
                    <motion.div
                        className="h-full bg-blue-500"
                        initial={{ width: `${Math.min(100, (prevEff.current / 10) * 100)}%` }}
                        animate={{ width: `${Math.min(100, (char.efficiency / 10) * 100)}%` }}
                        transition={{ duration: 0.5 }}
                    />
                </div>

            </div>

            {/* Availability Bar */}
            <div className="relative">
                <div className="flex justify-between text-[10px] text-gray-400 mb-0.5">
                    <span className="flex items-center gap-1"><Clock size={10} /> Dostępność (PD)</span>
                    <span className={`transition-colors duration-300 ${availChange ? (availChange > 0 ? 'text-green-400 scale-125' : 'text-red-400 scale-125') : (char.availability > 0 ? 'text-white' : 'text-red-400')}`}>
                        {/* Show Projected: Current - Cost */}
                        {state.projectedTeamCost?.[char.id] ? (
                            <span className="text-red-400 font-bold animate-pulse">
                                {Math.max(0, char.availability - state.projectedTeamCost[char.id])}/{char.maxAvailability}
                            </span>
                        ) : (
                            <span>{char.availability}/{char.maxAvailability}</span>
                        )}
                    </span>
                </div>
                <div className="h-1.5 bg-gray-900 rounded-full overflow-hidden flex">
                    {/* Remaining Bar */}
                    <motion.div
                        className={`h-full transition-colors duration-300 ${char.availability > 5 ? 'bg-green-500' :
                            char.availability > 0 ? 'bg-orange-500' : 'bg-red-500'
                            }`}
                        initial={{ width: `${(prevAvail.current / char.maxAvailability) * 100}%` }}
                        animate={{ width: `${(Math.max(0, char.availability - (state.projectedTeamCost?.[char.id] || 0)) / char.maxAvailability) * 100}%` }}
                        transition={{ duration: 0.3 }}
                    />
                    {/* COST Ghost Bar */}
                    {state.projectedTeamCost?.[char.id] ? (
                        <div
                            className="h-full bg-red-600/50 animate-pulse"
                            style={{ width: `${(Math.min(char.availability, state.projectedTeamCost[char.id]) / char.maxAvailability) * 100}%` }}
                        />
                    ) : null}
                </div>
            </div>

            {/* Stat Change Overlay (Side-by-Side) */}
            <AnimatePresence>
                {effChange !== null && (
                    <motion.div
                        key="eff"
                        initial={{ opacity: 0, scale: 0.5, x: -20 }}
                        animate={{ opacity: 1, scale: 1.2, x: 0 }}
                        exit={{ opacity: 0, scale: 0.8 }}
                        className={`absolute top-0 bottom-0 left-0 w-1/2 z-50 flex items-center justify-center text-3xl font-extrabold ${effChange > 0 ? 'text-green-400' : 'text-red-500'} drop-shadow-[0_2px_4px_rgba(0,0,0,1)] pointer-events-none`}
                    >
                        {effChange > 0 ? '+' : ''}{effChange} PE
                    </motion.div>
                )}
                {availChange !== null && (
                    <motion.div
                        key="avail"
                        initial={{ opacity: 0, scale: 0.5, x: 20 }}
                        animate={{ opacity: 1, scale: 1.2, x: 0 }}
                        exit={{ opacity: 0, scale: 0.8 }}
                        className={`absolute top-0 bottom-0 right-0 w-1/2 z-50 flex items-center justify-center text-3xl font-extrabold ${availChange > 0 ? 'text-green-400' : 'text-red-500'} drop-shadow-[0_2px_4px_rgba(0,0,0,1)] pointer-events-none`}
                    >
                        {availChange > 0 ? '+' : ''}{availChange} PD
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    )
    // End CharacterStatusCard
}

function OldCodeRemoved() { }
