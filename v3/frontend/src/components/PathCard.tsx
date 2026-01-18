'use client'

import { useRouter } from 'next/navigation'
import { BookOpen, Clock, Trophy, ChevronRight, CheckCircle } from 'lucide-react'
import { getCategoryColor } from '@/lib/categories'

interface LearningPath {
    id: string
    path_slug: string
    title: string
    description: string
    estimated_hours: number
    difficulty: 'beginner' | 'intermediate' | 'advanced'
    total_xp_reward: number
    lesson_count: number
    completed_lessons: number
    progress_percent: number
    status: 'not_started' | 'in_progress' | 'completed'
}

interface PathCardProps {
    path: LearningPath
}

export default function PathCard({ path }: PathCardProps) {
    const router = useRouter()

    const difficultyLabels = {
        beginner: 'Początkujący',
        intermediate: 'Średniozaawansowany',
        advanced: 'Zaawansowany'
    }

    const getStatusColor = () => {
        switch (path.status) {
            case 'completed': return '#00ff88'
            case 'in_progress': return '#00d4ff'
            default: return 'rgba(255, 255, 255, 0.6)'
        }
    }

    const getStatusLabel = () => {
        switch (path.status) {
            case 'completed': return '✓ Ukończona'
            case 'in_progress': return 'W trakcie'
            default: return 'Rozpocznij'
        }
    }

    const accentColor = '#b000ff' // Purple for paths

    return (
        <div
            onClick={() => router.push(`/paths/${path.path_slug}`)}
            style={{
                background: 'rgba(20, 20, 35, 0.6)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.08)',
                borderRadius: '16px',
                padding: '20px',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                position: 'relative',
                overflow: 'hidden',
                minWidth: '300px',
                flex: '1 1 300px',
                maxWidth: '400px'
            }}
            onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = accentColor
                e.currentTarget.style.transform = 'translateY(-4px)'
                e.currentTarget.style.boxShadow = `0 12px 40px ${accentColor}33`
            }}
            onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.08)'
                e.currentTarget.style.transform = 'translateY(0)'
                e.currentTarget.style.boxShadow = 'none'
            }}
        >
            {/* Status Badge */}
            {path.status !== 'not_started' && (
                <div style={{
                    position: 'absolute',
                    top: '16px',
                    right: '16px',
                    padding: '4px 12px',
                    background: `${getStatusColor()}20`,
                    border: `1px solid ${getStatusColor()}`,
                    borderRadius: '20px',
                    fontSize: '11px',
                    fontWeight: 600,
                    color: getStatusColor(),
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                }}>
                    {path.status === 'completed' && <CheckCircle size={12} />}
                    {getStatusLabel()}
                </div>
            )}

            {/* Icon */}
            <div style={{
                width: '48px',
                height: '48px',
                background: `${accentColor}20`,
                borderRadius: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '16px',
                color: accentColor
            }}>
                <Trophy size={24} />
            </div>

            {/* Title */}
            <h3 style={{
                fontSize: '18px',
                fontWeight: 600,
                marginBottom: '8px',
                paddingRight: path.status !== 'not_started' ? '100px' : '0'
            }}>
                {path.title}
            </h3>

            {/* Description */}
            <p style={{
                fontSize: '13px',
                color: 'rgba(255, 255, 255, 0.6)',
                lineHeight: 1.5,
                marginBottom: '16px',
                display: '-webkit-box',
                WebkitLineClamp: 2,
                WebkitBoxOrient: 'vertical',
                overflow: 'hidden'
            }}>
                {path.description}
            </p>

            {/* Meta Info */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '16px',
                fontSize: '12px',
                color: 'rgba(255, 255, 255, 0.5)',
                marginBottom: '16px'
            }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <BookOpen size={14} />
                    {path.lesson_count} lekcji
                </span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Clock size={14} />
                    {path.estimated_hours}h
                </span>
                <span style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                    color: '#ffd700'
                }}>
                    <Trophy size={14} />
                    +{path.total_xp_reward} XP
                </span>
            </div>

            {/* Progress Bar */}
            <div style={{
                height: '6px',
                background: 'rgba(255, 255, 255, 0.1)',
                borderRadius: '3px',
                overflow: 'hidden',
                marginBottom: '12px'
            }}>
                <div style={{
                    height: '100%',
                    width: `${path.progress_percent}%`,
                    background: `linear-gradient(90deg, ${accentColor}, #00d4ff)`,
                    borderRadius: '3px',
                    transition: 'width 0.4s ease'
                }} />
            </div>

            {/* Footer */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
            }}>
                <span style={{
                    fontSize: '12px',
                    color: 'rgba(255, 255, 255, 0.6)'
                }}>
                    {path.completed_lessons}/{path.lesson_count} ukończonych
                </span>
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                    color: accentColor,
                    fontSize: '13px',
                    fontWeight: 600
                }}>
                    {path.status === 'not_started' ? 'Rozpocznij' : 'Kontynuuj'}
                    <ChevronRight size={16} />
                </div>
            </div>
        </div>
    )
}
