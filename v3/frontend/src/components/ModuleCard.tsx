'use client'

import { BookOpen, Clock, Trophy, ChevronRight, CheckCircle, Folder } from 'lucide-react'
import { getCategoryColor } from '@/lib/categories'

interface Lesson {
    lesson_id: string
    duration_minutes: number
    xp_reward: number
    status?: string
}

interface Module {
    id: string
    title: string
    description: string
    track: string
    display_order: number
}

interface ModuleCardProps {
    module: Module
    lessons: Lesson[]
    progress: Record<string, any>
    onClick: () => void
}

export default function ModuleCard({ module, lessons, progress, onClick }: ModuleCardProps) {
    // Calculate stats
    const totalLessons = lessons.length
    const completedLessons = lessons.filter(l => progress[l.lesson_id]?.status === 'completed').length
    const totalDuration = lessons.reduce((acc, l) => acc + l.duration_minutes, 0)
    const totalXP = lessons.reduce((acc, l) => acc + l.xp_reward, 0)

    const progressPercent = totalLessons > 0 ? Math.round((completedLessons / totalLessons) * 100) : 0
    const isCompleted = progressPercent === 100 && totalLessons > 0
    const status = isCompleted ? 'completed' : progressPercent > 0 ? 'in_progress' : 'not_started'

    const accentColor = '#ffd700' // Gold for modules

    const getStatusColor = () => {
        switch (status) {
            case 'completed': return '#00ff88'
            case 'in_progress': return '#00d4ff'
            default: return 'rgba(255, 255, 255, 0.6)'
        }
    }

    const getStatusLabel = () => {
        switch (status) {
            case 'completed': return '✓ Ukończony'
            case 'in_progress': return 'W trakcie'
            default: return 'Rozpocznij'
        }
    }

    return (
        <div
            onClick={onClick}
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
            {status !== 'not_started' && (
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
                    {status === 'completed' && <CheckCircle size={12} />}
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
                <Folder size={24} />
            </div>

            {/* Title */}
            <h3 style={{
                fontSize: '18px',
                fontWeight: 600,
                marginBottom: '8px',
                paddingRight: status !== 'not_started' ? '100px' : '0'
            }}>
                {module.title}
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
                {module.description}
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
                    {totalLessons} lekcji
                </span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Clock size={14} />
                    {(totalDuration / 60).toFixed(1)}h
                </span>
                <span style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                    color: '#ffd700'
                }}>
                    <Trophy size={14} />
                    +{totalXP} XP
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
                    width: `${progressPercent}%`,
                    background: `linear-gradient(90deg, ${accentColor}, #ff8e00)`,
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
                    {completedLessons}/{totalLessons} ukończonych
                </span>
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                    color: accentColor,
                    fontSize: '13px',
                    fontWeight: 600
                }}>
                    {status === 'not_started' ? 'Otwórz' : 'Kontynuuj'}
                    <ChevronRight size={16} />
                </div>
            </div>
        </div>
    )
}
