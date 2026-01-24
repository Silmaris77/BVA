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
            case 'alert': return <AlertTriangle size={18} color="#ef4444" />
            case 'warning': return <AlertTriangle size={18} color="#f59e0b" />
            case 'success': return <CheckCircle size={18} color="#00ff88" />
            default: return <Info size={18} color="#00d4ff" />
        }
    }

    const getBg = (type: string) => {
        switch (type) {
            case 'alert': return 'rgba(239, 68, 68, 0.1)'
            case 'warning': return 'rgba(245, 158, 11, 0.1)'
            case 'success': return 'rgba(0, 255, 136, 0.1)'
            default: return 'rgba(0, 212, 255, 0.1)'
        }
    }

    return (
        <div style={{
            background: 'rgba(20, 20, 35, 0.4)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            borderRadius: '20px',
            padding: '24px',
            marginBottom: '24px'
        }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
                <Bell size={20} color="#ffd700" />
                <h3 style={{ fontSize: '18px', fontWeight: 700 }}>Aktualności</h3>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {news.map(item => (
                    <div key={item.id} style={{
                        padding: '16px',
                        background: getBg(item.type),
                        borderRadius: '12px',
                        borderLeft: `4px solid ${item.type === 'alert' ? '#ef4444' : item.type === 'success' ? '#00ff88' : '#00d4ff'}`
                    }}>
                        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
                            <div style={{ marginTop: '2px' }}>
                                {getIcon(item.type)}
                            </div>
                            <div>
                                <h4 style={{ fontSize: '15px', fontWeight: 600, marginBottom: '4px' }}>
                                    {item.title}
                                </h4>
                                <p style={{ fontSize: '13px', color: 'rgba(255, 255, 255, 0.7)', lineHeight: '1.5' }}>
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
