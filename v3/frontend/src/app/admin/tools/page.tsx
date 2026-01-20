'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import {
    Wrench, ArrowLeft, Plus, Trash2, Save, X,
    AlertTriangle, Check, Zap, ChevronDown, ChevronUp
} from 'lucide-react'

interface Tool {
    id: string
    tool_id: string
    title: string
    description: string
    tier: number
    usage_xp: number
    config: any
    created_at: string
}

export default function AdminToolsPage() {
    const { user, loading: authLoading } = useAuth()
    const router = useRouter()
    const [tools, setTools] = useState<Tool[]>([])
    const [loading, setLoading] = useState(true)
    const [isAdmin, setIsAdmin] = useState(false)
    const [expandedId, setExpandedId] = useState<string | null>(null)
    const [showCreateForm, setShowCreateForm] = useState(false)
    const [saving, setSaving] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [success, setSuccess] = useState<string | null>(null)

    const [formData, setFormData] = useState({
        tool_id: '',
        title: '',
        description: '',
        tier: 1,
        usage_xp: 50,
        config: '{}'
    })

    useEffect(() => {
        async function loadTools() {
            if (!user) return
            try {
                const response = await fetch('/api/admin/tools')
                if (response.ok) {
                    setIsAdmin(true)
                    const data = await response.json()
                    setTools(data.tools || [])
                } else {
                    setIsAdmin(false)
                }
            } catch (error) {
                console.error('Error loading tools:', error)
            } finally {
                setLoading(false)
            }
        }
        if (!authLoading) loadTools()
    }, [user, authLoading])

    const handleCreate = async () => {
        setSaving(true)
        setError(null)
        try {
            let configJson
            try { configJson = JSON.parse(formData.config) } catch { setError('Nieprawidłowy format JSON'); setSaving(false); return }

            const response = await fetch('/api/admin/tools', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ...formData, config: configJson })
            })

            if (response.ok) {
                const data = await response.json()
                setTools([data.tool, ...tools])
                setShowCreateForm(false)
                setFormData({ tool_id: '', title: '', description: '', tier: 1, usage_xp: 50, config: '{}' })
                setSuccess('Narzędzie utworzone!')
                setTimeout(() => setSuccess(null), 3000)
            } else {
                const data = await response.json()
                setError(data.error || 'Błąd podczas tworzenia')
            }
        } catch { setError('Błąd połączenia z serwerem') }
        finally { setSaving(false) }
    }

    const handleDelete = async (id: string) => {
        if (!confirm('Czy na pewno chcesz usunąć to narzędzie?')) return
        try {
            const response = await fetch(`/api/admin/tools?id=${id}`, { method: 'DELETE' })
            if (response.ok) {
                setTools(tools.filter(t => t.id !== id))
                setSuccess('Narzędzie usunięte!')
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

    const tierColors = { 1: '#00ff88', 2: '#ffd700', 3: '#ff4444' }
    const tierNames = { 1: 'Podstawowy', 2: 'Zaawansowany', 3: 'Ekspert' }

    return (
        <div style={{ minHeight: '100vh', padding: '32px 48px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '32px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <Link href="/admin" style={{ width: '40px', height: '40px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'rgba(255, 255, 255, 0.8)' }}>
                        <ArrowLeft size={20} />
                    </Link>
                    <div style={{ width: '48px', height: '48px', background: 'rgba(255, 136, 0, 0.2)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#ff8800' }}>
                        <Wrench size={24} />
                    </div>
                    <div>
                        <h1 style={{ fontSize: '24px', fontWeight: 700 }}>Zarządzanie Narzędziami</h1>
                        <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px' }}>{tools.length} narzędzi w bazie</p>
                    </div>
                </div>
                <button onClick={() => setShowCreateForm(true)} style={{ padding: '12px 24px', background: 'linear-gradient(135deg, #ff8800, #cc6600)', border: 'none', borderRadius: '12px', color: 'white', fontSize: '14px', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Plus size={18} /> Nowe narzędzie
                </button>
            </div>

            {error && <div style={{ padding: '16px', background: 'rgba(255, 68, 68, 0.1)', border: '1px solid #ff4444', borderRadius: '12px', marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '12px', color: '#ff4444' }}><AlertTriangle size={20} /> {error} <button onClick={() => setError(null)} style={{ marginLeft: 'auto', background: 'none', border: 'none', color: '#ff4444', cursor: 'pointer' }}><X size={18} /></button></div>}
            {success && <div style={{ padding: '16px', background: 'rgba(0, 255, 136, 0.1)', border: '1px solid #00ff88', borderRadius: '12px', marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '12px', color: '#00ff88' }}><Check size={20} /> {success}</div>}

            {showCreateForm && (
                <div style={{ background: 'rgba(20, 20, 35, 0.6)', border: '1px solid #ff8800', borderRadius: '16px', padding: '24px', marginBottom: '24px' }}>
                    <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '20px' }}>Nowe narzędzie</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
                        <div><label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>ID Narzędzia *</label><input type="text" value={formData.tool_id} onChange={(e) => setFormData({ ...formData, tool_id: e.target.value })} placeholder="np. tool-torque-calculator" style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }} /></div>
                        <div><label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>Tytuł *</label><input type="text" value={formData.title} onChange={(e) => setFormData({ ...formData, title: e.target.value })} placeholder="np. Kalkulator Momentu" style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }} /></div>
                    </div>
                    <div style={{ marginBottom: '16px' }}><label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>Opis</label><textarea value={formData.description} onChange={(e) => setFormData({ ...formData, description: e.target.value })} rows={2} style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px', resize: 'vertical' }} /></div>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
                        <div><label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>Tier</label><select value={formData.tier} onChange={(e) => setFormData({ ...formData, tier: parseInt(e.target.value) })} style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }}><option value={1}>1 - Podstawowy</option><option value={2}>2 - Zaawansowany</option><option value={3}>3 - Ekspert</option></select></div>
                        <div><label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>Usage XP</label><input type="number" value={formData.usage_xp} onChange={(e) => setFormData({ ...formData, usage_xp: parseInt(e.target.value) || 50 })} style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '14px' }} /></div>
                    </div>
                    <div style={{ marginBottom: '20px' }}><label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', color: 'rgba(255,255,255,0.7)' }}>Config (JSON) *</label><textarea value={formData.config} onChange={(e) => setFormData({ ...formData, config: e.target.value })} rows={4} style={{ width: '100%', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '13px', fontFamily: 'monospace', resize: 'vertical' }} /></div>
                    <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
                        <button onClick={() => setShowCreateForm(false)} style={{ padding: '10px 20px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'rgba(255, 255, 255, 0.8)', fontSize: '14px', cursor: 'pointer' }}>Anuluj</button>
                        <button onClick={handleCreate} disabled={saving} style={{ padding: '10px 20px', background: 'linear-gradient(135deg, #ff8800, #cc6600)', border: 'none', borderRadius: '8px', color: 'white', fontSize: '14px', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px', opacity: saving ? 0.6 : 1 }}><Save size={16} /> {saving ? 'Zapisywanie...' : 'Utwórz narzędzie'}</button>
                    </div>
                </div>
            )}

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {tools.map(tool => (
                    <div key={tool.id} style={{ background: 'rgba(20, 20, 35, 0.4)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '12px', overflow: 'hidden' }}>
                        <div style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', cursor: 'pointer' }} onClick={() => setExpandedId(expandedId === tool.id ? null : tool.id)}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                                <div style={{ width: '40px', height: '40px', background: 'rgba(255, 136, 0, 0.15)', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#ff8800' }}><Wrench size={20} /></div>
                                <div>
                                    <h3 style={{ fontSize: '15px', fontWeight: 600, marginBottom: '2px' }}>{tool.title}</h3>
                                    <code style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.5)', background: 'rgba(255, 255, 255, 0.05)', padding: '2px 6px', borderRadius: '4px' }}>{tool.tool_id}</code>
                                </div>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                                <span style={{ padding: '4px 10px', background: `${tierColors[tool.tier as keyof typeof tierColors]}20`, color: tierColors[tool.tier as keyof typeof tierColors], borderRadius: '12px', fontSize: '12px', fontWeight: 600 }}>Tier {tool.tier}</span>
                                <span style={{ fontSize: '12px', color: 'rgba(255,255,255,0.6)', display: 'flex', alignItems: 'center', gap: '4px' }}><Zap size={14} style={{ color: '#ffd700' }} /> {tool.usage_xp}XP</span>
                                <button onClick={(e) => { e.stopPropagation(); handleDelete(tool.id); }} style={{ width: '32px', height: '32px', background: 'rgba(255, 68, 68, 0.1)', border: '1px solid rgba(255, 68, 68, 0.3)', borderRadius: '8px', color: '#ff4444', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}><Trash2 size={14} /></button>
                                {expandedId === tool.id ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                            </div>
                        </div>
                        {expandedId === tool.id && (
                            <div style={{ padding: '16px 20px', borderTop: '1px solid rgba(255, 255, 255, 0.08)', background: 'rgba(0, 0, 0, 0.2)' }}>
                                <div style={{ marginBottom: '12px' }}><strong style={{ fontSize: '12px', color: 'rgba(255,255,255,0.5)' }}>Opis:</strong><p style={{ fontSize: '14px', marginTop: '4px' }}>{tool.description || 'Brak opisu'}</p></div>
                                <div><strong style={{ fontSize: '12px', color: 'rgba(255,255,255,0.5)' }}>Config:</strong><pre style={{ marginTop: '8px', padding: '12px', background: 'rgba(0, 0, 0, 0.3)', borderRadius: '8px', fontSize: '11px', overflow: 'auto', maxHeight: '150px' }}>{JSON.stringify(tool.config, null, 2)}</pre></div>
                            </div>
                        )}
                    </div>
                ))}
                {tools.length === 0 && <div style={{ padding: '48px', textAlign: 'center', color: 'rgba(255, 255, 255, 0.5)' }}>Brak narzędzi w bazie.</div>}
            </div>
        </div>
    )
}
