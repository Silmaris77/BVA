// Spaced Repetition System for Engrams
// Implements a simplified Leitner System with decay calculation

/**
 * Calculate current strength of an engram based on time since last refresh
 * Engram decays approximately:
 * - Day 1: 100%
 * - Day 3: ~80%
 * - Day 7: ~60%
 * - Day 14: ~40%
 * - Day 30: ~20%
 * - Day 60+: ~10% (minimum)
 */
export function calculateEngramStrength(lastRefreshedAt: string | null): number {
    if (!lastRefreshedAt) return 0;

    const lastRefresh = new Date(lastRefreshedAt);
    const now = new Date();
    const daysSinceRefresh = Math.floor((now.getTime() - lastRefresh.getTime()) / (1000 * 60 * 60 * 24));

    // Decay curve using modified Ebbinghaus formula
    // S = 100 * e^(-k*t) where k ≈ 0.05
    const decayRate = 0.05;
    const minStrength = 10;
    const strength = Math.max(minStrength, Math.round(100 * Math.exp(-decayRate * daysSinceRefresh)));

    return strength;
}

/**
 * Calculate next refresh due date based on refresh count (Leitner intervals)
 * More refreshes = longer intervals
 */
export function calculateNextRefreshDue(refreshCount: number, lastRefreshedAt: string): Date {
    // Leitner-style intervals: 1, 3, 7, 14, 30, 60 days
    const intervals = [1, 3, 7, 14, 30, 60];
    const intervalIndex = Math.min(refreshCount, intervals.length - 1);
    const daysUntilRefresh = intervals[intervalIndex];

    const lastRefresh = new Date(lastRefreshedAt);
    const nextDue = new Date(lastRefresh);
    nextDue.setDate(nextDue.getDate() + daysUntilRefresh);

    return nextDue;
}

/**
 * Check if an engram needs refresh
 */
export function needsRefresh(strength: number, threshold: number = 70): boolean {
    return strength < threshold;
}

/**
 * Get refresh urgency level for UI styling
 */
export function getRefreshUrgency(strength: number): 'critical' | 'warning' | 'good' | 'excellent' {
    if (strength <= 30) return 'critical';  // Red - urgent refresh needed
    if (strength <= 60) return 'warning';    // Orange - refresh soon
    if (strength <= 85) return 'good';       // Yellow - stable
    return 'excellent';                       // Green - fresh
}

/**
 * Get status label in Polish
 */
export function getStrengthLabel(strength: number): string {
    if (strength >= 90) return 'Doskonała';
    if (strength >= 70) return 'Dobra';
    if (strength >= 50) return 'Średnia';
    if (strength >= 30) return 'Słaba';
    return 'Zapomniane';
}

/**
 * Get color for strength visualization
 */
export function getStrengthColor(strength: number): string {
    if (strength >= 90) return '#00ff88';  // Bright green
    if (strength >= 70) return '#00d4ff';  // Cyan
    if (strength >= 50) return '#ffd700';  // Gold
    if (strength >= 30) return '#ff8800';  // Orange
    return '#ff4444';                       // Red
}

/**
 * Format time until refresh in Polish
 */
export function formatTimeUntilRefresh(nextRefreshDue: string | Date | null): string {
    if (!nextRefreshDue) return 'Teraz';

    const due = nextRefreshDue instanceof Date ? nextRefreshDue : new Date(nextRefreshDue);
    const now = new Date();
    const diffMs = due.getTime() - now.getTime();

    if (diffMs <= 0) return 'Teraz';

    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    const diffHours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));

    if (diffDays > 0) {
        if (diffDays === 1) return 'za 1 dzień';
        if (diffDays < 5) return `za ${diffDays} dni`;
        return `za ${diffDays} dni`;
    }

    if (diffHours > 0) {
        if (diffHours === 1) return 'za 1 godzinę';
        if (diffHours < 5) return `za ${diffHours} godziny`;
        return `za ${diffHours} godzin`;
    }

    return 'wkrótce';
}

export interface EngramWithSpacedRepetition {
    id: string;
    engram_id: string;
    title: string;
    installed: boolean;
    strength: number;
    refreshCount: number;
    lastRefreshedAt: string | null;
    nextRefreshDue: string | null;
    urgency: 'critical' | 'warning' | 'good' | 'excellent';
    needsRefresh: boolean;
}

/**
 * Sort engrams by refresh priority (most urgent first)
 */
export function sortByRefreshPriority(engrams: EngramWithSpacedRepetition[]): EngramWithSpacedRepetition[] {
    return [...engrams].sort((a, b) => {
        // First, installed engrams needing refresh come first
        if (a.needsRefresh && !b.needsRefresh) return -1;
        if (!a.needsRefresh && b.needsRefresh) return 1;

        // Then sort by strength (lower = more urgent)
        return a.strength - b.strength;
    });
}

/**
 * Get engrams due for refresh today
 */
export function getEngramsDueToday(engrams: EngramWithSpacedRepetition[]): EngramWithSpacedRepetition[] {
    const today = new Date();
    today.setHours(23, 59, 59, 999);

    return engrams.filter(e => {
        if (!e.installed || !e.nextRefreshDue) return e.strength < 70;
        const due = new Date(e.nextRefreshDue);
        return due <= today || e.strength < 70;
    });
}
