'use client';

import { useState } from 'react';
import { CheckCircle2, Mic, Save, X, ChevronDown, ChevronUp, ScanFace, Info } from 'lucide-react';

export default function ShadowingToolPage() {
    // BARS Scale: 1 = Low, 5 = High
    const [scores, setScores] = useState<Record<string, number>>({});
    const [expandedSection, setExpandedSection] = useState<string | null>('diagnoza');

    const toggleScore = (section: string, value: number) => {
        setScores(prev => ({ ...prev, [section]: value }));
    };

    return (
        <div className="min-h-screen bg-black text-white font-sans max-w-md mx-auto border-x border-white/10 relative pb-24">

            {/* Nav */}
            <div className="sticky top-0 z-50 bg-black/80 backdrop-blur-md border-b border-white/10 p-4 flex justify-between items-center">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-orange-500 flex items-center justify-center font-bold text-xs">MT</div>
                    <div>
                        <h1 className="font-bold text-sm leading-none">Shadowing: Mike T.</h1>
                        <p className="text-[10px] text-gray-500 mt-0.5">Klient: Budmex SA • Wizyta Aplikacyjna</p>
                    </div>
                </div>
                <button className="text-gray-400 hover:text-white"><X size={20} /></button>
            </div>

            {/* Content */}
            <div className="p-4 space-y-6">

                {/* Section 1: Diagnoza */}
                <ShadowingSection
                    id="diagnoza"
                    title="1. DIAGNOZA (Application First)"
                    expanded={expandedSection === 'diagnoza'}
                    onToggle={() => setExpandedSection(expandedSection === 'diagnoza' ? null : 'diagnoza')}
                    score={scores['diagnoza']}
                    setScore={(v: number) => toggleScore('diagnoza', v)}
                    bars={[
                        { val: 1, desc: "Brak pytań. Od razu przeszedł do prezentacji produktu." },
                        { val: 3, desc: "Zadał pytania, ale powierzchowne. Nie dotarł do 'bólu'." },
                        { val: 5, desc: "Pełna diagnoza. Klient sam policzył koszt problemu." }
                    ]}
                />

                {/* Section 2: Prezentacja */}
                <ShadowingSection
                    id="prezentacja"
                    title="2. PREZENTACJA ROZWIĄZANIA"
                    expanded={expandedSection === 'prezentacja'}
                    onToggle={() => setExpandedSection(expandedSection === 'prezentacja' ? null : 'prezentacja')}
                    score={scores['prezentacja']}
                    setScore={(v: number) => toggleScore('prezentacja', v)}
                    bars={[
                        { val: 1, desc: "Prezentacja cech (katalogowa). Brak języka korzyści." },
                        { val: 3, desc: "Połączył produkt z problemem, ale chaotycznie." },
                        { val: 5, desc: "Idealny 'System Pitch'. Klient potwierdził wartość." }
                    ]}
                />

                {/* Section 3: Domknięcie */}
                <ShadowingSection
                    id="closing"
                    title="3. DOMKNIĘCIE (Next Steps)"
                    expanded={expandedSection === 'closing'}
                    onToggle={() => setExpandedSection(expandedSection === 'closing' ? null : 'closing')}
                    score={scores['closing']}
                    setScore={(v: number) => toggleScore('closing', v)}
                    bars={[
                        { val: 1, desc: "Brak ustaleń. 'Zdzwonimy się'." },
                        { val: 3, desc: "Ustalił kolejny krok, ale bez daty lub właściciela." },
                        { val: 5, desc: "Jasne Kto-Co-Kiedy. Wysłany invite/mail podsumowujący." }
                    ]}
                />

                {/* Notes */}
                <div className="bg-neutral-900 rounded-xl border border-white/10 p-4">
                    <label className="text-xs font-bold uppercase text-gray-500 mb-2 block">Szybkie wnioski (Voice Note)</label>
                    <div className="bg-neutral-950 h-24 rounded-lg border border-white/5 flex items-center justify-center cursor-pointer hover:bg-neutral-800 transition">
                        <div className="text-center space-y-2">
                            <div className="w-12 h-12 rounded-full bg-red-600 flex items-center justify-center mx-auto shadow-lg shadow-red-900/40">
                                <Mic size={20} fill="white" />
                            </div>
                            <p className="text-[10px] text-gray-400">Naciśnij, aby nagrać feedback</p>
                        </div>
                    </div>
                </div>

            </div>

            {/* Footer */}
            <div className="fixed bottom-0 left-0 right-0 bg-neutral-900 border-t border-white/10 p-4 max-w-md mx-auto">
                <button className="w-full bg-white text-black font-bold py-3 rounded-xl flex items-center justify-center gap-2 hover:bg-gray-200 transition">
                    <Save size={18} />
                    Zapisz Obserwację
                </button>
            </div>
        </div>
    );
}

// Helper Component for Sections
function ShadowingSection({ id, title, expanded, onToggle, score, setScore, bars }: any) {
    return (
        <div className={`rounded-xl border transition-all duration-300 overflow-hidden
            ${score ? 'bg-neutral-900 border-green-500/30' : 'bg-neutral-900 border-white/10'}
        `}>
            <button onClick={onToggle} className="w-full flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                    <div className={`w-6 h-6 rounded flex items-center justify-center text-xs font-bold transition-colors
                        ${score ? 'bg-green-500 text-black' : 'bg-neutral-800 text-gray-500'}
                    `}>
                        {score || id[0].toUpperCase()}
                    </div>
                    <span className={`text-sm font-bold ${score ? 'text-white' : 'text-gray-300'}`}>{title}</span>
                </div>
                {expanded ? <ChevronUp size={16} className="text-gray-500" /> : <ChevronDown size={16} className="text-gray-500" />}
            </button>

            {expanded && (
                <div className="p-4 pt-0 border-t border-white/5 space-y-4 animate-in slide-in-from-top-2">

                    {/* BARS Description Hints */}
                    <div className="space-y-2 mt-4">
                        {bars.map((bar: any) => (
                            <div key={bar.val}
                                onClick={() => setScore(bar.val)}
                                className={`text-xs p-3 rounded-lg border cursor-pointer transition-all
                                ${score === bar.val
                                        ? 'bg-green-500/10 border-green-500 text-white'
                                        : 'bg-neutral-950/50 border-white/5 text-gray-500 hover:border-white/20 hover:text-gray-300'}
                            `}>
                                <div className="flex gap-2">
                                    <span className={`font-bold ${score === bar.val ? 'text-green-500' : 'text-gray-600'}`}>{bar.val}</span>
                                    <span>{bar.desc}</span>
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Slider Visualization (Simple Dots for MVP) */}
                    <div className="flex justify-between items-center px-2 pt-2">
                        {[1, 2, 3, 4, 5].map(val => (
                            <button
                                key={val}
                                onClick={() => setScore(val)}
                                className={`w-8 h-8 rounded-full font-bold text-xs flex items-center justify-center border transition-all
                                    ${score === val
                                        ? 'bg-green-500 border-green-500 text-black scale-110 shadow-lg shadow-green-900/50'
                                        : 'bg-neutral-800 border-white/5 text-gray-500 hover:bg-neutral-700'}
                                `}
                            >
                                {val}
                            </button>
                        ))}
                    </div>

                </div>
            )}
        </div>
    );
}
