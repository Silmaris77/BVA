"use client"

import React from 'react'
import Link from 'next/link'
import { Brain, Play } from 'lucide-react'

export default function BrainVenturePage() {
    return (
        <div className="container mx-auto px-4 py-8 flex flex-col items-center justify-center min-h-[80vh]">
            <div className="text-center max-w-2xl">
                <div className="flex justify-center mb-6">
                    <div className="w-20 h-20 bg-blue-600/20 rounded-full flex items-center justify-center border border-blue-500/50 shadow-[0_0_30px_rgba(30,115,185,0.4)]">
                        <Brain size={40} className="text-blue-400" />
                    </div>
                </div>

                <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
                    BrainVenture
                </h1>

                <p className="text-xl text-blue-100/70 mb-8 leading-relaxed">
                    Wciel się w rolę lidera, który rozumie, jak działa mózg.
                    Balansuj miedzy wynikami finansowymi a dobrostanem zespołu.
                    Wykorzystaj neurobiologię w biznesie.
                </p>

                <div className="flex gap-4 justify-center">
                    <Link href="/brainventure/game"
                        className="group relative px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg font-bold text-lg shadow-lg hover:shadow-blue-500/40 transition-all hover:-translate-y-1 overflow-hidden"
                    >
                        <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                        <span className="relative flex items-center gap-2">
                            <Play size={20} fill="currentColor" /> Rozpocznij Symulację
                        </span>
                    </Link>
                </div>
            </div>
        </div>
    )
}
