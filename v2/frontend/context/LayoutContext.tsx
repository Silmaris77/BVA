"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { api, UserStats } from "@/services/api";

type Theme = "glass" | "minimal" | "cyberpunk" | "executive";

interface LayoutState {
    theme: Theme;
    setTheme: (theme: Theme) => void;
}

const LayoutContext = createContext<LayoutState | undefined>(undefined);

export function LayoutProvider({ children }: { children: React.ReactNode }) {
    const [theme, setThemeState] = useState<Theme>("glass");
    const [user, setUser] = useState<UserStats | null>(null);

    // Load detailed user settings on mount
    useEffect(() => {
        async function loadSettings() {
            try {
                // Here we might need a dedicated settings endpoint or just use user profile
                // For now, let's assume getMe returns preferences
                const userData = await api.getCurrentUser();
                setUser(userData);

                if (userData.preferences?.theme) {
                    setThemeState(userData.preferences.theme as Theme);
                }
            } catch (e) {
                console.warn("Failed to load user preferences", e);
            }
        }
        loadSettings();
    }, []);

    useEffect(() => {
        document.body.setAttribute('data-theme', theme);
    }, [theme]);

    const setTheme = async (newTheme: Theme) => {
        setThemeState(newTheme);
        try {
            await api.updateUser({
                preferences: { ...user?.preferences, theme: newTheme }
            });
        } catch (e) { console.error("Failed to save theme", e); }
    };

    return (
        <LayoutContext.Provider value={{ theme, setTheme }}>
            {children}
            <style jsx global>{`
                /* === DEFAULT / GLASS THEME === */
                :root {
                    --bg-primary: #0f0c29;
                    --text-primary: #ffffff;
                    --glass-bg: rgba(255, 255, 255, 0.05);
                    --glass-border: rgba(255, 255, 255, 0.1);
                }

                .app-wrapper {
                    background-color: var(--bg-primary);
                    color: var(--text-primary);
                }

                /* === MINIMAL THEME === */
                body[data-theme='minimal'] {
                    --bg-primary: #f4f4f5; /* zinc-100 */
                    --text-primary: #18181b; /* zinc-900 */
                }

                body[data-theme='minimal'] .app-wrapper {
                    background-color: #f4f4f5 !important;
                    color: #18181b !important;
                }

                /* Hide background blobs in minimal */
                body[data-theme='minimal'] .bg-gradient-blobs {
                    display: none !important;
                }

                /* Reset Glass Cards to Clean Cards */
                body[data-theme='minimal'] .glass-card, 
                body[data-theme='minimal'] div[class*="GlassCard"] {
                    background: #ffffff !important;
                    border: 1px solid #e4e4e7 !important; /* zinc-200 */
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
                    backdrop-filter: none !important;
                    color: #18181b !important;
                }

                /* Text Colors Override for Minimal */
                body[data-theme='minimal'] h1, 
                body[data-theme='minimal'] h2, 
                body[data-theme='minimal'] h3,
                body[data-theme='minimal'] span,
                body[data-theme='minimal'] p,
                body[data-theme='minimal'] div {
                    color: inherit; /* Allow inheritance forcing */
                }
                
                body[data-theme='minimal'] .text-white { color: #18181b !important; }
                body[data-theme='minimal'] .text-white\/50 { color: #71717a !important; }
                body[data-theme='minimal'] .text-white\/60 { color: #52525b !important; }
                
                /* Sidebar Adjustments for Minimal */
                body[data-theme='minimal'] aside {
                     background: #ffffff !important;
                     border-right: 1px solid #e4e4e7 !important;
                }

                /* === EXECUTIVE THEME (1:1 Port) === */
                body[data-theme='executive'] {
                    --bg-primary: #f8f9fa; /* slate-50 */
                    --text-primary: #1e293b; /* slate-800 */
                }

                body[data-theme='executive'] .app-wrapper {
                    background-color: #f8f9fa !important;
                    color: #1e293b !important;
                }

                body[data-theme='executive'] .bg-gradient-blobs {
                    display: none !important;
                }

                /* Executive Cards - Exact Match */
                body[data-theme='executive'] .glass-card, 
                body[data-theme='executive'] div[class*="GlassCard"] {
                    background: #ffffff !important;
                    border: 1px solid #e2e8f0 !important; /* slate-200 */
                    border-radius: 6px !important;
                    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
                    backdrop-filter: none !important;
                    color: #1e293b !important;
                }

                /* Executive Typography */
                body[data-theme='executive'] h1, 
                body[data-theme='executive'] h2 {
                    color: #0f172a !important; /* slate-900 */
                    font-weight: 700;
                    letter-spacing: -0.025em;
                }
                
                body[data-theme='executive'] h3 {
                    color: #0f172a !important;
                    font-weight: 600;
                }
                
                body[data-theme='executive'] p, 
                body[data-theme='executive'] span,
                body[data-theme='executive'] div {
                    color: inherit;
                }

                /* Fix Text Colors */
                body[data-theme='executive'] .text-white { color: #0f172a !important; }
                body[data-theme='executive'] .text-white\/50 { color: #64748b !important; } /* slate-500 */
                body[data-theme='executive'] .text-white\/60 { color: #475569 !important; } /* slate-600 */
                body[data-theme='executive'] .text-gray-400 { color: #94a3b8 !important; } /* slate-400 */

                /* Executive Sidebar - Dark Navy Blue */
                body[data-theme='executive'] aside {
                     background: #0f172a !important; /* slate-900 */
                     border-right: 1px solid #1e293b !important;
                     color: white !important;
                }
                
                /* Sidebar specific overrides to keep it white/light-gray text */
                body[data-theme='executive'] aside .text-white { color: #ffffff !important; }
                body[data-theme='executive'] aside .text-white\/50 { color: #94a3b8 !important; } /* slate-400 */
                body[data-theme='executive'] aside .text-gray-400 { color: #94a3b8 !important; }
                body[data-theme='executive'] aside div { color: inherit; }

                /* Sidebar Active Item Style */
                body[data-theme='executive'] aside .bg-white\/10 {
                    background-color: rgba(59, 130, 246, 0.2) !important; /* blue-900/50-ish */
                    border-left: 4px solid #3b82f6 !important; /* blue-500 */
                    border-radius: 4px !important;
                    color: #dbeafe !important; /* blue-100 */
                }

                /* === CYBERPUNK THEME === */
                body[data-theme='cyberpunk'] .app-wrapper {
                    background-color: #000000 !important;
                    background-image: 
                        linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px);
                    background-size: 30px 30px;
                }
                
                body[data-theme='cyberpunk'] .glass-card, 
                body[data-theme='cyberpunk'] div[class*="GlassCard"] {
                    background: rgba(0, 0, 0, 0.9) !important;
                    border: 1px solid #fcee0a !important; /* Cyber Yellow */
                    box-shadow: 4px 4px 0px #0ef !important; /* Cyan shadow */
                    border-radius: 0 !important;
                }
                body[data-theme='cyberpunk'] .bg-gradient-blobs {
                    filter: hue-rotate(90deg) contrast(1.5);
                }
            `}</style>
        </LayoutContext.Provider>
    );
}

export const useLayout = () => {
    const context = useContext(LayoutContext);
    if (context === undefined) {
        throw new Error("useLayout must be used within a LayoutProvider");
    }
    return context;
};
