'use client'

import React from 'react'
import { CardType } from '@/components/lesson/CardRenderer'

interface CardListSidebarProps {
    cards: { id: number; title?: string; type: CardType }[]
    selectedId: number
    onSelect: (id: number) => void
    onAdd: (type: CardType) => void
    onDelete: (id: number) => void
}

const CARD_TYPES: CardType[] = [
    'hero', 'content', 'story', 'quiz', 'flashcards', 'habit', 'ending'
]

export default function CardListSidebar({ cards, selectedId, onSelect, onAdd, onDelete }: CardListSidebarProps) {
    return (
        <div className="flex flex-col h-full">
            {/* List */}
            <div className="flex-1 overflow-y-auto p-2 space-y-2">
                {cards.map((card, index) => (
                    <div
                        key={card.id}
                        onClick={() => onSelect(card.id)}
                        className={`
                            group flex items-center justify-between p-3 rounded-lg cursor-pointer transition-all
                            ${card.id === selectedId
                                ? 'bg-[#00ff88]/10 border border-[#00ff88]/30 text-white'
                                : 'hover:bg-white/5 text-gray-400 hover:text-white border border-transparent'}
                        `}
                    >
                        <div className="flex items-center gap-3 overflow-hidden">
                            <span className="text-xs font-mono opacity-50 w-4">{index + 1}</span>
                            <div className="flex flex-col truncate">
                                <span className="text-sm font-medium truncate">{card.title}</span>
                                <span className="text-[10px] uppercase opacity-60">{card.type}</span>
                            </div>
                        </div>
                        {cards.length > 1 && (
                            <button
                                onClick={(e) => { e.stopPropagation(); onDelete(card.id); }}
                                className="opacity-0 group-hover:opacity-100 p-1 hover:text-red-400 transition-opacity"
                            >
                                ×
                            </button>
                        )}
                    </div>
                ))}
            </div>

            {/* Add Button */}
            <div className="p-4 border-t border-white/10 bg-[#0a0a0f]">
                <div className="grid grid-cols-2 gap-2">
                    {CARD_TYPES.map(type => (
                        <button
                            key={type}
                            onClick={() => onAdd(type)}
                            className="px-3 py-2 text-xs bg-white/5 hover:bg-white/10 border border-white/10 rounded text-gray-300 hover:text-white transition-colors"
                        >
                            + {type}
                        </button>
                    ))}
                    <button
                        onClick={() => onAdd('data')} // Extra one
                        className="col-span-2 px-3 py-2 text-xs bg-[#00ff88]/10 hover:bg-[#00ff88]/20 border border-[#00ff88]/30 rounded text-[#00ff88] font-medium transition-colors"
                    >
                        + Add Custom
                    </button>
                </div>
            </div>
        </div>
    )
}
