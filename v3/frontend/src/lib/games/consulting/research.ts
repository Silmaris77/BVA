import { ConsultingGameState } from './types';

export const RESEARCH_PROJECTS = {
    'swot_2': { id: 'swot_2', name: 'Framework SWOT 2.0', cost: 500, duration_minutes: 60, effect_description: '+10% Strategy Contract Pay' },
    'agile_hr': { id: 'agile_hr', name: 'Agile HR Methodology', cost: 800, duration_minutes: 120, effect_description: '-20% Employee Burnout' },
};

export function startResearch(state: ConsultingGameState, projectId: string): ConsultingGameState {
    if (state.research.active_project_id) {
        throw new Error("Research already in progress");
    }

    // Deduct cost
    const project = RESEARCH_PROJECTS[projectId as keyof typeof RESEARCH_PROJECTS];
    if (!project) throw new Error("Invalid project ID");

    if (state.resources.coins < project.cost) {
        throw new Error("Insufficient funds");
    }

    return {
        ...state,
        resources: {
            ...state.resources,
            coins: state.resources.coins - project.cost
        },
        research: {
            ...state.research,
            active_project_id: projectId
        }
    };
}
