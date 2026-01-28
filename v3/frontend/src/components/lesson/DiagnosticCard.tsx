import React, { useState } from 'react';
import { Activity, ArrowRight, RefreshCw, ClipboardList, User, Search } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface DiagnosticQuestion {
    id: string;
    text: string;
    answers: {
        text: string;
        score: string; // Maps to a result ID (e.g., 'R1', 'R2')
    }[];
}

interface DiagnosticResult {
    id: string;
    title: string;
    description: string;
    color: string;
    icon?: string;
}

interface DiagnosticCardProps {
    title: string;
    description: string;
    questions: DiagnosticQuestion[];
    results: DiagnosticResult[];
}

export default function DiagnosticCard({
    title = "Diagnostyka",
    description = "Odpowiedz na pytania, aby postawić diagnozę.",
    questions = [],
    results = []
}: DiagnosticCardProps) {
    const [currentStep, setCurrentStep] = useState(0);
    const [scores, setScores] = useState<Record<string, number>>({});
    const [finalResult, setFinalResult] = useState<DiagnosticResult | null>(null);

    const handleAnswer = (scoreKey: string) => {
        const newScores = { ...scores, [scoreKey]: (scores[scoreKey] || 0) + 1 };
        setScores(newScores);

        // Small delay for interaction feel
        setTimeout(() => {
            if (currentStep < questions.length - 1) {
                setCurrentStep(prev => prev + 1);
            } else {
                // Calculate winner
                let winner = Object.keys(newScores).reduce((a, b) => newScores[a] > newScores[b] ? a : b);
                const result = results.find(r => r.id === winner) || results[0];
                setFinalResult(result);
            }
        }, 300);
    };

    const reset = () => {
        setCurrentStep(0);
        setScores({});
        setFinalResult(null);
    };

    // --- RESULT VIEW ---
    if (finalResult) {
        return (
            <div className="flex flex-col h-full items-center justify-center p-6 text-center space-y-8 animate-fadeIn">
                <div className="relative group">
                    <div className="absolute inset-0 bg-white opacity-5 blur-2xl rounded-full group-hover:opacity-10 transition-opacity"></div>
                    <div className="relative w-32 h-32 rounded-full border-4 flex items-center justify-center shadow-2xl transition-transform transform group-hover:scale-105"
                        style={{ borderColor: finalResult.color, backgroundColor: `${finalResult.color}10` }}>
                        <Activity className="w-16 h-16" style={{ color: finalResult.color }} />
                    </div>
                </div>

                <div className="space-y-4 max-w-lg">
                    <div className="text-sm font-bold tracking-[0.2em] text-gray-400 uppercase">
                        Wynik Diagnozy
                    </div>
                    <h2 className="text-4xl font-bold text-white tracking-tight">
                        {finalResult.title}
                    </h2>
                    <div className="w-16 h-1 bg-gray-700 mx-auto rounded-full"></div>
                    <p className="text-gray-300 text-lg leading-relaxed">
                        {finalResult.description}
                    </p>
                </div>

                <button
                    onClick={reset}
                    className="flex items-center space-x-2 px-8 py-3 bg-gray-800/80 hover:bg-gray-700 rounded-full text-gray-400 hover:text-white transition-all border border-gray-700 hover:border-gray-500"
                >
                    <RefreshCw className="w-4 h-4" />
                    <span>Powtórz Analizę</span>
                </button>
            </div>
        );
    }

    const currentQ = questions[currentStep];

    // --- DIAGNOSTIC VIEW ---
    return (
        <div className="flex flex-col h-full max-w-4xl mx-auto w-full">
            {/* Header / Case File */}
            <div className="flex-none p-6 pb-2">
                <div className="bg-gray-800/40 rounded-2xl border border-gray-700/50 overflow-hidden backdrop-blur-sm">
                    {/* Badge header */}
                    <div className="bg-gray-900/50 px-6 py-3 border-b border-gray-700/50 flex justify-between items-center">
                        <div className="flex items-center space-x-2">
                            <ClipboardList className="w-5 h-5 text-emerald-400" />
                            <span className="font-bold text-emerald-400 tracking-wider text-xs uppercase">
                                Karta Pacjenta (Case Study)
                            </span>
                        </div>
                        <span className="text-xs font-mono text-gray-500">
                            ANALIZA 00{currentStep + 1}
                        </span>
                    </div>

                    {/* Case Description */}
                    <div className="p-6 md:p-8 flex flex-col md:flex-row gap-6 items-start">
                        <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gray-700 flex items-center justify-center">
                            <User className="w-6 h-6 text-gray-400" />
                        </div>
                        <div className="space-y-1">
                            <h3 className="text-xl font-bold text-white">{title}</h3>
                            <p className="text-gray-300 leading-relaxed text-sm md:text-base">
                                {description}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Interaction Area */}
            <div className="flex-1 flex flex-col px-6 pb-6 pt-4 space-y-4 overflow-y-auto">
                <div className="flex items-center space-x-3 mb-2 px-1">
                    <Search className="w-5 h-5 text-emerald-500 animate-pulse" />
                    <span className="text-sm font-semibold text-emerald-400 uppercase tracking-widest">
                        Kryterium Diagnostyczne {currentStep + 1}/{questions.length}
                    </span>
                </div>

                <h4 className="text-2xl font-bold text-white px-1 leading-snug">
                    {currentQ.text}
                </h4>

                <div className="grid grid-cols-1 gap-3 mt-4">
                    {currentQ.answers.map((ans, idx) => (
                        <button
                            key={idx}
                            onClick={() => handleAnswer(ans.score)}
                            className="group relative w-full text-left p-6 rounded-2xl bg-gradient-to-br from-gray-800 to-gray-800/50 hover:from-gray-700 hover:to-gray-700/80 border border-gray-700 hover:border-emerald-500/50 transition-all duration-300 shadow-lg hover:shadow-xl hover:-translate-y-0.5"
                        >
                            <div className="flex items-start justify-between">
                                <span className="text-lg text-gray-200 font-medium pr-8 group-hover:text-white transition-colors">
                                    {ans.text}
                                </span>
                                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-900 border border-gray-600 group-hover:border-emerald-500 flex items-center justify-center transition-all">
                                    <ArrowRight className="w-4 h-4 text-gray-500 group-hover:text-emerald-400 transform group-hover:translate-x-0.5 transition-all" />
                                </div>
                            </div>
                        </button>
                    ))}
                </div>
            </div>

            {/* Progress Bar */}
            <div className="px-8 pb-8 pt-0">
                <div className="h-1 w-full bg-gray-800 rounded-full overflow-hidden">
                    <div
                        className="h-full bg-emerald-500 transition-all duration-500 ease-out"
                        style={{ width: `${((currentStep) / questions.length) * 100}%` }}
                    ></div>
                </div>
            </div>
        </div>
    );
}
