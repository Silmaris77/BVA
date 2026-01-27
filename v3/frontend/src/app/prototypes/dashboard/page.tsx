'use client';

import { useState } from 'react';
import Link from 'next/link';
import {
    Shield, Trophy, Flame, ChevronRight, Users, TrendingUp, AlertCircle,
    CheckCircle2, Target, Calendar, ClipboardList, BookOpen, Activity, Play, Microscope,
    FileBarChart, BrainCircuit, BarChart3, ScatterChart as ScatterIcon, Grid2X2,
    Mic, MessageSquare, ArrowRight, User, Eye, LayoutGrid, Zap, Sparkles,
    Globe, Building2, PieChart as PieChartIcon, ArrowUpRight
} from 'lucide-react';
import {
    ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, ZAxis, Tooltip as RechartsTooltip, Cell, ReferenceLine, CartesianGrid,
    AreaChart, Area, BarChart, Bar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ComposedChart, Legend, PieChart, Pie
} from 'recharts';

// --- DATA TYPES & MOCKS ---

type CoachingFocus = {
    person: string;
    focus: string;
    gapType: string;
    reason: string;
    questions: string[];
};

// HEATMAP DATA (DIAGNOSTICS)
const heatmapCols = ['Sarah L.', 'Mike T.', 'Emily R.', 'John D.', 'Chris P.', 'Anna K.'];
const heatmapRows = [
    // PRZYGOTOWANIE (PLAN)
    { name: '1. Cel SMART wizyty', scores: [95, 40, 90, 85, 50, 90] },
    { name: '2. Research i CRM', scores: [90, 50, 85, 90, 60, 95] },
    { name: '3. Scenariusz wizyty', scores: [85, 30, 80, 95, 40, 90] },

    // WIZYTA (VISIT)
    { name: '4. Otwarcie (Cel-Agenda)', scores: [95, 60, 95, 80, 50, 90] },
    { name: '5. Pytania Odkrywające', scores: [90, 40, 95, 90, 55, 95] },
    { name: '6. Prezentacja Wartości', scores: [85, 50, 90, 85, 60, 90] },
    { name: '7. Reakcja na Obiekcje', scores: [90, 40, 85, 90, 50, 95] },
    { name: '8. Domykanie (Kroki)', scores: [95, 30, 90, 85, 40, 90] },

    // BHP & SAFETY
    { name: '9. Środki Ochrony (PPE)', scores: [100, 90, 100, 100, 80, 100] },
    { name: '10. Analiza Ryzyka', scores: [95, 50, 90, 95, 60, 95] },

    // TECHNICZNE / DEMO
    { name: '11. Dobór narzędzi Demo', scores: [90, 70, 85, 95, 50, 95] },
    { name: '12. Pokaz (Hands-on)', scores: [95, 80, 90, 95, 60, 100] },
    { name: '13. Dokumentacja (Foto/Pain)', scores: [85, 40, 80, 100, 50, 95] },

    // POST-WIZYTA
    { name: '14. Follow-up 24h', scores: [100, 20, 90, 100, 40, 100] },
];

// COACHING PLAN MOCK (Linked to Interaction)
const activeCoachingPlan = {
    person: 'Mike T.',
    gapType: 'Luka Egzekucji (Execution Gap)',
    focus: 'Domykanie (Kroki)', // From Standard
    reason: 'Mike świetnie buduje relacje, ale 70% wizyt kończy się "miłą rozmową" bez konkretnego ustalenia Next Steps.',
    questions: [
        'Jakie konkretne zobowiązanie klienta uzyskałeś na ostatniej wizycie?',
        'Co byś zmienił w otwarciu, żeby łatwiej było domknąć na końcu?',
        'Zróbmy symulację: Ja jestem klientem, który mówi "muszę to przemyśleć".'
    ]
};
const getCoachingPlan = (person: string, topic: string | null): CoachingFocus => {
    if (topic === 'Closing') {
        return {
            person,
            focus: "Zamykanie Sprzedaży",
            gapType: "Luka Egzekucji",
            reason: "Handlowiec robi świetne demo, ale nie prosi o zamówienie (Strach przed odmową?).",
            questions: [
                "Jak się czujesz w momencie, gdy trzeba zapytać o zamówienie?",
                "Jaki jest najgorszy scenariusz, jeśli klient powie 'nie'?"
            ]
        };
    }
    if (topic === 'Diagnoza') {
        return {
            person,
            focus: "Pogłębiona Diagnoza",
            gapType: "Luka Kompetencji",
            reason: "Zbyt powierzchowne pytania. Klient nie widzi wartości rozwiązania.",
            questions: [
                "Jakie 3 pytania zadałbyś, żeby odkryć ukryte koszty klienta?",
                "Co robisz, gdy klient mówi 'u nas wszystko działa'?"
            ]
        };
    }
    // Default / Fallback
    return {
        person,
        focus: "Standard Wizyty",
        gapType: "Ogólny Rozwój",
        reason: "Przegląd wyników z ostatniego kwartału.",
        questions: ["Z czego jesteś najbardziej dumny w tym miesiącu?", "Gdzie widzisz największą rezerwę?"]
    };
};

// ... (Other Data Mocks same as before) ...
const jssStatus = {
    header: "Twoim największym lewarem jest dziś: Diagnoza aplikacji",
    nextAction: { title: "Pogłębianie Diagnozy", desc: "Zadaj min. 3 pytania o koszty przestojów (TCO).", },
    feedback: { author: "Marta K.", text: "Świetna relacja z Budmex — pracuj nad diagnozą.", }
};
const matrixData = [
    { x: 90, y: 90, z: 120, name: 'Sarah L.', pattern: 'Model (Idealny)' },
    { x: 95, y: 30, z: 60, name: 'Mike T.', pattern: 'Luka Egzekucji' },
    { x: 30, y: 30, z: 40, name: 'Emily R.', pattern: 'Luka Kompetencji' },
    { x: 35, y: 85, z: 110, name: 'David K.', pattern: 'Talent Intuicyjny' },
    { x: 80, y: 70, z: 90, name: 'Alex M.', pattern: 'Rozwój' },
];

const gapAnalysisData = [
    { name: 'Diagnoza', theory: 90, practice: 85, gap: 5 },
    { name: 'Prezentacja', theory: 95, practice: 60, gap: 35 },
    { name: 'Demo', theory: 88, practice: 90, gap: -2 },
    { name: 'Obiekcje', theory: 92, practice: 40, gap: 52 },
    { name: 'Domknięcie', theory: 85, practice: 70, gap: 15 },
];

const jssRadarData = [
    { subject: 'Wiedza', A: 120, B: 110, fullMark: 150 },
    { subject: 'Standard', A: 98, B: 130, fullMark: 150 },
    { subject: 'App First', A: 86, B: 130, fullMark: 150 },
    { subject: 'Closing', A: 40, B: 100, fullMark: 150 },
    { subject: 'CRM', A: 85, B: 90, fullMark: 150 },
    { subject: 'Wsp.', A: 65, B: 85, fullMark: 150 },
];


// Custom Tooltip for Matrix
const MatrixTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
        const data = payload[0].payload;
        return (
            <div className="bg-neutral-900 border border-white/20 p-3 rounded-lg shadow-xl z-50">
                <p className="font-bold text-white mb-1">{data.name}</p>
                <div className="flex gap-4 text-xs text-gray-300">
                    <span>Theory: {data.x}%</span>
                    <span>Practice: {data.y}%</span>
                </div>
                <div className="mt-1 text-[10px] text-gray-400 uppercase tracking-wider">{data.pattern}</div>
            </div>
        );
    }
    return null;
};

