'use client'

import React from 'react'
import CardRenderer from '@/components/lesson/CardRenderer'

export default function LivePreview({ card }: { card: any }) {
    if (!card) return <div className="text-center text-gray-500 mt-20">No card selected</div>

    // Wrap in a mock container to simulate active lesson view
    return (
        <div className="transform scale-90 origin-top">
            <CardRenderer
                card={card}
                onAnswer={() => { }}
                onTestResult={() => { }}
                onReset={() => { }}
            />
        </div>
    )
}
