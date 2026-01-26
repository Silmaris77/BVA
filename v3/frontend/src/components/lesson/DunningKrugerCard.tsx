'use client';

import { useState, useEffect } from 'react';
import { TrendingUp, AlertTriangle, Lightbulb, Trophy, HelpCircle } from 'lucide-react';

interface ChartPoint {
    stage: number;
    title: string;
    label: string;
    description: string;
    details: string;
    color: string;
}

interface DunningKrugerCardProps {
    title?: string;
    description?: string;
    points?: ChartPoint[];
}

const defaultPoints: ChartPoint[] = [
    {
        stage: 0,
        title: 'Szczyt Głupoty',
        label: 'Pewność siebie',
        description: 'Wysoka pewność, niska wiedza',
        details: 'Paradoksalnie, gdy wiemy najmniej, czujemy się najpewniej. Nie dostrzegamy trudności i złożoności tematu. To niebezpieczny moment dla menedżera.',
        color: '#ef4444' // Red - Danger
    },
    {
        stage: 1,
        title: 'Dolina Rozpaczy',
        label: 'Zwątpienie',
        description: 'Spadek pewności, wzrost wiedzy',
        details: 'Zderzenie z rzeczywistością. Uświadamiasz sobie, jak wiele jeszcze nie wiesz. Motywacja spada, pojawia się frustracja.',
        color: '#f59e0b' // Orange - Caution
    },
    {
        stage: 2,
        title: 'Droga Oświecenia',
        label: 'Zrozumienie',
        description: 'Rośnie wiedza i pewność',
        details: 'Dzięki praktyce i nauce zaczynasz rozumieć zależności. Pewność siebie powoli wraca, ale tym razem jest poparta realnymi umiejętnościami.',
        color: '#10b981' // Green - Growth
    },
    {
        stage: 3,
        title: 'Płaskowyż Stabilności',
        label: 'Ekspert',
        description: 'Wysoka wiedza i stabilna pewność',
        details: 'Wiedza stała się intuicją. Działasz pewnie i skutecznie, ale masz w sobie pokorę eksperta.',
        color: '#3b82f6' // Blue - Stability
    }
];

