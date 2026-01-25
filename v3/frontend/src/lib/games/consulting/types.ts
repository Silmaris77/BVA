export type DeptType = 'office' | 'finance' | 'sales' | 'hr' | 'research' | 'marketing';
export type ContractDifficulty = 'Easy' | 'Medium' | 'Hard' | 'Expert';
export type ContractTopic = 'Strategy' | 'IT' | 'Finance' | 'HR' | 'Marketing' | 'Operations';
export type ViewType = 'dashboard' | 'market' | 'comms' | 'wiki' | 'team' | 'office'; // Added for UI routing

export interface GameResources {
    coins: number;
    reputation: number;
    cashflow: {
        revenue: number; // Daily revenue
        burn: number;    // Daily costs
    };
}

export interface Department {
    id: DeptType;
    level: number;
    stats: Record<string, any>; // e.g., { capacity: 12, efficiency: 1.1 }
}

export interface Contract {
    id: string;
    is_global: boolean;
    title: string;
    description: string;
    difficulty: ContractDifficulty;
    topic: ContractTopic;

    requirements: {
        min_reputation?: number;
        required_skills?: string[];
    };

    reward: {
        coins: number;
        reputation: number;
        xp?: number;
    };

    // State for active contracts
    progress?: number; // 0-100
    deadline?: string; // ISO Date for active local contracts

    // Market specific
    expires_at?: string;
    auction_end?: string;
    current_high_bid?: number;
    negotiation_required?: boolean; // New: Requires sales interaction
    instant_accept?: boolean;       // New: Can be taken immediately without overhead
}

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

export interface Employee {
    id: string;
    name: string;
    role: string;
    specialty: ContractTopic;
    salary: number;
    stats: {
        morale: number;
        skill_level: number;
        speed?: number;     // Added
        quality?: number;   // Added
        stamina?: number;   // Added
    };
    assigned_to?: string | null; // Contract ID or 'bench' or 'research'
}

export interface ResearchProject {
    id: string;
    name: string;
    cost: number;
    duration_minutes: number;
    effect_description: string;
    status: 'locked' | 'available' | 'in_progress' | 'completed';
    progress?: number;
}

export interface ConsultingGameState {
    user_id: string;
    resources: GameResources;
    departments: Record<DeptType, Department>;
    active_contracts: Contract[]; // Accepted and in progress
    market_contracts: Contract[]; // Available for taking
    employees: Employee[];
    active_events: GameEvent[]; // Added for Live Intel
    research: {
        active_project_id: string | null;
        completed_projects: string[]; // IDs
    };
    last_updated: string;
}
