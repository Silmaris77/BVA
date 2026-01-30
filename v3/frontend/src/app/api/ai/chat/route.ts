
import { GoogleGenerativeAI } from '@google/generative-ai'
import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

// Initialize Gemini API
// ERROR HANDLING: If the API key is missing, the backend will return a 500 error.
// We should properly handle this in the client, but for now, we'll log it server-side.
const apiKey = process.env.GOOGLE_API_KEY
const genAI = apiKey ? new GoogleGenerativeAI(apiKey) : null

export async function POST(req: Request) {
    if (!genAI) {
        return NextResponse.json(
            { error: 'GOOGLE_API_KEY is not set in environment variables.' },
            { status: 500 }
        )
    }

    try {
        const { messages, systemPrompt } = await req.json()

        // 1. Prepare history for Gemini
        // Gemini expects a specific format. We'll include the system prompt as the first part of the conversation or as a system instruction (depending on model capabilities, but for 1.5 Flash we can pretend it's the first message from Developer or just context).
        // For simplicity with the standard API, we'll prepend the system prompt to the first user message or use the 'systemInstruction' feature if available in the SDK version.

        const model = genAI.getGenerativeModel({
            model: 'gemini-2.5-flash',
            systemInstruction: systemPrompt
        })

        // 2. Convert frontend message format to Gemini format
        // Frontend: { id, role: 'user' | 'assistant', content }
        // Gemini: { role: 'user' | 'model', parts: [{ text: ... }] }
        let history = messages.slice(0, -1).map((msg: any) => ({
            role: msg.role === 'user' ? 'user' : 'model',
            parts: [{ text: msg.content }]
        }))

        // GEMINI CONSTRAINT: History must start with a 'user' message.
        // If the chat starts with an AI Greeting (which is common in our app), prepending a dummy user message fixes the error.
        if (history.length > 0 && history[0].role === 'model') {
            history.unshift({
                role: 'user',
                parts: [{ text: 'Start conversation' }] // Placeholder to satisfy strict alternating history requirement
            })
        }

        const lastMessage = messages[messages.length - 1].content

        const chat = model.startChat({
            history: history,
            generationConfig: {
                maxOutputTokens: 1000,
            },
        })

        const result = await chat.sendMessage(lastMessage)
        const response = await result.response
        const text = response.text()

        return NextResponse.json({ response: text })

    } catch (error: any) {
        console.error('Gemini API Error Detail:', JSON.stringify(error, null, 2));
        console.error('Gemini API Error Message:', error.message);

        return NextResponse.json(
            {
                error: 'Failed to generate response',
                details: error.message || String(error),
                debug: process.env.NODE_ENV === 'development' ? JSON.stringify(error) : undefined
            },
            { status: 500 }
        )
    }
}
