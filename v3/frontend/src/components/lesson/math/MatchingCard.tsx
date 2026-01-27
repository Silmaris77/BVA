'use client';

import { useState, useEffect } from 'react';
import MathRenderer from './MathRenderer';
import { Check, X, RefreshCw } from 'lucide-react';

interface MatchingPair {
    id: string;
    left: string;
    right: string;
}

interface MatchingCardProps {
    title: string;
    question?: string;
    pairs: MatchingPair[];
    explanations?: Record<string, string>; // key: pair.id
}

function shuffleArray<T>(array: T[]): T[] {
    const newArray = [...array];
    for (let i = newArray.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
    }
    return newArray;
}

export default function MatchingCard({ title, question, pairs, explanations }: MatchingCardProps) {
    const [leftItems, setLeftItems] = useState<{ id: string, content: string }[]>([]);
    const [rightItems, setRightItems] = useState<{ id: string, content: string }[]>([]);

    const [selectedLeft, setSelectedLeft] = useState<string | null>(null);
    const [matches, setMatches] = useState<Record<string, string>>({}); // leftId -> rightId (confirmed matches)
    const [completed, setCompleted] = useState(false);
    const [wrongAttempt, setWrongAttempt] = useState<string | null>(null);

    const formatMath = (text: string) => {
        // Simple fraction detection: 1/2 -> $\frac{1}{2}$
        // Only if it doesn't look like LaTeX already
        if (text.includes('$') || text.includes('\\')) return text;
        return text.replace(/\b(\d+)\/(\d+)\b/g, '$\\frac{$1}{$2}$');
    };

    useEffect(() => {
        // Initialize and shuffle items
        const left = pairs.map(p => ({ id: p.id, content: formatMath(p.left) }));
        const right = pairs.map(p => ({ id: p.id, content: p.right })); // User asked for left, keeping right as is for now

        setLeftItems(shuffleArray(left));
        setRightItems(shuffleArray(right));
    }, [pairs]);

    const handleLeftClick = (id: string) => {
        if (matches[id]) return; // Already matched
        setSelectedLeft(id);
        setWrongAttempt(null);
    };

    const handleRightClick = (targetId: string) => {
        if (Object.values(matches).includes(targetId)) return; // Already matched
        if (!selectedLeft) return;

        // Check match
        if (selectedLeft === targetId) {
            // Correct match
            const newMatches = { ...matches, [selectedLeft]: targetId };
            setMatches(newMatches);
            setSelectedLeft(null);

            if (Object.keys(newMatches).length === pairs.length) {
                setCompleted(true);
            }
        } else {
            // Wrong match
            setWrongAttempt(targetId);
            setTimeout(() => {
                setWrongAttempt(null);
                setSelectedLeft(null);
            }, 1000);
        }
    };

    const resetGame = () => {
        setMatches({});
        setCompleted(false);
        setSelectedLeft(null);
        setWrongAttempt(null);
        // Reshuffle
        setLeftItems(shuffleArray(leftItems));
        setRightItems(shuffleArray(rightItems));
    };

    return (
        <div style={{
            maxWidth: '900px',
            width: '100%',
            position: 'relative',
            background: 'rgba(20, 20, 35, 0.6)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            border: '1px solid rgba(59, 130, 246, 0.2)',
            borderRadius: '20px',
            padding: '40px',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
            borderLeft: '4px solid #3b82f6'
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
                color: '#3b82f6',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(59, 130, 246, 0.1)',
                border: '1px solid rgba(59, 130, 246, 0.2)',
                borderRadius: '20px'
            }}>
                DOPASUJ PARY
            </div>

            {/* Title */}
            <h2 style={{
                fontSize: '28px',
                fontWeight: 700,
                marginBottom: '24px',
                marginTop: '20px',
                color: '#3b82f6',
                textAlign: 'center'
            }}>
                {title}
            </h2>

            {question && <div className="text-gray-300 text-center mb-8"><MathRenderer content={question} /></div>}

            <div className="grid grid-cols-2 gap-8 md:gap-12 relative">
                {/* Connecting Lines Layer could go here if implemented with SVG */}

                {/* Left Column */}
                <div className="flex flex-col gap-4">
                    {leftItems.map(item => {
                        const isMatched = !!matches[item.id];
                        const isSelected = selectedLeft === item.id;

                        return (
                            <button
                                key={item.id}
                                onClick={() => handleLeftClick(item.id)}
                                disabled={isMatched || completed}
                                className={`
                                    relative p-4 rounded-xl border-2 transition-all flex items-center justify-center text-center
                                    ${isMatched
                                        ? 'bg-green-500/20 border-green-500 text-green-300 opacity-60'
                                        : isSelected
                                            ? 'bg-blue-500/20 border-blue-500 text-white translate-x-2'
                                            : 'bg-black/30 border-white/10 text-gray-300 hover:bg-white/5 hover:border-white/30'
                                    }
                                `}
                            >
                                <div className="w-full flex justify-center"><MathRenderer content={item.content} className="text-2xl" /></div>
                                {isMatched && <Check size={16} className="absolute right-4" />}
                            </button>
                        );
                    })}
                </div>

                {/* Right Column */}
                <div className="flex flex-col gap-4">
                    {rightItems.map(item => {
                        const isMatched = Object.values(matches).includes(item.id);
                        const isWrong = wrongAttempt === item.id;

                        return (
                            <button
                                key={item.id}
                                onClick={() => handleRightClick(item.id)}
                                disabled={isMatched || completed}
                                className={`
                                    relative p-4 rounded-xl border-2 transition-all flex items-center justify-center text-center
                                    ${isMatched
                                        ? 'bg-green-500/20 border-green-500 text-green-300 opacity-60'
                                        : isWrong
                                            ? 'bg-red-500/20 border-red-500 text-red-300 animate-shake'
                                            : selectedLeft
                                                ? 'bg-black/30 border-white/10 text-gray-300 hover:border-blue-500/50 hover:bg-blue-500/5 cursor-pointer'
                                                : 'bg-black/30 border-white/10 text-gray-300 opacity-70 cursor-default'
                                    }
                                `}
                            >
                                <div className="w-full flex justify-center"><MathRenderer content={item.content} className="text-2xl" /></div>
                                {isMatched && <Check size={16} className="absolute right-4" />}
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* Success State */}
            {completed && (
                <div className="mt-8 text-center animate-in fade-in slide-in-from-bottom-4">
                    <div className="inline-flex items-center gap-2 px-4 py-2 bg-green-500/20 border border-green-500 rounded-full text-green-300 font-bold mb-4">
                        <Check size={18} />
                        Wszystkie pary dopasowane!
                    </div>
                    <button
                        onClick={resetGame}
                        className="flex items-center gap-2 mx-auto text-sm text-gray-400 hover:text-white transition-colors"
                    >
                        <RefreshCw size={14} />
                        Zagraj jeszcze raz
                    </button>
                </div>
            )}
        </div>
    );
}
