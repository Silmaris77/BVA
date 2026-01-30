
import { GoogleGenerativeAI } from '@google/generative-ai'
import { NextResponse } from 'next/server'

// Initialize Gemini
const apiKey = process.env.GOOGLE_API_KEY
const genAI = apiKey ? new GoogleGenerativeAI(apiKey) : null

export async function POST(req: Request) {
    if (!genAI) {
        return NextResponse.json({ error: 'Missing API Key' }, { status: 500 })
    }

    try {
        // W przyszłości: pobierz realne wyniki z bazy danych
        // const { userId, behaviorData } = await req.json()

        // MOCK DATA - ROZSZERZONE O BEHAWIOR (Symulacja wyników użytkownika)
        const userProfile = {
            // 1. Wyniki testów (Tożsamość deklaratywna)
            tests: {
                kolb: "Refleksyjny Obserwator (Assimilator)",
                neuroleader: "Visionary (Wizjoner)",
                mi: "Logiczno-Matematyczna",
            },

            // 2. Statystyki RPG (Rzeczywiste kompetencje)
            stats: {
                "Leadership": 75, // Level 3
                "Strategy": 80,   // Level 4
                "Sales": 20,      // Level 1
                "Technical": 45,  // Level 2
                "Communication": 60, // Level 3
                "Mindset": 30     // Level 1
            },

            // 3. Historia Aktywności (Behawior)
            activity: {
                streak: 7, // Dni z rzędu
                top_activities: ["analiza_danych", "planowanie_strategiczne"],
                ignored_activities: ["zimne_telefony", "negocjacje"],
                learning_hours: {
                    morning: 10,
                    afternoon: 2,
                    evening: 45 // Uczy się głównie wieczorami
                }
            },

            // 4. Odblokowane Klasy
            classes: ["Strategiczny Architekt", "Analityk Danych"]
        }

        const prompt = `
            Jesteś zaawansowanym psychologiem biznesu, trenerem liderów i analitykiem danych. 
            Przeanalizuj poniższy profil użytkownika, łącząc wyniki testów psychometrycznych z JEGO RZECZYWISTYM ZACHOWANIEM w aplikacji.
            
            DANE UŻYTKOWNIKA:
            
            1. PSYCHOMETRIA (Kim mówi, że jest):
            - Styl Kolba: ${userProfile.tests.kolb}
            - Typ Neuroleader: ${userProfile.tests.neuroleader}
            - Inteligencja: ${userProfile.tests.mi}
            
            2. RPG STATYSTYKI (W czym jest faktycznie dobry):
            - Leadership: ${userProfile.stats.Leadership}%
            - Strategy: ${userProfile.stats.Strategy}%
            - Sales: ${userProfile.stats.Sales}% (Niski wynik!)
            - Technical: ${userProfile.stats.Technical}%
            
            3. BEHAWIOR (Jak się zachowuje):
            - Streak: ${userProfile.activity.streak} dni
            - Ignoruje tematy: ${userProfile.activity.ignored_activities.join(', ')}
            - Pora nauki: Głównie wieczory (${userProfile.activity.learning_hours.evening}h vs reszta dnia śladowo)
            
            ZADANIE:
            Stwórz profil, który skonfrontuje to kim on "jest" z tym co "robi".
            Np. jeśli jest "Wizjonerem" ale ignoruje "Sales", napisz mu że jego wizje nie sprzedadzą się same.
            Zauważ jego wieczorny tryb pracy.
            
            FORMAT ODPOWIEDZI (zwróć TYLKO czysty JSON, bez markdowna):
            {
                "synthesis": {
                    "archetype": "Kreatywna nazwa archetypu (np. Nocny Strateg)",
                    "description": "3-4 zdania głębokiej analizy. Odnieś się do tego, że np. świetnie planuje, ale unika egzekucji."
                },
                "strengths": [
                    { "title": "Nazwa mocnej strony", "desc": "Wynikająca z połączenia testów i statystyk." }
                ],
                "blind_spots": [
                    { "title": "Ślepa plamka", "desc": "Coś, co użytkownik ignoruje lub gdzie wyniki testów "kłamią" w porównaniu do zachowania." }
                ],
                "energy_profile": {
                    "type": "np. Nocny Marek / Ranny Ptaszek",
                    "tips": "Porada jak wykorzystać ten rytm dnia."
                },
                "communication_style": "Krótki opis jak ten lider komunikuje się z zespołem (na bazie Kolba i Neurolidera).",
                "recommendations": [
                    { 
                        "title": "Konkretna akcja rozwojowa", 
                        "desc": "Odnieś się do słabych statystyk lub ignorowanych tematów.", 
                        "priority": "high" | "medium" | "low"
                    }
                ],
                "motivational_message": "Jedno zdanie, które trafi w serce tego typu osobowości (np. cytat lub mądrość)."
            }
            
            Wymagam: 5 mocnych stron, 3 ślepych plamek, 3 rekomendacji, 1 przesłania motywacyjnego.
        `

        console.log('--- STARTING IDENTITY REPORT GENERATION ---')
        console.log('API Key present:', !!apiKey)

        const model = genAI.getGenerativeModel({
            model: 'gemini-2.5-flash',
            generationConfig: { responseMimeType: "application/json" }
        })

        console.log('Sending request to Gemini...')
        const result = await model.generateContent(prompt)
        console.log('Gemini response received.')

        const responseText = result.response.text()
        console.log('Raw Response Text length:', responseText.length)
        // console.log('Raw Response Text:', responseText) // Uncomment if needed

        let data;
        try {
            data = JSON.parse(responseText)
            console.log('JSON Parse Successful')
        } catch (parseError) {
            console.error('JSON PARSE ERROR. Raw text:', responseText)
            throw new Error('Failed to parse AI response as JSON')
        }

        return NextResponse.json({
            ...data,
            tests: {
                kolb: { name: "Styl Kolba", result: userProfile.tests.kolb, color: "#667eea" },
                neuroleader: { name: "Neuroleader", result: userProfile.tests.neuroleader, color: "#b000ff" },
                mi: { name: "Inteligencje", result: userProfile.tests.mi, color: "#00d4ff" }
            }
        })

    } catch (error: any) {
        console.error('AI Report CRITICAL Error:', error)
        return NextResponse.json({
            error: error.message || 'Unknown error',
            details: error.toString()
        }, { status: 500 })
    }
}
