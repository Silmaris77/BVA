'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import {
    FileText, ArrowLeft, Plus, Trash2, Save, X,
    AlertTriangle, Check, Zap, ChevronDown, ChevronUp
} from 'lucide-react'

interface Resource {
    id: string
    resource_id: string
    title: string
    description: string
    resource_type: string
    content: any
    download_xp: number
    created_at: string
}

export default function AdminResourcesPage() {
    const { user, loading: authLoading } = useAuth()
    const router = useRouter()
    const [resources, setResources] = useState<Resource[]>([])
    const [loading, setLoading] = useState(true)
    const [isAdmin, setIsAdmin] = useState(false)
    const [expandedId, setExpandedId] = useState<string | null>(null)
    const [showCreateForm, setShowCreateForm] = useState(false)
    const [saving, setSaving] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [success, setSuccess] = useState<string | null>(null)

    const [formData, setFormData] = useState({
        resource_id: '',
        title: '',
        description: '',
        resource_type: 'guide',
        content: '{}',
        download_xp: 10
    })

    useEffect(() => {
        async function loadResources() {
            if (!user) return
            try {
                const response = await fetch('/api/admin/resources')
                if (response.ok) {
                    setIsAdmin(true)
                    const data = await response.json()
                    setResources(data.resources || [])
                } else {
                    setIsAdmin(false)
                }
            } catch (error) {
                console.error('Error loading resources:', error)
            } finally {
                setLoading(false)
            }
        }
        if (!authLoading) loadResources()
    }, [user, authLoading])

    const handleCreate = async () => {
        setSaving(true)
        setError(null)
        try {
            let contentJson
            try { contentJson = JSON.parse(formData.content) } catch { setError('Nieprawidłowy format JSON'); setSaving(false); return }

            const response = await fetch('/api/admin/resources', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ...formData, content: contentJson })
            })

            if (response.ok) {
                const data = await response.json()
                setResources([data.resource, ...resources])
                setShowCreateForm(false)
                setFormData({ resource_id: '', title: '', description: '', resource_type: 'guide', content: '{}', download_xp: 10 })
                setSuccess('Zasób utworzony!')
                setTimeout(() => setSuccess(null), 3000)
            } else {
                const data = await response.json()
                setError(data.error || 'Błąd podczas tworzenia')
            }
        } catch { setError('Błąd połączenia z serwerem') }
        finally { setSaving(false) }
    }

    const handleDelete = async (id: string) => {
        if (!confirm('Czy na pewno chcesz usunąć ten zasób?')) return
        try {
            const response = await fetch(`/api/admin/resources?id=${id}`, { method: 'DELETE' })
            if (response.ok) {
                setResources(resources.filter(r => r.id !== id))
                setSuccess('Zasób usunięty!')
                setTimeout(() => setSuccess(null), 3000)
            } else {
                const data = await response.json()
                setError(data.error || 'Błąd podczas usuwania')
            }
        } catch { setError('Błąd połączenia z serwerem') }
    }

    // Redirect if not authorized
    useEffect(() => {
        if (!authLoading && !loading && (!user || !isAdmin)) {
            router.push('/admin')
        }
    }, [user, isAdmin, authLoading, loading, router])

    if (authLoading || loading) {
        return <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'rgba(255, 255, 255, 0.6)' }}>Ładowanie...</div>
    }

    if (!user || !isAdmin) { return null }

    const typeColors: Record<string, string> = { pdf: '#ff4444', table: '#00d4ff', guide: '#00ff88', template: '#ffd700' }
    const typeNames: Record<string, string> = { pdf: 'PDF', table: 'Tabela', guide: 'Poradnik', template: 'Szablon' }

    return (
        <div style={{ minHeight: '100vh', padding: '32px 48px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '32px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <Link href="/admin" style={{ width: '40px', height: '40px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'rgba(255, 255, 255, 0.8)' }}>
                        <ArrowLeft size={20} />
                    </Link>
                    <div style={{ width: '48px', height: '48px', background: 'rgba(0, 255, 136, 0.2)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#00ff88' }}>
                        <FileText size={24} />
                    </div>
                    <div>
                        <h1 style={{ fontSize: '24px', fontWeight: 700 }}>Zarządzanie Zasobami</h1>
                        <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px' }}>{resources.length} zasobów w bazie</p>
                    </div>
                </div>
                <button onClick={() => setShowCreateForm(true)} style={{ padding: '12px 24px', background: 'linear-gradient(135deg, #00ff88, #00cc66)', border: 'none', borderRadius: '12px', color: 'white', fontSize: '14px', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Plus size={18} /> Nowy zasób
                </button>
            </div>

            {error && <div style={{ padding: '16px', background: 'rgba(255, 68, 68, 0.1)', border: '1px solid #ff4444', borderRadius: '12px', marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '12px', color: '#ff4444' }}><AlertTriangle size={20} /> {error} <button onClick={() => setError(null)} style={{ marginLeft: 'auto', background: 'none', border: 'none', color: '#ff4444', cursor: 'pointer' }}><X size={18} /></button></div>}
            {success && <div style={{ padding: '16px', background: 'rgba(0, 255, 136, 0.1)', border: '1px solid #00ff88', borderRadius: '12px', marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '12px', color: '#00ff88' }}><Check size={20} /> {success}</div>}

            {showCreateForm && (
                <div style={{ background: 'rgba(20, 20, 35, 0.6)', border: '1px solid #00ff88', borderRadius: '16px', padding: '24px', marginBottom: '24px' }}>
                    <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '20px' }}>Nowy zasób</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
                        <div><label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>ID Zasobu *</label><input type="text" value={formData.resource_id} onChange={(e) => setFormData({ ...formData, resource_id: e.target.value })} placeholder="np. resource-torque-chart" style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }} /></div>
                        <div><label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>Tytuł *</label><input type="text" value={formData.title} onChange={(e) => setFormData({ ...formData, title: e.target.value })} placeholder="np. Tabela Momentów" style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }} /></div>
                    </div>
                    <div style={{ marginBottom: '16px' }}><label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>Opis</label><textarea value={formData.description} onChange={(e) => setFormData({ ...formData, description: e.target.value })} rows={2} style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px', resize: 'vertical' }} /></div>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
                        <div><label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>Typ zasobu</label><select value={formData.resource_type} onChange={(e) => setFormData({ ...formData, resource_type: e.target.value })} style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }}><option value="guide">Poradnik</option><option value="table">Tabela</option><option value="pdf">PDF</option><option value="template">Szablon</option></select></div>
                        <div><label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>Download XP</label><input type="number" value={formData.download_xp} onChange={(e) => setFormData({ ...formData, download_xp: parseInt(e.target.value) || 10 })} style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }} /></div>
                    </div>
                    <div style={{ marginBottom: '20px' }}><label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>Content (JSON) *</label><textarea value={formData.content} onChange={(e) => setFormData({ ...formData, content: e.target.value })} rows={4} style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '13px', fontFamily: 'monospace', resize: 'vertical' }} /></div>
                    <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
                        <button onClick={() => setShowCreateForm(false)} style={{ padding: '10px 20px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'rgba(255, 255, 255, 0.8)', fontSize: '14px', cursor: 'pointer' }}>Anuluj</button>
                        <button onClick={handleCreate} disabled={saving} style={{ padding: '10px 20px', background: 'linear-gradient(135deg, #00ff88, #00cc66)', border: 'none', borderRadius: '8px', color: 'white', fontSize: '14px', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px', opacity: saving ? 0.6 : 1 }}><Save size={16} /> {saving ? 'Zapisywanie...' : 'Utwórz zasób'}</button>
                    </div>
                </div>
            )}

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {resources.map(resource => (
                    <div key={resource.id} style={{ background: 'rgba(20, 20, 35, 0.4)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '12px', overflow: 'hidden' }}>
                        <div style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', cursor: 'pointer' }} onClick={() => setExpandedId(expandedId === resource.id ? null : resource.id)}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                                <div style={{ width: '40px', height: '40px', background: 'rgba(0, 255, 136, 0.15)', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#00ff88' }}><FileText size={20} /></div>
                                <div>
                                    <h3 style={{ fontSize: '15px', fontWeight: 600, marginBottom: '2px' }}>{resource.title}</h3>
                                    <code style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.5)', background: 'rgba(255, 255, 255, 0.05)', padding: '2px 6px', borderRadius: '4px' }}>{resource.resource_id}</code>
                                </div>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                                <span style={{ padding: '4px 10px', background: `${typeColors[resource.resource_type] || '#888'}20`, color: typeColors[resource.resource_type] || '#888', borderRadius: '12px', fontSize: '12px', fontWeight: 600 }}>{typeNames[resource.resource_type] || resource.resource_type}</span>
                                <span style={{ fontSize: '12px', color: 'rgba(255,255,255,0.6)', display: 'flex', alignItems: 'center', gap: '4px' }}><Zap size={14} style={{ color: '#ffd700' }} /> {resource.download_xp}XP</span>
                                <button onClick={(e) => { e.stopPropagation(); handleDelete(resource.id); }} style={{ width: '32px', height: '32px', background: 'rgba(255, 68, 68, 0.1)', border: '1px solid rgba(255, 68, 68, 0.3)', borderRadius: '8px', color: '#ff4444', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}><Trash2 size={14} /></button>
                                {expandedId === resource.id ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                            </div>
                        </div>
                        {expandedId === resource.id && (
                            <div style={{ padding: '16px 20px', borderTop: '1px solid rgba(255, 255, 255, 0.08)', background: 'rgba(0, 0, 0, 0.2)' }}>
                                <div style={{ marginBottom: '12px' }}><strong style={{ fontSize: '12px', color: 'rgba(255,255,255,0.5)' }}>Opis:</strong><p style={{ fontSize: '14px', marginTop: '4px' }}>{resource.description || 'Brak opisu'}</p></div>
                                <div><strong style={{ fontSize: '12px', color: 'rgba(255,255,255,0.5)' }}>Content:</strong><pre style={{ marginTop: '8px', padding: '12px', background: 'rgba(0, 0, 0, 0.3)', borderRadius: '8px', fontSize: '11px', overflow: 'auto', maxHeight: '150px' }}>{JSON.stringify(resource.content, null, 2)}</pre></div>
                            </div>
                        )}
                    </div>
                ))}
                {resources.length === 0 && <div style={{ padding: '48px', textAlign: 'center', color: 'rgba(255, 255, 255, 0.5)' }}>Brak zasobów w bazie.</div>}
            </div>
        </div>
    )
}
