'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { useResourceAccess } from '@/hooks/useResourceAccess'
import ToolShell from '@/components/tools/ToolShell'
import ROICalculator from '@/components/tools/ROICalculator'
import KolbTest from '@/components/tools/KolbTest'
import DegenTest from '@/components/tools/DegenTest'
import { Wrench, Lock } from 'lucide-react'
import Link from 'next/link'

interface Tool {
    id: string
    tool_id: string
    title: string
    description: string
    tier: number
    default_xp: number
    config?: any
    usage_count?: number
    lastUsage?: any
}

export default function ToolDetailPage() {
    const params = useParams()
    const router = useRouter()
    const { user, profile } = useAuth()
    const [tool, setTool] = useState<any>(null)
    const [lastUsage, setLastUsage] = useState<any>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchTool = async () => { // Renamed loadTool to fetchTool
            try {
                const res = await fetch(`/api/tools/${params.id}`) // Renamed response to res
                if (!res.ok) { // Changed response.ok to res.ok
                    console.error('Tool response not ok', res.status) // Changed response.status to res.status
                    // router.push('/tools')
                    setLoading(false)
                    return
                }
                const data = await res.json()
                setTool(data.tool)
                setLastUsage(data.lastUsage)
            } catch (err) { // Changed error to err
                console.error('Error fetching tool:', err) // Changed 'Error loading tool:' to 'Error fetching tool:'
                // router.push('/tools')
            } finally {
                setLoading(false)
            }
        }
        if (params.id) fetchTool() // Changed loadTool() to fetchTool()
    }, [params.id, router]) // Corrected dependency array

    // Access Control (Dynamic)
    const { hasAccess, loading: accessLoading } = useResourceAccess(tool?.tool_id === 'degen-test' ? 'degen-test' : '')

    // Helper functions (moved outside or defined before returns)
    const getTips = (toolId: string) => {
        if (toolId === 'degen-test') {
            return [
                'Twój typ może się zmieniać w zależności od sytuacji rynkowej (Hossa/Bessa).',
                'Kluczem do sukcesu nie jest zmiana osobowości, ale świadomość własnych pułapek.',
                'Wróć do testu za miesiąc, aby sprawdzić czy Twoje nawyki ewoluowały.'
            ]
        }
        if (toolId === 'kolb-test') {
            return [
                'Zrozumienie swojego stylu uczenia się przyspiesza przyswajanie nowej wiedzy.',
                'Spróbuj zastosować metody z innych stylów, aby poszerzyć swoje kompetencje.',
                'Wykorzystaj wynik, aby lepiej dobierać materiały edukacyjne (np. wideo vs tekst).'
            ]
        }
        return [
            'Użyj tego narzędzia, aby zwiększyć swoją samoświadomość.',
            'Regularne powtarzanie ćwiczeń buduje trwałe nawyki.',
            'Eksperymentuj z nowymi podejściami w bezpiecznym środowisku.'
        ]
    }

    const getResources = (toolId: string) => {
        if (toolId === 'degen-test') {
            return [
                { label: 'Atlas Degenów (Artykuł)', url: '/learning/resources/degen-atlas', type: 'guide' as const }
            ]
        }
        return []
    }

    const renderContent = () => {
        if (!tool) return null;
        switch (tool.tool_id) {
            case 'roi-calculator':
            case 'roi_calculator':
            case 'kalkulator-roi':
                return <ROICalculator />
            case 'kolb-test':
                return <KolbTest initialResult={lastUsage?.output_data} lastCompletedAt={lastUsage?.created_at} />
            case 'degen-test':
                return <DegenTest initialResult={lastUsage?.output_data} lastCompletedAt={lastUsage?.created_at} />
            case 'objection-handler':
                return <PlaceholderTool toolId={tool.tool_id} />
            default:
                return <PlaceholderTool toolId={tool.tool_id} />
        }
    }

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

    const tips = getTips(tool.tool_id)
    const resources = getResources(tool.tool_id)

    if (tool.tool_id === 'degen-test') {
        if (accessLoading) {
            return (
                <div className="flex items-center justify-center min-h-screen">
                    <div className="text-white/60">Sprawdzanie uprawnień...</div>
                </div>
            )
        }

        if (!hasAccess) {
            return (
                <div style={{
                    minHeight: '100vh',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    padding: '20px',
                    textAlign: 'center'
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
                        <Lock size={40} className="text-gray-400" />
                    </div>
                    <h1 className="text-2xl font-bold mb-4">Dostęp Zablokowany 🔒</h1>
                    <p className="text-gray-400 max-w-md mb-8">
                        To narzędzie jest dostępne wyłącznie dla autoryzowanych ról (np. Inwestor).
                    </p>
                    <Link
                        href="/lessons"
                        className="px-6 py-3 bg-white/10 hover:bg-white/20 rounded-xl transition-colors font-medium"
                    >
                        Wróć do nauki
                    </Link>
                </div>
            )
        }
    }

    return (
        <ToolShell tool={tool} tips={tips} resources={resources}>
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

function DiagnosticPlaceholder({ toolId, title, description }: { toolId: string; title: string; description: string }) {
    return (
        <div style={{
            background: 'rgba(20, 20, 35, 0.4)',
            backdropFilter: 'blur(15px)',
            border: '1px solid rgba(176, 0, 255, 0.2)',
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
                background: 'rgba(176, 0, 255, 0.1)',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '24px',
                fontSize: '40px'
            }}>
                🧪
            </div>
            <h3 style={{ fontSize: '24px', fontWeight: 600, color: '#fff', marginBottom: '12px' }}>
                {title}
            </h3>
            <p style={{ color: 'rgba(255,255,255,0.7)', maxWidth: '500px', lineHeight: 1.6, marginBottom: '24px' }}>
                {description}
            </p>
            <div style={{
                padding: '16px 24px',
                background: 'rgba(176, 0, 255, 0.1)',
                border: '1px solid rgba(176, 0, 255, 0.3)',
                borderRadius: '12px',
                color: '#e0aaff',
                fontSize: '14px',
                maxWidth: '450px'
            }}>
                <strong>🚧 W budowie</strong><br />
                Ten test diagnostyczny jest obecnie w fazie implementacji. Wkrótce będziesz mógł zmierzyć swoje kompetencje i zapisać wyniki do profilu.
            </div>
        </div>
    )
}
