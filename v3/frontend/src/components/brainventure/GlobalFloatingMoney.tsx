"use client"

import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useBrainVenture } from './BrainVentureContext'

interface FloatingItem {
    id: number
    amount: number
}

export default function GlobalFloatingMoney() {
    const { state } = useBrainVenture()
    const [items, setItems] = useState<FloatingItem[]>([])

    // Listen for global transactions
    useEffect(() => {
        if (state.lastCashTransaction) {
            const newItem = state.lastCashTransaction
            setItems(prev => [...prev, newItem])
        }
    }, [state.lastCashTransaction])

    const remove = (id: number) => {
        setItems(prev => prev.filter(i => i.id !== id))
    }

    return (
        <div className="fixed inset-0 pointer-events-none z-[100] overflow-hidden">
            <AnimatePresence>
                {items.map(item => (
                    <FloatingMoney key={item.id} item={item} onComplete={() => remove(item.id)} />
                ))}
            </AnimatePresence>
        </div>
    )
}

function FloatingMoney({ item, onComplete }: { item: FloatingItem, onComplete: () => void }) {
    const isIncome = item.amount >= 0
    const text = isIncome ? `+${item.amount} PLN` : `${item.amount} PLN`
    const colorClass = isIncome ? 'text-green-400' : 'text-red-500'
    const emoji = isIncome ? '💰' : '💸'

    // Randomize start position slightly to avoid stacking perfectly if multiple trigger at once
    const randomX = Math.random() * 20 - 10 // -10% to +10%

    return (
        <motion.div
            initial={{ opacity: 0, y: '50%', x: '-50%', scale: 0.5 }}
            animate={{ opacity: 1, y: '30%', scale: isIncome ? 1.5 : 1.2 }}
            exit={{ opacity: 0, y: '10%' }}
            transition={{ duration: 2, ease: "easeOut" }}
            onAnimationComplete={onComplete}
            style={{ left: `calc(50% + ${randomX}px)` }}
            className={`fixed top-1/2 transform -translate-x-1/2 -translate-y-1/2 
                       text-5xl font-bold ${colorClass} drop-shadow-[0_2px_4px_rgba(0,0,0,0.8)] 
                       font-mono flex items-center gap-2`}
        >
            <span>{emoji}</span> {text}
        </motion.div>
    )
}
