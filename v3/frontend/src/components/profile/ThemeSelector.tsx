'use client'
import { useTheme, Theme } from '@/contexts/ThemeContext'
import { Check, Layout } from 'lucide-react'

export default function ThemeSelector() {
    const { theme, setTheme } = useTheme()

    const themes: { id: Theme; name: string; color: string }[] = [
        { id: 'default', name: 'Standardowy (BVA)', color: '#4f46e5' },
        { id: 'cyber', name: 'Cyberpunk', color: '#00d4ff' },
        { id: 'slate', name: 'Slate Focus', color: '#64748b' },
        { id: 'light', name: 'Jasny (High Contrast)', color: '#f8fafc' },
        { id: 'halloween', name: '🎃 HALLOWEEN', color: '#ff6600' },
        { id: 'chaos', name: '⚡ GEN Z CHAOS', color: '#ccff00' },
        { id: 'drunk', name: '🥴 DRUNK MODE', color: '#ff00aa' },
        { id: 'winter', name: '❄️ WINTER', color: '#a5f3fc' },
        { id: 'milwaukee', name: '🔴 HEAVY DUTY', color: '#db0000' },
        { id: 'executive', name: '💼 EXECUTIVE', color: '#d4af37' },
        { id: 'diplomat', name: '🏛️ SENATOR', color: '#722F37' },
        { id: 'brainventure', name: '🧠 BRAINVENTURE', color: '#B10A4A' },
        { id: 'modern-ios', name: '📱 MODERN iOS', color: '#000000' },
    ]

    return (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '12px' }}>
            {themes.map((t) => (
                <button
                    key={t.id}
                    onClick={() => setTheme(t.id)}
                    style={{
                        position: 'relative',
                        padding: '16px',
                        borderRadius: '16px',
                        background: theme === t.id
                            ? 'rgba(255, 255, 255, 0.1)'
                            : 'rgba(255, 255, 255, 0.03)',
                        border: theme === t.id
                            ? `2px solid ${t.color}`
                            : '2px solid transparent', // Fixed height border
                        cursor: 'pointer',
                        textAlign: 'left',
                        transition: 'all 0.2s',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '8px'
                    }}
                >
                    <div style={{
                        width: '24px',
                        height: '24px',
                        borderRadius: '50%',
                        background: t.color,
                        boxShadow: theme === t.id ? `0 0 10px ${t.color}` : 'none'
                    }} />

                    <span style={{
                        fontSize: '13px',
                        fontWeight: 600,
                        color: theme === t.id ? 'white' : 'rgba(255,255,255,0.6)'
                    }}>
                        {t.name}
                    </span>

                    {theme === t.id && (
                        <div style={{
                            position: 'absolute',
                            top: '12px',
                            right: '12px',
                            color: t.color
                        }}>
                            <Check size={16} />
                        </div>
                    )}
                </button>
            ))}
        </div>
    )
}
