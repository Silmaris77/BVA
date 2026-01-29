"use client"

import React from 'react'
import { BrainVentureProvider } from '../../components/brainventure/BrainVentureContext'

export default function BrainVentureLayout({ children }: { children: React.ReactNode }) {
    return (
        <BrainVentureProvider>
            <div className="brainventure-theme min-h-screen bg-[var(--bg-deep)] text-white font-[Outfit]">
                {/* Background ambient effects could go here */}
                <div className="fixed inset-0 pointer-events-none opacity-20 bg-[url('/grid-pattern.png')]"></div>
                {children}
            </div>
        </BrainVentureProvider>
    )
}
