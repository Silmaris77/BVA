'use server'

import { createClient } from '@/lib/supabase/server';
import { ConsultingGameState, DeptType } from './types';
import { INITIAL_STATE, reconcileState, calculateBurnRate, hireEmployee as engineHire, upgradeOffice as engineUpgrade, generateContracts } from './engine';
import { revalidatePath } from 'next/cache';

// ... (existing code)

export async function refreshGlobalMarketAction() {
    return performGameAction('refreshMarket', (state) => {
        const newContracts = generateContracts(state);
        // Replace current market contracts with new ones (daily refresh)
        state.market_contracts = newContracts;
        return state;
    });
}

/**
 * Fetches the current user's game state.
 * If no game exists, creates a new one with INITIAL_STATE.
 * Applies reconcileState to update values based on time passed.
 */
export async function getGame(): Promise<ConsultingGameState> {
    const supabase = await createClient();
    const { data: { user } } = await supabase.auth.getUser();

    if (!user) {
        throw new Error('Unauthorized');
    }

    const { data: gameRow, error } = await supabase
        .from('consulting_games')
        .select('*')
        .eq('user_id', user.id)
        .single();

    if (error && error.code !== 'PGRST116') { // PGRST116 = JSON not found (0 rows)
        console.error('Error fetching game:', error);
        throw new Error('Failed to fetch consulting game');
    }

    // 1. New Game Creation
    if (!gameRow) {
        const newState = { ...INITIAL_STATE, user_id: user.id };

        // Insert new game
        const { error: insertError } = await supabase
            .from('consulting_games')
            .insert({
                user_id: user.id,
                state: newState,
            });

        if (insertError) {
            console.error('Error creating game:', insertError);
            throw new Error('Failed to create new game');
        }

        return newState;
    }

    // 2. Existing Game - Load & Reconcile
    let currentState = gameRow.state as ConsultingGameState;

    // Reconcile (Catch up real-time stats)
    const reconciledState = reconcileState(currentState);

    // If state changed significantly (e.g. burn rate applied), save it back
    if (reconciledState.last_updated !== currentState.last_updated) {
        await saveGame(reconciledState);
    }

    return reconciledState;
}

/**
 * Persists the game state to Supabase.
 */
export async function saveGame(state: ConsultingGameState) {
    const supabase = await createClient();
    const { data: { user } = {} } = await supabase.auth.getUser();

    if (!user || user.id !== state.user_id) {
        throw new Error('Unauthorized');
    }

    const { error } = await supabase
        .from('consulting_games')
        .update({
            state: state,
            updated_at: new Date().toISOString()
        })
        .eq('user_id', user.id);

    if (error) {
        console.error('Error saving game:', error);
        throw new Error('Failed to save game');
    }
}


/**
 * GENERIC ACTION HANDLER
 * Wraps logic to: Get Game -> Modify State -> Save Game -> Revalidate
 */
export async function performGameAction(
    actionName: string,
    updateFn: (state: ConsultingGameState) => ConsultingGameState
) {
    try {
        const state = await getGame();
        const newState = updateFn(state); // Logic runs here
        await saveGame(newState);
        revalidatePath('/practice/games/consulting');
        return { success: true, state: newState };
    } catch (e) {
        console.error(`Action ${actionName} failed:`, e);
        return { success: false, error: 'Action failed' };
    }
}

// --- PUBLIC ACTIONS ---

export async function advanceTime() {
    return performGameAction('advanceTime', (state) => {
        // Simple manual tick: Advance 4 hours (240 mins)
        // In a real game, this might be calculated.
        // For MVP, "Work" just pushes time forward and triggers passive income/burn calculation implicitly via next reconcile
        // But reconcileState relies on Date.now().
        // So "Actively Working" should probably grant immediate progress on Active Contract.

        const activeContract = state.active_contracts[0];
        if (activeContract) {
            activeContract.progress = (activeContract.progress || 0) + 10; // +10% progress
            if (activeContract.progress >= 100) {
                // COMPLETE CONTRACT LOGIC (Simplified)
                state.resources.coins += activeContract.reward.coins;
                state.resources.reputation += activeContract.reward.reputation;
                state.active_contracts = state.active_contracts.filter(c => c.id !== activeContract.id);
            }
        }
        return state;
    });
}

export async function hireEmployeeAction(role: string, cost: number) {
    return performGameAction('hireEmployee', (state) => {
        return engineHire(state, role as any, cost);
    });
}

export async function upgradeOfficeAction() {
    return performGameAction('upgradeOffice', (state) => {
        return engineUpgrade(state);
    });
}



export async function acceptContractAction(contractId: string) {
    return performGameAction('acceptContract', (state) => {
        // Find in market based on ID
        const contractIndex = state.market_contracts.findIndex(c => c.id === contractId);
        if (contractIndex === -1) {
            // Check if it's already active (idempotency)
            if (state.active_contracts.find(c => c.id === contractId)) return state;
            return state; // Not found
        }

        const contract = state.market_contracts[contractIndex];

        // START CONTRACT LOGIC
        // Move to active
        const activeContract: any = { ...contract };
        activeContract.is_global = false; // Now it's considered accepted/local context
        activeContract.progress = 0;

        // Deadline logic: Mock 2 days deadline for now. 
        // In engine.ts we set expires_at for the offer. Here we set deadline for completion.
        activeContract.deadline = new Date(Date.now() + 1000 * 60 * 60 * 24 * 3).toISOString(); // 3 days to finish

        state.active_contracts.push(activeContract);

        // Remove from market
        state.market_contracts.splice(contractIndex, 1);

        return state;
    });
}
