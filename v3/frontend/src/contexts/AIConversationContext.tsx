'use client'

import React, { createContext, useContext, useReducer, useCallback, ReactNode } from 'react'
import { v4 as uuidv4 } from 'uuid'
import { ChatMessage, ConversationAction, ConversationState, Persona } from '@/components/ai/types'
import { getPersona } from '@/components/ai/PersonaSystem'

// --- Initial State ---
const INITIAL_STATE: ConversationState = {
    isOpen: false,
    isMinimized: false,
    activePersonaId: null,
    messages: [],
    status: 'idle'
}

// --- Reducer ---
function conversationReducer(state: ConversationState, action: ConversationAction): ConversationState {
    switch (action.type) {
        case 'OPEN_CHAT':
            return {
                ...state,
                isOpen: true,
                isMinimized: false,
                activePersonaId: action.payload.personaId,
                messages: action.payload.initialMessage
                    ? [{
                        id: uuidv4(),
                        role: 'assistant',
                        content: action.payload.initialMessage,
                        timestamp: Date.now()
                    }]
                    : state.messages.length > 0 && state.activePersonaId === action.payload.personaId
                        ? state.messages // Keep history if re-opening same persona
                        : [] // Clear if new persona (or deciding logic could vary)
            }
        case 'CLOSE_CHAT':
            return { ...state, isOpen: false }
        case 'MINIMIZE_CHAT':
            return { ...state, isMinimized: true }
        case 'MAXIMIZE_CHAT':
            return { ...state, isMinimized: false }
        case 'ADD_MESSAGE':
            return { ...state, messages: [...state.messages, action.payload] }
        case 'SET_STATUS':
            return { ...state, status: action.payload }
        case 'CLEAR_MESSAGES':
            return { ...state, messages: [] }
        default:
            return state
    }
}

// --- Context ---
interface AIConversationContextType {
    state: ConversationState
    startConversation: (personaId: string, initialMessage?: string) => void
    sendMessage: (content: string) => Promise<void>
    closeConversation: () => void
    minimizeConversation: () => void
    maximizeConversation: () => void
    activePersona: Persona | null
}

const AIConversationContext = createContext<AIConversationContextType | undefined>(undefined)

export function AIConversationProvider({ children }: { children: ReactNode }) {
    const [state, dispatch] = useReducer(conversationReducer, INITIAL_STATE)

    const activePersona = state.activePersonaId ? getPersona(state.activePersonaId) : null

    // --- Actions ---
    const startConversation = useCallback((personaId: string, initialMessage?: string) => {
        dispatch({ type: 'OPEN_CHAT', payload: { personaId, initialMessage } })
    }, [])

    const closeConversation = useCallback(() => {
        dispatch({ type: 'CLOSE_CHAT' })
    }, [])

    const minimizeConversation = useCallback(() => {
        dispatch({ type: 'MINIMIZE_CHAT' })
    }, [])

    const maximizeConversation = useCallback(() => {
        dispatch({ type: 'MAXIMIZE_CHAT' })
    }, [])

    // --- Mock Intelligence for now ---
    const sendMessage = useCallback(async (content: string) => {
        // 1. Add User Message
        const userMsg: ChatMessage = {
            id: uuidv4(),
            role: 'user',
            content,
            timestamp: Date.now()
        }
        dispatch({ type: 'ADD_MESSAGE', payload: userMsg })
        dispatch({ type: 'SET_STATUS', payload: 'thinking' })

        // 2. Simulate Delay for "AI Thinking"
        setTimeout(() => {
            dispatch({ type: 'SET_STATUS', payload: 'typing' })

            setTimeout(() => {
                // 3. Add Assistant Response (Mock)
                const responseMsg: ChatMessage = {
                    id: uuidv4(),
                    role: 'assistant',
                    content: `[MOCK RESPONSE from ${activePersona?.name || 'AI'}]\nI received your message: "${content}". \n\nI am currently a simulated intelligence. Connect me to an LLM API to get real responses!`,
                    timestamp: Date.now()
                }
                dispatch({ type: 'ADD_MESSAGE', payload: responseMsg })
                dispatch({ type: 'SET_STATUS', payload: 'idle' })
            }, 1500) // Typing delay

        }, 1000) // Thinking delay
    }, [activePersona])

    return (
        <AIConversationContext.Provider value={{
            state,
            startConversation,
            sendMessage,
            closeConversation,
            minimizeConversation,
            maximizeConversation,
            activePersona
        }}>
            {children}
        </AIConversationContext.Provider>
    )
}

export function useAIConversation() {
    const context = useContext(AIConversationContext)
    if (context === undefined) {
        throw new Error('useAIConversation must be used within an AIConversationProvider')
    }
    return context
}
