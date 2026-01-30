
export type PersonaRole = 'mentor' | 'client' | 'team_member' | 'adversary' | 'system'

export interface Persona {
    id: string
    name: string
    role: string // Display role, e.g. "Senior Consultant"
    avatar: string // URL or Lucide Icon Name
    color: string // Theme color for the persona
    tone: 'formal' | 'casual' | 'warm' | 'aggressive' | 'analytical'
    systemPrompt: string
}

export interface ChatMessage {
    id: string
    role: 'user' | 'assistant' | 'system'
    content: string
    timestamp: number
    isLoading?: boolean
}

export interface ConversationState {
    isOpen: boolean
    isMinimized: boolean
    activePersonaId: string | null
    messages: ChatMessage[]
    status: 'idle' | 'thinking' | 'typing' | 'speaking'
}

export type ConversationAction =
    | { type: 'OPEN_CHAT'; payload: { personaId: string; initialMessage?: string } }
    | { type: 'CLOSE_CHAT' }
    | { type: 'MINIMIZE_CHAT' }
    | { type: 'MAXIMIZE_CHAT' }
    | { type: 'ADD_MESSAGE'; payload: ChatMessage }
    | { type: 'SET_STATUS'; payload: ConversationState['status'] }
    | { type: 'CLEAR_MESSAGES' }
