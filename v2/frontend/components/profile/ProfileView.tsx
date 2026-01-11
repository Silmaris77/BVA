"use client";

import React, { useEffect, useState } from "react";
import { GlassCard } from "@/components/ui/GlassCard";
import { api, UserStats, ActivityLog, UserUpdate } from "@/services/api";
import { User, Shield, Zap, Coins, Clock, Award, Edit, X, Save, Palette, Check, Briefcase, Mail } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useLayout } from "@/context/LayoutContext";
import { cn } from "@/app/utils/cn";

export function ProfileView() {
    const [user, setUser] = useState<UserStats | null>(null);
    const [activities, setActivities] = useState<ActivityLog[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Edit State
    const [isEditing, setIsEditing] = useState(false);
    const [editForm, setEditForm] = useState<UserUpdate>({});
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        async function fetchData() {
            try {
                const apiClient = api;

                if (!apiClient.getToken()) {
                    setError("Nie jesteś zalogowany.");
                    setLoading(false);
                    return;
                }

                // Fetch User Data
                const userData = await apiClient.getCurrentUser();
                setUser(userData);
                setEditForm({
                    full_name: userData.full_name || "",
                    company: userData.company || "",
                    avatar_url: userData.avatar_url || "",
                    degen_type: userData.degen_type || ""
                });

                // Fetch Activities
                const activityData = await apiClient.getUserActivities(userData.username);
                setActivities(activityData);
            } catch (err: any) {
                console.error("Profile fetch error:", err);
                setError("Nie udało się pobrać danych profilu.");
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, []);

    const handleSave = async () => {
        setSaving(true);
        try {
            const updatedUser = await api.updateUser(editForm);
            setUser(updatedUser);
            setIsEditing(false);
        } catch (e) {
            console.error("Failed to update profile", e);
            alert("Błąd zapisu profilu");
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return <div className="p-10 text-center text-white/50 animate-pulse">Ładowanie profilu...</div>;
    }

    if (error || !user) {
        return (
            <div className="p-10 text-center">
                <div className="text-red-500 mb-4">{error || "Brak danych użytkownika"}</div>
            </div>
        );
    }

    const nextLevelXp = user.level * 1000;
    const progressPercent = Math.min(100, (user.xp / nextLevelXp) * 100);

    return (
        <div className="space-y-8 max-w-7xl mx-auto p-4 relative">

            {/* EDIT MODAL */}
            <AnimatePresence>
                {isEditing && (
                    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="w-full max-w-lg"
                        >
                            <GlassCard className="border-neon-blue/30">
                                <div className="flex justify-between items-center mb-6">
                                    <h2 className="text-2xl font-bold text-white">Edycja Profilu</h2>
                                    <button onClick={() => setIsEditing(false)} className="text-gray-400 hover:text-white">
                                        <X />
                                    </button>
                                </div>

                                <div className="space-y-4">
                                    <div>
                                        <label className="block text-sm text-gray-400 mb-1">Nazwa Wyświetlana</label>
                                        <input
                                            type="text"
                                            value={editForm.full_name}
                                            onChange={(e) => setEditForm({ ...editForm, full_name: e.target.value })}
                                            className="w-full bg-black/40 border border-white/10 rounded-lg p-2 text-white outline-none focus:border-neon-blue"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm text-gray-400 mb-1">Typ Gracza (Tytuł)</label>
                                        <input
                                            type="text"
                                            value={editForm.degen_type}
                                            onChange={(e) => setEditForm({ ...editForm, degen_type: e.target.value })}
                                            className="w-full bg-black/40 border border-white/10 rounded-lg p-2 text-white outline-none focus:border-neon-blue"
                                            placeholder="np. Nowicjusz, Mistrz Skryptów"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm text-gray-400 mb-1">Firma</label>
                                        <input
                                            type="text"
                                            value={editForm.company}
                                            onChange={(e) => setEditForm({ ...editForm, company: e.target.value })}
                                            className="w-full bg-black/40 border border-white/10 rounded-lg p-2 text-white outline-none focus:border-neon-blue"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm text-gray-400 mb-1">URL Avatara</label>
                                        <input
                                            type="text"
                                            value={editForm.avatar_url}
                                            onChange={(e) => setEditForm({ ...editForm, avatar_url: e.target.value })}
                                            className="w-full bg-black/40 border border-white/10 rounded-lg p-2 text-white outline-none focus:border-neon-blue"
                                            placeholder="https://..."
                                        />
                                        <div className="mt-2 text-xs text-gray-500">
                                            Podgląd:
                                            <div className="w-10 h-10 rounded-full bg-white/10 mt-1 overflow-hidden">
                                                {editForm.avatar_url ? (
                                                    <img src={editForm.avatar_url} className="w-full h-full object-cover" />
                                                ) : <User className="p-2 w-full h-full text-white/50" />}
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div className="mt-8 flex justify-end gap-3">
                                    <button
                                        onClick={() => setIsEditing(false)}
                                        className="px-4 py-2 rounded-lg text-gray-300 hover:text-white"
                                    >
                                        Anuluj
                                    </button>
                                    <button
                                        onClick={handleSave}
                                        disabled={saving}
                                        className="px-6 py-2 bg-neon-blue hover:bg-neon-blue/80 text-black font-bold rounded-lg flex items-center gap-2"
                                    >
                                        {saving ? "Zapisywanie..." : <><Save size={18} /> Zapisz</>}
                                    </button>
                                </div>
                            </GlassCard>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>

            {/* Header Section */}
            <GlassCard className="flex flex-col md:flex-row items-center gap-8 p-8 border-none bg-gradient-to-r from-violet-500/10 to-fuchsia-500/10 relative group">
                <button
                    onClick={() => setIsEditing(true)}
                    className="absolute top-4 right-4 p-2 bg-white/5 hover:bg-white/10 rounded-lg text-white/50 hover:text-white transition-all opacity-0 group-hover:opacity-100 z-10 cursor-pointer"
                    title="Edytuj profil"
                >
                    <Edit size={20} />
                </button>

                <div className="relative">
                    <div className="w-32 h-32 rounded-full bg-gradient-to-br from-neon-blue to-neon-purple p-[2px] shadow-lg shadow-neon-blue/20">
                        <div className="w-full h-full rounded-full bg-black flex items-center justify-center overflow-hidden">
                            {user.avatar_url ? (
                                <img src={user.avatar_url} alt={user.username} className="w-full h-full object-cover" />
                            ) : (
                                <User className="w-16 h-16 text-white/50" />
                            )}
                        </div>
                    </div>
                    <div className="absolute -bottom-2 -right-2 bg-black/80 backdrop-blur border border-white/10 px-3 py-1 rounded-full flex items-center gap-1">
                        <Shield className="w-3 h-3 text-yellow-400" />
                        <span className="text-xs font-bold text-white">Lvl {user.level}</span>
                    </div>
                </div>

                <div className="flex-1 text-center md:text-left space-y-2">
                    <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-white/70">
                        {user.full_name || user.username}
                    </h1>
                    <p className="text-white/50 flex items-center justify-center md:justify-start gap-2">
                        <span className="px-2 py-0.5 rounded bg-white/10 text-sm border border-white/5">
                            {user.degen_type || "Nowicjusz"}
                        </span>
                        {user.company && (
                            <span className="text-sm">@ {user.company}</span>
                        )}
                    </p>

                    {/* XP Bar */}
                    <div className="mt-4 max-w-md">
                        <div className="flex justify-between text-xs text-white/40 mb-1">
                            <span>XP: {user.xp}</span>
                            <span>Next: {nextLevelXp}</span>
                        </div>
                        <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                            <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${progressPercent}%` }}
                                transition={{ duration: 1, ease: "easeOut" }}
                                className="h-full bg-gradient-to-r from-neon-blue to-neon-purple"
                            />
                        </div>
                    </div>
                </div>

                <div className="flex flex-col items-center gap-2">
                    <div className="flex items-center gap-2 bg-gradient-to-r from-yellow-500/20 to-orange-500/20 px-6 py-3 rounded-xl border border-yellow-500/20">
                        <Coins className="w-8 h-8 text-yellow-400" />
                        <div className="text-left">
                            <div className="text-xs text-yellow-200/50">DegenCoins</div>
                            <div className="text-2xl font-bold text-yellow-100">{user.degencoins}</div>
                        </div>
                    </div>
                </div>
            </GlassCard>

            {/* Personalization Section */}
            <GlassCard className="p-8 border-neon-blue/20">
                <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 rounded-lg bg-pink-500/20 text-pink-400">
                        <Palette size={24} />
                    </div>
                    <h2 className="text-xl font-bold text-white">Personalizacja</h2>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <ThemeCard
                        id="glass"
                        name="Glassmorphism"
                        description="Nowoczesny, półprzezroczysty styl."
                        color="from-purple-500 to-blue-500"
                    />
                    <ThemeCard
                        id="minimal"
                        name="Minimalistyczny"
                        description="Czysty, jasny styl dla skupienia."
                        color="bg-zinc-200"
                    />
                    <ThemeCard
                        id="executive"
                        name="Executive"
                        description="Profesjonalny, menedżerski styl."
                        color="bg-slate-200 border-b-4 border-slate-800"
                    />
                    <ThemeCard
                        id="cyberpunk"
                        name="Cyberpunk"
                        description="Ciemny motyw z neonami."
                        color="bg-black border border-yellow-400"
                    />
                </div>
            </GlassCard>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Achievements / Stats Column */}
                <div className="space-y-6">
                    <GlassCard delay={0.1}>
                        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                            <Award className="w-5 h-5 text-neon-purple" />
                            Osiągnięcia
                        </h3>
                        <div className="grid grid-cols-3 gap-2">
                            {/* Placeholders for now */}
                            {[1, 2, 3].map((i) => (
                                <div key={i} className="aspect-square rounded-lg bg-white/5 border border-white/5 flex items-center justify-center hover:bg-white/10 transition-colors cursor-help group relative">
                                    <Award className="w-6 h-6 text-white/20 group-hover:text-neon-blue transition-colors" />
                                </div>
                            ))}
                            {[4, 5, 6].map((i) => (
                                <div key={i} className="aspect-square rounded-lg bg-black/20 border border-white/5 flex items-center justify-center opacity-50">
                                    <Award className="w-6 h-6 text-white/10" />
                                </div>
                            ))}
                        </div>
                    </GlassCard>

                    <GlassCard delay={0.2} className="bg-gradient-to-br from-green-500/5 to-transparent">
                        <div className="flex items-center justify-between">
                            <div>
                                <div className="text-sm text-white/50">Wykonanych aktywności</div>
                                <div className="text-3xl font-bold mt-1">{activities.length}</div>
                            </div>
                            <Zap className="w-10 h-10 text-green-400/20" />
                        </div>
                    </GlassCard>
                </div>

                {/* Recent Activity Column */}
                <div className="md:col-span-2">
                    <GlassCard delay={0.3}>
                        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                            <Clock className="w-5 h-5 text-neon-blue" />
                            Ostatnia Aktywność
                        </h3>

                        <div className="space-y-3">
                            {activities.length === 0 ? (
                                <div className="text-center py-8 text-white/30">Brak aktywności. Zrób coś!</div>
                            ) : (
                                activities.map((act, index) => (
                                    <div key={act.id || index} className="flex items-start gap-4 p-3 rounded-lg hover:bg-white/5 transition-colors border-b border-white/5 last:border-0">
                                        <div className="mt-1 w-2 h-2 rounded-full bg-neon-blue shadow-[0_0_8px_rgba(0,243,255,0.5)] shrink-0" />
                                        <div className="flex-1">
                                            <div className="font-medium text-white/90">{act.description}</div>
                                            <div className="text-xs text-white/40 mt-1">{new Date(act.timestamp).toLocaleString()}</div>
                                        </div>
                                        {act.xp_awarded > 0 && (
                                            <div className="text-neon-purple font-mono text-sm font-bold">+{act.xp_awarded} XP</div>
                                        )}
                                    </div>
                                ))
                            )}
                        </div>
                    </GlassCard>
                </div>
            </div>
        </div>
    );
}

function ThemeCard({ id, name, description, color }: { id: string, name: string, description: string, color: string }) {
    const { theme, setTheme } = useLayout();
    const isActive = theme === id;

    return (
        <button
            onClick={() => setTheme(id as any)}
            className={`relative group p-4 rounded-xl text-left transition-all duration-300 border ${isActive ? 'border-neon-blue bg-white/10' : 'border-white/5 bg-white/5 hover:bg-white/10 hover:border-white/10'}`}
        >
            <div className={`h-20 w-full rounded-lg mb-3 ${color} ${id === 'glass' ? 'bg-gradient-to-r' : ''} opacity-80 group-hover:opacity-100 transition-opacity relative overflow-hidden`}>
                {isActive && (
                    <div className="absolute inset-0 flex items-center justify-center bg-black/20 backdrop-blur-sm">
                        <div className="bg-neon-blue text-black p-2 rounded-full">
                            <Check size={20} className="stroke-[3]" />
                        </div>
                    </div>
                )}
            </div>
            <h3 className="font-bold text-white mb-1">{name}</h3>
            <p className="text-xs text-white/50">{description}</p>
        </button>
    );
}
