export interface NegotiationSession {
    id: string;
    contract_id: string;
    client_name: string;
    client_personality: 'aggressive' | 'logical' | 'friendly';
    messages: ChatMessage[];
    status: 'active' | 'won' | 'lost';
    current_offer: number;
    patience: number; // 0-100
}

export interface ChatMessage {
    sender: 'user' | 'client' | 'system';
    text: string;
    timestamp: string;
}

/**
 * Starts a new negotiation session for a contract.
 * In a real app, this would call an LLM (OpenAI) to generate the persona.
 * reliable mock for MVP.
 */
export async function startNegotiation(contractId: string): Promise<NegotiationSession> {
    return {
        id: crypto.randomUUID(),
        contract_id: contractId,
        client_name: 'John Arasaka',
        client_personality: 'aggressive',
        messages: [
            { sender: 'client', text: 'Stawka jest za wysoka. Mamy tańsze oferty. Dlaczego Ty?', timestamp: new Date().toISOString() }
        ],
        status: 'active',
        current_offer: 1000,
        patience: 100
    };
}

export function handleUserMessage(session: NegotiationSession, message: string): NegotiationSession {
    // Mock AI Logic
    const newMessages = [...session.messages, { sender: 'user', text: message, timestamp: new Date().toISOString() } as ChatMessage];

    // Simple Keyword matching for MVP
    let responseText = "Rozumiem, ale budżet jest sztywny.";
    let newPatience = session.patience - 10;

    if (message.toLowerCase().includes('doświadczenie') || message.toLowerCase().includes('portfolio')) {
        responseText = "Hmm, to faktycznie zmienia postać rzeczy. Możemy rozważyć mały bonus.";
        newPatience += 5;
    }

    newMessages.push({ sender: 'client', text: responseText, timestamp: new Date().toISOString() });

    return {
        ...session,
        messages: newMessages,
        patience: newPatience
    };
}
