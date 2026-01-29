"use client"

import React, { createContext, useContext, useState, useReducer, useEffect } from 'react'
import { GameState, Character, ContractCard, ActiveContract, EventCard } from '@/types/brainventure'

// Initial State
const INITIAL_TEAM: Character[] = [
    { id: 'manager', name: 'Menedżer', role: 'MANAGER', efficiency: 5, availability: 10, maxAvailability: 10 },
    { id: 'emp1', name: 'Pracownik 1', role: 'EMPLOYEE', efficiency: 3, availability: 10, maxAvailability: 10 },
    { id: 'emp2', name: 'Pracownik 2', role: 'EMPLOYEE', efficiency: 3, availability: 10, maxAvailability: 10 },
]

const PHASES = ['EVENT', 'PILL', 'TASK', 'DEVELOPMENT', 'CONTRACT', 'SUMMARY'] as const
type GamePhase = typeof PHASES[number]

const INITIAL_STATE: GameState = {
    round: 1,
    maxRounds: 8,
    phase: 'EVENT',
    cash: 1000,
    knowledgeCrystals: 0,
    team: INITIAL_TEAM,
    activeContracts: [],
    currentEvent: null,
    currentRoundStats: {
        income: 0,
        expenses: 0
    },
    isPhaseReady: false, // New flag for navigation
    history: {
        events: [],
        pills: [],
        completedContracts: [],
        roundStats: [{
            round: 0,
            cashStart: 1000,
            cashEnd: 1000,
            income: 0,
            expenses: 0,
            balance: 0,
            teamEfficiency: 11
        }]
    }
}

// Actions
type GameAction =
    | { type: 'NEXT_PHASE' }
    | { type: 'SET_PHASE_READY'; payload: boolean }
    | { type: 'NEXT_ROUND' }
    | { type: 'UPDATE_CASH'; payload: number; silent?: boolean }
    | { type: 'UPDATE_KW'; payload: number }
    | { type: 'UPDATE_EFFICIENCY'; payload: { charId: string; amount: number } }
    | { type: 'UPDATE_AVAILABILITY'; payload: { charId: string; amount: number } }
    | { type: 'SET_AVAILABILITY'; payload: { charId: string; amount: number } }
    | { type: 'ADD_CONTRACT'; payload: ActiveContract }
    | { type: 'UPDATE_CONTRACT_PROGRESS'; payload: { contractId: string; amount: number } }
    | { type: 'COMPLETE_CONTRACT'; payload: string }
    | { type: 'FAIL_CONTRACT'; payload: string }
    | { type: 'LOG_EVENT'; payload: string }
    | { type: 'SET_CURRENT_EVENT'; payload: EventCard | null }
    | { type: 'UNLOCK_PILL'; payload: string }
    | { type: 'SET_PROJECTED_COST'; payload: Record<string, number> }
    | { type: 'SET_THEME'; payload: 'default' | 'ios' } // New action

