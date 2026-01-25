import React from 'react';
import { Contract } from '@/lib/games/consulting/types';

interface ContractsViewProps {
    contracts: Contract[]; // Passed from parent or fetched
}

export default function ContractsView({ contracts = [], onAccept, onRefresh }: any) {
    return (
        <div className="h-full flex flex-col p-4">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-white uppercase tracking-wider flex items-center gap-3">
                    <i className="fa-solid fa-globe text-[var(--accent-blue)]"></i>
                    Globalny Rynek Zleceń
                </h2>
                <div className="flex gap-2">
                    <button onClick={onRefresh} className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-xs font-bold uppercase tracking-wider transition flex items-center gap-2">
                        <i className="fa-solid fa-sync"></i> Aktualizacja
                    </button>
                    <div className="flex gap-2 border-l border-white/10 pl-4">
                        <button className="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-xs font-bold uppercase tracking-wider border border-white/10 transition">Strategia</button>
                        <button className="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-xs font-bold uppercase tracking-wider border border-white/10 transition">Systemy IT</button>
                        <button className="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-xs font-bold uppercase tracking-wider border border-white/10 transition">HR</button>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 overflow-y-auto pb-10">
                {contracts.length === 0 && (
                    <div className="col-span-full flex flex-col items-center justify-center p-10 border-2 border-dashed border-white/10 rounded-xl">
                        <p className="text-gray-500 mb-4">Brak dostępnych zleceń.</p>
                        <button onClick={onRefresh} className="px-6 py-3 bg-[var(--accent-blue)] text-black font-bold uppercase rounded-lg hover:scale-105 transition">
                            Generuj Nowe Leady
                        </button>
                    </div>
                )}

                {contracts.map((c: any) => (
                    <ContractCard
                        key={c.id}
                        id={c.id}
                        title={c.title}
                        reward={c.reward.coins.toLocaleString()}
                        type={c.topic}
                        description={c.description}
                        difficulty={c.difficulty}
                        reputation={c.requirements?.min_reputation || 0}
                        negotiation={c.negotiation_required}
                        onAccept={() => onAccept && onAccept(c.id)}
                    />
                ))}
            </div>
        </div>
    );
}

function ContractCard({ id, title, reward, type, description, difficulty, negotiation, onAccept }: any) {
    return (
        <div className={`glass-card p-6 rounded-xl border relative group hover:border-[var(--accent-blue)] transition cursor-pointer flex flex-col gap-5 overflow-visible min-h-[320px] ${negotiation ? 'border-[var(--accent-purple)]/30' : 'border-white/10'}`}>
            <div className="flex justify-between items-start">
                <span className={`text-[10px] font-bold px-2 py-1 rounded border ${type === 'Strategy' ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' :
                    type === 'IT' ? 'bg-purple-500/10 text-purple-400 border-purple-500/20' :
                        'bg-green-500/10 text-green-400 border-green-500/20'
                    }`}>
                    {type ? type.toUpperCase() : 'GENERAL'}
                </span>
                {negotiation && <span className="text-[10px] font-bold text-[var(--accent-purple)] flex items-center gap-1"><i className="fa-solid fa-handshake"></i> NEGOCJACJE</span>}
                {!negotiation && <span className="text-[10px] font-bold text-green-400 flex items-center gap-1"><i className="fa-solid fa-check"></i> NATYCHMIAST</span>}
            </div>

            <div>
                <h3 className="text-lg font-bold text-white leading-tight mb-1">{title}</h3>
                <p className="text-xs text-gray-400 line-clamp-2">{description}</p>
            </div>

            <div className="grid grid-cols-2 gap-4 my-2 border-y border-white/5 py-3">
                <div>
                    <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Wynagrodzenie</p>
                    <p className="text-lg font-mono font-bold text-white">{reward} <span className="text-[10px] text-[var(--accent-gold)]">C</span></p>
                </div>
                <div className="text-right">
                    <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Trudność</p>
                    <p className={`text-sm font-bold ${difficulty === 'Hard' ? 'text-red-400' : 'text-gray-300'}`}>
                        {difficulty}
                    </p>
                </div>
            </div>

            <button
                onClick={(e) => { e.stopPropagation(); onAccept(); }}
                className={`w-full py-3 rounded-lg font-bold text-[10px] md:text-xs uppercase tracking-widest transition shadow-lg mt-auto hover:-translate-y-0.5 relative z-10 ${negotiation
                    ? 'bg-[var(--accent-purple)] text-white hover:bg-purple-500 hover:shadow-[0_0_20px_rgba(168,85,247,0.5)]'
                    : 'bg-[var(--accent-blue)] text-black hover:bg-cyan-400 hover:shadow-[0_0_20px_rgba(0,212,255,0.5)]'
                    }`}>
                <span className="flex items-center justify-center gap-2">
                    {negotiation ? <i className="fa-solid fa-handshake"></i> : <i className="fa-solid fa-check"></i>}
                    {negotiation ? 'Negocjuj' : 'Przyjmij'}
                </span>
            </button>
        </div>
    )
}
