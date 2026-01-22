'use client'

import { useState } from 'react'
import { ArrowRight, Drill, Hammer, Zap, Check, RotateCcw, ChevronRight, Disc, Battery, Settings, PenTool } from 'lucide-react'
import data from '@/lib/data/catalog.json'
import Link from 'next/link'

// Define types based on our catalog
type Product = {
    sku: string
    name: string
    category_id: string
    system?: string
    image_url?: string
    price_msrp?: number
    features?: string[]
    specs?: Record<string, any>
    warranty_years?: number
    fuel?: boolean
}

type Category = {
    id: string
    name: string
    description: string
    icon: string
    products: Product[]
}

const catalog = data as { categories: Category[] }

export default function ProductSelectorPage() {
    const [step, setStep] = useState(1)
    const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
    const [selectedSystem, setSelectedSystem] = useState<string | null>(null)
    const [recommendedProduct, setRecommendedProduct] = useState<Product | null>(null)

    // Icons map
    const iconMap: Record<string, any> = {
        drill: Drill,
        impact: Hammer,
        saw: Disc, // Approximation
        grinder: Disc,
        battery: Battery,
        accessory: Settings,
        charger: Zap
    }

    const handleCategorySelect = (categoryId: string) => {
        setSelectedCategory(categoryId)
        // If drill, go to system selection. If others, straight to recommend (simple logic for now)
        if (categoryId === 'drills' || categoryId === 'impact_drivers' || categoryId === 'saws') {
            setStep(2)
        } else {
            // Auto recommend first product for simple categories
            const category = catalog.categories.find(c => c.id === categoryId)
            if (category && category.products.length > 0) {
                setRecommendedProduct(category.products[0])
                setStep(3)
            } else {
                // Fallback if no products
                setStep(3)
            }
        }
    }

    const handleSystemSelect = (system: string) => {
        setSelectedSystem(system)

        // Find product match
        if (selectedCategory) {
            const category = catalog.categories.find(c => c.id === selectedCategory)
            if (category) {
                // Find product matching system
                const product = category.products.find(p => p.system === system) || category.products[0]
                setRecommendedProduct(product)
                setStep(3)
            }
        }
    }

    const handleRestart = () => {
        setStep(1)
        setSelectedCategory(null)
        setSelectedSystem(null)
        setRecommendedProduct(null)
    }

    const getSystemDescription = (system: string) => {
        if (system === 'M18') return 'Maksymalna moc i wydajność'
        if (system === 'M12') return 'Kompaktowość i mobilność'
        return ''
    }

    return (
        <div style={{ minHeight: '100vh', padding: '48px 32px' }}>
            {/* Header */}
            <div style={{ marginBottom: '40px', maxWidth: '800px', margin: '0 auto 40px auto' }}>
                <Link href="/lessons" style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '8px',
                    color: 'rgba(255,255,255,0.6)',
                    textDecoration: 'none',
                    fontSize: '14px',
                    marginBottom: '16px'
                }}>
                    <ChevronRight size={14} style={{ transform: 'rotate(180deg)' }} />
                    Powrót do nauki
                </Link>
                <h1 style={{ fontSize: '36px', fontWeight: 700, marginBottom: '12px' }}>
                    <span style={{ color: '#ff0000' }}>Milwaukee</span> Product Selector
                </h1>
                <p style={{ fontSize: '18px', color: 'rgba(255, 255, 255, 0.6)' }}>
                    Znajdź idealne narzędzie do swojego zadania w 3 prostych krokach.
                </p>
            </div>

            <div style={{ maxWidth: '800px', margin: '0 auto 48px auto', display: 'flex', gap: '8px' }}>
                {[1, 2, 3].map(s => (
                    <div key={s} style={{
                        flex: 1,
                        height: '4px',
                        background: s <= step ? '#ff0000' : 'rgba(255,255,255,0.1)',
                        borderRadius: '2px',
                        transition: 'all 0.3s'
                    }} />
                ))}
            </div>

            <div style={{ maxWidth: '800px', margin: '0 auto' }}>

                {/* STEP 1: CATEGORY */}
                {step === 1 && (
                    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <h2 style={{ fontSize: '24px', fontWeight: 600, marginBottom: '32px' }}>
                            Krok 1: Jakiego rodzaju narzędzia szukasz?
                        </h2>
                        <div style={{
                            display: 'grid',
                            gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
                            gap: '24px'
                        }}>
                            {catalog.categories.map(category => {
                                const Icon = iconMap[category.icon] || PenTool
                                return (
                                    <button
                                        key={category.id}
                                        onClick={() => handleCategorySelect(category.id)}
                                        style={{
                                            background: 'rgba(255, 255, 255, 0.05)',
                                            border: '1px solid rgba(255, 255, 255, 0.1)',
                                            borderRadius: '16px',
                                            padding: '32px',
                                            display: 'flex',
                                            flexDirection: 'column',
                                            alignItems: 'center',
                                            gap: '16px',
                                            cursor: 'pointer',
                                            transition: 'all 0.2s',
                                            textAlign: 'center'
                                        }}
                                        onMouseOver={(e) => {
                                            e.currentTarget.style.borderColor = '#ff0000'
                                            e.currentTarget.style.transform = 'translateY(-4px)'
                                            e.currentTarget.style.background = 'rgba(255, 0, 0, 0.05)'
                                        }}
                                        onMouseOut={(e) => {
                                            e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)'
                                            e.currentTarget.style.transform = 'translateY(0)'
                                            e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)'
                                        }}
                                    >
                                        <div style={{
                                            width: '64px',
                                            height: '64px',
                                            borderRadius: '50%',
                                            background: '#ff0000',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            color: 'white'
                                        }}>
                                            <Icon size={32} />
                                        </div>
                                        <div>
                                            <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '8px', color: 'white' }}>
                                                {category.name}
                                            </h3>
                                            <p style={{ fontSize: '13px', color: 'rgba(255, 255, 255, 0.5)' }}>
                                                {category.description}
                                            </p>
                                        </div>
                                    </button>
                                )
                            })}
                        </div>
                    </div>
                )}

                {/* STEP 2: SYSTEM / PREFERENCE */}
                {step === 2 && (
                    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <h2 style={{ fontSize: '24px', fontWeight: 600, marginBottom: '32px' }}>
                            Krok 2: Jaki system preferujesz?
                        </h2>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '32px' }}>
                            {['M18', 'M12'].map(sys => (
                                <button
                                    key={sys}
                                    onClick={() => handleSystemSelect(sys)}
                                    style={{
                                        background: 'rgba(255, 255, 255, 0.05)',
                                        border: '1px solid rgba(255, 255, 255, 0.1)',
                                        borderRadius: '16px',
                                        padding: '40px',
                                        textAlign: 'left',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s',
                                        position: 'relative',
                                        overflow: 'hidden'
                                    }}
                                    onMouseOver={(e) => {
                                        e.currentTarget.style.borderColor = '#ff0000'
                                        e.currentTarget.style.background = 'rgba(255, 0, 0, 0.05)'
                                    }}
                                    onMouseOut={(e) => {
                                        e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)'
                                        e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)'
                                    }}
                                >
                                    <div style={{
                                        fontSize: '48px',
                                        fontWeight: 900,
                                        color: '#ff0000',
                                        marginBottom: '16px',
                                        fontStyle: 'italic'
                                    }}>
                                        {sys}
                                    </div>
                                    <h3 style={{ fontSize: '20px', fontWeight: 600, color: 'white', marginBottom: '8px' }}>
                                        {sys === 'M18' ? 'Performance Driven' : 'Portable Productivity'}
                                    </h3>
                                    <p style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.6)', lineHeight: 1.6 }}>
                                        {getSystemDescription(sys)}
                                    </p>
                                </button>
                            ))}
                        </div>
                        <button
                            onClick={() => setStep(1)}
                            style={{
                                marginTop: '32px',
                                background: 'transparent',
                                border: 'none',
                                color: 'rgba(255,255,255,0.5)',
                                cursor: 'pointer',
                                fontSize: '14px',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '8px'
                            }}
                        >
                            <ChevronRight size={14} style={{ transform: 'rotate(180deg)' }} /> Cofnij
                        </button>
                    </div>
                )}

                {/* STEP 3: RECOMMENDATION */}
                {step === 3 && recommendedProduct && (
                    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
                            <div style={{
                                width: '64px',
                                height: '64px',
                                borderRadius: '50%',
                                background: '#00ff88',
                                color: '#000',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                margin: '0 auto 16px auto',
                                boxShadow: '0 0 20px rgba(0, 255, 136, 0.3)'
                            }}>
                                <Check size={32} strokeWidth={3} />
                            </div>
                            <h2 style={{ fontSize: '28px', fontWeight: 700 }}>
                                Twoja Rekomendacja
                            </h2>
                            <p style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
                                Na podstawie Twoich wyborów, to jest idealne narzędzie:
                            </p>
                        </div>

                        {/* Product Card */}
                        <div style={{
                            background: 'rgba(20, 20, 35, 0.6)',
                            backdropFilter: 'blur(20px)',
                            border: '1px solid rgba(255, 255, 255, 0.1)',
                            borderRadius: '24px',
                            overflow: 'hidden',
                            display: 'flex',
                            flexDirection: 'column',
                            maxWidth: '600px',
                            margin: '0 auto'
                        }}>
                            {/* Mock Image Area since we don't have real images yet */}
                            <div style={{
                                height: '240px',
                                background: 'linear-gradient(135deg, #2a2a3e, #1a1a2e)',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                position: 'relative'
                            }}>
                                <span style={{ fontSize: '64px' }}>🛠️</span>
                                {recommendedProduct.fuel && (
                                    <div style={{
                                        position: 'absolute',
                                        top: '24px',
                                        right: '24px',
                                        background: '#ff0000',
                                        color: 'white',
                                        padding: '4px 12px',
                                        borderRadius: '4px',
                                        fontWeight: 900,
                                        fontStyle: 'italic',
                                        fontSize: '14px'
                                    }}>
                                        FUEL
                                    </div>
                                )}
                            </div>

                            <div style={{ padding: '32px' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
                                    <div>
                                        <div style={{
                                            fontSize: '13px',
                                            color: '#ff0000',
                                            fontWeight: 700,
                                            marginBottom: '4px',
                                            textTransform: 'uppercase',
                                            letterSpacing: '1px'
                                        }}>
                                            SKU: {recommendedProduct.sku}
                                        </div>
                                        <h3 style={{ fontSize: '24px', fontWeight: 700, lineHeight: 1.3 }}>
                                            {recommendedProduct.name}
                                        </h3>
                                    </div>
                                </div>

                                {/* Features */}
                                <div style={{ marginBottom: '24px' }}>
                                    {recommendedProduct.features?.slice(0, 3).map((feature, i) => (
                                        <div key={i} style={{ display: 'flex', gap: '12px', marginBottom: '8px', fontSize: '14px', color: 'rgba(255, 255, 255, 0.8)' }}>
                                            <div style={{ minWidth: '6px', height: '6px', borderRadius: '50%', background: '#ff0000', marginTop: '7px' }} />
                                            {feature}
                                        </div>
                                    ))}
                                </div>

                                {/* Specs Grid */}
                                <div style={{
                                    display: 'grid',
                                    gridTemplateColumns: '1fr 1fr',
                                    gap: '16px',
                                    background: 'rgba(0, 0, 0, 0.2)',
                                    padding: '16px',
                                    borderRadius: '12px',
                                    marginBottom: '32px'
                                }}>
                                    {Object.entries(recommendedProduct.specs || {}).slice(0, 4).map(([key, value]) => (
                                        <div key={key}>
                                            <div style={{ fontSize: '11px', color: 'rgba(255, 255, 255, 0.4)', textTransform: 'uppercase', marginBottom: '2px' }}>
                                                {key.replace('_', ' ')}
                                            </div>
                                            <div style={{ fontSize: '14px', fontWeight: 600 }}>
                                                {Array.isArray(value) ? value.join(', ') : value}
                                            </div>
                                        </div>
                                    ))}
                                </div>

                                <div style={{ display: 'flex', gap: '16px' }}>
                                    <button
                                        onClick={handleRestart}
                                        style={{
                                            flex: 1,
                                            padding: '14px',
                                            borderRadius: '12px',
                                            border: '1px solid rgba(255, 255, 255, 0.1)',
                                            background: 'transparent',
                                            color: 'white',
                                            cursor: 'pointer',
                                            fontWeight: 600,
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            gap: '8px'
                                        }}
                                    >
                                        <RotateCcw size={16} /> Rozpocznij od nowa
                                    </button>
                                    <button style={{
                                        flex: 1,
                                        padding: '14px',
                                        borderRadius: '12px',
                                        background: '#ff0000',
                                        border: 'none',
                                        color: 'white',
                                        fontWeight: 700,
                                        cursor: 'pointer'
                                    }}>
                                        Zobacz detale
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
