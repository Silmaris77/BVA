'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
    PolarAngleAxis,
    PolarGrid,
    PolarRadiusAxis,
    Radar,
    RadarChart,
    ResponsiveContainer,
    Tooltip
} from 'recharts'
import { ChevronRight, RefreshCw, Trophy } from 'lucide-react'
import { DEGEN_TYPES, DegenTypeKey } from '@/data/degen-types'

// --- Data Definitions ---

interface QuestionOption {
    text: string;
    scores: Partial<Record<DegenTypeKey, number>>;
}

interface Question {
    question: string;
    options: QuestionOption[];
}

const TEST_QUESTIONS: Question[] = [
    {
        question: "Jak reagujesz, gdy cena aktywa gwałtownie wzrasta?",
        options: [
            { "text": "Natychmiast kupuję, nie analizując zbyt dużo.", "scores": { "YOLO Degen": 1 } },
            { "text": "Zastanawiam się, czy to zgodne z moją strategią.", "scores": { "Strategist Degen": 1 } },
            { "text": "Czuję euforię i szybko kupuję.", "scores": { "Emo Degen": 1 } },
            { "text": "Czekam na spokojniejszy moment na rynku.", "scores": { "Zen Degen": 1 } },
            { "text": "Analizuję dane, by przewidzieć kolejny ruch.", "scores": { "Mad Scientist Degen": 1 } },
            { "text": "Sprawdzam dane historyczne i ryzyko.", "scores": { "Spreadsheet Degen": 1 } },
            { "text": "Analizuję kontekst i większy trend.", "scores": { "Meta Degen": 1 } },
            { "text": "Kupuję, bo widzę, że wszyscy o tym mówią.", "scores": { "Hype Degen": 1 } }
        ]
    },
    {
        question: "Co robisz, gdy rynek zaczyna się zmieniać w sposób nieprzewidywalny?",
        options: [
            { "text": "Działam natychmiast – instynkt to podstawa.", "scores": { "YOLO Degen": 1 } },
            { "text": "Analizuję dane, zanim coś zrobię.", "scores": { "Strategist Degen": 1 } },
            { "text": "Wpadam w panikę, sprzedaję wszystko.", "scores": { "Emo Degen": 1 } },
            { "text": "Zachowuję spokój, nic nie zmieniam.", "scores": { "Zen Degen": 1 } },
            { "text": "Tworzę własny model predykcyjny.", "scores": { "Mad Scientist Degen": 1 } },
            { "text": "Odświeżam arkusze z analizami.", "scores": { "Spreadsheet Degen": 1 } },
            { "text": "Szukam głębszego sensu w makroekonomii.", "scores": { "Meta Degen": 1 } },
            { "text": "Reaguję tak, jak społeczność Twittera.", "scores": { "Hype Degen": 1 } }
        ]
    },
    {
        question: "Jak często zmieniasz swoje decyzje inwestycyjne?",
        options: [
            { "text": "Ciągle – każda okazja to nowy ruch.", "scores": { "YOLO Degen": 1 } },
            { "text": "Tylko gdy plan tego wymaga.", "scores": { "Strategist Degen": 1 } },
            { "text": "Za każdym razem, gdy się zestresuję.", "scores": { "Emo Degen": 1 } },
            { "text": "Prawie nigdy – spokój to podstawa.", "scores": { "Zen Degen": 1 } },
            { "text": "Kiedy dane dają zielone światło.", "scores": { "Mad Scientist Degen": 1 } },
            { "text": "Gdy model pokazuje, że to uzasadnione.", "scores": { "Spreadsheet Degen": 1 } },
            { "text": "W rytmie zmian rynkowych i geopolitycznych.", "scores": { "Meta Degen": 1 } },
            { "text": "Gdy coś trenduje – wchodzę!", "scores": { "Hype Degen": 1 } }
        ]
    },
    {
        question: "Jak wygląda Twoje poranne podejście do inwestowania?",
        options: [
            { "text": "Włączam aplikację i kupuję na ślepo.", "scores": { "YOLO Degen": 1 } },
            { "text": "Sprawdzam moją strategię i wykonuję plan.", "scores": { "Strategist Degen": 1 } },
            { "text": "Sprawdzam nastroje i kieruję się emocjami.", "scores": { "Emo Degen": 1 } },
            { "text": "Medytuję, zanim podejmę decyzję.", "scores": { "Zen Degen": 1 } },
            { "text": "Odpalam skrypty z analizami.", "scores": { "Mad Scientist Degen": 1 } },
            { "text": "Aktualizuję swój Excel z danymi.", "scores": { "Spreadsheet Degen": 1 } },
            { "text": "Przeglądam światowe wydarzenia.", "scores": { "Meta Degen": 1 } },
            { "text": "Sprawdzam TikToka i Twittera.", "scores": { "Hype Degen": 1 } }
        ]
    },
    {
        question: "Jak się czujesz, gdy Twoja inwestycja traci na wartości?",
        options: [
            { "text": "Trudno, YOLO – lecę dalej.", "scores": { "YOLO Degen": 1 } },
            { "text": "To część planu, mam to pod kontrolą.", "scores": { "Strategist Degen": 1 } },
            { "text": "Jestem załamany, nie mogę spać.", "scores": { "Emo Degen": 1 } },
            { "text": "Akceptuję to. Taki jest rynek.", "scores": { "Zen Degen": 1 } },
            { "text": "Analizuję, dlaczego tak się stało.", "scores": { "Mad Scientist Degen": 1 } },
            { "text": "Aktualizuję plik i zmieniam parametry.", "scores": { "Spreadsheet Degen": 1 } },
            { "text": "Sprawdzam, czy to nie wynik globalnych trendów.", "scores": { "Meta Degen": 1 } },
            { "text": "Obwiniam influencerów z internetu.", "scores": { "Hype Degen": 1 } }
        ]
    },
    {
        question: "Jak wybierasz projekt lub spółkę do inwestycji?",
        options: [
            { "text": "Klikam w to, co akurat wygląda fajnie.", "scores": { "YOLO Degen": 1 } },
            { "text": "Szukam zgodności z moją strategią.", "scores": { "Strategist Degen": 1 } },
            { "text": "Wybieram to, co wzbudza emocje.", "scores": { "Emo Degen": 1 } },
            { "text": "Wybieram intuicyjnie, po przemyśleniu.", "scores": { "Zen Degen": 1 } },
            { "text": "Patrzę na technologię i innowacyjność.", "scores": { "Mad Scientist Degen": 1 } },
            { "text": "Analizuję wskaźniki i liczby.", "scores": { "Spreadsheet Degen": 1 } },
            { "text": "Czytam białą księgę i analizuję ekosystem.", "scores": { "Meta Degen": 1 } },
            { "text": "To, co trenduje na socialach.", "scores": { "Hype Degen": 1 } }
        ]
    },
    {
        question: "Jak planujesz swoje portfolio?",
        options: [
            { "text": "Nie planuję – pełen spontan.", "scores": { "YOLO Degen": 1 } },
            { "text": "Mam rozpisany plan i cel.", "scores": { "Strategist Degen": 1 } },
            { "text": "Dodaję i usuwam po impulsie.", "scores": { "Emo Degen": 1 } },
            { "text": "Portfolio to droga – zmienia się naturalnie.", "scores": { "Zen Degen": 1 } },
            { "text": "Symuluję wiele scenariuszy.", "scores": { "Mad Scientist Degen": 1 } },
            { "text": "Optymalizuję strukturę w arkuszu kalkulacyjnym.", "scores": { "Spreadsheet Degen": 1 } },
            { "text": "Układam pod mega trendy i narracje.", "scores": { "Meta Degen": 1 } },
            { "text": "Kupuję to, co polecają inni.", "scores": { "Hype Degen": 1 } }
        ]
    },
    {
        question: "Co robisz w dniu dużej korekty rynkowej?",
        options: [
            { "text": "Wchodzę all-in w dołku.", "scores": { "YOLO Degen": 1 } },
            { "text": "Trzymam się planu.", "scores": { "Strategist Degen": 1 } },
            { "text": "Wpadam w panikę i wyprzedaję.", "scores": { "Emo Degen": 1 } },
            { "text": "Obserwuję i nie działam pochopnie.", "scores": { "Zen Degen": 1 } },
            { "text": "Weryfikuję modele i dane.", "scores": { "Mad Scientist Degen": 1 } },
            { "text": "Uaktualniam wyceny i alokację.", "scores": { "Spreadsheet Degen": 1 } },
            { "text": "Szacuję konsekwencje makroekonomiczne.", "scores": { "Meta Degen": 1 } },
            { "text": "Patrzę co robią znani YouTuberzy.", "scores": { "Hype Degen": 1 } }
        ]
    },
    {
        question: "Jaki jest Twój ulubiony sposób zdobywania wiedzy o inwestowaniu?",
        options: [
            { "text": "Z memów i shortów.", "scores": { "YOLO Degen": 1 } },
            { "text": "Z książek i analiz.", "scores": { "Strategist Degen": 1 } },
            { "text": "Z podcastów o sukcesach i porażkach.", "scores": { "Emo Degen": 1 } },
            { "text": "Z doświadczenia i uważności.", "scores": { "Zen Degen": 1 } },
            { "text": "Z badań naukowych.", "scores": { "Mad Scientist Degen": 1 } },
            { "text": "Z raportów i arkuszy.", "scores": { "Spreadsheet Degen": 1 } },
            { "text": "Z rozmów i debat o przyszłości.", "scores": { "Meta Degen": 1 } },
            { "text": "Z komentarzy pod filmami influencerów.", "scores": { "Hype Degen": 1 } }
        ]
    },
    {
        question: "Jak oceniasz sukces swojej inwestycji?",
        options: [
            { "text": "Czy zrobiłem szybki zysk?", "scores": { "YOLO Degen": 1 } },
            { "text": "Czy osiągnąłem cel zgodnie z planem?", "scores": { "Strategist Degen": 1 } },
            { "text": "Czy poczułem się z tym dobrze?", "scores": { "Emo Degen": 1 } },
            { "text": "Czy nie cierpiałem w procesie?", "scores": { "Zen Degen": 1 } },
            { "text": "Czy moja hipoteza się potwierdziła?", "scores": { "Mad Scientist Degen": 1 } },
            { "text": "Czy ROI było zgodne z kalkulacją?", "scores": { "Spreadsheet Degen": 1 } },
            { "text": "Czy wpisało się to w większy trend?", "scores": { "Meta Degen": 1 } },
            { "text": "Czy znajomi byli pod wrażeniem?", "scores": { "Hype Degen": 1 } }
        ]
    },
    {
        question: "Jak podejmujesz decyzję o sprzedaży aktywów?",
        options: [
            { "text": "Sprzedaję wszystko nagle, gdy tylko czuję się zagrożony.", "scores": { "Emo Degen": 1 } },
            { "text": "Sprzedaję tylko wtedy, gdy osiągnę planowany cel.", "scores": { "Strategist Degen": 1 } },
            { "text": "Sprzedaję od razu po dużym wzroście – lepiej nie ryzykować.", "scores": { "YOLO Degen": 1 } },
            { "text": "Sprzedaję spokojnie i bez emocji, zgodnie z filozofią spokoju.", "scores": { "Zen Degen": 1 } },
            { "text": "Tworzę modele ryzyka i podejmuję decyzję na podstawie wyników.", "scores": { "Mad Scientist Degen": 1 } },
            { "text": "Najpierw aktualizuję dane, potem analizuję.", "scores": { "Spreadsheet Degen": 1 } },
            { "text": "Próbuję przewidzieć przyszłość rynku i na tej podstawie decyduję.", "scores": { "Meta Degen": 1 } },
            { "text": "Sprzedaję, gdy widzę, że wszyscy to robią.", "scores": { "Hype Degen": 1 } }
        ]
    },
    {
        question: "Co motywuje Cię najbardziej do inwestowania?",
        options: [
            { "text": "Możliwość zysku tu i teraz.", "scores": { "YOLO Degen": 1 } },
            { "text": "Realizacja długoterminowej strategii.", "scores": { "Strategist Degen": 1 } },
            { "text": "Emocje – ekscytacja, adrenalina.", "scores": { "Emo Degen": 1 } },
            { "text": "Praktyka spokoju i cierpliwości.", "scores": { "Zen Degen": 1 } },
            { "text": "Chęć przetestowania własnych hipotez.", "scores": { "Mad Scientist Degen": 1 } },
            { "text": "Obliczenia pokazujące potencjalny zwrot.", "scores": { "Spreadsheet Degen": 1 } },
            { "text": "Wiara w przełomowe technologie.", "scores": { "Meta Degen": 1 } },
            { "text": "Trendy, memy, hype i to, co popularne.", "scores": { "Hype Degen": 1 } }
        ]
    },
    {
        question: "Co robisz po udanej inwestycji?",
        options: [
            { "text": "Czuję euforię i szukam kolejnej szansy!", "scores": { "Emo Degen": 1 } },
            { "text": "Analizuję, czy było to zgodne z planem.", "scores": { "Strategist Degen": 1 } },
            { "text": "Wypłacam zyski i idę dalej – YOLO.", "scores": { "YOLO Degen": 1 } },
            { "text": "Praktykuję wdzięczność i pozostaję spokojny.", "scores": { "Zen Degen": 1 } },
            { "text": "Zapisuję dane i aktualizuję model.", "scores": { "Spreadsheet Degen": 1 } },
            { "text": "Zastanawiam się, jak to powtórzyć na poziomie systemowym.", "scores": { "Mad Scientist Degen": 1 } },
            { "text": "Snuję wizje przyszłości i szukam czegoś jeszcze bardziej innowacyjnego.", "scores": { "Meta Degen": 1 } },
            { "text": "Chwalę się znajomym – niech wiedzą!", "scores": { "Hype Degen": 1 } }
        ]
    },
    {
        question: "Co robisz, gdy masz zainwestować większą sumę?",
        options: [
            { "text": "Wchodzę od razu, bez zastanowienia.", "scores": { "YOLO Degen": 1 } },
            { "text": "Sprawdzam, czy to pasuje do mojego planu i alokacji.", "scores": { "Strategist Degen": 1 } },
            { "text": "Waham się, analizuję i w końcu nic nie robię.", "scores": { "Mad Scientist Degen": 1 } },
            { "text": "Medytuję, a potem podejmuję decyzję w zgodzie ze sobą.", "scores": { "Zen Degen": 1 } },
            { "text": "Ekscytuję się, ale potem się boję i działam impulsywnie.", "scores": { "Emo Degen": 1 } },
            { "text": "Tworzę pełną analizę w Excelu, zanim zrobię cokolwiek.", "scores": { "Spreadsheet Degen": 1 } },
            { "text": "Zastanawiam się, jak ta inwestycja wpisuje się w przyszłość.", "scores": { "Meta Degen": 1 } },
            { "text": "Wpisuję nazwę aktywa w Google Trends i Twittera.", "scores": { "Hype Degen": 1 } }
        ]
    }
];

