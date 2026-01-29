"use client"

import React, { useState } from 'react'
import { useBrainVenture } from '../../../components/brainventure/BrainVentureContext'
import { motion, AnimatePresence } from 'framer-motion'
import { TrendingUp, DollarSign, Gem, Clock, BarChart2 } from 'lucide-react'

import EventPhase from '../../../components/brainventure/EventPhase'
import PillPhase from '../../../components/brainventure/PillPhase'
import TaskPhase from '../../../components/brainventure/TaskPhase'
import DevelopmentPhase from '../../../components/brainventure/DevelopmentPhase'
import ContractPhase from '../../../components/brainventure/ContractPhase'
import SummaryPhase from '../../../components/brainventure/SummaryPhase'
import GameSidebar from '../../../components/brainventure/GameSidebar'
import GameContextPanel from '../../../components/brainventure/GameContextPanel'
import GlobalFloatingMoney from '../../../components/brainventure/GlobalFloatingMoney'
import GlobalFloatingKW from '../../../components/brainventure/GlobalFloatingKW'

// Placeholder Views (To be extracted)
import PILLS_DATA from '../../../data/brainventure/pills.json'
import { KnowledgePill } from '../../../types/brainventure'
import ReactMarkdown from 'react-markdown'

const WikiView = ({ unlockedPillIds }: { unlockedPillIds: string[] }) => {
    const unlockedPills = PILLS_DATA.filter(p => unlockedPillIds.includes(p.id)) as unknown as KnowledgePill[]

    return (
        <div className="p-8 text-center text-gray-400">
            <h2 className="text-2xl font-bold text-white mb-4">Baza Wiedzy (Wiki)</h2>
            <p>Tutaj znajdziesz wszystkie odblokowane Pigułki Wiedzy.</p>

            {unlockedPills.length > 0 ? (
                <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-8 text-left max-w-7xl mx-auto">
                    {unlockedPills.map(pill => (
                        <div key={pill.id} className="bg-gray-800 p-8 rounded-2xl border border-gray-700 hover:border-purple-500/50 transition-colors shadow-2xl flex flex-col h-96">
                            <h4 className="font-bold text-2xl text-purple-300 mb-4 truncate" title={pill.title}>{pill.title}</h4>
                            <div className="flex-1 overflow-y-auto custom-scrollbar text-base text-gray-300 prose prose-invert prose-lg max-w-none leading-relaxed">
                                <ReactMarkdown>{pill.content}</ReactMarkdown>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="mt-12 flex flex-col items-center justify-center opacity-30">
                    <Gem size={64} className="mb-4" />
                    <p className="text-lg">Twoja baza wiedzy jest pusta.</p>
                    <p className="text-sm">Kupuj Pigułki Wiedzy w Fazie 2, aby je tutaj gromadzić.</p>
                </div>
            )}
        </div>
    )
}

const TeamView = ({ team }: { team: any[] }) => (
    <div className="p-8 max-w-4xl mx-auto">
        <h2 className="text-3xl font-bold text-white mb-8">Zarządzanie Zespołem</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {team.map((char) => (
                <div key={char.id} className="bg-gray-800 rounded-xl p-6 border border-gray-700 shadow-xl relative overflow-hidden group hover:border-blue-500/50 transition-colors">
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                        <UsersIcon size={120} />
                    </div>

                    <div className="relative z-10">
                        <div className="flex justify-between items-start mb-6">
                            <div>
                                <h3 className={`text-xl font-bold ${char.role === 'MANAGER' ? 'text-yellow-400' : 'text-blue-300'}`}>
                                    {char.name}
                                </h3>
                                <span className="text-xs text-gray-500 uppercase tracking-widest font-bold">{char.role}</span>
                            </div>
                            <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center font-bold text-gray-400">
                                {char.name.charAt(0)}
                            </div>
                        </div>

                        <div className="space-y-6">
                            <div>
                                <div className="flex justify-between text-sm mb-2">
                                    <span className="text-gray-400 flex items-center gap-2"><Clock size={16} /> Dostępność (PD)</span>
                                    <span className="text-white font-mono font-bold">{char.availability}/{char.maxAvailability}</span>
                                </div>
                                <div className="h-3 bg-gray-900 rounded-full overflow-hidden border border-gray-700">
                                    <div
                                        className="h-full bg-blue-500 rounded-full transition-all duration-500"
                                        style={{ width: `${(char.availability / char.maxAvailability) * 100}%` }}
                                    ></div>
                                </div>
                            </div>

                            <div>
                                <div className="flex justify-between text-sm mb-2">
                                    <span className="text-gray-400 flex items-center gap-2"><TrendingUp size={16} /> Efektywność (PE)</span>
                                    <span className="text-green-400 font-mono font-bold text-lg">{char.efficiency}</span>
                                </div>
                                <div className="flex gap-1">
                                    {Array.from({ length: 15 }).map((_, i) => (
                                        <div key={i} className={`h-2 flex-1 rounded-sm ${i < char.efficiency ? 'bg-green-500' : 'bg-gray-700'}`} />
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    </div>
)

const ContractsView = ({ activeContracts, completedContracts }: { activeContracts: any[], completedContracts: any[] }) => (
    <div className="p-8">
        <h2 className="text-2xl font-bold text-white mb-8">Rejestr Kontraktów</h2>

        {/* Active Contracts */}
        <div className="mb-8">
            <h3 className="text-xl font-bold text-blue-300 mb-4 border-b border-gray-700 pb-2">W Realizacji / Aktywne</h3>
            <div className="overflow-x-auto bg-gray-900/50 rounded-xl border border-gray-700">
                <table className="w-full text-left text-sm text-gray-400">
                    <thead className="bg-gray-800 text-gray-200 uppercase font-bold text-xs">
                        <tr>
                            <th className="p-4">Nazwa</th>
                            <th className="p-4">Wartość</th>
                            <th className="p-4">Postęp</th>
                        </tr>
                    </thead>
                    <tbody>
                        {activeContracts.map(c => (
                            <tr key={c.id} className="border-b border-gray-700 hover:bg-gray-800/50">
                                <td className="p-4 font-bold text-white">{c.title}</td>
                                <td className="p-4 text-green-400">{c.value} PLN</td>
                                <td className="p-4">
                                    <div className="w-32 h-2 bg-gray-700 rounded-full overflow-hidden">
                                        <div className="h-full bg-blue-500" style={{ width: `${(c.currentProductivity / c.requiredProductivity) * 100}%` }}></div>
                                    </div>
                                    <div className="text-[10px] mt-1">{c.currentProductivity} / {c.requiredProductivity} W</div>
                                </td>
                            </tr>
                        ))}
                        {activeContracts.length === 0 && (
                            <tr>
                                <td colSpan={3} className="p-8 text-center italic opacity-50">Brak aktywnych kontraktów</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>

        {/* Completed Contracts */}
        <div>
            <h3 className="text-xl font-bold text-green-400 mb-4 border-b border-gray-700 pb-2">Ukończone (Archiwum)</h3>
            <div className="overflow-x-auto bg-gray-900/50 rounded-xl border border-gray-700">
                <table className="w-full text-left text-sm text-gray-400">
                    <thead className="bg-gray-800 text-gray-200 uppercase font-bold text-xs">
                        <tr>
                            <th className="p-4">Nazwa</th>
                            <th className="p-4">Wartość</th>
                            <th className="p-4">Zakończono</th>
                        </tr>
                    </thead>
                    <tbody>
                        {completedContracts.map((c: any) => (
                            <tr key={c.id + c.completedRound} className="border-b border-gray-700 hover:bg-gray-800/50">
                                <td className="p-4 font-bold text-gray-300">{c.title}</td>
                                <td className="p-4 text-green-400 font-mono">+{c.value} PLN</td>
                                <td className="p-4 text-gray-500">Runda {c.completedRound || '?'}</td>
                            </tr>
                        ))}
                        {completedContracts.length === 0 && (
                            <tr>
                                <td colSpan={3} className="p-8 text-center italic opacity-50">Brak ukończonych kontraktów</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
)

// ... imports
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts'

const StatsView = ({ history }: { history: any }) => {
    const stats: any[] = history.roundStats || []

    return (
        <div className="p-8 max-w-6xl mx-auto h-full overflow-y-auto custom-scrollbar">
            <h2 className="text-3xl font-bold text-white mb-8 flex items-center gap-2"><TrendingUp /> Zestawienia i Raporty</h2>

            {stats.length === 0 ? (
                <div className="text-center text-gray-500 py-20 flex flex-col items-center">
                    <BarChart2 size={64} className="mb-4 opacity-30" />
                    <p>Brak danych. Ukończ co najmniej jedną rundę, aby zobaczyć statystyki.</p>
                </div>
            ) : (
                <div className="flex flex-col gap-12">
                    {/* Charts Section */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        {/* Cash Flow Chart */}
                        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-xl">
                            <h3 className="text-lg font-bold text-gray-300 mb-4">Dynamika Finansowa (PLN)</h3>
                            <div className="h-64 cursor-default">
                                <ResponsiveContainer width="100%" height="100%">
                                    <LineChart data={stats}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                        <XAxis dataKey="round" stroke="#9CA3AF" label={{ value: 'Runda', position: 'insideBottomRight', offset: -5 }} />
                                        <YAxis stroke="#9CA3AF" />
                                        <Tooltip
                                            contentStyle={{ backgroundColor: '#1F2937', borderColor: '#374151', color: '#F3F4F6' }}
                                            formatter={(value: any) => [`${value} PLN`, '']}
                                        />
                                        <Legend />
                                        <Line type="monotone" dataKey="cashEnd" name="Stan Konta" stroke="#10B981" strokeWidth={2} dot={{ r: 4 }} />
                                        <Line type="monotone" dataKey="balance" name="Balans Rundy" stroke="#3B82F6" strokeWidth={2} strokeDasharray="5 5" />
                                    </LineChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        {/* Efficiency Chart */}
                        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-xl">
                            <h3 className="text-lg font-bold text-gray-300 mb-4">Efektywność Zespołu (PE)</h3>
                            <div className="h-64 cursor-default">
                                <ResponsiveContainer width="100%" height="100%">
                                    <BarChart data={stats}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                        <XAxis dataKey="round" stroke="#9CA3AF" />
                                        <YAxis stroke="#9CA3AF" />
                                        <Tooltip contentStyle={{ backgroundColor: '#1F2937', borderColor: '#374151', color: '#F3F4F6' }} />
                                        <Legend />
                                        <Bar dataKey="teamEfficiency" name="Suma Efektywności" fill="#8B5CF6" radius={[4, 4, 0, 0]} />
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </div>

                    {/* Data Table */}
                    <div className="bg-gray-800 rounded-xl border border-gray-700 shadow-xl overflow-hidden">
                        <div className="p-4 border-b border-gray-700 bg-gray-900/50">
                            <h3 className="font-bold text-white">Szczegółowy Raport Finansowy</h3>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-gray-900 text-gray-400 uppercase font-bold text-xs">
                                    <tr>
                                        <th className="p-4">Runda</th>
                                        <th className="p-4 text-green-400">Przychody</th>
                                        <th className="p-4 text-red-400">Koszty</th>
                                        <th className="p-4 text-blue-300">Balans</th>
                                        <th className="p-4">Stan Konta (Koniec)</th>
                                        <th className="p-4 text-purple-400">Efektywność</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-700">
                                    {stats.map((row: any) => (
                                        <tr key={row.round} className="hover:bg-gray-700/50 transition-colors">
                                            <td className="p-4 font-bold text-white">Runda {row.round}</td>
                                            <td className="p-4 text-green-400">+{row.income} PLN</td>
                                            <td className="p-4 text-red-400">-{row.expenses} PLN</td>
                                            <td className={`p-4 font-bold ${row.balance >= 0 ? 'text-blue-300' : 'text-orange-400'}`}>
                                                {row.balance > 0 ? '+' : ''}{row.balance} PLN
                                            </td>
                                            <td className="p-4 text-gray-200">{row.cashEnd} PLN</td>
                                            <td className="p-4 text-purple-300 font-mono">{row.teamEfficiency} PE</td>
                                        </tr>
                                    ))}
                                    {/* Cumulative Row (Optional/Simplified) */}
                                    <tr className="bg-gray-900/30 font-bold border-t-2 border-gray-600">
                                        <td className="p-4 text-white">SUMA</td>
                                        <td className="p-4 text-green-400">
                                            +{stats.reduce((acc: number, curr: any) => acc + curr.income, 0)} PLN
                                        </td>
                                        <td className="p-4 text-red-400">
                                            -{stats.reduce((acc: number, curr: any) => acc + curr.expenses, 0)} PLN
                                        </td>
                                        <td className="p-4 text-blue-300">
                                            {stats.reduce((acc: number, curr: any) => acc + curr.balance, 0)} PLN
                                        </td>
                                        <td className="p-4">-</td>
                                        <td className="p-4">-</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

// Helper Icon
const UsersIcon = ({ size }: { size: number }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M22 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /></svg>
)

const PHASE_LABELS: Record<string, string> = {
    'EVENT': '1. Zdarzenia',
    'PILL': '2. Pigułki Wiedzy',
    'TASK': '3. Zadania',
    'DEVELOPMENT': '4. Rozwój Zespołu',
    'CONTRACT': '5. Kontrakty',
    'SUMMARY': 'Podsumowanie'
}

type ViewType = 'GAME' | 'WIKI' | 'TEAM' | 'CONTRACTS' | 'HISTORY' | 'STATS' | 'SETTINGS'

export default function GamePage() {
    const { state, dispatch, formatMoney, getTeamProductivity } = useBrainVenture()
    const [currentView, setCurrentView] = useState<ViewType>('GAME')
    // ... (rest of render logic, adding STATS to switch)


    const productivity = getTeamProductivity()

    return (
        <div className="flex h-screen w-full bg-[var(--bg-deep)] text-white font-sans overflow-hidden">
            <GlobalFloatingMoney />
            <GlobalFloatingKW />

            {/* Sidebar */}
            <GameSidebar currentView={currentView} onViewChange={setCurrentView} />

            {/* Main Content Area */}
            <div className="flex-1 flex flex-col min-w-0">

                {/* Top HUD */}
                <header className="bg-gray-900/50 border-b border-gray-700/50 p-4 flex justify-between items-center z-10 backdrop-blur-md">
                    <div className="flex gap-4 items-center">
                        <div className="flex flex-col pl-2">
                            <span className="text-[10px] uppercase font-bold text-gray-500 tracking-widest leading-none mb-1">Runda</span>
                            <span className="text-xl font-bold text-white leading-none">{state.round} / 8</span>
                        </div>
                        <div className="h-8 w-px bg-gray-700 mx-2"></div>
                        <div className="flex flex-col">
                            <span className="text-[10px] uppercase font-bold text-gray-500 tracking-widest leading-none mb-1">Aktualna Faza</span>
                            <span className="text-lg font-bold text-blue-300 leading-none">{PHASE_LABELS[state.phase]}</span>
                        </div>
                    </div>

                    <div className="flex gap-8 items-center">
                        <button
                            onClick={() => dispatch({ type: 'NEXT_PHASE' })}
                            disabled={!state.isPhaseReady}
                            className={`px-6 py-2 rounded-lg font-bold uppercase tracking-wider text-sm transition-all shadow-lg flex items-center gap-2 ${state.isPhaseReady
                                ? 'bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white shadow-green-900/40 hover:scale-105 active:scale-95'
                                : 'bg-gray-800 text-gray-600 cursor-not-allowed border border-gray-700'
                                }`}
                        >
                            {state.phase === 'SUMMARY' ? 'Nowa Runda' : 'Dalej'}
                            <div className={`w-2 h-2 rounded-full ${state.isPhaseReady ? 'bg-white animate-pulse' : 'bg-gray-500'}`} />
                        </button>

                        <div className="h-8 w-px bg-gray-700 mx-2"></div>

                        <div className="flex gap-6">
                            <div className="flex flex-col items-end">
                                <span className="text-[10px] uppercase font-bold text-gray-500 tracking-widest leading-none mb-1">Budżet</span>
                                <div className="flex items-center gap-2 text-green-400 font-mono font-bold text-xl leading-none">
                                    <DollarSign size={16} /> {formatMoney(state.cash)}
                                </div>
                            </div>

                            <div className="flex flex-col items-end">
                                <span className="text-[10px] uppercase font-bold text-gray-500 tracking-widest leading-none mb-1">Wiedza (KW)</span>
                                <div className="flex items-center gap-2 text-blue-400 font-mono font-bold text-xl leading-none">
                                    <Gem size={16} /> {state.knowledgeCrystals}
                                </div>
                            </div>

                            <div className="flex flex-col items-end">
                                <span className="text-[10px] uppercase font-bold text-gray-500 tracking-widest leading-none mb-1">Moc Zespołu (W)</span>
                                <div className="flex items-center gap-2 text-blue-400 font-mono font-bold text-xl leading-none">
                                    <TrendingUp size={16} /> {productivity}
                                </div>
                            </div>
                        </div>
                    </div>
                </header>

                {/* Content View Switcher */}
                <main className="flex-1 relative overflow-y-auto bg-gradient-to-br from-gray-900 via-[#0f172a] to-gray-900">
                    <AnimatePresence mode="wait">
                        {currentView === 'GAME' ? (
                            <motion.div
                                key={state.phase}
                                initial={{ opacity: 0, scale: 0.98 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 1.02 }}
                                transition={{ duration: 0.3 }}
                                className="h-full flex flex-row overflow-hidden"
                            >
                                {/* LEFT PANEL: Persistent Context */}
                                <GameContextPanel />

                                {/* RIGHT PANEL: Main Game Phase */}
                                <div className="flex-1 overflow-y-auto custom-scrollbar p-6 relative bg-gradient-to-br from-gray-900 via-[#0f172a] to-gray-900">
                                    {/* Grid Background Effect */}
                                    <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-[0.03] pointer-events-none"></div>

                                    <div className="max-w-5xl mx-auto h-full flex flex-col">
                                        {state.phase === 'EVENT' && <EventPhase />}
                                        {state.phase === 'PILL' && <PillPhase />}
                                        {state.phase === 'TASK' && <TaskPhase />}
                                        {state.phase === 'DEVELOPMENT' && <DevelopmentPhase />}
                                        {state.phase === 'CONTRACT' && <ContractPhase />}
                                        {state.phase === 'SUMMARY' && <SummaryPhase />}
                                    </div>
                                </div>
                            </motion.div>
                        ) : (
                            <motion.div
                                key={currentView}
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                transition={{ duration: 0.2 }}
                                className="h-full"
                            >
                                {currentView === 'WIKI' && <WikiView unlockedPillIds={state.history.pills} />}
                                {currentView === 'TEAM' && <TeamView team={state.team} />}
                                {currentView === 'CONTRACTS' && <ContractsView activeContracts={state.activeContracts} completedContracts={state.history.completedContracts} />}
                                {currentView === 'STATS' && <StatsView history={state.history} />}
                            </motion.div>
                        )}
                    </AnimatePresence>
                </main>
            </div>


        </div>
    )
}
