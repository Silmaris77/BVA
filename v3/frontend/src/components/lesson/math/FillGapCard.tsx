'use client';

import { useState } from 'react';
import MathRenderer from './MathRenderer';
import { Check } from 'lucide-react';

interface Gap {
    id: string; // "gap1"
    correctRange?: { min: number, max: number };
    correctExact?: number;
    placeholder?: string;
}

interface FillGapCardProps {
    title: string;
    parts: (string | Gap)[]; // ["0 < ", {id: "gap1"}, " < 1/4"]
    explanation?: string;
}

function isGap(part: string | Gap): part is Gap {
    return typeof part !== 'string';
}

export default function FillGapCard({ title, parts, explanation }: FillGapCardProps) {
    const [values, setValues] = useState<Record<string, string>>({});
    const [isSubmitted, setIsSubmitted] = useState(false);

    // Check results
    const results = parts.filter(isGap).map(gap => {
        const valStr = values[gap.id]?.replace(',', '.') || '';
        const val = parseFloat(valStr);

        let correct = false;

        if (!isNaN(val)) {
            if (gap.correctExact !== undefined) {
                correct = Math.abs(val - gap.correctExact) < 0.0001;
            } else if (gap.correctRange) {
                correct = val > gap.correctRange.min && val < gap.correctRange.max;
            }
        }

        return { id: gap.id, correct };
    });

    const allCorrect = results.every(r => r.correct);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
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
            border: '1px solid rgba(6, 182, 212, 0.2)', // Cyan
            borderRadius: '20px',
            padding: '40px',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
            borderLeft: '4px solid #06b6d4'
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
                UZUPEŁNIJ LUKI
            </div>

            <h2 style={{
                fontSize: '28px',
                fontWeight: 700,
                marginBottom: '40px',
                marginTop: '20px',
                color: '#06b6d4',
                textAlign: 'center'
            }}>
                {title}
            </h2>

            <form onSubmit={handleSubmit}>
                <div className="flex flex-wrap items-center justify-center gap-3 text-xl md:text-2xl font-serif leading-loose">
                    {parts.map((part, index) => {
                        if (typeof part === 'string') {
                            // Check for newlines (either \n or literal \n coming from JSON)
                            const segments = part.split(/\\n|\n/);
                            return segments.map((segment, segIndex) => (
                                <span key={`${index}-${segIndex}`} className={segIndex > 0 ? "w-full text-center mt-2" : ""}>
                                    <MathRenderer content={segment} inline />
                                </span>
                            ));
                        } else {
                            const gap = part;
                            const isCorrect = results.find(r => r.id === gap.id)?.correct;

                            return (
                                <input
                                    key={gap.id}
                                    type="text"
                                    value={values[gap.id] || ''}
                                    onChange={(e) => setValues({ ...values, [gap.id]: e.target.value })}
                                    disabled={isSubmitted && isCorrect}
                                    placeholder={gap.placeholder || '?'}
                                    className={`
                                        w-20 text-center px-1 py-1 rounded-lg border-2 outline-none font-bold transition-all mx-1
                                        ${isSubmitted
                                            ? isCorrect
                                                ? 'bg-green-500/20 border-green-500 text-green-400'
                                                : 'bg-red-500/20 border-red-500 text-red-400'
                                            : 'bg-black/30 border-white/20 focus:border-blue-500 focus:bg-black/50 text-white'
                                        }
                                    `}
                                />
                            );
                        }
                    })}
                </div>

                {!isSubmitted ? (
                    <div className="mt-8 flex justify-center">
                        <button
                            type="submit"
                            disabled={Object.keys(values).length < parts.filter(isGap).length}
                            className="bg-[var(--accent-blue)] text-black px-8 py-2 rounded-lg font-bold hover:brightness-110 transition disabled:opacity-50"
                        >
                            Sprawdź
                        </button>
                    </div>
                ) : (
                    <div className="mt-8 text-center animate-in fade-in slide-in-from-bottom-2">
                        {allCorrect ? (
                            <div className="flex items-center justify-center gap-2 text-green-400 font-bold bg-green-500/10 px-4 py-2 rounded-lg border border-green-500/20 mb-4">
                                <Check size={20} /> Świetnie! Warunek spełniony.
                            </div>
                        ) : (
                            <button
                                type="button"
                                onClick={() => { setIsSubmitted(false); setValues({}); }}
                                className="text-sm text-gray-400 hover:text-white underline mb-4"
                            >
                                Spróbuj jeszcze raz
                            </button>
                        )}

                        {(allCorrect || explanation) && explanation && (
                            <div className="text-gray-300 text-sm border-t border-white/10 pt-4">
                                <MathRenderer content={explanation} />
                            </div>
                        )}
                    </div>
                )}
            </form>
        </div>
    );
}
