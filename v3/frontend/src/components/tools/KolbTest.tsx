'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { ChevronRight, RefreshCw, CheckCircle, Info } from 'lucide-react'
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts'


const questions = [
    {
        id: 1,
        question: "Kiedy uczę się czegoś nowego, najlepiej mi się pracuje gdy:",
        options: {
            "CE": "Angażuję się osobiście i uczę się przez doświadczenie",
            "RO": "Mam czas na obserwację i refleksję",
            "AC": "Mogę analizować i tworzyć logiczne teorie",
            "AE": "Mogę aktywnie testować i eksperymentować"
        }
    },
    {
        id: 2,
        question: "W procesie uczenia się najbardziej cenię:",
        options: {
            "CE": "Konkretne przykłady i osobiste doświadczenia",
            "RO": "Możliwość przemyślenia i obserwacji",
            "AC": "Abstrakcyjne koncepcje i modele teoretyczne",
            "AE": "Praktyczne zastosowania i działanie"
        }
    },
    {
        id: 3,
        question: "Podczas rozwiązywania problemów:",
        options: {
            "CE": "Polegam na intuicji i uczuciach",
            "RO": "Słucham różnych perspektyw i zbieramy informacje",
            "AC": "Analizuję logicznie i systematycznie",
            "AE": "Testuję różne rozwiązania w praktyce"
        }
    },
    {
        id: 4,
        question: "W zespole najlepiej funkcjonuję jako:",
        options: {
            "CE": "Osoba, która wnosi osobiste zaangażowanie i empatię",
            "RO": "Obserwator, który dostrzega różne perspektywy",
            "AC": "Analityk, który tworzy strategie i plany",
            "AE": "Praktyk, który wdraża i koordynuje działania"
        }
    },
    {
        id: 5,
        question: "Podczas szkolenia/warsztatu najbardziej odpowiada mi:",
        options: {
            "CE": "Osobiste zaangażowanie i doświadczenie sytuacji",
            "RO": "Czas na dyskusję i przemyślenie tematu",
            "AC": "Solidne podstawy teoretyczne i modele",
            "AE": "Praktyczne ćwiczenia i testowanie umiejętności"
        }
    },
    {
        id: 6,
        question: "Podejmuję decyzje głównie na podstawie:",
        options: {
            "CE": "Osobistych wartości i bezpośredniego doświadczenia",
            "RO": "Obserwacji sytuacji i przemyśleń",
            "AC": "Logicznej analizy i racjonalnych przesłanek",
            "AE": "Praktycznych testów i sprawdzania w działaniu"
        }
    },
    {
        id: 7,
        question: "W sytuacji nowej/stresowej:",
        options: {
            "CE": "Kieruję się emocjami i bezpośrednim odczuciem",
            "RO": "Wycofuję się i najpierw obserwuję",
            "AC": "Szukam racjonalnych wyjaśnień i teorii",
            "AE": "Działam szybko i sprawdzam co zadziała"
        }
    },
    {
        id: 8,
        question: "Moja największa mocna strona to:",
        options: {
            "CE": "Empatia i wrażliwość na ludzi",
            "RO": "Umiejętność słuchania i refleksji",
            "AC": "Zdolności analityczne i logiczne myślenie",
            "AE": "Praktyczność i skuteczność działania"
        }
    },
    {
        id: 9,
        question: "Przy nauce nowego narzędzia/programu:",
        options: {
            "CE": "Eksperymentuję swobodnie i uczę się przez próby",
            "RO": "Obserwuję innych i czytam opinie",
            "AC": "Czytam dokumentację i poznaję strukturę",
            "AE": "Od razu zaczynam używać i testuję funkcje"
        }
    },
    {
        id: 10,
        question: "W projektach zawodowych najbardziej lubię:",
        options: {
            "CE": "Pracę z ludźmi i budowanie relacji",
            "RO": "Analizowanie danych i integrację różnych perspektyw",
            "AC": "Tworzenie strategii i systemów",
            "AE": "Realizację konkretnych zadań i wdrażanie"
        }
    },
    {
        id: 11,
        question: "Najlepiej pamiętam, gdy:",
        options: {
            "CE": "Czuję emocjonalne połączenie z tematem",
            "RO": "Mam czas na obserwację i rozważanie",
            "AC": "Rozumiem logikę i teorię stojącą za tym",
            "AE": "Praktykuję i wielokrotnie testuję"
        }
    },
    {
        id: 12,
        question: "Mój naturalny sposób działania to:",
        options: {
            "CE": "Spontaniczne reagowanie na sytuacje",
            "RO": "Cierpliwe obserwowanie przed działaniem",
            "AC": "Systematyczne planowanie i analizowanie",
            "AE": "Szybkie podejmowanie decyzji i działanie"
        }
    }
]