// --- Sub-components for Results ---

function RadarChartResult({ scores }: { scores: Record<string, number> }) {
    // Transform scores for Recharts
    // Recharts radar expects data like [{ subject: 'Math', A: 120, fullMark: 150 }, ...]
    const data = Object.keys(DEGEN_TYPES).map(key => ({
        subject: key,
        A: scores[key as DegenTypeKey] || 0,
        fullMark: 20 // Approx max score
    }));

    // Calculate max value to set domain properly
    // We use dynamic scaling to ensure the shape is always visible and attractive, 
    // regardless of the absolute score (which might be low).
    const currentMax = Math.max(...Object.values(scores)) || 1;
    // Add 10-20% padding and ensure integer ceiling for nice grid
    const domainMax = Math.ceil(Math.max(currentMax * 1.2, 5));

    return (
        <div className="w-full h-[350px] md:h-[400px] flex items-center justify-center relative hover:scale-[1.02] transition-transform duration-500 cursor-crosshair">
            <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
                    <defs>
                        <linearGradient id="radarGradient" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#8a2be2" stopOpacity={0.7} />
                            <stop offset="95%" stopColor="#8a2be2" stopOpacity={0.1} />
                        </linearGradient>
                    </defs>
                    <PolarGrid stroke="rgba(255,255,255,0.1)" strokeWidth={1} />
                    <PolarAngleAxis
                        dataKey="subject"
                        tick={{ fill: 'rgba(255,255,255,0.7)', fontSize: 11 }}
                    />
                    <PolarRadiusAxis
                        angle={30}
                        domain={[0, domainMax]}
                        tickCount={6}
                        tick={false}
                        axisLine={false}
                    />
                    <Radar
                        name="Wynik"
                        dataKey="A"
                        stroke="#8a2be2"
                        strokeWidth={3}
                        fill="url(#radarGradient)"
                        fillOpacity={1}
                        activeDot={{ r: 6, fill: '#fff', stroke: '#8a2be2', strokeWidth: 2 }}
                        isAnimationActive={true}
                    />
                    <Tooltip
                        contentStyle={{ backgroundColor: 'rgba(30, 30, 45, 0.95)', borderRadius: '12px', border: '1px solid rgba(138, 43, 226, 0.3)', boxShadow: '0 4px 20px rgba(0,0,0,0.4)' }}
                        itemStyle={{ color: '#fff', fontWeight: 600 }}
                        cursor={{ stroke: 'rgba(138, 43, 226, 0.5)', strokeWidth: 2 }}
                    />
                </RadarChart>
            </ResponsiveContainer>
        </div>
    );
}

