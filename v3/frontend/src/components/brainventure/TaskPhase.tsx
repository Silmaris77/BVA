"use client"

import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useBrainVenture } from './BrainVentureContext'
import TASKS_DATA from '@/data/brainventure/tasks.json'
import PILLS_DATA from '@/data/brainventure/pills.json'
import { TaskCard, KnowledgePill } from '@/types/brainventure'
import { Brain, Check, X, HelpCircle, ChevronRight, Clock } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

export default function TaskPhase() {
    const { state, dispatch } = useBrainVenture()
    const [task, setTask] = useState<TaskCard | null>(null)
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [answerPill, setAnswerPill] = useState<KnowledgePill | null>(null)
    const [showAnswer, setShowAnswer] = useState(false)
    const [timeLeft, setTimeLeft] = useState(180) // 3 minutes
    const [isAnswered, setIsAnswered] = useState(false)

    useEffect(() => {
        // Random task logic
        const randomTask = TASKS_DATA[Math.floor(Math.random() * TASKS_DATA.length)] as unknown as TaskCard
        setTask(randomTask)

        // Find related pill for answer key
        const pill = PILLS_DATA.find(p => p.id === randomTask.relatedPillId) as unknown as KnowledgePill
        setAnswerPill(pill)
    }, [])

    useEffect(() => {
        if (isAnswered || timeLeft <= 0) return
        const timer = setInterval(() => {
            setTimeLeft(prev => prev - 1)
        }, 1000)
        return () => clearInterval(timer)
    }, [isAnswered, timeLeft])

    const handleSelfEvaluation = (success: boolean) => {
        setIsAnswered(true)
        if (success && task) {
            dispatch({ type: 'UPDATE_KW', payload: task.rewardKW })
        }
        dispatch({ type: 'SET_PHASE_READY', payload: true })
    }

    if (!task) return <div>Ładowanie zadania...</div>

    const minutes = Math.floor(timeLeft / 60)
    const seconds = timeLeft % 60

    return (
        <div className="h-full flex flex-col items-center max-w-4xl mx-auto w-full pt-4">
            <div className="flex justify-between w-full items-center mb-6">
                <div>
                    <h2 className="text-3xl font-bold text-indigo-400">Faza 3: Zadanie (Wyzwanie)</h2>
                    <p className="text-gray-400">Masz 3 minuty na udzielenie odpowiedzi.</p>
                </div>
                <div className={`flex items-center gap-2 text-2xl font-mono font-bold ${timeLeft < 30 ? 'text-red-500 animate-pulse' : 'text-blue-300'}`}>
                    <Clock /> {minutes}:{seconds.toString().padStart(2, '0')}
                </div>
            </div>

            <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="bg-slate-800 border border-indigo-500/30 rounded-2xl p-8 w-full shadow-2xl mb-8 flex-1"
            >
                <div className="flex items-center gap-4 mb-6">
                    <div className="w-12 h-12 bg-indigo-900/50 rounded-full flex items-center justify-center text-indigo-400">
                        <HelpCircle size={28} />
                    </div>
                    <h3 className="text-xl font-bold text-white">Pytanie:</h3>
                </div>

                <p className="text-2xl font-medium text-indigo-100 leading-relaxed mb-8">
                    {task.question}
                </p>

                <div className="flex justify-center">
                    {!showAnswer ? (
                        <button
                            onClick={() => setShowAnswer(true)}
                            className="bg-indigo-600 hover:bg-indigo-500 text-white px-8 py-3 rounded-xl font-bold text-lg shadow-lg flex items-center gap-2 transition-colors"
                        >
                            Pokaż Odpowiedź (Klucz) <ChevronRight />
                        </button>
                    ) : (
                        <div className="w-full">
                            <div className="bg-slate-900/50 p-6 rounded-xl border border-slate-700 mb-8">
                                <h4 className="text-sm font-bold text-slate-400 uppercase mb-2">Wzorcowa odpowiedź (z Pigułki):</h4>
                                <div className="prose prose-invert prose-sm">
                                    <ReactMarkdown>{answerPill ? answerPill.content : "Brak danych."}</ReactMarkdown>
                                </div>
                            </div>

                            {!isAnswered && (
                                <div className="flex justify-center gap-6">
                                    <button
                                        onClick={() => handleSelfEvaluation(false)}
                                        className="flex flex-col items-center gap-2 px-8 py-4 rounded-xl bg-red-900/20 border border-red-500/50 hover:bg-red-900/40 transition-colors group"
                                    >
                                        <X size={32} className="text-red-500 group-hover:scale-110 transition-transform" />
                                        <span className="text-red-300 font-bold">Błędna / Niepełna</span>
                                    </button>

                                    <button
                                        onClick={() => handleSelfEvaluation(true)}
                                        className="flex flex-col items-center gap-2 px-8 py-4 rounded-xl bg-green-900/20 border border-green-500/50 hover:bg-green-900/40 transition-colors group"
                                    >
                                        <Check size={32} className="text-green-500 group-hover:scale-110 transition-transform" />
                                        <span className="text-green-300 font-bold">Poprawna (+{task.rewardKW} KW)</span>
                                    </button>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </motion.div>
        </div>
    )
}
