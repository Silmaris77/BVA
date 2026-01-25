'use client'

import React, { useState, useEffect } from 'react'
import LessonEditorLayout from '@/components/admin/lesson-editor/LessonEditorLayout'
import CardListSidebar from '@/components/admin/lesson-editor/CardListSidebar'
import CardForm from '@/components/admin/lesson-editor/CardForm'
import LivePreview from '@/components/admin/lesson-editor/LivePreview'
import { CardType, LessonCardData } from '@/components/lesson/CardRenderer'

// Temporary mock type until we import shared types
import SqlExportModal from '@/components/admin/lesson-editor/SqlExportModal'

export interface LessonCard extends LessonCardData {
    id: number
}

export default function LessonEditorPage() {
    const [cards, setCards] = useState<LessonCard[]>([
        { id: 1, type: 'hero', title: 'New Lesson', subtitle: 'Start here' }
    ])
    const [selectedCardId, setSelectedCardId] = useState<number>(1)
    const [showExport, setShowExport] = useState(false)

    const activeCard = cards.find(c => c.id === selectedCardId) || cards[0]

    const handleUpdateCard = (updatedCard: LessonCard) => {
        setCards(cards.map(c => c.id === updatedCard.id ? updatedCard : c))
    }

    const handleAddCard = (type: CardType) => {
        const newId = Math.max(...cards.map(c => c.id), 0) + 1
        const newCard: LessonCard = { id: newId, type, title: `New ${type}` }
        setCards([...cards, newCard])
        setSelectedCardId(newId)
    }

    const handleDeleteCard = (id: number) => {
        const newCards = cards.filter(c => c.id !== id)
        setCards(newCards)
        if (selectedCardId === id && newCards.length > 0) {
            setSelectedCardId(newCards[0].id)
        }
    }

    return (
        <LessonEditorLayout>
            {/* LEFT: Sidebar */}
            <div className="w-64 border-r border-white/10 flex flex-col bg-[#111118]">
                <div className="p-4 border-b border-white/10 font-bold text-[#00ff88] flex justify-between items-center">
                    <span>LESSON EDITOR</span>
                </div>
                <CardListSidebar
                    cards={cards}
                    selectedId={selectedCardId}
                    onSelect={setSelectedCardId}
                    onAdd={handleAddCard}
                    onDelete={handleDeleteCard}
                />
                {/* Export Button inside Sidebar Footer */}
                <div className="p-4 border-t border-white/10 bg-[#0a0a0f]">
                    <button
                        onClick={() => setShowExport(true)}
                        className="w-full py-2 bg-[#00ff88]/20 hover:bg-[#00ff88]/30 text-[#00ff88] border border-[#00ff88]/50 rounded font-bold uppercase text-xs tracking-wider transition-all"
                    >
                        ⚡ Export SQL
                    </button>
                </div>
            </div>

            {/* MIDDLE: Form */}
            <div className="flex-1 border-r border-white/10 bg-[#0a0a0f] flex flex-col h-full overflow-hidden">
                <div className="p-4 border-b border-white/10 flex justify-between items-center bg-[#111118]">
                    <span className="font-bold text-gray-400">EDIT CARD</span>
                    <span className="text-xs px-2 py-1 bg-white/10 rounded">{activeCard?.type}</span>
                </div>
                <div className="flex-1 overflow-y-auto p-6">
                    {activeCard && (
                        <CardForm
                            card={activeCard}
                            onChange={handleUpdateCard}
                        />
                    )}
                </div>
            </div>

            {/* RIGHT: Preview */}
            <div className="w-[500px] bg-[#1a1a24] flex flex-col border-l border-white/10">
                <div className="p-4 border-b border-white/10 font-bold text-gray-400 flex justify-between">
                    <span>LIVE PREVIEW</span>
                    <button className="text-[#00ff88] text-xs hover:underline">
                        Switch View
                    </button>
                </div>
                <div className="flex-1 overflow-y-auto p-8 relative">
                    <LivePreview card={activeCard} />
                </div>
            </div>

            {showExport && (
                <SqlExportModal
                    cards={cards}
                    onClose={() => setShowExport(false)}
                />
            )}
        </LessonEditorLayout>
    )
}
