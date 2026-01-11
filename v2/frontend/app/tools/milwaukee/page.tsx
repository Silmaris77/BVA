"use client";

import { MilwaukeeApplicationEngine } from "@/components/tools/MilwaukeeApplicationEngine";
import { Briefcase } from "lucide-react";

export default function MilwaukeeToolsPage() {
    return (
        <div className="min-h-screen p-8 md:p-12 max-w-7xl mx-auto pb-32">
            <div className="text-center mb-12">
                <div className="inline-flex items-center justify-center p-4 rounded-full bg-neon-red/10 text-neon-red mb-6">
                    <Briefcase size={32} />
                </div>
                <h1 className="text-5xl font-bold mb-4">Narzędzia Milwaukee</h1>
                <p className="text-gray-400 text-lg max-w-2xl mx-auto">
                    Profesjonalne narzędzia wsparcia sprzedaży. Zdiagnozuj potrzeby klienta i dobierz idealne rozwiązanie.
                </p>
            </div>

            <MilwaukeeApplicationEngine />
        </div>
    );
}
