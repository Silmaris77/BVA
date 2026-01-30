import { useState, useRef, useEffect, useCallback } from 'react'

interface UseSpeechRecognitionProps {
    onResult: (transcript: string) => void
    lang?: string
}

export function useSpeechRecognition({ onResult, lang = 'pl-PL' }: UseSpeechRecognitionProps) {
    const [isListening, setIsListening] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const recognitionRef = useRef<any>(null)

    const startListening = useCallback(() => {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            setError('Twoja przeglądarka nie obsługuje rozpoznawania mowy.')
            return
        }

        try {
            const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
            const recognition = new SpeechRecognition()
            recognitionRef.current = recognition

            recognition.lang = lang
            recognition.interimResults = false
            recognition.maxAlternatives = 1

            recognition.onstart = () => {
                setIsListening(true)
                setError(null)
            }

            recognition.onresult = (event: any) => {
                const transcript = event.results[0][0].transcript
                if (transcript) {
                    onResult(transcript)
                }
            }

            recognition.onend = () => {
                setIsListening(false)
            }

            recognition.onerror = (event: any) => {
                if (event.error !== 'no-speech') {
                    console.error('Speech recognition error', event.error)
                    setError(event.error)
                }
                setIsListening(false)
            }

            recognition.start()
        } catch (err) {
            console.error('Failed to start speech recognition', err)
            setError(String(err))
            setIsListening(false)
        }
    }, [lang, onResult])

    const stopListening = useCallback(() => {
        if (recognitionRef.current) {
            recognitionRef.current.stop()
            recognitionRef.current = null
        }
        setIsListening(false)
    }, [])

    const toggleListening = useCallback(() => {
        if (isListening) {
            stopListening()
        } else {
            startListening()
        }
    }, [isListening, startListening, stopListening])

    // Cleanup
    useEffect(() => {
        return () => {
            if (recognitionRef.current) {
                recognitionRef.current.stop()
            }
        }
    }, [])

    return {
        isListening,
        error,
        startListening,
        stopListening,
        toggleListening
    }
}
