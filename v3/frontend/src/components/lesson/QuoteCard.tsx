'use client'

import { Quote } from 'lucide-react'

interface QuoteCardProps {
    text: string
    author: string
    role?: string
    image?: string
}

export default function QuoteCard({ text, author, role, image }: QuoteCardProps) {
    return (
        <div style={{
            maxWidth: '800px',
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            gap: '24px'
        }}>
            <div style={{
                background: 'rgba(20, 20, 35, 0.6)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                borderRadius: '24px',
                padding: '50px',
                position: 'relative',
                overflow: 'hidden',
                border: '1px solid rgba(255, 255, 255, 0.05)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                textAlign: 'center'
            }}>
                {/* Background Accent */}
                <div style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '8px',
                    height: '100%',
                    background: '#DA291C'
                }} />

                {/* Giant Quote Icon */}
                <div style={{
                    position: 'absolute',
                    top: '20px',
                    left: '30px',
                    opacity: 0.1,
                    transform: 'rotate(180deg)'
                }}>
                    <Quote size={120} color="#fff" />
                </div>

                {/* Content */}
                <div style={{
                    position: 'relative',
                    zIndex: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '30px'
                }}>
                    <Quote size={48} color="#DA291C" style={{ marginBottom: '10px' }} />

                    <blockquote style={{
                        fontSize: '28px',
                        lineHeight: '1.4',
                        fontWeight: 300,
                        fontStyle: 'italic',
                        color: '#fff',
                        margin: 0,
                        fontFamily: '"Outfit", sans-serif'
                    }}>
                        "{text}"
                    </blockquote>

                    <div style={{
                        width: '60px',
                        height: '2px',
                        background: 'rgba(255, 255, 255, 0.2)'
                    }} />

                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '20px'
                    }}>
                        {image && (
                            <div style={{
                                width: '60px',
                                height: '60px',
                                borderRadius: '50%',
                                overflow: 'hidden',
                                border: '2px solid rgba(218, 41, 28, 0.5)'
                            }}>
                                <img
                                    src={image}
                                    alt={author}
                                    style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                                />
                            </div>
                        )}
                        <div style={{ textAlign: image ? 'left' : 'center' }}>
                            <div style={{
                                fontSize: '20px',
                                fontWeight: 700,
                                color: '#fff'
                            }}>
                                {author}
                            </div>
                            {role && (
                                <div style={{
                                    fontSize: '14px',
                                    color: '#DA291C',
                                    fontWeight: 600,
                                    textTransform: 'uppercase',
                                    marginTop: '4px',
                                    letterSpacing: '1px'
                                }}>
                                    {role}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
