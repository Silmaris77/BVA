'use client';

import { useState } from 'react';
import { RotateCw, Lightbulb, Brain, Target, CheckCircle, ArrowRight, Settings } from 'lucide-react';

interface CycleStep {
    id: number;
    title: string;
    description: string;
    icon?: 'lightbulb' | 'brain' | 'target' | 'check' | 'rotate';
    color?: string;
}

interface CycleCardProps {
    title?: string;
    description?: string;
    steps?: CycleStep[];
    cycleType?: 'kolb' | 'pdca' | 'ooda' | 'custom';
}

const defaultKolbSteps: CycleStep[] = [
    { id: 1, title: 'Doświadczenie', description: 'Konkretne zdarzenie', icon: 'target', color: '#00d4ff' },
    { id: 2, title: 'Refleksja', description: 'Analiza sytuacji', icon: 'brain', color: '#7dd956' },
    { id: 3, title: 'Teoria', description: 'Wyciągnięcie wniosków', icon: 'lightbulb', color: '#ffd700' },
    { id: 4, title: 'Eksperyment', description: 'Plan działania', icon: 'check', color: '#ff0055' }
];

const iconMap = {
    lightbulb: Lightbulb,
    brain: Brain,
    target: Target,
    check: CheckCircle,
    rotate: RotateCw
};

