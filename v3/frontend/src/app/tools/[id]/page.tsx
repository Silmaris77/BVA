'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import ToolShell from '@/components/tools/ToolShell'
import ROICalculator from '@/components/tools/ROICalculator'
import { Wrench } from 'lucide-react'

interface Tool {
    id: string
    tool_id: string
    title: string
    description: string
    tier: number
    default_xp: number
    config?: any
    usage_count?: number
}

export default function ToolDetailPage() {
    const params = useParams()
    const router = useRouter()
    const [tool, setTool] = useState<Tool | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function loadTool() {
            try {
                const response = await fetch(`/api/tools/${params.id}`)
                if (!response.ok) {
                    console.error('Tool response not ok', response.status)
                    // router.push('/tools')
                    setLoading(false)
                    return
                }
                const data = await response.json()
                setTool(data.tool)
            } catch (error) {
                console.error('Error loading tool:', error)
                // router.push('/tools')
            } finally {
                setLoading(false)
            }
        }
        if (params.id) loadTool()
    }, [params.id, router])

    if (loading) {
        return (
            <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <div style={{ color: 'rgba(255,255,255,0.6)' }}>Ładowanie...</div>
            </div>
        )
    }

    if (!tool) return (
        <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <div style={{ textAlign: 'center' }}>
                <h1 style={{ color: 'white', marginBottom: '10px' }}>Nie znaleziono narzędzia</h1>
                <p style={{ color: 'rgba(255,255,255,0.6)' }}>ID: {JSON.stringify(params.id)}</p>
                <button onClick={() => router.push('/tools')} style={{ marginTop: '20px', padding: '10px 20px', background: '#333', color: 'white', border: 'none', borderRadius: '5px' }}>Wróć</button>
            </div>
        </div>
    )

    // Render content based on tool ID
    const renderContent = () => {
        switch (tool.tool_id) {
            case 'roi-calculator':
            case 'roi_calculator':
            case 'kalkulator-roi':
                return <ROICalculator />

            // Future tools go here...
            case 'objection-handler':
                // return <ObjectionHandler />
                return <PlaceholderTool toolId={tool.tool_id} />

            default:
                return <PlaceholderTool toolId={tool.tool_id} />
        }
    }

    // Default tips (can be enriched from DB closer to production)
    const defaultTips = [
        'Użyj tego narzędzia podczas rozmowy z klientem.',
        'Możesz eksportować wyniki do PDF.',
        'Każde użycie zwiększa Twój poziom ekspercki.'
    ]

    return (
        <ToolShell tool={tool} tips={defaultTips}>
            {renderContent()}
        </ToolShell>
    )
}

function PlaceholderTool({ toolId }: { toolId: string }) {
    return (
        <div style={{
            background: 'rgba(20, 20, 35, 0.4)',
            backdropFilter: 'blur(15px)',
            border: '1px solid rgba(255,255,255,0.08)',
            borderRadius: '20px',
            padding: '48px',
            textAlign: 'center',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '400px'
        }}>
            <div style={{
                width: '80px',
                height: '80px',
                background: 'rgba(255, 255, 255, 0.05)',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '24px'
            }}>
                <Wrench size={40} style={{ color: 'rgba(255, 255, 255, 0.4)' }} />
            </div>
            <h3 style={{ fontSize: '20px', fontWeight: 600, color: '#fff', marginBottom: '12px' }}>
                W trakcie budowy
            </h3>
            <p style={{ color: 'rgba(255,255,255,0.6)', maxWidth: '400px', lineHeight: 1.6 }}>
                To narzędzie ({toolId}) jest obecnie w fazie implementacji. Sprawdź ponownie wkrótce!
            </p>
        </div>
    )
}
