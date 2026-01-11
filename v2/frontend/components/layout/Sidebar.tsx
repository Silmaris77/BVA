"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Wrench, User, LogOut, Menu, X, Gamepad2, BookOpen, Brain, Settings } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/app/utils/cn";
import { api } from "@/services/api";

const menuItems = [
    { icon: LayoutDashboard, label: "Pulpit", href: "/" }, // Changed label and icon
    { icon: BookOpen, label: "Lekcje", href: "/lessons" }, // Added
    { icon: Wrench, label: "Narzędzia", href: "/tools/milwaukee" },
    { icon: Gamepad2, label: "Symulacje", href: "/simulations" },
    { icon: User, label: "Profil", href: "/profile" },
];

export function Sidebar() {
    const pathname = usePathname();

    const handleLogout = () => {
        api.clearToken();
        window.location.href = "/login";
    };

    return (
        <aside className="hidden md:flex flex-col w-64 h-screen fixed left-0 top-0 border-r border-white/10 z-50 sidebar-container bg-[#0f0c29] transition-colors duration-300">
            {/* Logo Area */}
            <div className="p-8 pb-4">
                <Link href="/" className="flex items-center gap-3 mb-8">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-neon-blue to-neon-purple flex items-center justify-center text-white">
                        <Brain size={24} />
                    </div>
                    <div className="font-bold text-lg leading-tight">
                        Brain Venture <br />
                        <span className="text-neon-blue">Academy</span>
                    </div>
                </Link>
            </div>

            {/* Navigation */}
            <nav className="flex-1 px-4 space-y-2">
                {menuItems.map((item) => {
                    const isActive = pathname === item.href;
                    const Icon = item.icon;

                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group relative overflow-hidden",
                                isActive
                                    ? "text-white bg-white/10 shadow-lg shadow-black/20"
                                    : "text-gray-400 hover:text-white hover:bg-white/5"
                            )}
                        >
                            {isActive && (
                                <motion.div
                                    layoutId="sidebar-active"
                                    className="absolute left-0 top-0 bottom-0 w-1 bg-neon-blue rounded-full"
                                />
                            )}
                            <Icon size={20} className={cn(isActive && "text-neon-blue")} />
                            <span className="font-medium">{item.label}</span>
                        </Link>
                    );
                })}
            </nav>

            {/* Bottom Actions */}
            <div className="p-4 border-t border-white/5 space-y-2">
                <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-gray-400 hover:text-white hover:bg-white/5 transition-colors">
                    <Settings size={20} />
                    <span className="font-medium">Ustawienia</span>
                </button>
                <button
                    onClick={handleLogout}
                    className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-red-400 hover:text-red-300 hover:bg-red-500/10 transition-colors"
                >
                    <LogOut size={20} />
                    <span className="font-medium">Wyloguj</span>
                </button>
            </div>
        </aside>
    );
}
