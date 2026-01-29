"use client"

import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useBrainVenture } from './BrainVentureContext'
import { Gem } from 'lucide-react'

interface FloatingItem {
    id: number
    amount: number
}

export default function GlobalFloatingKW() {
    const { state } = useBrainVenture()
    const [items, setItems] = useState<FloatingItem[]>([])
    const lastProcessedId = React.useRef<number | null>(null)

    // Listen for global transactions
    useEffect(() => {
        if (state.lastKWTransaction) {
            // Check if transaction is recent (within 2s) to avoid replaying old state on remount
            const isFresh = (Date.now() - Math.floor(state.lastKWTransaction.id)) < 2000;

            if (lastProcessedId.current === state.lastKWTransaction.id || !isFresh) return

            lastProcessedId.current = state.lastKWTransaction.id
            const newItem = state.lastKWTransaction
            setItems(prev => [...prev, newItem])
        }
    }, [state.lastKWTransaction])

    const remove = React.useCallback((id: number) => {
        setItems(prev => prev.filter(i => i.id !== id))
    }, [])

    return (
        <div className="fixed inset-0 pointer-events-none z-[100] overflow-hidden">
            <AnimatePresence>
                {items.map(item => (
                    <FloatingKW key={item.id} item={item} onRemove={remove} />
                ))}
            </AnimatePresence>
        </div>
    )
}

function FloatingKW({ item, onRemove }: { item: FloatingItem, onRemove: (id: number) => void }) {
    const isIncome = item.amount >= 0
    const text = isIncome ? `+${item.amount} KW` : `${item.amount} KW`
    const colorClass = isIncome ? 'text-blue-400' : 'text-purple-400'

    const startX = '65%'
    const startY = '10%'

    // Stable callback for completion
    const handleComplete = React.useCallback(() => {
        onRemove(item.id)
    }, [item.id, onRemove])

    // Fallback: Force remove after 3s in case animation callback hangs
    useEffect(() => {
        const timer = setTimeout(handleComplete, 3000)
        return () => clearTimeout(timer)
    }, [handleComplete])

    return (
        <motion.div
            initial={{ opacity: 0, y: 50, x: '-50%', scale: 0.5, left: startX, top: startY }}
            animate={{ opacity: 1, y: -20, scale: 1.5 }}
            exit={{ opacity: 0, y: -50 }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            onAnimationComplete={handleComplete}
            className={`fixed transform -translate-x-1/2 
                       text-4xl font-bold ${colorClass} drop-shadow-[0_2px_4px_rgba(0,0,0,0.8)] 
                       font-mono flex items-center gap-2`}
        >
            <Gem size={32} /> {text}
        </motion.div>
    )
}