// Helper: Competency Triangle (Scalar Radar: Theory/Practice/Result)
function CompetencyTriangle({ scores = { theory: 7, practice: 4, result: 2 } }) {
    // Canvas & Geometry
    const size = 180;
    const center = size / 2;
    const radius = 70; // Max radius for score 10

    // 3 Vertices of the Equilateral Triangle (Angles: -90, 30, 150)
    // 0 deg is right (3 o'clock). SVG coords: 0,0 is top-left.
    const angles = [-90, 30, 150].map(a => (a * Math.PI) / 180);

    // Helper: Value (0-10) -> Coordinates
    const getPoint = (value: number, angleIndex: number) => {
        const r = (value / 10) * radius;
        const x = center + r * Math.cos(angles[angleIndex]);
        const y = center + r * Math.sin(angles[angleIndex]);
        return `${x},${y}`;
    };

    // Data Points
    const maxPoints = angles.map((_, i) => getPoint(10, i)).join(" ");
    const userPoints = [
        getPoint(scores.result, 0),    // Top: Result
        getPoint(scores.practice, 1),  // Right: Practice
        getPoint(scores.theory, 2)     // Left: Theory
    ].join(" ");

    // Single coordinates for dots
    const pResult = getPoint(scores.result, 0).split(',');
    const pPractice = getPoint(scores.practice, 1).split(',');
    const pTheory = getPoint(scores.theory, 2).split(',');

    return (
        <div className="relative w-full max-w-[200px] h-[180px] mx-auto select-none flex items-center justify-center">
            <svg viewBox={`0 0 ${size} ${size}`} className="w-full h-full filter drop-shadow-xl">
                {/* Defs */}
                <defs>
                    <radialGradient id="gradScore" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
                        <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.6" />
                        <stop offset="100%" stopColor="#2563eb" stopOpacity="0.2" />
                    </radialGradient>
                    <radialGradient id="gradBg" cx="50%" cy="50%" r="50%">
                        <stop offset="80%" stopColor="#1e293b" stopOpacity="0.5" />
                        <stop offset="100%" stopColor="#0f172a" stopOpacity="0.0" />
                    </radialGradient>
                </defs>

                {/* Background Circle/Decor */}
                <circle cx={center} cy={center} r={radius} fill="url(#gradBg)" />

                {/* MAX TRIANGLE (Scale 10) */}
                <polygon points={maxPoints} fill="none" stroke="#334155" strokeWidth="1" strokeDasharray="4 4" />

                {/* AXES (Center to Max) */}
                <line x1={center} y1={center} x2={getPoint(10, 0).split(',')[0]} y2={getPoint(10, 0).split(',')[1]} stroke="#334155" strokeWidth="1" className="opacity-30" />
                <line x1={center} y1={center} x2={getPoint(10, 1).split(',')[0]} y2={getPoint(10, 1).split(',')[1]} stroke="#334155" strokeWidth="1" className="opacity-30" />
                <line x1={center} y1={center} x2={getPoint(10, 2).split(',')[0]} y2={getPoint(10, 2).split(',')[1]} stroke="#334155" strokeWidth="1" className="opacity-30" />

                {/* USER SCORE TRIANGLE */}
                <polygon points={userPoints} fill="url(#gradScore)" stroke="#60a5fa" strokeWidth="2" className="animate-in fade-in duration-1000" />

                {/* VERTEX DOTS */}
                <circle cx={pResult[0]} cy={pResult[1]} r="4" fill="#60a5fa" className="animate-pulse" />
                <circle cx={pPractice[0]} cy={pPractice[1]} r="4" fill="#60a5fa" />
                <circle cx={pTheory[0]} cy={pTheory[1]} r="4" fill="#60a5fa" />

                {/* LABELS */}
                {/* Top: WYNIK */}
                <text x={center} y={15} textAnchor="middle" fill="#94a3b8" fontSize="10" fontWeight="bold" fontFamily="sans-serif">WYNIK ({scores.result})</text>

                {/* Right: PRAKTYKA */}
                <text x={size - 20} y={130} textAnchor="middle" fill={scores.practice < 5 ? "#fbbf24" : "#94a3b8"} fontSize="10" fontWeight="bold" fontFamily="sans-serif">PRAKTYKA</text>

                {/* Left: WIEDZA */}
                <text x={20} y={130} textAnchor="middle" fill="#94a3b8" fontSize="10" fontWeight="bold" fontFamily="sans-serif">WIEDZA ({scores.theory})</text>

            </svg>
        </div>
    );
}

const kpiStats = [
    { label: "Średnia Kompetencji", value: "78%", change: "+5%", icon: Sparkles, color: "text-purple-400" },
    { label: "Aktywni Uczniowie", value: "8/10", change: "80%", icon: Users, color: "text-blue-400" },
    { label: "Pokrycie Coachingowe", value: "40%", change: "-12%", icon: MessageSquare, color: "text-orange-400" },
    { label: "Wpływ na Przychód", value: "+120k", change: "PLN", icon: TrendingUp, color: "text-green-400" },
];

const activityFeed = [
    { user: "Bartek K.", action: "Ukończył lekcję 'Closing'", time: "2 min temu", type: "success" },
    { user: "Marta W.", action: "Rozpoczęła test 'Diagnoza'", time: "15 min temu", type: "neutral" },
    { user: "Piotr N.", action: "Niski wynik w 'Obiekcje' (45%)", time: "1 godz. temu", type: "warning" },
    { user: "System", action: "Nowy moduł 'Negocjacje' dostępny", time: "3 godz. temu", type: "info" },
];

// BOARD MOCK DATA
const boardKPIs = [
    { label: "Globalny ROI", value: "3.4x", change: "+0.2x", icon: TrendingUp, color: "text-yellow-400" },
    { label: "Adopcja Systemu", value: "88%", change: "+2%", icon: Globe, color: "text-blue-400" },
    { label: "Wzrost Sprzedaży", value: "+18%", change: "YoY", icon: ArrowUpRight, color: "text-green-400" },
    { label: "Ryzyko Odejść", value: "Low", change: "-2%", icon: AlertCircle, color: "text-emerald-400" },
];

const adoptionRegionData = [
    { region: "North", adoption: 92, target: 85 },
    { region: "South", adoption: 78, target: 85 },
    { region: "East", adoption: 88, target: 85 },
    { region: "West", adoption: 95, target: 85 },
];

const roiTrendData = [
    { month: 'Sty', investment: 20, revenue: 25 },
    { month: 'Lut', investment: 22, revenue: 35 },
    { month: 'Mar', investment: 25, revenue: 48 },
    { month: 'Kwi', investment: 25, revenue: 62 },
    { month: 'Maj', investment: 28, revenue: 85 },
    { month: 'Cze', investment: 30, revenue: 110 },
];

// BOARD: ROI METRICS (Level 1, 2, 3)
const boardRoiMetrics = [
    // LEVEL 1: OPERATIONAL (Hard Money/Time)
    { label: 'Wzrost Marży (YTD)', value: '+1.2M PLN', sub: 'Dzięki lepszej argumentacji wartości (Practice)', icon: TrendingUp, color: 'text-green-400' },
    { label: 'Oszczędzony Czas', value: '120h / msc', sub: 'Mniej nietrafionych szkoleń i szybsze 1:1', icon: Calendar, color: 'text-blue-400' },

    // LEVEL 2: DECISION (Avoided Costs)
    { label: 'Uniknięte Koszty', value: '450k PLN', sub: 'Zatrzymane szkolenia "na ślepo" (3 interwencje)', icon: Shield, color: 'text-purple-400' },

    // LEVEL 3: QUALITATIVE (Risk/Stability)
    { label: 'Stability Index', value: 'High (85%)', sub: 'Spadek zmienności wyników o 30%', icon: Activity, color: 'text-yellow-400' }
];

