'use client'

import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface TimelineItem {
    year: string
    title: string
    description: string
    icon: string
}

interface TimelineCardProps {
    title: string
    data: {
        items: TimelineItem[]
    }
}

export default function TimelineCard({ title, data }: TimelineCardProps) {
    return (
        <div style={{
            maxWidth: '1000px',
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            gap: '24px',
            boxSizing: 'border-box'
        }}>
            {/* Main Card */}
            <div style={{
                background: 'rgba(20, 20, 35, 0.6)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '20px',
                padding: '40px',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
                boxSizing: 'border-box',
                position: 'relative'
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
                    color: '#ff8800',
                    fontWeight: 600,
                    padding: '6px 12px',
                    background: 'rgba(255, 136, 0, 0.1)',
                    border: '1px solid rgba(255, 136, 0, 0.2)',
                    borderRadius: '20px'
                }}>
                    TIMELINE
                </div>
                <h2 style={{
                    fontSize: '28px',
                    fontWeight: 700,
                    marginBottom: '60px',
                    background: 'linear-gradient(135deg, #ff8800, #ffd700)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    textAlign: 'center'
                }}>
                    {title}
                </h2>

                <div style={{ position: 'relative', padding: '10px 0' }}>
                    {/* Vertical Center Line */}
                    <div style={{
                        position: 'absolute',
                        left: '50%',
                        top: 0,
                        bottom: 0,
                        width: '2px',
                        background: 'linear-gradient(180deg, #ff8800, #ffd700)',
                        transform: 'translateX(-50%)',
                        opacity: 0.3
                    }} />

                    {data.items.map((item, index) => {
                        const isLeft = index % 2 === 0;
                        return (
                            <div key={index} style={{
                                display: 'grid',
                                gridTemplateColumns: '1fr 1fr',
                                width: '100%',
                                marginBottom: '40px',
                                position: 'relative',
                                alignItems: 'center' // Align content vertically with marker
                            }}>
                                {/* Content Box */}
                                <div style={{
                                    gridColumn: isLeft ? '1' : '2',
                                    paddingRight: isLeft ? '50px' : '0',
                                    paddingLeft: isLeft ? '0' : '50px',
                                    justifySelf: isLeft ? 'end' : 'start',
                                    textAlign: isLeft ? 'right' : 'left',
                                    width: '100%', // Take full width of the cell minus padding
                                    boxSizing: 'border-box'
                                }}>
                                    <div style={{
                                        background: 'rgba(255, 255, 255, 0.03)',
                                        border: '1px solid rgba(255, 255, 255, 0.1)',
                                        borderRadius: '16px',
                                        padding: '24px',
                                        transition: 'all 0.3s ease',
                                        display: 'inline-block', // allows box to shrink to content if needed, but width 100 on parent usually expands it
                                        width: '100%',
                                        boxSizing: 'border-box'
                                    }}
                                        onMouseOver={(e) => {
                                            e.currentTarget.style.background = 'rgba(255, 136, 0, 0.1)';
                                            e.currentTarget.style.borderColor = 'rgba(255, 136, 0, 0.3)';
                                            e.currentTarget.style.transform = 'scale(1.02)';
                                        }}
                                        onMouseOut={(e) => {
                                            e.currentTarget.style.background = 'rgba(255, 255, 255, 0.03)';
                                            e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)';
                                            e.currentTarget.style.transform = 'scale(1)';
                                        }}
                                    >
                                        <div style={{
                                            fontWeight: 600,
                                            fontSize: '18px',
                                            marginBottom: '8px',
                                            color: '#ff8800'
                                        }}>
                                            {item.title}
                                        </div>
                                        <div style={{
                                            fontSize: '14px',
                                            color: 'rgba(255, 255, 255, 0.7)',
                                            lineHeight: '1.6'
                                        }}>
                                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                                {item.description}
                                            </ReactMarkdown>
                                        </div>
                                    </div>
                                </div>

                                {/* Circle Marker - Absolute Center */}
                                <div style={{
                                    position: 'absolute',
                                    left: '50%',
                                    top: '50%',
                                    transform: 'translate(-50%, -50%)', // Center perfectly on the row
                                    width: '60px',
                                    height: '60px',
                                    background: 'linear-gradient(135deg, #ff8800, #ffd700)',
                                    borderRadius: '50%',
                                    display: 'flex',
                                    flexDirection: 'column',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    fontWeight: 700,
                                    fontSize: '14px',
                                    color: '#000',
                                    boxShadow: '0 0 20px rgba(255, 136, 0, 0.4)',
                                    zIndex: 2,
                                    lineHeight: '1.2'
                                }}>
                                    <span style={{ fontSize: '10px', opacity: 0.8, textTransform: 'uppercase' }}>Rok</span>
                                    {item.year}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    )
}
