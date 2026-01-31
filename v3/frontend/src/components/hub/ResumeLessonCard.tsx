'use client'

import { Play, ArrowRight, BookOpen } from 'lucide-react'
import { useRouter } from 'next/navigation'

interface ResumeLessonCardProps {
    lesson: {
        lesson_id: string
        title: string
        progress_index: number
    } | null
}

export default function ResumeLessonCard({ lesson }: ResumeLessonCardProps) {
    const router = useRouter()

    if (!lesson) return null

    return (
        <div 
            className="theme-card-accent"
            style={{
                background: 'linear-gradient(135deg, var(--t-card-bg), transparent)',
                borderColor: 'var(--t-accent-secondary)',
                marginBottom: '32px',
                position: 'relative',
                overflow: 'hidden'
            }}
        >
            {/* Glow Effect */}
            <div style={{
                position: 'absolute',
                top: 0,
                right: 0,
                width: '150px',
                height: '150px',
                background: 'radial-gradient(circle, rgba(176,0,255,0.2) 0%, transparent 70%)',
                pointerEvents: 'none'
            }} />

            <div style={{ 
                position: 'relative', 
                zIndex: 1, 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'space-between', 
                flexWrap: 'wrap', 
                gap: '20px' 
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                    <div style={{
                        width: '56px',
                        height: '56px',
                        borderRadius: '16px',
                        background: 'var(--t-accent-secondary)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        boxShadow: '0 8px 24px rgba(176, 0, 255, 0.4)'
                    }}>
                        <Play size={28} fill="white" color="white" style={{ marginLeft: '4px' }} />
                    </div>
                    <div>
                        <div style={{
                            fontSize: '12px',
                            textTransform: 'uppercase',
                            letterSpacing: '1px',
                            fontWeight: 700,
                            color: 'var(--t-accent-secondary)',
                            marginBottom: '4px'
                        }}>
                            Kontynuuj naukę
                        </div>
                        <h2 style={{ 
                            fontSize: '20px', 
                            fontWeight: 700, 
                            marginBottom: '4px',
                            color: 'var(--t-text)' 
                        }}>
                            {lesson.title}
                        </h2>
                        <p style={{ 
                            fontSize: '14px', 
                            color: 'var(--t-text-muted)' 
                        }}>
                            Ostatnio przerabiana karta #{lesson.progress_index + 1}
                        </p>
                    </div>
                </div>

                <button
                    className="theme-button"
                    onClick={() => router.push(`/lessons/${lesson.lesson_id}`)}
                    style={{
                        background: 'var(--t-text)',
                        color: 'var(--t-bg)'
                    }}
                >
                    Wznów
                    <ArrowRight size={18} />
                </button>
            </div>
        </div>
    )
}
