'use client';

import { useState, useRef } from 'react';
import { Check, X, HelpCircle, Mic, Loader2 } from 'lucide-react';
import MathRenderer from './MathRenderer';

// Helper function for conditional classnames
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

    // Speech Recognition State
    const [listening, setListening] = useState(false);
    const recognitionRef = useRef<any>(null);

    const toggleListening = () => {
        if (listening) {
            if (recognitionRef.current) recognitionRef.current.stop();
            return;
        }

        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert('Twoja przeglądarka nie obsługuje rozpoznawania mowy.');
            return;
        }

        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognitionRef.current = recognition;

        recognition.lang = 'pl-PL';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = () => setListening(true);

        recognition.onresult = (event: any) => {
            const raw = event.results[0][0].transcript.toLowerCase().trim();

            // 1. Remove common conversation fillers
            let processed = raw.replace(/^(wynik|to|jest|odpowiedź|równa się)\s+/g, '');

            // 2. Map Polish math terms to symbols/numbers
            const replacements: [RegExp, string][] = [
                [/minus /g, '-'],
                [/przecinek/g, '.'],
                [/kropka/g, '.'],
                // Common fractions
                [/jedna druga/g, '1/2'],
                [/pół/g, '0.5'], // Context dependent, but 0.5 is safe for inputs usually
                [/jedna trzecia/g, '1/3'],
                [/dwie trzecie/g, '2/3'],
                [/jedna czwarta/g, '1/4'],
                [/trzy czwarte/g, '3/4'],
                [/jedna piąta/g, '1/5'],
                [/dwie piąte/g, '2/5'],
                [/trzy piąte/g, '3/5'],
                [/cztery piąte/g, '4/5'],
                // Handle "cała/całe" for mixed numbers if needed: "jedna cała i jedna druga" -> "1 1/2"
                // STT might give "1 cała i 1/2" -> map "cała i" to space
                [/(\d+)\s+(cała|całe|całych)\s+i\s+/g, '$1 '],
            ];

            replacements.forEach(([pattern, replacement]) => {
                processed = processed.replace(pattern, replacement);
            });

            // 3. Cleanup whitespace
            processed = processed.replace(/\s*\/\s*/g, '/').trim();

            // 4. Extract the mathematical part
            // Matches:
            // - Negative numbers (-5)
            // - Decimals (5.2)
            // - Mixed numbers (1 1/2) - requires space
            // - Simple fractions (3/4)
            const mathRegex = /^-?(\d+([.,]\d+)?(\s+\d+\/\d+)?|\d+\/\d+)$/;

            // If the whole string matches a math expression, use it. 
            // Otherwise, try to find a match inside.
            const match = processed.match(/-?(\d+([.,]\d+)?(\s+\d+\/\d+)?|\d+\/\d+)/);

            if (match) {
                // Formatting: ensure dot for decimals
                setValue(match[0].replace(',', '.'));
            } else {
                // Fallback: set whatever we have, user can correct
                setValue(processed);
            }
        };

        recognition.onerror = (event: any) => {
            // Ignore 'no-speech' error
            if (event.error !== 'no-speech') {
                console.error('Speech recognition error', event.error);
            }
            setListening(false);
        };

        recognition.onend = () => {
            setListening(false);
        };

        recognition.start();
    };

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
                <div className="flex gap-2 w-full max-w-xs justify-center items-center">
                    <div className="relative w-full group">
                        <input
                            type="text"
                            value={value}
                            onChange={(e) => setValue(e.target.value)}
                            disabled={isSubmitted && isCorrect}
                            placeholder={listening ? 'Słucham...' : (placeholder || 'Wpisz wynik...')}
                            className={classNames(
                                "w-full bg-black/30 border-2 rounded-xl px-4 py-3 text-center text-xl font-mono text-white outline-none transition-all placeholder:text-white/20",
                                isSubmitted
                                    ? (isCorrect ? "border-green-500 bg-green-500/10" : "border-red-500 bg-red-500/10")
                                    : (listening ? "border-[var(--accent-purple)] bg-black/50" : "border-white/10 focus:border-[var(--accent-blue)] focus:bg-black/50")
                            )}
                            autoComplete="off"
                        />
                        {unit && (
                            <span className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 font-mono">
                                <MathRenderer content={`$${unit}$`} inline />
                            </span>
                        )}
                    </div>

                    <button
                        type="button"
                        onClick={toggleListening}
                        disabled={isSubmitted && isCorrect}
                        className={classNames(
                            "w-12 h-[52px] flex items-center justify-center rounded-xl border-2 transition-all shrink-0",
                            listening
                                ? "bg-red-500/20 border-red-500 text-red-500 animate-pulse"
                                : "bg-white/5 border-white/10 text-white/50 hover:bg-white/10 hover:text-white hover:border-white/30"
                        )}
                        title="Wprowadź głosowo"
                    >
                        {listening ? <Loader2 size={20} className="animate-spin" /> : <Mic size={20} />}
                    </button>
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
