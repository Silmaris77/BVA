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

            // 2. Improved Polish math mapping
            // 2. Improved Polish math mapping

            const fractionMap: Record<string, string> = {
                'pół': '0.5', 'połowa': '0.5', 'ćwierć': '1/4',
                'drugich': '/2', 'druga': '/2', 'drugie': '/2',
                'trzecich': '/3', 'trzecia': '/3', 'trzecie': '/3',
                'czwartych': '/4', 'czwarta': '/4', 'czwarte': '/4',
                'piątych': '/5', 'piąta': '/5', 'piąte': '/5',
                'szóstych': '/6', 'szósta': '/6', 'szóste': '/6',
                'siódmych': '/7', 'siódma': '/7', 'siódme': '/7',
                'ósmych': '/8', 'ósma': '/8', 'ósme': '/8',
                'dziewiątych': '/9', 'dziewiąta': '/9', 'dziewiąte': '/9',
                'dziesiątych': '/10', 'dziesiąta': '/10', 'dziesiąte': '/10',
                'dwunastych': '/12', 'dwunasta': '/12', 'dwunaste': '/12',
                'setnych': '/100', 'setna': '/100', 'setne': '/100',
            };

            const wordToDigit: Record<string, string> = {
                'zero': '0', 'jeden': '1', 'jedna': '1', 'jedno': '1',
                'dwa': '2', 'dwie': '2', 'trzy': '3', 'cztery': '4',
                'pięć': '5', 'sześć': '6', 'siedem': '7', 'osiem': '8', 'dziewięć': '9', 'dziesięć': '10'
            };

            // Replace number words first
            for (const [word, digit] of Object.entries(wordToDigit)) {
                processed = processed.replace(new RegExp(`\\b${word}\\b`, 'gi'), digit);
            }

            // Replace denominators
            for (const [word, replacement] of Object.entries(fractionMap)) {
                processed = processed.replace(new RegExp(`\\b${word}\\b`, 'gi'), replacement);
            }

            // Basic operators
            processed = processed
                .replace(/\s+plus\s+/g, '+')
                .replace(/\s+minus\s+/g, '-')
                .replace(/\s+razy\s+/g, '*')
                .replace(/\s+podzielić\s+(przez\s+)?/g, '/')
                .replace(/\s+przez\s+/g, '/')
                .replace(/przecinek/g, '.')
                .replace(/kropka/g, '.');

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
        <div style={{
            maxWidth: '900px',
            width: '100%',
            position: 'relative',
            background: 'rgba(20, 20, 35, 0.6)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            border: '1px solid rgba(6, 182, 212, 0.2)', // Cyan
            borderRadius: '20px',
            padding: '40px',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
            borderLeft: '4px solid #06b6d4',
            margin: '0 auto'
        }}>
            {/* Badge */}
            <div style={{
                position: 'absolute',
                top: '20px',
                left: '20px',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                fontSize: '11px',
                textTransform: 'uppercase',
                letterSpacing: '1px',
                color: '#06b6d4',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(6, 182, 212, 0.1)',
                border: '1px solid rgba(6, 182, 212, 0.2)',
                borderRadius: '20px'
            }}>
                ZADANIE
            </div>

            {/* Question */}
            <div className="mt-8 mb-8 text-xl md:text-2xl font-medium text-white text-center">
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
