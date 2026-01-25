'use client';

import React from 'react';
import { hireEmployeeAction } from '@/lib/games/consulting/actions';
import { Employee } from '@/lib/games/consulting/types';

interface TeamViewProps {
    employees: Employee[];
}

export default function TeamView({ employees = [] }: TeamViewProps) {
    return (
        <div className="h-full flex flex-col p-4 gap-6 overflow-hidden">
            <div className="flex justify-between items-center mb-2">
                <div>
                    <h2 className="text-2xl font-bold text-white uppercase tracking-wider flex items-center gap-3">
                        <i className="fa-solid fa-users text-[var(--accent-purple)]"></i>
                        Zarządzanie Zespołem
                    </h2>
                    <p className="text-sm text-gray-400">Rekrutuj i zarządzaj swoim zespołem konsultantów.</p>
                </div>
                <div className="bg-white/5 px-4 py-2 rounded-lg border border-white/10 text-right">
                    <p className="text-[10px] uppercase font-bold text-gray-500 tracking-wider">Zespół</p>
                    <p className="text-xl font-mono font-bold text-white">{employees.length} <span className="text-gray-500 text-sm">/ 12</span></p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full overflow-hidden">
                {/* LEFT: Current Team */}
                <div className="flex flex-col glass-card border-white/5 rounded-xl overflow-hidden">
                    <div className="p-3 border-b border-white/5 bg-white/5 font-bold text-sm text-[var(--accent-purple)] uppercase tracking-wider">
                        Aktywny Skład
                    </div>
                    <div className="flex-1 overflow-y-auto p-2 flex flex-col gap-2">
                        {employees.length === 0 && (
                            <div className="text-center p-10 text-gray-500 text-sm border-2 border-dashed border-white/5 rounded-xl">
                                Brak pracowników. <br /> Zatrudnij kogoś z rynku.
                            </div>
                        )}
                        {employees.map(emp => (
                            <div key={emp.id} className="p-3 bg-white/5 hover:bg-white/10 rounded-lg flex items-center justify-between border border-transparent hover:border-white/10 transition cursor-pointer group">
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center font-bold text-white">
                                        {emp.name.substring(0, 2).toUpperCase()}
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-white text-sm">{emp.name}</h4>
                                        <span className="text-[10px] text-gray-400 uppercase bg-black/30 px-1.5 rounded">{emp.role}</span>
                                        <span className="text-[10px] text-[var(--accent-blue)] ml-2">{emp.specialty}</span>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <p className="text-[10px] text-gray-500">Salary</p>
                                    <p className="font-mono text-white text-sm">{emp.salary.toLocaleString()} <span className="text-[var(--accent-gold)]">C</span></p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* RIGHT: Recruitment */}
                <div className="flex flex-col gap-4">
                    <div className="glass-card border-white/5 rounded-xl p-6 flex flex-col gap-4 relative overflow-hidden group">
                        {/* Decoration */}
                        <div className="absolute top-0 right-0 w-32 h-32 bg-[var(--accent-purple)]/10 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none"></div>

                        <div className="flex justify-between items-start z-10">
                            <div>
                                <span className="px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 border border-blue-500/20 text-[10px] font-bold uppercase">Junior</span>
                                <h3 className="text-xl font-bold text-white mt-2">Młodszy Konsultant</h3>
                                <p className="text-xs text-gray-400 mt-1">Chętny do nauki. Dobry do prostych zadań.</p>
                            </div>
                            <div className="text-right">
                                <p className="text-2xl font-bold font-mono text-white">500 <span className="text-[var(--accent-gold)] text-sm">C</span></p>
                                <p className="text-[10px] text-gray-500 uppercase">Premia na start</p>
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-2 text-xs text-gray-300 z-10">
                            <div className="bg-black/20 p-2 rounded flex justify-between"><span>Umiejętności</span> <span className="text-white">1-3</span></div>
                            <div className="bg-black/20 p-2 rounded flex justify-between"><span>Pensja</span> <span className="text-white">Niska</span></div>
                        </div>

                        <form action={async () => { await hireEmployeeAction('Junior', 500); }}>
                            <button className="w-full py-3 bg-[var(--accent-purple)] hover:bg-purple-500 text-white font-bold uppercase tracking-widest rounded-lg transition shadow-lg z-10">
                                Zatrudnij Juniora
                            </button>
                        </form>
                    </div>

                    <div className="glass-card border-white/5 rounded-xl p-6 flex flex-col gap-4 relative overflow-hidden opacity-60 hover:opacity-100 transition">
                        <div className="flex justify-between items-start">
                            <div>
                                <span className="px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20 text-[10px] font-bold uppercase">Senior</span>
                                <h3 className="text-xl font-bold text-white mt-2">Ekspert / Senior</h3>
                                <p className="text-xs text-gray-400 mt-1">Doświadczony. Może prowadzić projekty.</p>
                            </div>
                            <div className="text-right">
                                <p className="text-2xl font-bold font-mono text-white">2,500 <span className="text-[var(--accent-gold)] text-sm">C</span></p>
                            </div>
                        </div>
                        <button className="w-full py-3 bg-white/5 text-gray-400 font-bold uppercase tracking-widest rounded-lg border border-white/10 hover:border-[var(--accent-purple)] hover:text-white transition">
                            Znajdź Kandydata
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
