import { ConsultingGameState } from './types';

export interface MarketingCampaign {
    id: string;
    type: 'social' | 'webinar' | 'pr';
    cost: number;
    duration_minutes: number;
    lead_multiplier: number;
}

export const CAMPAIGNS: Record<string, MarketingCampaign> = {
    'social_basic': { id: 'social_basic', type: 'social', cost: 200, duration_minutes: 1440, lead_multiplier: 1.2 }, // 24h boost
    'webinar_pro': { id: 'webinar_pro', type: 'webinar', cost: 1000, duration_minutes: 60, lead_multiplier: 2.0 }, // Short heavy boost
};

export function calculateLeadMultiplier(state: ConsultingGameState): number {
    let multiplier = 1.0;
    const brandLevel = state.departments.marketing.level;

    multiplier += (brandLevel * 0.1); // Base multiplier from dept Level

    // Verify active campaigns (Todo: Add active_campaigns to state in types if not there)

    return multiplier;
}
