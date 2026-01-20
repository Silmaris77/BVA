'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import {
    BookOpen, ArrowLeft, Plus, Trash2, Edit3, Save, X,
    AlertTriangle, Check, Clock, Zap, ChevronDown, ChevronUp
} from 'lucide-react'

interface Lesson {
    id: string
    lesson_id: string
    title: string
    description: string
    duration_minutes: number
    xp_reward: number
    difficulty: string
    content: any
    created_at: string
    updated_at: string
}

export default function AdminLessonsPage() {
    const { user, loading: authLoading } = useAuth()
    const router = useRouter()
    const [lessons, setLessons] = useState<Lesson[]>([])
    const [loading, setLoading] = useState(true)
    const [isAdmin, setIsAdmin] = useState(false)
    const [editingId, setEditingId] = useState<string | null>(null)
    const [expandedId, setExpandedId] = useState<string | null>(null)
    const [showCreateForm, setShowCreateForm] = useState(false)
    const [saving, setSaving] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [success, setSuccess] = useState<string | null>(null)

    // Form state
    const [formData, setFormData] = useState({
        lesson_id: '',
        title: '',
        description: '',
        duration_minutes: 10,
        xp_reward: 150,
        difficulty: 'beginner',
        content: '{"cards": []}'
    })

    useEffect(() => {
        async function loadLessons() {
            if (!user) return

            try {
                const response = await fetch('/api/admin/lessons')
                if (response.ok) {
                    setIsAdmin(true)
                    const data = await response.json()
                    setLessons(data.lessons || [])
                } else {
                    setIsAdmin(false)
                }
            } catch (error) {
                console.error('Error loading lessons:', error)
                setIsAdmin(false)
            } finally {
                setLoading(false)
            }
        }

        if (!authLoading) {
            loadLessons()
        }
    }, [user, authLoading])

    const handleCreate = async () => {
        setSaving(true)
        setError(null)

        try {
            let contentJson
            try {
                contentJson = JSON.parse(formData.content)
            } catch {
                setError('Nieprawidłowy format JSON dla content')
                setSaving(false)
                return
            }

            const response = await fetch('/api/admin/lessons', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    ...formData,
                    content: contentJson
                })
            })

            if (response.ok) {
                const data = await response.json()
                setLessons([data.lesson, ...lessons])
                setShowCreateForm(false)
                setFormData({
                    lesson_id: '',
                    title: '',
                    description: '',
                    duration_minutes: 10,
                    xp_reward: 150,
                    difficulty: 'beginner',
                    content: '{"cards": []}'
                })
                setSuccess('Lekcja utworzona!')
                setTimeout(() => setSuccess(null), 3000)
            } else {
                const data = await response.json()
                setError(data.error || 'Błąd podczas tworzenia lekcji')
            }
        } catch (error) {
            setError('Błąd połączenia z serwerem')
        } finally {
            setSaving(false)
        }
    }

    const handleUpdate = async (lesson: Lesson) => {
        setSaving(true)
        setError(null)

        try {
            const response = await fetch('/api/admin/lessons', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(lesson)
            })

            if (response.ok) {
                const data = await response.json()
                setLessons(lessons.map(l => l.id === lesson.id ? data.lesson : l))
                setEditingId(null)
                setSuccess('Lekcja zaktualizowana!')
                setTimeout(() => setSuccess(null), 3000)
            } else {
                const data = await response.json()
                setError(data.error || 'Błąd podczas aktualizacji')
            }
        } catch (error) {
            setError('Błąd połączenia z serwerem')
        } finally {
            setSaving(false)
        }
    }

    const handleDelete = async (id: string) => {
        if (!confirm('Czy na pewno chcesz usunąć tę lekcję?')) return

        try {
            const response = await fetch(`/api/admin/lessons?id=${id}`, {
                method: 'DELETE'
            })

            if (response.ok) {
                setLessons(lessons.filter(l => l.id !== id))
                setSuccess('Lekcja usunięta!')
                setTimeout(() => setSuccess(null), 3000)
            } else {
                const data = await response.json()
                setError(data.error || 'Błąd podczas usuwania')
            }
        } catch (error) {
            setError('Błąd połączenia z serwerem')
        }
    }

    // Redirect to admin if not authenticated/authorized
    useEffect(() => {
        if (!authLoading && !loading && (!user || !isAdmin)) {
            router.push('/admin')
        }
    }, [user, isAdmin, authLoading, loading, router])

    if (authLoading || loading) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'rgba(255, 255, 255, 0.6)'
            }}>
                Ładowanie...
            </div>
        )
    }

    if (!user || !isAdmin) {
        return null
    }

    return (
        <div style={{ minHeight: '100vh', padding: '32px 48px' }}>
            {/* Header */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: '32px'
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <Link
                        href="/admin"
                        style={{
                            width: '40px',
                            height: '40px',
                            background: 'rgba(255, 255, 255, 0.05)',
                            border: '1px solid rgba(255, 255, 255, 0.1)',
                            borderRadius: '10px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: 'rgba(255, 255, 255, 0.8)'
                        }}
                    >
                        <ArrowLeft size={20} />
                    </Link>
                    <div style={{
                        width: '48px',
                        height: '48px',
                        background: 'rgba(0, 212, 255, 0.2)',
                        borderRadius: '12px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: '#00d4ff'
                    }}>
                        <BookOpen size={24} />
                    </div>
                    <div>
                        <h1 style={{ fontSize: '24px', fontWeight: 700 }}>Zarządzanie Lekcjami</h1>
                        <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px' }}>
                            {lessons.length} lekcji w bazie
                        </p>
                    </div>
                </div>

                <button
                    onClick={() => setShowCreateForm(true)}
                    style={{
                        padding: '12px 24px',
                        background: 'linear-gradient(135deg, #00d4ff, #0099ff)',
                        border: 'none',
                        borderRadius: '12px',
                        color: 'white',
                        fontSize: '14px',
                        fontWeight: 600,
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px'
                    }}
                >
                    <Plus size={18} />
                    Nowa lekcja
                </button>
            </div>

            {/* Notifications */}
            {error && (
                <div style={{
                    padding: '16px',
                    background: 'rgba(255, 68, 68, 0.1)',
                    border: '1px solid #ff4444',
                    borderRadius: '12px',
                    marginBottom: '24px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    color: '#ff4444'
                }}>
                    <AlertTriangle size={20} />
                    {error}
                    <button onClick={() => setError(null)} style={{ marginLeft: 'auto', background: 'none', border: 'none', color: '#ff4444', cursor: 'pointer' }}>
                        <X size={18} />
                    </button>
                </div>
            )}

            {success && (
                <div style={{
                    padding: '16px',
                    background: 'rgba(0, 255, 136, 0.1)',
                    border: '1px solid #00ff88',
                    borderRadius: '12px',
                    marginBottom: '24px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    color: '#00ff88'
                }}>
                    <Check size={20} />
                    {success}
                </div>
            )}

            {/* Create Form */}
            {showCreateForm && (
                <div style={{
                    background: 'rgba(20, 20, 35, 0.6)',
                    border: '1px solid #00d4ff',
                    borderRadius: '16px',
                    padding: '24px',
                    marginBottom: '24px'
                }}>
                    <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '20px' }}>
                        Nowa lekcja
                    </h3>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
                        <div>
                            <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>
                                ID Lekcji *
                            </label>
                            <input
                                type="text"
                                value={formData.lesson_id}
                                onChange={(e) => setFormData({ ...formData, lesson_id: e.target.value })}
                                placeholder="np. lesson-torque-basics"
                                style={{
                                    width: '100%',
                                    padding: '10px 14px',
                                    background: 'rgba(255, 255, 255, 0.05)',
                                    border: '1px solid rgba(255, 255, 255, 0.1)',
                                    borderRadius: '8px',
                                    color: 'white',
                                    fontSize: '14px'
                                }}
                            />
                        </div>
                        <div>
                            <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>
                                Tytuł *
                            </label>
                            <input
                                type="text"
                                value={formData.title}
                                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                                placeholder="np. Podstawy Momentu Obrotowego"
                                style={{
                                    width: '100%',
                                    padding: '10px 14px',
                                    background: 'rgba(255, 255, 255, 0.05)',
                                    border: '1px solid rgba(255, 255, 255, 0.1)',
                                    borderRadius: '8px',
                                    color: 'white',
                                    fontSize: '14px'
                                }}
                            />
                        </div>
                    </div>

                    <div style={{ marginBottom: '16px' }}>
                        <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>
                            Opis
                        </label>
                        <textarea
                            value={formData.description}
                            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                            placeholder="Krótki opis lekcji..."
                            rows={2}
                            style={{
                                width: '100%',
                                padding: '10px 14px',
                                background: 'rgba(255, 255, 255, 0.05)',
                                border: '1px solid rgba(255, 255, 255, 0.1)',
                                borderRadius: '8px',
                                color: 'white',
                                fontSize: '14px',
                                resize: 'vertical'
                            }}
                        />
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '16px', marginBottom: '16px' }}>
                        <div>
                            <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>
                                Czas (min)
                            </label>
                            <input
                                type="number"
                                value={formData.duration_minutes}
                                onChange={(e) => setFormData({ ...formData, duration_minutes: parseInt(e.target.value) || 10 })}
                                style={{
                                    width: '100%',
                                    padding: '10px 14px',
                                    background: 'rgba(255, 255, 255, 0.05)',
                                    border: '1px solid rgba(255, 255, 255, 0.1)',
                                    borderRadius: '8px',
                                    color: 'white',
                                    fontSize: '14px'
                                }}
                            />
                        </div>
                        <div>
                            <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>
                                XP
                            </label>
                            <input
                                type="number"
                                value={formData.xp_reward}
                                onChange={(e) => setFormData({ ...formData, xp_reward: parseInt(e.target.value) || 150 })}
                                style={{
                                    width: '100%',
                                    padding: '10px 14px',
                                    background: 'rgba(255, 255, 255, 0.05)',
                                    border: '1px solid rgba(255, 255, 255, 0.1)',
                                    borderRadius: '8px',
                                    color: 'white',
                                    fontSize: '14px'
                                }}
                            />
                        </div>
                        <div>
                            <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>
                                Poziom
                            </label>
                            <select
                                value={formData.difficulty}
                                onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
                                style={{
                                    width: '100%',
                                    padding: '10px 14px',
                                    background: 'rgba(255, 255, 255, 0.05)',
                                    border: '1px solid rgba(255, 255, 255, 0.1)',
                                    borderRadius: '8px',
                                    color: 'white',
                                    fontSize: '14px'
                                }}
                            >
                                <option value="beginner">Początkujący</option>
                                <option value="intermediate">Średniozaawansowany</option>
                                <option value="advanced">Zaawansowany</option>
                            </select>
                        </div>
                    </div>

                    <div style={{ marginBottom: '20px' }}>
                        <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>
                            Content (JSON) *
                        </label>
                        <textarea
                            value={formData.content}
                            onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                            rows={6}
                            style={{
                                width: '100%',
                                padding: '10px 14px',
                                background: 'rgba(255, 255, 255, 0.05)',
                                border: '1px solid rgba(255, 255, 255, 0.1)',
                                borderRadius: '8px',
                                color: 'white',
                                fontSize: '13px',
                                fontFamily: 'monospace',
                                resize: 'vertical'
                            }}
                        />
                    </div>

                    <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
                        <button
                            onClick={() => setShowCreateForm(false)}
                            style={{
                                padding: '10px 20px',
                                background: 'rgba(255, 255, 255, 0.05)',
                                border: '1px solid rgba(255, 255, 255, 0.1)',
                                borderRadius: '8px',
                                color: 'rgba(255, 255, 255, 0.8)',
                                fontSize: '14px',
                                cursor: 'pointer'
                            }}
                        >
                            Anuluj
                        </button>
                        <button
                            onClick={handleCreate}
                            disabled={saving}
                            style={{
                                padding: '10px 20px',
                                background: 'linear-gradient(135deg, #00d4ff, #0099ff)',
                                border: 'none',
                                borderRadius: '8px',
                                color: 'white',
                                fontSize: '14px',
                                fontWeight: 600,
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '8px',
                                opacity: saving ? 0.6 : 1
                            }}
                        >
                            <Save size={16} />
                            {saving ? 'Zapisywanie...' : 'Utwórz lekcję'}
                        </button>
                    </div>
                </div>
            )}

            {/* Lessons List */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {lessons.map(lesson => (
                    <div
                        key={lesson.id}
                        style={{
                            background: 'rgba(20, 20, 35, 0.4)',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            borderRadius: '12px',
                            overflow: 'hidden'
                        }}
                    >
                        {/* Lesson Header */}
                        <div
                            style={{
                                padding: '16px 20px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'space-between',
                                cursor: 'pointer'
                            }}
                            onClick={() => setExpandedId(expandedId === lesson.id ? null : lesson.id)}
                        >
                            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                                <div style={{
                                    width: '40px',
                                    height: '40px',
                                    background: 'rgba(0, 212, 255, 0.15)',
                                    borderRadius: '10px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    color: '#00d4ff'
                                }}>
                                    <BookOpen size={20} />
                                </div>
                                <div>
                                    <h3 style={{ fontSize: '15px', fontWeight: 600, marginBottom: '2px' }}>
                                        {lesson.title}
                                    </h3>
                                    <code style={{
                                        fontSize: '12px',
                                        color: 'rgba(255, 255, 255, 0.5)',
                                        background: 'rgba(255, 255, 255, 0.05)',
                                        padding: '2px 6px',
                                        borderRadius: '4px'
                                    }}>
                                        {lesson.lesson_id}
                                    </code>
                                </div>
                            </div>

                            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                                <div style={{ display: 'flex', gap: '12px', fontSize: '12px', color: 'rgba(255,255,255,0.6)' }}>
                                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                        <Clock size={14} /> {lesson.duration_minutes}min
                                    </span>
                                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                        <Zap size={14} style={{ color: '#ffd700' }} /> {lesson.xp_reward}XP
                                    </span>
                                </div>

                                <div style={{ display: 'flex', gap: '8px' }}>
                                    <button
                                        onClick={(e) => { e.stopPropagation(); setEditingId(lesson.id); setExpandedId(lesson.id); }}
                                        style={{
                                            width: '32px',
                                            height: '32px',
                                            background: 'rgba(0, 212, 255, 0.1)',
                                            border: '1px solid rgba(0, 212, 255, 0.3)',
                                            borderRadius: '8px',
                                            color: '#00d4ff',
                                            cursor: 'pointer',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center'
                                        }}
                                    >
                                        <Edit3 size={14} />
                                    </button>
                                    <button
                                        onClick={(e) => { e.stopPropagation(); handleDelete(lesson.id); }}
                                        style={{
                                            width: '32px',
                                            height: '32px',
                                            background: 'rgba(255, 68, 68, 0.1)',
                                            border: '1px solid rgba(255, 68, 68, 0.3)',
                                            borderRadius: '8px',
                                            color: '#ff4444',
                                            cursor: 'pointer',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center'
                                        }}
                                    >
                                        <Trash2 size={14} />
                                    </button>
                                </div>

                                {expandedId === lesson.id ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                            </div>
                        </div>

                        {/* Expanded Content */}
                        {expandedId === lesson.id && (
                            <div style={{
                                padding: '16px 20px',
                                borderTop: '1px solid rgba(255, 255, 255, 0.08)',
                                background: 'rgba(0, 0, 0, 0.2)'
                            }}>
                                <div style={{ marginBottom: '12px' }}>
                                    <strong style={{ fontSize: '12px', color: 'rgba(255,255,255,0.5)' }}>Opis:</strong>
                                    <p style={{ fontSize: '14px', marginTop: '4px' }}>{lesson.description || 'Brak opisu'}</p>
                                </div>
                                <div style={{ marginBottom: '12px' }}>
                                    <strong style={{ fontSize: '12px', color: 'rgba(255,255,255,0.5)' }}>Poziom trudności:</strong>
                                    <span style={{
                                        marginLeft: '8px',
                                        padding: '2px 8px',
                                        background: lesson.difficulty === 'beginner' ? 'rgba(0, 255, 136, 0.2)' :
                                            lesson.difficulty === 'intermediate' ? 'rgba(255, 215, 0, 0.2)' : 'rgba(255, 68, 68, 0.2)',
                                        color: lesson.difficulty === 'beginner' ? '#00ff88' :
                                            lesson.difficulty === 'intermediate' ? '#ffd700' : '#ff4444',
                                        borderRadius: '4px',
                                        fontSize: '12px'
                                    }}>
                                        {lesson.difficulty === 'beginner' ? 'Początkujący' :
                                            lesson.difficulty === 'intermediate' ? 'Średniozaawansowany' : 'Zaawansowany'}
                                    </span>
                                </div>
                                <div>
                                    <strong style={{ fontSize: '12px', color: 'rgba(255,255,255,0.5)' }}>Content (JSON):</strong>
                                    <pre style={{
                                        marginTop: '8px',
                                        padding: '12px',
                                        background: 'rgba(0, 0, 0, 0.3)',
                                        borderRadius: '8px',
                                        fontSize: '11px',
                                        overflow: 'auto',
                                        maxHeight: '200px'
                                    }}>
                                        {JSON.stringify(lesson.content, null, 2)}
                                    </pre>
                                </div>
                            </div>
                        )}
                    </div>
                ))}

                {lessons.length === 0 && (
                    <div style={{
                        padding: '48px',
                        textAlign: 'center',
                        color: 'rgba(255, 255, 255, 0.5)'
                    }}>
                        Brak lekcji w bazie. Kliknij "Nowa lekcja" aby dodać pierwszą.
                    </div>
                )}
            </div>
        </div>
    )
}
