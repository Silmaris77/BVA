// API client for Neural Engrams
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface NeuralEngram {
    id: string;
    name: string;
    category: string;
    description: string;
    status: 'available' | 'downloading' | 'calibration' | 'active' | 'degraded';
    progress: number;
    skill_points: number;
    prerequisites: string[];
    estimated_time: string;
    icon_type: string;
    difficulty: string;
}

export interface EngramsResponse {
    engrams: NeuralEngram[];
    categories: string[];
}

export interface EngramDetail {
    engram: NeuralEngram;
    learning_objectives: string[];
    next_steps: string;
    recommended_practice: string;
}

export async function fetchEngrams(category?: string, status?: string): Promise<EngramsResponse> {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (status) params.append('status', status);

    // TODO: Update to /api/engrams when backend is ready
    const url = `${API_BASE_URL}/api/implants?${params}`;
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`Failed to fetch engrams: ${response.statusText}`);
    }

    return response.json();
}

export async function fetchEngramDetail(engramId: string): Promise<EngramDetail> {
    // TODO: Update to /api/engrams when backend is ready
    const response = await fetch(`${API_BASE_URL}/api/implants/${engramId}`);

    if (!response.ok) {
        throw new Error(`Failed to fetch engram detail: ${response.statusText}`);
    }

    return response.json();
}

export async function downloadEngram(engramId: string) {
    // TODO: Update to /api/engrams when backend is ready
    const response = await fetch(`${API_BASE_URL}/api/implants/${engramId}/download`, {
        method: 'POST'
    });

    if (!response.ok) {
        throw new Error(`Failed to download engram: ${response.statusText}`);
    }

    return response.json();
}

export async function calibrateEngram(engramId: string) {
    // TODO: Update to /api/engrams when backend is ready
    const response = await fetch(`${API_BASE_URL}/api/implants/${engramId}/calibrate`, {
        method: 'POST'
    });

    if (!response.ok) {
        throw new Error(`Failed to calibrate engram: ${response.statusText}`);
    }

    return response.json();
}
