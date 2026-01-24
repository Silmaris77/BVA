import React, { useEffect, useState } from 'react'

interface DrillTimerProps {
    durationSeconds: number
    onTimeUp: () => void
    isActive: boolean
}

export default function DrillTimer({ durationSeconds, onTimeUp, isActive }: DrillTimerProps) {
    const [timeLeft, setTimeLeft] = useState(durationSeconds)

    // Reset timer when duration changes
    useEffect(() => {
        setTimeLeft(durationSeconds)
    }, [durationSeconds])

    useEffect(() => {
        if (!isActive || timeLeft <= 0) return

        const interval = setInterval(() => {
            setTimeLeft((prev) => {
                if (prev <= 1) {
                    clearInterval(interval)
                    onTimeUp()
                    return 0
                }
                return prev - 1
            })
        }, 1000)

        return () => clearInterval(interval)
    }, [isActive, timeLeft, onTimeUp])

    // Calculate percentage for progress bar
    const percentage = (timeLeft / durationSeconds) * 100

    // Color logic: Green > 50%, Orange > 20%, Red <= 20%
    const getColor = () => {
        if (percentage > 50) return '#00ff88'
        if (percentage > 20) return '#ffd700'
        return '#ff4444'
    }

    return (
        <div style={{ width: '100%', marginBottom: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '14px', fontWeight: 600 }}>
                <span style={{ color: 'rgba(255,255,255,0.6)' }}>Czas</span>
                <span style={{ color: getColor() }}>{timeLeft}s</span>
            </div>
            <div style={{ width: '100%', height: '8px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{
                    width: `${percentage}%`,
                    height: '100%',
                    background: getColor(),
                    transition: 'width 1s linear, background 0.3s'
                }}></div>
            </div>
        </div>
    )
}
