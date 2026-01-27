'use client'

import MathRenderer from './math/MathRenderer'
import { Sparkles, Scroll } from 'lucide-react'

interface CuriosityCardProps {
    title: string
    content: string
}

export default function CuriosityCard({ title, content }: CuriosityCardProps) {
    return (
        <div style={{
            maxWidth: '900px',
            width: '100%'
        }}>
            {/* Glass Card Container - Gold/Amber Theme */}
            <div style={{
                position: 'relative',
                background: 'linear-gradient(145deg, rgba(40, 30, 20, 0.8), rgba(20, 20, 35, 0.6))',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 190, 0, 0.3)',
                borderRadius: '20px',
                padding: '40px',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
                borderLeft: '4px solid #ffbe00',
                overflow: 'hidden' // Ensure decoration doesn't spill out
            }}>
                {/* Type Badge - Top Left Corner */}
                <div style={{
                    position: 'absolute',
                    top: '20px',
                    left: '20px',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '6px',
                    fontSize: '11px',
                    textTransform: 'uppercase',
                    letterSpacing: '1px',
                    color: '#ffbe00',
                    fontWeight: 600,
                    padding: '6px 12px',
                    background: 'rgba(255, 190, 0, 0.1)',
                    border: '1px solid rgba(255, 190, 0, 0.25)',
                    borderRadius: '20px',
                    zIndex: 2
                }}>
                    <Sparkles size={12} />
                    CIEKAWOSTKA
                </div>

                {/* Decorative Icon Background */}
                <div style={{
                    position: 'absolute',
                    top: '-15px',
                    right: '20px',
                    opacity: 0.1,
                    transform: 'rotate(15deg)',
                    pointerEvents: 'none',
                    zIndex: 1
                }}>
                    <Scroll size={140} color="#ffbe00" />
                </div>

                {/* Title */}
                <div style={{
                    marginTop: '20px',
                    marginBottom: '24px',
                    position: 'relative',
                    zIndex: 2,
                    textAlign: 'center'
                }}>
                    <h2 style={{
                        fontSize: '28px',
                        fontWeight: 700,
                        background: 'linear-gradient(135deg, #ffbe00, #fff)',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        margin: 0
                    }}>
                        {title}
                    </h2>
                </div>

                {/* Content */}
                <div style={{
                    fontSize: '17px',
                    lineHeight: '1.8',
                    color: 'rgba(255, 235, 200, 0.95)',
                    background: 'rgba(0, 0, 0, 0.2)',
                    padding: '24px',
                    borderRadius: '12px',
                    border: '1px solid rgba(255, 190, 0, 0.1)',
                    position: 'relative',
                    zIndex: 2
                }}>
                    <MathRenderer content={content.replace(/\\n/g, '\n')} />
                </div>
            </div>
        </div>
    )
}
