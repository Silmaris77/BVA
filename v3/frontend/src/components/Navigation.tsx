'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { useRouter } from 'next/navigation'
import { Home, BookOpen, Gamepad2, User, Bot, Settings, LogOut } from 'lucide-react'

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
            className="flex flex-col"
            style={{
                width: '200px',
                background: 'rgba(0, 0, 0, 0.3)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                borderRight: '1px solid rgba(255, 255, 255, 0.08)',
                padding: '24px 16px',
                position: 'fixed',
                left: 0,
                top: 0,
                bottom: 0,
                zIndex: 100
            }}>
            {/* Logo */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '8px 12px',
                marginBottom: '32px'
            }}>
                <div style={{
                    width: '36px',
                    height: '36px',
                    background: 'linear-gradient(135deg, #b000ff, #00d4ff)',
                    borderRadius: '10px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: 800,
                    fontSize: '18px'
                }}>B</div>
                <div style={{
                    fontSize: '18px',
                    fontWeight: 700,
                    background: 'linear-gradient(135deg, #00d4ff, #b000ff)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text'
                }}>BrainVenture</div>
            </div>

            {/* Main Nav */}
            <nav style={{ marginBottom: '32px' }}>
                <NavItem href="/" icon={<Home size={20} />} label="Hub" active={isActive('/')} />
                <NavItem href="/lessons" icon={<BookOpen size={20} />} label="Nauka" active={isActive('/lessons')} />
                <NavItem href="/practice" icon={<Gamepad2 size={20} />} label="Praktyka" active={isActive('/practice')} />
                <NavItem href="/profile" icon={<User size={20} />} label="Profil" active={isActive('/profile')} />
            </nav>

            {/* Footer Nav */}
            <div style={{ marginTop: 'auto', paddingTop: '24px', borderTop: '1px solid rgba(255, 255, 255, 0.08)' }}>
                <NavItem href="/ai-assistant" icon={<Bot size={20} />} label="AI Assistant" active={false} />
                <NavItem href="/settings" icon={<Settings size={20} />} label="Ustawienia" active={false} />
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
                color: active ? '#ffffff' : 'rgba(255, 255, 255, 0.6)',
                border: active ? '1px solid #00d4ff' : '1px solid transparent',
                background: active ? 'rgba(0, 212, 255, 0.15)' : 'transparent',
                boxShadow: active ? '0 0 20px rgba(0, 212, 255, 0.2)' : 'none',
                textDecoration: 'none',
                transition: 'all 0.2s'
            }}
        >
            {icon}
            <span>{label}</span>
        </Link>
    )
}
