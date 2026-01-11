"use client";

import React from "react";
import { GlassCard } from "@/components/ui/GlassCard";
import { Clock, Star, Brain, ArrowRight } from "lucide-react";
import { motion } from "framer-motion";

interface LessonCardProps {
    id: string;
    title: string;
    description: string;
    category: string;
    xp: number;
    difficulty: string; // beginner, intermediate, advanced
    estimatedTime: string;
    available: boolean;
    onClick: () => void;
}

export function LessonCard({
    id, title, description, category, xp, difficulty, estimatedTime, available, onClick
}: LessonCardProps) {

    const difficultyStars = {
        "beginner": 1,
        "intermediate": 2,
        "advanced": 3,
        "expert": 4
    }[difficulty.toLowerCase()] || 1;

    return (
        <GlassCard
            className={`flex flex-col h-full border-t-2 ${available ? 'border-neon-blue/50 hover:border-neon-blue' : 'border-gray-700 opacity-60 cursor-not-allowed'}`}
            onClick={available ? onClick : undefined}
        >
            <div className="flex justify-between items-start mb-4">
                <span className="px-2 py-1 rounded-md bg-white/10 text-xs font-mono text-white/70">
                    {category}
                </span>
                <div className="flex text-yellow-500">
                    {[...Array(difficultyStars)].map((_, i) => (
                        <Star key={i} size={14} fill="currentColor" />
                    ))}
                </div>
            </div>

            <h3 className="text-xl font-bold text-white mb-2 line-clamp-2">{title}</h3>
            <p className="text-white/60 text-sm mb-4 flex-grow line-clamp-3">
                {description}
            </p>

            <div className="flex items-center justify-between mt-auto pt-4 border-t border-white/5">
                <div className="flex items-center gap-3 text-xs text-white/50">
                    <span className="flex items-center gap-1">
                        <Clock size={14} /> {estimatedTime}
                    </span>
                    <span className="flex items-center gap-1 text-neon-purple font-bold">
                        <Brain size={14} /> +{xp} XP
                    </span>
                </div>

                {available && (
                    <div className="p-2 rounded-full bg-white/5 hover:bg-neon-blue hover:text-black transition-colors">
                        <ArrowRight size={16} />
                    </div>
                )}
            </div>
        </GlassCard>
    );
}