// BOARD: DECISION EFFICIENCY (Mass vs Targeted)
const decisionEfficiencyData = [
    { name: 'Ilość Szkoleń', mass: 100, targeted: 20 }, // 80% reduction
    { name: 'Koszt (tys. PLN)', mass: 200, targeted: 40 },
    { name: 'Impact (Zmiana)', mass: 15, targeted: 85 }, // Low impact vs High impact
];

// TEAM DATA WITH SCORES (For Pattern Recognition)
// BOARD: PATTERN DISTRIBUTION MOCK
const boardPatternDistribution = [
    { name: 'Luka Egzekucji', value: 35, color: '#f59e0b' }, // 35%
    { name: 'Luka Systemowa', value: 25, color: '#ef4444' }, // 25% (Alarm!)
    { name: 'Talent Intuicyjny', value: 15, color: '#10b981' }, // 15%
    { name: 'Mistrzostwo', value: 10, color: '#8b5cf6' }, // 10%
    { name: 'Rozwój Podstaw', value: 15, color: '#3b82f6' }, // 15%
];

// BOARD: SYSTEM CORRELATION (Effort vs Result)
const systemCorrelationData = [
    { x: 80, y: 30, z: 10, name: 'Cohort A (High Effort/Low Res)' }, // System Gap
    { x: 85, y: 40, z: 10, name: 'Cohort B' },
    { x: 90, y: 80, z: 50, name: 'Cohort C (Ideal)' },
    { x: 40, y: 20, z: 20, name: 'Cohort D (Low/Low)' },
    { x: 30, y: 80, z: 30, name: 'Cohort E (Talent)' },
];

const teamMembers = [
    { name: "Sarah L.", role: "Senior JSS", scores: { theory: 9, practice: 9, result: 9 }, img: "/avatars/sarah.jpg" },
    { name: "Mike T.", role: "JSS", scores: { theory: 8, practice: 4, result: 3 }, img: "/avatars/mike.jpg" }, // Execution Gap
    { name: "Emily R.", role: "JSS", scores: { theory: 4, practice: 8, result: 8 }, img: "/avatars/emily.jpg" }, // Intuition
    { name: "John D.", role: "JSS", scores: { theory: 9, practice: 8, result: 4 }, img: "/avatars/john.jpg" }, // System Gap
    { name: "Chris P.", role: "Junior JSS", scores: { theory: 4, practice: 5, result: 6 }, img: "/avatars/chris.jpg" }, // Luck/Context
    { name: "Anna K.", role: "JSS", scores: { theory: 9, practice: 9, result: 5 }, img: "/avatars/anna.jpg" }, // System Gap
];

// Helper: Team Pattern Card
function TeamPatternCard({ member }: { member: any }) {
    const pattern = getCompetencyPattern(member.scores);
    const color = pattern.name.includes("Mistrzostwo") ? "text-purple-400 border-purple-500/30 bg-purple-500/10" :
        pattern.name.includes("Egzekucji") ? "text-orange-400 border-orange-500/30 bg-orange-500/10" :
            pattern.name.includes("Systemowa") ? "text-blue-400 border-blue-500/30 bg-blue-500/10" :
                pattern.name.includes("Intuicyjny") ? "text-green-400 border-green-500/30 bg-green-500/10" :
                    "text-gray-400 border-gray-500/30 bg-gray-500/10";

    return (
        <div className={`p-3 rounded-xl border ${color.split(' ')[1]} ${color.split(' ')[2]} flex flex-col gap-2 transition-all hover:scale-105 cursor-pointer`}>
            <div className="flex justify-between items-start">
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center font-bold text-xs">{member.name.charAt(0)}</div>
                    <div>
                        <div className="font-bold text-xs text-white">{member.name}</div>
                        <div className="text-[10px] opacity-70">{pattern.name.split('(')[0]}</div>
                    </div>
                </div>
                {pattern.name.includes("Egzekucji") && <AlertCircle size={14} className="text-orange-400 animate-pulse" />}
            </div>

            <div className="mt-1 pt-2 border-t border-white/5 border-dashed">
                <div className="flex justify-between text-[10px] text-gray-400 mb-1">
                    <span>Interwencja:</span>
                </div>
                <div className="text-[10px] font-bold truncate max-w-full leading-tight">
                    {pattern.intervention.split(',')[0]}
                </div>
            </div>
        </div>
    );
}

// 6.4. Kluczowe wzorce w Trójkącie Kompetencji
function getCompetencyPattern(scores: { theory: number, practice: number, result: number }) {
    const { theory, practice, result } = scores;

    // Wzorzec 1: Wysoka THEORY – Niska PRACTICE – Niska PERFORMANCE
    if (theory >= 7 && practice < 6 && result < 6) {
        return {
            name: "Luka Egzekucji (Execution Gap)",
            quote: "„Wiem, ale nie robię”",
            desc: "Osoba rozumie standard i deklaruje poprawne podejście, ale w praktyce skraca lub omija działania.",
            strength: "Solidne Fundamenty",
            strengthDesc: "Znakomita wiedza teoretyczna. Wiesz CO robić, masz potencjał na szybki awans po odblokowaniu bariery psychicznej/nawyksowej.",
            intervention: "OJT / Shadowing, Mikro-zadania wdrożeniowe"
        };
    }
    // Wzorzec 2: Wysoka THEORY – Wysoka PRACTICE – Niska PERFORMANCE
    if (theory >= 7 && practice >= 7 && result < 6) {
        return {
            name: "Luka Systemowa (System Gap)",
            quote: "„Robię poprawnie, ale to nie działa”",
            desc: "Standard jest rozumiany i stosowany, ale mimo to efekt jest niski. Problem może leżeć w segmencie lub ofercie.",
            strength: "Dyscyplina Procesowa",
            strengthDesc: "Perfekcyjne przygotowanie i egzekucja. Twoja postawa jest wzorowa, problem leży poza Tobą (rynek/produkt).",
            intervention: "Analiza kontekstu biznesowego, Weryfikacja Standardu"
        };
    }
    // Wzorzec 3: Niska THEORY – Wysoka PRACTICE – Wysoka PERFORMANCE
    if (theory < 6 && practice >= 7 && result >= 7) {
        return {
            name: "Talent Intuicyjny (Intuition)",
            quote: "„Działa, ale nie wiem dlaczego”",
            desc: "Dowozi wynik intuicyjnie. Ryzyko niestabilności i trudność w przekazywaniu wiedzy innym.",
            strength: "Naturalny Talent",
            strengthDesc: "Masz instynkt handlowca. Osiągasz wyniki tam, gdzie inni polegają, działając nieszablonowo.",
            intervention: "Uświadomienie mechanizmów, Kalibracja do standardu"
        };
    }
    // Wzorzec 4: Niska THEORY – Niska PRACTICE – Wysoka PERFORMANCE
    if (theory < 6 && practice < 6 && result >= 7) {
        return {
            name: "Szczęście / Relacje (Luck/Context)",
            quote: "„Dowiozłem wynik mimo standardu”",
            desc: "Efekt osiągnięty krótkoterminowo (szczęście, relacje). Wysokie ryzyko w długim okresie.",
            strength: "Spryt i Relacyjność",
            strengthDesc: "Potrafisz wykorzystać okazję i budować relacje, co ratuje wynik mimo braków procesowych.",
            intervention: "Zabezpieczenie ryzyk, Standaryzacja, Rozmowa rozwojowa"
        };
    }
    // Wzorzec 5: High High High
    if (theory >= 7 && practice >= 7 && result >= 7) {
        return {
            name: "Mistrzostwo (Mastery)",
            quote: "„Standard działa”",
            desc: "Pełna spójność trzech wymiarów. Stabilne wyniki i wysoka jakość zachowań.",
            strength: "Kompletny Ekspert",
            strengthDesc: "Łączysz wiedzę z praktyką i wynikiem. Jesteś gotowym materiałem na Mentora.",
            intervention: "Utrzymanie, Dzielenie się praktykami (Mentor)"
        };
    }

    // Default Fallback
    return {
        name: "Rozwój Podstaw (Fundamentals)",
        quote: "„Budowanie fundamentów”",
        desc: "Praca nad podstawami wiedzy i pewnością siebie w roli.",
        strength: "Otwartość na naukę",
        strengthDesc: "Jesteś na początku drogi, co oznacza brak złych nawyków i dużą chłonność wiedzy.",
        intervention: "Szkolenia podstawowe, Trening bezpieczny (Roleplay)"
    };
}

