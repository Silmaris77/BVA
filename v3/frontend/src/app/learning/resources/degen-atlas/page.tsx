'use client'

import { DEGEN_TYPES, DegenTypeKey } from '@/data/degen-types'
import { ArrowLeft, BookOpen, Trophy, AlertTriangle, Target, Lock } from 'lucide-react'
import Link from 'next/link'
import { useResourceAccess } from '@/hooks/useResourceAccess'

export default function DegenAtlasPage() {
    const { hasAccess, loading: accessLoading } = useResourceAccess('degen-atlas')

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
                    Ten artykuł jest dostępny wyłącznie dla autoryzowanych ról (np. Inwestor).
                </p>
                <Link
                    href="/resources"
                    className="px-6 py-3 bg-white/10 hover:bg-white/20 rounded-xl transition-colors font-medium"
                >
                    Wróć do zasobów
                </Link>
            </div>
        )
    }
    return (
        <div style={{ minHeight: '100vh', padding: '40px 24px', maxWidth: '1200px', margin: '0 auto' }}>
            {/* Navigation */}
            <Link
                href="/resources"
                className="inline-flex items-center gap-2 px-4 py-2 bg-white/5 rounded-lg text-white/70 hover:bg-white/10 hover:text-white transition-colors mb-8"
            >
                <ArrowLeft size={16} />
                Powrót do zasobów
            </Link>

            {/* Header */}
            <header className="mb-16 text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-500 to-indigo-600 mb-6 shadow-lg shadow-purple-500/20">
                    <BookOpen size={32} className="text-white" />
                </div>
                <h1 className="text-4xl md:text-5xl font-bold text-white mb-6">
                    Atlas Degenów 🌍
                </h1>
                <p className="text-xl text-gray-400 max-w-2xl mx-auto leading-relaxed">
                    Poznaj 8 archetypów inwestorów. Zrozum ich supermoce, słabości i strategie, które pomogą Ci przetrwać na rynku. Pamiętaj – każdy typ może zarabiać, jeśli jest świadomy swojej natury.
                </p>
            </header>

            {/* Content Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {(Object.entries(DEGEN_TYPES) as [DegenTypeKey, typeof DEGEN_TYPES[DegenTypeKey]][]).map(([key, details]) => (
                    <div
                        key={key}
                        className="bg-[#13131f] rounded-3xl overflow-hidden border border-white/5 hover:border-white/10 transition-colors"
                    >
                        {/* Card Header */}
                        <div
                            className="p-8 relative overflow-hidden"
                            style={{ background: `linear-gradient(135deg, ${details.color}20, transparent)` }}
                        >
                            <div className="absolute top-0 right-0 p-8 opacity-10 scale-150 transform translate-x-4 -translate-y-4">
                                <span className="text-9xl">{details.icon}</span>
                            </div>

                            <div className="relative z-10">
                                <div className="text-4xl mb-4">{details.icon}</div>
                                <h2 className="text-2xl font-bold text-white mb-2" style={{ color: details.color }}>
                                    {key}
                                </h2>
                                <p className="text-gray-300 leading-relaxed">
                                    {details.description}
                                </p>
                            </div>
                        </div>

                        {/* Card Body */}
                        <div className="p-8 pt-6 space-y-6">
                            {/* Strengths */}
                            <div>
                                <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-2">
                                    <Trophy size={14} className="text-green-500" />
                                    Mocne Strony
                                </h3>
                                <div className="flex flex-wrap gap-2">
                                    {details.strengths.map((str, i) => (
                                        <span key={i} className="px-3 py-1 bg-green-500/10 text-green-400 rounded-full text-xs font-medium border border-green-500/10">
                                            {str}
                                        </span>
                                    ))}
                                </div>
                            </div>

                            {/* Challenges */}
                            <div>
                                <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-2">
                                    <AlertTriangle size={14} className="text-orange-500" />
                                    Wyzwania
                                </h3>
                                <ul className="space-y-2">
                                    {details.challenges.map((chal, i) => (
                                        <li key={i} className="text-sm text-gray-400 flex items-start gap-2">
                                            <span className="w-1 h-1 rounded-full bg-orange-500 mt-2 shrink-0" />
                                            {chal}
                                        </li>
                                    ))}
                                </ul>
                            </div>

                            {/* Strategy */}
                            <div className="pt-6 border-t border-white/5">
                                <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-2">
                                    <Target size={14} className="text-blue-500" />
                                    Strategia
                                </h3>
                                <p className="text-sm text-blue-200/80 bg-blue-500/10 p-4 rounded-xl border border-blue-500/20 italic">
                                    "{details.strategy}"
                                </p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Footer */}
            <div className="mt-16 text-center pb-8 border-t border-white/5 pt-8">
                <p className="text-gray-500 text-sm">
                    ZenDegen Academy © 2024 • BrainVenture Application
                </p>
            </div>
        </div>
    )
}
