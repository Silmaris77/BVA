'use client';

import { useState, useRef, useEffect } from 'react';
import { Check, X, HelpCircle, MoveHorizontal } from 'lucide-react';
import MathRenderer from './MathRenderer';

interface NumberLineCardProps {
    question: string;         // e.g., "Zaznacz liczbę $1.5$"
    min: number;              // start of line, e.g. -5
    max: number;              // end of line, e.g. 5
    step?: number;            // visual tick interval, e.g. 1
    correctValue: number;     // e.g. 1.5
    tolerance?: number;       // how close to accept? default 0.1
    initialValue?: number;    // default: (min+max)/2
    explanation?: string;
}

export default function NumberLineCard({
    question, min, max, step = 1, correctValue, tolerance = 0.25, initialValue, explanation
}: NumberLineCardProps) {
    const [value, setValue] = useState(initialValue ?? (min + max) / 2);
    const [isDragging, setIsDragging] = useState(false);
    const [isSubmitted, setIsSubmitted] = useState(false);
    const [isCorrect, setIsCorrect] = useState(false);

    const trackRef = useRef<HTMLDivElement>(null);

    // Calculate precision for display based on step (if step is 0.5, show 1 decimal)
    // Calculate precision based on step
    const getPrecision = (num: number) => {
        if (!isFinite(num)) return 0;
        let e = 1, p = 0;
        while (Math.round(num * e) / e !== num) { e *= 10; p++; }
        return p;
    };

    const stepPrecision = getPrecision(step);
    // Display precision should be at least step precision, but maybe simplified for integers
    const displayPrecision = stepPrecision;

    // Generate ticks
    const ticks = [];
    const safetyLimit = 100;
    let current = min;
    let count = 0;
    // float correction loop
    while (current <= max + 0.0001 && count < safetyLimit) {
        ticks.push(current);
        current += step;
        count++;
    }

    const valueToPercent = (val: number) => ((val - min) / (max - min)) * 100;

    const handleInteract = (clientX: number) => {
        if (isSubmitted && isCorrect) return; // Locked if correct
        if (!trackRef.current) return;

        const rect = trackRef.current.getBoundingClientRect();
        const offsetX = clientX - rect.left;
        let percent = (offsetX / rect.width) * 100;

        // Clamp
        if (percent < 0) percent = 0;
        if (percent > 100) percent = 100;

        // Convert back to value
        const rawValue = min + (percent / 100) * (max - min);

        // Snap to nearest step
        // We want to snap relative to min
        const relativeValue = rawValue - min;
        const snappedRelative = Math.round(relativeValue / step) * step;
        const snappedValue = min + snappedRelative;

        // Fix floating point errors (e.g. 0.30000000004)
        const fixedValue = Number(snappedValue.toFixed(stepPrecision));

        // Clamp again to be sure
        const clampedValue = Math.max(min, Math.min(max, fixedValue));

        setValue(clampedValue);
    };

    const handleMouseDown = (e: React.MouseEvent) => {
        setIsDragging(true);
        handleInteract(e.clientX);
    };

    const handleTouchStart = (e: React.TouchEvent) => {
        setIsDragging(true);
        handleInteract(e.touches[0].clientX);
    };

    useEffect(() => {
        const handleMove = (e: MouseEvent) => {
            if (isDragging) handleInteract(e.clientX);
        };
        const handleUp = () => setIsDragging(false);

        // Touch counterparts
        const handleTouchMove = (e: TouchEvent) => {
            if (isDragging) handleInteract(e.touches[0].clientX);
        };

        if (isDragging) {
            window.addEventListener('mousemove', handleMove);
            window.addEventListener('mouseup', handleUp);
            window.addEventListener('touchmove', handleTouchMove);
            window.addEventListener('touchend', handleUp);
        }

        return () => {
            window.removeEventListener('mousemove', handleMove);
            window.removeEventListener('mouseup', handleUp);
            window.removeEventListener('touchmove', handleTouchMove);
            window.removeEventListener('touchend', handleUp);
        };
    }, [isDragging]);


    const handleSubmit = () => {
        const diff = Math.abs(value - correctValue);
        const correct = diff <= tolerance;
        setIsCorrect(correct);
        setIsSubmitted(true);
    };

    const handleRetry = () => {
        setIsSubmitted(false);
        setIsCorrect(false);
        setValue(initialValue ?? (min + max) / 2);
    };

    return (
        <div className="w-full max-w-2xl mx-auto glass-card p-8 rounded-2xl border border-white/10 relative">
            {/* Badge */}
            <div className="absolute top-4 left-4 flex items-center gap-2">
                <span className="bg-cyan-500/10 text-cyan-300 px-2 py-0.5 rounded text-[10px] font-bold uppercase border border-cyan-500/20 tracking-wider">
                    Oś Liczbowa
                </span>
            </div>

            {/* Question */}
            <div className="mt-6 mb-12 text-xl font-medium text-white text-center">
                <MathRenderer content={question} />
            </div>

            {/* The Line UI */}
            <div className="relative h-24 mb-6 select-none" ref={trackRef}>
                {/* Track Line */}
                <div className="absolute top-1/2 left-0 right-0 h-1 bg-white/20 rounded-full" />

                {/* Arrow Heads */}
                <div className="absolute top-1/2 -translate-y-1/2 -left-2 text-white/20">◀</div>
                <div className="absolute top-1/2 -translate-y-1/2 -right-2 text-white/20">▶</div>

                {/* Ticks */}
                {ticks.map((tickVal) => {
                    const pct = valueToPercent(tickVal);
                    // Determine if major or minor tick (integers are major)
                    const isMajor = Number.isInteger(tickVal);

                    return (
                        <div
                            key={tickVal.toFixed(2)}
                            className="absolute top-1/2 -translate-y-1/2 flex flex-col items-center gap-3 transition-all"
                            style={{ left: `${pct}%` }}
                        >
                            {/* Tick mark */}
                            <div className={`w-[2px] bg-white/30 rounded-full ${isMajor ? 'h-4' : 'h-2'}`} />

                            {/* Tick Label */}
                            {isMajor && (
                                <span className="text-xs text-gray-400 font-mono translate-y-4">
                                    {tickVal}
                                </span>
                            )}
                        </div>
                    );
                })}

                {/* Correct Answer MARKER (Shown on Submit + Correct or Give Up) */}
                {/* Let's show it only if user is correct or maybe after fail? For now, keep it hidden until correct. */}
                {isSubmitted && isCorrect && (
                    <div
                        className="absolute top-1/2 -translate-y-1/2 z-10 flex flex-col items-center animate-in fade-in zoom-in"
                        style={{ left: `${valueToPercent(correctValue)}%` }}
                    >
                        <div className="w-4 h-4 rounded-full bg-green-500 shadow-[0_0_15px_rgba(0,255,100,0.5)] border-2 border-white" />
                    </div>
                )}

                {/* Draggable Handle (User Cursor) */}
                <div
                    className={`absolute top-1/2 -translate-y-1/2 z-20 -ml-3 cursor-grab active:cursor-grabbing group`}
                    style={{ left: `${valueToPercent(value)}%` }}
                    onMouseDown={handleMouseDown}
                    onTouchStart={handleTouchStart}
                >
                    {/* Tooltip Value Bubble */}
                    <div className="absolute -top-10 left-1/2 -translate-x-1/2 bg-[var(--accent-blue)] text-black font-bold text-xs px-2 py-1 rounded opacity-100 shadow-lg pointer-events-none whitespace-nowrap">
                        {value.toFixed(displayPrecision)}
                        <div className="absolute bottom-[-4px] left-1/2 -translate-x-1/2 w-2 h-2 bg-[var(--accent-blue)] rotate-45" />
                    </div>

                    <div className={`w-6 h-6 rounded-full border-2 shadow-lg transition-transform hover:scale-110 ${isDragging ? 'bg-white border-[var(--accent-blue)] scale-110'
                        : isSubmitted
                            ? (isCorrect ? 'bg-green-500 border-green-300' : 'bg-red-500 border-red-300')
                            : 'bg-[var(--accent-blue)] border-white'
                        }`}>
                        <div className="absolute inset-0 flex items-center justify-center">
                            <MoveHorizontal size={12} className="text-black/50" />
                        </div>
                    </div>
                </div>

                {/* Interact Layer (Invisible wide hit area) */}
                <div
                    className="absolute inset-x-0 -top-4 -bottom-4 cursor-pointer z-0"
                    onMouseDown={handleMouseDown}
                    onTouchStart={handleTouchStart}
                />
            </div>

            {/* Controls */}
            <div className="flex flex-col items-center gap-4 mt-8">
                {!isSubmitted ? (
                    <button
                        onClick={handleSubmit}
                        className="bg-white/10 hover:bg-white/20 text-white font-bold px-8 py-2 rounded-lg border border-white/20 transition flex items-center gap-2"
                    >
                        Zatwierdź
                    </button>
                ) : (
                    <div className="animate-in fade-in slide-in-from-bottom-2 flex flex-col items-center gap-4">
                        {isCorrect ? (
                            <div className="flex items-center gap-2 text-green-400 font-bold bg-green-500/10 px-4 py-2 rounded-lg border border-green-500/20">
                                <Check size={20} /> Dobrze! Odległość poprawna.
                            </div>
                        ) : (
                            <div className="flex flex-col items-center gap-2">
                                <div className="flex items-center gap-2 text-red-400 font-bold bg-red-500/10 px-4 py-2 rounded-lg border border-red-500/20">
                                    <X size={20} /> Trochę za daleko.
                                </div>
                                <button
                                    onClick={handleRetry}
                                    className="text-xs text-gray-400 hover:text-white underline"
                                >
                                    Spróbuj ponownie
                                </button>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Explanation */}
            {isSubmitted && (isCorrect || explanation) && (
                <div className="mt-6 pt-6 border-t border-white/5 text-sm text-gray-300">
                    <p className="font-bold text-gray-400 mb-1 flex items-center gap-2">
                        <HelpCircle size={14} /> Wyjaśnienie:
                    </p>
                    <MathRenderer content={explanation || `Szukana liczba to **${correctValue}**.`} />
                </div>
            )}

        </div>
    )
}
