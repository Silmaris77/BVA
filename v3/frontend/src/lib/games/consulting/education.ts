import { Contract } from './types';

// This would ideally be fetched from the DB or a shared config
// For now, hardcoded mapping
export const LESSON_CONTRACT_MAP: Record<string, Contract> = {
    'lesson_ojt_1': {
        id: 'contract_ojt_basic',
        is_global: false,
        title: 'Wdrożenie OJT w Fabryce',
        description: 'Klient potrzebuje planu szkolenia stanowiskowego dla nowych operatorów.',
        difficulty: 'Easy',
        topic: 'HR',
        requirements: { required_skills: ['ojt'] },
        reward: { coins: 500, reputation: 2 }
    },
    'lesson_swot_1': {
        id: 'contract_swot_startup',
        is_global: false,
        title: 'Analiza Strategiczna Startup-u',
        description: 'Software House potrzebuje analizy SWOT przed wejściem inwestora.',
        difficulty: 'Medium',
        topic: 'Strategy',
        requirements: { required_skills: ['analysis'] },
        reward: { coins: 1200, reputation: 5 }
    },
    'lesson_negocjacje_1': {
        id: 'contract_mediacje_it',
        is_global: false,
        title: 'Mediacje w Zespole IT',
        description: 'Konflikt między Seniorami a Juniorami. Rozwiąż to.',
        difficulty: 'Hard',
        topic: 'HR',
        requirements: { required_skills: ['negotiation'] },
        reward: { coins: 2500, reputation: 10 }
    }
};

export function getUnlockedContracts(completedLessonIds: string[]): Contract[] {
    const contracts: Contract[] = [];

    completedLessonIds.forEach(lessonId => {
        if (LESSON_CONTRACT_MAP[lessonId]) {
            contracts.push(LESSON_CONTRACT_MAP[lessonId]);
        }
    });

    return contracts;
}
