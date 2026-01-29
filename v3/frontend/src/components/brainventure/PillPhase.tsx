"use client"

import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useBrainVenture } from './BrainVentureContext'
import PILLS_DATA from '@/data/brainventure/pills.json'
import { KnowledgePill } from '@/types/brainventure'
import { Clock, BookOpen, CheckCircle, XCircle } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

export default function PillPhase() {
    const { state, dispatch } = useBrainVenture()
    const [pill, setPill] = useState<KnowledgePill | null>(null)
    const [timeLeft, setTimeLeft] = useState(120) // 2 minutes
    const [isActive, setIsActive] = useState(true)

    useEffect(() => {
        // Simple sequential or random pill logic. 
        // For MVP random, effectively infinite pool without history checking for now logic
        const randomPill = PILLS_DATA[Math.floor(Math.random() * PILLS_DATA.length)] as unknown as KnowledgePill
        setPill(randomPill)
    }, [])

    useEffect(() => {
        if (!isActive || timeLeft <= 0) return
        const timer = setInterval(() => {
            setTimeLeft(prev => prev - 1)
        }, 1000)
        return () => clearInterval(timer)
    }, [isActive, timeLeft])

    const handleReturn = () => {
        dispatch({ type: 'SET_PHASE_READY', payload: true })
    }

    const [showCostAnim, setShowCostAnim] = useState(false)

    // ... useEffects ...

    const handleBuy = () => {
        if (state.cash >= 100 && pill) {
            setShowCostAnim(true)
            dispatch({ type: 'UPDATE_CASH', payload: -100, silent: true })
            dispatch({ type: 'UNLOCK_PILL', payload: pill.id })

            setTimeout(() => {
                dispatch({ type: 'SET_PHASE_READY', payload: true })
            }, 1000)
        } else {
            alert('Nie masz wystarczająco środków!')
        }
    }

    if (!pill) return <div>Ładowanie wiedzy...</div>

    const minutes = Math.floor(timeLeft / 60)
    const seconds = timeLeft % 60

    return (
        <div className="h-full flex flex-col items-center max-w-5xl mx-auto w-full pt-4">
            {/* Header with Timer */}
            <div className="flex justify-between w-full items-center mb-6">
                <div>
                    <h2 className="text-3xl font-bold text-purple-400">Faza 2: Pigułka Wiedzy</h2>
                    <p className="text-gray-400">Masz 2 minuty na zapoznanie się z treścią.</p>
                </div>
                <div className={`flex items-center gap-2 text-2xl font-mono font-bold ${timeLeft < 20 ? 'text-red-500 animate-pulse' : 'text-blue-300'}`}>
                    <Clock /> {minutes}:{seconds.toString().padStart(2, '0')}
                </div>
            </div>

            {/* Pill Content */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-gray-800 border-2 border-purple-500/30 rounded-2xl p-8 w-full shadow-2xl flex-1 overflow-y-auto custom-scrollbar mb-6"
            >
                <div className="prose prose-invert max-w-none">
                    <h1 className="text-purple-300 mb-6 border-b border-purple-500/20 pb-4">{pill.title}</h1>
                    <ReactMarkdown>{pill.content}</ReactMarkdown>
                </div>
            </motion.div>

            {/* Action Bar */}
            <div className="grid grid-cols-2 gap-6 w-full max-w-3xl mb-4 relative">
                <button
                    onClick={handleReturn}
                    className="flex flex-col items-center justify-center p-6 rounded-xl border border-gray-600 bg-gray-800/50 hover:bg-gray-700 transition-colors group"
                >
                    <span className="text-gray-400 group-hover:text-white font-bold text-lg mb-1 flex items-center gap-2">
                        <XCircle size={20} /> Oddaj Pigułkę
                    </span>
                    <span className="text-sm text-gray-500">Zapamiętaj co możesz (Koszt: 0 zł)</span>
                </button>

                <div className="relative">
                    <button
                        onClick={handleBuy}
                        disabled={state.cash < 100 || showCostAnim}
                        className="w-full h-full flex flex-col items-center justify-center p-6 rounded-xl border border-purple-500 bg-purple-900/20 hover:bg-purple-900/40 transition-colors group disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <span className="text-purple-300 group-hover:text-purple-100 font-bold text-lg mb-1 flex items-center gap-2">
                            <CheckCircle size={20} /> Kup Wiedzę
                        </span>
                        <span className="text-sm text-purple-400/60">Zyskaj dostęp na stałe (Koszt: 100 zł)</span>
                    </button>

                    {/* Local Cost Animation */}
                    <AnimatePresence>
                        {showCostAnim && (
                            <motion.div
                                initial={{ opacity: 0, y: 0, scale: 0.5 }}
                                animate={{ opacity: 1, y: -50, scale: 1.2 }}
                                exit={{ opacity: 0 }}
                                className="absolute top-0 right-0 left-0 flex justify-center -mt-8 pointer-events-none"
                            >
                                <span className="text-4xl font-bold text-red-500 drop-shadow-md font-mono">💸 -100 PLN</span>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </div>
        </div>
    )
}
