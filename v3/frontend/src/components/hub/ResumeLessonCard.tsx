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
        <div style={{
            background: 'linear-gradient(135deg, rgba(176, 0, 255, 0.1), rgba(0, 0, 0, 0))',
            border: '1px solid rgba(176, 0, 255, 0.3)',
            borderRadius: '20px',
            padding: '24px',
            marginBottom: '32px',
            position: 'relative',
            overflow: 'hidden'
        }}>
            <div style={{
                position: 'absolute',
                top: 0,
                right: 0,
                width: '150px',
                height: '150px',
                background: 'radial-gradient(circle, rgba(176,0,255,0.2) 0%, rgba(0,0,0,0) 70%)',
                pointerEvents: 'none'
            }} />

            <div style={{ position: 'relative', zIndex: 1, display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '20px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                    <div style={{
                        width: '56px',
                        height: '56px',
                        borderRadius: '16px',
                        background: '#b000ff',
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
                            color: '#b000ff',
                            marginBottom: '4px'
                        }}>
                            Kontynuuj naukę
                        </div>
                        <h2 style={{ fontSize: '20px', fontWeight: 700, marginBottom: '4px' }}>
                            {lesson.title}
                        </h2>
                        <p style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.6)' }}>
                            Ostatnio przerabiana karta #{lesson.progress_index + 1}
                        </p>
                    </div>
                </div>

                <button
                    onClick={() => router.push(`/lessons/${lesson.lesson_id}`)}
                    style={{
                        padding: '12px 24px',
                        background: 'white',
                        color: 'black',
                        border: 'none',
                        borderRadius: '12px',
                        fontWeight: 700,
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        transition: 'transform 0.2s'
                    }}
                    onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.05)'}
                    onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}
                >
                    Wznów
                    <ArrowRight size={18} />
                </button>
            </div>
        </div>
    )
}