export default function CycleCardVariantB({
    title = 'Cykl Uczenia się',
    description = 'Proces ciągłego doskonalenia',
    steps = defaultKolbSteps,
}: CycleCardProps) {
    const [activeStep, setActiveStep] = useState(0);

    const activeStepData = steps[activeStep];
    const totalSteps = steps.length;

    // Grid positions for Reactor Layout
    const getPosition = (index: number) => {
        const angle = (index / totalSteps) * 2 * Math.PI - Math.PI / 2;
        const radius = 100; // px
        const x = 150 + radius * Math.cos(angle);
        const y = 150 + radius * Math.sin(angle);
        return { x, y, angle };
    };

    return (
        <div className="w-full max-w-5xl mx-auto glass-card p-6 md:p-10 rounded-2xl border border-white/10 flex flex-col items-center relative overflow-hidden">
            {/* Dynamic Background Mesh */}
            <div className="absolute inset-0 opacity-20 pointer-events-none">
                <div
                    className="absolute w-[600px] h-[600px] bg-gradient-to-r from-transparent via-current to-transparent opacity-20 blur-[80px] transition-all duration-700 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
                    style={{ color: activeStepData.color }}
                />
            </div>

            {/* Header */}
            <div className="text-center mb-10 z-10 w-full max-w-2xl">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-mono text-gray-400 mb-3 uppercase tracking-widest">
                    <span>Variant B: Reactor Core</span>
                </div>
                <h2 className="text-3xl md:text-4xl font-black bg-gradient-to-br from-white via-gray-200 to-gray-500 bg-clip-text text-transparent mb-3">
                    {title}
                </h2>
                <p className="text-gray-400 font-light">{description}</p>
            </div>

            {/* Main Content Layout */}
            <div className="flex flex-col md:flex-row items-center gap-12 w-full z-10">

                {/* Visual Side (Left/Top) */}
                <div className="relative w-[320px] h-[320px] flex-shrink-0">
                    <svg viewBox="0 0 300 300" className="w-full h-full drop-shadow-2xl overflow-visible">
                        <defs>
                            <filter id="glow-b">
                                <feGaussianBlur stdDeviation="3" result="coloredBlur" />
                                <feMerge>
                                    <feMergeNode in="coloredBlur" />
                                    <feMergeNode in="SourceGraphic" />
                                </feMerge>
                            </filter>
                            <linearGradient id="orbitGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stopColor="white" stopOpacity="0" />
                                <stop offset="50%" stopColor="white" stopOpacity="1" />
                                <stop offset="100%" stopColor="white" stopOpacity="0" />
                            </linearGradient>
                        </defs>

                        {/* Connection Ring - Static */}
                        <circle cx="150" cy="150" r="100" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="20" />

                        {/* ORBIT ANIMATION */}
                        {/* Rotating Group for particle - Slowed down to 12s */}
                        <g className="animate-[spin_12s_linear_infinite] origin-center" style={{ transformOrigin: '150px 150px' }}>
                            {/* The Particle */}
                            <circle cx="150" cy="50" r="4" fill="white" filter="url(#glow-b)" className="drop-shadow-[0_0_8px_rgba(255,255,255,1)]" />
                            {/* A trailing tail (fading arc) could be complex in SVG, let's stick to a simple particle or a second trailing one */}
                            <circle cx="140" cy="51" r="2" fill="white" opacity="0.5" />
                            <circle cx="132" cy="54" r="1" fill="white" opacity="0.2" />
                        </g>

                        {/* Step Segments */}
                        {steps.map((step, index) => {
                            const { x, y } = getPosition(index);
                            const isActive = activeStep === index;
                            const Icon = iconMap[step.icon || 'target'];

                            return (
                                <foreignObject
                                    key={step.id}
                                    x={x - 40}
                                    y={y - 40}
                                    width="80"
                                    height="80"
                                    className="overflow-visible"
                                >
                                    <div
                                        className="w-full h-full flex items-center justify-center cursor-pointer group relative"
                                        onClick={() => setActiveStep(index)}
                                        onMouseEnter={() => setActiveStep(index)}
                                    >
                                        {/* Outer Circle Ring - REDUCED SCALE (110% instead of 125%) */}
                                        <div
                                            className={`absolute inset-0 rounded-full border-2 transition-all duration-500 ${isActive
                                                ? 'scale-110 border-white bg-black/50 shadow-[0_0_20px_rgba(255,255,255,0.3)]'
                                                : 'scale-90 border-white/10 bg-black/80 hover:border-white/40'
                                                }`}
                                            style={{
                                                borderColor: isActive ? step.color : undefined,
                                                boxShadow: isActive ? `0 0 30px ${step.color}60` : undefined
                                            }}
                                        />

                                        {/* Icon */}
                                        <div className={`relative z-10 transition-all duration-300 ${isActive ? 'text-white scale-110' : 'text-gray-500 scale-100'}`}>
                                            <Icon size={24} />
                                        </div>

                                        {/* Number Badge */}
                                        <div
                                            className={`absolute -top-1 -right-1 w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold border border-black z-20 transition-all duration-300 ${isActive ? 'bg-white text-black scale-110' : 'bg-gray-800 text-gray-400'
                                                }`}
                                        >
                                            {step.id}
                                        </div>
                                    </div>
                                </foreignObject>
                            )
                        })}

                        {/* Center Core - SVG implementation to avoid square clipping */}
                        {/* Glow Gradient */}
                        <defs>
                            <radialGradient id="coreGlow" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
                                <stop offset="0%" stopColor={activeStepData.color} stopOpacity="0.5" />
                                <stop offset="100%" stopColor={activeStepData.color} stopOpacity="0" />
                            </radialGradient>
                        </defs>

                        {/* Outer Glow Circle */}
                        <circle cx="150" cy="150" r="60" fill="url(#coreGlow)" className="transition-all duration-700" opacity="0.6" />

                        {/* Core Circle Background */}
                        <circle
                            cx="150"
                            cy="150"
                            r="40"
                            fill="rgba(0,0,0,0.3)"
                            stroke={activeStepData.color}
                            strokeWidth="2"
                            strokeOpacity="0.4"
                            className="transition-all duration-700"
                        />

                        {/* Icon Container */}
                        <foreignObject x="110" y="110" width="80" height="80">
                            <div className="w-full h-full flex items-center justify-center">
                                <Settings
                                    className="animate-[spin_12s_linear_infinite] transition-colors duration-700"
                                    color={activeStepData.color}
                                    style={{ opacity: 0.8 }}
                                    size={40}
                                />
                            </div>
                        </foreignObject>
                    </svg>
                </div>

                {/* Details Side (Right/Bottom) */}
                <div className="flex-1 w-full relative">
                    {/* Animated card swap effect */}
                    <div className="relative min-h-[200px] bg-white/5 border border-white/10 rounded-2xl p-8 backdrop-blur-md overflow-hidden">

                        {/* Subtle Corner Glow */}
                        <div
                            className="absolute -top-20 -right-20 w-60 h-60 rounded-full blur-[80px] pointer-events-none transition-colors duration-500 opacity-20"
                            style={{ background: activeStepData.color }}
                        />

                        <div key={activeStep} className="animate-[slideUp_0.4s_ease-out] relative z-10">
                            <div className="flex items-center gap-3 mb-4">
                                <span
                                    className="text-xs font-bold uppercase tracking-wider px-2 py-1 rounded"
                                    style={{ background: `${activeStepData.color}33`, color: activeStepData.color }}
                                >
                                    Faza {activeStep + 1}
                                </span>
                                <div className="h-px flex-1 bg-white/10" />
                            </div>

                            <h3 className="text-3xl font-bold text-white mb-4">
                                {activeStepData.title}
                            </h3>

                            <p className="text-gray-300 text-lg leading-relaxed mb-6">
                                {activeStepData.description}
                            </p>

                            <button
                                onClick={() => setActiveStep((prev) => (prev + 1) % steps.length)}
                                className="flex items-center gap-2 text-sm font-bold transition-colors hover:gap-3"
                                style={{ color: activeStepData.color }}
                            >
                                Następny krok <ArrowRight size={16} />
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <style jsx global>{`
                @keyframes slideUp {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
            `}</style>
        </div>
    );
}
