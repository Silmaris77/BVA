'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { useRouter } from 'next/navigation'
import { useState } from 'react'
import { Home, BookOpen, Gamepad2, User, LogOut } from 'lucide-react'

export default function Sidebar() {
    const pathname = usePathname()
    const { signOut } = useAuth()
    const router = useRouter()

    const isActive = (path: string) => pathname === path

    const handleSignOut = async () => {
        await signOut()
        router.push('/auth/login')
    }

    return (
        <div
            className="nav-sidebar flex flex-col fixed left-0 top-0 bottom-0 z-[100] w-[200px] px-4 py-0"
        >
            {/* Logo - wyrównane do wysokości TopBar (65px) */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                height: '65px',
                marginBottom: '24px',
                borderBottom: '1px solid rgba(255, 255, 255, 0.05)'
            }}>
                <div style={{
                    fontSize: '18px',
                    fontWeight: 700,
                    background: 'linear-gradient(135deg, #0E2A47, #1E73B9, #B10A4A)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text',
                    textAlign: 'center',
                    lineHeight: '1.2'
                }}>BrainVenture</div>
            </div>

            {/* Main Nav */}
            <nav style={{ marginBottom: '32px' }}>
                <NavItem href="/" icon={<Home size={20} />} label="Hub" active={pathname === '/'} />
                <NavItem href="/lessons" icon={<BookOpen size={20} />} label="Nauka" active={pathname?.startsWith('/lessons') || pathname?.startsWith('/engrams') || pathname?.startsWith('/resources')} />
                <NavItem href="/practice" icon={<Gamepad2 size={20} />} label="Praktyka" active={pathname?.startsWith('/practice')} />
                <NavItem href="/profile" icon={<User size={20} />} label="Profil" active={pathname?.startsWith('/profile')} />
            </nav>

            {/* Footer Nav */}
            <div style={{ marginTop: 'auto', paddingTop: '24px', borderTop: '1px solid rgba(255, 255, 255, 0.08)' }}>
                <button
                    onClick={handleSignOut}
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        padding: '12px 16px',
                        margin: '4px 0',
                        borderRadius: '12px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: 500,
                        color: 'rgba(255, 255, 255, 0.6)',
                        border: '1px solid transparent',
                        background: 'transparent',
                        width: '100%',
                        transition: 'all 0.2s'
                    }}
                    onMouseOver={(e) => {
                        e.currentTarget.style.background = 'rgba(255, 68, 68, 0.1)'
                        e.currentTarget.style.borderColor = '#ef4444'
                    }}
                    onMouseOut={(e) => {
                        e.currentTarget.style.background = 'transparent'
                        e.currentTarget.style.borderColor = 'transparent'
                    }}
                >
                    <LogOut size={20} />
                    <span>Wyloguj</span>
                </button>
            </div>
        </div>
    )
}

function NavItem({ href, icon, label, active }: { href: string; icon: React.ReactNode; label: string; active: boolean }) {
    return (
        <Link
            href={href}
            className={`nav-item-link ${active ? 'active' : ''}`}
        >
            <div style={{ position: 'relative', zIndex: 2, display: 'flex', alignItems: 'center', gap: '12px' }}>
                {icon}
                <span>{label}</span>
            </div>
        </Link>
    )
}
