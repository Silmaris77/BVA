"use client"

import React, { useEffect, useState } from 'react'
import { useBrainVenture } from './BrainVentureContext'
import { motion } from 'framer-motion'
import { PlayCircle, AlertTriangle, CheckCircle, TrendingUp } from 'lucide-react'

export default function SummaryPhase() {
    const { state, dispatch, formatMoney } = useBrainVenture()
    const [summary, setSummary] = useState<{
        penalties: number,
        completed: number,
        failed: string[]
    } | null>(null)

    useEffect(() => {
        // Calculate End of Round Logic
        // 1. Check contracts deadlines
        // For MVP, we assumed simplistic deadline check.
        // Let's assume deadline logic was: duration is total rounds allowed.
        // We need to track rounds passed for active contracts.
        // Since we didn't fully implement 'rounds active' tracking in the reducer yet, 
        // we'll simulate a simple check or just skip precise penalties for MVP v1.

        // Let's pretend we calculated it:
        setSummary({
            penalties: 0,
            completed: 0,
            failed: []
        })

        // Enable Global Nav
        dispatch({ type: 'SET_PHASE_READY', payload: true })

    }, [])

    return (
        <div className="h-full flex flex-col items-center justify-center max-w-4xl mx-auto w-full text-center">
            <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="bg-gray-800 border-2 border-gray-600 rounded-2xl p-12 shadow-2xl"
            >
                <h2 className="text-4xl font-bold text-white mb-8">Podsumowanie Rundy {state.round}</h2>

                <div className="grid grid-cols-2 gap-8 mb-8 text-left">
                    <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-700">
                        <h3 className="text-gray-400 text-sm uppercase tracking-wider mb-2">Stan Finansów</h3>
                        <div className="text-3xl font-mono text-green-400 font-bold">{formatMoney(state.cash)}</div>
                    </div>
                    <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-700">
                        <h3 className="text-gray-400 text-sm uppercase tracking-wider mb-2">Rozwój (Efektywność)</h3>
                        <div className="text-3xl font-mono text-blue-400 font-bold flex items-center gap-2">
                            <TrendingUp size={28} />
                            {state.team.reduce((acc, c) => acc + c.efficiency, 0)} pkt
                        </div>
                    </div>
                </div>

                <div className="space-y-4 mb-10">
                    <div className="flex items-center gap-3 text-red-400 bg-red-900/20 p-4 rounded-lg border border-red-900/50">
                        <AlertTriangle />
                        <span>Kary za nieterminowe kontrakty: {formatMoney(summary?.penalties || 0)}</span>
                    </div>
                    {/* Add more summary stats here */}
                </div>
            </motion.div>
        </div>
    )
}
