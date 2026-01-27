'use client'

import MathRenderer from './math/MathRenderer'
import { useState, useRef, useEffect } from 'react'
import { ChevronDown, ChevronUp, Mic, Loader2 } from 'lucide-react'

interface PracticeCardProps {
    title: string
    content: string
    keyPoints?: string[]
    actionSteps?: string[]
    // New fields for OJT lessons
    scenario?: string
    instruction?: string
    inputs?: Array<{
        label: string
        placeholder: string
        type?: 'text' | 'textarea'
    }>
    sampleAnswers?: {
        title?: string
        answers: string[]
        tip?: string
    }
}

export default function PracticeCard({ title, content, keyPoints, actionSteps, scenario, instruction, inputs, sampleAnswers }: PracticeCardProps) {
    const [inputValues, setInputValues] = useState<Record<number, string>>({})
    const [showAnswers, setShowAnswers] = useState(false)

    const handleInputChange = (index: number, value: string) => {
        setInputValues(prev => ({ ...prev, [index]: value }))
    }

    const [listeningIndex, setListeningIndex] = useState<number | null>(null)
    const [processingIndex, setProcessingIndex] = useState<number | null>(null)
    const recognitionRef = useRef<any>(null)

    const processWithAI = async (index: number, text: string) => {
        if (!text || text.trim().length < 5) return // Skip short texts

        setProcessingIndex(index)
        try {
            const response = await fetch('/api/ai/punctuate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            })

            const data = await response.json()
            if (data.text) {
                handleInputChange(index, data.text)
            }
        } catch (error) {
            console.error('AI Punctuation error:', error)
        } finally {
            setProcessingIndex(null)
        }
    }

    const toggleListening = (index: number) => {
        // If already listening on this index, stop.
        if (listeningIndex === index) {
            if (recognitionRef.current) {
                recognitionRef.current.stop()
            }
            return
        }

        // If listening elsewhere, stop that first.
        if (listeningIndex !== null) {
            if (recognitionRef.current) {
                recognitionRef.current.stop()
            }
        }

        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert('Twoja przeglądarka nie obsługuje rozpoznawania mowy.')
            return
        }

        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
        const recognition = new SpeechRecognition()
        recognitionRef.current = recognition

        recognition.lang = 'pl-PL'
        recognition.interimResults = false
        recognition.maxAlternatives = 1

        // Capture starting state to check for changes changes
        const startValue = inputValues[index] || ''
        let finalValue = startValue

        recognition.onstart = () => {
            setListeningIndex(index)
        }

        recognition.onresult = (event: any) => {
            const transcript = event.results[0][0].transcript

            // Normalize the transcript (Polish Math -> Symbols)
            let normalized = transcript.toLowerCase().trim()

            // 1. Remove fillers
            normalized = normalized.replace(/^(wynik|to|jest|odpowiedź|równa się)\s+/g, '')

            // 2. Map specific fraction words to denominators (mostly generic approach)
            // "5 szóstych" -> "5/6"
            const fractionMap: Record<string, string> = {
                'pół': '0.5',
                'połowa': '0.5',
                'ćwierć': '1/4',
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
            }

            // Word-to-digit map for small numbers often spoken as words before fractions
            // e.g. "pięć szóstych" (STT might output "pięć" instead of "5")
            const wordToDigit: Record<string, string> = {
                'zero': '0', 'jeden': '1', 'jedna': '1', 'jedno': '1',
                'dwa': '2', 'dwie': '2',
                'trzy': '3',
                'cztery': '4',
                'pięć': '5',
                'sześć': '6',
                'siedem': '7',
                'osiem': '8',
                'dziewięć': '9',
                'dziesięć': '10'
            }

            // Replace number words followed by fractions FIRST
            // e.g. "pięć szóstych" -> "5 szóstych"
            for (const [word, digit] of Object.entries(wordToDigit)) {
                const regex = new RegExp(`\\b${word}\\b`, 'gi')
                normalized = normalized.replace(regex, digit)
            }

            // Replace denominators
            for (const [word, replacement] of Object.entries(fractionMap)) {
                // Look for word boundary or typical endings
                // e.g. "szóstych"
                const regex = new RegExp(`\\b${word}\\b`, 'gi')
                normalized = normalized.replace(regex, replacement)
            }

            // 3. Basic operators
            normalized = normalized
                .replace(/\s+plus\s+/g, '+')
                .replace(/\s+minus\s+/g, '-')
                .replace(/\s+razy\s+/g, '*')
                .replace(/\s+podzielić\s+(przez\s+)?/g, '/')
                .replace(/\s+przez\s+/g, '/') // "5 przez 6" -> "5/6"
                .replace(/przecinek/g, '.')
                .replace(/kropka/g, '.')

            // 4. Cleanup spaces around slashes
            // "5 / 6" -> "5/6"
            // "5 /6" -> "5/6"
            normalized = normalized.replace(/\s*\/\s*/g, '/')

            // 5. Append or set
            // If the field was empty, just set. If not, append.
            // Check if normalized is just a math expression, if so, maybe replace?
            // For now, let's just append carefully.

            // If the user said ONLY a fraction "5/6", and the input is empty, set it.
            // If input has text, append with space.

            finalValue = startValue ? `${startValue} ${normalized}` : normalized
            handleInputChange(index, finalValue)
        }

        recognition.onend = () => {
            setListeningIndex(null)
            recognitionRef.current = null

            // logic to optional auto-punctuate if it's long text text explanation? 
            // For math inputs simpler is better.
            // Let's NOT call processWithAI for short math-like inputs.
        }

        recognition.onerror = (event: any) => {
            if (event.error !== 'no-speech') {
                console.error('Speech recognition error', event.error)
            }
            setListeningIndex(null)
            recognitionRef.current = null
        }

        recognition.start()
    }



    return (
        <div style={{
            maxWidth: '900px',
            width: '100%'
        }}>
            {/* Main Content Card */}
            <div style={{
                position: 'relative',
                background: 'rgba(20, 20, 35, 0.6)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(0, 255, 136, 0.2)',
                borderRadius: '20px',
                padding: '40px',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
                borderLeft: '4px solid #00ff88'
            }}>
                {/* Type Badge - Top Left Corner */}
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
                    color: '#00ff88',
                    fontWeight: 600,
                    padding: '6px 12px',
                    background: 'rgba(0, 255, 136, 0.1)',
                    border: '1px solid rgba(0, 255, 136, 0.2)',
                    borderRadius: '20px'
                }}>
                    PRACTICE
                </div>

                {/* Title */}
                <h2 style={{
                    fontSize: '28px',
                    fontWeight: 700,
                    marginBottom: '24px',
                    marginTop: '20px',
                    color: '#00ff88'
                }}>
                    {title}
                </h2>

                {/* Scenario (if present) */}
                {scenario && (
                    <div style={{
                        marginBottom: '20px',
                        padding: '20px',
                        background: 'rgba(255, 136, 0, 0.1)',
                        borderRadius: '12px',
                        borderLeft: '4px solid #ff8800'
                    }}>
                        <h4 style={{ color: '#ff8800', marginBottom: '10px', fontSize: '1rem', fontWeight: 600 }}>Scenariusz:</h4>
                        <div style={{ fontSize: '15px', lineHeight: '1.7', color: 'rgba(255, 255, 255, 0.9)' }}>
                            <MathRenderer content={scenario} />
                        </div>
                    </div>
                )}

                {/* Instruction (if present) */}
                {instruction && (
                    <div style={{
                        marginBottom: '20px',
                        padding: '16px',
                        background: 'rgba(0, 212, 255, 0.1)',
                        borderRadius: '8px',
                        fontSize: '15px',
                        fontWeight: 600,
                        color: '#00d4ff'
                    }}>
                        {instruction}
                    </div>
                )}

                {/* Content */}
                <div style={{
                    fontSize: '16px',
                    lineHeight: '1.8',
                    color: 'rgba(255, 255, 255, 0.9)',
                    marginBottom: keyPoints || actionSteps || inputs ? '24px' : '0'
                }}>
                    <MathRenderer content={content} />
                </div>

                {/* Interactive Inputs (if present) */}
                {inputs && inputs.length > 0 && (
                    <div style={{ marginTop: '24px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
                        {inputs.map((input, index) => (
                            <div key={index}>
                                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                                    <label style={{
                                        display: 'block',
                                        fontSize: '14px',
                                        fontWeight: 600,
                                        color: '#00ff88'
                                    }}>
                                        {input.label}
                                    </label>

                                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>


                                        {/* Speech Button */}
                                        <button
                                            onClick={() => toggleListening(index)}
                                            style={{
                                                background: listeningIndex === index ? 'rgba(239, 68, 68, 0.2)' : processingIndex === index ? 'rgba(176, 0, 255, 0.1)' : 'rgba(255, 255, 255, 0.1)',
                                                border: listeningIndex === index ? '1px solid #ef4444' : processingIndex === index ? '1px solid #b000ff' : '1px solid rgba(255, 255, 255, 0.1)',
                                                borderRadius: '50%',
                                                width: '32px',
                                                height: '32px',
                                                display: 'flex',
                                                alignItems: 'center',
                                                justifyContent: 'center',
                                                cursor: processingIndex === index ? 'wait' : 'pointer',
                                                color: listeningIndex === index ? '#ef4444' : processingIndex === index ? '#b000ff' : 'rgba(255, 255, 255, 0.7)',
                                                transition: 'all 0.2s',
                                                animation: listeningIndex === index ? 'pulse-red 1.5s infinite' : processingIndex === index ? 'pulse-purple 1.5s infinite' : 'none'
                                            }}
                                            title={listeningIndex === index ? 'Zatrzymaj nagrywanie' : 'Nagraj odpowiedź'}
                                            disabled={processingIndex === index}
                                        >
                                            {listeningIndex === index ? (
                                                <div style={{ width: '10px', height: '10px', background: 'currentColor', borderRadius: '2px' }} />
                                            ) : processingIndex === index ? (
                                                <Loader2 size={16} className="animate-spin" />
                                            ) : (
                                                <Mic size={16} />
                                            )}
                                        </button>
                                    </div>
                                </div>
                                <style>{`
                                    @keyframes pulse-red {
                                        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
                                        70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
                                        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
                                    }
                                    @keyframes pulse-purple {
                                        0% { box-shadow: 0 0 0 0 rgba(176, 0, 255, 0.4); }
                                        70% { box-shadow: 0 0 0 10px rgba(176, 0, 255, 0); }
                                        100% { box-shadow: 0 0 0 0 rgba(176, 0, 255, 0); }
                                    }
                                `}</style>

                                {input.type === 'textarea' ? (
                                    <textarea
                                        value={inputValues[index] || ''}
                                        onChange={(e) => handleInputChange(index, e.target.value)}
                                        placeholder={listeningIndex === index ? 'Słucham...' : processingIndex === index ? 'AI poprawia tekst...' : input.placeholder}
                                        style={{
                                            width: '100%',
                                            padding: '12px',
                                            background: 'rgba(0, 0, 0, 0.3)',
                                            border: listeningIndex === index ? '1px solid #ef4444' : processingIndex === index ? '1px solid #b000ff' : '1px solid rgba(0, 255, 136, 0.3)',
                                            borderRadius: '8px',
                                            color: '#fff',
                                            fontSize: '15px',
                                            fontFamily: 'inherit',
                                            resize: 'vertical',
                                            minHeight: '80px',
                                            transition: 'border 0.3s ease',
                                            opacity: processingIndex === index ? 0.7 : 1
                                        }}
                                        disabled={processingIndex === index}
                                    />
                                ) : (
                                    <input
                                        type="text"
                                        value={inputValues[index] || ''}
                                        onChange={(e) => handleInputChange(index, e.target.value)}
                                        placeholder={listeningIndex === index ? 'Słucham...' : processingIndex === index ? 'AI poprawia tekst...' : input.placeholder}
                                        style={{
                                            width: '100%',
                                            padding: '12px',
                                            background: 'rgba(0, 0, 0, 0.3)',
                                            border: listeningIndex === index ? '1px solid #ef4444' : processingIndex === index ? '1px solid #b000ff' : '1px solid rgba(0, 255, 136, 0.3)',
                                            borderRadius: '8px',
                                            color: '#fff',
                                            fontSize: '15px',
                                            fontFamily: 'inherit',
                                            transition: 'border 0.3s ease',
                                            opacity: processingIndex === index ? 0.7 : 1
                                        }}
                                        disabled={processingIndex === index}
                                    />
                                )}
                            </div>
                        ))}
                    </div>
                )}

                {/* Sample Answers (collapsible) */}
                {sampleAnswers && (
                    <div style={{ marginTop: '24px' }}>
                        <button
                            onClick={() => setShowAnswers(!showAnswers)}
                            style={{
                                width: '100%',
                                padding: '14px 20px',
                                background: 'rgba(176, 0, 255, 0.2)',
                                border: '1px solid rgba(176, 0, 255, 0.4)',
                                borderRadius: '8px',
                                color: '#b000ff',
                                fontSize: '15px',
                                fontWeight: 600,
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                gap: '8px',
                                transition: 'all 0.2s'
                            }}
                        >
                            {showAnswers ? (
                                <><ChevronUp size={20} /> Ukryj przykładowe odpowiedzi</>
                            ) : (
                                <><ChevronDown size={20} /> Pokaż przykładowe odpowiedzi</>
                            )}
                        </button>
                        {showAnswers && (
                            <div style={{
                                marginTop: '16px',
                                padding: '20px',
                                background: 'rgba(176, 0, 255, 0.1)',
                                borderRadius: '12px',
                                border: '1px solid rgba(176, 0, 255, 0.2)'
                            }}>
                                {sampleAnswers.title && (
                                    <h4 style={{ color: '#b000ff', marginBottom: '12px', fontSize: '1rem' }}>
                                        {sampleAnswers.title}
                                    </h4>
                                )}
                                <ol style={{ paddingLeft: '20px', margin: 0, display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                    {sampleAnswers.answers.map((answer, index) => (
                                        <li key={index} style={{
                                            fontSize: '15px',
                                            lineHeight: '1.7',
                                            color: 'rgba(255, 255, 255, 0.9)'
                                        }}>
                                            <MathRenderer content={answer} />
                                        </li>
                                    ))}
                                </ol>
                                {sampleAnswers.tip && (
                                    <div style={{
                                        marginTop: '16px',
                                        padding: '16px',
                                        background: 'rgba(0, 255, 136, 0.1)',
                                        borderRadius: '8px',
                                        borderLeft: '4px solid #00ff88'
                                    }}>
                                        <MathRenderer content={sampleAnswers.tip} />
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                )}

                {/* Key Points */}
                {keyPoints && keyPoints.length > 0 && (
                    <div style={{
                        marginTop: '24px',
                        padding: '20px',
                        background: 'rgba(0, 255, 136, 0.05)',
                        borderRadius: '12px',
                        border: '1px solid rgba(0, 255, 136, 0.1)'
                    }}>
                        <h4 style={{
                            fontSize: '14px',
                            fontWeight: 600,
                            marginBottom: '12px',
                            color: '#00ff88',
                            textTransform: 'uppercase',
                            letterSpacing: '0.5px'
                        }}>
                            💡 Kluczowe praktyki:
                        </h4>
                        <ul style={{
                            listStyle: 'none',
                            padding: 0,
                            margin: 0,
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '8px'
                        }}>
                            {keyPoints.map((point, index) => (
                                <li key={index} style={{
                                    display: 'flex',
                                    alignItems: 'flex-start',
                                    gap: '12px',
                                    fontSize: '15px',
                                    lineHeight: '1.6'
                                }}>
                                    <span style={{ color: '#00ff88', fontSize: '18px' }}>✓</span>
                                    <span>{point}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}

                {/* Action Steps */}
                {actionSteps && actionSteps.length > 0 && (
                    <div style={{
                        marginTop: '24px',
                        padding: '20px',
                        background: 'rgba(0, 212, 255, 0.05)',
                        borderRadius: '12px',
                        border: '1px solid rgba(0, 212, 255, 0.15)'
                    }}>
                        <h4 style={{
                            fontSize: '14px',
                            fontWeight: 600,
                            marginBottom: '12px',
                            color: '#00d4ff',
                            textTransform: 'uppercase',
                            letterSpacing: '0.5px'
                        }}>
                            🎯 Do zrobienia:
                        </h4>
                        <ol style={{
                            paddingLeft: '24px',
                            margin: 0,
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '8px'
                        }}>
                            {actionSteps.map((step, index) => (
                                <li key={index} style={{
                                    fontSize: '15px',
                                    lineHeight: '1.6',
                                    color: 'rgba(255, 255, 255, 0.9)'
                                }}>
                                    {step}
                                </li>
                            ))}
                        </ol>
                    </div>
                )}
            </div>
        </div>
    )
}
