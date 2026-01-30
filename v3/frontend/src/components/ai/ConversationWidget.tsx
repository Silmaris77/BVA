'use client'

import React, { useEffect, useRef, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, Minus, Send, Bot, UserMinus, Palette, User, MessageCircle } from 'lucide-react'
import { useAIConversation } from '@/contexts/AIConversationContext'
import { Persona } from '@/components/ai/types'
import MathRenderer from '@/components/lesson/math/MathRenderer'

// Map known icons
const IconMap: Record<string, any> = {
    'Bot': Bot,
    'UserMinus': UserMinus,
    'Palette': Palette
}

export default function AIConversationWidget() {
    const { state, activePersona, closeConversation, minimizeConversation, maximizeConversation, sendMessage } = useAIConversation()
    const [inputValue, setInputValue] = useState('')
    const messagesEndRef = useRef<HTMLDivElement>(null)

    // Auto-scroll logic
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [state.messages, state.status, state.isOpen])

    if (!state.isOpen) return null

    const PersonaIcon = activePersona && IconMap[activePersona.avatar] ? IconMap[activePersona.avatar] : Bot

    // Minimized View (Bubble)
    if (state.isMinimized) {
        return (
            <motion.div
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0, opacity: 0 }}
                onClick={maximizeConversation}
                className="fixed bottom-6 right-6 z-[9999] cursor-pointer"
            >
                <div
                    className="w-16 h-16 rounded-full shadow-2xl flex items-center justify-center border-2 border-white/20 backdrop-blur-md transition-transform hover:scale-110"
                    style={{ background: activePersona?.color || '#00d4ff' }}
                >
                    <PersonaIcon size={32} color="white" />
                    {/* Badge if active/thinking */}
                    {state.status !== 'idle' && (
                        <div className="absolute top-0 right-0 w-4 h-4 bg-white rounded-full animate-bounce" />
                    )}
                </div>
            </motion.div>
        )
    }

    // Full Chat View
    return (
        <AnimatePresence>
            <motion.div
                initial={{ y: 100, opacity: 0, scale: 0.9 }}
                animate={{ y: 0, opacity: 1, scale: 1 }}
                exit={{ y: 50, opacity: 0, scale: 0.9 }}
                transition={{ type: "spring", stiffness: 300, damping: 30 }}
                className="fixed bottom-6 right-6 z-[9999] w-[400px] h-[600px] max-h-[80vh] flex flex-col rounded-2xl overflow-hidden shadow-2xl border border-white/10 backdrop-blur-md"
                style={{ background: 'rgba(15, 23, 42, 0.95)' }} // Deep slate background
            >
                {/* HEADERA */}
                <div
                    className="h-16 flex items-center justify-between px-4"
                    style={{ background: activePersona?.color ? `linear-gradient(90deg, ${activePersona.color}dd, ${activePersona.color}aa)` : '#334155' }}
                >
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center backdrop-blur-sm">
                            <PersonaIcon size={24} color="white" />
                        </div>
                        <div>
                            <h3 className="font-bold text-white text-lg leading-tight">{activePersona?.name || 'AI Assistant'}</h3>
                            <p className="text-white/80 text-xs font-medium uppercase tracking-wide">{activePersona?.role || 'Virtual Guide'}</p>
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
                        <button
                            onClick={minimizeConversation}
                            className="p-1.5 rounded-full hover:bg-white/20 text-white transition-colors"
                        >
                            <Minus size={18} />
                        </button>
                        <button
                            onClick={closeConversation}
                            className="p-1.5 rounded-full hover:bg-white/20 text-white transition-colors"
                        >
                            <X size={18} />
                        </button>
                    </div>
                </div>

                {/* MESSAGES AREA */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar bg-black/20">
                    {state.messages.map((msg) => {
                        const isUser = msg.role === 'user'
                        return (
                            <div
                                key={msg.id}
                                className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
                            >
                                <div
                                    className={`max-w-[85%] p-3 rounded-2xl text-sm leading-relaxed shadow-sm ${isUser
                                        ? 'bg-blue-600 text-white rounded-br-none'
                                        : 'bg-white/10 text-gray-100 rounded-bl-none border border-white/5'
                                        }`}
                                >
                                    <MathRenderer content={msg.content} />
                                    <div className={`text-[10px] mt-1 opacity-50 ${isUser ? 'text-right' : 'text-left'}`}>
                                        {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    </div>
                                </div>
                            </div>
                        )
                    })}

                    {/* Status Indicators */}
                    {state.status === 'thinking' && (
                        <div className="flex justify-start">
                            <div className="bg-white/5 text-gray-400 text-xs p-2 rounded-lg italic flex items-center gap-2 animate-pulse">
                                <BrainIconSpin /> Thinking...
                            </div>
                        </div>
                    )}
                    {state.status === 'typing' && (
                        <div className="flex justify-start">
                            <div className="bg-white/10 p-3 rounded-2xl rounded-bl-none flex gap-1 items-center h-10">
                                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-75" />
                                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150" />
                                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-300" />
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* INPUT AREA */}
                <div className="p-4 bg-slate-900 border-t border-white/5">
                    <form
                        onSubmit={(e) => {
                            e.preventDefault()
                            if (inputValue.trim()) {
                                sendMessage(inputValue.trim())
                                setInputValue('')
                            }
                        }}
                        className="flex gap-2"
                    >
                        <div className="flex-1 relative">
                            <input
                                type="text"
                                value={inputValue}
                                onChange={(e) => setInputValue(e.target.value)}
                                placeholder={`Message ${activePersona?.name || 'AI'}...`}
                                className="w-full bg-slate-800 text-white placeholder-slate-400 text-sm rounded-xl pl-4 pr-10 py-3 border border-slate-700 focus:border-blue-500 focus:bg-slate-750 focus:outline-none transition-colors"
                            />
                            <MicButton
                                onResult={(text) => setInputValue(prev => prev + (prev ? ' ' : '') + text)}
                            />
                        </div>
                        <button
                            type="submit"
                            disabled={!inputValue.trim() || state.status !== 'idle'}
                            className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white p-3 rounded-xl transition-all shadow-lg shadow-blue-900/20 active:scale-95 flex items-center justify-center"
                        >
                            <Send size={18} />
                        </button>
                    </form>
                </div>
            </motion.div>
        </AnimatePresence>
    )
}

import { Mic, Loader2 } from 'lucide-react'
import { useSpeechRecognition } from '@/hooks/useSpeechRecognition'

function MicButton({ onResult }: { onResult: (text: string) => void }) {
    const { isListening, toggleListening, error } = useSpeechRecognition({ onResult })

    return (
        <button
            type="button"
            onClick={toggleListening}
            className={`absolute right-2 top-1/2 -translate-y-1/2 p-1.5 rounded-lg transition-all ${isListening
                ? 'text-red-500 hover:bg-red-500/10 animate-pulse'
                : 'text-slate-400 hover:text-white hover:bg-white/10'
                }`}
            title={error || (isListening ? 'Stop recording' : 'Start recording')}
        >
            {isListening ? (
                <div className="w-4 h-4 rounded-full bg-current animate-pulse" />
            ) : (
                <Mic size={18} />
            )}
        </button>
    )
}

function BrainIconSpin() {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="animate-spin">
            <path d="M12 2a10 10 0 1 0 10 10 4 4 0 0 1-5-5 4 4 0 0 1-5-5c0-5.523 4.477-10 10-10Z" />
        </svg>
    )
}
