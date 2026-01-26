'use client';

import { useState, useEffect } from 'react';
import { Target, TrendingUp, CheckCircle, Sparkles } from 'lucide-react';

interface PathLevel {
    stage: number;
    title: string;
    subtitle: string;
    details?: string;
    status: 'completed' | 'current' | 'locked';
    color: string;
}

interface LearningPathCardProps {
    title?: string;
    description?: string;
    levels?: PathLevel[];
}

const defaultLevels: PathLevel[] = [
    {
        stage: 0,
        title: 'START',
        subtitle: 'Nie wiem, że nie umiem',
        details: 'Etap początkowy. Dopiero odkrywasz, jak wiele jest jeszcze do nauczenia. To moment inspiracji i pierwszej styczności z tematem.',
        status: 'completed',
        color: '#00d4ff'
    },
    {
        stage: 1,
        title: 'Poziom I',
        subtitle: 'Nieświadoma niekompetencja',
        details: 'Zaczynasz rozumieć podstawy, ale popełniasz błędy, z których jeszcze nie zdajesz sobie sprawy. To czas eksperymentowania.',
        status: 'completed',
        color: '#7dd956'
    },
    {
        stage: 2,
        title: 'Poziom II',
        subtitle: 'Świadoma niekompetencja\nWiem, że nie umiem',
        details: 'Kluczowy moment kryzysu i wzrostu. Wiesz już, czego nie potrafisz, i aktywnie szukasz wiedzy, by te braki uzupełnić.',
        status: 'current',
        color: '#ffaa00'
    },
    {
        stage: 3,
        title: 'Poziom III',
        subtitle: 'Świadoma kompetencja\nWiem, że umiem',
        details: 'Potrafisz wykonać zadanie poprawnie, ale wymaga to od Ciebie skupienia i wysiłku. Twoje umiejętności są solidne, ale nie automatyczne.',
        status: 'locked',
        color: '#7dd956'
    },
    {
        stage: 4,
        title: 'META',
        subtitle: 'Nieświadoma kompetencja\nNie wiem, że umiem',
        details: 'Mistrzostwo. Działasz intuicyjnie, szybko i bezbłędnie. Twoja wiedza stała się drugą naturą.',
        status: 'locked',
        color: '#DA291C'
    }
];

