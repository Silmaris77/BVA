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
        <div 
            className="theme-card"
            style={{
                background: 'linear-gradient(135deg, var(--t-card-bg), transparent)',
                borderColor: 'var(--t-border-accent)',
                marginBottom: '24px'
            }}
        >
            <div className="theme-section-header">
                <div 
                    className="theme-icon-container"
                    style={{ background: 'rgba(0, 212, 255, 0.2)' }}
                >
                    <Lightbulb size={18} style={{ color: 'var(--t-accent)' }} />
                </div>
                <h3 className="theme-section-title">Pigułka Wiedzy</h3>
            </div>

            <p style={{
                fontSize: '15px',
                lineHeight: '1.6',
                fontStyle: 'italic',
                marginBottom: '12px',
                color: 'var(--t-text)'
            }}>
                "{tip.content}"
            </p>

            {tip.author && (
                <div style={{ 
                    fontSize: '12px', 
                    color: 'var(--t-text-muted)', 
                    textAlign: 'right' 
                }}>
                    — {tip.author}
                </div>
            )}
        </div>
    )
}
