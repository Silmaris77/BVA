'use client';

import { useState } from 'react';
import { Battery, BatteryCharging, BatteryFull, BatteryMedium, TrendingUp, Zap, HelpCircle, CheckCircle, Brain, Target } from 'lucide-react';

interface ReadinessLevel {
    id: string; // R1, R2, R3, R4
    title: string;
    subtitle: string;
    competence: 'low' | 'some' | 'high';
    commitment: 'high' | 'low' | 'variable';
    description: string;
    needs: string; // What they need from leader
    color: string;
    icon: any;
}

const levels: ReadinessLevel[] = [
    {
        id: 'R1',
        title: 'Entuzjastyczny Debiutant',
        subtitle: '„Nie umiem, ale chcę”',
        competence: 'low',
        commitment: 'high',
        description: 'Brak doświadczenia nadrabia zapałem. Często nieświadomy trudności (Szczyt Głupoty).',
        needs: 'Instruktaż (S1) - Konkretne polecenia, co i jak robić. Mało wsparcia emocjonalnego (bo zapał jest).',
        color: '#fbbf24', // Amber
        icon: Zap // Energy
    },
    {
        id: 'R2',
        title: 'Rozczarowany Adept',
        subtitle: '„Nie umiem i już mi się nie chce”',
        competence: 'some',
        commitment: 'low',
        description: 'Pierwsze porażki. Zderzenie z rzeczywistością. Frustracja (Dolina Rozpaczy).',
        needs: 'Trenowanie (S2) - Wyjaśnianie decyzji, dużo wsparcia, chwalenie postępów.',
        color: '#ef4444', // Red
        icon: HelpCircle // Doubt
    },
    {
        id: 'R3',
        title: 'Ostrożny Praktyk',
        subtitle: '„Umiem, ale się boję”',
        competence: 'high', // effectively high but insecure
        commitment: 'variable',
        description: 'Ma kompetencje, ale brakuje mu pewności siebie lub motywacji. Wahania formy.',
        needs: 'Wspieranie (S3) - Słuchanie, zachęcanie do samodzielności, budowanie pewności.',
        color: '#3b82f6', // Blue
        icon: TrendingUp // Improving
    },
    {
        id: 'R4',
        title: 'Samodzielny Ekspert',
        subtitle: '„Umiem i chcę”',
        competence: 'high',
        commitment: 'high',
        description: 'Ekspert. Działa samodzielnie, skutecznie i z pasją.',
        needs: 'Delegowanie (S4) - Wolna ręka, zaufanie, wyzwania, autonomia.',
        color: '#10b981', // Emerald
        icon: Target // Mastery
    }
];

