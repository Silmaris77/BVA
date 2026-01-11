import React, { useState, useEffect } from "react";
import { GlassCard } from "@/components/ui/GlassCard";
import { api, LessonResponse } from "@/services/api";
import { BookOpen, CheckCircle, ChevronLeft, PlayCircle } from "lucide-react";
import { motion } from "framer-motion";
import { cn } from "@/app/utils/cn";
import Link from "next/link";
import { useRouter } from "next/navigation";

export function LessonPlayer({ lessonId }: { lessonId: string }) {
    const [lesson, setLesson] = useState<LessonResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [completed, setCompleted] = useState(false);
    const router = useRouter();

    useEffect(() => {
        async function loadLesson() {
            try {
                const data = await api.getLessonDetails(lessonId);
                setLesson(data);
                if (data.completed) setCompleted(true);
            } catch (e) {
                console.error("Failed to load lesson", e);
            } finally {
                setLoading(false);
            }
        }
        loadLesson();
    }, [lessonId]);

    const handleComplete = async () => {
        if (!lesson) return;
        try {
            await api.completeLesson(lesson.id);
            setCompleted(true);
            // Optional: Show toast or confetti
        } catch (e) {
            console.error("Failed to complete lesson", e);
        }
    };

    if (loading) return <div className="p-20 text-center text-white/50 animate-pulse">Ładowanie lekcji...</div>;
    if (!lesson) return <div className="p-20 text-center text-red-400">Nie znaleziono lekcji</div>;

    return (
        <div className="flex h-[calc(100vh-6rem)] gap-6 overflow-hidden">
            {/* Back Button & Sidebar Placeholder */}
            <div className="hidden md:flex flex-col w-64 shrink-0 gap-4">
                <Link href="/lessons" className="flex items-center gap-2 text-white/60 hover:text-white transition-colors">
                    <ChevronLeft size={20} />
                    Powrót do listy
                </Link>
                <GlassCard className="p-6 bg-white/5 border-none h-full flex flex-col justify-between">
                    <div>
                        <h3 className="text-sm font-bold text-white/40 uppercase tracking-wider mb-4">Informacje</h3>
                        <div className="space-y-4">
                            <div>
                                <span className="text-xs text-white/40 block">Kategoria</span>
                                <span className="text-sm text-neon-blue">{lesson.category}</span>
                            </div>
                            <div>
                                <span className="text-xs text-white/40 block">Trudność</span>
                                <span className="text-sm text-white">{lesson.difficulty}</span>
                            </div>
                            <div>
                                <span className="text-xs text-white/40 block">XP za ukończenie</span>
                                <span className="text-sm text-yellow-400 font-bold">+{lesson.xp_reward} XP</span>
                            </div>
                        </div>
                    </div>

                    {!completed ? (
                        <button
                            onClick={handleComplete}
                            className="w-full py-3 px-4 bg-neon-blue hover:bg-neon-blue/80 text-white rounded-lg font-bold transition-all shadow-lg shadow-neon-blue/20 flex items-center justify-center gap-2"
                        >
                            <CheckCircle size={18} />
                            Oznacz jako ukończone
                        </button>
                    ) : (
                        <div className="w-full py-3 px-4 bg-green-500/20 text-green-400 border border-green-500/50 rounded-lg text-center font-medium flex items-center justify-center gap-2">
                            <CheckCircle size={18} />
                            Ukończono
                        </div>
                    )}
                </GlassCard>
            </div>

            {/* Main Content Area */}
            <div className="flex-1 flex flex-col min-w-0">
                <GlassCard className="flex-1 overflow-y-auto p-0 relative border-white/5 flex flex-col">
                    {/* Video Header */}
                    <div className="aspect-video w-full bg-black relative">
                        <iframe
                            src={lesson.video_url}
                            title={lesson.title}
                            className="w-full h-full"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowFullScreen
                        />
                    </div>

                    <div className="p-8 md:p-12">
                        <header className="mb-8 pb-8 border-b border-white/5">
                            <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">{lesson.title}</h1>
                            <div className="prose prose-invert max-w-none text-white/80 leading-relaxed">
                                <p>{lesson.description}</p>
                            </div>
                        </header>

                        {/* Mobile Complete Button */}
                        <div className="md:hidden mt-8">
                            {!completed ? (
                                <button
                                    onClick={handleComplete}
                                    className="w-full py-3 px-4 bg-neon-blue text-white rounded-lg font-bold"
                                >
                                    Oznacz jako ukończone (+{lesson.xp_reward} XP)
                                </button>
                            ) : (
                                <div className="w-full py-3 px-4 bg-green-500/20 text-green-400 border border-green-500/50 rounded-lg text-center">
                                    Lekcja Ukończona
                                </div>
                            )}
                        </div>
                    </div>
                </GlassCard>
            </div>
        </div>
    );
}
