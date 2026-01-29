export type PlayerRole = 'MANAGER' | 'EMPLOYEE'

export interface Character {
    id: string
    name: string
    role: PlayerRole
    efficiency: number // Efektywność (PE)
    availability: number // Dostępność (PD)
    maxAvailability: number
}

export interface RoundStats {
    round: number
    cashStart: number
    cashEnd: number
    income: number
    expenses: number
    balance: number // income - expenses
    teamEfficiency: number
}

export interface GameState {
    round: number
    maxRounds: number
    phase: GamePhase
    cash: number
    knowledgeCrystals: number // KW
    team: Character[]
    activeContracts: ActiveContract[]
    currentEvent: EventCard | null // [NEW]

    // Stats Tracking
    currentRoundStats: {
        income: number
        expenses: number
    }

    isPhaseReady?: boolean // [NEW] Navigation lock

    // UI Effects
    lastCashTransaction?: { amount: number, id: number } | null
    lastKWTransaction?: { amount: number, id: number } | null // [NEW]
    projectedTeamCost?: Record<string, number> // Map charId -> cost to show in UI


    history: {
        events: string[]
        pills: string[]
        completedContracts: CompletedContract[] // Changed from string[]
        roundStats: RoundStats[]
    }
}

export type GamePhase = 'EVENT' | 'PILL' | 'TASK' | 'DEVELOPMENT' | 'CONTRACT' | 'SUMMARY'

// --- Content Types ---

export interface EventEffect {
    type: 'CASH' | 'KW' | 'EFFICIENCY' | 'AVAILABILITY' | 'NONE'
    target?: 'MANAGER' | 'EMPLOYEE' | 'EMPLOYEES' | 'TEAM' | 'ALL'
    amount: number
    description?: string
}

export interface EventRisk {
    diceCount: number
    // Rules:
    // 'CONTAINS': succeeds if roll includes targetValue
    // 'SUM_GE': succeeds if sum >= targetValue
    // 'SUM_LE': succeeds if sum <= targetValue
    rule: 'CONTAINS' | 'SUM_GE' | 'SUM_LE'
    targetValue: number
    modifier?: 'MANAGER_EFFICIENCY'
    successEffect?: EventEffect[]
    failureEffect?: EventEffect[]
    successMessage?: string // [NEW] Custom narrative for success
    failureMessage?: string // [NEW] Custom narrative for failure ("To było miłe...")
}

export interface EventOption {
    id: string
    label: string
    risk?: EventRisk
    immediateEffects?: EventEffect[]
}

export interface EventCard {
    id: string
    title: string
    description: string
    type: 'POSITIVE' | 'NEGATIVE' | 'NEUTRAL'
    // New structure
    options?: EventOption[]
    immediateEffects?: EventEffect[]
    // For events that are just a forced dice roll, we can treat them as having 1 option "Rzuć kostką" or handle specifically. 
    // To keep it simple, we will use options for everything interactive.
    // Dynamic effect function (Legacy support or for complex logic)
    effect?: (state: GameState) => Partial<GameState>
}

export interface KnowledgePill {
    id: string
    title: string
    content: string // Markdown content
    cost: number // usually 100 or 0
    relatedTaskId?: string
}

export interface TaskCard {
    id: string
    question: string
    type: 'OPEN' | 'QUIZ'
    options?: string[] // for quiz
    correctAnswer?: number | string // index or string match
    rewardKW: number
    relatedPillId: string
}

export interface ContractCard {
    id: string
    title: string // e.g. "KONTRAKT - 2 000 PLN"
    value: number // PLN
    requiredProductivity: number // Wymagana Wydajność
    currentProductivity: number // Progress
    duration: number // 1, 2, or 3 rounds
    roundsLeft: number
    description: string
    bonusCondition?: string
}

export interface ActiveContract extends ContractCard {
    startedRound: number
}

export interface CompletedContract extends ActiveContract {
    completedRound: number
}
