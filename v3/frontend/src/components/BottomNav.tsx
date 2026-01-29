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
                {navItems.map((item) => {
                    const Icon = item.icon
                    const active = isActive(item.path)

                    return (
                        <Link
                            key={item.path}
                            href={item.path}
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
