'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ConsultingGameState, ViewType } from '@/lib/games/consulting/types';
import { acceptContractAction, refreshGlobalMarketAction } from '@/lib/games/consulting/actions';
import DashboardView from '@/app/practice/games/consulting/components/DashboardView';
import ContractsView from '@/app/practice/games/consulting/components/ContractsView';
import NegotiationView from '@/app/practice/games/consulting/components/NegotiationView';
import ResearchView from '@/app/practice/games/consulting/components/ResearchView';
import TeamView from '@/app/practice/games/consulting/components/TeamView';
import OfficeView from '@/app/practice/games/consulting/components/OfficeView';

interface ConsultingGameLayoutProps {
    initialState: ConsultingGameState;
    children?: React.ReactNode; // This will likely be the view switcher based on state
}

export default function ConsultingGameLayout({ initialState }: ConsultingGameLayoutProps) {
    const router = useRouter();
    const [currentView, setCurrentView] = useState<ViewType>('dashboard');
    const [theme, setTheme] = useState<'cyber' | 'light' | 'slate' | 'graphite'>('cyber');
    const [showSettings, setShowSettings] = useState(false);

    // Theme application logic
    useEffect(() => {
        const root = document.documentElement;
        if (theme === 'cyber') {
            root.style.setProperty('--bg-deep', '#0f0c29');
            root.style.setProperty('--glass-bg', 'rgba(30, 30, 45, 0.6)');
            root.style.setProperty('--text-main', '#e2e8f0');
            root.style.setProperty('--accent-blue', '#00d4ff');
        } else if (theme === 'light') {
            root.style.setProperty('--bg-deep', '#f8fafc');
            root.style.setProperty('--glass-bg', 'rgba(255, 255, 255, 0.7)');
            root.style.setProperty('--text-main', '#1e293b');
            root.style.setProperty('--accent-blue', '#2563eb');
        } else if (theme === 'slate') {
            root.style.setProperty('--bg-deep', '#1e293b');
            root.style.setProperty('--glass-bg', 'rgba(51, 65, 85, 0.6)');
            root.style.setProperty('--text-main', '#f1f5f9');
            root.style.setProperty('--accent-blue', '#38bdf8');
        } else if (theme === 'graphite') {
            root.style.setProperty('--bg-deep', '#1a1a1a');
            root.style.setProperty('--glass-bg', 'rgba(40, 40, 40, 0.7)');
            root.style.setProperty('--text-main', '#f0f0f0');
            root.style.setProperty('--accent-blue', '#bdc3c7');
        }
    }, [theme]);

    return (
        <div className="flex h-screen w-full overflow-hidden font-sans text-[var(--text-main)] bg-[var(--bg-deep)] transition-colors duration-500" style={{ background: theme === 'cyber' ? 'linear-gradient(135deg, #050510, #16162a, #101025)' : theme === 'graphite' ? 'linear-gradient(135deg, #1e1e1e, #2d2d2d, #1a1a1a)' : undefined }}>

            {/* SIDEBAR ("Dock") */}
            <nav className="w-16 md:w-20 glass-card border-r border-white/5 flex flex-col items-center py-6 z-20 m-2 rounded-2xl shrink-0">
                <div className="mb-8 w-10 h-10 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl flex items-center justify-center shadow-lg hover:scale-105 transition cursor-pointer group">
                    <i className="fa-solid fa-diamond text-white text-lg group-hover:rotate-180 transition duration-500"></i>
                </div>

                <div className="flex-1 flex flex-col gap-6 w-full px-2">
                    <NavButton icon="fa-layer-group" label="Centrum Dowodzenia" active={currentView === 'dashboard'} onClick={() => setCurrentView('dashboard')} />
                    <NavButton icon="fa-globe" label="Rynek Globalny" active={currentView === 'market'} onClick={() => setCurrentView('market')} notification />
                    <NavButton icon="fa-comments" label="Komunikacja" active={currentView === 'comms'} onClick={() => setCurrentView('comms')} />
                    <NavButton icon="fa-database" label="Baza Wiedzy" active={currentView === 'wiki'} onClick={() => setCurrentView('wiki')} />
                </div>

                <div className="w-full px-2 mt-auto relative">

                    <button
                        onClick={() => setShowSettings(!showSettings)}
                        className={`w-full aspect-square rounded-xl flex items-center justify-center transition ${showSettings ? 'bg-white/10 text-white' : 'hover:bg-white/5 text-gray-500'}`}
                    >
                        <i className={`fa-solid fa-gear text-lg ${showSettings ? 'rotate-90' : ''} transition-transform duration-500`}></i>
                    </button>
                </div>
            </nav>

            {/* SETTINGS POPOVER */}
            {showSettings && (
                <div className="absolute left-24 bottom-6 z-50 bg-black/90 border border-white/10 p-3 rounded-2xl backdrop-blur-xl flex flex-col gap-2 shadow-[0_0_30px_rgba(0,0,0,0.5)] animate-in slide-in-from-left-2">
                    <p className="text-[10px] uppercase font-bold text-gray-500 px-1 mb-1 tracking-widest">Motyw Interfejsu</p>
                    <div className="flex gap-2 mb-3">
                        <ThemeBtn theme="cyber" color="#0f0c29" onClick={() => setTheme('cyber')} active={theme === 'cyber'} />
                        <ThemeBtn theme="slate" color="#1e293b" onClick={() => setTheme('slate')} active={theme === 'slate'} />
                        <ThemeBtn theme="light" color="#f8fafc" onClick={() => setTheme('light')} active={theme === 'light'} />
                        <ThemeBtn theme="graphite" color="#2d2d2d" onClick={() => setTheme('graphite')} active={theme === 'graphite'} />
                    </div>

                    <button
                        onClick={() => router.push('/practice?view=gry')}
                        className="w-full py-2 bg-red-500/20 hover:bg-red-500/30 border border-red-500/30 rounded-lg text-red-200 text-xs font-bold uppercase tracking-widest transition flex items-center justify-center gap-2"
                    >
                        <i className="fa-solid fa-power-off"></i> Zakończ
                    </button>
                </div>
            )}

            {/* MAIN AREA */}
            <div className="flex-1 flex flex-col p-2 h-full gap-2 relative">

                {/* TOP BAR */}
                <header className="glass-card p-3 rounded-xl flex items-center justify-between px-6 shrink-0 z-10">
                    <div className="flex items-center gap-4">
                        <div className="flex flex-col">
                            <h1 className="text-sm font-bold tracking-[0.2em] uppercase leading-none">Dream Team <span className="text-[var(--accent-blue)]">OS</span></h1>
                            <div className="flex items-center gap-2 mt-1">
                                <span className="text-[9px] opacity-60 font-mono tracking-widest">v3.0.4 stable</span>
                                <span className="px-1.5 py-0.5 rounded-full bg-green-500/10 border border-green-500/20 text-[9px] text-green-400 font-mono flex items-center gap-1">
                                    <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></span> ONLINE
                                </span>
                            </div>
                        </div>
                    </div>

                    {/* Game Clock (Center) */}
                    <div className="absolute left-1/2 transform -translate-x-1/2 bg-black/30 px-6 py-1.5 rounded-b-xl border-b border-x border-white/5 backdrop-blur-md shadow-lg -mt-3">
                        <div className="flex items-center gap-3 font-mono text-gray-300 text-xs">
                            <i className="fa-regular fa-clock text-[var(--accent-blue)]"></i>
                            <span className="font-bold text-white">DZIEŃ 14</span>
                            <span className="opacity-50">|</span>
                            <span>10:42 AM</span>
                        </div>
                    </div>

                    {/* Resources */}
                    <div className="flex items-center gap-6 text-xs">
                        <ResourceDisplay label="Płynne Aktywa" value={initialState.resources.coins.toLocaleString()} unit="Coins" />

                        {/* Net Flow Display */}
                        <div className="text-right hidden md:block">
                            <p className="text-[9px] opacity-60 uppercase font-bold tracking-widest mb-0.5">Przepływy</p>
                            <div className="flex items-center justify-end gap-2 font-mono">
                                <span className="text-green-400">+{initialState.resources.cashflow.revenue}</span>
                                <span className="text-[var(--text-muted)]">/</span>
                                <span className="text-red-400">-{initialState.resources.cashflow.burn}</span>
                            </div>
                        </div>

                        <ResourceDisplay label="Reputacja" value={initialState.resources.reputation} icon="fa-medal" color="text-purple-400" />

                        {/* User Profile */}
                        <div className="w-9 h-9 rounded-lg bg-[var(--accent-blue)] text-black font-bold flex items-center justify-center cursor-pointer hover:scale-105 transition shadow-[0_0_15px_rgba(0,212,255,0.3)]">
                            US
                        </div>
                    </div>
                </header>

                {/* CONTENT VIEW SWITCHER */}
                <main className="flex-1 overflow-hidden relative">
                    {/* We will inject the specific view here mostly, 
                    but for now sticking to children if the page uses composition, 
                    OR efficiently we can render content here directly.
                    For this V3 port, I'll pass currentView into a context or prop
                    so the parent Page can render the right component.
                */}
                    {/* 
                   Wait, this is a Layout component. Layouts usually wrap children.
                   But if I want this component to control the View State, it might be better
                   called `ConsultingGameContainer` and handle the switching internally.
                   I will assume the `children` prop here isn't the best approach if *this* 
                   component manages the `currentView` state.
                   Instead, I should import the Views here.
                */}
                    {renderView(currentView, initialState, setCurrentView, { onAccept: acceptContractAction, onRefresh: refreshGlobalMarketAction })}
                </main>
            </div>

        </div>
    );
}

