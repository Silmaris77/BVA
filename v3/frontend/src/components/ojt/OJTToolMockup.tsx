'use client'

import React, { useState, useEffect } from 'react';
import {
    Smartphone, CheckCircle2, AlertTriangle, Mic, Play,
    MessageSquare, Battery, Signal, Wifi, ChevronLeft,
    MoreVertical, User, Target, BarChart3, Send, ThumbsUp,
    ThumbsDown, Search, ArrowRight, Zap, Calculator, X
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// --- MOCK DATA & TYPES ---
type Phase = 'home' | 'profile' | 'contract' | 'mirror' | 'goal' | 'action' | 'debrief' | 'feedback' | 'commitment';

export default function OJTToolMockup() {
    const [phase, setPhase] = useState<Phase>('home');
    const [batteryLevel, setBatteryLevel] = useState(85);
    const [debriefStep, setDebriefStep] = useState(0);
    const [isRecording, setIsRecording] = useState(false);
    const [recordingTime, setRecordingTime] = useState(0);

    const DEBRIEF_QUESTIONS = [
        "Jaki był JEDEN kluczowy fakt, który wpłynął na wynik wizyty?",
        "Co klient DOKŁADNIE powiedział lub zrobił w reakcji na handlowca?",
        "Jaką jedną rzecz zmienilibyśmy w następnym podejściu?"
    ];

    // Simulate timer
    useEffect(() => {
        let interval: any;
        if (isRecording) {
            interval = setInterval(() => {
                setRecordingTime(prev => prev + 1);
            }, 1000);
        } else {
            setRecordingTime(0);
        }
        return () => clearInterval(interval);
    }, [isRecording]);

    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    };

    // --- RENDERERS ---

    const renderStatusBar = () => (
        <div className="flex justify-between items-center px-6 py-3 text-xs font-medium text-gray-400 border-b border-gray-800 bg-gray-950">
            <div className="flex items-center space-x-2">
                <span>09:41</span>
            </div>
            <div className="flex items-center space-x-2">
                <Signal className="w-3 h-3" />
                <Wifi className="w-3 h-3" />
                <div className="flex items-center space-x-1">
                    <span>{batteryLevel}%</span>
                    <Battery className="w-3 h-3" />
                </div>
            </div>
        </div>
    );

    const renderHome = () => (
        <div className="p-6 space-y-8 h-full flex flex-col">
            <div className="space-y-2 mt-8">
                <h2 className="text-3xl font-bold text-white tracking-tight">Dzień dobry, Marek</h2>
                <p className="text-gray-400">Masz dziś 1 aktywny trening.</p>
            </div>

            <div
                onClick={() => setPhase('profile')}
                className="bg-gradient-to-br from-indigo-900 to-gray-900 p-6 rounded-2xl border border-indigo-500/30 relative overflow-hidden group cursor-pointer hover:scale-[1.02] transition-transform"
            >
                <div className="absolute top-0 right-0 p-4 opacity-10">
                    <Target className="w-24 h-24 text-white" />
                </div>
                <div className="flex justify-between items-start mb-4">
                    <div className="w-12 h-12 rounded-full bg-indigo-500/20 flex items-center justify-center text-indigo-400 font-bold text-lg border border-indigo-500/50 relative z-10">
                        T
                    </div>
                    <span className="bg-green-500/20 text-green-400 text-xs font-bold px-2 py-1 rounded-full z-10">
                        08:30
                    </span>
                </div>
                <h3 className="text-xl font-bold text-white mb-1">Wizyta z Tomkiem</h3>
                <p className="text-sm text-gray-400 mb-4">Klient: Budex Sp. z o.o.</p>
                <div className="flex items-center space-x-2 text-xs text-indigo-300 font-medium">
                    <User className="w-4 h-4" />
                    <span>Zobacz Profil i Przygotuj się</span>
                    <ArrowRight className="w-4 h-4" />
                </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-900 p-4 rounded-xl border border-gray-800 text-center">
                    <div className="text-2xl font-bold text-white mb-1">4/5</div>
                    <div className="text-xs text-gray-500">Treningi w tym miesiącu</div>
                </div>
                <div className="bg-gray-900 p-4 rounded-xl border border-gray-800 text-center">
                    <div className="text-2xl font-bold text-emerald-400 mb-1">+12%</div>
                    <div className="text-xs text-gray-500">Skuteczność Zespołu</div>
                </div>
            </div>
        </div>
    );

    const renderProfile = () => (
        <div className="p-6 h-full flex flex-col bg-gray-950">
            <div className="flex items-center space-x-4 mb-6">
                <button onClick={() => setPhase('home')}><ChevronLeft className="text-gray-400" /></button>
                <h3 className="text-lg font-bold text-white">Profil Pracownika</h3>
            </div>

            <div className="flex-1 overflow-y-auto space-y-6">
                {/* Header Profile */}
                <div className="flex items-center space-x-4">
                    <div className="w-20 h-20 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-3xl font-bold text-white shadow-xl">
                        T
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-white">Tomek</h2>
                        <span className="text-sm text-gray-400">Junior Sales Rep</span>
                    </div>
                </div>

                {/* Insight Card: Learning Style */}
                <div className="bg-gray-900 p-5 rounded-2xl border border-gray-800 space-y-3">
                    <div className="flex items-center justify-between">
                        <h4 className="text-sm font-bold text-gray-400 uppercase tracking-widest">Styl Uczenia (Kolb)</h4>
                        <span className="px-2 py-1 bg-orange-500/20 text-orange-400 text-xs font-bold rounded">AKTYWISTA</span>
                    </div>
                    <p className="text-gray-300 text-sm leading-relaxed">
                        Tomek uczy się przez <strong>działanie</strong>. Nudzą go długie instrukcje.
                    </p>
                    <div className="bg-blue-500/10 p-3 rounded-lg border-l-2 border-blue-500 flex items-start space-x-2">
                        <Zap className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" />
                        <p className="text-xs text-blue-200">
                            <strong>Tip:</strong> Nie tłumacz teorii w samochodzie. Rzuć mu szybkie wyzwanie ("Spróbuj zrobić to po swojemu") i omów wyniki.
                        </p>
                    </div>
                </div>

                {/* Competence Matrix */}
                <div className="space-y-3">
                    <h4 className="text-sm font-bold text-gray-400 px-1">Poziom Kompetencji</h4>

                    <div className="bg-gray-900 p-4 rounded-xl border border-gray-800 flex justify-between items-center">
                        <span className="text-gray-300 text-sm">Badanie Potrzeb</span>
                        <div className="flex items-center space-x-2">
                            <div className="flex space-x-0.5">
                                <div className="w-2 h-4 bg-green-500 rounded-sm"></div>
                                <div className="w-2 h-4 bg-green-500 rounded-sm"></div>
                                <div className="w-2 h-4 bg-green-500 rounded-sm"></div>
                                <div className="w-2 h-4 bg-gray-700 rounded-sm"></div>
                            </div>
                            <span className="text-xs font-bold text-green-400">R3</span>
                        </div>
                    </div>

                    <div className="bg-gray-900 p-4 rounded-xl border border-gray-800 flex justify-between items-center ring-1 ring-indigo-500/50">
                        <span className="text-white font-medium text-sm">Zamykanie Sprzedaży</span>
                        <div className="flex items-center space-x-2">
                            <div className="flex space-x-0.5">
                                <div className="w-2 h-4 bg-red-500 rounded-sm"></div>
                                <div className="w-2 h-4 bg-gray-700 rounded-sm"></div>
                                <div className="w-2 h-4 bg-gray-700 rounded-sm"></div>
                                <div className="w-2 h-4 bg-gray-700 rounded-sm"></div>
                            </div>
                            <span className="text-xs font-bold text-red-400">R1</span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-800">
                <button
                    onClick={() => setPhase('mirror')}
                    className="w-full py-4 bg-indigo-600 rounded-xl text-sm font-bold text-white hover:bg-indigo-500 flex items-center justify-center space-x-2 transition-all"
                >
                    <span>Rozpocznij Kalibrację (Mirror)</span>
                    <ArrowRight className="w-4 h-4" />
                </button>
            </div>
        </div>
    );

    const renderMirror = () => (
        <div className="p-6 h-full flex flex-col">
            <div className="flex items-center space-x-4 mb-8">
                <button onClick={() => setPhase('home')}><ChevronLeft className="text-gray-400" /></button>
                <h3 className="text-lg font-bold text-white">Kalibracja (Mirror)</h3>
            </div>

            <div className="space-y-8 flex-1">
                <div className="bg-gray-900/50 p-6 rounded-2xl border border-gray-800 text-center space-y-4">
                    <User className="w-12 h-12 text-blue-400 mx-auto" />
                    <h4 className="text-white font-medium">Tomek ocenił siebie:</h4>
                    <div className="text-5xl font-bold text-blue-400">8<span className="text-xl text-gray-600">/10</span></div>
                    <p className="text-xs text-gray-500 uppercase tracking-widest">Kompetencja: Zamykanie Sprzedaży</p>
                </div>

                <div className="space-y-4">
                    <label className="text-sm text-gray-400">Twoja ocena Tomka:</label>
                    <input type="range" className="w-full accent-indigo-500 h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer" />
                    <div className="flex justify-between text-xs text-gray-600 font-mono">
                        <span>1 (R1)</span>
                        <span>5 (R3)</span>
                        <span>10 (R4)</span>
                    </div>
                </div>

                <div className="bg-red-500/10 border border-red-500/20 p-4 rounded-xl flex items-start space-x-3">
                    <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0" />
                    <p className="text-sm text-red-200">
                        <span className="font-bold">Uwaga: Dunning-Kruger.</span> Tomek nie widzi swoich braków (Gap = 5 pkt). Spodziewaj się oporu.
                    </p>
                </div>
            </div>

            <button
                onClick={() => setPhase('goal')}
                className="w-full py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold transition-all"
            >
                Dalej: Wybierz Cel
            </button>
        </div>
    );

    const renderDebrief = () => (
        <div className="h-full flex flex-col p-6 bg-gray-950">
            <div className="flex items-center space-x-4 mb-8">
                <button onClick={() => setPhase('action')}><ChevronLeft className="text-gray-400" /></button>
                <div className="flex flex-col">
                    <h3 className="text-lg font-bold text-white">Asystent Notatki</h3>
                    <span className="text-xs text-indigo-400 font-medium">AI Coach Mode</span>
                </div>
            </div>

            <div className="flex-1 flex flex-col items-center justify-center space-y-8 text-center relative">

                {/* Progress Indicators */}
                <div className="flex space-x-2 absolute top-0">
                    {DEBRIEF_QUESTIONS.map((_, i) => (
                        <div key={i} className={`h-1 w-8 rounded-full transition-all ${i === debriefStep ? 'bg-indigo-500 w-12' : 'bg-gray-800'}`}></div>
                    ))}
                </div>

                <AnimatePresence mode="wait">
                    <motion.div
                        key={debriefStep}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        className="space-y-6 max-w-xs"
                    >
                        <h2 className="text-2xl font-bold text-white leading-tight">
                            {DEBRIEF_QUESTIONS[debriefStep]}
                        </h2>
                    </motion.div>
                </AnimatePresence>

                <div
                    onClick={() => {
                        // Simulate recording interaction
                        if (debriefStep < DEBRIEF_QUESTIONS.length - 1) {
                            setDebriefStep(prev => prev + 1);
                        } else {
                            setPhase('feedback');
                        }
                    }}
                    className="w-32 h-32 rounded-full border-4 border-indigo-500/30 flex items-center justify-center cursor-pointer relative group"
                >
                    <div className="absolute inset-0 bg-indigo-500/10 rounded-full animate-ping group-hover:bg-indigo-500/20"></div>
                    <div className="w-24 h-24 bg-indigo-600 rounded-full flex items-center justify-center shadow-[0_0_40px_rgba(79,70,229,0.5)] transition-transform group-hover:scale-95">
                        <Mic className="w-8 h-8 text-white" />
                    </div>
                </div>

                <p className="text-gray-500 text-sm">
                    {debriefStep < DEBRIEF_QUESTIONS.length - 1 ? "Dotknij by odpowiedzieć i przejść dalej" : "Dotknij by zakończyć wywiad"}
                </p>
            </div>
        </div>
    );

    const renderRecordingOverlay = () => (
        <div className="absolute inset-0 bg-black/95 z-50 flex flex-col items-center justify-center p-8 space-y-12 animate-in fade-in zoom-in duration-300">
            <div className="text-center space-y-2">
                <div className="inline-flex items-center space-x-2 bg-red-500/10 text-red-500 px-4 py-1.5 rounded-full animate-pulse">
                    <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                    <span className="text-xs font-bold tracking-widest uppercase">Recording</span>
                </div>
                <h3 className="text-gray-400 font-medium">Notatka Głosowa</h3>
            </div>

            <div className="text-7xl font-mono font-bold text-white tracking-widest tabular-nums">
                {formatTime(recordingTime)}
            </div>

            {/* Simulated Waveform */}
            <div className="flex items-center justify-center gap-1 h-16 w-full">
                {[...Array(20)].map((_, i) => (
                    <div
                        key={i}
                        className="w-2 bg-indigo-500 rounded-full animate-bounce"
                        style={{
                            height: `${Math.random() * 100}%`,
                            animationDuration: `${0.5 + Math.random() * 0.5}s`,
                            animationDelay: `${i * 0.05}s`
                        }}
                    ></div>
                ))}
            </div>

            <div className="flex items-center gap-6">
                <button
                    onClick={() => setIsRecording(false)}
                    className="w-16 h-16 rounded-full bg-gray-800 flex items-center justify-center hover:bg-gray-700 transition-colors"
                >
                    <X className="w-6 h-6 text-white" />
                </button>
                <button
                    onClick={() => {
                        setIsRecording(false);
                        // Simulate saving
                        setTimeout(() => alert("Notatka zapisana! (Symulacja)"), 200);
                    }}
                    className="w-24 h-24 rounded-full bg-red-600 flex items-center justify-center hover:bg-red-500 shadow-lg shadow-red-900/50 transition-all transform hover:scale-105"
                >
                    <div className="w-8 h-8 bg-white rounded-lg"></div>
                </button>
            </div>

            <p className="text-gray-500 text-sm max-w-xs text-center">
                Możesz nagrywać tak długo jak chcesz. Transkrypcja AI wyciągnie kluczowe wnioski automatycznie.
            </p>
        </div>
    );

    const renderAction = () => (
        <div className="h-full flex flex-col bg-black relative">
            {/* Stealth Mode Header */}
            <div className="absolute top-4 left-0 right-0 flex justify-center opacity-30">
                <div className="bg-red-500 w-2 h-2 rounded-full animate-pulse mr-2"></div>
                <span className="text-red-500 text-xs font-mono">OBSERVATION MODE</span>
            </div>

            <div className="flex-1 flex flex-col justify-center gap-6 p-6">

                <button className="flex-1 bg-green-900/20 border border-green-500/30 rounded-3xl flex flex-col items-center justify-center space-y-2 active:bg-green-500/20 transition-all group">
                    <div className="w-16 h-16 rounded-full bg-green-500/20 flex items-center justify-center group-hover:scale-110 transition-transform">
                        <ThumbsUp className="w-8 h-8 text-green-400" />
                    </div>
                    <span className="text-green-400 font-bold tracking-widest uppercase">Super</span>
                </button>

                <div className="h-24 flex gap-4">
                    <button className="flex-1 bg-yellow-900/20 border border-yellow-500/30 rounded-3xl flex flex-col items-center justify-center active:bg-yellow-500/20 transition-all">
                        <Zap className="w-6 h-6 text-yellow-400 mb-1" />
                        <span className="text-yellow-400 text-xs font-bold uppercase">Szansa</span>
                    </button>
                    <button className="flex-1 bg-red-900/20 border border-red-500/30 rounded-3xl flex flex-col items-center justify-center active:bg-red-500/20 transition-all">
                        <AlertTriangle className="w-6 h-6 text-red-400 mb-1" />
                        <span className="text-red-400 text-xs font-bold uppercase">Błąd</span>
                    </button>
                </div>

                <button
                    onClick={() => setIsRecording(true)}
                    className="h-24 bg-gray-800 rounded-3xl flex items-center justify-center space-x-3 active:bg-gray-700 transition-all hover:bg-gray-750 border border-gray-700 hover:border-indigo-500 group"
                >
                    <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center group-hover:bg-indigo-600 transition-colors">
                        <Mic className="w-5 h-5 text-white" />
                    </div>
                    <div className="flex flex-col items-start">
                        <span className="text-white font-bold">Notatka Głosowa</span>
                        <span className="text-xs text-gray-500">Kliknij by nagrać podsumowanie</span>
                    </div>
                </button>

            </div>

            <div className="p-6 pb-8">
                <button
                    onClick={() => setPhase('debrief')}
                    className="w-full py-4 bg-gray-900 border border-gray-700 text-gray-400 rounded-xl font-bold hover:text-white transition-all text-sm"
                >
                    Zakończ Wizytę i Generuj Feedback
                </button>
            </div>

            {isRecording && renderRecordingOverlay()}
        </div>
    );

    const renderFeedback = () => (
        <div className="p-6 h-full flex flex-col">
            <div className="flex items-center space-x-4 mb-4">
                <button onClick={() => setPhase('debrief')}><ChevronLeft className="text-gray-400" /></button>
                <h3 className="text-lg font-bold text-white">Generator Feedbacku</h3>
            </div>

            <div className="flex-1 space-y-4 overflow-y-auto">
                <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center flex-shrink-0">
                        <Zap className="w-4 h-4 text-white" />
                    </div>
                    <div className="bg-gray-800 p-4 rounded-2xl rounded-tl-none max-w-[90%] space-y-2">
                        <p className="text-gray-400 text-xs font-bold uppercase tracking-widest mb-1">
                            MODEL: FUKO (Fakty - Uczucia - Konsekwencje - Oczekiwania)
                        </p>
                        <div className="text-gray-200 text-sm leading-relaxed">
                            "Tomek, rozmowa z klientem była wyzwaniem. Doceniam Twoją energię."
                            <br /><br />
                            "Jednak <span className="text-green-400 font-bold bg-green-400/10 px-1 rounded">w 15. minucie przerwałeś klientowi</span>, gdy mówił o budżecie.
                            <span className="text-green-400 font-bold bg-green-400/10 px-1 rounded ml-1">Klient wycofał się i skrzyżował ręce</span>."
                            <br /><br />
                            "Spowodowało to utratę inicjatywy. Czego potrzebujesz, żeby w przyszłości wysłuchać do końca?"
                        </div>
                    </div>
                </div>

                <div className="flex items-center space-x-2 text-xs text-gray-500 px-2">
                    <CheckCircle2 className="w-3 h-3 text-green-500" />
                    <span>Filtr Obiektywizmu aktywny (Fakty podświetlone)</span>
                </div>
            </div>

            <div className="pt-4 space-y-3">
                <button
                    onClick={() => setPhase('commitment')}
                    className="w-full py-4 bg-indigo-600 rounded-xl text-sm font-bold text-white hover:bg-indigo-500 flex items-center justify-center space-x-2 transition-all shadow-lg shadow-indigo-900/50"
                >
                    <Send className="w-4 h-4" />
                    <span>Zatwierdź i Wyślij Plan</span>
                </button>
            </div>
        </div>
    );

    const renderCommitment = () => (
        <div className="p-6 h-full flex flex-col items-center justify-center text-center space-y-8 bg-gradient-to-br from-indigo-900/50 to-gray-950">
            <div className="w-24 h-24 bg-green-500/20 rounded-full flex items-center justify-center border-2 border-green-500/50">
                <CheckCircle2 className="w-12 h-12 text-green-400" />
            </div>

            <div className="space-y-4">
                <h2 className="text-3xl font-bold text-white">Cykl Zamknięty!</h2>
                <div className="bg-gray-800/50 p-6 rounded-2xl border border-gray-700/50 text-left space-y-2 max-w-xs mx-auto">
                    <div className="text-xs text-gray-400 uppercase tracking-widest">Ustalony Plan (Next Step)</div>
                    <p className="text-white font-medium text-lg">
                        "W kolejnych 3 wizytach stosuję zasadę 3 sekund ciszy przed odpowiedzią na obiekcję."
                    </p>
                </div>
            </div>

            <button
                onClick={() => setPhase('home')}
                className="px-8 py-3 bg-white text-gray-900 rounded-full font-bold hover:bg-gray-100 transition-colors flex items-center space-x-2"
            >
                <span>Wróć do Dashboardu</span>
            </button>

            <p className="text-xs text-gray-500 px-8">
                Tomek otrzymał powiadomienie i musi zaakceptować plan w swojej aplikacji.
            </p>
        </div>
    );

    // --- MAIN RENDER ---
    return (
        <div className="min-h-screen bg-black flex items-center justify-center p-4 md:p-8 font-sans">

            {/* Phone Mockup Container */}
            <div className="w-full max-w-[375px] h-[812px] bg-gray-950 rounded-[40px] border-[12px] border-gray-900 shadow-2xl relative overflow-hidden flex flex-col">

                {/* Dynamic Island / Notch */}
                <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-[120px] h-[30px] bg-black rounded-b-2xl z-50 flex items-center justify-center">
                    <div className="w-16 h-16 rounded-full bg-black/50 blur-xl absolute -top-8"></div>
                </div>

                {renderStatusBar()}

                {/* Screen Content */}
                <div className="flex-1 overflow-hidden relative bg-gray-950">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={phase}
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="h-full"
                        >
                            {phase === 'home' && renderHome()}
                            {phase === 'profile' && renderProfile()}
                            {phase === 'contract' && renderMirror()} {/* Skipping straight to mirror for demo */}
                            {phase === 'mirror' && renderMirror()}
                            {phase === 'goal' && (
                                <div className="p-6 h-full flex flex-col items-center justify-center text-center space-y-6">
                                    <Target className="w-16 h-16 text-indigo-500 animate-bounce" />
                                    <h3 className="text-xl font-bold text-white">Goal Picker</h3>
                                    <p className="text-gray-400">Tutaj będzie karuzela celów.</p>
                                    <button onClick={() => setPhase('action')} className="px-6 py-2 bg-indigo-600 rounded-full text-white">Rozpocznij Wizytę</button>
                                </div>
                            )}
                            {phase === 'action' && renderAction()}
                            {phase === 'debrief' && renderDebrief()}
                            {phase === 'feedback' && renderFeedback()}
                            {phase === 'commitment' && renderCommitment()}
                        </motion.div>
                    </AnimatePresence>
                </div>
                {/* ... (Home Indicator) */}
                <div className="h-1 w-32 bg-gray-800 rounded-full mx-auto mb-2 mt-4"></div>
            </div>
            {/* ... (Desktop Info) */}
            <div className="hidden md:block ml-12 max-w-sm">
                <div className="flex items-center space-x-3 mb-6">
                    <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center">
                        <Zap className="text-white" />
                    </div>
                    <h1 className="text-3xl font-bold text-white">OJT Companion</h1>
                </div>
                <p className="text-gray-400 mb-8 leading-relaxed">
                    To jest interaktywny prototyp narzędzia "Live Coaching Tool" (Enterprise v1.0).
                </p>
                <div className="space-y-4 text-sm text-gray-300">
                    <p>👉 Kliknij w kartę "Wizyta z Tomkiem", aby zobaczyć jego profil.</p>
                    <p>Dowiesz się, że jest "Aktywistą" (Kolb), co zmienia strategię OJT.</p>
                </div>
            </div>
        </div>
    );
}
