// src/lib/access-control.ts
// Access control helper functions for content restrictions

import { createClient } from '@/lib/supabase/client';

export interface User {
    id: string;
    companyId: string;
    roleId: string;
    department?: string;
    totalXp: number;
    completedLessons: string[];
}

export interface AccessRule {
    contentType: 'lesson' | 'engram' | 'tool' | 'resource' | 'drill' | 'path';
    contentId: string;
    allowedCompanies?: string[];
    allowedRoles?: string[];
    requiredDepartments?: string[];
    minXpRequired: number;
    prerequisiteLessons?: string[];
}

export interface AccessCheckResult {
    hasAccess: boolean;
    reason?: string;
    missingPrerequisites?: string[];
    xpNeeded?: number;
}

/**
 * Check if user has access to specific content
 */
export async function checkContentAccess(
    userId: string,
    contentId: string,
    contentType: 'lesson' | 'engram' | 'tool' | 'resource' | 'drill' | 'path'
): Promise<AccessCheckResult> {
    const supabase = createClient();

    // Get user profile
    const { data: profile } = await supabase
        .from('user_profiles')
        .select(`
      company_id,
      role_id,
      department,
      company:companies(company_slug, is_general_group)
    `)
        .eq('id', userId)
        .single();

    if (!profile) {
        return { hasAccess: false, reason: 'User profile not found' };
    }

    // Get access rules for this content
    const { data: rule } = await supabase
        .from('content_access_rules')
        .select('*')
        .eq('content_type', contentType)
        .eq('content_id', contentId)
        .single();

    // No rules = public content
    if (!rule) {
        return { hasAccess: true };
    }

    // Check 1: Company restriction
    if (rule.allowed_companies && rule.allowed_companies.length > 0) {
        if (!rule.allowed_companies.includes(profile.company_id)) {
            const companyData = Array.isArray(profile.company) ? profile.company[0] : profile.company;
            const isGeneral = companyData?.is_general_group;
            return {
                hasAccess: false,
                reason: isGeneral
                    ? 'Content dostępny tylko dla przypisanych firm. Skontaktuj się z administratorem.'
                    : 'Content dostępny tylko dla określonych firm.'
            };
        }
    }

    // Check 2: Role restriction
    if (rule.allowed_roles && rule.allowed_roles.length > 0) {
        if (!rule.allowed_roles.includes(profile.role_id)) {
            return {
                hasAccess: false,
                reason: 'Content dostępny tylko dla określonych stanowisk.'
            };
        }
    }

    // Check 3: Department restriction
    if (rule.required_departments && rule.required_departments.length > 0) {
        if (!profile.department || !rule.required_departments.includes(profile.department)) {
            return {
                hasAccess: false,
                reason: 'Content dostępny tylko dla określonych działów.'
            };
        }
    }

    // Check 4: XP requirement
    if (rule.min_xp_required > 0) {
        const { data: xpData } = await supabase
            .rpc('get_user_total_xp', { user_uuid: userId });

        const userXp = xpData || 0;

        if (userXp < rule.min_xp_required) {
            return {
                hasAccess: false,
                reason: `Wymagane ${rule.min_xp_required} XP`,
                xpNeeded: rule.min_xp_required - userXp
            };
        }
    }

    // Check 5: Prerequisites
    if (rule.prerequisite_lessons && rule.prerequisite_lessons.length > 0) {
        const { data: completedLessons } = await supabase
            .from('user_lesson_progress')
            .select('lesson_id')
            .eq('user_id', userId)
            .eq('status', 'completed');

        const completedIds = (completedLessons || []).map((l: { lesson_id: string }) => l.lesson_id);
        const missing = rule.prerequisite_lessons.filter(
            (prereq: string) => !completedIds.includes(prereq)
        );

        if (missing.length > 0) {
            return {
                hasAccess: false,
                reason: 'Wymagane ukończenie wcześniejszych lekcji',
                missingPrerequisites: missing
            };
        }
    }

    // All checks passed
    return { hasAccess: true };
}

/**
 * Get user's total XP
 */
export async function getUserTotalXp(userId: string): Promise<number> {
    const supabase = createClient();
    const { data } = await supabase.rpc('get_user_total_xp', { user_uuid: userId });
    return data || 0;
}

/**
 * Award XP to user and log transaction
 */
export async function awardXP(params: {
    userId: string;
    sourceType: 'lesson' | 'engram' | 'tool' | 'drill' | 'path' | 'bonus';
    sourceId: string;
    xpAmount: number;
    description?: string;
}): Promise<boolean> {
    const supabase = createClient();

    const { error } = await supabase
        .from('user_xp_transactions')
        .insert({
            user_id: params.userId,
            source_type: params.sourceType,
            source_id: params.sourceId,
            xp_amount: params.xpAmount,
            description: params.description
        });

    return !error;
}

/**
 * Get user's completed lessons
 */
export async function getUserCompletedLessons(userId: string): Promise<string[]> {
    const supabase = createClient();

    const { data } = await supabase
        .from('user_lesson_progress')
        .select('lesson_id')
        .eq('user_id', userId)
        .eq('status', 'completed');

    return (data || []).map((l: { lesson_id: string }) => l.lesson_id);
}