// Update renderView signature
function renderView(view: ViewType, state: ConsultingGameState, setView: (v: ViewType) => void, actions?: any) {
    switch (view) {
        case 'dashboard': return <DashboardView gameState={state} onViewChange={setView} />;
        case 'market': return <ContractsView contracts={state.market_contracts || []} onAccept={actions?.onAccept} onRefresh={actions?.onRefresh} />;
        case 'comms': return <NegotiationView />;
        case 'wiki': return <ResearchView />;
        case 'team': return <TeamView employees={state.employees} />;
        case 'office': return <OfficeView office={state.departments.office} />;
        default: return null;
    }
}

function NavButton({ icon, label, active, onClick, notification }: any) {
    return (
        <button
            onClick={onClick}
            className={`w-full aspect-square rounded-xl flex items-center justify-center transition group relative border ${active ? 'bg-white/10 text-white shadow-inner border-white/20' : 'bg-white/5 hover:bg-white/10 text-gray-400 border-white/5 hover:border-white/10'}`}
        >
            <i className={`fa-solid ${icon} text-xl ${active ? 'text-[var(--accent-blue)]' : ''}`}></i>
            {notification && <span className="absolute top-2 right-3 w-2 h-2 bg-red-500 rounded-full animate-pulse border border-black"></span>}
        </button>
    );
}

function ResourceDisplay({ label, value, unit, icon, color }: any) {
    return (
        <div className="text-right">
            <p className="text-[9px] opacity-60 uppercase font-bold tracking-widest mb-0.5">{label}</p>
            <div className={`flex items-center justify-end gap-1.5 ${color || 'text-yellow-400'}`}>
                <span className="text-lg font-bold font-mono">{value}</span>
                {unit && <span className="text-[10px] opacity-60">{unit}</span>}
                {icon && <i className={`fa-solid ${icon} text-sm`}></i>}
            </div>
        </div>
    );
}

function ThemeBtn({ theme, color, onClick, active }: any) {
    return (
        <button
            onClick={onClick}
            className={`w-8 h-8 rounded-full border-2 transition ${active ? 'border-white scale-110' : 'border-white/20 hover:scale-105'}`}
            style={{ backgroundColor: color }}
            title={theme}
        ></button>
    )
}
