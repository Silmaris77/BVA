import { ConsultingGameState } from './types';

export interface GameEvent {
    id: string;
    title: string;
    description: string;
    type: 'positive' | 'negative' | 'neutral';
    effect: {
        resource?: string;
        multiplier?: number;
    };
    duration_minutes: number;
    timestamp: string;
}

export const POSSIBLE_EVENTS: GameEvent[] = [
    { id: 'market_crash', title: 'Market Crash: Tech', description: 'Tech contracts pay -20% for 4 hours.', type: 'negative', effect: { resource: 'tech_payout', multiplier: 0.8 }, duration_minutes: 240, timestamp: '' },
    { id: 'viral_post', title: 'Viral LinkedIn Post', description: 'Reputation gain +50% for 2 hours.', type: 'positive', effect: { resource: 'reputation', multiplier: 1.5 }, duration_minutes: 120, timestamp: '' },
];

export function checkForRandomEvent(state: ConsultingGameState): GameEvent | null {
    // 5% chance every time this is checked (usually once per session/hour)
    if (Math.random() < 0.05) {
        const event = POSSIBLE_EVENTS[Math.floor(Math.random() * POSSIBLE_EVENTS.length)];
        return {
            ...event,
            timestamp: new Date().toISOString()
        };
    }
    return null;
}