type AnswerType = 'CE' | 'RO' | 'AC' | 'AE'

interface KolbResult {
    dominantStyle: string
    description: string
    details: string
    strengths: string[]
    scores: {
        CE: number
        RO: number
        AC: number
        AE: number
    }
}

export default function KolbTest({ initialResult, lastCompletedAt }: { initialResult?: any; lastCompletedAt?: string }) {
    const [started, setStarted] = useState(false)
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
    const [answers, setAnswers] = useState<Record<number, AnswerType>>({})

    // Initialize result from saved data if available
    const [result, setResult] = useState<KolbResult | null>(() => {
        if (initialResult) return initialResult;
        return null;
    });

    const handleAnswer = (option: AnswerType) => {
        const newAnswers = { ...answers, [questions[currentQuestionIndex].id]: option }
        setAnswers(newAnswers)

        if (currentQuestionIndex < questions.length - 1) {
            setTimeout(() => {
                setCurrentQuestionIndex(currentQuestionIndex + 1)
            }, 300)
        } else {
            calculateResult(newAnswers)
        }
    }

    const calculateResult = (finalAnswers: Record<number, AnswerType>) => {
        const scores = { CE: 0, RO: 0, AC: 0, AE: 0 }

        Object.values(finalAnswers).forEach(answer => {
            scores[answer]++
        })

        // Obliczanie wymiarów
        const ac_ce = scores.AC - scores.CE
        const ae_ro = scores.AE - scores.RO

        let dominantStyle = ''
        let description = ''
        let details = ''
        let strengths: string[] = []

        if (ac_ce > 0 && ae_ro > 0) {
            dominantStyle = "Konwergent (Decyzyjny)"
            description = "Łączysz teoretyczne myślenie z praktycznym działaniem."
            details = "Jesteś świetny w znajdowaniu praktycznych zastosowań dla idei i teorii. Wolisz zadania techniczne i rozwiązywanie konkretnych problemów niż zagadnienia społeczne czy interpersonalne."
            strengths = ["Rozwiązywanie problemów", "Podejmowanie decyzji", "Logiczne myślenie", "Definiowanie problemów"]
        } else if (ac_ce > 0 && ae_ro <= 0) {
            dominantStyle = "Asymilator (Teoretyk)"
            description = "Łączysz teoretyczne myślenie z refleksyjną obserwacją."
            details = "Najlepiej uczysz się, analizując i organizując informacje. Potrafisz zrozumieć szeroki zakres informacji i syntetyzować je w logiczną, zwięzłą formę. Mniej interesują Cię ludzie, a bardziej abstrakcyjne koncepcje."
            strengths = ["Planowanie", "Tworzenie modeli", "Definiowanie problemów", "Rozwijanie teorii"]
        } else if (ac_ce <= 0 && ae_ro > 0) {
            dominantStyle = "Akomodator (Działacz)"
            description = "Łączysz konkretne doświadczenie z aktywnym eksperymentowaniem."
            details = "Jesteś 'człowiekiem czynu'. Lubisz robić rzeczy, realizować plany i angażować się w nowe wyzwania. Często działasz na podstawie intuicji ('przeczucia') raczej niż logicznej analizy. W rozwiązywaniu problemów polegasz na innych ludziach."
            strengths = ["Działanie", "Inicjowanie", "Przewodzenie", "Podejmowanie ryzyka"]
        } else {
            dominantStyle = "Dywergent (Obserwator)"
            description = "Łączysz konkretne doświadczenie z refleksyjną obserwacją."
            details = "Masz dużą wyobraźnię i potrafisz spojrzeć na sytuacje z wielu perspektyw. Jesteś wrażliwy na uczucia i zainteresowany ludźmi. Preferujesz obserwację niż działanie. Świetnie radzisz sobie w sytuacjach wymagających generowania pomysłów (burza mózgów)."
            strengths = ["Wyobraźnia", "Burza mózgów", "Słuchanie", "Otwartość na innych"]
        }

        const finalResult = {
            dominantStyle,
            description,
            details,
            strengths,
            scores
        };

        setResult(finalResult)
        saveResult(finalResult)
    }

    const saveResult = async (resultData: KolbResult) => {
        try {
            const response = await fetch('/api/tools/kolb-test/complete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    input_data: {},
                    output_data: resultData,
                    xp_awarded: 100
                })
            });

            if (!response.ok) {
                if (response.status === 401) {
                    alert("Twój wynik nie został zapisany. Zaloguj się, aby śledzić postępy!");
                } else {
                    console.error('Failed to save Kolb result', response.status);
                    alert("Wystąpił błąd podczas zapisywania wyniku.");
                }
            }
        } catch (error) {
            console.error('Error saving Kolb result:', error);
        }
    }

    const resetTest = () => {
        setStarted(false)
        setCurrentQuestionIndex(0)
        setAnswers({})
        setResult(null)
    }

    if (result) {
        const chartData = [
            { subject: 'CE (Czucie)', A: result.scores.CE, fullMark: 12 },
            { subject: 'RO (Obserwacja)', A: result.scores.RO, fullMark: 12 },
            { subject: 'AC (Myślenie)', A: result.scores.AC, fullMark: 12 },
            { subject: 'AE (Działanie)', A: result.scores.AE, fullMark: 12 },
        ]

        return (
            <div style={{ maxWidth: '800px', margin: '0 auto', color: 'white' }}>
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    style={{
                        background: 'rgba(255, 255, 255, 0.05)',
                        borderRadius: '24px',
                        padding: '40px',
                        textAlign: 'center'
                    }}
                >
                    <div style={{
                        width: '80px',
                        height: '80px',
                        background: 'linear-gradient(135deg, #00C6FF 0%, #0072FF 100%)',
                        borderRadius: '50%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '40px',
                        margin: '0 auto 24px auto'
                    }}>
                        🎓
                    </div>

                    <h2 style={{ fontSize: '32px', marginBottom: '8px' }}>Twój Styl Uczenia się:</h2>
                    <h1 style={{ fontSize: '48px', background: 'linear-gradient(to right, #00C6FF, #0072FF)', backgroundClip: 'text', WebkitBackgroundClip: 'text', color: 'transparent', fontWeight: 800, marginBottom: '24px' }}>
                        {result.dominantStyle}
                    </h1>

                    <div style={{ width: '100%', height: '300px', marginBottom: '32px' }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
                                <PolarGrid stroke="rgba(255,255,255,0.2)" />
                                <PolarAngleAxis dataKey="subject" tick={{ fill: 'white', fontSize: 12 }} />
                                <PolarRadiusAxis angle={30} domain={[0, 12]} tick={false} axisLine={false} />
                                <Radar
                                    name="Twój Wynik"
                                    dataKey="A"
                                    stroke="#00C6FF"
                                    strokeWidth={3}
                                    fill="#00C6FF"
                                    fillOpacity={0.3}
                                />
                            </RadarChart>
                        </ResponsiveContainer>
                    </div>

                    <p style={{ fontSize: '20px', lineHeight: 1.6, color: 'rgba(255,255,255,0.9)', marginBottom: '32px' }}>
                        {result.description}
                    </p>

                    <div style={{
                        background: 'rgba(0,0,0,0.2)',
                        padding: '24px',
                        borderRadius: '16px',
                        textAlign: 'left',
                        marginBottom: '32px'
                    }}>
                        <h4 style={{ color: '#00C6FF', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <Info size={18} /> Szczegółowy opis
                        </h4>
                        <p style={{ lineHeight: 1.6, color: 'rgba(255,255,255,0.7)' }}>
                            {result.details}
                        </p>
                    </div>

                    <div style={{ textAlign: 'left', marginBottom: '40px' }}>
                        <h4 style={{ marginBottom: '16px' }}>Twoje Mocne Strony:</h4>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px' }}>
                            {result.strengths.map(str => (
                                <div key={str} style={{
                                    background: 'rgba(255,255,255,0.05)',
                                    padding: '12px 16px',
                                    borderRadius: '12px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '10px'
                                }}>
                                    <CheckCircle size={16} color="#00C6FF" />
                                    {str}
                                </div>
                            ))}
                        </div>
                    </div>

                    <button
                        onClick={resetTest}
                        style={{
                            background: 'transparent',
                            border: '1px solid rgba(255,255,255,0.2)',
                            color: 'white',
                            padding: '12px 24px',
                            borderRadius: '12px',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            margin: '0 auto',
                            fontSize: '14px'
                        }}
                    >
                        <RefreshCw size={16} /> Rozwiąż ponownie
                    </button>
                    {lastCompletedAt && (
                        <p style={{ textAlign: 'center', marginTop: '16px', fontSize: '13px', color: 'rgba(255,255,255,0.6)' }}>
                            Ostatnio ukończono: {new Date(lastCompletedAt).toLocaleDateString('pl-PL', {
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric',
                                hour: '2-digit',
                                minute: '2-digit'
                            })}
                        </p>
                    )}
                </motion.div>
            </div>
        )
    }

    if (!started) {
        return (
            <div style={{ maxWidth: '800px', margin: '0 auto', color: 'white' }}>
                <div style={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    borderRadius: '24px',
                    padding: '40px',
                    textAlign: 'center',
                    marginBottom: '32px'
                }}>
                    <div style={{ fontSize: '64px', marginBottom: '16px' }}>🎓</div>
                    <h1 style={{ fontSize: '32px', marginBottom: '16px', fontWeight: 800 }}>
                        Teoria Uczenia się przez Doświadczenie
                    </h1>
                    <p style={{ fontSize: '18px', lineHeight: 1.6, maxWidth: '600px', margin: '0 auto', opacity: 0.9 }}>
                        Teoria Davida Kolba definiuje uczenie się jako dynamiczny proces,
                        w którym wiedza jest tworzona poprzez transformację doświadczenia.
                        Rozwiąż test (12 pytań), aby poznać swój unikalny styl.
                    </p>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
                    <div style={{ background: 'rgba(255,255,255,0.05)', padding: '24px', borderRadius: '16px', backdropFilter: 'blur(10px)' }}>
                        <h3 style={{ color: '#E74C3C', marginBottom: '8px' }}>1. Konkretne Doświadczenie</h3>
                        <p style={{ fontSize: '14px', opacity: 0.7 }}>Uczenie się przez czucie i osobiste doświadczanie sytuacji (Feeling).</p>
                    </div>
                    <div style={{ background: 'rgba(255,255,255,0.05)', padding: '24px', borderRadius: '16px', backdropFilter: 'blur(10px)' }}>
                        <h3 style={{ color: '#4A90E2', marginBottom: '8px' }}>2. Refleksyjna Obserwacja</h3>
                        <p style={{ fontSize: '14px', opacity: 0.7 }}>Uczenie się przez obserwację i przemyślenia (Watching).</p>
                    </div>
                    <div style={{ background: 'rgba(255,255,255,0.05)', padding: '24px', borderRadius: '16px', backdropFilter: 'blur(10px)' }}>
                        <h3 style={{ color: '#9B59B6', marginBottom: '8px' }}>3. Abstrakcyjna Konceptualizacja</h3>
                        <p style={{ fontSize: '14px', opacity: 0.7 }}>Uczenie się przez myślenie i analizę teoretyczną (Thinking).</p>
                    </div>
                    <div style={{ background: 'rgba(255,255,255,0.05)', padding: '24px', borderRadius: '16px', backdropFilter: 'blur(10px)' }}>
                        <h3 style={{ color: '#2ECC71', marginBottom: '8px' }}>4. Aktywne Eksperymentowanie</h3>
                        <p style={{ fontSize: '14px', opacity: 0.7 }}>Uczenie się przez działanie i testowanie w praktyce (Doing).</p>
                    </div>
                </div>

                <div style={{ textAlign: 'center', marginTop: '48px' }}>
                    <button
                        onClick={() => setStarted(true)}
                        style={{
                            background: 'white',
                            color: 'black',
                            border: 'none',
                            padding: '16px 48px',
                            borderRadius: '50px',
                            fontSize: '18px',
                            fontWeight: 700,
                            cursor: 'pointer',
                            boxShadow: '0 4px 20px rgba(0,0,0,0.3)',
                            transition: 'transform 0.2s',
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '12px'
                        }}
                    >
                        {result ? 'Rozwiąż ponownie' : 'Rozpocznij Test'} <ChevronRight />
                    </button>
                    {result && lastCompletedAt && (
                        <p style={{ marginTop: '16px', fontSize: '13px', color: 'rgba(255,255,255,0.6)', textAlign: 'center' }}>
                            Ostatnio ukończono: {new Date(lastCompletedAt).toLocaleDateString('pl-PL', {
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric',
                                hour: '2-digit',
                                minute: '2-digit'
                            })}
                        </p>
                    )}
                </div>
            </div>
        )
    }

    const currentQ = questions[currentQuestionIndex]

    return (
        <div style={{ maxWidth: '700px', margin: '0 auto', minHeight: '600px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <div style={{ marginBottom: '32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: 'rgba(255,255,255,0.5)' }}>
                <span>Pytanie {currentQuestionIndex + 1} z {questions.length}</span>
                <span>{Math.round(((currentQuestionIndex) / questions.length) * 100)}% ukończono</span>
            </div>

            <div style={{ height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px', marginBottom: '40px', overflow: 'hidden' }}>
                <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${((currentQuestionIndex) / questions.length) * 100}%` }}
                    style={{ height: '100%', background: '#00C6FF' }}
                />
            </div>

            <motion.div
                key={currentQ.id}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
            >
                <h2 style={{ fontSize: '24px', fontWeight: 600, color: 'white', marginBottom: '32px', lineHeight: 1.4 }}>
                    {currentQ.question}
                </h2>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    {Object.entries(currentQ.options).map(([key, text]) => (
                        <button
                            key={key}
                            onClick={() => handleAnswer(key as AnswerType)}
                            style={{
                                textAlign: 'left',
                                padding: '20px 24px',
                                background: answers[currentQ.id] === key ? 'rgba(0, 198, 255, 0.15)' : 'rgba(255, 255, 255, 0.05)',
                                border: answers[currentQ.id] === key ? '1px solid #00C6FF' : '1px solid rgba(255, 255, 255, 0.1)',
                                borderRadius: '16px',
                                color: 'white',
                                fontSize: '16px',
                                cursor: 'pointer',
                                transition: 'all 0.2s',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '16px'
                            }}
                        >
                            <div style={{
                                width: '24px',
                                height: '24px',
                                borderRadius: '50%',
                                border: answers[currentQ.id] === key ? '6px solid #00C6FF' : '2px solid rgba(255,255,255,0.3)',
                                flexShrink: 0
                            }} />
                            {text}
                        </button>
                    ))}
                </div>
            </motion.div>
        </div>
    )
}
