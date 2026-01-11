"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
    ChevronRight,
    ChevronLeft,
    CheckCircle,
    Briefcase,
    Users,
    Layers,
    Scale,
    Wrench,
    MessageSquare,
    Calculator,
    Trophy
} from "lucide-react";
import { GlassCard } from "@/components/ui/GlassCard";
import { api, MilwaukeeContext, MilwaukeeAppMatch, DiscoveryQuestion, RecommendationPackage } from "@/services/api";
import { cn } from "@/app/utils/cn";

// --- STEPS ---
type Step = "CONTEXT" | "APP_SELECTION" | "DISCOVERY" | "RECOMMENDATION";

export function MilwaukeeApplicationEngine() {
    const [step, setStep] = useState<Step>("CONTEXT");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Data State
    const [contextQuestions, setContextQuestions] = useState<any>(null);
    const [context, setContext] = useState<MilwaukeeContext>({
        typ_klienta: "",
        typ_pracy: "",
        materialy_srodowisko: [],
        skala: ""
    });

    const [appMatches, setAppMatches] = useState<MilwaukeeAppMatch[]>([]);
    const [selectedAppId, setSelectedAppId] = useState<string | null>(null);

    const [discoveryQuestions, setDiscoveryQuestions] = useState<DiscoveryQuestion[]>([]);
    const [answers, setAnswers] = useState<any>({});

    const [recommendation, setRecommendation] = useState<RecommendationPackage | null>(null);

    // Initial Load
    useEffect(() => {
        const loadQuestions = async () => {
            try {
                setError(null);
                const data = await api.getContextQuestions();
                setContextQuestions(data);
            } catch (e: any) {
                console.error("Failed to load context questions", e);
                setError("Nie udało się pobrać danych z serwera. Sprawdź połączenie.");
            }
        };
        loadQuestions();
    }, []);

    // --- HANDLERS ---
    const handleRetry = () => {
        setError(null);
        window.location.reload();
    };

    const handleContextSubmit = async () => {
        setLoading(true);
        setError(null);
        try {
            const matches = await api.matchApplication(context);
            setAppMatches(matches);
            setStep("APP_SELECTION");
        } catch (e: any) {
            console.error(e);
            setError("Wystąpił błąd podczas dopasowywania aplikacji.");
        } finally {
            setLoading(false);
        }
    };

    const handleAppSelect = async (appId: string) => {
        setSelectedAppId(appId);
        setLoading(true);
        setError(null);
        try {
            // Pobierz pytania dla typu klienta
            const questions = await api.getDiscoveryQuestions(context.typ_klienta);
            setDiscoveryQuestions(questions);
            setStep("DISCOVERY");
        } catch (e: any) {
            console.error(e);
            setError("Wystąpił błąd podczas pobierania pytań.");
        } finally {
            setLoading(false);
        }
    };

    const handleDiscoverySubmit = async () => {
        if (!selectedAppId) return;
        setLoading(true);
        setError(null);
        try {
            const result = await api.getRecommendation(selectedAppId, answers);
            setRecommendation(result);
            setStep("RECOMMENDATION");
        } catch (e: any) {
            console.error(e);
            setError("Wystąpił błąd podczas generowania rekomendacji.");
        } finally {
            setLoading(false);
        }
    };

    const renderProgressBar = () => {
        const steps: Step[] = ["CONTEXT", "APP_SELECTION", "DISCOVERY", "RECOMMENDATION"];
        const labels = ["Kontekst", "Wybór Aplikacji", "Pytania", "Rekomendacja"];
        const currentIndex = steps.indexOf(step);

        return (
            <div className="flex justify-between mb-8 relative">
                <div className="absolute top-1/2 left-0 w-full h-1 bg-white/10 -z-10 -translate-y-1/2 rounded-full" />
                <div
                    className="absolute top-1/2 left-0 h-1 bg-neon-red -z-10 -translate-y-1/2 rounded-full transition-all duration-500"
                    style={{ width: `${(currentIndex / 3) * 100}%` }}
                />

                {steps.map((s, idx) => {
                    const isCompleted = idx <= currentIndex;
                    const isCurrent = idx === currentIndex;

                    return (
                        <div key={s} className="flex flex-col items-center">
                            <div className={cn(
                                "w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-300 border-2",
                                isCompleted
                                    ? "bg-neon-red border-neon-red text-white"
                                    : "bg-[#0f1016] border-gray-600 text-gray-500"
                            )}>
                                {idx + 1}
                            </div>
                            <div className={cn(
                                "mt-2 text-xs font-medium",
                                isCurrent ? "text-white" : "text-gray-500"
                            )}>
                                {labels[idx]}
                            </div>
                        </div>
                    );
                })}
            </div>
        );
    };

    if (error) {
        return (
            <div className="p-10 text-center">
                <div className="text-red-500 mb-4 text-xl">⚠️ {error}</div>
                <button
                    onClick={handleRetry}
                    className="px-6 py-2 bg-neon-red hover:bg-neon-red/80 rounded-lg text-white font-bold"
                >
                    Spróbuj ponownie
                </button>
            </div>
        );
    }

    // 1. CONTEXT STEP
    if (step === "CONTEXT") {
        if (!contextQuestions) return <div className="p-10 text-center text-gray-400">Ładowanie kontekstu...</div>;

        return (
            <div className="max-w-3xl mx-auto">
                {renderProgressBar()}

                <GlassCard>
                    <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                        <Users className="text-neon-red" />
                        Kontekst Klienta
                    </h2>

                    <div className="space-y-6">
                        {/* Typ Klienta */}
                        <div>
                            <label className="block text-sm font-medium text-gray-400 mb-2">Typ Klienta</label>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                {contextQuestions.typ_klienta.options.map((opt: any) => (
                                    <button
                                        key={opt.value}
                                        onClick={() => setContext({ ...context, typ_klienta: opt.value })}
                                        className={cn(
                                            "p-3 rounded-xl border text-left transition-all",
                                            context.typ_klienta === opt.value
                                                ? "border-neon-red bg-neon-red/10 text-white"
                                                : "border-white/10 hover:bg-white/5 text-gray-400"
                                        )}
                                    >
                                        <div className="font-semibold">{opt.label}</div>
                                        <div className="text-xs opacity-70">{opt.description}</div>
                                    </button>
                                ))}
                            </div>
                        </div>

                        {/* Typ Pracy */}
                        <div>
                            <label className="block text-sm font-medium text-gray-400 mb-2">Typ Pracy</label>
                            <select
                                className="w-full p-3 rounded-xl bg-black/40 border border-white/10 text-white focus:border-neon-red outline-none"
                                value={context.typ_pracy}
                                onChange={(e) => setContext({ ...context, typ_pracy: e.target.value })}
                            >
                                <option value="">Wybierz...</option>
                                {contextQuestions.typ_pracy.options.map((opt: any) => (
                                    <option key={opt.value} value={opt.value}>{opt.label}</option>
                                ))}
                            </select>
                        </div>

                        {/* Materiały (Multi) */}
                        <div>
                            <label className="block text-sm font-medium text-gray-400 mb-2">Materiały / Środowisko</label>
                            <div className="flex flex-wrap gap-2">
                                {contextQuestions.materialy_srodowisko.options.map((opt: any) => {
                                    const isSelected = context.materialy_srodowisko.includes(opt.value);
                                    return (
                                        <button
                                            key={opt.value}
                                            onClick={() => {
                                                const newMats = isSelected
                                                    ? context.materialy_srodowisko.filter(m => m !== opt.value)
                                                    : [...context.materialy_srodowisko, opt.value];
                                                setContext({ ...context, materialy_srodowisko: newMats });
                                            }}
                                            className={cn(
                                                "px-4 py-2 rounded-full text-sm border transition-all",
                                                isSelected
                                                    ? "bg-neon-red text-white border-neon-red"
                                                    : "bg-transparent text-gray-400 border-white/20 hover:border-white/40"
                                            )}
                                        >
                                            {opt.label}
                                        </button>
                                    );
                                })}
                            </div>
                        </div>

                        {/* Skala */}
                        <div>
                            <label className="block text-sm font-medium text-gray-400 mb-2">Skala Działalności</label>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                                {contextQuestions.skala.options.map((opt: any) => (
                                    <button
                                        key={opt.value}
                                        onClick={() => setContext({ ...context, skala: opt.value })}
                                        className={cn(
                                            "p-3 rounded-xl border text-center transition-all",
                                            context.skala === opt.value
                                                ? "border-neon-red bg-neon-red/10 text-white"
                                                : "border-white/10 hover:bg-white/5 text-gray-400"
                                        )}
                                    >
                                        <div className="font-semibold">{opt.label}</div>
                                    </button>
                                ))}
                            </div>
                        </div>

                        <div className="pt-6 border-t border-white/10 flex justify-end">
                            <button
                                onClick={handleContextSubmit}
                                disabled={!context.typ_klienta || !context.typ_pracy || context.materialy_srodowisko.length === 0 || loading}
                                className="px-6 py-3 bg-neon-red hover:bg-neon-red/80 disabled:opacity-50 disabled:cursor-not-allowed rounded-xl text-white font-bold flex items-center gap-2 transition-colors"
                            >
                                {loading ? "Przetwarzanie..." : "Znajdź Rozwiązania"} <ChevronRight />
                            </button>
                        </div>
                    </div>
                </GlassCard>
            </div>
        );
    }

    // 2. APP SELECTION
    if (step === "APP_SELECTION") {
        return (
            <div className="max-w-4xl mx-auto">
                {renderProgressBar()}

                <h2 className="text-2xl font-bold mb-6 text-center">Sugerowane Aplikacje</h2>

                <div className="grid grid-cols-1 gap-4">
                    {appMatches.map((match) => (
                        <GlassCard key={match.app_id} className="hover:border-neon-red/50 transition-colors group cursor-pointer" onClick={() => handleAppSelect(match.app_id)}>
                            <div className="flex items-center gap-6">
                                <div className="w-16 h-16 rounded-xl bg-neon-red/10 flex items-center justify-center text-3xl">
                                    {match.details.icon || "🔧"}
                                </div>
                                <div className="flex-1">
                                    <div className="flex items-center justify-between mb-1">
                                        <h3 className="text-xl font-bold group-hover:text-neon-red transition-colors">{match.details.title}</h3>
                                        <div className="text-neon-red font-mono font-bold">{match.score.toFixed(0)}% Dopasowania</div>
                                    </div>
                                    <p className="text-gray-400 text-sm mb-2">{match.reason}</p>
                                    <div className="flex flex-wrap gap-2">
                                        {match.details.charakterystyka?.slice(0, 3).map((char: string) => (
                                            <span key={char} className="px-2 py-1 rounded bg-white/5 text-xs text-gray-300">{char}</span>
                                        ))}
                                    </div>
                                </div>
                                <ChevronRight className="text-gray-600 group-hover:text-white" />
                            </div>
                        </GlassCard>
                    ))}
                </div>

                <div className="mt-6 text-center">
                    <button onClick={() => setStep("CONTEXT")} className="text-gray-500 hover:text-white transition-colors">
                        ← Wróć do kontekstu
                    </button>
                </div>
            </div>
        );
    }

    // 3. DISCOVERY
    if (step === "DISCOVERY") {
        return (
            <div className="max-w-3xl mx-auto">
                {renderProgressBar()}

                <GlassCard>
                    <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                        <MessageSquare className="text-neon-red" />
                        Pytania Pogłębiające
                    </h2>
                    <p className="text-gray-400 mb-6">Doprecyzuj szczegóły, aby otrzymać idealną rekomendację.</p>

                    <div className="space-y-8">
                        {discoveryQuestions.length > 0 ? discoveryQuestions.map((q) => (
                            <div key={q.id} className="space-y-2">
                                <label className="block font-medium text-white">{q.question}</label>
                                {q.purpose && <p className="text-xs text-gray-500 mb-2">{q.purpose}</p>}

                                {/* Simple render logic for brevity */}
                                {q.type === 'choice' && (
                                    <div className="flex flex-wrap gap-2">
                                        {q.options?.map(opt => (
                                            <button
                                                key={opt}
                                                onClick={() => setAnswers({ ...answers, [q.id]: opt })}
                                                className={cn(
                                                    "px-4 py-2 rounded-lg border text-sm transition-all",
                                                    answers[q.id] === opt
                                                        ? "bg-neon-red border-neon-red text-white"
                                                        : "border-white/20 hover:bg-white/5 text-gray-400"
                                                )}
                                            >
                                                {opt}
                                            </button>
                                        ))}
                                    </div>
                                )}
                                {q.type === 'yes_no' && (
                                    <div className="flex gap-4">
                                        {['Tak', 'Nie'].map(opt => (
                                            <button
                                                key={opt}
                                                onClick={() => setAnswers({ ...answers, [q.id]: opt })}
                                                className={cn(
                                                    "px-6 py-2 rounded-lg border text-sm transition-all",
                                                    answers[q.id] === opt
                                                        ? "bg-neon-red border-neon-red text-white"
                                                        : "border-white/20 hover:bg-white/5 text-gray-400"
                                                )}
                                            >
                                                {opt}
                                            </button>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )) : (
                            <div className="text-center py-10 text-gray-500">
                                Brak dodatkowych pytań dla tego scenariusza.
                            </div>
                        )}

                        <div className="pt-6 border-t border-white/10 flex justify-between">
                            <button onClick={() => setStep("APP_SELECTION")} className="text-gray-400 hover:text-white">
                                Wstecz
                            </button>
                            <button
                                onClick={handleDiscoverySubmit}
                                disabled={loading}
                                className="px-6 py-3 bg-neon-red hover:bg-neon-red/80 rounded-xl text-white font-bold transition-colors"
                            >
                                Generuj Rekomendację
                            </button>
                        </div>
                    </div>
                </GlassCard>
            </div>
        );
    }

    // 4. RECOMMENDATION
    if (step === "RECOMMENDATION" && recommendation) {
        return (
            <div className="max-w-5xl mx-auto space-y-6">
                {renderProgressBar()}

                <div className="text-center mb-8">
                    <h1 className="text-4xl font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-neon-red to-orange-500">
                        Rekomendacja Systemowa
                    </h1>
                    <p className="text-gray-400">Wygenerowano na podstawie analizy kontekstu i potrzeb.</p>
                </div>

                {/* TABS (Simplified) */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <GlassCard>
                        <h3 className="text-xl font-bold mb-4 flex items-center gap-2"><Briefcase /> Pakiet Produktów</h3>
                        <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
                            {recommendation.package.narzedzia?.map((tool: any) => (
                                <div key={tool.name} className="p-3 bg-white/5 rounded-lg border border-white/5">
                                    <div className="flex justify-between font-bold">
                                        <span>{tool.name}</span>
                                        <span className="text-neon-red">{tool.price} PLN</span>
                                    </div>
                                    <div className="text-xs text-gray-400 mt-1">{tool.reason}</div>
                                </div>
                            ))}
                            <div className="pt-4 border-t border-white/10 flex justify-between text-xl font-bold">
                                <span>Razem:</span>
                                <span>{recommendation.package.total_price} PLN</span>
                            </div>
                        </div>
                    </GlassCard>

                    <GlassCard>
                        <h3 className="text-xl font-bold mb-4 flex items-center gap-2"><MessageSquare /> Skrypt Perswazyjny</h3>
                        <div className="space-y-4">
                            <div className="p-3 bg-blue-500/10 border border-blue-500/30 rounded-lg">
                                <div className="text-xs text-blue-400 uppercase font-bold">Headline</div>
                                <div className="font-medium">"{recommendation.persuasion_script?.headline}"</div>
                            </div>
                            <div>
                                <div className="text-xs text-gray-500 uppercase font-bold mb-1">Problem</div>
                                <p className="text-sm">{recommendation.persuasion_script?.problem}</p>
                            </div>
                            <div>
                                <div className="text-xs text-gray-500 uppercase font-bold mb-1">Rozwiązanie</div>
                                <p className="text-sm">{recommendation.persuasion_script?.solution}</p>
                            </div>
                        </div>
                    </GlassCard>
                </div>

                <div className="flex justify-center gap-4 mt-8">
                    <button onClick={() => window.print()} className="px-6 py-3 bg-white/10 hover:bg-white/20 rounded-xl transition-colors">
                        Drukuj / PDF
                    </button>
                    <button onClick={() => setStep("CONTEXT")} className="px-6 py-3 bg-neon-red hover:bg-neon-red/80 rounded-xl font-bold transition-colors">
                        Nowa Symulacja
                    </button>
                </div>
            </div>
        );
    }

    return null;
}
