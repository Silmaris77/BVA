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

        // If there's an internal monologue or initial greeting needed from AI, we could trigger it here.
        // For now, if we start with a user message (e.g. from a trigger), we handle it.
        // But usually startConversation just opens the window.
    }, [])

    const closeConversation = useCallback(() => dispatch({ type: 'CLOSE_CHAT' }), [])

    const minimizeConversation = useCallback(() => dispatch({ type: 'MINIMIZE_CHAT' }), [])
    const maximizeConversation = useCallback(() => dispatch({ type: 'MAXIMIZE_CHAT' }), [])

    const sendMessage = useCallback(async (content: string) => {
        if (!state.activePersonaId || !activePersona) return

        const userMsgId = uuidv4()
        const userMessage: ChatMessage = {
            id: userMsgId,
            role: 'user',
            content,
            timestamp: Date.now()
        }

        dispatch({ type: 'ADD_MESSAGE', payload: userMessage })
        dispatch({ type: 'SET_STATUS', payload: 'thinking' })

        try {
            // Prepare messages context including the new user message
            const conversationHistory = [...state.messages, userMessage];

            const response = await fetch('/api/ai/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    messages: conversationHistory,
                    systemPrompt: activePersona.systemPrompt
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to fetch AI response');
            }

            const data = await response.json();

            const aiMsgId = uuidv4()
            const aiMessage: ChatMessage = {
                id: aiMsgId,
                role: 'assistant',
                content: data.response,
                timestamp: Date.now()
            }

            dispatch({ type: 'ADD_MESSAGE', payload: aiMessage })
            dispatch({ type: 'SET_STATUS', payload: 'idle' })

        } catch (error) {
            console.error("Chat Error:", error);
            // Optional: Add an error message to the chat
            const errorMsgId = uuidv4()
            dispatch({
                type: 'ADD_MESSAGE', payload: {
                    id: errorMsgId,
                    role: 'assistant', // Or a system role if we had one
                    content: "Przepraszam, napotkałem problem z połączeniem. Spróbuj ponownie później.",
                    timestamp: Date.now()
                }
            })
            dispatch({ type: 'SET_STATUS', payload: 'error' })
        }
    }, [state.activePersonaId, state.messages, activePersona])

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