export default function ReadinessCard({
    title = 'Poziomy Gotowości (R1-R4)',
    description = 'Dopasuj styl zarządzania do poziomu pracownika. Kliknij kartę, aby zobaczyć szczegóły.',
    imageSrc = '/lessons/ojt/Poziomy Gotowości.png' // Default fallback
}: { title?: string; description?: string, imageSrc?: string }) {
    const [activeId, setActiveId] = useState<string>('R1');
    const activeLevel = levels.find(l => l.id === activeId) || levels[0];

    return (
        <div className="w-full max-w-5xl mx-auto glass-card p-4 md:p-8 rounded-2xl border border-white/10 flex flex-col gap-6 relative overflow-hidden">

            {/* Header */}
            <div className="flex flex-col md:flex-row items-center justify-between gap-4 z-10 relative">
                <div className="flex-1 text-center md:text-left">
                    <h2 className="text-2xl md:text-3xl font-black bg-gradient-to-r from-white via-blue-200 to-blue-400 bg-clip-text text-transparent tracking-tight">
                        {title}
                    </h2>
                    <p className="text-gray-400 text-sm md:text-base font-medium mt-1">{description}</p>
                </div>
            </div>

            {/* Content Area */}
            <div className="relative min-h-[400px] w-full flex flex-col md:flex-row gap-6 mt-4">

                {/* Matrix View */}
                {/* Visual Grid (Left) */}
                <div className="flex-1 grid grid-cols-2 grid-rows-2 gap-3 h-[320px] md:h-[400px] flex-shrink-0 animate-[fadeIn_0.5s_ease-out]">
                    {levels.map((level) => {
                        const isActive = activeId === level.id;
                        const Icon = level.icon;

                        return (
                            <div
                                key={level.id}
                                onClick={() => setActiveId(level.id)}
                                className={`relative rounded-xl border transition-all duration-300 cursor-pointer flex flex-col items-center justify-center p-4 group overflow-hidden ${isActive
                                        ? 'bg-white/10 border-white/40 shadow-[0_0_20px_rgba(59,130,246,0.3)] scale-[1.02] z-10'
                                        : 'bg-black/40 border-white/5 hover:border-white/20 hover:bg-white/5'
                                    }`}
                                style={{ borderColor: isActive ? level.color : undefined }}
                            >
                                {/* Background Splatter */}
                                <div
                                    className={`absolute inset-0 opacity-0 transition-opacity duration-500 ${isActive ? 'opacity-20' : 'group-hover:opacity-10'}`}
                                    style={{ background: `radial-gradient(circle at center, ${level.color}, transparent 70%)` }}
                                />

                                <div className="z-10 bg-black/50 p-3 rounded-full mb-3 backdrop-blur-sm transition-transform duration-300 group-hover:scale-110" style={{ color: level.color }}>
                                    <Icon size={32} />
                                </div>

                                <h3 className="text-xl font-bold text-white z-10">{level.id}</h3>
                                <span className="text-[10px] uppercase tracking-widest text-gray-400 z-10 font-bold mt-1 text-center hidden md:block">{level.title}</span>

                                {isActive && (
                                    <div className="absolute top-2 right-2">
                                        <div className="w-2 h-2 rounded-full animate-ping" style={{ backgroundColor: level.color }} />
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>

                {/* Details Panel (Right) */}
                <div className="flex-1 bg-white/5 border border-white/10 rounded-xl p-6 md:p-8 backdrop-blur-md flex flex-col justify-center animate-[slideLeft_0.4s_ease-out] relative overflow-hidden min-h-[300px]">
                    {/* Ambient Glow */}
                    <div
                        className="absolute -top-20 -right-20 w-80 h-80 rounded-full blur-[100px] pointer-events-none transition-colors duration-700 opacity-20"
                        style={{ background: activeLevel.color }}
                    />

                    <div className="relative z-10">
                        <div className="flex items-center gap-3 mb-2">
                            <span className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-br from-white to-gray-400 tracking-tighter">
                                {activeLevel.id}
                            </span>
                            <div className="h-8 w-px bg-white/20 mx-2" />
                            <div>
                                <h3 className="text-xl font-bold text-white leading-none">{activeLevel.title}</h3>
                                <p className="text-sm text-gray-400 italic mt-0.5">{activeLevel.subtitle}</p>
                            </div>
                        </div>

                        <div className="mt-6 space-y-4">
                            <div>
                                <div className="flex items-center justify-between text-xs font-bold text-gray-500 uppercase tracking-widest mb-1">
                                    <span>Kompetencje</span>
                                    <span className={activeLevel.competence === 'high' ? 'text-green-400' : activeLevel.competence === 'some' ? 'text-yellow-400' : 'text-red-400'}>
                                        {activeLevel.competence === 'high' ? 'Wysokie' : activeLevel.competence === 'some' ? 'Średnie' : 'Niskie'}
                                    </span>
                                </div>
                                <div className="h-1.5 w-full bg-white/10 rounded-full overflow-hidden">
                                    <div
                                        className="h-full rounded-full transition-all duration-1000"
                                        style={{
                                            width: activeLevel.competence === 'high' ? '100%' : activeLevel.competence === 'some' ? '50%' : '20%',
                                            backgroundColor: activeLevel.color
                                        }}
                                    />
                                </div>
                            </div>

                            <div>
                                <div className="flex items-center justify-between text-xs font-bold text-gray-500 uppercase tracking-widest mb-1">
                                    <span>Zaangażowanie</span>
                                    <span className={activeLevel.commitment === 'high' ? 'text-green-400' : activeLevel.commitment === 'variable' ? 'text-yellow-400' : 'text-red-400'}>
                                        {activeLevel.commitment === 'high' ? 'Wysokie' : activeLevel.commitment === 'variable' ? 'Zmienne' : 'Niskie'}
                                    </span>
                                </div>
                                <div className="h-1.5 w-full bg-white/10 rounded-full overflow-hidden">
                                    <div
                                        className="h-full rounded-full transition-all duration-1000 delay-100"
                                        style={{
                                            width: activeLevel.commitment === 'high' ? '100%' : activeLevel.commitment === 'variable' ? '60%' : '30%',
                                            backgroundColor: activeLevel.color
                                        }}
                                    />
                                </div>
                            </div>
                        </div>

                        <div className="mt-8 bg-black/20 rounded-lg p-4 border-l-2" style={{ borderColor: activeLevel.color }}>
                            <p className="text-gray-300 leading-relaxed text-sm md:text-base">
                                {activeLevel.description}
                            </p>
                        </div>

                        <div className="mt-4 flex items-center gap-3 text-sm font-medium text-white/80">
                            <Target size={18} className="text-gray-400" />
                            <span>Potrzebuje: <strong className="text-white">{activeLevel.needs}</strong></span>
                        </div>
                    </div>
                </div>
            </div>
            <style jsx global>{`
                @keyframes fadeIn {
                    from { opacity: 0; transform: scale(0.98); }
                    to { opacity: 1; transform: scale(1); }
                }
                @keyframes slideLeft {
                    from { opacity: 0; transform: translateX(20px); }
                    to { opacity: 1; transform: translateX(0); }
                }
            `}</style>
        </div>
    );
}
