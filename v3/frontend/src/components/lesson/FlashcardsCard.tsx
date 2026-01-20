'use client'

import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { RotateCw } from 'lucide-react'

interface FlashcardItem {
    front: string
    back: string
}

interface FlashcardsCardProps {
    title: string
    cards: FlashcardItem[]
}

export default function FlashcardsCard({ title, cards }: FlashcardsCardProps) {
    const [flippedStates, setFlippedStates] = useState<boolean[]>(new Array(cards.length).fill(false));

    const handleFlip = (index: number) => {
        const newStates = [...flippedStates];
        newStates[index] = !newStates[index];
        setFlippedStates(newStates);
    }

    return (
        <div style={{
            maxWidth: '900px',
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            gap: '24px'
        }}>
            {/* Type Badge */}
            <div style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                fontSize: '11px',
                textTransform: 'uppercase',
                letterSpacing: '1px',
                color: '#b000ff',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(176, 0, 255, 0.1)',
                border: '1px solid rgba(176, 0, 255, 0.2)',
                borderRadius: '20px',
                width: 'fit-content'
            }}>
                FLASHCARDS
            </div>

            <div style={{
                background: 'rgba(20, 20, 35, 0.6)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '20px',
                padding: '40px',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)'
            }}>
                <h2 style={{
                    fontSize: '28px',
                    fontWeight: 700,
                    marginBottom: '40px',
                    textAlign: 'center',
                    background: 'linear-gradient(135deg, #b000ff, #00d4ff)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent'
                }}>
                    {title}
                </h2>

                <div style={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    gap: '30px',
                    justifyContent: 'center',
                    perspective: '1000px'
                }}>
                    {cards.map((card, index) => (
                        <div
                            key={index}
                            onClick={() => handleFlip(index)}
                            style={{
                                height: '300px',
                                width: 'calc(50% - 15px)', // Precise width for 2 columns with 30px gap
                                minWidth: '280px',
                                cursor: 'pointer',
                                position: 'relative',
                                boxSizing: 'border-box'
                            }}
                        >
                            <div style={{
                                position: 'relative',
                                width: '100%',
                                height: '100%',
                                transition: 'transform 0.6s',
                                transformStyle: 'preserve-3d',
                                transform: flippedStates[index] ? 'rotateY(180deg)' : 'rotateY(0deg)'
                            }}>
                                {/* Front */}
                                <div style={{
                                    position: 'absolute',
                                    width: '100%',
                                    height: '100%',
                                    backfaceVisibility: 'hidden',
                                    WebkitBackfaceVisibility: 'hidden',
                                    background: 'rgba(255, 255, 255, 0.05)', // Reverted to lighter glass
                                    border: '1px solid rgba(255, 255, 255, 0.1)',
                                    borderRadius: '16px',
                                    padding: '30px',
                                    display: 'flex',
                                    flexDirection: 'column',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    textAlign: 'center',
                                    transform: 'rotateY(0deg)', // Explicit transform to enforce 3D context
                                    zIndex: 2,
                                    boxSizing: 'border-box'
                                }}>
                                    <div style={{
                                        marginBottom: '20px',
                                        color: '#b000ff'
                                    }}>
                                        <RotateCw size={32} />
                                    </div>
                                    <div style={{
                                        fontSize: '20px',
                                        fontWeight: 600,
                                        color: '#fff'
                                    }}>
                                        {card.front}
                                    </div>
                                    <div style={{
                                        marginTop: 'auto',
                                        fontSize: '12px',
                                        color: 'rgba(255,255,255,0.4)',
                                        textTransform: 'uppercase',
                                        letterSpacing: '1px'
                                    }}>
                                        Kliknij by obrócić
                                    </div>
                                </div>

                                {/* Back */}
                                <div style={{
                                    position: 'absolute',
                                    width: '100%',
                                    height: '100%',
                                    backfaceVisibility: 'hidden',
                                    WebkitBackfaceVisibility: 'hidden',
                                    transform: 'rotateY(180deg)',
                                    background: 'linear-gradient(135deg, rgba(176, 0, 255, 0.1), rgba(0, 212, 255, 0.1))',
                                    border: '1px solid rgba(176, 0, 255, 0.3)',
                                    borderRadius: '16px',
                                    padding: '30px',
                                    display: 'flex',
                                    flexDirection: 'column',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    textAlign: 'center',
                                    zIndex: 2,
                                    boxSizing: 'border-box'
                                }}>
                                    <div style={{
                                        fontSize: '16px',
                                        lineHeight: '1.6',
                                        color: '#fff'
                                    }}>
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                            {card.back}
                                        </ReactMarkdown>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}
