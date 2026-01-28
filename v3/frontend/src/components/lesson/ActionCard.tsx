import React, { useState } from 'react';
import { Share2, Mail, MessageCircle, Copy, CheckCircle, Smartphone, Send, Zap, ArrowRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface ActionCardProps {
    title: string;
    description: string;
    actionType: 'sms' | 'email' | 'copy';
    content: string; // The text to be sent/copied
    buttonSensitive?: boolean;
}

export default function ActionCard({
    title = "Podejmij Działanie",
    description = "Wykonaj to zadanie teraz.",
    actionType = "copy",
    content = ""
}: ActionCardProps) {
    const [status, setStatus] = useState<'idle' | 'success'>('idle');

    const handleAction = () => {
        if (actionType === 'copy') {
            navigator.clipboard.writeText(content);
            setStatus('success');
            setTimeout(() => setStatus('idle'), 2000);
            return;
        }

        if (actionType === 'sms') {
            window.open(`sms:?body=${encodeURIComponent(content)}`);
        }

        if (actionType === 'email') {
            window.open(`mailto:?body=${encodeURIComponent(content)}`);
        }

        setStatus('success');
        setTimeout(() => setStatus('idle'), 3000);
    };

    const getIcon = () => {
        if (status === 'success') return <CheckCircle className="w-5 h-5" />;
        if (actionType === 'sms') return <MessageCircle className="w-5 h-5" />;
        if (actionType === 'email') return <Mail className="w-5 h-5" />;
        return <Copy className="w-5 h-5" />;
    };

    const getLabel = () => {
        if (status === 'success') return "Zadanie Wykonane!";
        if (actionType === 'sms') return "Otwórz Wiadomości";
        if (actionType === 'email') return "Otwórz Pocztę";
        return "Skopiuj Treść";
    };

    const getHeaderIcon = () => {
        if (actionType === 'sms') return <Smartphone className="w-6 h-6 text-white" />;
        if (actionType === 'email') return <Mail className="w-6 h-6 text-white" />;
        return <Zap className="w-6 h-6 text-white" />;
    };

    return (
        <div className="flex flex-col h-full items-center justify-center p-6 w-full max-w-4xl mx-auto">

            {/* --- MISSION HEADER --- */}
            <div className="text-center space-y-4 mb-8">
                <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-indigo-500 to-purple-600 px-4 py-1.5 rounded-full shadow-lg shadow-purple-900/40 border border-purple-400/20">
                    <Zap className="w-4 h-4 text-yellow-300 fill-yellow-300 animate-pulse" />
                    <span className="text-xs font-bold text-white tracking-widest uppercase">
                        Active Challenge
                    </span>
                </div>

                <h3 className="text-3xl md:text-4xl font-bold text-white tracking-tight">
                    {title}
                </h3>
                <p className="text-gray-400 text-lg max-w-xl mx-auto leading-relaxed">
                    {description}
                </p>
            </div>

            <div className="flex flex-col md:flex-row items-center gap-8 md:gap-12 w-full max-w-3xl">

                {/* --- PHONE PREVIEW (Visual) --- */}
                <div className="relative group w-full max-w-xs md:w-80 flex-shrink-0 mx-auto">
                    {/* Phone Frame */}
                    <div className="relative bg-gray-900 rounded-[2.5rem] border-[8px] border-gray-800 shadow-2xl overflow-hidden h-[400px] transform group-hover:-translate-y-2 transition-transform duration-500">
                        {/* Notch */}
                        <div className="absolute top-0 inset-x-0 h-6 bg-gray-800 rounded-b-xl w-32 mx-auto z-20"></div>

                        {/* Screen Content */}
                        <div className="h-full bg-gray-950 p-4 pt-12 flex flex-col relative">
                            {/* Contact Header */}
                            <div className="flex items-center space-x-3 pb-4 border-b border-gray-800/50 mb-4">
                                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-gray-700 to-gray-600 flex items-center justify-center text-xs font-bold text-gray-300">
                                    ?
                                </div>
                                <div className="flex flex-col">
                                    <span className="text-xs font-bold text-gray-400">Twój Pracownik</span>
                                    <span className="text-[10px] text-gray-600">Mobile</span>
                                </div>
                            </div>

                            {/* Message Bubble - RIGHT (Sent by User) */}
                            <div className="flex justify-end mb-4">
                                <div className="bg-gradient-to-br from-indigo-600 to-blue-600 text-white p-3 rounded-2xl rounded-tr-none text-sm leading-relaxed shadow-lg max-w-[90%] relative">
                                    {content}
                                    {/* Tail */}
                                    <div className="absolute top-0 -right-2 w-4 h-4 bg-blue-600 clip-path-triangle transform rotate-90"></div>
                                </div>
                            </div>

                            {/* Typing Indicator / Input Mock */}
                            <div className="mt-auto flex items-center space-x-2 opacity-50">
                                <div className="h-8 bg-gray-800 rounded-full flex-1"></div>
                                <div className="w-8 h-8 bg-blue-600/50 rounded-full"></div>
                            </div>
                        </div>
                    </div>

                    {/* Glow effect behind phone */}
                    <div className="absolute -inset-4 bg-blue-500/20 blur-2xl rounded-[3rem] -z-10 group-hover:bg-blue-500/30 transition-all"></div>
                </div>

                {/* --- ACTION AREA --- */}
                <div className="flex flex-col items-center md:items-start space-y-6 flex-1 text-center md:text-left w-full">
                    <div className="space-y-2">
                        <div className="text-xs font-bold text-gray-500 uppercase tracking-wider">
                            Twoje Zadanie
                        </div>
                        <p className="text-gray-300">
                            Gotowy szablon jest przygotowany. Wystarczy, że klikniesz przycisk poniżej, a treść zostanie przeniesiona do aplikacji.
                        </p>
                    </div>

                    <div className="w-full relative">
                        {status === 'success' && (
                            <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="absolute -top-12 left-0 right-0 flex justify-center md:justify-start"
                            >
                                <span className="text-green-400 font-bold bg-green-400/10 px-3 py-1 rounded-full text-sm">
                                    Świetnie! Zadanie zaliczone.
                                </span>
                            </motion.div>
                        )}

                        <button
                            onClick={handleAction}
                            className={`
                                group relative flex items-center justify-center md:justify-between px-8 py-5 w-full rounded-2xl 
                                font-bold text-lg transition-all transform active:scale-95 shadow-xl hover:shadow-2xl overflow-hidden
                                ${status === 'success'
                                    ? 'bg-green-600 text-white hover:bg-green-700'
                                    : 'bg-white hover:bg-gray-50 text-gray-900'
                                }
                            `}
                        >
                            <div className="flex items-center space-x-3 z-10">
                                {getIcon()}
                                <span>{getLabel()}</span>
                            </div>

                            {status !== 'success' && (
                                <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-gray-900 group-hover:translate-x-1 transition-all z-10 hidden md:block" />
                            )}

                            {/* Button Shine Effect */}
                            {status !== 'success' && (
                                <div className="absolute inset-0 -translate-x-full group-hover:animate-shine bg-gradient-to-r from-transparent via-white/20 to-transparent z-0"></div>
                            )}
                        </button>
                    </div>

                    <p className="text-xs text-gray-500 max-w-xs">
                        *Kliknięcie otworzy domyślną aplikację na Twoim urządzeniu. Możesz edytować wiadomość przed wysłaniem.
                    </p>
                </div>
            </div>
        </div>
    );
}
