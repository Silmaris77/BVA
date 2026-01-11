// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface DashboardData {
    operator_name: string;
    stats: {
        xp: number;
        xp_change: string;
        vc: number;
        vc_level: number;
        neural_link_status: string;
        neural_link_latency: string;
    };
    missions: Array<{
        id: string;
        icon_type: string;
        title: string;
        subtitle: string;
        reward_xp: string;
        reward_vc?: string;
        action: string;
        is_crisis: boolean;
    }>;
    top_operators: Array<{
        rank: number;
        name: string;
        score: number;
        is_current_user: boolean;
    }>;
    competence: {
        labels: string[];
        values: number[];
    };
    system_status: string;
    calendar_sync: string;
}

export async function fetchDashboard(): Promise<DashboardData> {
    const response = await fetch(`${API_BASE_URL}/api/dashboard`);

    if (!response.ok) {
        throw new Error(`Failed to fetch dashboard: ${response.statusText}`);
    }

    return response.json();
}
