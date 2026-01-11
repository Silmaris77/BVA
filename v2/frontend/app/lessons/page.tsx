"use client";

import React, { useEffect, useState } from "react";
import { api, LessonResponse } from "@/services/api";
import { LessonCard } from "@/components/lessons/LessonCard";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";

export default function LessonsPage() {
    const [lessons, setLessons] = useState<LessonResponse[]>([]);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        async function fetchLessons() {
            try {
                const data = await api.getLessons();
                setLessons(data);
            } catch (err) {
                console.error("Failed to fetch lessons", err);
            } finally {
                setLoading(false);
            }
        }
        fetchLessons();
    }, []);

    const handleLessonSelect = (lessonId: string) => {
        router.push(`/lessons/${lessonId}`);
    };

    if (loading) {
        return <div className="p-10 text-center text-white/50 animate-pulse">Ładowanie lekcji...</div>;
    }

    return (
        <div className="space-y-8 max-w-7xl mx-auto p-4">
            <header className="mb-8">
                <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-white/70 mb-2">
                    Lekcje
                </h1>
                <p className="text-white/60">
                    Rozwijaj swoje umiejętności i zdobywaj punkty doświadczenia.
                </p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {lessons.map((lesson) => (
                    <LessonCard
                        key={lesson.id}
                        id={lesson.id}
                        title={lesson.title}
                        description={lesson.description}
                        category={lesson.category}
                        xp={lesson.xp_reward}
                        difficulty={lesson.difficulty}
                        estimatedTime={`${Math.ceil(lesson.duration / 60)} min`}
                        available={lesson.available ?? true} // legacy support or default true
                        onClick={() => handleLessonSelect(lesson.id)}
                    />
                ))}
            </div>
        </div>
    );
}
