// API client for Neural Implants
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface NeuralImplant {
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

export interface ImplantsResponse {
    implants: NeuralImplant[];
    categories: string[];
}

export interface ImplantDetail {
    implant: NeuralImplant;
    learning_objectives: string[];
    next_steps: string;
    recommended_practice: string;
}

export async function fetchImplants(category?: string, status?: string): Promise<ImplantsResponse> {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (status) params.append('status', status);

    const url = `${API_BASE_URL}/api/implants?${params}`;
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`Failed to fetch implants: ${response.statusText}`);
    }

    return response.json();
}

export async function fetchImplantDetail(implantId: string): Promise<ImplantDetail> {
    const response = await fetch(`${API_BASE_URL}/api/implants/${implantId}`);

    if (!response.ok) {
        throw new Error(`Failed to fetch implant detail: ${response.statusText}`);
    }

    return response.json();
}

export async function downloadImplant(implantId: string) {
    const response = await fetch(`${API_BASE_URL}/api/implants/${implantId}/download`, {
        method: 'POST'
    });

    if (!response.ok) {
        throw new Error(`Failed to download implant: ${response.statusText}`);
    }

    return response.json();
}

export async function calibrateImplant(implantId: string) {
    const response = await fetch(`${API_BASE_URL}/api/implants/${implantId}/calibrate`, {
        method: 'POST'
    });

    if (!response.ok) {
        throw new Error(`Failed to calibrate implant: ${response.statusText}`);
    }

    return response.json();
}
