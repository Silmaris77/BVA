"use client";

import React, { useState, useEffect } from 'react';
import {
    Download,
    Zap,
    CheckCircle,
    Clock,
    AlertCircle,
    Filter
} from 'lucide-react';
import { fetchImplants, type NeuralImplant } from '@/utils/implants-api';

export default function ImplantsPage() {
    const [implants, setImplants] = useState<NeuralImplant[]>([]);
    const [categories, setCategories] = useState<string[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedCategory, setSelectedCategory] = useState<string>('all');

    useEffect(() => {
        async function loadImplants() {
            try {
                const data = await fetchImplants();
                setImplants(data.implants);
                setCategories(data.categories);
                setLoading(false);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to load implants');
                setLoading(false);
            }
        }
        loadImplants();
    }, []);

    const filteredImplants = selectedCategory === 'all'
        ? implants
        : implants.filter(i => i.category === selectedCategory);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-screen w-full">
                <div className="text-white text-2xl">
                    <Zap className="animate-pulse w-16 h-16 mx-auto mb-4" />
                    <p>Loading Neural Implants...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex items-center justify-center h-screen w-full">
                <div className="glass-card p-8 max-w-md text-center">
                    <AlertCircle className="w-16 h-16 mx-auto mb-4 text-[#ff0055]" />
                    <p className="text-[rgba(255,255,255,0.6)]">{error}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="main" style={{ padding: '2rem' }}>
            {/* Header */}
            <div style={{ marginBottom: '2rem' }}>
                <h1 style={{ fontSize: '3rem', fontWeight: 700, margin: 0, marginBottom: '0.5rem' }}>
                    Neural Implants
                </h1>
                <p style={{ color: 'var(--text-muted)', fontSize: '1rem' }}>
                    Download and calibrate business skills directly into your neural architecture
                </p>
            </div>

            {/* Filter Bar */}
            <div style={{
                display: 'flex',
                gap: '1rem',
                marginBottom: '2rem',
                alignItems: 'center'
            }}>
                <Filter size={20} style={{ color: 'var(--neon-blue)' }} />
                <button
                    onClick={() => setSelectedCategory('all')}
                    className={selectedCategory === 'all' ? 'btn-glow' : 'btn-glow'}
                    style={{
                        background: selectedCategory === 'all' ? 'var(--neon-purple)' : 'transparent',
                        borderColor: selectedCategory === 'all' ? 'var(--neon-purple)' : 'rgba(255,255,255,0.2)'
                    }}
                >
                    All ({implants.length})
                </button>
                {categories.map(cat => (
                    <button
                        key={cat}
                        onClick={() => setSelectedCategory(cat)}
                        className="btn-glow"
                        style={{
                            background: selectedCategory === cat ? 'var(--neon-purple)' : 'transparent',
                            borderColor: selectedCategory === cat ? 'var(--neon-purple)' : 'rgba(255,255,255,0.2)'
                        }}
                    >
                        {cat} ({implants.filter(i => i.category === cat).length})
                    </button>
                ))}
            </div>

            {/* Implants Grid */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
                gap: '1.5rem'
            }}>
                {filteredImplants.map(implant => (
                    <ImplantCard key={implant.id} implant={implant} />
                ))}
            </div>

            {filteredImplants.length === 0 && (
                <div className="glass-card" style={{ padding: '3rem', textAlign: 'center' }}>
                    <p style={{ color: 'var(--text-muted)' }}>
                        No implants found in this category
                    </p>
                </div>
            )}
        </div>
    );
}

function ImplantCard({ implant }: { implant: NeuralImplant }) {
    const statusConfig = {
        available: { color: 'var(--text-muted)', icon: Download, label: 'Available' },
        downloading: { color: 'var(--neon-blue)', icon: Clock, label: 'Downloading' },
        calibration: { color: 'var(--neon-gold)', icon: Zap, label: 'Calibration' },
        active: { color: 'var(--neon-purple)', icon: CheckCircle, label: 'Active' },
        degraded: { color: 'var(--neon-red)', icon: AlertCircle, label: 'Degraded' }
    };

    const config = statusConfig[implant.status];
    const StatusIcon = config.icon;

    return (
        <div className="glass-card" style={{
            padding: '1.5rem',
            borderLeft: `3px solid ${config.color}`,
            transition: 'all 0.3s',
            cursor: 'pointer'
        }}>
            {/* Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
                <div>
                    <h3 style={{ margin: 0, fontSize: '1.2rem', fontWeight: 700 }}>{implant.name}</h3>
                    <div style={{
                        display: 'flex',
                        gap: '0.5rem',
                        alignItems: 'center',
                        marginTop: '0.5rem',
                        fontSize: '0.85rem'
                    }}>
                        <span style={{
                            background: 'rgba(255,255,255,0.1)',
                            padding: '0.2rem 0.6rem',
                            borderRadius: '4px',
                            fontSize: '0.75rem'
                        }}>
                            {implant.category}
                        </span>
                        <span style={{ color: 'var(--text-muted)' }}>{implant.difficulty}</span>
                    </div>
                </div>
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    color: config.color,
                    fontSize: '0.9rem',
                    fontWeight: 600
                }}>
                    <StatusIcon size={18} />
                    {config.label}
                </div>
            </div>

            {/* Description */}
            <p style={{
                color: 'var(--text-muted)',
                fontSize: '0.9rem',
                marginBottom: '1rem',
                lineHeight: 1.5
            }}>
                {implant.description}
            </p>

            {/* Progress Bar (if applicable) */}
            {implant.progress > 0 && implant.progress < 100 && (
                <div style={{ marginBottom: '1rem' }}>
                    <div style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        fontSize: '0.8rem',
                        marginBottom: '0.5rem'
                    }}>
                        <span>Progress</span>
                        <span style={{ color: config.color }}>{implant.progress}%</span>
                    </div>
                    <div style={{
                        height: '6px',
                        background: 'rgba(255,255,255,0.1)',
                        borderRadius: '3px',
                        overflow: 'hidden'
                    }}>
                        <div style={{
                            height: '100%',
                            width: `${implant.progress}%`,
                            background: `linear-gradient(90deg, ${config.color}, var(--neon-blue))`,
                            transition: 'width 0.3s'
                        }} />
                    </div>
                </div>
            )}

            {/* Footer */}
            <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                paddingTop: '1rem',
                borderTop: '1px solid rgba(255,255,255,0.05)'
            }}>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                    <div>⏱️ {implant.estimated_time}</div>
                    <div style={{ color: 'var(--neon-gold)' }}>💎 +{implant.skill_points} SP</div>
                </div>
                <button className="btn-glow" style={{
                    fontSize: '0.85rem',
                    padding: '0.5rem 1rem'
                }}>
                    {implant.status === 'available' && 'Download'}
                    {implant.status === 'downloading' && 'Continue'}
                    {implant.status === 'calibration' && 'Calibrate'}
                    {implant.status === 'active' && 'Review'}
                    {implant.status === 'degraded' && 'Re-calibrate'}
                </button>
            </div>
        </div>
    );
}
