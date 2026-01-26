'use client';

import { useState } from 'react';
import { RotateCw, Lightbulb, Brain, Target, CheckCircle } from 'lucide-react';

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
    {
        id: 1,
        title: 'Konkretne doświadczenie',
        description: 'Podejmuję jakieś działanie, uczestniczę w jakimś zdarzeniu.',
        icon: 'target',
        color: '#7dd956'
    },
    {
        id: 2,
        title: 'Refleksja',
        description: 'Myślę o tym co się stało. Analizuję przyczyny, działania i skutki.',
        icon: 'brain',
        color: '#7dd956'
    },
    {
        id: 3,
        title: 'Generalizowanie',
        description: 'Wyciągam wnioski, definiuję prawidłowości.',
        icon: 'lightbulb',
        color: '#7dd956'
    },
    {
        id: 4,
        title: 'Zastosowanie',
        description: 'Próbuję działać inaczej, sprawdzam się.',
        icon: 'check',
        color: '#7dd956'
    }
];

const iconMap = {
    lightbulb: Lightbulb,
    brain: Brain,
    target: Target,
    check: CheckCircle,
    rotate: RotateCw
};

export default function CycleCard({
    title = 'Cykl Uczenia się Kolba',
    description = 'Poznaj 4-etapowy proces skutecznego uczenia się',
    steps = defaultKolbSteps,
    cycleType = 'kolb'
}: CycleCardProps) {
    const [activeStep, setActiveStep] = useState(0);
    const stepCount = steps.length;

    // Calculate positions in a circle
    const getStepPosition = (index: number) => {
        const angle = (index / stepCount) * 2 * Math.PI - Math.PI / 2; // Start from top
        const radius = 35; // Percentage from center
        const x = 50 + radius * Math.cos(angle);
        const y = 50 + radius * Math.sin(angle);
        return { x, y, angle };
    };

    const activeStepData = steps[activeStep];

    return (
        <div className="w-full max-w-4xl mx-auto glass-card p-8 md:p-12 rounded-2xl border border-white/10 relative overflow-hidden">
            {/* Ambient Background */}
            <div
                className="absolute w-96 h-96 rounded-full blur-[100px] opacity-10 transition-all duration-1000 pointer-events-none"
                style={{
                    background: activeStepData.color || '#7dd956',
                    left: '50%',
                    top: '50%',
                    transform: 'translate(-50%, -50%)'
                }}
            />

            {/* Header */}
            <div className="text-center mb-8 relative z-10">
                <h2 className="text-3xl font-bold bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent mb-2">
                    {title}
                </h2>
                <p className="text-gray-400 text-lg">{description}</p>
            </div>

            {/* Circular Diagram */}
            <div className="relative w-full aspect-square max-w-2xl mx-auto mb-8">
                <svg
                    className="absolute inset-0 w-full h-full"
                    viewBox="0 0 100 100"
                    style={{ transform: 'rotate(-90deg)' }}
                >
                    <defs>
                        {/* Arrow marker */}
                        <marker
                            id="arrowhead"
                            markerWidth="10"
                            markerHeight="10"
                            refX="9"
                            refY="3"
                            orient="auto"
                        >
                            <polygon points="0 0, 10 3, 0 6" fill="url(#cycleGradient)" />
                        </marker>

                        {/* Gradient for arrows */}
                        <linearGradient id="cycleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#00d4ff" />
                            <stop offset="100%" stopColor="#7dd956" />
                        </linearGradient>

                        {/* Glow filter */}
                        <filter id="glow">
                            <feGaussianBlur stdDeviation="2" result="coloredBlur" />
                            <feMerge>
                                <feMergeNode in="coloredBlur" />
                                <feMergeNode in="SourceGraphic" />
                            </feMerge>
                        </filter>
                    </defs>

                    {/* Central circle (background) */}
                    <circle
                        cx="50"
                        cy="50"
                        r="30"
                        fill="none"
                        stroke="rgba(255,255,255,0.05)"
                        strokeWidth="0.3"
                    />

                    {/* Connecting arrows between steps */}
                    {steps.map((_, index) => {
                        const start = getStepPosition(index);
                        const end = getStepPosition((index + 1) % stepCount);
                        
                        // Calculate control points for curved arrow
                        const midX = 50;
                        const midY = 50;
                        
                        // Use quadratic bezier curve towards center
                        const pathD = `M ${start.x} ${start.y} Q ${midX} ${midY}, ${end.x} ${end.y}`;

                        const isPast = index < activeStep;
                        const isCurrent = index === activeStep;

                        return (
                            <path
                                key={`arrow-${index}`}
                                d={pathD}
                                fill="none"
                                stroke={isCurrent ? 'url(#cycleGradient)' : (isPast ? '#7dd95650' : 'rgba(255,255,255,0.1)')}
                                strokeWidth={isCurrent ? '0.8' : '0.4'}
                                markerEnd={isCurrent ? 'url(#arrowhead)' : undefined}
                                filter={isCurrent ? 'url(#glow)' : undefined}
                                className="transition-all duration-500"
                                strokeDasharray={isCurrent ? '0' : '2 2'}
                            />
                        );
                    })}
                </svg>

                {/* Step nodes positioned absolutely */}
                {steps.map((step, index) => {
                    const { x, y } = getStepPosition(index);
                    const Icon = iconMap[step.icon || 'rotate'];
                    const isActive = activeStep === index;
                    const isPast = index < activeStep;

                    return (
                        <div
                            key={step.id}
                            className="absolute cursor-pointer group"
                            style={{
                                left: `${x}%`,
                                top: `${y}%`,
                                transform: 'translate(-50%, -50%)'
                            }}
                            onClick={() => setActiveStep(index)}
                        >
                            {/* Pulse ring for active */}
                            {isActive && (
                                <div className="absolute inset-0 w-20 h-20 -m-2">
                                    <div
                                        className="absolute inset-0 rounded-full animate-ping opacity-20"
                                        style={{ background: step.color }}
                                    />
                                </div>
                            )}

                            {/* Main node */}
                            <div
                                className={`relative w-16 h-16 rounded-full flex items-center justify-center border-[3px] transition-all duration-500 backdrop-blur-md ${
                                    isActive
                                        ? 'scale-125 bg-black/40 border-white shadow-2xl'
                                        : isPast
                                        ? 'scale-100 bg-black/60 border-transparent'
                                        : 'scale-90 bg-black/80 border-white/10 hover:scale-105'
                                }`}
                                style={{
                                    boxShadow: isActive
                                        ? `0 0 30px ${step.color}70, inset 0 0 20px ${step.color}30`
                                        : undefined,
                                    color: isActive ? '#fff' : isPast ? step.color : '#666'
                                }}
                            >
                                <Icon size={isActive ? 28 : 22} />

                                {/* Step number badge */}
                                <div
                                    className="absolute -top-1 -right-1 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold border-2 border-black"
                                    style={{
                                        background: isActive ? step.color : '#333',
                                        color: '#fff'
                                    }}
                                >
                                    {step.id}
                                </div>
                            </div>

                            {/* Step label */}
                            <div
                                className={`absolute top-20 left-1/2 -translate-x-1/2 px-3 py-1.5 rounded-lg text-xs font-bold uppercase whitespace-nowrap transition-all duration-300 ${
                                    isActive
                                        ? 'bg-white text-black scale-105'
                                        : 'bg-black/60 text-gray-500 backdrop-blur-md border border-white/5 group-hover:text-white'
                                }`}
                            >
                                {step.title.length > 20 ? step.title.substring(0, 18) + '...' : step.title}
                            </div>
                        </div>
                    );
                })}

                {/* Central icon */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-20 h-20 rounded-full bg-gradient-to-br from-white/10 to-black/20 border border-white/10 flex items-center justify-center backdrop-blur-xl">
                    <RotateCw
                        size={32}
                        className="text-cyan-400 animate-[spin_10s_linear_infinite]"
                    />
                </div>
            </div>

            {/* Details Panel */}
            <div className="bg-gradient-to-br from-white/10 to-black/20 border border-white/10 rounded-xl p-6 backdrop-blur-xl shadow-xl relative overflow-hidden">
                <div
                    className="absolute top-0 left-0 w-1 h-full transition-all duration-500"
                    style={{
                        background: activeStepData.color,
                        boxShadow: `0 0 15px ${activeStepData.color}`
                    }}
                />

                <div className="flex items-start gap-6">
                    {/* Icon */}
                    <div
                        className="w-16 h-16 rounded-xl flex items-center justify-center flex-shrink-0 shadow-lg border border-white/10"
                        style={{
                            background: `linear-gradient(135deg, ${activeStepData.color}20, transparent)`,
                            color: activeStepData.color
                        }}
                    >
                        {(() => {
                            const Icon = iconMap[activeStepData.icon || 'rotate'];
                            return <Icon size={32} />;
                        })()}
                    </div>

                    {/* Text */}
                    <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                            <span
                                className="px-2 py-1 rounded-md text-xs font-bold"
                                style={{
                                    background: `${activeStepData.color}20`,
                                    color: activeStepData.color
                                }}
                            >
                                Krok {activeStepData.id}
                            </span>
                            <h3 className="text-xl font-bold text-white">
                                {activeStepData.title}
                            </h3>
                        </div>
                        <p className="text-gray-300 leading-relaxed">
                            {activeStepData.description}
                        </p>
                    </div>
                </div>

                {/* Navigation dots */}
                <div className="flex justify-center gap-2 mt-6">
                    {steps.map((_, index) => (
                        <button
                            key={index}
                            onClick={() => setActiveStep(index)}
                            className={`w-2 h-2 rounded-full transition-all duration-300 ${
                                activeStep === index
                                    ? 'w-8 bg-white'
                                    : 'bg-white/20 hover:bg-white/40'
                            }`}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}
