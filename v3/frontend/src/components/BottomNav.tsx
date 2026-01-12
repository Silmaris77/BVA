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
            className="nav-bottom"
            style={{
                position: 'fixed',
                bottom: 0,
                left: 0,
                right: 0,
                width: '100%',
                zIndex: 9999,
                background: 'rgba(20, 20, 35, 0.95)',
                backdropFilter: 'blur(20px)',
                borderTop: '1px solid rgba(255, 255, 255, 0.1)',
            }}
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
                            style={{
                                display: 'flex',
                                flexDirection: 'column',
                                alignItems: 'center',
                                justifyContent: 'center',
                                flex: 1,
                                height: '100%',
                                position: 'relative',
                                textDecoration: 'none'
                            }}
                        >
                            {/* Active indicator */}
                            {active && (
                                <div
                                    style={{
                                        position: 'absolute',
                                        top: 0,
                                        left: '50%',
                                        transform: 'translateX(-50%)',
                                        height: '4px',
                                        width: '48px',
                                        borderRadius: '2px',
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
                                    marginBottom: '4px',
                                }}
                            />

                            {/* Label */}
                            <span
                                style={{
                                    fontSize: '11px',
                                    color: active ? '#00d4ff' : 'rgba(255, 255, 255, 0.5)',
                                    fontWeight: active ? 600 : 400,
                                }}
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