export default function DunningKrugerCard({
    title = 'Efekt Krugera-Dunninga',
    description = 'Dlaczego ignoranci czują się ekspertami?',
    points = defaultPoints
}: DunningKrugerCardProps) {
    const [activeStage, setActiveStage] = useState<number>(0);
    const [animPercent, setAnimPercent] = useState(0);

    const getProgressPercent = (stageIndex: number) => {
        const percentages = [25, 50, 75, 100];
        return percentages[stageIndex] || 0;
    };

    useEffect(() => {
        const target = getProgressPercent(activeStage);
        setAnimPercent(target);
    }, [activeStage]);

    const getIcon = (stage: number) => {
        if (stage === 0) return AlertTriangle;
        if (stage === 1) return HelpCircle;
        if (stage === 2) return Lightbulb;
        return Trophy;
    };

    const activePoint = points.find(p => p.stage === activeStage) || points[0];

    // FINAL GEOMETRY FIXES
    // Explicit curves to avoid "humps" or "dips"
    // 1. Peak (250, 80)
    // 2. Valley (500, 320)
    // 3. Slope (750, 180)
    // 4. Plateau (900, 120) - Ensure this last segment is monontonically rising (decreasing Y)
    // Curve: (750, 180) -> CP(825, 120) -> (900, 120)
    // CP y=120 ensures it flattens out towards the end without going above 120.
    const pathDefinition = "M 50 320 Q 150 50, 250 80 Q 350 110, 500 320 Q 650 320, 750 180 Q 825 120, 900 120";

    const pointPositions = [
        { x: 250, y: 80 },
        { x: 500, y: 320 },
        { x: 750, y: 180 },
        { x: 900, y: 120 }
    ];

    const activePos = pointPositions[activeStage] || pointPositions[0];

    return (
        <div className="w-full max-w-5xl mx-auto glass-card p-4 md:p-8 rounded-2xl border border-white/10 flex flex-col gap-4 md:gap-6 relative overflow-hidden group">

            {/* Header */}
            <div className="text-center relative z-10 px-2 md:px-4">
                <h2 className="text-2xl md:text-3xl font-black bg-gradient-to-r from-white via-gray-200 to-gray-400 bg-clip-text text-transparent mb-2 tracking-tight">
                    {title}
                </h2>
                <p className="text-gray-400 text-sm md:text-base font-medium">{description}</p>
            </div>

            {/* Chart Area */}
            <div className="relative w-full h-[250px] md:h-[350px] select-none z-10 my-2 overflow-x-auto overflow-y-hidden">
                <div className="min-w-[600px] h-full relative">
                    {/* Axis Labels */}
                    <div className="absolute top-10 left-0 text-[10px] text-gray-500 font-bold tracking-widest uppercase -rotate-90 origin-top-left translate-y-full pl-4 opacity-50">
                        Pewność Siebie
                    </div>
                    <div className="absolute bottom-0 right-0 text-[10px] text-gray-500 font-bold tracking-widest uppercase mb-2 mr-4 opacity-50">
                        Kompetencje
                    </div>

                    {/* Chart Container */}
                    <svg
                        className="absolute inset-0 w-full h-full drop-shadow-[0_0_15px_rgba(0,0,0,0.5)]"
                        viewBox="0 0 1000 400"
                        preserveAspectRatio="xMidYMid meet"
                        style={{ overflow: 'visible' }}
                    >
                        <defs>
                            <linearGradient id="dkGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stopColor="#ef4444" /> {/* Red */}
                                <stop offset="40%" stopColor="#f59e0b" /> {/* Orange */}
                                <stop offset="70%" stopColor="#10b981" /> {/* Green */}
                                <stop offset="100%" stopColor="#3b82f6" /> {/* Blue */}
                            </linearGradient>

                            {/* Radial Gradient for Ambient Glow - Replaces CSS Blur */}
                            <radialGradient id="ambientGlow" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
                                <stop offset="0%" stopColor={activePoint.color} stopOpacity="0.4" />
                                <stop offset="70%" stopColor={activePoint.color} stopOpacity="0.1" />
                                <stop offset="100%" stopColor={activePoint.color} stopOpacity="0" />
                            </radialGradient>

                            <clipPath id="dkProgressClip">
                                <rect
                                    x="0"
                                    y="0"
                                    width={`${animPercent}%`}
                                    height="100%"
                                    className="transition-all duration-1000 ease-in-out"
                                />
                            </clipPath>

                            <filter id="dk-glow" x="-50%" y="-50%" width="200%" height="200%">
                                <feGaussianBlur stdDeviation="3" result="coloredBlur" />
                                <feMerge>
                                    <feMergeNode in="coloredBlur" />
                                    <feMergeNode in="SourceGraphic" />
                                </feMerge>
                            </filter>
                        </defs>

                        {/* Ambient Glow - SVG Circle with Radial Gradient */}
                        {/* Centered perfectly on activePos */}
                        <circle
                            cx={activePos.x}
                            cy={activePos.y}
                            r="180"
                            fill="url(#ambientGlow)"
                            className="transition-all duration-1000 ease-in-out"
                        />

                        {/* Dotted Lines */}
                        <line x1="50" y1="350" x2="950" y2="350" stroke="rgba(255,255,255,0.05)" strokeWidth="2" strokeDasharray="4 4" />
                        <line x1="50" y1="350" x2="50" y2="50" stroke="rgba(255,255,255,0.05)" strokeWidth="2" strokeDasharray="4 4" />

                        {/* Inactive Path */}
                        <path
                            d={pathDefinition}
                            fill="none"
                            stroke="rgba(255,255,255,0.1)"
                            strokeWidth="6"
                            strokeLinecap="round"
                        />

                        {/* Active Path */}
                        <path
                            d={pathDefinition}
                            fill="none"
                            stroke="url(#dkGradient)"
                            strokeWidth="6"
                            strokeLinecap="round"
                            filter="url(#dk-glow)"
                            clipPath="url(#dkProgressClip)"
                            className="transition-all duration-500"
                        />

                        {/* Nodes */}
                        {points.map((point, index) => {
                            const Icon = getIcon(point.stage);
                            const { x, y } = pointPositions[index];
                            const isActive = activeStage === point.stage;
                            const isPast = index < activeStage;

                            return (
                                <foreignObject
                                    key={point.stage}
                                    x={x - 60}
                                    y={y - 60}
                                    width="120"
                                    height="120"
                                    style={{ overflow: 'visible' }}
                                >
                                    <div
                                        className="w-full h-full flex items-center justify-center relative cursor-pointer group"
                                        onClick={() => setActiveStage(point.stage)}
                                    >
                                        {/* Ripple - Centered Absolute */}
                                        {isActive && (
                                            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none">
                                                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-20 h-20 rounded-full animate-ping opacity-20" style={{ background: point.color }} />
                                                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-28 h-28 rounded-full animate-pulse opacity-10" style={{ background: point.color }} />
                                            </div>
                                        )}

                                        {/* Node Bubble */}
                                        <div
                                            className={`relative z-20 w-12 h-12 rounded-full flex items-center justify-center border-[3px] transition-all duration-500 backdrop-blur-sm ${isActive
                                                ? 'scale-125 bg-black/40 border-white shadow-[0_0_20px_rgba(255,255,255,0.3)]'
                                                : 'scale-90 bg-black/80 border-white/10 hover:scale-105 hover:border-white/30'
                                                }`}
                                            style={{
                                                boxShadow: isActive ? `0 0 15px ${point.color}50` : '',
                                                borderColor: isActive ? '#fff' : (isPast ? point.color : 'rgba(255,255,255,0.1)'),
                                                color: isActive ? '#fff' : (isPast ? point.color : '#666')
                                            }}
                                        >
                                            <Icon size={18} />
                                        </div>

                                        {/* Label - Pushed further way */}
                                        <div
                                            className={`absolute left-1/2 -translate-x-1/2 px-3 py-1 rounded-lg text-center min-w-[140px] transition-all duration-500 z-20 pointer-events-none ${isActive
                                                ? 'opacity-100 transform translate-y-0'
                                                : 'opacity-60 group-hover:opacity-100'
                                                }`}
                                            style={{
                                                // Increased top offset to 85px to clear any rings
                                                top: index === 0 ? '-55px' : '85px',
                                                color: point.color
                                            }}
                                        >
                                            <div className="font-bold text-[10px] md:text-xs uppercase tracking-wider">{point.label}</div>
                                            <div className="text-[9px] md:text-[10px] text-gray-400 font-medium leading-tight mt-0.5">{point.title}</div>
                                        </div>
                                    </div>
                                </foreignObject>
                            );
                        })}

                    </svg>
                </div>
            </div>

            {/* Details Panel */}
            <div className="bg-gradient-to-br from-white/5 to-black/40 border-l-4 border-white/10 rounded-r-xl p-6 backdrop-blur-xl shadow-xl transition-all duration-500 min-h-[140px] relative overflow-hidden flex items-center"
                style={{ borderColor: activePoint.color }}
            >
                <div className="flex flex-col md:flex-row gap-6 items-center relative z-10 w-full">
                    <div
                        key={`icon-dk-${activeStage}`}
                        className="w-14 h-14 rounded-xl flex items-center justify-center flex-shrink-0 animate-[fadeIn_0.5s_ease-out] border border-white/10"
                        style={{ background: `${activePoint.color}20`, color: activePoint.color }}
                    >
                        {(() => {
                            const Icon = getIcon(activePoint.stage);
                            return <Icon size={28} />;
                        })()}
                    </div>

                    <div className="flex-1 animate-[slideRight_0.4s_ease-out]">
                        <h3 className="text-xl font-bold text-white mb-1">
                            {activePoint.title}
                        </h3>
                        <p className="text-gray-300 leading-relaxed text-sm md:text-base">
                            {activePoint.details}
                        </p>
                    </div>
                </div>
            </div>

            <style jsx global>{`
                @keyframes fadeIn {
                    from { opacity: 0; transform: scale(0.95); }
                    to { opacity: 1; transform: scale(1); }
                }
                @keyframes slideRight {
                    from { opacity: 0; transform: translateX(-10px); }
                    to { opacity: 1; transform: translateX(0); }
                }
            `}</style>
        </div>
    );
}
