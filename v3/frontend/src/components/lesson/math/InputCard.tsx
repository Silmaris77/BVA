'use client';

import { useState } from 'react';
import { Check, X, HelpCircle } from 'lucide-react';
import MathRenderer from './MathRenderer';
import { cn } from '@/lib/utils'; // Assuming utils exist or I will use simple class strings if not

// Fallback for cn if not exists (I'll implement it inline to be safe)
function classNames(...classes: (string | undefined | null | false)[]) {
    return classes.filter(Boolean).join(' ');
}

interface InputCardProps {
    question: string; // "Oblicz pole: $P = a^2$"
    correctAnswer: string | number; // "16"
    placeholder?: string;
    unit?: string; // "cm²"
    hint?: string;
    explanation?: string;
}

export default function InputCard({ question, correctAnswer, placeholder, unit, hint, explanation }: InputCardProps) {
    const [value, setValue] = useState('');
    const [isSubmitted, setIsSubmitted] = useState(false);
    const [isCorrect, setIsCorrect] = useState(false);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!value) return;

        // Simple validation logic (string comparison for now, can be upgraded to math equivalence later)
        const isMatch = value.trim().toLowerCase() === String(correctAnswer).toLowerCase();

        setIsSubmitted(true);
        setIsCorrect(isMatch);
    };

    const handleRetry = () => {
        setIsSubmitted(false);
        setValue('');
    };

    return (
        <div className="w-full max-w-2xl mx-auto glass-card p-8 rounded-2xl border border-white/10 relative overflow-hidden">
            {/* Badge */}
            <div className="absolute top-4 left-4 flex items-center gap-2">
                <span className="bg-purple-500/10 text-purple-300 px-2 py-0.5 rounded text-[10px] font-bold uppercase border border-purple-500/20 tracking-wider">
                    Zadanie
                </span>
            </div>

            {/* Question */}
            <div className="mt-6 mb-8 text-xl md:text-2xl font-medium text-white text-center">
                <MathRenderer content={question} />
            </div>

            {/* Input Area */}
            <form onSubmit={handleSubmit} className="flex flex-col items-center gap-4">
                <div className="relative w-full max-w-xs group">
                    <input
                        type="text"
                        value={value}
                        onChange={(e) => setValue(e.target.value)}
                        disabled={isSubmitted && isCorrect}
                        placeholder={placeholder || 'Wpisz wynik...'}
                        className={classNames(
                            "w-full bg-black/30 border-2 rounded-xl px-4 py-3 text-center text-xl font-mono text-white outline-none transition-all placeholder:text-white/20",
                            isSubmitted
                                ? (isCorrect ? "border-green-500 bg-green-500/10" : "border-red-500 bg-red-500/10")
                                : "border-white/10 focus:border-[var(--accent-blue)] focus:bg-black/50"
                        )}
                        autoComplete="off"
                    />
                    {unit && (
                        <span className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 font-mono">
                            <MathRenderer content={`$${unit}$`} inline />
                        </span>
                    )}
                </div>

                {/* Submit / Feedback */}
                {!isSubmitted ? (
                    <button
                        type="submit"
                        disabled={!value}
                        className="bg-[var(--accent-blue)] text-black font-bold px-8 py-2 rounded-lg hover:brightness-110 transition disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        Sprawdź
                    </button>
                ) : (
                    <div className="animate-in fade-in slide-in-from-bottom-2 flex flex-col items-center gap-4">
                        {isCorrect ? (
                            <div className="flex items-center gap-2 text-green-400 font-bold bg-green-500/10 px-4 py-2 rounded-lg border border-green-500/20">
                                <Check size={20} /> Świetnie! To poprawny wynik.
                            </div>
                        ) : (
                            <div className="flex flex-col items-center gap-2">
                                <div className="flex items-center gap-2 text-red-400 font-bold bg-red-500/10 px-4 py-2 rounded-lg border border-red-500/20">
                                    <X size={20} /> Niestety, to nie to.
                                </div>
                                <button
                                    onClick={handleRetry}
                                    type="button"
                                    className="text-xs text-gray-400 hover:text-white underline"
                                >
                                    Spróbuj ponownie
                                </button>
                            </div>
                        )}
                    </div>
                )}
            </form>

            {/* Explanation / Hint */}
            {isSubmitted && (isCorrect || explanation) && (
                <div className="mt-8 pt-6 border-t border-white/5 text-sm text-gray-300">
                    <p className="font-bold text-[var(--accent-blue)] mb-1 flex items-center gap-2">
                        <HelpCircle size={14} /> Wyjaśnienie:
                    </p>
                    <MathRenderer content={explanation || `Poprawny wynik to: ${correctAnswer}`} />
                </div>
            )}
        </div>
    );
}
