import React, { useState } from 'react';
import { advanceTime } from '@/lib/games/consulting/actions';
import { ConsultingGameState, Department, ViewType } from '@/lib/games/consulting/types';

interface DashboardViewProps {
    gameState: ConsultingGameState;
    onViewChange?: (view: ViewType) => void;
}

export default function DashboardView({ gameState, onViewChange }: DashboardViewProps) {
    const { departments, resources } = gameState;
    // Forced Slider View
    return (
        <div className="flex-1 grid grid-rows-[auto_1fr] gap-6 h-full p-2 overflow-hidden">

            {/* ROW 1: ACTIVE & MARKET (Compact) */}
            <section className="grid grid-cols-1 md:grid-cols-12 gap-4 h-auto md:h-52 shrink-0">

                {/* Active Operations */}
                <div className="col-span-1 md:col-span-8 flex flex-col min-h-0">
                    <div className="flex items-center justify-between mb-2 px-1">
                        <h2 className="text-xs font-bold uppercase text-[var(--accent-blue)] tracking-widest"><i className="fa-solid fa-play mr-2"></i>Aktywne Projekty</h2>
                    </div>

                    {/* CONTENT AREA: SLIDER */}
                    <div className="flex-1 flex overflow-x-auto gap-4 px-1 pb-2 snap-x items-stretch scrollbar-thin scrollbar-thumb-[var(--accent-blue)]/30 scrollbar-track-white/5 hover:scrollbar-thumb-[var(--accent-blue)]/60 transition-colors">
                        {gameState.active_contracts.length === 0 && (
                            <div className="w-full glass-card p-4 rounded-xl border border-white/5 flex items-center justify-center text-gray-500 text-xs text-center border-dashed">
                                Brak aktywnych projektów. <br /> Odwiedź Rynek Globalny.
                            </div>
                        )}
                        {gameState.active_contracts.map((contract) => (
                            <div key={contract.id} className="glass-card p-4 rounded-xl border-l-4 border-[var(--accent-blue)] relative group hover:bg-white/5 transition cursor-pointer min-w-[280px] w-[280px] shrink-0 snap-start flex flex-col justify-between">
                                <div>
                                    <div className="flex justify-between mb-2">
                                        <span className={`text-[10px] px-2 py-0.5 rounded border ${contract.topic === 'Strategy' ? 'bg-blue-500/10 text-blue-300 border-blue-500/20' :
                                            contract.topic === 'IT' ? 'bg-purple-500/10 text-purple-300 border-purple-500/20' :
                                                'bg-green-500/10 text-green-300 border-green-500/20'}`}>
                                            {contract.topic.toUpperCase()}
                                        </span>
                                        <span className="text-[10px] text-gray-400 bg-black/40 px-1.5 rounded">
                                            {contract.deadline ? new Date(contract.deadline).toLocaleDateString(undefined, { month: 'numeric', day: 'numeric' }) : 'N/A'}
                                        </span>
                                    </div>
                                    <h3 className="font-bold text-sm mb-1 text-white truncate" title={contract.title}>{contract.title}</h3>
                                    <div className="w-full bg-gray-700/50 h-1 rounded-full overflow-hidden mb-2 mt-2">
                                        <div className="bg-[var(--accent-blue)] h-full transition-all duration-500" style={{ width: `${contract.progress || 0}%` }}></div>
                                    </div>
                                </div>
                                <div className="flex justify-between text-[10px] text-gray-400 items-center mt-2">
                                    <span>Postęp: {contract.progress || 0}%</span>
                                    <form action={async () => { await advanceTime(); }}>
                                        <button className="text-[var(--accent-blue)] hover:text-white transition px-2 py-1 bg-blue-500/10 rounded hover:bg-blue-500/20"><i className="fa-solid fa-play mr-1"></i> Pracuj</button>
                                    </form>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Live Intel (Events & Auctions) */}
                <div className="col-span-1 md:col-span-4 flex flex-col">
                    <div className="flex items-center justify-between mb-2 px-1">
                        <h2 className="text-xs font-bold uppercase text-[var(--accent-gold)] tracking-widest"><i className="fa-solid fa-satellite-dish mr-2"></i>Wywiad Gospodarczy</h2>
                        <span className="text-[10px] text-[var(--accent-red)] font-mono animate-pulse">Pobieranie Danych...</span>
                    </div>

                    <div className="flex-1 glass-card p-0 rounded-xl border border-[var(--accent-gold)]/20 relative overflow-hidden flex flex-col bg-black/20">
                        {/* Events Feed (Mock + Real) */}
                        {gameState.active_events.map(event => (
                            <div key={event.id} className="p-3 border-b border-white/10 bg-red-500/10 flex gap-3 items-center">
                                <div className="w-8 h-8 rounded bg-red-500/20 flex items-center justify-center shrink-0">
                                    <i className="fa-solid fa-triangle-exclamation text-[var(--accent-red)]"></i>
                                </div>
                                <div>
                                    <h4 className="text-xs font-bold text-white leading-tight">{event.title}</h4>
                                    <p className="text-[10px] text-gray-400">{event.description}</p>
                                </div>
                            </div>
                        ))}

                        {/* Auction Item (Mock) */}
                        <div className="p-3 flex gap-3 items-center hover:bg-white/5 transition cursor-pointer">
                            <div className="w-8 h-8 rounded bg-[var(--accent-gold)]/20 flex items-center justify-center shrink-0">
                                <i className="fa-solid fa-gavel text-[var(--accent-gold)]"></i>
                            </div>
                            <div className="flex-1">
                                <div className="flex justify-between items-center mb-1">
                                    <h4 className="text-xs font-bold text-white leading-tight">Global Crisis Mgmt</h4>
                                    <span className="text-[9px] font-mono text-[var(--accent-gold)]">4,500 C</span>
                                </div>
                                <div className="w-full bg-gray-700 h-1 rounded-full overflow-hidden">
                                    <div className="bg-[var(--accent-gold)] w-[70%] h-full"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* ROW 2: DEPARTMENT CARDS (3x2 Grid) */}
            <section className="grid grid-cols-1 md:grid-cols-3 gap-3 pb-2 pt-2 px-1 overflow-y-auto min-h-0 content-start">
                <DepartmentCard dept={departments.office} title="Siedziba Główna" icon="fa-building" color="text-[var(--accent-blue)]"
                    stats={[{ label: 'Miejsca', value: `${departments.office.stats.capacity}/20` }, { label: 'Zajętość', value: '34%' }]}
                    image="https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=600&q=80"
                    onClick={() => onViewChange?.('office')}
                />
                <DepartmentCard dept={departments.finance} title="Finanse" icon="fa-sack-dollar" color="text-[var(--accent-green)]"
                    stats={[{ label: 'Marża', value: '+35%' }, { label: 'Runway', value: '42d' }]}
                    image="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=600&q=80"
                    overlayColor="bg-green-900/10 mix-blend-overlay"
                />
                <DepartmentCard dept={departments.research} title="Laboratorium R&D" icon="fa-microchip" color="text-[var(--accent-blue)]"
                    stats={[{ label: 'Aktywne', value: '3' }, { label: 'Badania', value: 'W toku...' }]}
                    image="https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&w=600&q=80"
                    overlayColor="bg-blue-900/10 mix-blend-overlay"
                />
                <DepartmentCard dept={departments.hr} title="Dział Kadr" icon="fa-users" color="text-[var(--accent-purple)]"
                    stats={[{ label: 'Zespół', value: `${departments.hr.stats.max_employees}` }, { label: 'Morale', value: '92%' }]}
                    image="https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=600&q=80"
                    onClick={() => onViewChange?.('team')}
                />
                <DepartmentCard dept={departments.sales} title="Sprzedaż i Oferty" icon="fa-handshake" color="text-[var(--accent-gold)]"
                    stats={[{ label: 'Skuteczność', value: '68%' }, { label: 'Trend', value: 'Wzrost' }]}
                    image="https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=600&q=80"
                />
                <DepartmentCard dept={departments.marketing} title="Marketing" icon="fa-bullhorn" color="text-pink-500"
                    stats={[{ label: 'Widoczność', value: 'Wysoka' }, { label: 'Zasięg', value: '12k' }]}
                    image="https://images.unsplash.com/photo-1533750516457-a7f992034fec?auto=format&fit=crop&w=600&q=80"
                />
            </section>
        </div>
    );
}

function DepartmentCard({ dept, title, icon, color, stats, image, overlayColor, onClick }: any) {
    return (
        <div onClick={onClick} className={`dept-card glass-card rounded-2xl border border-white/10 group cursor-pointer flex flex-col h-40 relative overflow-hidden shrink-0 hover:translate-y-[-2px] transition duration-300 ${onClick ? 'hover:border-blue-400/50' : ''}`}>
            <div className="absolute inset-0 bg-cover bg-center transition duration-700 group-hover:scale-105 opacity-40" style={{ backgroundImage: `url('${image}')` }}></div>
            {overlayColor && <div className={`absolute inset-0 ${overlayColor}`}></div>}

            <div className="dept-content flex-1 p-4 flex flex-col justify-end relative z-10">
                <div className="mb-2">
                    <span className={`text-[10px] font-bold uppercase tracking-wider block mb-1 ${color}`}>{dept.id}</span>
                    <h3 className="text-lg font-bold text-white">{title}</h3>
                </div>
                <div className="flex justify-between text-[10px] border-t border-white/20 pt-2">
                    {stats.map((stat: any, i: number) => (
                        <span key={i} className="text-gray-400">{stat.label}: <span className="text-white font-mono">{stat.value}</span></span>
                    ))}
                </div>
            </div>
            {/* Gradient Overlay for text readability */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent pointer-events-none"></div>
        </div>
    );
}
