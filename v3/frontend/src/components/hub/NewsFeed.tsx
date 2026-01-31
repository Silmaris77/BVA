'use client'

import { Bell, Info, AlertTriangle, CheckCircle } from 'lucide-react'

interface Announcement {
    id: string
    title: string
    content: string
    type: 'info' | 'alert' | 'success' | 'warning'
    created_at: string
}

interface NewsFeedProps {
    news: Announcement[]
}

export default function NewsFeed({ news }: NewsFeedProps) {
    if (!news || news.length === 0) return null

    const getIcon = (type: string) => {
        switch (type) {
            case 'alert': return <AlertTriangle size={18} color="var(--t-accent-error)" />
            case 'warning': return <AlertTriangle size={18} color="var(--t-accent-warning)" />
            case 'success': return <CheckCircle size={18} color="var(--t-accent-success)" />
            default: return <Info size={18} color="var(--t-accent)" />
        }
    }

    const getBorderColor = (type: string) => {
        switch (type) {
            case 'alert': return 'var(--t-accent-error)'
            case 'warning': return 'var(--t-accent-warning)'
            case 'success': return 'var(--t-accent-success)'
            default: return 'var(--t-accent)'
        }
    }

    return (
        <div className="theme-card-glass" style={{ marginBottom: '24px' }}>
            <div className="theme-section-header" style={{ marginBottom: '20px' }}>
                <Bell size={20} style={{ color: 'var(--t-accent-warning)' }} />
                <h3 style={{ fontSize: '18px', fontWeight: 700, color: 'var(--t-text)' }}>
                    Aktualności
                </h3>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {news.map(item => (
                    <div 
                        key={item.id} 
                        style={{
                            padding: '16px',
                            background: 'var(--t-card-bg)',
                            borderRadius: '12px',
                            borderLeft: `4px solid ${getBorderColor(item.type)}`
                        }}
                    >
                        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
                            <div style={{ marginTop: '2px' }}>
                                {getIcon(item.type)}
                            </div>
                            <div>
                                <h4 style={{ 
                                    fontSize: '15px', 
                                    fontWeight: 600, 
                                    marginBottom: '4px',
                                    color: 'var(--t-text)'
                                }}>
                                    {item.title}
                                </h4>
                                <p style={{ 
                                    fontSize: '13px', 
                                    color: 'var(--t-text-muted)', 
                                    lineHeight: '1.5' 
                                }}>
                                    {item.content}
                                </p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}
