'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/contexts/AuthContext'
import {
    ArrowLeft,
    FileText,
    Download,
    BookOpen,
    Table,
    FileSpreadsheet,
    ExternalLink,
    Printer,
    Mail,
    Calendar,
    CheckCircle,
    Lightbulb,
    Eye
} from 'lucide-react'

interface Resource {
    id: string
    resource_id: string
    title: string
    description: string
    resource_type: 'pdf' | 'guide' | 'table' | 'template'
    file_url?: string
    content?: any
    download_count?: number
    page_count?: number
    last_updated?: string
    verified?: boolean
    related_tools?: Array<{
        tool_id: string
        title: string
    }>
    related_lessons?: Array<{
        lesson_id: string
        title: string
    }>
}

export default function ResourceDetailPage() {
    const params = useParams()
    const router = useRouter()
    const { user, loading: authLoading } = useAuth()
    const [resource, setResource] = useState<Resource | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (!authLoading && !user) {
            router.push('/auth/login')
            return
        }

        async function loadResource() {
            try {
                const response = await fetch(`/api/resources/${params.id}`)
                if (!response.ok) {
                    router.push('/resources')
                    return
                }
                const data = await response.json()
                setResource(data.resource)
            } catch (error) {
                console.error('Error loading resource:', error)
                router.push('/resources')
            } finally {
                setLoading(false)
            }
        }
        if (params.id && user) loadResource()
    }, [params.id, router, user, authLoading])

    const handleDownload = () => {
        if (resource?.file_url) {
            window.open(resource.file_url, '_blank')
        } else {
            console.log('Download initiated for resource:', resource?.resource_id)
        }
    }

    const handlePrint = () => {
        window.print()
    }

    const handleEmail = () => {
        const subject = encodeURIComponent(`BrainVenture - ${resource?.title}`)
        const body = encodeURIComponent(`Sprawdź ten zasób: ${window.location.href}`)
        window.location.href = `mailto:?subject=${subject}&body=${body}`
    }

    const getTypeInfo = (type: string) => {
        const types = {
            pdf: { label: 'PDF', color: '#ff4444', bg: 'rgba(255,68,68,0.2)', icon: FileText },
            guide: { label: 'Poradnik', color: '#b000ff', bg: 'rgba(176,0,255,0.2)', icon: BookOpen },
            table: { label: 'Tabela', color: '#00d4ff', bg: 'rgba(0,212,255,0.2)', icon: Table },
            template: { label: 'Szablon', color: '#ffd700', bg: 'rgba(255,215,0,0.2)', icon: FileSpreadsheet }
        }
        return types[type as keyof typeof types] || types.pdf
    }

    if (loading) {
        return (
            <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <div style={{ color: 'rgba(255,255,255,0.6)' }}>Ładowanie...</div>
            </div>
        )
    }

    if (!resource) return null

    const typeInfo = getTypeInfo(resource.resource_type)
    const Icon = typeInfo.icon

    return (
        <div style={{ minHeight: '100vh', padding: '40px 48px', maxWidth: '1200px', margin: '0 auto' }}>
            {/* Back Button */}
            <Link
                href="/resources"
                style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '10px 16px',
                    background: 'rgba(255,255,255,0.05)',
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: '10px',
                    color: 'rgba(255,255,255,0.8)',
                    textDecoration: 'none',
                    marginBottom: '32px',
                    transition: 'all 0.3s'
                }}
            >
                <ArrowLeft size={16} />
                Powrót do zasobów
            </Link>

            {/* Resource Header */}
            <div style={{
                background: 'rgba(20, 20, 35, 0.4)',
                backdropFilter: 'blur(15px)',
                border: '1px solid rgba(255,255,255,0.08)',
                borderRadius: '20px',
                padding: '32px',
                marginBottom: '32px',
                position: 'relative',
                overflow: 'hidden'
            }}>
                {/* Top Border */}
                <div style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '4px',
                    background: 'linear-gradient(90deg, #00ff88, #00cc66)'
                }} />

                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '20px', marginBottom: '20px' }}>
                    <div style={{
                        width: '72px',
                        height: '72px',
                        background: typeInfo.bg,
                        borderRadius: '18px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        flexShrink: 0
                    }}>
                        <Icon size={36} style={{ color: typeInfo.color }} />
                    </div>
                    <div style={{ flex: 1 }}>
                        <h1 style={{ fontSize: '32px', fontWeight: 700, marginBottom: '8px' }}>
                            {resource.title}
                        </h1>
                        <span style={{
                            display: 'inline-block',
                            padding: '6px 14px',
                            background: typeInfo.bg,
                            color: typeInfo.color,
                            borderRadius: '16px',
                            fontSize: '12px',
                            fontWeight: 600,
                            textTransform: 'uppercase'
                        }}>
                            {typeInfo.label}
                        </span>
                    </div>
                </div>

                <p style={{ color: 'rgba(255,255,255,0.7)', fontSize: '16px', lineHeight: 1.6 }}>
                    {resource.description}
                </p>

                {/* Meta Information */}
                <div style={{
                    display: 'flex',
                    gap: '24px',
                    fontSize: '14px',
                    color: 'rgba(255, 255, 255, 0.6)',
                    marginTop: '16px',
                    flexWrap: 'wrap'
                }}>
                    {resource.download_count !== undefined && (
                        <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                            <Download size={16} />
                            {resource.download_count.toLocaleString('pl-PL')} pobrań
                        </span>
                    )}
                    {resource.page_count && (
                        <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                            <FileText size={16} />
                            {resource.page_count} {resource.page_count === 1 ? 'strona' : resource.page_count < 5 ? 'strony' : 'stron'}
                        </span>
                    )}
                    {resource.last_updated && (
                        <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                            <Calendar size={16} />
                            Zaktualizowano: {new Date(resource.last_updated).toLocaleDateString('pl-PL')}
                        </span>
                    )}
                    {resource.verified && (
                        <span style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#00ff88' }}>
                            <CheckCircle size={16} />
                            Zweryfikowano przez ekspertów
                        </span>
                    )}
                </div>

                {/* Action Buttons */}
                <div style={{ display: 'flex', gap: '12px', marginTop: '24px', flexWrap: 'wrap' }}>
                    <button
                        onClick={handleDownload}
                        style={{
                            padding: '12px 24px',
                            background: 'linear-gradient(135deg, #00ff88, #00cc66)',
                            border: 'none',
                            borderRadius: '12px',
                            color: 'white',
                            fontSize: '14px',
                            fontWeight: 600,
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            transition: 'all 0.3s'
                        }}
                    >
                        <Download size={18} />
                        Pobierz PDF
                    </button>
                    <button
                        onClick={handlePrint}
                        style={{
                            padding: '12px 24px',
                            background: 'rgba(255,255,255,0.05)',
                            border: '1px solid rgba(255,255,255,0.1)',
                            borderRadius: '12px',
                            color: 'rgba(255,255,255,0.8)',
                            fontSize: '14px',
                            fontWeight: 600,
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            transition: 'all 0.3s'
                        }}
                    >
                        <Printer size={18} />
                        Drukuj
                    </button>
                    <button
                        onClick={handleEmail}
                        style={{
                            padding: '12px 24px',
                            background: 'rgba(255,255,255,0.05)',
                            border: '1px solid rgba(255,255,255,0.1)',
                            borderRadius: '12px',
                            color: 'rgba(255,255,255,0.8)',
                            fontSize: '14px',
                            fontWeight: 600,
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            transition: 'all 0.3s'
                        }}
                    >
                        <Mail size={18} />
                        Wyślij email
                    </button>
                </div>
            </div>

            {/* Content Panel */}
            <div style={{
                background: 'rgba(20, 20, 35, 0.4)',
                backdropFilter: 'blur(15px)',
                border: '1px solid rgba(255,255,255,0.08)',
                borderRadius: '20px',
                padding: '32px'
            }}>
                <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '20px', color: '#00ff88' }}>
                    Podgląd zasobu
                </h3>

                {/* Placeholder Content */}
                <div style={{
                    padding: '48px',
                    background: 'rgba(0,0,0,0.2)',
                    borderRadius: '16px',
                    textAlign: 'center',
                    border: '2px dashed rgba(0,255,136,0.3)'
                }}>
                    <Icon size={48} style={{ color: 'rgba(0,255,136,0.5)', margin: '0 auto 16px' }} />
                    <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: '14px' }}>
                        Pełna zawartość {typeInfo.label.toLowerCase()} zostanie wyświetlona tutaj
                    </p>
                    <p style={{ color: 'rgba(255,255,255,0.4)', fontSize: '12px', marginTop: '8px' }}>
                        {resource.resource_type === 'pdf' && 'Podgląd PDF z możliwością przewijania'}
                        {resource.resource_type === 'guide' && 'Formatowany przewodnik krok po kroku'}
                        {resource.resource_type === 'table' && 'Interaktywna tabela z danymi'}
                        {resource.resource_type === 'template' && 'Podgląd szablonu do pobrania'}
                    </p>
                </div>

                {/* Additional Info / Tips */}
                {(resource.content?.notes || resource.resource_type === 'table') && (
                    <div style={{
                        background: 'rgba(0,212,255,0.1)',
                        border: '1px solid rgba(0,212,255,0.3)',
                        borderRadius: '12px',
                        padding: '16px',
                        marginTop: '24px'
                    }}>
                        <h4 style={{
                            color: '#00d4ff',
                            marginBottom: '8px',
                            fontSize: '14px',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px'
                        }}>
                            <Lightbulb size={16} />
                            Ważne wskazówki
                        </h4>
                        <p style={{ color: 'rgba(255,255,255,0.7)', fontSize: '13px', lineHeight: 1.6 }}>
                            {resource.content?.notes || (
                                <>
                                    • Zasób jest dostępny dla wszystkich użytkowników<br />
                                    • Możesz pobrać lub wydrukować ten zasób<br />
                                    • Regularnie aktualizowany przez ekspertów
                                </>
                            )}
                        </p>
                    </div>
                )}
            </div>

            {/* Related Content */}
            {(resource.related_tools?.length || resource.related_lessons?.length) ? (
                <div style={{
                    marginTop: '32px',
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
                    gap: '20px'
                }}>
                    {resource.related_tools && resource.related_tools.length > 0 && (
                        <div style={{
                            background: 'rgba(20, 20, 35, 0.4)',
                            backdropFilter: 'blur(15px)',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            borderRadius: '20px',
                            padding: '24px'
                        }}>
                            <h3 style={{
                                fontSize: '18px',
                                fontWeight: 600,
                                marginBottom: '16px',
                                color: '#00ff88'
                            }}>
                                Powiązane narzędzia
                            </h3>
                            <ul style={{
                                listStyle: 'none',
                                padding: 0,
                                margin: 0
                            }}>
                                {resource.related_tools.map((tool) => (
                                    <li key={tool.tool_id} style={{ marginBottom: '8px' }}>
                                        <Link
                                            href={`/tools/${tool.tool_id}`}
                                            style={{
                                                color: 'rgba(255, 255, 255, 0.8)',
                                                textDecoration: 'none',
                                                transition: 'color 0.3s'
                                            }}
                                        >
                                            → {tool.title}
                                        </Link>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}

                    {resource.related_lessons && resource.related_lessons.length > 0 && (
                        <div style={{
                            background: 'rgba(20, 20, 35, 0.4)',
                            backdropFilter: 'blur(15px)',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            borderRadius: '20px',
                            padding: '24px'
                        }}>
                            <h3 style={{
                                fontSize: '18px',
                                fontWeight: 600,
                                marginBottom: '16px',
                                color: '#00d4ff'
                            }}>
                                Powiązane lekcje
                            </h3>
                            <ul style={{
                                listStyle: 'none',
                                padding: 0,
                                margin: 0
                            }}>
                                {resource.related_lessons.map((lesson) => (
                                    <li key={lesson.lesson_id} style={{ marginBottom: '8px' }}>
                                        <Link
                                            href={`/lessons/${lesson.lesson_id}`}
                                            style={{
                                                color: 'rgba(255, 255, 255, 0.8)',
                                                textDecoration: 'none',
                                                transition: 'color 0.3s'
                                            }}
                                        >
                                            → {lesson.title}
                                        </Link>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            ) : null}
        </div>
    )
}
