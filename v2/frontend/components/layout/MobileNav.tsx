"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import {
    Home,
    Gamepad2,
    Wrench,
    User,
    Menu
} from "lucide-react";
import { cn } from "@/app/utils/cn";

const menuItems = [
    { icon: Home, label: "Home", href: "/" },
    { icon: Gamepad2, label: "Gry", href: "/simulations" },
    // { icon: Menu, label: "Menu", href: "/menu", isMain: true }, // Opcja na przyszłość
    { icon: Wrench, label: "Narzędzia", href: "/tools" },
    { icon: User, label: "Profil", href: "/profile" },
];

export function MobileNav() {
    const pathname = usePathname();

    return (
        <div className="md:hidden fixed bottom-6 left-4 right-4 z-50">
            <div className="glass-effect rounded-2xl bg-[#0f1016]/80 backdrop-blur-xl border border-white/10 shadow-2xl overflow-hidden">
                <nav className="flex items-center justify-around p-2">
                    {menuItems.map((item) => {
                        const isActive = pathname === item.href;
                        const Icon = item.icon;

                        return (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={cn(
                                    "relative flex flex-col items-center justify-center w-14 h-14 rounded-xl transition-all duration-200",
                                    isActive ? "text-white" : "text-gray-500"
                                )}
                            >
                                {isActive && (
                                    <motion.div
                                        layoutId="mobile-nav-active"
                                        className="absolute inset-0 bg-white/10 rounded-xl -z-10"
                                        transition={{ type: "spring", stiffness: 300, damping: 30 }}
                                    />
                                )}

                                <Icon
                                    size={24}
                                    className={cn(
                                        "transition-transform duration-200",
                                        isActive ? "scale-110 text-neon-blue" : "scale-100"
                                    )}
                                />

                                {/* Opcjonalne labele - na małym ekranie mogą być ukryte lub pokazywać się tylko aktywne */}
                                {/* <span className="text-[10px] mt-1 font-medium">{item.label}</span> */}
                            </Link>
                        );
                    })}
                </nav>
            </div>
        </div>
    );
}
