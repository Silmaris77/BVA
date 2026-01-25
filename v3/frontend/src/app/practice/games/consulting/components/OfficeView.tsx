'use client';

import React from 'react';
import { upgradeOfficeAction } from '@/lib/games/consulting/actions';
import { Department } from '@/lib/games/consulting/types';

interface OfficeViewProps {
    office: Department;
}

export default function OfficeView({ office }: OfficeViewProps) {
    const nextLevelCost = office.level === 1 ? 5000 : office.level === 2 ? 15000 : 0;
    const nextLevelName = office.level === 1 ? 'Small Office' : office.level === 2 ? 'Downtown Floor' : 'Max Level';
    const currentName = office.level === 1 ? 'Home Office' : 'Small Office';

    return (
        <div className="h-full flex flex-col p-4 gap-6 overflow-hidden">
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h2 className="text-2xl font-bold text-white uppercase tracking-wider flex items-center gap-3">
                        <i className="fa-solid fa-building text-[var(--accent-blue)]"></i>
                        Rozbudowa Biura
                    </h2>
                    <p className="text-sm text-gray-400">Ulepszaj swoją siedzibę, aby zatrudniać więcej pracowników.</p>
                </div>
                <div className="bg-white/5 px-4 py-2 rounded-lg border border-white/10 text-right">
                    <p className="text-[10px] uppercase font-bold text-gray-500 tracking-wider">Status Bieżący</p>
                    <p className="text-xl font-mono font-bold text-white">Poziom {office.level}</p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 h-full">
                {/* CURRENT OFFICE */}
                <div className="glass-card p-0 rounded-2xl overflow-hidden flex flex-col relative border border-[var(--accent-blue)]">
                    <div className="absolute top-4 left-4 z-10 bg-[var(--accent-blue)] text-black font-bold px-3 py-1 rounded text-xs uppercase tracking-widest">
                        Current HQ
                    </div>
                    <div className="h-48 bg-cover bg-center" style={{ backgroundImage: 'url("https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80")' }}>
                        <div className="w-full h-full bg-gradient-to-t from-black via-transparent to-transparent"></div>
                    </div>
                    <div className="p-6 flex-1 flex flex-col gap-4">
                        <h3 className="text-2xl font-bold text-white">{currentName}</h3>
                        <div className="grid grid-cols-2 gap-4">
                            <Stat label="Capacity" value={`${office.stats.capacity} Desks`} />
                            <Stat label="Prestige" value="Low" />
                            <Stat label="Upkeep" value="-200/day" color="text-red-400" />
                        </div>
                    </div>
                </div>

                {/* UPGRADE PATH */}
                <div className="flex flex-col gap-4">
                    <h3 className="text-sm font-bold text-gray-400 uppercase tracking-widest">Dostępne Ulepszenie</h3>

                    <div className="glass-card p-6 rounded-2xl border border-white/10 flex flex-col gap-4 relative overflow-hidden group hover:border-[var(--accent-gold)] transition duration-300">
                        <div className="absolute inset-0 bg-blue-500/5 group-hover:bg-blue-500/10 transition"></div>

                        <div className="flex justify-between items-start z-10">
                            <div>
                                <h4 className="text-xl font-bold text-white">{nextLevelName}</h4>
                                <p className="text-sm text-gray-400 mt-1">Profesjonalna przestrzeń w dzielnicy.</p>
                            </div>
                            <div className="text-right">
                                <p className="text-2xl font-bold text-[var(--accent-gold)] font-mono">{nextLevelCost.toLocaleString()} C</p>
                            </div>
                        </div>

                        <div className="grid grid-cols-3 gap-2 my-2 z-10">
                            <Benefit icon="fa-user-plus" text="+4 Miejsca" />
                            <Benefit icon="fa-arrow-trend-up" text="+10% Rep" />
                            <Benefit icon="fa-bolt" text="Szybsze Operacje" />
                        </div>

                        <form action={async () => { await upgradeOfficeAction(); }}>
                            <button className="w-full py-4 bg-white/5 hover:bg-[var(--accent-gold)] hover:text-black border border-white/10 hover:border-[var(--accent-gold)] rounded-xl font-bold uppercase tracking-widest transition z-10 shadow-lg">
                                Kup Ulepszenie
                            </button>
                        </form>
                    </div>

                    <div className="mt-auto text-center p-4">
                        <p className="text-xs text-gray-500">Upgrading your office increases operational costs but unlocks higher tier contracts and more staff capacity.</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

function Stat({ label, value, color }: any) {
    return (
        <div>
            <p className="text-[10px] text-gray-500 uppercase">{label}</p>
            <p className={`font-mono font-bold ${color || 'text-white'}`}>{value}</p>
        </div>
    )
}

function Benefit({ icon, text }: any) {
    return (
        <div className="bg-black/20 rounded p-2 flex flex-col items-center gap-1 text-center">
            <i className={`fa-solid ${icon} text-[var(--accent-blue)]`}></i>
            <span className="text-[10px] text-gray-300 font-bold">{text}</span>
        </div>
    )
}
