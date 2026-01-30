'use client'
import { useTheme } from '@/contexts/ThemeContext'
import { useEffect, useState, useMemo } from 'react'
import { Ghost, Skull, Zap, Star } from 'lucide-react'

export default function EffectsOverlay() {
    const { theme } = useTheme()
    const [mounted, setMounted] = useState(false)
    const [trail, setTrail] = useState<{ x: number, y: number, id: number }[]>([])


    // Memoize snowflakes to prevent re-render jitter
    const snowflakes = useMemo(() => [...Array(50)].map((_, i) => ({
        id: i,
        size: Math.random() * 8 + 2,
        left: Math.random() * 100,
        duration: Math.random() * 15 + 15,
        delay: Math.random() * 5
    })), [])

    useEffect(() => {
        setMounted(true)

        const handleMouseMove = (e: MouseEvent) => {
            if (theme === 'chaos') {
                setTrail(prev => [...prev.slice(-20), { x: e.clientX, y: e.clientY, id: Date.now() + Math.random() }])
            }
        }

        // Winter Accumulation Logic Removed
        window.addEventListener('mousemove', handleMouseMove)
        return () => window.removeEventListener('mousemove', handleMouseMove)
    }, [theme])



    if (!mounted) return null

    // HALLOWEEN MODE 🎃
    if (theme === 'halloween') {
        return (
            <div style={{ position: 'fixed', inset: 0, pointerEvents: 'none', zIndex: 9999, overflow: 'hidden' }}>
                <div className="ghost-float" style={{ position: 'absolute', top: '20%', left: '-10%' }}><Ghost size={64} color="rgba(255,255,255,0.4)" /></div>
                <div className="ghost-float" style={{ position: 'absolute', top: '60%', left: '-10%', animationDelay: '5s', animationDuration: '15s' }}><Ghost size={48} color="rgba(255,255,255,0.3)" /></div>
                <div className="ghost-float-reverse" style={{ position: 'absolute', top: '40%', right: '-10%', animationDelay: '2s', animationDuration: '18s' }}><Ghost size={56} color="rgba(255,255,255,0.35)" /></div>
                <div className="skull-bounce" style={{ position: 'absolute', bottom: '10%', left: '15%' }}><Skull size={32} color="rgba(255, 100, 0, 0.6)" /></div>
                <div className="skull-bounce" style={{ position: 'absolute', bottom: '20%', right: '25%', animationDelay: '1s' }}><Skull size={40} color="rgba(255, 0, 100, 0.5)" /></div>
                <div style={{ position: 'absolute', inset: 0, background: 'radial-gradient(circle, transparent 60%, rgba(20,0,0,0.8) 100%)', mixBlendMode: 'multiply' }} />
            </div>
        )
    }

    // CHAOS MODE ⚡
    if (theme === 'chaos') {
        return (
            <div style={{ position: 'fixed', inset: 0, pointerEvents: 'none', zIndex: 9999, overflow: 'hidden' }}>
                {/* Mouse Trail */}
                {trail.map((t, i) => (
                    <div key={t.id} style={{
                        position: 'absolute',
                        left: t.x - 5,
                        top: t.y - 5,
                        width: '10px',
                        height: '10px',
                        background: i % 2 === 0 ? '#ff00ff' : '#00ffff',
                        opacity: (i / trail.length),
                        transform: `scale(${i / trail.length})`,
                        borderRadius: '50%'
                    }} />
                ))}

                {/* Floating Geometric Chaos */}
                <div className="chaos-spin" style={{ position: 'absolute', top: '10%', right: '10%', opacity: 0.5 }}>
                    <Zap size={120} color="#ccff00" strokeWidth={3} />
                </div>
                <div className="chaos-spin-reverse" style={{ position: 'absolute', bottom: '10%', left: '5%', opacity: 0.5 }}>
                    <Star size={80} color="#ff00ff" fill="transparent" strokeWidth={3} />
                </div>

                {/* Noise Overlay */}
                <div style={{
                    position: 'absolute',
                    inset: 0,
                    backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E")`,
                    mixBlendMode: 'overlay',
                    opacity: 0.2
                }} />
            </div>
        )
    }

    // WINTER MODE ❄️
    if (theme === 'winter') {
        return (
            <div style={{ position: 'fixed', inset: 0, pointerEvents: 'none', zIndex: 9999, overflow: 'hidden' }}>
                {/* Falling Snow CSS */}
                <style dangerouslySetInnerHTML={{
                    __html: `
                    @keyframes snowfall {
                        0% { transform: translateY(-10vh) translateX(0); opacity: 0; }
                        10% { opacity: 1; }
                        25% { transform: translateY(20vh) translateX(15px); }
                        50% { transform: translateY(50vh) translateX(-15px); }
                        75% { transform: translateY(80vh) translateX(15px); }
                        100% { transform: translateY(110vh) translateX(0); opacity: 0.3; }
                    }
                    .snowflake {
                        position: absolute;
                        background: white;
                        border-radius: 50%;
                        opacity: 0.8;
                        animation: snowfall linear infinite;
                    }
                `}} />

                {/* Generating Snowflakes (Memoized) */}
                {snowflakes.map((flake) => (
                    <div key={flake.id} className="snowflake" style={{
                        width: flake.size + 'px',
                        height: flake.size + 'px',
                        left: flake.left + 'vw',
                        animationDuration: flake.duration + 's',
                        animationDelay: flake.delay + 's',
                        filter: 'blur(1px)'
                    }} />
                ))}

                {/* Snowman (Fixed Stacking) */}
                <div style={{ position: 'absolute', bottom: '20px', right: '50px', filter: 'drop-shadow(0 10px 10px rgba(0,0,0,0.1))' }}>
                    {/* Head */}
                    <div style={{ width: '40px', height: '40px', background: 'white', borderRadius: '50%', margin: '0 auto', position: 'relative', zIndex: 3, marginBottom: '-10px' }}>
                        {/* Eyes */}
                        <div style={{ width: '4px', height: '4px', background: 'black', borderRadius: '50%', position: 'absolute', top: '15px', left: '12px' }}></div>
                        <div style={{ width: '4px', height: '4px', background: 'black', borderRadius: '50%', position: 'absolute', top: '15px', left: '24px' }}></div>
                        {/* Nose */}
                        <div style={{ width: '0', height: '0', borderLeft: '4px solid transparent', borderRight: '4px solid transparent', borderBottom: '12px solid orange', position: 'absolute', top: '18px', left: '16px', transform: 'rotate(90deg)' }}></div>
                    </div>
                    {/* Middle */}
                    <div style={{ width: '60px', height: '60px', background: 'white', borderRadius: '50%', margin: '0 auto', marginBottom: '-15px', position: 'relative', zIndex: 2 }}>
                        {/* Buttons */}
                        <div style={{ width: '6px', height: '6px', background: '#333', borderRadius: '50%', position: 'absolute', top: '25px', left: '27px' }}></div>
                        <div style={{ width: '6px', height: '6px', background: '#333', borderRadius: '50%', position: 'absolute', top: '35px', left: '27px' }}></div>
                    </div>
                    {/* Body */}
                    <div style={{ width: '80px', height: '80px', background: 'white', borderRadius: '50%', position: 'relative', zIndex: 1 }}></div>
                </div>


            </div>
        )
    }

    // MOONSHOT MODE 🚀 (Candlesticks)
    if (theme === 'moonshot') {
        const candles = [...Array(30)].map((_, i) => ({
            id: i,
            left: Math.random() * 100,
            duration: Math.random() * 8 + 4,
            delay: Math.random() * 5,
            isGreen: Math.random() > 0.4,
            height: Math.random() * 20 + 10,
            width: Math.random() * 3 + 2
        }))

        return (
            <div style={{ position: 'fixed', inset: 0, pointerEvents: 'none', zIndex: 9999, overflow: 'hidden' }}>
                <style dangerouslySetInnerHTML={{
                    __html: `
                    @keyframes candleFall {
                        0% { transform: translateY(-100px); opacity: 0; }
                        10% { opacity: 0.6; }
                        90% { opacity: 0.6; }
                        100% { transform: translateY(110vh); opacity: 0; }
                    }
                    .candle {
                        position: absolute;
                        animation: candleFall linear infinite;
                    }
                `}} />
                {candles.map((c) => (
                    <div key={c.id} className="candle" style={{
                        left: c.left + 'vw',
                        width: c.width + 'px',
                        height: c.height + 'px',
                        background: c.isGreen ? '#00ff9d' : '#ff4d4d',
                        boxShadow: `0 0 8px ${c.isGreen ? '#00ff9d' : '#ff4d4d'}`,
                        animationDuration: c.duration + 's',
                        animationDelay: c.delay + 's'
                    }}>
                        {/* Wick */}
                        <div style={{
                            position: 'absolute',
                            top: '-5px',
                            left: '50%',
                            width: '1px',
                            height: c.height + 10 + 'px',
                            background: 'currentColor',
                            transform: 'translateX(-50%)',
                            opacity: 0.5
                        }} />
                    </div>
                ))}
            </div>
        )
    }

    return null
}
