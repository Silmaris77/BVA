'use client'

import { useRouter } from 'next/navigation'

export default function LessonEditorLayout({ children }: { children: React.ReactNode }) {
    const router = useRouter()

    return (
        <div className="fixed inset-0 z-[9999] flex h-screen w-full bg-[#0a0a0f] text-white overflow-hidden font-sans">
            <button
                onClick={() => router.push('/practice')}
                className="absolute top-4 right-4 z-50 bg-[#1a1a24] hover:bg-black border border-white/10 text-white/50 hover:text-white px-3 py-1 text-xs rounded-full transition-colors"
            >
                ✕ Exit Editor
            </button>
            {children}
        </div>
    )
}
