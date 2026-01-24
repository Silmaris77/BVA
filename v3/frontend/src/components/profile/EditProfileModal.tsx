'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useAuth } from '@/contexts/AuthContext'
import { X, User, Zap, Target, Sun, Shield, Brain, Rocket, Eye, Crown } from 'lucide-react'
import { useRouter } from 'next/navigation'

interface EditProfileModalProps {
    isOpen: boolean
    onClose: () => void
    currentName: string
    currentAvatar: string
    userId: string
}

// Archetype Definitions
export const ARCHETYPES = [
    { id: 'strategist', label: 'Strategist', icon: Target, color: '#b000ff' }, // Purple
    { id: 'executor', label: 'Executor', icon: Zap, color: '#ffd700' },     // Gold
    { id: 'visionary', label: 'Visionary', icon: Sun, color: '#00d4ff' },   // Cyan
    { id: 'guardian', label: 'Guardian', icon: Shield, color: '#0055ff' },  // Blue
    { id: 'sage', label: 'Sage', icon: Brain, color: '#ff00ff' },           // Magenta
    { id: 'pioneer', label: 'Pioneer', icon: Rocket, color: '#ff8800' },    // Orange
    { id: 'observer', label: 'Observer', icon: Eye, color: '#00ff88' },     // Green
    { id: 'ruler', label: 'Commander', icon: Crown, color: '#ff4757' },     // Red
]

export default function EditProfileModal({ isOpen, onClose, currentName, currentAvatar, userId }: EditProfileModalProps) {
    const [name, setName] = useState(currentName)
    const [selectedArchetype, setSelectedArchetype] = useState(currentAvatar || 'strategist')
    const [saving, setSaving] = useState(false)
    const { refreshProfile: refreshContext } = useAuth()
    const router = useRouter()
    const supabase = createClient()

    if (!isOpen) return null

    const handleSave = async () => {
        setSaving(true)
        try {
            const { error } = await supabase
                .from('user_profiles')
                .update({
                    display_name: name,
                    avatar_url: selectedArchetype
                })
                .eq('id', userId)

            if (error) throw error

            // Force refresh of Auth context to update avatar immediately
            await refreshContext()

            router.refresh()
            onClose()
        } catch (e) {
            console.error('Error updating profile:', e)
            alert('Wystąpił błąd podczas zapisywania profilu.')
        } finally {
            setSaving(false)
        }
    }

    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0,0,0,0.8)',
            backdropFilter: 'blur(8px)',
            zIndex: 1000,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '20px'
        }}>
            <div style={{
                background: '#1a1a2e',
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '24px',
                width: '100%',
                maxWidth: '500px',
                padding: '32px',
                position: 'relative',
                boxShadow: '0 20px 50px rgba(0,0,0,0.5)'
            }}>
                <button
                    onClick={onClose}
                    style={{
                        position: 'absolute',
                        top: '20px',
                        right: '20px',
                        background: 'none',
                        border: 'none',
                        color: 'rgba(255,255,255,0.5)',
                        cursor: 'pointer'
                    }}
                >
                    <X size={24} />
                </button>

                <h2 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '24px', color: 'white' }}>
                    Edycja Profilu
                </h2>

                {/* Name Input */}
                <div style={{ marginBottom: '32px' }}>
                    <label style={{ display: 'block', fontSize: '12px', color: 'rgba(255,255,255,0.5)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '1px' }}>
                        Nazwa Wyświetlana
                    </label>
                    <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        style={{
                            width: '100%',
                            background: 'rgba(255,255,255,0.05)',
                            border: '1px solid rgba(255,255,255,0.1)',
                            borderRadius: '12px',
                            padding: '16px',
                            color: 'white',
                            fontSize: '16px',
                            outline: 'none'
                        }}
                        placeholder="Wpisz swoje imię..."
                    />
                </div>

                {/* Archetype Selector */}
                <div style={{ marginBottom: '40px' }}>
                    <label style={{ display: 'block', fontSize: '12px', color: 'rgba(255,255,255,0.5)', marginBottom: '16px', textTransform: 'uppercase', letterSpacing: '1px' }}>
                        Wybierz Archetyp
                    </label>
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(4, 1fr)',
                        gap: '12px'
                    }}>
                        {ARCHETYPES.map(arch => {
                            const isSelected = selectedArchetype === arch.id
                            const Icon = arch.icon
                            return (
                                <button
                                    key={arch.id}
                                    onClick={() => setSelectedArchetype(arch.id)}
                                    title={arch.label}
                                    style={{
                                        aspectRatio: '1',
                                        background: isSelected ? `linear-gradient(135deg, ${arch.color}33, ${arch.color}11)` : 'rgba(255,255,255,0.03)',
                                        border: isSelected ? `2px solid ${arch.color}` : '1px solid rgba(255,255,255,0.1)',
                                        borderRadius: '16px',
                                        display: 'flex',
                                        flexDirection: 'column',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s'
                                    }}
                                >
                                    <Icon size={24} color={isSelected ? arch.color : 'rgba(255,255,255,0.4)'} />
                                </button>
                            )
                        })}
                    </div>
                    <div style={{ textAlign: 'center', marginTop: '12px', height: '20px', color: 'rgba(255,255,255,0.5)', fontSize: '13px' }}>
                        {ARCHETYPES.find(a => a.id === selectedArchetype)?.label}
                    </div>
                </div>

                {/* Actions */}
                <button
                    onClick={handleSave}
                    disabled={saving}
                    style={{
                        width: '100%',
                        padding: '16px',
                        background: saving ? 'rgba(255,255,255,0.1)' : '#00d4ff',
                        color: saving ? 'rgba(255,255,255,0.5)' : '#000',
                        fontSize: '16px',
                        fontWeight: 700,
                        border: 'none',
                        borderRadius: '16px',
                        cursor: saving ? 'not-allowed' : 'pointer',
                        transition: 'opacity 0.2s'
                    }}
                >
                    {saving ? 'Zapisywanie...' : 'Zapisz Zmiany'}
                </button>
            </div>
        </div>
    )
}
