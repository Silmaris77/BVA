'use client';

import { useState } from 'react';
import { CheckCircle2, XCircle, ArrowRight, BrainCircuit, Shield } from 'lucide-react';

export default function TheoryTestPage() {
    const [selected, setSelected] = useState<number | null>(null);
    const [submitted, setSubmitted] = useState(false);

    const scenario = {
        title: "Obiekcje Cenowe",
        context: "Jesteś na budowie. Kierownik mówi: 'Fajne to wasze M18, ale Hilti daje nam lepszy serwis w cenie, a DeWalt jest tańszy. Czemu mam przepłacać?'",
        question: "Jaka jest Twoja pierwsza reakcja (zgodnie z metodologią Application First)?",
        options: [
            { id: 1, text: "Pokazuję tabelę porównawczą momentu obrotowego, gdzie M18 wygrywa.", feedback: "Błąd. To jest walka na parametry (Produkt), a nie Application First.", correct: false },
            { id: 2, text: "Pytam: 'A ile dokładnie płacicie za serwis Hilti? Może policzymy TCO?'", feedback: "Ryzykowne. Wchodzisz w dyskusję finansową za wcześnie, nie znając problemów operacyjnych.", correct: false },
            { id: 3, text: "Pytam: 'Rozumiem. A jak często serwisy powodują przestoje w Waszej pracy tu na budowie?'", feedback: "Doskonale! Przekierowujesz rozmowę z Ceny na Koszt Problemu (Przestoje).", correct: true },
            { id: 4, text: "Daję rabat 10% na start, żeby wyrównać ofertę.", feedback: "Krytyczny błąd. Obniżasz wartość zanim ją zbudowałeś.", correct: false },
        ]
    };

    return (
        <div className="min-h-screen bg-neutral-950 text-white font-sans flex items-center justify-center p-4">
            <div className="max-w-md w-full bg-neutral-900 border border-white/10 rounded-2xl overflow-hidden shadow-2xl">

                {/* Header */}
                <div className="bg-gradient-to-r from-blue-900/40 to-neutral-900 p-6 border-b border-white/5">
                    <div className="flex justify-between items-center mb-4">
                        <div className="flex items-center gap-2 text-blue-400">
                            <BrainCircuit size={18} />
                            <span className="text-xs font-bold uppercase tracking-widest">Theory Check</span>
                        </div>
                        <span className="text-xs text-gray-500">Scenariusz 3/5</span>
                    </div>
                    <h1 className="text-xl font-bold leading-tight">{scenario.title}</h1>
                </div>

                {/* Scenario Context */}
                <div className="p-6 space-y-6">
                    <div className="bg-white/5 p-4 rounded-xl border border-white/5 text-sm leading-relaxed text-gray-200 italic">
                        "{scenario.context}"
                    </div>
                    <p className="font-bold text-sm text-gray-400">{scenario.question}</p>

                    {/* Options */}
                    <div className="space-y-3">
                        {scenario.options.map((opt) => (
                            <button
                                key={opt.id}
                                onClick={() => !submitted && setSelected(opt.id)}
                                disabled={submitted}
                                className={`w-full text-left p-4 rounded-xl text-sm border transition-all duration-200
                                    ${submitted && opt.correct ? 'bg-green-500/20 border-green-500 text-green-100' :
                                        submitted && selected === opt.id && !opt.correct ? 'bg-red-500/20 border-red-500 text-red-100' :
                                            selected === opt.id ? 'bg-blue-600 border-blue-500 text-white shadow-lg shadow-blue-900/20' :
                                                'bg-neutral-800 border-white/5 text-gray-400 hover:bg-neutral-800/80 hover:border-white/10'}
                                    ${submitted ? 'cursor-default' : 'cursor-pointer'}
                                `}
                            >
                                <div className="flex items-start gap-3">
                                    <div className={`mt-0.5 w-4 h-4 rounded-full border flex items-center justify-center shrink-0
                                        ${submitted && opt.correct ? 'border-green-500 bg-green-500' :
                                            submitted && selected === opt.id && !opt.correct ? 'border-red-500 bg-red-500' :
                                                selected === opt.id ? 'border-white bg-white' : 'border-gray-600'}
                                    `}>
                                        {(submitted || selected === opt.id) && <div className={`w-1.5 h-1.5 rounded-full ${selected === opt.id && !submitted ? 'bg-blue-600' : 'bg-neutral-900'}`} />}
                                    </div>
                                    <span>{opt.text}</span>
                                </div>

                                {/* Feedback */}
                                {submitted && (selected === opt.id || opt.correct) && (
                                    <div className={`mt-3 pt-3 border-t text-xs font-bold
                                        ${opt.correct ? 'border-green-500/30 text-green-400' : 'border-red-500/30 text-red-400'}
                                    `}>
                                        {opt.feedback}
                                    </div>
                                )}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Footer Controls */}
                <div className="p-4 border-t border-white/5 bg-neutral-950/30">
                    {!submitted ? (
                        <button
                            onClick={() => setSubmitted(true)}
                            disabled={selected === null}
                            className="w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 rounded-xl transition-all shadow-lg shadow-blue-900/20"
                        >
                            Zatwierdź Decyzję
                        </button>
                    ) : (
                        <button className="w-full bg-white hover:bg-gray-200 text-black font-bold py-3 rounded-xl transition-all flex items-center justify-center gap-2">
                            Następny Scenariusz <ArrowRight size={18} />
                        </button>
                    )}
                </div>

            </div>
        </div>
    );
}
