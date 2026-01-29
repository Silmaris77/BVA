'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'

export type Theme = 'default' | 'cyber' | 'light' | 'slate' | 'graphite' | 'halloween' | 'chaos' | 'drunk' | 'winter' | 'milwaukee' | 'executive' | 'diplomat' | 'brainventure' | 'modern-ios'

interface ThemeContextType {
    theme: Theme
    setTheme: (theme: Theme) => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
    // Default to 'default' (App Standard)
    const [theme, setTheme] = useState<Theme>('default')

    // Optional: Persist to localStorage
    useEffect(() => {
        const saved = localStorage.getItem('app-theme') as Theme
        if (saved) setTheme(saved)
    }, [])

    useEffect(() => {
        localStorage.setItem('app-theme', theme)

        // Apply global CSS variables if needed in the future
        // For now, we act as a state holder for components to react to
        const root = document.documentElement
        root.dataset.theme = theme
    }, [theme])

    return (
        <ThemeContext.Provider value={{ theme, setTheme }}>
            {children}
        </ThemeContext.Provider>
    )
}

export function useTheme() {
    const context = useContext(ThemeContext)
    if (context === undefined) {
        throw new Error('useTheme must be used within a ThemeProvider')
    }
    return context
}
