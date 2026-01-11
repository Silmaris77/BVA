"use client";

import { useState, useEffect } from "react";
import { GlassCard } from "@/components/ui/GlassCard";
import { motion } from "framer-motion";
import { Activity, Award, Brain, History, Zap, LogIn } from "lucide-react";
import { api, UserStats, ActivityLog } from "@/services/api";
import Link from "next/link";
import { cn } from "./utils/cn";

export default function Home() {
  const [user, setUser] = useState<UserStats | null>(null);
  const [activities, setActivities] = useState<ActivityLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Próba pobrania danych użytkownika z API
    const fetchUser = async () => {
      try {
        // Najpierw sprawdź czy jest zalogowany
        const token = localStorage.getItem("auth_token");
        if (token) {
          const userData = await api.getCurrentUser();
          setUser(userData);

          // Pobierz aktywności
          try {
            const userActivities = await api.getUserActivities(userData.username);
            setActivities(userActivities);
          } catch (actErr) {
            console.error("Failed to fetch activities", actErr);
          }
        } else {
          // Demo mode
          setUser(null);
          setActivities([]);
        }
      } catch (err) {
        console.log("Not logged in or API error, showing demo");
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  // Demo data when not logged in
  const displayData = user || {
    username: "Demo User",
    xp: 0,
    level: 1,
    degencoins: 0,
    degen_type: null,
    company: null,
  };

  const isLoggedIn = user !== null;

  // Format daty (np. "2 godziny temu")
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));

    if (diffHours < 1) return "przed chwilą";
    if (diffHours < 24) return `${diffHours} godz. temu`;
    return date.toLocaleDateString();
  };

  return (
    <main className="min-h-screen p-8 md:p-12 max-w-7xl mx-auto">
      {/* Login prompt when not logged in */}
      {!isLoggedIn && !loading && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6 p-4 rounded-xl bg-neon-purple/10 border border-neon-purple/30 flex items-center justify-between"
        >
          <span className="text-gray-300">
            Zaloguj się, aby zobaczyć swoje statystyki
          </span>
          <Link
            href="/login"
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-neon-purple text-white text-sm font-semibold hover:bg-neon-purple/80 transition-colors"
          >
            <LogIn size={16} />
            Zaloguj się
          </Link>
        </motion.div>
      )}

      {/* Header */}
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className="mb-12 flex justify-between items-end"
      >
        <div>
          <h1 className="text-4xl md:text-6xl font-bold mb-2">
            Witaj, <span className="bg-clip-text text-transparent bg-gradient-to-r from-neon-blue to-neon-purple">
              {isLoggedIn ? displayData.username : "Neo"}
            </span>
          </h1>
          <p className="text-gray-400 text-lg">Twoje centrum dowodzenia w Brain Venture Academy</p>
        </div>
        <div className="text-right hidden md:block">
          <div className="text-sm text-gray-500">Poziom {displayData.level}</div>
          <div className="text-2xl font-mono text-neon-blue">
            {displayData.degen_type || "Dyrektor Generalny"}
          </div>
        </div>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <GlassCard delay={0.1}>
          <div className="flex items-start justify-between mb-4">
            <div className="p-3 rounded-xl bg-neon-blue/10 text-neon-blue">
              <Zap size={24} />
            </div>
            <span className="text-xs font-mono text-green-400">+12%</span>
          </div>
          <h3 className="text-gray-400 text-sm mb-1">Punkty XP</h3>
          <div className="text-3xl font-bold">{displayData.xp.toLocaleString()}</div>
        </GlassCard>

        <GlassCard delay={0.2}>
          <div className="flex items-start justify-between mb-4">
            <div className="p-3 rounded-xl bg-neon-purple/10 text-neon-purple">
              <Award size={24} />
            </div>
            <span className="text-xs font-mono text-gray-400">Ranga</span>
          </div>
          <h3 className="text-gray-400 text-sm mb-1">Aktualna Pozycja</h3>
          <div className="text-3xl font-bold">{displayData.degen_type || "Lider Zmian"}</div>
        </GlassCard>

        <GlassCard delay={0.3}>
          <div className="flex items-start justify-between mb-4">
            <div className="p-3 rounded-xl bg-green-500/10 text-green-400">
              <Activity size={24} />
            </div>
            <span className="text-xs font-mono text-green-400">+{displayData.degencoins}</span>
          </div>
          <h3 className="text-gray-400 text-sm mb-1">DegenCoins</h3>
          <div className="text-3xl font-bold">{displayData.degencoins}</div>
        </GlassCard>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content Area */}
        <div className="lg:col-span-2 space-y-6">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <Brain size={20} className="text-neon-purple" />
            Polecane dla Ciebie
          </h2>

          <GlassCard className="from-white/10 to-transparent bg-gradient-to-r">
            <div className="flex flex-col md:flex-row gap-6 items-center">
              <div className="w-full md:w-1/3 aspect-video rounded-lg bg-black/40 border border-white/10 flex items-center justify-center">
                <span className="text-3xl">🎮</span>
              </div>
              <div className="flex-1">
                <div className="text-xs text-neon-blue font-bold mb-2">NOWA GRA</div>
                <h3 className="text-xl font-bold mb-2">Negocjacje Kryzysowe</h3>
                <p className="text-gray-400 text-sm mb-4">
                  Przejmij stery w symulacji trudnych rozmów z kluczowym klientem. Masz 15 minut na uratowanie kontraktu.
                </p>
                <button className="px-6 py-2 rounded-lg bg-neon-purple text-white text-sm font-semibold hover:bg-neon-purple/80 transition-colors shadow-lg shadow-neon-purple/20">
                  Rozpocznij Symulację
                </button>
              </div>
            </div>
          </GlassCard>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <GlassCard>
              <h3 className="font-bold mb-2">Autodiagnoza Liderska</h3>
              <p className="text-sm text-gray-400 mb-4">Sprawdź swój styl zarządzania i odkryj mocne strony.</p>
              <div className="w-full bg-white/5 rounded-full h-1.5 mb-2">
                <div className="bg-neon-blue w-3/4 h-1.5 rounded-full"></div>
              </div>
              <div className="text-right text-xs text-gray-400">75% ukończono</div>
            </GlassCard>
            <GlassCard>
              <h3 className="font-bold mb-2">Narzędzia Milwaukee</h3>
              <p className="text-sm text-gray-400 mb-4">Dobierz idealny zestaw narzędzi do specyfiki Twojej pracy.</p>
              <button className="text-sm text-neon-blue hover:text-white transition-colors">Otwórz konfigurator →</button>
            </GlassCard>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <History size={20} className="text-gray-400" />
            Ostatnie Aktywności
          </h2>

          <GlassCard className="p-0 overflow-hidden min-h-[200px]">
            {activities.length > 0 ? (
              activities.map((act) => (
                <div key={act.id} className="p-4 border-b border-white/5 hover:bg-white/5 cursor-pointer transition-colors flex items-center gap-4 group">
                  <div className={cn(
                    "w-2 h-2 rounded-full transition-shadow",
                    act.xp_awarded > 0 ? "bg-neon-blue group-hover:shadow-[0_0_10px_#00f3ff]" : "bg-gray-500"
                  )}></div>
                  <div>
                    <div className="text-sm font-medium">{act.description}</div>
                    <div className="text-xs text-gray-500 flex gap-2">
                      <span>{formatDate(act.timestamp)}</span>
                      {act.xp_awarded > 0 && <span className="text-neon-blue">+{act.xp_awarded} XP</span>}
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="p-8 text-center text-gray-500 text-sm">
                Brak ostatnich aktywności
              </div>
            )}

            {activities.length > 0 && (
              <div className="p-4 text-center text-xs text-gray-400 hover:text-white cursor-pointer">
                Zobacz całą historię
              </div>
            )}
          </GlassCard>
        </div>
      </div>
    </main>
  );
}
