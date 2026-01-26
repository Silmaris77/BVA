
import { GoogleGenerativeAI } from '@google/generative-ai'
import { NextResponse } from 'next/server'

export async function POST(req: Request) {
    try {
        const { text } = await req.json()

        if (!text) {
            return NextResponse.json({ error: 'Missing text' }, { status: 400 })
        }

        const apiKey = process.env.GEMINI_API_KEY

        if (!apiKey) {
            console.error('Missing GEMINI_API_KEY')
            // Return original text if AI is not configured, to avoid breaking the UI
            return NextResponse.json({ text, warning: 'AI not configured' })
        }

        const genAI = new GoogleGenerativeAI(apiKey)
        const model = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' })

        const prompt = `
        Jesteś asystentem korekty tekstu. Twoim zadaniem jest poprawienie interpunkcji i wielkości liter w podanym tekście, który pochodzi z rozpoznawania mowy (speech-to-text).
        
        Zasady:
        1. Dodaj odpowiednie znaki interpunkcyjne (kropki, przecinki, znaki zapytania).
        2. Popraw wielkość liter (rozpocznij zdania wielką literą).
        3. NIE zmieniaj słów ani sensu wypowiedzi.
        4. NIE dodawaj żadnych komentarzy, wstępów ani zakończeń. Zwróć TYLKO poprawiony tekst.
        5. Jeśli tekst jest bardzo krótki lub urwany, postaraj się go sensownie domknąć interpunkcyjnie.

        Tekst do poprawy:
        "${text}"
        `

        const result = await model.generateContent(prompt)
        const response = await result.response
        const correctedText = response.text().trim()

        // Clean up any remaining quotes if the model added them
        const cleanText = correctedText.replace(/^"/, '').replace(/"$/, '')

        return NextResponse.json({ text: cleanText })

    } catch (error) {
        console.error('Error processing AI punctuation:', error)
        // Fallback to original text on error
        const originalText = (await req.json().catch(() => ({}))).text || ''
        return NextResponse.json({ text: originalText, error: 'AI processing failed' })
    }
}
