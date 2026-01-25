'use client'

import React from 'react'
import { LessonCard } from '@/app/admin/lessons/create/page'

interface CardFormProps {
    card: LessonCard
    onChange: (card: LessonCard) => void
}

export default function CardForm({ card, onChange }: CardFormProps) {

    const handleChange = (field: string, value: any) => {
        onChange({ ...card, [field]: value })
    }

    const renderCommonFields = () => (
        <div className="space-y-4 mb-8 pb-8 border-b border-white/10">
            <div>
                <label className="block text-xs uppercase text-gray-500 mb-1">Title</label>
                <input
                    type="text"
                    value={card.title || ''}
                    onChange={e => handleChange('title', e.target.value)}
                    className="w-full bg-[#1a1a24] border border-white/10 rounded p-3 text-white focus:border-[#00ff88] focus:outline-none"
                />
            </div>
            {card.type !== 'hero' && (
                <div>
                    <label className="block text-xs uppercase text-gray-500 mb-1">Subtitle / Context</label>
                    <input
                        type="text"
                        value={card.subtitle || ''}
                        onChange={e => handleChange('subtitle', e.target.value)}
                        className="w-full bg-[#1a1a24] border border-white/10 rounded p-3 text-white focus:border-[#00ff88] focus:outline-none"
                    />
                </div>
            )}
        </div>
    )

    const renderTypeSpecificFields = () => {
        switch (card.type) {
            case 'hero':
                return (
                    <div className="space-y-4">
                        <div>
                            <label className="block text-xs uppercase text-gray-500 mb-1">Content (Description)</label>
                            <textarea
                                value={card.content || ''}
                                onChange={e => handleChange('content', e.target.value)}
                                className="w-full bg-[#1a1a24] border border-white/10 rounded p-3 text-white min-h-[100px]"
                            />
                        </div>
                        <div>
                            <label className="block text-xs uppercase text-gray-500 mb-1">Icon (Emoji)</label>
                            <input
                                type="text"
                                value={card.icon || ''}
                                onChange={e => handleChange('icon', e.target.value)}
                                className="w-full bg-[#1a1a24] border border-white/10 rounded p-3 text-white"
                            />
                        </div>
                        <div className="p-4 bg-yellow-500/10 border border-yellow-500/20 rounded text-yellow-200 text-sm">
                            ⚠️ Full Hero editing (sections, metadata) requires JSON mode for now.
                        </div>
                    </div>
                )
            case 'content':
                return (
                    <div className="space-y-4">
                        <div>
                            <label className="block text-xs uppercase text-gray-500 mb-1">Markdown Content</label>
                            <textarea
                                value={card.content || ''}
                                onChange={e => handleChange('content', e.target.value)}
                                className="w-full bg-[#1a1a24] border border-white/10 rounded p-3 text-white min-h-[300px] font-mono text-sm"
                            />
                        </div>
                    </div>
                )
            case 'story':
                return (
                    <div className="space-y-6">
                        <div className="p-4 bg-[#1a1a24] rounded border border-white/10">
                            <h4 className="text-[#00ff88] font-bold mb-4 uppercase text-xs">Scenario</h4>
                            <input
                                placeholder="Heading (e.g. The Situation)"
                                value={typeof card.scenario === 'object' && card.scenario?.heading ? card.scenario.heading : ''}
                                onChange={e => handleChange('scenario', { ...(typeof card.scenario === 'object' ? card.scenario : {}), heading: e.target.value })}
                                className="w-full bg-black/20 border border-white/10 rounded p-2 text-white mb-2"
                            />
                            <textarea
                                placeholder="Scenario text..."
                                value={typeof card.scenario === 'object' && card.scenario?.text ? card.scenario.text : ''}
                                onChange={e => handleChange('scenario', { ...(typeof card.scenario === 'object' ? card.scenario : {}), text: e.target.value })}
                                className="w-full bg-black/20 border border-white/10 rounded p-2 text-white min-h-[100px]"
                            />
                        </div>

                        <div className="p-4 bg-[#1a1a24] rounded border border-white/10">
                            <h4 className="text-[#00ff88] font-bold mb-4 uppercase text-xs">Lesson / Conclusion</h4>
                            <input
                                placeholder="Heading (e.g. The Key Takeaway)"
                                value={card.lesson?.heading || ''}
                                onChange={e => handleChange('lesson', { ...card.lesson, heading: e.target.value })}
                                className="w-full bg-black/20 border border-white/10 rounded p-2 text-white mb-2"
                            />
                            <textarea
                                placeholder="Lesson text..."
                                value={card.lesson?.text || ''}
                                onChange={e => handleChange('lesson', { ...card.lesson, text: e.target.value })}
                                className="w-full bg-black/20 border border-white/10 rounded p-2 text-white min-h-[100px]"
                            />
                        </div>
                    </div>
                )
            case 'flashcards':
                return (
                    <div className="space-y-6">
                        <div className="flex justify-between items-center mb-4">
                            <label className="text-xs uppercase text-gray-500">Flashcards List</label>
                            <button
                                onClick={() => {
                                    const newCards = [...(card.cards || []), { front: '', back: '' }]
                                    handleChange('cards', newCards)
                                }}
                                className="text-xs bg-[#00ff88]/10 text-[#00ff88] px-2 py-1 rounded hover:bg-[#00ff88]/20"
                            >
                                + Add Card
                            </button>
                        </div>

                        {(card.cards || []).map((flashcard, index) => (
                            <div key={index} className="p-4 bg-[#1a1a24] rounded border border-white/10 relative group">
                                <button
                                    onClick={() => {
                                        const currentCards = card.cards || []
                                        const newCards = currentCards.filter((_, i) => i !== index)
                                        handleChange('cards', newCards)
                                    }}
                                    className="absolute top-2 right-2 text-gray-600 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"
                                >
                                    Remove
                                </button>
                                <div className="grid grid-cols-1 gap-4">
                                    <div>
                                        <label className="block text-[10px] uppercase text-gray-500 mb-1">Front (Question)</label>
                                        <input
                                            value={flashcard.front || ''}
                                            onChange={e => {
                                                const newCards = [...(card.cards || [])]
                                                newCards[index].front = e.target.value
                                                handleChange('cards', newCards)
                                            }}
                                            className="w-full bg-black/20 border border-white/10 rounded p-2 text-white text-sm"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-[10px] uppercase text-gray-500 mb-1">Back (Answer)</label>
                                        <textarea
                                            value={flashcard.back || ''}
                                            onChange={e => {
                                                const newCards = [...(card.cards || [])]
                                                newCards[index].back = e.target.value
                                                handleChange('cards', newCards)
                                            }}
                                            className="w-full bg-black/20 border border-white/10 rounded p-2 text-white text-sm min-h-[60px]"
                                        />
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )
            default:
                return (
                    <div className="space-y-4">
                        <p className="text-gray-500 text-sm">Generic content field for type: {card.type}</p>
                        <textarea
                            value={JSON.stringify(card, null, 2)}
                            onChange={e => {
                                try {
                                    onChange(JSON.parse(e.target.value))
                                } catch (err) {
                                    // ignore parse errors while typing
                                }
                            }}
                            className="w-full bg-[#1a1a24] border border-white/10 rounded p-3 text-[#00ff88] min-h-[300px] font-mono text-sm"
                        />
                    </div>
                )
        }
    }

    return (
        <div className="max-w-2xl mx-auto">
            {renderCommonFields()}
            {renderTypeSpecificFields()}

            <div className="mt-8 pt-8 border-t border-white/10">
                <details>
                    <summary className="text-xs text-gray-500 cursor-pointer hover:text-white">Advanced: Edit Raw JSON</summary>
                    <textarea
                        value={JSON.stringify(card, null, 2)}
                        onChange={e => {
                            try {
                                onChange(JSON.parse(e.target.value))
                            } catch (err) { }
                        }}
                        className="w-full mt-4 bg-black/50 border border-white/10 rounded p-4 text-gray-400 font-mono text-xs min-h-[200px]"
                    />
                </details>
            </div>
        </div>
    )
}