export default function LearningPathCard({
    title = 'Ścieżka Rozwoju',
    description = 'Twoja droga od początkującego do eksperta',
    levels = defaultLevels
}: LearningPathCardProps) {
    const [activeStage, setActiveStage] = useState<number>(0);
    const [animWidth, setAnimWidth] = useState(0);

    const getProgressWidth = (stageIndex: number) => {
        const xPositions = [10, 30, 50, 70, 90];
        return xPositions[stageIndex] || 0;
    };

    useEffect(() => {
        const targetWidth = getProgressWidth(activeStage);
        setAnimWidth(targetWidth);
    }, [activeStage]);

    const getIcon = (stage: number) => {
        if (stage === 0) return Target;
        if (stage === 4) return Sparkles;
        return stage <= 2 ? TrendingUp : CheckCircle;
    };

    const activeLevelData = levels.find(l => l.stage === activeStage) || levels[0];

    // Updated Path Coordinates to lift curve and fix dip
    // M 100 320 -> Start higher (was 350)
    // Points: (100,320), (300, 260), (500, 200), (700, 140), (900, 60)
    const pathDefinition = "M 100 320 Q 200 320, 300 260 T 500 200 T 700 140 T 900 60";

    return (
        <div className="w-full max-w-5xl mx-auto glass-card p-8 md:p-12 rounded-2xl border border-white/10 flex flex-col gap-8 relative overflow-hidden group">
            {/* Ambient Background Glow - Reduced Intensity */}
            <div
                className="absolute w-[500px] h-[500px] rounded-full blur-[90px] opacity-15 transition-all duration-1000 pointer-events-none"
                style={{
                    background: activeLevelData.color,
                    left: `${getProgressWidth(activeStage)}%`,
                    top: '50%',
                    transform: 'translate(-50%, -50%)'
                }}
            />

            {/* Header */}
            <div className="text-center relative z-10">
                <h2 className="text-4xl font-black bg-gradient-to-r from-white via-gray-200 to-gray-400 bg-clip-text text-transparent mb-3 tracking-tight drop-shadow-lg">
                    {title}
                </h2>
                <p className="text-gray-400 text-lg font-medium">{description}</p>
            </div>

            {/* Interactive SVG Path */}
            <div className="relative w-full h-[300px] md:h-[400px] select-none z-10">
                <svg
                    className="absolute inset-0 w-full h-full drop-shadow-[0_0_15px_rgba(0,0,0,0.5)]"
                    viewBox="0 0 1000 400"
                    preserveAspectRatio="xMidYMid meet"
                >
                    <defs>
                        {/* Define gradients */}
                        <linearGradient id="pathGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#00d4ff" />
                            <stop offset="50%" stopColor="#7dd956" />
                            <stop offset="100%" stopColor="#DA291C" />
                        </linearGradient>

                        <linearGradient id="activeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor={activeLevelData.color} stopOpacity="0" />
                            <stop offset="50%" stopColor={activeLevelData.color} />
                            <stop offset="100%" stopColor={activeLevelData.color} stopOpacity="0" />
                        </linearGradient>

                        <clipPath id="progressClip">
                            <rect
                                x="0"
                                y="0"
                                width={`${animWidth}%`}
                                height="400"
                                className="transition-all duration-1000 ease-in-out"
                            />
                        </clipPath>

                        <filter id="neon-glow" x="-50%" y="-50%" width="200%" height="200%">
                            <feGaussianBlur stdDeviation="3" result="coloredBlur" />
                            <feMerge>
                                <feMergeNode in="coloredBlur" />
                                <feMergeNode in="SourceGraphic" />
                            </feMerge>
                        </filter>
                    </defs>

                    {/* Inactive Track - Dashed */}
                    <path
                        d={pathDefinition}
                        fill="none"
                        stroke="rgba(255,255,255,0.05)"
                        strokeWidth="8"
                        strokeLinecap="round"
                    />
                    <path
                        d={pathDefinition}
                        fill="none"
                        stroke="rgba(255,255,255,0.15)"
                        strokeWidth="2"
                        strokeDasharray="4 8"
                        strokeLinecap="round"
                    />

                    {/* Active Path - Animated Flow */}
                    <path
                        d={pathDefinition}
                        fill="none"
                        stroke="url(#pathGradient)"
                        strokeWidth="6"
                        strokeLinecap="round"
                        filter="url(#neon-glow)"
                        clipPath="url(#progressClip)"
                        className="transition-all duration-500"
                    />

                    {/* Travelling Pulse Effect */}
                    <path
                        d={pathDefinition}
                        fill="none"
                        stroke="white"
                        strokeWidth="2"
                        strokeDasharray="20 980"
                        strokeDashoffset={-10 * animWidth} // Move dash based on progress
                        strokeOpacity="0.5"
                        clipPath="url(#progressClip)"
                        className="transition-all duration-1000 ease-out"
                        style={{ strokeDashoffset: -10 * animWidth }}
                    />

                    {/* Milestone Nodes */}
                    {levels.map((level, index) => {
                        const Icon = getIcon(level.stage);
                        const xPositions = [100, 300, 500, 700, 900];
                        // MATCH Y POSITIONS WITH PATH DEFINITION
                        // (100,320), (300, 260), (500, 200), (700, 140), (900, 60)
                        const yPositions = [320, 260, 200, 140, 60];
                        const x = xPositions[index];
                        const y = yPositions[index];
                        const isActive = activeStage === level.stage;
                        const isPast = index < activeStage;

                        return (
                            <foreignObject
                                key={level.stage}
                                x={x - 60}
                                y={y - 60}
                                width="120"
                                height="120"
                                style={{ overflow: 'visible' }}
                            >
                                <div
                                    className="w-full h-full flex items-center justify-center relative cursor-pointer group"
                                    onClick={() => setActiveStage(level.stage)}
                                >
                                    {/* Ripple Effect for active node - Centered absolutely */}
                                    {isActive && (
                                        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none">
                                            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-24 h-24 rounded-full animate-ping opacity-20" style={{ background: level.color }} />
                                            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-32 h-32 rounded-full animate-pulse opacity-10" style={{ background: level.color }} />
                                        </div>
                                    )}

                                    {/* Main Node Circle */}
                                    <div
                                        className={`relative z-20 w-16 h-16 rounded-full flex items-center justify-center border-[3px] transition-all duration-500 backdrop-blur-sm ${isActive
                                                ? 'scale-125 bg-black/40 border-white shadow-[0_0_25px_rgba(255,255,255,0.3)]'
                                                : isPast
                                                    ? 'scale-100 bg-black/60 border-transparent shadow-[0_0_10px_rgba(0,0,0,0.2)]'
                                                    : 'scale-90 bg-black/80 border-white/10 hover:scale-105 hover:border-white/30'
                                            }`}
                                        style={{
                                            boxShadow: isActive ? `0 0 30px ${level.color}50, inset 0 0 20px ${level.color}30` : (isPast ? `0 0 10px ${level.color}30` : ''),
                                            color: isActive ? '#fff' : (isPast ? level.color : '#666')
                                        }}
                                    >
                                        <Icon
                                            size={isActive ? 28 : 22}
                                            className={`transition-all duration-300 ${isActive ? 'drop-shadow-[0_0_10px_rgba(255,255,255,0.8)]' : ''}`}
                                        />

                                        {/* Inner ring for aesthetic */}
                                        {isActive && (
                                            <div className="absolute inset-1 rounded-full border border-white/20 animate-[spin_10s_linear_infinite]" />
                                        )}
                                    </div>

                                    {/* Stage Label - Absolute below center */}
                                    <div
                                        className={`absolute top-[75%] left-1/2 -translate-x-1/2 px-3 py-1.5 rounded-lg text-xs font-bold tracking-wider uppercase transition-all duration-500 whitespace-nowrap z-20 ${isActive
                                                ? 'bg-white text-black translate-y-3 scale-110 shadow-lg'
                                                : 'bg-black/40 text-gray-500 backdrop-blur-md border border-white/5 translate-y-1 group-hover:text-white group-hover:border-white/20'
                                            }`}
                                    >
                                        {level.title}
                                    </div>
                                </div>
                            </foreignObject>
                        );
                    })}
                </svg>
            </div>

            {/* Details Panel - Glassmorphism & Smooth Transition */}
            <div className="bg-gradient-to-br from-white/10 to-black/20 border border-white/10 rounded-2xl p-8 backdrop-blur-xl shadow-2xl transition-all duration-500 min-h-[220px] relative overflow-hidden">
                {/* Decorative accent line */}
                <div className="absolute top-0 left-0 w-1 h-full transition-all duration-500" style={{ background: activeLevelData.color, boxShadow: `0 0 20px ${activeLevelData.color}` }} />

                <div className="flex flex-col md:flex-row gap-8 items-start relative z-10">

                    {/* Big Icon Animated */}
                    <div
                        key={`icon-${activeStage}`} // Force remount for animation
                        className="w-20 h-20 rounded-2xl flex items-center justify-center flex-shrink-0 animate-[fadeIn_0.5s_ease-out] shadow-2xl border border-white/10"
                        style={{
                            background: `linear-gradient(135deg, ${activeLevelData.color}20, transparent)`,
                            color: activeLevelData.color,
                            boxShadow: `inset 0 0 30px ${activeLevelData.color}10`
                        }}
                    >
                        {(() => {
                            const Icon = getIcon(activeLevelData.stage);
                            return <Icon size={44} className="drop-shadow-lg" />;
                        })()}
                    </div>

                    <div className="flex-1">
                        <div className="animate-[slideRight_0.4s_ease-out]">
                            <h3 className="text-3xl font-bold text-white mb-2 tracking-tight">
                                {activeLevelData.title}
                            </h3>

                            <h4
                                className="text-xl font-medium mb-4 flex items-center gap-3"
                                style={{ color: activeLevelData.color }}
                            >
                                {activeLevelData.subtitle.replace('\n', ' • ')}
                            </h4>

                            <p
                                key={`text-${activeStage}`} // Animate text change
                                className="text-gray-300 leading-relaxed text-lg max-w-3xl animate-[fadeIn_0.6s_ease-out]"
                            >
                                {activeLevelData.details || activeLevelData.subtitle}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <style jsx global>{`
                @keyframes fadeIn {
                    from { opacity: 0; transform: scale(0.95); }
                    to { opacity: 1; transform: scale(1); }
                }
                @keyframes slideRight {
                    from { opacity: 0; transform: translateX(-20px); }
                    to { opacity: 1; transform: translateX(0); }
                }
            `}</style>
        </div>
    );
}
