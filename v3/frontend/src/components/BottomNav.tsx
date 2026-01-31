'use client'

import { Home, BookOpen, Gamepad2, User, Bot } from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useAIConversation } from '@/contexts/AIConversationContext'

export default function BottomNav() {
    const pathname = usePathname()
    const { startConversation, state } = useAIConversation()

    const navItems = [
        { name: 'Hub', icon: Home, path: '/' },
        { name: 'Nauka', icon: BookOpen, path: '/lessons' },
        { name: 'AI', icon: Bot, path: null, isAI: true }, // Środkowy przycisk AI
        { name: 'Praktyka', icon: Gamepad2, path: '/practice' },
        { name: 'Ja', icon: User, path: '/profile' },
    ]

    const isActive = (path: string | null) => {
        if (!path) return false
        if (path === '/') return pathname === '/'
        return pathname.startsWith(path)
    }

    const handleAIClick = () => {
        if (!state.isOpen) {
            startConversation('mentor', "Cześć! Jestem Twoim wirtualnym mentorem. W czym mogę pomóc?")
        }
    }

    return (
        <nav
            className="nav-bottom fixed bottom-0 left-0 right-0 z-[9999] w-full"
        >
            <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-evenly',
                width: '100%',
                height: '80px',
                padding: '0 16px',
                boxSizing: 'border-box'
            }}>
                {navItems.map((item, index) => {
                    const Icon = item.icon
                    const active = item.isAI ? state.isOpen : isActive(item.path)

                    // Specjalny przycisk AI
                    if (item.isAI) {
                        return (
                            <button
                                key="ai-button"
                                onClick={handleAIClick}
                                className={`nav-bottom-item nav-bottom-ai ${active ? 'active' : ''}`}
                                style={{
                                    background: active 
                                        ? 'linear-gradient(135deg, #00d4ff, #00a0cc)' 
                                        : 'linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(0, 160, 204, 0.2))',
                                    border: '2px solid rgba(0, 212, 255, 0.5)',
                                    borderRadius: '50%',
                                    width: '56px',
                                    height: '56px',
                                    marginTop: '-20px',
                                    boxShadow: active 
                                        ? '0 0 20px rgba(0, 212, 255, 0.5)' 
                                        : '0 4px 15px rgba(0, 0, 0, 0.3)'
                                }}
                            >
                                <Icon size={28} color={active ? '#000' : '#00d4ff'} />
                            </button>
                        )
                    }

                    return (
                        <Link
                            key={item.path}
                            href={item.path!}
                            className={`nav-bottom-item ${active ? 'active' : ''}`}
                        >
                            {/* Active indicator */}
                            {active && <div className="nav-bottom-indicator" />}

                            {/* Icon */}
                            <Icon size={24} className="nav-icon" />

                            {/* Label */}
                            <span className="nav-label">{item.name}</span>
                        </Link>
                    )
                })}
            </div>
        </nav>
    )
}