export default function DashboardPage() {
    const [role, setRole] = useState<'jss' | 'manager' | 'board'>('board');
    const [showDetails, setShowDetails] = useState(true);

    // MANAGER INTERACTION STATE
    const [activePerson, setActivePerson] = useState('Mike T.');
    const [activeTopic, setActiveTopic] = useState<string | null>('Diagnoza');

    const activeCoachingPlan = getCoachingPlan(activePerson, activeTopic);

    return (
        <div className="min-h-screen bg-neutral-950 text-white font-sans selection:bg-red-900 selection:text-white pb-20">

            {/* Top Navigation */}
            <nav className="border-b border-white/10 bg-neutral-900/50 backdrop-blur-md sticky top-0 z-50">
                <div className="max-w-md md:max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="bg-red-600 p-1.5 rounded-lg">
                            <Shield className="w-5 h-5 text-white" fill="white" />
                        </div>
                        <span className="font-bold tracking-tight text-lg hidden md:inline">MILWAUKEE <span className="text-red-500">OS</span></span>
                    </div>

                    <div className="flex bg-black/40 p-1 rounded-lg border border-white/10">
                        <button onClick={() => setRole('jss')} className={`px-4 py-1.5 rounded-md text-xs font-bold transition-all flex items-center gap-2 ${role === 'jss' ? 'bg-red-600 text-white shadow-lg shadow-red-900/20' : 'text-gray-400'}`}>
                            <User size={14} /> JSS
                        </button>
                        <button onClick={() => setRole('manager')} className={`px-4 py-1.5 rounded-md text-xs font-bold transition-all flex items-center gap-2 ${role === 'manager' ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20' : 'text-gray-400 hover:text-white'}`}>
                            <Users size={14} /> MANAGER
                        </button>
                        <button onClick={() => setRole('board')} className={`px-4 py-1.5 rounded-md text-xs font-bold transition-all flex items-center gap-2 ${role === 'board' ? 'bg-yellow-600 text-white shadow-lg shadow-yellow-900/20' : 'text-gray-400 hover:text-white'}`}>
                            <Building2 size={14} /> BOARD
                        </button>
                    </div>
                </div>
            </nav>

            <main className="max-w-md md:max-w-6xl mx-auto p-4 mt-6 animate-in fade-in slide-in-from-bottom-4 duration-500">

                {role === 'jss' && (
                    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-500">

                        {/* 1. FLOW HEADER (Simplified) */}
                        <div className="flex items-center justify-between bg-neutral-900/50 p-4 rounded-2xl border border-white/5">
                            <div>
                                <h1 className="text-xl font-bold">Dzień dobry, Bartek</h1>
                                <p className="text-sm text-gray-400">Twój dzisiejszy fokus: <span className="text-white font-bold">Budowanie Zaufania</span></p>
                            </div>
                            <div className="flex items-center gap-4">
                                <div className="text-right">
                                    <div className="text-xs text-gray-500 uppercase tracking-wider font-bold">Flow</div>
                                    <div className="flex items-center gap-1 text-green-400 font-bold">
                                        <Zap size={14} fill="currentColor" /> Stabilny
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

                            {/* LEFT COL (1/3) - FEEDBACK & WINS */}
                            <div className="space-y-6">

                                {/* FEEDBACK CARD (Simplified) */}
                                <div className="bg-neutral-900 rounded-2xl border border-white/10 p-5 relative group">
                                    <div className="flex items-center gap-3 mb-3">
                                        <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-xs font-bold">MK</div>
                                        <div>
                                            <p className="text-xs font-bold text-gray-300">Marta (Twój Manager)</p>
                                            <p className="text-[10px] text-gray-500">Notatka z wizyty (2h temu)</p>
                                        </div>
                                    </div>
                                    <div className="bg-blue-500/10 p-3 rounded-xl border border-blue-500/20">
                                        <p className="text-sm italic text-gray-200">"{jssStatus.feedback.text}"</p>
                                    </div>
                                    <button className="w-full mt-3 bg-white/5 hover:bg-white/10 py-2 rounded-lg text-[10px] font-bold transition flex items-center justify-center gap-2 text-gray-300">
                                        <Play size={10} /> Odsłuchaj (Voice Note)
                                    </button>
                                </div>

                                {/* MY WINS (Motivation) */}
                                <div className="bg-neutral-900 rounded-2xl border border-white/10 p-5">
                                    <h3 className="font-bold text-xs text-gray-400 uppercase tracking-widest mb-4 flex items-center gap-2">
                                        <Trophy size={14} className="text-yellow-500" /> Ostatnie Sukcesy
                                    </h3>
                                    <div className="space-y-4">
                                        <div className="flex gap-3 items-start opacity-50">
                                            <CheckCircle2 size={16} className="text-green-500 shrink-0 mt-0.5" />
                                            <div>
                                                <p className="text-xs line-through text-gray-500 font-medium">Badanie Potrzeb</p>
                                                <p className="text-[10px] text-gray-600">Zaliczone 2 dni temu</p>
                                            </div>
                                        </div>
                                        <div className="flex gap-3 items-start opacity-50">
                                            <CheckCircle2 size={16} className="text-green-500 shrink-0 mt-0.5" />
                                            <div>
                                                <p className="text-xs line-through text-gray-500 font-medium">Prezentacja Oferty</p>
                                                <p className="text-[10px] text-gray-600">Zaliczone tydzień temu</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* RIGHT COL (2/3) - HERO FOCUS ACTION */}
                            <div className="md:col-span-2">
                                <div className="bg-gradient-to-br from-neutral-900 to-neutral-950 rounded-2xl border border-white/10 p-8 relative overflow-hidden h-full flex flex-col">

                                    {/* STATUS INDICATOR (Simplified TPP) */}
                                    <div className="flex items-center gap-2 mb-6">
                                        <div className="bg-orange-500/20 text-orange-400 border border-orange-500/30 px-3 py-1 rounded-full text-[10px] font-bold tracking-wider uppercase flex items-center gap-2">
                                            <AlertCircle size={12} />
                                            Wzorzec: Luka Egzekucji
                                        </div>
                                    </div>

                                    <div className="flex-1">
                                        <h2 className="text-4xl font-bold mb-4 text-white tracking-tight">{jssStatus.nextAction.title}</h2>

                                        {/* WHY IT MATTERS (Context) */}
                                        <div className="mb-8 border-l-2 border-yellow-500/30 pl-4 py-1">
                                            <p className="text-xs text-yellow-500 mb-1 font-bold uppercase tracking-wider">Dlaczego to ważne?</p>
                                            <p className="text-sm text-gray-400 italic">"Bez dobrej diagnozy, klient traktuje Twoją ofertę jak zwykły cennik. Zrozumienie bólu klienta to klucz do marży."</p>
                                        </div>
                                    </div>

                                    <div className="mt-auto grid grid-cols-1 sm:grid-cols-2 gap-4">
                                        <Link href="/prototypes/theory-test" className="group relative overflow-hidden rounded-xl">
                                            <div className="absolute inset-0 bg-blue-600 group-hover:bg-blue-500 transition-colors"></div>
                                            <div className="relative p-4 flex items-center justify-between">
                                                <div className="flex items-center gap-3">
                                                    <div className="bg-white/20 p-2 rounded-lg"><Play size={20} fill="white" className="text-white" /></div>
                                                    <div>
                                                        <p className="font-bold text-sm text-white">Ćwiczenie (3 min)</p>
                                                        <p className="text-[10px] text-blue-200">Symulacja rozmowy</p>
                                                    </div>
                                                </div>
                                                <ArrowRight className="text-white/50 group-hover:translate-x-1 transition-transform" size={18} />
                                            </div>
                                        </Link>

                                        <button className="group relative overflow-hidden rounded-xl border border-white/10 hover:border-white/20 transition-colors bg-white/5 hover:bg-white/10">
                                            <div className="relative p-4 flex items-center justify-between">
                                                <div className="flex items-center gap-3">
                                                    <div className="bg-white/5 p-2 rounded-lg text-gray-400 group-hover:text-white transition-colors"><ClipboardList size={20} /></div>
                                                    <div className="text-left">
                                                        <p className="font-bold text-sm text-gray-200 group-hover:text-white">Checklista</p>
                                                        <p className="text-[10px] text-gray-500 group-hover:text-gray-400">Przed wizytą</p>
                                                    </div>
                                                </div>
                                            </div>
                                        </button>
                                    </div>

                                </div>
                            </div>
                        </div>

                        {/* 4. Deep Dive Toggle (Restored) */}
                        <button onClick={() => setShowDetails(!showDetails)} className="w-full py-4 text-xs font-bold text-gray-500 hover:text-white flex items-center justify-center gap-2 border-t border-white/5 transition-colors mt-4">
                            {showDetails ? 'Ukryj Analitykę' : 'Rozwiń Szczegóły Analityczne'} <ChevronRight size={14} className={`transition ${showDetails ? '-rotate-90' : 'rotate-90'}`} />
                        </button>

                        {/* 5. Analytical Section (Restored & Enhanced) */}
                        {showDetails && (
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-in slide-in-from-top-2">

                                {/* LEFT: COMPETENCY TRIANGLE (Radar) */}
                                <div className="bg-neutral-900/50 rounded-2xl p-6 border border-white/10 backdrop-blur-sm flex flex-col items-center justify-center relative">
                                    <div className="absolute top-4 left-4"><h2 className="font-bold text-xs flex items-center gap-2 text-gray-400"><Activity size={14} /> Model Kompetencji</h2></div>
                                    <div className="mt-8">
                                        <CompetencyTriangle scores={{ theory: 8, practice: 4, result: 3 }} />
                                    </div>
                                    <div className="mt-6 grid grid-cols-3 gap-4 text-center w-full">
                                        <div><div className="text-xl font-bold text-green-500">8/10</div><div className="text-[9px] uppercase tracking-widest text-gray-500">Wiedza</div></div>
                                        <div><div className="text-xl font-bold text-yellow-500">4/10</div><div className="text-[9px] uppercase tracking-widest text-gray-500">Praktyka</div></div>
                                        <div><div className="text-xl font-bold text-gray-500">3/10</div><div className="text-[9px] uppercase tracking-widest text-gray-500">Wynik</div></div>
                                    </div>
                                </div>

                                {/* RIGHT: GAP-TO-ACTION ENGINE (Insights) */}
                                <div className="bg-neutral-900/50 rounded-2xl p-6 border border-white/10 backdrop-blur-sm relative overflow-hidden">
                                    {/* Background Decor */}
                                    <div className="absolute -right-10 -top-10 w-40 h-40 bg-blue-500/5 rounded-full blur-3xl"></div>

                                    <div className="relative z-10">
                                        <h2 className="font-bold text-xs flex items-center gap-2 text-blue-400 mb-6 uppercase tracking-widest">
                                            <BrainCircuit size={14} /> Gap-to-Action Engine
                                        </h2>

                                        {/* Dynamic Insight based on pattern */}
                                        {(() => {
                                            const pattern = getCompetencyPattern({ theory: 8, practice: 4, result: 3 });
                                            return (
                                                <div className="space-y-6">
                                                    <div>
                                                        <h3 className="text-xl font-bold text-white mb-1">{pattern.name}</h3>
                                                        <p className="text-sm text-gray-400 italic">"{pattern.quote}"</p>
                                                    </div>

                                                    <div className="bg-white/5 p-4 rounded-xl border border-white/5">
                                                        <p className="text-xs text-gray-300 leading-relaxed mb-3"><strong className="text-white">Diagnoza:</strong> {pattern.desc}</p>

                                                        {/* NEW: STRENGTHS SECTION */}
                                                        <div className="flex items-start gap-2 pt-3 border-t border-white/5">
                                                            <Flame size={14} className="text-yellow-500 mt-0.5" />
                                                            <div>
                                                                <p className="text-xs font-bold text-yellow-500 uppercase tracking-wider mb-1">Twoja Siła:{pattern.strength}</p>
                                                                <p className="text-[11px] text-gray-400 italic">"{pattern.strengthDesc}"</p>
                                                            </div>
                                                        </div>
                                                    </div>

                                                    <div>
                                                        <p className="text-[10px] uppercase tracking-widest text-gray-500 font-bold mb-3">Rekomendowana Interwencja</p>
                                                        <div className="flex items-start gap-3">
                                                            <div className="bg-green-500/20 p-2 rounded-lg text-green-400"><Target size={18} /></div>
                                                            <div>
                                                                <p className="font-bold text-sm text-green-400">{pattern.intervention}</p>
                                                                <p className="text-xs text-gray-500 mt-1">System sugeruje działania praktyczne w terenie, zamiast kolejnych szkoleń teoretycznych.</p>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            );
                                        })()}
                                    </div>
                                </div>

                                {/* OLD CHARTS (Restored Below) */}
                            </div>
                        )}

                        {/* 6. Detailed Analytics (Previous Charts) */}
                        {showDetails && (
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-in slide-in-from-top-3">
                                <div className="bg-neutral-900/50 rounded-2xl p-4 border border-white/10 backdrop-blur-sm">
                                    <div className="mb-4 border-b border-white/5 pb-2"><h2 className="font-bold text-xs flex items-center gap-2 text-gray-400"><Activity size={14} /> Szczegółowy Radar</h2></div>
                                    <div className="h-[250px] w-full mt-2 relative">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <RadarChart cx="50%" cy="50%" outerRadius="70%" data={jssRadarData}>
                                                <PolarGrid stroke="#333" />
                                                <PolarAngleAxis dataKey="subject" tick={{ fill: '#999', fontSize: 10 }} />
                                                <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
                                                <Radar name="Wiedza" dataKey="A" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.1} />
                                                <Radar name="Praktyka" dataKey="B" stroke="#ef4444" fill="#ef4444" fillOpacity={0.3} />
                                                <Legend wrapperStyle={{ fontSize: '10px' }} />
                                            </RadarChart>
                                        </ResponsiveContainer>
                                    </div>
                                </div>
                                <div className="bg-neutral-900/50 rounded-2xl p-4 border border-white/10 backdrop-blur-sm">
                                    <div className="mb-4 border-b border-white/5 pb-2"><h2 className="font-bold text-xs flex items-center gap-2 text-gray-400"><BarChart3 size={14} /> Analiza Luk (Teoria vs Praktyka)</h2></div>
                                    <div className="h-[250px] w-full text-xs">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <ComposedChart layout="vertical" data={gapAnalysisData} margin={{ top: 0, right: 20, bottom: 0, left: 30 }}>
                                                <XAxis type="number" domain={[0, 100]} hide />
                                                <YAxis dataKey="name" type="category" width={80} stroke="#666" fontSize={10} tickLine={false} axisLine={false} />
                                                <RechartsTooltip cursor={{ fill: '#ffffff05' }} contentStyle={{ backgroundColor: '#111', borderColor: '#333' }} />
                                                <Bar dataKey="theory" fill="#3b82f6" barSize={8} radius={[0, 4, 4, 0]} name="Wiedza" />
                                                <Bar dataKey="practice" fill="#ef4444" barSize={8} radius={[0, 4, 4, 0]} name="Praktyka" />
                                            </ComposedChart>
                                        </ResponsiveContainer>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {role === 'manager' && (
                    // ==========================================
                    // MANAGER VIEW (Interactive)
                    // ==========================================
                    <div className="space-y-6">

                        {/* 1. KPI HEADERS (NEW) */}
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            {kpiStats.map((stat, i) => (
                                <div key={i} className="bg-neutral-900/80 rounded-xl border border-white/10 p-4 relative overflow-hidden group">
                                    <div className="flex justify-between items-start mb-2">
                                        <stat.icon size={18} className={`${stat.color} opacity-80`} />
                                        <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded bg-white/5 ${stat.change.startsWith('+') ? 'text-green-400' : stat.change.startsWith('-') ? 'text-red-400' : 'text-blue-400'}`}>
                                            {stat.change}
                                        </span>
                                    </div>
                                    <div className="text-2xl font-bold mb-0.5">{stat.value}</div>
                                    <div className="text-[10px] text-gray-500 uppercase tracking-wider font-bold">{stat.label}</div>
                                </div>
                            ))}
                        </div>

                        {/* 2. TEAM PATTERNS & DECISION ENGINE (NEW) */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 animate-in slide-in-from-bottom-4 duration-700">

                            {/* LEFT: TEAM MAP (Who fits which pattern?) */}
                            <div className="md:col-span-2 bg-neutral-900/50 rounded-2xl border border-white/10 p-5 backdrop-blur-sm">
                                <div className="flex justify-between items-center mb-4">
                                    <h3 className="font-bold text-sm text-white flex items-center gap-2">
                                        <LayoutGrid size={16} className="text-blue-500" /> Mapa Wzorców Zespołu
                                    </h3>
                                    <span className="text-[10px] bg-white/5 px-2 py-1 rounded text-gray-400 uppercase tracking-widest">
                                        Wykryto 3 ryzyka
                                    </span>
                                </div>
                                <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                                    {teamMembers.map((member, i) => (
                                        <div key={i} onClick={() => setActivePerson(member.name)}>
                                            <TeamPatternCard member={member} />
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* RIGHT: COACHING PRIORITIES (Actionable) */}
                            <div className="bg-gradient-to-br from-blue-950/30 to-neutral-900 rounded-2xl border border-blue-500/20 p-5 relative overflow-hidden">
                                <h3 className="font-bold text-sm text-blue-400 mb-4 flex items-center gap-2">
                                    <Zap size={16} /> Priorytet Coachingowy
                                </h3>

                                {(() => {
                                    const activeMember = teamMembers.find(m => m.name === activePerson) || teamMembers[1];
                                    const pattern = getCompetencyPattern(activeMember.scores);

                                    return (
                                        <div className="space-y-4 relative z-10">
                                            <div className="flex items-center gap-3 mb-2">
                                                <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center font-bold text-lg text-white shadow-lg shadow-blue-900/50">{activeMember.name.charAt(0)}</div>
                                                <div>
                                                    <div className="font-bold text-lg text-white">{activeMember.name}</div>
                                                    <div className="text-xs text-blue-300">{pattern.name}</div>
                                                </div>
                                            </div>

                                            <div className="bg-black/20 p-3 rounded-lg border border-white/5">
                                                <p className="text-[10px] text-gray-500 uppercase font-bold mb-1">Cel rozmowy 1:1</p>
                                                <p className="text-sm font-medium text-gray-200">"{pattern.intervention.split(',')[0]}"</p>
                                            </div>

                                            <div className="space-y-2">
                                                <p className="text-[10px] text-gray-500 uppercase font-bold">Narzędzia:</p>
                                                <button className="w-full text-left bg-white/5 hover:bg-white/10 p-2 rounded flex items-center gap-2 transition-colors border border-white/5 group">
                                                    <Mic size={14} className="text-green-400 group-hover:scale-110 transition-transform" />
                                                    <span className="text-xs text-gray-300">Nagraj Feedback (Voice)</span>
                                                </button>
                                                <button className="w-full text-left bg-white/5 hover:bg-white/10 p-2 rounded flex items-center gap-2 transition-colors border border-white/5 group">
                                                    <Eye size={14} className="text-blue-400 group-hover:scale-110 transition-transform" />
                                                    <span className="text-xs text-gray-300">Tryb Shadowing (Obserwacja)</span>
                                                </button>
                                            </div>
                                        </div>
                                    );
                                })()}

                                {/* Decor */}
                                <div className="absolute -bottom-10 -right-10 w-32 h-32 bg-blue-500/10 rounded-full blur-2xl pointer-events-none"></div>
                            </div>

                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-12 gap-6">

                            {/* MAIN COL (8/12 -> 9/12) */}
                            <div className="md:col-span-9 space-y-6">

                                {/* Matrix */}
                                <div className="bg-neutral-900 rounded-2xl border border-white/10 p-5">
                                    <div className="flex justify-between items-center mb-4">
                                        <h3 className="font-bold flex items-center gap-2 text-sm"><Grid2X2 size={16} className="text-purple-500" /> Matryca Kompetencji Zespołu</h3>
                                    </div>
                                    <div className="h-[280px] w-full text-xs relative">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <ScatterChart margin={{ top: 20, right: 30, bottom: 30, left: 10 }}>
                                                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                                                <XAxis type="number" dataKey="x" name="Theory" domain={[0, 100]} stroke="#666" label={{ value: 'Theory', position: 'bottom', offset: 0, fill: '#666' }} />
                                                <YAxis type="number" dataKey="y" name="Practice" domain={[0, 100]} stroke="#666" label={{ value: 'Practice', angle: -90, position: 'left', fill: '#666' }} />
                                                <ZAxis type="number" dataKey="z" range={[100, 1000]} name="Performance" />
                                                <RechartsTooltip content={<MatrixTooltip />} cursor={{ strokeDasharray: '3 3' }} />
                                                <ReferenceLine x={50} stroke="#444" strokeDasharray="5 5" />
                                                <ReferenceLine y={50} stroke="#444" strokeDasharray="5 5" />
                                                <ReferenceLine y={95} label={{ value: 'MODEL', position: 'insideTopRight', fill: '#666', fontSize: 10 }} stroke="none" />
                                                <Scatter name="Team" data={matrixData} fill="#8884d8">
                                                    {matrixData.map((entry, index) => (
                                                        <Cell key={`cell-${index}`} fill={
                                                            entry.x > 50 && entry.y > 50 ? '#10b981' :
                                                                entry.x > 50 && entry.y <= 50 ? '#ef4444' :
                                                                    entry.x <= 50 && entry.y <= 50 ? '#f59e0b' : '#3b82f6'
                                                        } />
                                                    ))}
                                                </Scatter>
                                            </ScatterChart>
                                        </ResponsiveContainer>
                                    </div>
                                </div>

                                {/* INTERACTIVE HEATMAP */}
                                <div className="bg-neutral-900 rounded-2xl border border-white/10 p-5 overflow-hidden">
                                    <h3 className="font-bold text-sm text-gray-300 uppercase tracking-widest mb-4 flex items-center gap-2">
                                        <LayoutGrid size={14} /> Diagnoza Problemów (Kliknij wynik)
                                    </h3>
                                    <div className="overflow-x-auto">
                                        <table className="w-full text-xs border-collapse">
                                            <thead>
                                                <tr>
                                                    <th className="p-3 text-left text-gray-500 font-normal border-b border-white/10 uppercase tracking-widest">Obszar</th>
                                                    {heatmapCols.map((col, i) => (
                                                        <th key={i} className={`p-3 text-center font-bold border-b border-white/10 min-w-[80px] cursor-pointer transition
                                                            ${activePerson === col ? 'text-blue-400 bg-white/5' : 'text-white hover:text-gray-300'}
                                                        `} onClick={() => setActivePerson(col)}>
                                                            {col}
                                                        </th>
                                                    ))}
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {heatmapRows.map((row, i) => (
                                                    <tr key={i} className="hover:bg-white/5 transition">
                                                        <td className={`p-3 font-medium border-r border-white/5 ${activeTopic === row.name ? 'text-blue-400 font-bold' : 'text-gray-300'}`}>{row.name}</td>
                                                        {row.scores.map((score, j) => (
                                                            <td key={j} className="p-1 border-r border-white/5 border-b border-white/5 relative group cursor-pointer"
                                                                onClick={() => { setActivePerson(heatmapCols[j]); setActiveTopic(row.name); }}
                                                            >
                                                                <div className={`w-full h-8 rounded flex items-center justify-center font-bold transition-all duration-300 ${activePerson === heatmapCols[j] && activeTopic === row.name
                                                                    ? 'ring-2 ring-white scale-105 z-10'
                                                                    : ''
                                                                    } ${score >= 90 ? 'bg-green-500/20 text-green-400' :
                                                                        score >= 70 ? 'bg-yellow-500/20 text-yellow-400' :
                                                                            'bg-red-500/20 text-red-400'
                                                                    }`}>
                                                                    {score}
                                                                </div>
                                                            </td>
                                                        ))}
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>

                            {/* RIGHT COL (4/12 -> 3/12) - COACHING & PULSE */}
                            <div className="md:col-span-3 space-y-6">

                                {/* DYNAMIC COACHING CARD */}
                                <div className="bg-gradient-to-b from-blue-900/10 to-neutral-900 rounded-2xl border border-blue-500/20 p-5 sticky top-24 transition-all duration-300">
                                    <div className="flex justify-between items-center mb-4">
                                        <div className="flex items-center gap-3">
                                            <div className="w-10 h-10 rounded-full bg-orange-500 flex items-center justify-center font-bold shadow-lg shadow-orange-900/50">
                                                {activeCoachingPlan.person.split(' ').map(n => n[0]).join('')}
                                            </div>
                                            <div>
                                                <h3 className="font-bold leading-none">{activeCoachingPlan.person}</h3>
                                                <p className={`text-[10px] uppercase mt-1 font-bold ${activeCoachingPlan.gapType.includes('Luka') ? 'text-red-400' : 'text-green-400'
                                                    }`}>{activeCoachingPlan.gapType}</p>
                                            </div>
                                        </div>
                                        <Link href="/prototypes/shadowing-tool">
                                            <button className="bg-white/5 hover:bg-white/10 p-2 rounded-lg border border-white/10 transition"><Microscope size={18} /></button>
                                        </Link>
                                    </div>

                                    <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-500" key={activeCoachingPlan.focus}>
                                        <div className="bg-neutral-950 p-3 rounded-xl border border-white/5">
                                            <p className="text-[10px] text-gray-500 uppercase font-bold mb-1">🎯 Fokus Spotkania</p>
                                            <p className="text-sm font-bold text-blue-400">{activeCoachingPlan.focus}</p>
                                            <p className="text-xs text-gray-400 mt-1 italic">"{activeCoachingPlan.reason}"</p>
                                        </div>
                                        <div className="bg-neutral-950 p-3 rounded-xl border border-white/5">
                                            <p className="text-[10px] text-gray-500 uppercase font-bold mb-2">❓ Pytania</p>
                                            <ul className="space-y-2">
                                                {activeCoachingPlan.questions.map((q, i) => (
                                                    <li key={i} className="text-xs text-gray-300 flex gap-2"><span className="text-blue-500 font-bold">{i + 1}.</span>{q}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    </div>

                                    <button className="w-full mt-6 bg-blue-600 hover:bg-blue-500 hover:shadow-lg hover:shadow-blue-900/40 text-white font-bold py-3 rounded-xl text-xs transition-all flex items-center justify-center gap-2">
                                        <MessageSquare size={14} />
                                        Interwencja
                                    </button>
                                </div>

                                {/* TEAM PULSE (NEW) */}
                                <div className="bg-neutral-900/50 rounded-2xl border border-white/10 p-4">
                                    <h3 className="font-bold text-xs flex items-center gap-2 mb-4 text-gray-300 tracking-widest uppercase">
                                        <Activity size={14} /> Team Pulse
                                    </h3>
                                    <div className="space-y-4">
                                        {activityFeed.map((item, i) => (
                                            <div key={i} className="relative pl-4 border-l border-white/10 pb-1 last:pb-0">
                                                <div className={`absolute -left-1 top-0 w-2 h-2 rounded-full ${item.type === 'success' ? 'bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.5)]' :
                                                    item.type === 'warning' ? 'bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.5)]' :
                                                        'bg-blue-500'
                                                    }`}></div>
                                                <div className="flex justify-between items-start">
                                                    <p className="text-xs font-bold text-gray-200">{item.user}</p>
                                                    <span className="text-[10px] text-gray-600">{item.time}</span>
                                                </div>
                                                <p className="text-[10px] text-gray-400 mt-0.5">{item.action}</p>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                            </div>

                        </div>
                    </div>
                )}

                {role === 'board' && (
                    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
                        {/* 1. STRATEGIC KPI HERO */}
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                            {boardRoiMetrics.map((stat, i) => (
                                <div key={i} className="bg-gradient-to-b from-neutral-800 to-neutral-900 rounded-xl border border-white/10 p-6 relative overflow-hidden group shadow-lg">
                                    <div className="absolute right-0 top-0 w-24 h-24 bg-white/5 rounded-bl-full pointer-events-none -mr-4 -mt-4"></div>
                                    <div className="flex justify-between items-start mb-3">
                                        <stat.icon size={24} className={`${stat.color}`} />
                                    </div>
                                    <div className="text-3xl font-bold mb-1 text-white tracking-tight">{stat.value}</div>
                                    <div className="text-xs text-gray-400 font-bold uppercase tracking-widest mb-2">{stat.label}</div>
                                    <div className="text-[10px] text-gray-500 leading-tight">{stat.sub}</div>
                                </div>
                            ))}
                        </div>

                        {/* 2. SYSTEM DIAGNOSTICS (NEW: Patterns & Correlations) */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                            {/* LEFT: PATTERN DISTRIBUTION (Pie Chart) */}
                            <div className="bg-neutral-900/50 rounded-2xl border border-white/10 p-6 backdrop-blur-sm">
                                <h3 className="font-bold text-sm text-white mb-6 flex items-center gap-2">
                                    <PieChartIcon size={16} className="text-orange-500" /> Mapa Ryzyk Systemowych (Wzorce)
                                </h3>
                                <div className="flex flex-col md:flex-row items-center gap-8">
                                    <div className="h-[200px] w-[200px] relative">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <PieChart>
                                                <Pie data={boardPatternDistribution} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                                                    {boardPatternDistribution.map((entry, index) => (
                                                        <Cell key={`cell-${index}`} fill={entry.color} stroke="none" />
                                                    ))}
                                                </Pie>
                                                <RechartsTooltip contentStyle={{ backgroundColor: '#111', borderColor: '#333', fontSize: '12px' }} />
                                            </PieChart>
                                        </ResponsiveContainer>
                                        <div className="absolute inset-0 flex items-center justify-center flex-col pointer-events-none">
                                            <span className="text-2xl font-bold text-white">35%</span>
                                            <span className="text-[9px] uppercase tracking-widest text-gray-500">Egzekucja</span>
                                        </div>
                                    </div>
                                    <div className="flex-1 space-y-3">
                                        {boardPatternDistribution.map((item, i) => (
                                            <div key={i} className="flex justify-between items-center text-xs border-b border-white/5 pb-1 last:border-0">
                                                <div className="flex items-center gap-2">
                                                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: item.color }}></div>
                                                    <span className="text-gray-300">{item.name}</span>
                                                </div>
                                                <span className="font-bold text-white">{item.value}%</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                                <div className="mt-4 bg-red-500/10 border border-red-500/20 p-3 rounded-xl">
                                    <p className="text-[10px] uppercase font-bold text-red-400 mb-1 flex items-center gap-2"><AlertCircle size={12} /> Wniosek Strategiczny</p>
                                    <p className="text-xs text-gray-300">
                                        25% organizacji wpadło w <span className="text-white font-bold">Lukę Systemową</span>. Oznacza to, że standard jest realizowany, ale nie działa. Zalecany przegląd oferty dla segmentu B.
                                    </p>
                                </div>
                            </div>

                            {/* RIGHT: SYSTEM CORRELATION (Scatter) */}
                            <div className="bg-neutral-900/50 rounded-2xl border border-white/10 p-6 backdrop-blur-sm">
                                <div className="flex justify-between items-center mb-6">
                                    <h3 className="font-bold text-sm text-white flex items-center gap-2">
                                        <Activity size={16} className="text-blue-500" /> Korelacja: Wysiłek (Oś X) vs Wynik (Oś Y)
                                    </h3>
                                </div>
                                <div className="h-[200px] w-full text-xs">
                                    <ResponsiveContainer width="100%" height="100%">
                                        <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 0 }}>
                                            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                                            <XAxis type="number" dataKey="y" name="Practice" domain={[0, 100]} stroke="#666" label={{ value: 'Praktyka (Wysiłek)', position: 'bottom', offset: 0, fill: '#666' }} />
                                            <YAxis type="number" dataKey="x" name="Result" domain={[0, 100]} stroke="#666" label={{ value: 'Wynik', angle: -90, position: 'left', fill: '#666' }} />
                                            <ZAxis type="number" dataKey="z" range={[50, 400]} />
                                            <RechartsTooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: '#111', borderColor: '#333' }} />
                                            <Scatter name="Cohorts" data={systemCorrelationData} fill="#3b82f6">
                                                {systemCorrelationData.map((entry, index) => (
                                                    <Cell key={`cell-${index}`} fill={
                                                        entry.y > 70 && entry.x < 50 ? '#ef4444' : // High Effort, Low Result (System Gap)
                                                            entry.y > 70 && entry.x > 70 ? '#10b981' : '#666'
                                                    } />
                                                ))}
                                            </Scatter>
                                        </ScatterChart>
                                    </ResponsiveContainer>
                                </div>
                                <div className="mt-4 bg-blue-500/10 border border-blue-500/20 p-3 rounded-xl">
                                    <p className="text-[10px] uppercase font-bold text-blue-400 mb-1 flex items-center gap-2"><Target size={12} /> Decyzja Inwestycyjna</p>
                                    <p className="text-xs text-gray-300">
                                        Kohorta A (Czerwona) wykazuje <span className="text-white font-bold">Wysoki Wysiłek / Niski Wynik</span>. Inwestycja w szkolenia sprzedażowe będzie nieskuteczna. Wymagana interwencja produktowa.
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* 3. ROI & FINANCIALS (Existing) */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                            {/* DECISION EFFICIENCY (Level 2 - Avoided Costs) */}
                            <div className="bg-neutral-900/50 rounded-2xl border border-white/10 p-6 backdrop-blur-sm">
                                <div className="flex justify-between items-center mb-6">
                                    <div>
                                        <h3 className="text-lg font-bold flex items-center gap-2"><ArrowUpRight className="text-purple-500" /> Efektywność Decyzyjna (L2)</h3>
                                        <p className="text-xs text-gray-400">Porównanie: Podejście Masowe (Tradycyjne) vs TPP (Celowane)</p>
                                    </div>
                                </div>
                                <div className="h-[250px] w-full text-xs">
                                    <ResponsiveContainer width="100%" height="100%">
                                        <BarChart data={decisionEfficiencyData}>
                                            <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                                            <XAxis dataKey="name" stroke="#666" fontSize={10} axisLine={false} tickLine={false} />
                                            <YAxis stroke="#666" fontSize={10} axisLine={false} tickLine={false} />
                                            <RechartsTooltip cursor={{ fill: '#ffffff05' }} contentStyle={{ backgroundColor: '#111', borderColor: '#333' }} />
                                            <Legend iconType="circle" wrapperStyle={{ fontSize: '10px' }} />
                                            <Bar name="Tradycyjne (Masowe)" dataKey="mass" fill="#4b5563" radius={[4, 4, 0, 0]} maxBarSize={40} />
                                            <Bar name="TPP (Celowane)" dataKey="targeted" fill="#a855f7" radius={[4, 4, 0, 0]} maxBarSize={40} />
                                        </BarChart>
                                    </ResponsiveContainer>
                                </div>
                                <div className="mt-4 text-[10px] text-center text-gray-500 italic">
                                    "System pozwolił uniknąć 80% zbędnych interwencji szkoleniowych, zwiększając Impact 5-krotnie."
                                </div>
                            </div>

                            {/* ROI Summary Text */}
                            <div className="bg-neutral-900/50 rounded-2xl border border-white/10 p-8 backdrop-blur-sm flex flex-col justify-center">
                                <div className="mb-6">
                                    <h3 className="text-2xl font-bold text-white mb-2">Model ROI 3-Poziomowy</h3>
                                    <p className="text-sm text-gray-400 leading-relaxed">
                                        W tym projekcie nie mierzymy efektywności samym wynikiem sprzedażowym, ale jakością podejmowanych decyzji.
                                    </p>
                                </div>
                                <div className="space-y-4">
                                    <div className="flex items-start gap-3 p-3 bg-green-500/10 rounded-lg border border-green-500/20">
                                        <div className="text-green-400 font-bold text-lg">L1</div>
                                        <div>
                                            <p className="text-xs font-bold text-green-400 uppercase">Operacyjne</p>
                                            <p className="text-xs text-gray-300">Twarda gotówka z marży i oszczędzonego czasu.</p>
                                        </div>
                                    </div>
                                    <div className="flex items-start gap-3 p-3 bg-purple-500/10 rounded-lg border border-purple-500/20">
                                        <div className="text-purple-400 font-bold text-lg">L2</div>
                                        <div>
                                            <p className="text-xs font-bold text-purple-400 uppercase">Decyzyjne (Uniknięte Koszty)</p>
                                            <p className="text-xs text-gray-300">Pieniądze, których NIE wydaliśmy na błędne szkolenia.</p>
                                        </div>
                                    </div>
                                    <div className="flex items-start gap-3 p-3 bg-yellow-500/10 rounded-lg border border-yellow-500/20">
                                        <div className="text-yellow-400 font-bold text-lg">L3</div>
                                        <div>
                                            <p className="text-xs font-bold text-yellow-400 uppercase">Jakościowe (Ryzyko)</p>
                                            <p className="text-xs text-gray-300">Stabilność procesów i przewidywalność wyników.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}
