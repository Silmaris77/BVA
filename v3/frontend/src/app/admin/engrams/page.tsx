'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import {
    Brain, ArrowLeft, Plus, Trash2, Edit3, Save, X,
    AlertTriangle, Check, Zap, ChevronDown, ChevronUp
} from 'lucide-react'

interface Engram {
    id: string
    engram_id: string
    title: string
    lesson_id: string | null
    slides: any
    quiz_pool: any
    install_xp: number
    refresh_xp: number
    created_at: string
}

export default function AdminEngramsPage() {
    const { user, loading: authLoading } = useAuth()
    const router = useRouter()
    const [engrams, setEngrams] = useState<Engram[]>([])
    const [loading, setLoading] = useState(true)
    const [isAdmin, setIsAdmin] = useState(false)
    const [expandedId, setExpandedId] = useState<string | null>(null)
    const [showCreateForm, setShowCreateForm] = useState(false)
    const [saving, setSaving] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [success, setSuccess] = useState<string | null>(null)

    const [formData, setFormData] = useState({
        engram_id: '',
        title: '',
        lesson_id: '',
        slides: '[]',
        quiz_pool: '[]',
        install_xp: 50,
        refresh_xp: 25
    })

    useEffect(() => {
        async function loadEngrams() {
            if (!user) return

            try {
                const response = await fetch('/api/admin/engrams')
                if (response.ok) {
                    setIsAdmin(true)
                    const data = await response.json()
                    setEngrams(data.engrams || [])
                } else {
                    setIsAdmin(false)
                }
            } catch (error) {
                console.error('Error loading engrams:', error)
            } finally {
                setLoading(false)
            }
        }

        if (!authLoading) loadEngrams()
    }, [user, authLoading])

    const handleCreate = async () => {
        setSaving(true)
        setError(null)

        try {
            let slidesJson, quizPoolJson
            try {
                slidesJson = JSON.parse(formData.slides)
                quizPoolJson = JSON.parse(formData.quiz_pool)
            } catch {
                setError('Nieprawidłowy format JSON')
                setSaving(false)
                return
            }

            const response = await fetch('/api/admin/engrams', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    ...formData,
                    lesson_id: formData.lesson_id || null,
                    slides: slidesJson,
                    quiz_pool: quizPoolJson
                })
            })

            if (response.ok) {
                const data = await response.json()
                setEngrams([data.engram, ...engrams])
                setShowCreateForm(false)
                setFormData({
                    engram_id: '',
                    title: '',
                    lesson_id: '',
                    slides: '[]',
                    quiz_pool: '[]',
                    install_xp: 50,
                    refresh_xp: 25
                })
                setSuccess('Engram utworzony!')
                setTimeout(() => setSuccess(null), 3000)
            } else {
                const data = await response.json()
                setError(data.error || 'Błąd podczas tworzenia')
            }
        } catch (error) {
            setError('Błąd połączenia z serwerem')
        } finally {
            setSaving(false)
        }
    }

    const handleDelete = async (id: string) => {
        if (!confirm('Czy na pewno chcesz usunąć ten engram?')) return

        try {
            const response = await fetch(`/api/admin/engrams?id=${id}`, { method: 'DELETE' })
            if (response.ok) {
                setEngrams(engrams.filter(e => e.id !== id))
                setSuccess('Engram usunięty!')
                setTimeout(() => setSuccess(null), 3000)
            } else {
                const data = await response.json()
                setError(data.error || 'Błąd podczas usuwania')
            }
        } catch (error) {
            setError('Błąd połączenia z serwerem')
        }
    }

    // Redirect if not authorized
    useEffect(() => {
        if (!authLoading && !loading && (!user || !isAdmin)) {
            router.push('/admin')
        }
    }, [user, isAdmin, authLoading, loading, router])

    if (authLoading || loading) {
        return (
            <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'rgba(255, 255, 255, 0.6)' }}>
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
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '32px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <Link href="/admin" style={{
                        width: '40px', height: '40px', background: 'rgba(255, 255, 255, 0.05)',
                        border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '10px',
                        display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'rgba(255, 255, 255, 0.8)'
                    }}>
                        <ArrowLeft size={20} />
                    </Link>
                    <div style={{
                        width: '48px', height: '48px', background: 'rgba(176, 0, 255, 0.2)',
                        borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#b000ff'
                    }}>
                        <Brain size={24} />
                    </div>
                    <div>
                        <h1 style={{ fontSize: '24px', fontWeight: 700 }}>Zarządzanie Engramami</h1>
                        <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px' }}>{engrams.length} engramów w bazie</p>
                    </div>
                </div>

                <button onClick={() => setShowCreateForm(true)} style={{
                    padding: '12px 24px', background: 'linear-gradient(135deg, #b000ff, #8800cc)',
                    border: 'none', borderRadius: '12px', color: 'white', fontSize: '14px',
                    fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px'
                }}>
                    <Plus size={18} /> Nowy engram
                </button>
            </div>

            {/* Notifications */}
            {error && (
                <div style={{
                    padding: '16px', background: 'rgba(255, 68, 68, 0.1)', border: '1px solid #ff4444',
                    borderRadius: '12px', marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '12px', color: '#ff4444'
                }}>
                    <AlertTriangle size={20} /> {error}
                    <button onClick={() => setError(null)} style={{ marginLeft: 'auto', background: 'none', border: 'none', color: '#ff4444', cursor: 'pointer' }}>
                        <X size={18} />
                    </button>
                </div>
            )}

            {success && (
                <div style={{
                    padding: '16px', background: 'rgba(0, 255, 136, 0.1)', border: '1px solid #00ff88',
                    borderRadius: '12px', marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '12px', color: '#00ff88'
                }}>
                    <Check size={20} /> {success}
                </div>
            )}

            {/* Create Form */}
            {showCreateForm && (
                <div style={{
                    background: 'rgba(20, 20, 35, 0.6)', border: '1px solid #b000ff',
                    borderRadius: '16px', padding: '24px', marginBottom: '24px'
                }}>
                    <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '20px' }}>Nowy engram</h3>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
                        <div>
                            <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>ID Engramu *</label>
                            <input type="text" value={formData.engram_id} onChange={(e) => setFormData({ ...formData, engram_id: e.target.value })}
                                placeholder="np. engram-torque-formula"
                                style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }}
                            />
                        </div>
                        <div>
                            <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>Tytuł *</label>
                            <input type="text" value={formData.title} onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                                placeholder="np. Wzór na Moment Obrotowy"
                                style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }}
                            />
                        </div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '16px', marginBottom: '16px' }}>
                        <div>
                            <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>Powiązana lekcja</label>
                            <input type="text" value={formData.lesson_id} onChange={(e) => setFormData({ ...formData, lesson_id: e.target.value })}
                                placeholder="lesson-id (opcjonalne)"
                                style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }}
                            />
                        </div>
                        <div>
                            <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>Install XP</label>
                            <input type="number" value={formData.install_xp} onChange={(e) => setFormData({ ...formData, install_xp: parseInt(e.target.value) || 50 })}
                                style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }}
                            />
                        </div>
                        <div>
                            <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>Refresh XP</label>
                            <input type="number" value={formData.refresh_xp} onChange={(e) => setFormData({ ...formData, refresh_xp: parseInt(e.target.value) || 25 })}
                                style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }}
                            />
                        </div>
                    </div>

                    <div style={{ marginBottom: '16px' }}>
                        <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>Slides (JSON) *</label>
                        <textarea value={formData.slides} onChange={(e) => setFormData({ ...formData, slides: e.target.value })} rows={4}
                            placeholder='[{"type": "text", "title": "Slide 1", "content": "..."}]'
                            style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '13px', fontFamily: 'monospace', resize: 'vertical' }}
                        />
                    </div>

                    <div style={{ marginBottom: '20px' }}>
                        <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>Quiz Pool (JSON) *</label>
                        <textarea value={formData.quiz_pool} onChange={(e) => setFormData({ ...formData, quiz_pool: e.target.value })} rows={4}
                            placeholder='[{"q": "Pytanie?", "a": "Odpowiedź", "wrong": ["Zła1", "Zła2"]}]'
                            style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '13px', fontFamily: 'monospace', resize: 'vertical' }}
                        />
                    </div>

                    <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
                        <button onClick={() => setShowCreateForm(false)} style={{
                            padding: '10px 20px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)',
                            borderRadius: '8px', color: 'rgba(255, 255, 255, 0.8)', fontSize: '14px', cursor: 'pointer'
                        }}>
                            Anuluj
                        </button>
                        <button onClick={handleCreate} disabled={saving} style={{
                            padding: '10px 20px', background: 'linear-gradient(135deg, #b000ff, #8800cc)',
                            border: 'none', borderRadius: '8px', color: 'white', fontSize: '14px', fontWeight: 600,
                            cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px', opacity: saving ? 0.6 : 1
                        }}>
                            <Save size={16} /> {saving ? 'Zapisywanie...' : 'Utwórz engram'}
                        </button>
                    </div>
                </div>
            )}

            {/* Engrams List */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {engrams.map(engram => (
                    <div key={engram.id} style={{ background: 'rgba(20, 20, 35, 0.4)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '12px', overflow: 'hidden' }}>
                        <div style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', cursor: 'pointer' }}
                            onClick={() => setExpandedId(expandedId === engram.id ? null : engram.id)}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                                <div style={{ width: '40px', height: '40px', background: 'rgba(176, 0, 255, 0.15)', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#b000ff' }}>
                                    <Brain size={20} />
                                </div>
                                <div>
                                    <h3 style={{ fontSize: '15px', fontWeight: 600, marginBottom: '2px' }}>{engram.title}</h3>
                                    <code style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.5)', background: 'rgba(255, 255, 255, 0.05)', padding: '2px 6px', borderRadius: '4px' }}>
                                        {engram.engram_id}
                                    </code>
                                </div>
                            </div>

                            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                                <div style={{ display: 'flex', gap: '12px', fontSize: '12px', color: 'rgba(255,255,255,0.6)' }}>
                                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                        📑 {Array.isArray(engram.slides) ? engram.slides.length : 0} slides
                                    </span>
                                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                        ❓ {Array.isArray(engram.quiz_pool) ? engram.quiz_pool.length : 0} quizów
                                    </span>
                                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                        <Zap size={14} style={{ color: '#ffd700' }} /> {engram.install_xp}/{engram.refresh_xp}XP
                                    </span>
                                </div>

                                <div style={{ display: 'flex', gap: '8px' }}>
                                    <button onClick={(e) => { e.stopPropagation(); handleDelete(engram.id); }} style={{
                                        width: '32px', height: '32px', background: 'rgba(255, 68, 68, 0.1)',
                                        border: '1px solid rgba(255, 68, 68, 0.3)', borderRadius: '8px', color: '#ff4444',
                                        cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center'
                                    }}>
                                        <Trash2 size={14} />
                                    </button>
                                </div>

                                {expandedId === engram.id ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                            </div>
                        </div>

                        {expandedId === engram.id && (
                            <div style={{ padding: '16px 20px', borderTop: '1px solid rgba(255, 255, 255, 0.08)', background: 'rgba(0, 0, 0, 0.2)' }}>
                                {engram.lesson_id && (
                                    <div style={{ marginBottom: '12px' }}>
                                        <strong style={{ fontSize: '12px', color: 'rgba(255,255,255,0.5)' }}>Powiązana lekcja:</strong>
                                        <code style={{ marginLeft: '8px', fontSize: '12px' }}>{engram.lesson_id}</code>
                                    </div>
                                )}
                                <div style={{ marginBottom: '12px' }}>
                                    <strong style={{ fontSize: '12px', color: 'rgba(255,255,255,0.5)' }}>Slides:</strong>
                                    <pre style={{ marginTop: '8px', padding: '12px', background: 'rgba(0, 0, 0, 0.3)', borderRadius: '8px', fontSize: '11px', overflow: 'auto', maxHeight: '150px' }}>
                                        {JSON.stringify(engram.slides, null, 2)}
                                    </pre>
                                </div>
                                <div>
                                    <strong style={{ fontSize: '12px', color: 'rgba(255,255,255,0.5)' }}>Quiz Pool:</strong>
                                    <pre style={{ marginTop: '8px', padding: '12px', background: 'rgba(0, 0, 0, 0.3)', borderRadius: '8px', fontSize: '11px', overflow: 'auto', maxHeight: '150px' }}>
                                        {JSON.stringify(engram.quiz_pool, null, 2)}
                                    </pre>
                                </div>
                            </div>
                        )}
                    </div>
                ))}

                {engrams.length === 0 && (
                    <div style={{ padding: '48px', textAlign: 'center', color: 'rgba(255, 255, 255, 0.5)' }}>
                        Brak engramów w bazie. Kliknij "Nowy engram" aby dodać pierwszy.
                    </div>
                )}
            </div>
        </div>
    )
}
