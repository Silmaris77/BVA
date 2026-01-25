import React from 'react';

export default function ResearchView() {
    return (
        <div className="h-full flex flex-col p-4 overflow-hidden">
            <div className="flex justify-between items-end mb-6">
                <div>
                    <h2 className="text-2xl font-bold text-white uppercase tracking-wider flex items-center gap-3">
                        <i className="fa-solid fa-microchip text-[var(--accent-blue)]"></i>
                        R&D Intelligence
                    </h2>
                    <p className="text-sm text-gray-400">Develop methodologies to increase contract value and efficiency.</p>
                </div>
                <div className="text-right">
                    <p className="text-[10px] text-gray-500 uppercase tracking-widest mb-1">Research Capacity</p>
                    <div className="flex gap-1">
                        <span className="w-2 h-2 rounded-full bg-[var(--accent-blue)] shadow-[0_0_8px_#00d4ff]"></span>
                        <span className="w-2 h-2 rounded-full bg-[var(--accent-blue)] shadow-[0_0_8px_#00d4ff]"></span>
                        <span className="w-2 h-2 rounded-full bg-gray-700"></span>
                    </div>
                </div>
            </div>

            {/* Research Tree Grid */}
            <div className="flex-1 overflow-y-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 relative">
                {/* Connection Lines (Visual Mockup) */}
                <div className="absolute top-1/2 left-0 w-full h-1 bg-white/5 -z-10 hidden md:block"></div>

                {/* Node 1: Unlocked */}
                <ResearchNode
                    title="SWOT Framework v1.0"
                    category="Strategy"
                    status="unlocked"
                    description="Basic analysis tool. Increases Strategy Pay +5%."
                    cost="0"
                    time="0"
                />

                {/* Node 2: In Progress */}
                <ResearchNode
                    title="SWOT Framework v2.0"
                    category="Strategy"
                    status="progress"
                    description="Advanced insights. Increases Strategy Pay +15%."
                    progress={45}
                    cost="500"
                    time="60m"
                />

                {/* Node 3: Locked */}
                <ResearchNode
                    title="Agile Transformation"
                    category="IT / Ops"
                    status="locked"
                    description="Reduces project duration by 20%."
                    cost="1,200"
                    time="4h"
                />


                <ResearchNode
                    title="AI Market Analysis"
                    category="Big Data"
                    status="locked"
                    description="Auto-detects high value auctions."
                    cost="2,500"
                    time="12h"
                />
            </div>
        </div>
    );
}

function ResearchNode({ title, category, status, description, progress, cost, time }: any) {
    const isUnlocked = status === 'unlocked';
    const isProgress = status === 'progress';
    const isLocked = status === 'locked';

    return (
        <div className={`glass-card p-6 rounded-2xl border relative flex flex-col gap-4 group transition duration-300 ${isUnlocked ? 'border-[var(--accent-blue)]/50 bg-blue-900/10' :
                isProgress ? 'border-[var(--accent-blue)]/30' :
                    'border-white/5 opacity-60 hover:opacity-100 hover:border-white/20'
            }`}>
            {/* Status Indicator */}
            <div className="flex justify-between items-start">
                <span className="text-[10px] font-mono uppercase tracking-widest text-gray-500">{category}</span>
                {isUnlocked && <i className="fa-solid fa-check text-[var(--accent-green)]"></i>}
                {isLocked && <i className="fa-solid fa-lock text-gray-500"></i>}
                {isProgress && <span className="text-[10px] text-[var(--accent-blue)] animate-pulse">Researching...</span>}
            </div>

            <div className="flex-1">
                <h3 className={`text-xl font-bold mb-2 ${isUnlocked ? 'text-[var(--accent-blue)]' : 'text-white'}`}>{title}</h3>
                <p className="text-xs text-gray-400 leading-relaxed">{description}</p>
            </div>

            {isProgress ? (
                <div className="w-full bg-gray-700 h-1.5 rounded-full overflow-hidden mt-2">
                    <div className="bg-[var(--accent-blue)] h-full shadow-[0_0_10px_#00d4ff]" style={{ width: `${progress}%` }}></div>
                </div>
            ) : (
                <div className="pt-4 border-t border-white/10 flex justify-between items-center mt-2">
                    {isUnlocked ? (
                        <span className="text-xs text-gray-500 font-mono">INSTALLED</span>
                    ) : (
                        <>
                            <div className="text-xs font-mono text-gray-300 flex gap-3">
                                <span className={cost === '0' ? 'text-gray-600' : ''}><i className="fa-solid fa-coins mr-1 text-[var(--accent-gold)]"></i>{cost}</span>
                                <span><i className="fa-regular fa-clock mr-1"></i>{time}</span>
                            </div>
                            <button className="bg-white/10 hover:bg-[var(--accent-blue)] hover:text-black transition px-3 py-1 rounded text-[10px] uppercase font-bold tracking-wider">
                                Start
                            </button>
                        </>
                    )}
                </div>
            )}
        </div>
    )
}
