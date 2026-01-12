'use client'

import { Home, BookOpen, Gamepad2, User } from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function BottomNav() {
    const pathname = usePathname()

    const navItems = [
        { name: 'Hub', icon: Home, path: '/' },
        { name: 'Nauka', icon: BookOpen, path: '/lessons' },
        { name: 'Praktyka', icon: Gamepad2, path: '/practice' },
        { name: 'Ja', icon: User, path: '/profile' },
    ]

    const isActive = (path: string) => {
        if (path === '/') return pathname === '/'
        return pathname.startsWith(path)
    }

    return (
        <nav
            className="md:hidden fixed bottom-0 left-0 right-0 z-50"
            style={{
                background: 'rgba(20, 20, 35, 0.8)',
                backdropFilter: 'blur(20px)',
                borderTop: '1px solid rgba(255, 255, 255, 0.1)',
            }}
        >
            <div className="flex items-center justify-around h-20 px-2">
                {navItems.map((item) => {
                    const Icon = item.icon
                    const active = isActive(item.path)

                    return (
                        <Link
                            key={item.path}
                            href={item.path}
                            className="flex flex-col items-center justify-center flex-1 h-full relative group"
                        >
                            {/* Active indicator */}
                            {active && (
                                <div
                                    className="absolute top-0 left-1/2 -translate-x-1/2 h-1 w-12 rounded-full"
                                    style={{
                                        background: 'linear-gradient(90deg, #b000ff, #00d4ff)',
                                        boxShadow: '0 0 20px rgba(176, 0, 255, 0.6)',
                                    }}
                                />
                            )}

                            {/* Icon */}
                            <Icon
                                size={24}
                                style={{
                                    color: active ? '#00d4ff' : 'rgba(255, 255, 255, 0.5)',
                                    transition: 'all 0.3s ease',
                                }}
                                className={`mb-1 ${!active && 'group-hover:text-white'}`}
                            />

                            {/* Label */}
                            <span
                                style={{
                                    fontSize: '11px',
                                    color: active ? '#00d4ff' : 'rgba(255, 255, 255, 0.5)',
                                    fontWeight: active ? 600 : 400,
                                    transition: 'all 0.3s ease',
                                }}
                                className={!active ? 'group-hover:text-white' : ''}
                            >
                                {item.name}
                            </span>
                        </Link>
                    )
                })}
            </div>
        </nav>
    )
}
