'use client';

import { useState } from 'react';
import MathRenderer from './MathRenderer';
import { Check, X } from 'lucide-react';

interface ComparisonCardProps {
    title: string;
    expression: {
        left: string;
        right: string;
        relationship: '>' | '<' | '='; // Correct answer
    };
    explanation?: string;
}

export default function ComparisonCard({ title, expression, explanation }: ComparisonCardProps) {
    const [selected, setSelected] = useState<'<' | '>' | '=' | null>(null);
    const [isSubmitted, setIsSubmitted] = useState(false);

    const isCorrect = selected === expression.relationship;

    const handleSubmit = () => {
        if (!selected) return;
        setIsSubmitted(true);
    };

    return (
        <div style={{
            maxWidth: '900px',
            width: '100%',
            position: 'relative',
            background: 'rgba(20, 20, 35, 0.6)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            border: '1px solid rgba(249, 115, 22, 0.2)', // Orange
            borderRadius: '20px',
            padding: '40px',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
            borderLeft: '4px solid #f97316',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center'
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
                color: '#f97316',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(249, 115, 22, 0.1)',
                border: '1px solid rgba(249, 115, 22, 0.2)',
                borderRadius: '20px'
            }}>
                PORÓWNAJ
            </div>

            <h2 style={{
                fontSize: '28px',
                fontWeight: 700,
                marginBottom: '40px',
                marginTop: '10px',
                color: '#f97316',
                textAlign: 'center'
            }}>
                {title}
            </h2>

            <div className="flex items-center gap-8 md:gap-12 mb-10 w-full justify-center">
                {/* Left Value */}
                <div className="text-3xl md:text-5xl font-bold font-serif min-w-[80px] text-center">
                    <MathRenderer content={expression.left} />
                </div>

                {/* Operator Selector Area */}
                <div className="flex flex-col gap-2">
                    {/* If submitted, show the result clearly */}
                    {isSubmitted ? (
                        <div className={`
                            w-16 h-16 md:w-20 md:h-20 flex items-center justify-center rounded-2xl text-4xl md:text-5xl font-bold border-2
                            ${isCorrect
                                ? 'bg-green-500/20 border-green-500 text-green-400'
                                : 'bg-red-500/20 border-red-500 text-red-400'
                            }
                         `}>
                            {selected}
                        </div>
                    ) : (
                        // Selection Mode
                        <div className="flex flex-col gap-2">
                            <div className="flex gap-2">
                                {['<', '=', '>'].map((op) => (
                                    <button
                                        key={op}
                                        onClick={() => setSelected(op as any)}
                                        className={`
                                            w-12 h-12 md:w-14 md:h-14 rounded-xl text-2xl font-bold border-2 transition-all
                                            ${selected === op
                                                ? 'bg-blue-500 text-white border-blue-500 shadow-[0_0_20px_rgba(59,130,246,0.5)]'
                                                : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10 hover:border-white/30 hover:text-white'
                                            }
                                        `}
                                    >
                                        {op}
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}
                </div>

                {/* Right Value */}
                <div className="text-3xl md:text-5xl font-bold font-serif min-w-[80px] text-center">
                    <MathRenderer content={expression.right} />
                </div>
            </div>

            {!isSubmitted && (
                <button
                    onClick={handleSubmit}
                    disabled={!selected}
                    className="w-full py-3 bg-[var(--accent-blue)] text-black font-bold rounded-xl hover:brightness-110 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    Sprawdź
                </button>
            )}

            {isSubmitted && (
                <div className="mt-2 text-center animate-in fade-in zoom-in-95 duration-300">
                    {isCorrect ? (
                        <div className="text-green-400 font-medium">
                            <Check className="inline-block mr-2" size={20} />
                            Zgadza się!
                        </div>
                    ) : (
                        <div className="text-red-400 font-medium">
                            <X className="inline-block mr-2" size={20} />
                            Niestety nie. Poprawna odpowiedź to <span className="text-white font-bold text-lg mx-1">{expression.relationship}</span>
                        </div>
                    )}

                    {explanation && (
                        <div className="mt-4 pt-4 border-t border-white/10 text-gray-300 text-sm">
                            <MathRenderer content={explanation} />
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