// Reducer
function gameReducer(state: GameState, action: GameAction): GameState {
    switch (action.type) {
        case 'SET_PROJECTED_COST':
            return { ...state, projectedTeamCost: action.payload }

        case 'SET_PHASE_READY':
            return { ...state, isPhaseReady: action.payload }

        case 'NEXT_PHASE':
            const currentPhaseIndex = PHASES.indexOf(state.phase as GamePhase)
            const nextPhase = PHASES[(currentPhaseIndex + 1) % PHASES.length]

            if (state.phase === 'SUMMARY') {
                // End of Round Logic: Archive Stats
                const roundStats = {
                    round: state.round,
                    cashStart: state.cash - (state.currentRoundStats.income - state.currentRoundStats.expenses),
                    cashEnd: state.cash,
                    income: state.currentRoundStats.income,
                    expenses: state.currentRoundStats.expenses,
                    balance: state.currentRoundStats.income - state.currentRoundStats.expenses,
                    teamEfficiency: state.team.reduce((acc, char) => acc + char.efficiency, 0)
                }

                return {
                    ...state,
                    phase: 'EVENT',
                    currentEvent: null, // Reset event on new round
                    isPhaseReady: false,
                    round: state.round + 1,
                    team: state.team.map(c => ({ ...c, availability: c.maxAvailability })),
                    currentRoundStats: { income: 0, expenses: 0 },
                    history: {
                        ...state.history,
                        roundStats: [...state.history.roundStats, roundStats]
                    }
                }
            }
            return { ...state, phase: nextPhase, isPhaseReady: false }

        case 'NEXT_ROUND':
            // Logic handled in NEXT_PHASE if using Summary transition, keeping specific action just in case.
            return {
                ...state,
                round: state.round + 1,
                phase: 'EVENT',
                currentEvent: null,
                isPhaseReady: false,
                team: state.team.map(char => ({ ...char, availability: char.maxAvailability }))
            }

        case 'UPDATE_CASH':
            const amount = action.payload
            const isIncome = amount > 0
            return {
                ...state,
                cash: state.cash + amount,
                currentRoundStats: {
                    ...state.currentRoundStats,
                    income: isIncome ? state.currentRoundStats.income + amount : state.currentRoundStats.income,
                    expenses: !isIncome ? state.currentRoundStats.expenses + Math.abs(amount) : state.currentRoundStats.expenses
                },
                lastCashTransaction: action.silent ? state.lastCashTransaction : { amount, id: Date.now() + Math.random() }
            }

        case 'UPDATE_KW':
            return {
                ...state,
                knowledgeCrystals: state.knowledgeCrystals + action.payload,
                lastKWTransaction: { amount: action.payload, id: Date.now() + Math.random() }
            }

        case 'UPDATE_EFFICIENCY':
            return {
                ...state,
                team: state.team.map(char =>
                    char.id === action.payload.charId
                        ? { ...char, efficiency: Math.max(0, char.efficiency + action.payload.amount) }
                        : char
                )
            }

        case 'UPDATE_AVAILABILITY':
            return {
                ...state,
                team: state.team.map(char =>
                    char.id === action.payload.charId
                        ? { ...char, availability: Math.max(0, char.availability + action.payload.amount) }
                        : char
                )
            }

        case 'SET_AVAILABILITY':
            return {
                ...state,
                team: state.team.map(char =>
                    char.id === action.payload.charId
                        ? { ...char, availability: action.payload.amount }
                        : char
                )
            }

        case 'ADD_CONTRACT':
            return { ...state, activeContracts: [...state.activeContracts, action.payload] }

        case 'UPDATE_CONTRACT_PROGRESS':
            let parsedState = { ...state }
            const contractIndex = parsedState.activeContracts.findIndex(c => c.id === action.payload.contractId)

            if (contractIndex === -1) return state

            const targetContract = parsedState.activeContracts[contractIndex]
            const newProgress = (targetContract.currentProductivity || 0) + action.payload.amount

            parsedState.activeContracts = parsedState.activeContracts.map(c =>
                c.id === action.payload.contractId
                    ? { ...c, currentProductivity: newProgress }
                    : c
            )
            return parsedState

        case 'COMPLETE_CONTRACT':
            const completedContract = state.activeContracts.find(c => c.id === action.payload)
            if (!completedContract) return state // Should not happen

            return {
                ...state,
                activeContracts: state.activeContracts.filter(c => c.id !== action.payload),
                history: {
                    ...state.history,
                    completedContracts: [...state.history.completedContracts, { ...completedContract, completedRound: state.round }]
                }
            }

        case 'LOG_EVENT':
            return {
                ...state,
                history: { ...state.history, events: [...state.history.events, action.payload] }
            }

        case 'SET_CURRENT_EVENT':
            return { ...state, currentEvent: action.payload }

        case 'UNLOCK_PILL':
            if (state.history.pills.includes(action.payload)) return state
            return {
                ...state,
                history: { ...state.history, pills: [...state.history.pills, action.payload] }
            }

        default:
            return state
    }
}

// Context
interface BrainVentureContextType {
    state: GameState
    dispatch: React.Dispatch<GameAction>
    formatMoney: (amount: number) => string
    calculateProductivity: (char: Character) => number
    getTeamProductivity: () => number
}

const BrainVentureContext = createContext<BrainVentureContextType | undefined>(undefined)

export function BrainVentureProvider({ children }: { children: React.ReactNode }) {
    const [state, dispatch] = useReducer(gameReducer, INITIAL_STATE)

    const formatMoney = (amount: number) => {
        return new Intl.NumberFormat('pl-PL', { style: 'currency', currency: 'PLN', maximumFractionDigits: 0 }).format(amount)
    }

    const calculateProductivity = (char: Character) => {
        return char.efficiency * char.availability
    }

    const getTeamProductivity = () => {
        return state.team.reduce((acc, char) => acc + calculateProductivity(char), 0)
    }

    return (
        <BrainVentureContext.Provider value={{ state, dispatch, formatMoney, calculateProductivity, getTeamProductivity }}>
            {children}
        </BrainVentureContext.Provider>
    )
}

export function useBrainVenture() {
    const context = useContext(BrainVentureContext)
    if (context === undefined) {
        throw new Error('useBrainVenture must be used within a BrainVentureProvider')
    }
    return context
}
