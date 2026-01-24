'use client'

import { Lightbulb } from 'lucide-react'

interface Tip {
    content: string
    category: string
    author?: string
}

interface DailyTipProps {
    tip: Tip | null
}

export default function DailyTip({ tip }: DailyTipProps) {
    if (!tip) return null

    return (
        <div style={{
            background: 'linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 0, 0, 0))',
            border: '1px solid rgba(0, 212, 255, 0.2)',
            borderRadius: '20px',
            padding: '24px',
            marginBottom: '24px'
        }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
                <div style={{
                    padding: '8px',
                    borderRadius: '8px',
                    background: 'rgba(0, 212, 255, 0.2)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center'
                }}>
                    <Lightbulb size={18} color="#00d4ff" />
                </div>
                <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#00d4ff' }}>Pigułka Wiedzy</h3>
            </div>

            <p style={{
                fontSize: '15px',
                lineHeight: '1.6',
                fontStyle: 'italic',
                marginBottom: '12px',
                color: 'white'
            }}>
                "{tip.content}"
            </p>

            {tip.author && (
                <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.5)', textAlign: 'right' }}>
                    — {tip.author}
                </div>
            )}
        </div>
    )
}
