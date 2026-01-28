'use client'
import { useTheme } from '@/contexts/ThemeContext'
import { useEffect, useState } from 'react'
import { Ghost, Skull } from 'lucide-react'

export default function HalloweenOverlay() {
    const { theme } = useTheme()
    const [mounted, setMounted] = useState(false)

    useEffect(() => {
        setMounted(true)
    }, [])

    if (!mounted || theme !== 'halloween') return null

    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100vw',
            height: '100vh',
            pointerEvents: 'none',
            zIndex: 9999,
            overflow: 'hidden'
        }}>
            {/* Flying Ghosts */}
            <div className="ghost-float" style={{ position: 'absolute', top: '20%', left: '-10%', animationDelay: '0s' }}>
                <Ghost size={64} color="rgba(255,255,255,0.4)" />
            </div>
            <div className="ghost-float" style={{ position: 'absolute', top: '60%', left: '-10%', animationDelay: '5s', animationDuration: '15s' }}>
                <Ghost size={48} color="rgba(255,255,255,0.3)" />
            </div>
            <div className="ghost-float-reverse" style={{ position: 'absolute', top: '40%', right: '-10%', animationDelay: '2s', animationDuration: '18s' }}>
                <Ghost size={56} color="rgba(255,255,255,0.35)" />
            </div>

            {/* Random Skulls */}
            <div className="skull-bounce" style={{ position: 'absolute', bottom: '10%', left: '15%' }}>
                <Skull size={32} color="rgba(255, 100, 0, 0.6)" />
            </div>
            <div className="skull-bounce" style={{ position: 'absolute', bottom: '20%', right: '25%', animationDelay: '1s' }}>
                <Skull size={40} color="rgba(255, 0, 100, 0.5)" />
            </div>

            {/* Spooky Vignette */}
            <div style={{
                position: 'absolute',
                inset: 0,
                background: 'radial-gradient(circle, transparent 60%, rgba(20,0,0,0.8) 100%)',
                mixBlendMode: 'multiply'
            }} />
        </div>
    )
}