// --- Main Component ---

export default function DegenTest({ initialResult, lastCompletedAt }: { initialResult?: any; lastCompletedAt?: string }) {
    // State
    // If initialResult exists, start in 'results' mode and populate scores
    const [step, setStep] = useState<'intro' | 'test' | 'results'>(initialResult ? 'results' : 'intro');
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [isSaving, setIsSaving] = useState(false);

    // Parse initial result (which is stored as output_data JSON)
    // We expect output_data to have { scores: ... } or be the scores object itself depending on how we save it.
    // Let's assume we save { scores: ... } to be safe/extensible.
    const [scores, setScores] = useState<Record<DegenTypeKey, number>>(() => {
        if (initialResult && initialResult.scores) {
            return initialResult.scores;
        }
        return {
            "Zen Degen": 0, "YOLO Degen": 0, "Emo Degen": 0, "Strategist Degen": 0,
            "Mad Scientist Degen": 0, "Spreadsheet Degen": 0, "Meta Degen": 0, "Hype Degen": 0
        };
    });

    // Determine dominant type
    const getDominantType = () => {
        let maxScore = -1;
        let dominant: DegenTypeKey = "Zen Degen"; // Default

        Object.entries(scores).forEach(([key, score]) => {
            if (score > maxScore) {
                maxScore = score;
                dominant = key as DegenTypeKey;
            }
        });

        return dominant;
    };

    const saveResult = async (finalScores: Record<DegenTypeKey, number>) => {
        setIsSaving(true);
        try {
            const response = await fetch('/api/tools/degen-test/complete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    input_data: {}, // We could save answers map here if needed
                    output_data: { scores: finalScores },
                    xp_awarded: 150
                })
            });

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Failed to save result:', response.status, response.statusText, errorText);
                if (response.status === 401) {
                    alert("Zaloguj się, aby zapisać wynik testu!");
                } else {
                    alert("Wystąpił błąd podczas zapisywania wyniku. Sprawdź konsolę.");
                }
            } else {
                // Optional: Notify success? The UI transition to results is already implicit success.
            }
        } catch (error) {
            console.error('Error saving result:', error);
        } finally {
            setIsSaving(false);
        }
    };

    const handleAnswer = (optionScores: Partial<Record<DegenTypeKey, number>>) => {
        // Update scores
        const newScores = { ...scores };
        Object.keys(optionScores).forEach((key) => {
            const typeKey = key as DegenTypeKey;
            if (optionScores[typeKey]) {
                newScores[typeKey] += optionScores[typeKey]!;
            }
        });
        setScores(newScores);

        // Advance question or finish
        if (currentQuestionIndex < TEST_QUESTIONS.length - 1) {
            setCurrentQuestionIndex(currentQuestionIndex + 1);
        } else {
            setStep('results');
            saveResult(newScores);
        }
    };

    // --- Render Views ---

    if (step === 'intro') {
        return (
            <div className="max-w-4xl mx-auto p-6 md:p-12">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-center"
                >
                    <div className="w-24 h-24 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-8 shadow-xl shadow-purple-500/20">
                        <span className="text-4xl">🎭</span>
                    </div>

                    <h1 className="text-3xl md:text-5xl font-bold text-white mb-6">
                        Test Typu Degena
                    </h1>

                    <p className="text-xl text-gray-300 mb-10 max-w-2xl mx-auto leading-relaxed">
                        Sprawdź, jakim typem inwestora jesteś naprawdę. Czy kierujesz się zimną kalkulacją, emocjami, czy może intuicją?
                    </p>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-3xl mx-auto mb-12 text-left">
                        <div className="bg-white/5 p-6 rounded-2xl border border-white/10">
                            <h3 className="text-lg font-semibold text-white mb-2 flex items-center gap-2">
                                <span>🎯</span> Unikalne Archetypy
                            </h3>
                            <p className="text-gray-400">
                                8 zróżnicowanych profili inwestycyjnych - od Zen Degena po Szalonego Naukowca.
                            </p>
                        </div>
                        <div className="bg-white/5 p-6 rounded-2xl border border-white/10">
                            <h3 className="text-lg font-semibold text-white mb-2 flex items-center gap-2">
                                <span>📊</span> Wykres Radarowy
                            </h3>
                            <p className="text-gray-400">
                                Zobacz swoją osobowość na wielowymiarowym wykresie kompetencji.
                            </p>
                        </div>
                    </div>

                    <button
                        onClick={() => setStep('test')}
                        className="px-10 py-4 bg-white text-black font-bold text-lg rounded-full hover:bg-gray-200 transition-transform active:scale-95 shadow-lg shadow-white/10"
                    >
                        {initialResult ? 'Rozwiąż ponownie' : 'Rozpocznij Test'}
                    </button>
                    {initialResult && lastCompletedAt && (
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
                    <div className="mt-4 text-sm text-gray-500">
                        Czas trwania: ok. 5 minut | 14 pytań
                    </div>
                </motion.div>
            </div>
        );
    }

    if (step === 'test') {
        const question = TEST_QUESTIONS[currentQuestionIndex];
        const progress = ((currentQuestionIndex + 1) / TEST_QUESTIONS.length) * 100;

        return (
            <div className="max-w-3xl mx-auto p-4 md:p-8">
                {/* Progress Bar */}
                <div className="w-full h-2 bg-white/10 rounded-full mb-10 overflow-hidden">
                    <motion.div
                        className="h-full bg-gradient-to-r from-blue-500 to-purple-500"
                        initial={{ width: 0 }}
                        animate={{ width: `${progress}%` }}
                        transition={{ duration: 0.5 }}
                    />
                </div>

                <AnimatePresence mode="wait">
                    <motion.div
                        key={currentQuestionIndex}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        transition={{ duration: 0.3 }}
                    >
                        <h2 className="text-xl text-purple-300 font-medium mb-4">
                            Pytanie {currentQuestionIndex + 1} z {TEST_QUESTIONS.length}
                        </h2>

                        <h3 className="text-2xl md:text-3xl font-bold text-white mb-10 leading-tight">
                            {question.question}
                        </h3>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {question.options.map((option, idx) => (
                                <button
                                    key={idx}
                                    onClick={() => handleAnswer(option.scores)}
                                    className="p-6 text-left bg-white/5 hover:bg-white/10 border border-white/10 hover:border-purple-500/50 rounded-xl transition-all group flex flex-col"
                                >
                                    <span className="text-lg text-gray-200 group-hover:text-white transition-colors">
                                        {option.text}
                                    </span>
                                </button>
                            ))}
                        </div>
                    </motion.div>
                </AnimatePresence>
            </div>
        );
    }

    if (step === 'results') {
        const sortedScores = Object.entries(scores).sort(([, a], [, b]) => b - a);
        const dominantType = sortedScores[0][0] as DegenTypeKey;
        const secondaryType = sortedScores[1][0] as DegenTypeKey;

        const details = DEGEN_TYPES[dominantType];

        return (
            <div className="max-w-6xl mx-auto p-4 md:p-8">
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start"
                >
                    {/* Left Column: Result Details */}
                    <div>
                        <div className="mb-8">
                            <div className="inline-flex items-center gap-2 px-4 py-2 bg-purple-500/20 rounded-full text-purple-300 text-sm font-medium mb-4">
                                <Trophy size={16} /> Wynik Testu
                            </div>
                            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
                                Jesteś <span style={{ color: details.color }}>{dominantType}</span> {details.icon}
                            </h1>
                            <p className="text-xl text-gray-300 leading-relaxed">
                                {details.description}
                            </p>
                        </div>

                        {/* Chart for Mobile (visible only on small screens) */}
                        <div className="lg:hidden mb-8 bg-white/5 rounded-2xl p-4 border border-white/10">
                            <RadarChartResult scores={scores} />
                        </div>

                        <div className="grid grid-cols-1 gap-6 mb-8">
                            <div className="bg-green-500/10 p-6 rounded-2xl border border-green-500/20">
                                <h3 className="text-lg font-bold text-green-400 mb-3 flex items-center gap-2">
                                    <span>💪</span> Mocne strony
                                </h3>
                                <ul className="space-y-2">
                                    {details.strengths.map((s, i) => (
                                        <li key={i} className="flex items-start gap-2 text-gray-300">
                                            <span className="text-green-500 mt-1.5 w-1.5 h-1.5 bg-green-500 rounded-full shrink-0" />
                                            {s}
                                        </li>
                                    ))}
                                </ul>
                            </div>

                            <div className="bg-orange-500/10 p-6 rounded-2xl border border-orange-500/20">
                                <h3 className="text-lg font-bold text-orange-400 mb-3 flex items-center gap-2">
                                    <span>🚧</span> Wyzwania
                                </h3>
                                <ul className="space-y-2">
                                    {details.challenges.map((c, i) => (
                                        <li key={i} className="flex items-start gap-2 text-gray-300">
                                            <span className="text-orange-500 mt-1.5 w-1.5 h-1.5 bg-orange-500 rounded-full shrink-0" />
                                            {c}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>

                        <div className="bg-blue-600/20 p-6 rounded-2xl border border-blue-500/30 mb-8">
                            <h3 className="text-lg font-bold text-blue-300 mb-2 flex items-center gap-2">
                                <span>🎯</span> Rekomendowana Strategia
                            </h3>
                            <p className="text-blue-100 italic">
                                "{details.strategy}"
                            </p>
                        </div>

                        <button
                            onClick={() => {
                                setScores({
                                    "Zen Degen": 0, "YOLO Degen": 0, "Emo Degen": 0, "Strategist Degen": 0,
                                    "Mad Scientist Degen": 0, "Spreadsheet Degen": 0, "Meta Degen": 0, "Hype Degen": 0
                                });
                                setCurrentQuestionIndex(0);
                                setStep('test'); // Directly start test, skip intro
                            }}
                            className="flex items-center gap-2 px-6 py-3 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-colors"
                        >
                            <RefreshCw size={18} /> Rozwiąż ponownie
                        </button>
                        {lastCompletedAt && (
                            <p style={{ marginTop: '16px', fontSize: '13px', color: 'rgba(255,255,255,0.6)' }}>
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

                    {/* Right Column: Radar Chart (Desktop) */}
                    <div className="hidden lg:flex flex-col">
                        <div className="bg-white/5 p-8 rounded-3xl border border-white/10 relative overflow-hidden">
                            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500" />
                            <h3 className="text-xl font-bold text-white mb-6 text-center">Profil Kompetencji</h3>
                            <RadarChartResult scores={scores} />

                            <div className="mt-8 grid grid-cols-2 gap-4 text-sm text-gray-400">
                                <div className="text-center p-3 bg-white/5 rounded-lg border border-white/5 hover:bg-white/10 hover:border-purple-500/30 hover:scale-105 transition-all duration-300 cursor-default group">
                                    <div className="text-sm font-bold text-white mb-1 h-8 flex items-center justify-center group-hover:text-purple-300 transition-colors">
                                        {dominantType}
                                    </div>
                                    <div className="text-xs opacity-70">Styl Dominujący</div>
                                </div>
                                <div className="text-center p-3 bg-white/5 rounded-lg border border-white/5 hover:bg-white/10 hover:border-blue-500/30 hover:scale-105 transition-all duration-300 cursor-default group">
                                    <div className="text-sm font-bold text-white mb-1 h-8 flex items-center justify-center group-hover:text-blue-300 transition-colors">
                                        {secondaryType}
                                    </div>
                                    <div className="text-xs opacity-70">Styl Uzupełniający</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </motion.div>
            </div>
        );
    }

    return null;
}
