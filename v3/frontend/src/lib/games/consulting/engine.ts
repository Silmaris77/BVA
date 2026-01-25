import { ConsultingGameState, DeptType, Employee, Contract } from './types';

export const INITIAL_STATE: ConsultingGameState = {
    user_id: '', // Set on creation
    resources: {
        coins: 20000, // Seed capital
        reputation: 1,
        cashflow: {
            revenue: 0,
            burn: 200, // Basic office upkeep
        }
    },
    departments: {
        office: { id: 'office', level: 1, stats: { capacity: 5 } },
        finance: { id: 'finance', level: 1, stats: { efficiency: 1.0 } },
        sales: { id: 'sales', level: 1, stats: { lead_gen: 0 } },
        hr: { id: 'hr', level: 1, stats: { max_employees: 2 } },
        research: { id: 'research', level: 1, stats: { speed: 1.0 } },
        marketing: { id: 'marketing', level: 1, stats: { brand: 1.0 } },
    },
    active_contracts: [],
    market_contracts: [],
    employees: [],
    active_events: [],
    research: {
        active_project_id: null,
        completed_projects: [],
    },
    last_updated: new Date().toISOString(),
};

/**
 * Calculates offline progress and updates the state.
 * Should be called every time the user loads the game or performs an action.
 */
export function reconcileState(state: ConsultingGameState): ConsultingGameState {
    const now = new Date();
    const lastUpdate = new Date(state.last_updated);
    const diffMinutes = (now.getTime() - lastUpdate.getTime()) / (1000 * 60);

    if (diffMinutes < 1) {
        // Less than a minute passed, no widespread updates needed
        // But update timestamp to keep it fresh
        return { ...state, last_updated: now.toISOString() };
    }

    // 1. Calculate Financials (Burn Rate)
    // Burn rate is "Daily", so we calculate fractional day
    const daysPassed = diffMinutes / (60 * 24);
    const burnCost = Math.floor(state.resources.cashflow.burn * daysPassed);

    let newCoins = state.resources.coins - burnCost;

    // 2. Process Contracts (If they are auto-generating contracts/passive income)
    // For now, contracts are manual work, but maybe some have "passive" components later.

    // 3. Process Research
    // Implementation of Research Timer Logic would go here

    return {
        ...state,
        resources: {
            ...state.resources,
            coins: newCoins,
        },
        last_updated: now.toISOString(),
    };
}

export function calculateBurnRate(state: ConsultingGameState): number {
    let burn = 0;

    // Base Office Upkeep
    const officeLevel = state.departments.office.level;
    burn += officeLevel * 200;

    // Salaries
    state.employees.forEach(emp => {
        burn += emp.salary;
    });

    return burn;
}

export function hireEmployee(state: ConsultingGameState, role: 'Junior' | 'Senior' | 'Expert', cost: number): ConsultingGameState {
    // 1. Check if can afford
    if (state.resources.coins < cost) {
        return state; // Fail silently or throw error? For now, just return state (UI should handle disabled state)
    }

    // 2. Check Capacity
    if (state.employees.length >= (state.departments.hr.stats.max_employees as number)) {
        return state;
    }

    // 3. Deduction
    const newState = { ...state };
    newState.resources.coins -= cost;

    // 4. Create Employee
    const newEmp: Employee = {
        id: `emp_${Date.now()}`,
        name: role === 'Junior' ? 'Młodszy Analityk' : 'Starszy Konsultant',
        role: role === 'Junior' ? 'Analityk' : 'Ekspert',
        specialty: 'Strategy',
        salary: role === 'Junior' ? 100 : 500,
        stats: {
            morale: 100,
            skill_level: role === 'Junior' ? 1 : 3,
            speed: role === 'Junior' ? 1 : 3,
            quality: role === 'Junior' ? 1 : 3,
            stamina: 100,
        }
    };

    newState.employees = [...newState.employees, newEmp];

    // Recalculate Burn
    newState.resources.cashflow.burn = calculateBurnRate(newState);

    return newState;
}

export function upgradeOffice(state: ConsultingGameState): ConsultingGameState {
    const currentLevel = state.departments.office.level;
    const upgradeCost = currentLevel === 1 ? 5000 : currentLevel === 2 ? 15000 : 999999;

    if (state.resources.coins < upgradeCost) {
        return state;
    }

    if (currentLevel >= 3) return state; // Max level

    const newState = { ...state };
    newState.resources.coins -= upgradeCost;
    newState.departments.office.level += 1;

    // Improve Stats
    if (newState.departments.office.level === 2) {
        newState.departments.office.stats.capacity = 12;
        newState.departments.hr.stats.max_employees = 12; // HR Limit tied to office space usually, simplifies here
    } else if (newState.departments.office.level === 3) {
        newState.departments.office.stats.capacity = 30;
        newState.departments.hr.stats.max_employees = 30;
    }

    // Recalculate Burn
    newState.resources.cashflow.burn = calculateBurnRate(newState);

    return newState;
}

export function generateContracts(state: ConsultingGameState): Contract[] {
    const reputation = state.resources.reputation;
    const newContracts: Contract[] = [];

    // 1. Generate 2-3 Simple Contracts (Instant Accept)
    for (let i = 0; i < 3; i++) {
        newContracts.push({
            id: `cnt_${Date.now()}_simple_${i}`,
            is_global: true,
            title: `Szybki Audyt: ${['Finanse', 'IT', 'Procesy'][Math.floor(Math.random() * 3)]}`,
            description: "Standardowa procedura audytowa. Wymagany krótki czas realizacji.",
            difficulty: 'Easy',
            topic: 'Operations',
            requirements: { min_reputation: 0 },
            reward: { coins: 1500 + Math.floor(Math.random() * 500), reputation: 5 },
            instant_accept: true,
            negotiation_required: false,
            expires_at: new Date(Date.now() + 1000 * 60 * 60 * 24).toISOString() // 24h
        });
    }

    // 2. Generate 1 High-Value Contract (Requires Negotiation) - IF reputation is high enough
    if (reputation >= 0) { // Changed threshold for testing
        newContracts.push({
            id: `cnt_${Date.now()}_complex_1`,
            is_global: true,
            title: "Restrukturyzacja Globalna",
            description: "Gruntowna przebudowa działu międzynarodowego. Wysoka stawka. (Wymaga negocjacji)",
            difficulty: 'Hard',
            topic: 'Strategy',
            requirements: { min_reputation: 5 },
            reward: { coins: 15000, reputation: 50 },
            instant_accept: false,
            negotiation_required: true,
            expires_at: new Date(Date.now() + 1000 * 60 * 60 * 48).toISOString() // 48h
        });
    }

    return newContracts;
}
