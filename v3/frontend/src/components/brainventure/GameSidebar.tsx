"use client"

import React from 'react'
import { LayoutDashboard, Users, BookOpen, Briefcase, History, BarChart2 } from 'lucide-react'

type ViewType = 'GAME' | 'WIKI' | 'TEAM' | 'CONTRACTS' | 'HISTORY' | 'STATS' | 'SETTINGS'

interface GameSidebarProps {
    currentView: ViewType
    onViewChange: (view: ViewType) => void
}

export default function GameSidebar({ currentView, onViewChange }: GameSidebarProps) {
    return (
        <nav className="w-20 bg-gray-900 border-r border-gray-800 flex flex-col items-center py-6 z-20 shrink-0">
            {/* Logo / Brand Icon */}
            <div className="mb-8 w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg hover:scale-105 transition cursor-pointer group"
                onClick={() => onViewChange('GAME')}>
                <span className="text-2xl">🧠</span>
            </div>

            <div className="flex flex-col gap-6 w-full px-2">
                <NavButton
                    icon={<LayoutDashboard size={24} />}
                    label="Gra"
                    active={currentView === 'GAME'}
                    onClick={() => onViewChange('GAME')}
                />
                <NavButton
                    icon={<Users size={24} />}
                    label="Zespół"
                    active={currentView === 'TEAM'}
                    onClick={() => onViewChange('TEAM')}
                />
                <NavButton
                    icon={<BookOpen size={24} />}
                    label="Wiedza"
                    active={currentView === 'WIKI'}
                    onClick={() => onViewChange('WIKI')}
                />
                <NavButton
                    icon={<Briefcase size={24} />}
                    label="Kontrakty"
                    active={currentView === 'CONTRACTS'}
                    onClick={() => onViewChange('CONTRACTS')}
                />
                <NavButton
                    icon={<BarChart2 size={24} />}
                    label="Zestawienia"
                    active={currentView === 'STATS'}
                    onClick={() => onViewChange('STATS')}
                />
            </div>
        </nav>
    )
}

function NavButton({ icon, label, active, onClick }: { icon: React.ReactNode, label: string, active: boolean, onClick: () => void }) {
    return (
        <button
            onClick={onClick}
            title={label}
            className={`w-full aspect-square rounded-xl flex flex-col items-center justify-center gap-1 transition group relative border ${active ? 'bg-blue-600/20 text-blue-400 border-blue-500/50 shadow-[0_0_15px_rgba(59,130,246,0.3)]' : 'bg-gray-800/50 hover:bg-gray-800 text-gray-500 hover:text-gray-300 border-transparent hover:border-gray-700'}`}
        >
            {icon}
            <span className="text-[9px] font-bold uppercase tracking-wider opacity-70 group-hover:opacity-100">{label}</span>
        </button>
    )
}
