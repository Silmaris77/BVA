"use client";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

// --- Interfaces ---

export interface UserStats {
    username: string;
    email: string | null;
    full_name: string | null;
    avatar_url: string | null;
    xp: number;
    level: number;
    degencoins: number;
    degen_type: string | null;
    company: string | null;
    preferences: Record<string, any> | null;
}

export interface UserUpdate {
    full_name?: string;
    email?: string;
    company?: string;
    avatar_url?: string;
    degen_type?: string;
    preferences?: Record<string, any>;
}

export interface LoginResponse {
    access_token: string;
    token_type: string;
}

export interface ActivityLog {
    id: number;
    activity_type: string;
    description: string | null;
    xp_awarded: number;
    timestamp: string;
}

export interface MilwaukeeContext {
    typ_klienta: string;
    typ_pracy: string;
    materialy_srodowisko: string[];
    skala: string;
}

export interface MilwaukeeAppMatch {
    app_id: string;
    score: number;
    reason: string;
    details: any;
}

export interface DiscoveryQuestion {
    id: string;
    question: string;
    type: string;
    options?: string[];
    scale?: string[];
    purpose?: string;
}

export interface RecommendationPackage {
    package: any;
    persuasion_script?: any;
    roi_calculator?: any;
    case_studies?: any[];
}

export interface LessonListItem {
    id: string;
    title: string;
    description: string;
    tag: string;
    xp_reward: number;
    difficulty: string;
    estimated_time: string;
    available: boolean;
}

export interface LessonDetails {
    id: string;
    title: string;
    description: string;
    tag: string;
    xp_reward: number;
    difficulty: string;
    available: boolean;
    // ... dynamic content fields ...
    [key: string]: any;
}

// --- Api Client ---

class ApiClient {
    private baseUrl: string;
    private token: string | null = null;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
        if (typeof window !== "undefined") {
            this.token = localStorage.getItem("auth_token");
        }
    }

    setToken(token: string) {
        this.token = token;
        if (typeof window !== "undefined") {
            localStorage.setItem("auth_token", token);
        }
    }

    clearToken() {
        this.token = null;
        if (typeof window !== "undefined") {
            localStorage.removeItem("auth_token");
        }
    }

    getToken() {
        return this.token;
    }

    private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
        const headers: HeadersInit = {
            "Content-Type": "application/json",
            ...options.headers,
        };

        if (this.token) {
            (headers as Record<string, string>)["Authorization"] = `Bearer ${this.token}`;
        }

        const url = `${this.baseUrl}${endpoint}`;
        console.log(`[ApiClient] Requesting: ${url}`, options);

        try {
            const response = await fetch(url, {
                ...options,
                headers,
            });

            if (!response.ok) {
                const errText = await response.text();
                throw new Error(`API Error: ${response.status} ${response.statusText} - ${errText}`);
            }

            const text = await response.text();
            return text ? JSON.parse(text) : {} as T;

        } catch (error) {
            console.error(`[ApiClient] Error fetching ${url}:`, error);
            throw error;
        }
    }

    async login(username: string, password: string): Promise<LoginResponse> {
        const formData = new URLSearchParams();
        formData.append("username", username);
        formData.append("password", password);

        const response = await fetch(`${this.baseUrl}/token`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Login failed");
        }

        const data: LoginResponse = await response.json();
        this.setToken(data.access_token);
        return data;
    }

    async getCurrentUser(): Promise<UserStats> {
        return this.request<UserStats>("/users/me");
    }

    async getHealth(): Promise<{ status: string; version: string }> {
        return this.request("/api/health");
    }

    async getUserStats(username: string): Promise<UserStats> {
        return this.request<UserStats>(`/users/${username}/stats`);
    }

    async getUserActivities(username: string): Promise<ActivityLog[]> {
        return this.request<ActivityLog[]>(`/users/${username}/activities`);
    }

    async updateUser(data: UserUpdate): Promise<UserStats> {
        return this.request<UserStats>("/users/me", {
            method: "PUT",
            body: JSON.stringify(data)
        });
    }

    // --- Milwaukee Tools ---

    async getContextQuestions() {
        return this.request<any>("/tools/milwaukee/context-questions");
    }

    async matchApplication(context: MilwaukeeContext) {
        return this.request<MilwaukeeAppMatch[]>("/tools/milwaukee/match-application", {
            method: "POST",
            body: JSON.stringify(context),
        });
    }

    async getDiscoveryQuestions(clientType: string) {
        return this.request<DiscoveryQuestion[]>(`/tools/milwaukee/discovery-questions/${clientType}`);
    }

    async getRecommendation(appId: string, answers: any) {
        return this.request<RecommendationPackage>("/tools/milwaukee/recommendation", {
            method: "POST",
            body: JSON.stringify({ app_id: appId, answers }),
        });
    }

    // --- Lessons ---

    async getLessons(): Promise<LessonResponse[]> {
        return this.request<LessonResponse[]>("/lessons");
    }

    async getLessonDetails(lessonId: string): Promise<LessonResponse> {
        return this.request<LessonResponse>(`/lessons/${lessonId}`);
    }

    async completeLesson(lessonId: string): Promise<{ status: string; xp_gained: number }> {
        return this.request<{ status: string; xp_gained: number }>(`/lessons/${lessonId}/complete`, {
            method: "POST"
        });
    }
}

export interface LessonResponse {
    id: string;
    title: string;
    description: string;
    category: string;
    video_url: string;
    thumbnail_url: string | null;
    duration: number;
    xp_reward: number;
    difficulty: string;
    completed: boolean;
    available?: boolean; // legacy support
}

export const api = new ApiClient(API_BASE_URL);
