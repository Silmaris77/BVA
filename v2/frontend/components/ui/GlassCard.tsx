"use client";

import React from "react";
import { motion } from "framer-motion";
import { cn } from "@/app/utils/cn";

interface GlassCardProps {
    children: React.ReactNode;
    className?: string;
    delay?: number;
    onClick?: () => void;
}

export function GlassCard({ children, className, delay = 0, onClick }: GlassCardProps) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: delay }}
            onClick={onClick}
            className={cn(
                "bg-white/5 backdrop-blur-md border border-white/10 shadow-xl rounded-2xl p-6 relative overflow-hidden group hover:border-white/20 transition-all duration-300",
                onClick && "cursor-pointer hover:bg-white/10", // Add cursor pointer if clickable
                className
            )}
        >
            <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            <div className="relative z-10">{children}</div>
        </motion.div>
    );
}
