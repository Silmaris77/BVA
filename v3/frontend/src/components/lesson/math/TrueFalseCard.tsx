'use client';

import { useState } from 'react';
import MathRenderer from './MathRenderer';
import { Check, X } from 'lucide-react';

interface Statement {
    id: string;
    text: string;
    isTrue: boolean;
    explanation?: string;
}

interface TrueFalseCardProps {
    title: string;
    question?: string;
    statements: Statement[];
}

export default function TrueFalseCard({ title, question, statements }: TrueFalseCardProps) {
    const [answers, setAnswers] = useState<Record<string, boolean | null>>({}); // id -> true/false/null
    const [isSubmitted, setIsSubmitted] = useState(false);

    const handleSelect = (id: string, value: boolean) => {
        if (isSubmitted) return;
        setAnswers(prev => ({
            ...prev,
            [id]: value
        }));
    };

    const checkAnswers = () => {
        // Check if all answered
        if (Object.keys(answers).length < statements.length) return;
        setIsSubmitted(true);
    };

    const allCorrect = statements.every(s => answers[s.id] === s.isTrue);
    const score = statements.reduce((acc, s) => acc + (answers[s.id] === s.isTrue ? 1 : 0), 0);

    return (
        <div style={{
            maxWidth: '900px',
            width: '100%',
            position: 'relative',
            background: 'rgba(20, 20, 35, 0.6)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            border: '1px solid rgba(168, 85, 247, 0.2)', // Purple
            borderRadius: '20px',
            padding: '40px',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
            borderLeft: '4px solid #a855f7'
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
                color: '#a855f7',
                fontWeight: 600,
                padding: '6px 12px',
                background: 'rgba(168, 85, 247, 0.1)',
                border: '1px solid rgba(168, 85, 247, 0.2)',
                borderRadius: '20px'
            }}>
                PRAWDA CZY FAŁSZ
            </div>

            <h2 style={{
                fontSize: '28px',
                fontWeight: 700,
                marginBottom: '24px',
                marginTop: '20px',
                color: '#a855f7'
            }}>
                {title}
            </h2>
            {question && <p className="text-gray-300 mb-6">{question}</p>}

            <div className="flex flex-col gap-4">
                {statements.map((stmt) => {
                    const userAnswer = answers[stmt.id];
                    const isCorrect = isSubmitted && userAnswer === stmt.isTrue;
                    const isWrong = isSubmitted && userAnswer !== stmt.isTrue;

                    return (
                        <div
                            key={stmt.id}
                            className={`
                                relative p-4 rounded-xl border transition-all
                                ${isSubmitted
                                    ? isCorrect
                                        ? 'bg-green-500/10 border-green-500/30'
                                        : 'bg-red-500/10 border-red-500/30'
                                    : 'bg-black/20 border-white/5 hover:bg-black/30'
                                }
                            `}
                        >
                            <div className="flex items-start justify-between gap-4">
                                <div className="flex-1 text-base text-gray-200 pt-1">
                                    <MathRenderer content={stmt.text} />
                                </div>

                                <div className="flex gap-2 shrink-0">
                                    <button
                                        onClick={() => handleSelect(stmt.id, true)}
                                        disabled={isSubmitted}
                                        className={`
                                            px-3 py-1 rounded text-sm font-bold border transition-all
                                            ${userAnswer === true
                                                ? 'bg-green-500 text-black border-green-500'
                                                : 'bg-transparent text-gray-400 border-gray-600 hover:border-green-500 hover:text-green-500'
                                            }
                                            ${isSubmitted && 'opacity-50 cursor-not-allowed'}
                                        `}
                                    >
                                        PRAWDA
                                    </button>
                                    <button
                                        onClick={() => handleSelect(stmt.id, false)}
                                        disabled={isSubmitted}
                                        className={`
                                            px-3 py-1 rounded text-sm font-bold border transition-all
                                            ${userAnswer === false
                                                ? 'bg-red-500 text-white border-red-500'
                                                : 'bg-transparent text-gray-400 border-gray-600 hover:border-red-500 hover:text-red-500'
                                            }
                                            ${isSubmitted && 'opacity-50 cursor-not-allowed'}
                                        `}
                                    >
                                        FAŁSZ
                                    </button>
                                </div>
                            </div>

                            {/* Explanation */}
                            {isSubmitted && stmt.explanation && (
                                <div className="mt-3 text-sm text-gray-400 border-t border-white/5 pt-2">
                                    <strong className={isCorrect ? "text-green-400" : "text-red-400"}>
                                        {isCorrect ? "Dobrze!" : "Błąd."}
                                    </strong>{" "}
                                    <MathRenderer content={stmt.explanation} />
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>

            {!isSubmitted && (
                <button
                    onClick={checkAnswers}
                    disabled={Object.keys(answers).length < statements.length}
                    className="mt-8 w-full py-3 bg-[var(--accent-blue)] text-black font-bold rounded-xl hover:brightness-110 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    Sprawdź odpowiedzi
                </button>
            )}

            {isSubmitted && allCorrect && (
                <div className="mt-6 flex items-center justify-center gap-2 text-green-400 font-bold bg-green-500/10 p-4 rounded-xl border border-green-500/20">
                    <Check size={24} />
                    Brawo! Wszystkie odpowiedzi poprawne.
                </div>
            )}
        </div>
    );
}
