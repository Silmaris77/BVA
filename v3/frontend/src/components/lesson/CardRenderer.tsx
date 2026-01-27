import IntroCard from './IntroCard'
import ConceptCard from './ConceptCard'
import InputCard from './math/InputCard'
import NumberLineCard from './math/NumberLineCard'
import FractionVisualCard from './math/FractionVisualCard'
import NumberSortCard from './math/NumberSortCard'

import QuestionCard from './QuestionCard'
import SummaryCard from './SummaryCard'
import PracticeCard from './PracticeCard'
import WarningCard from './WarningCard'
import TimelineCard from './TimelineCard'
import LightbulbCard from './LightbulbCard'
import FlashcardsCard from './FlashcardsCard'
import HeroCard from './HeroCard'
import QuizCard from './QuizCard'
import AchievementCard from './AchievementCard'
import HabitBuilderCard from './HabitBuilderCard'
import QuoteCard from './QuoteCard'
import DataCard from './DataCard'
import StoryCard from './StoryCard'
import EndingCard from './EndingCard'
import TestCard from './TestCard'
import ChecklistCard from './ChecklistCard'
import CoverCard from './CoverCard'
import LearningPathCard from './LearningPathCard'
import CycleCard from './CycleCard'
import CycleCardVariantB from './CycleCardVariantB'
import DunningKrugerCard from './DunningKrugerCard'
import ReadinessCard from './ReadinessCard'

export type CardType = 'intro' | 'concept' | 'question' | 'summary' | 'practice' | 'warning' | 'hero' | 'content' | 'interactive' | 'timeline' | 'lightbulb' | 'flashcards' | 'quiz' | 'achievement' | 'habit' | 'quote' | 'data' | 'story' | 'ending' | 'test' | 'checklist' | 'input' | 'number-line' | 'fraction-visual' | 'number-sort' | 'cover' | 'learning-path' | 'cycle' | 'cycle-b' | 'dunning-kruger' | 'readiness'

export interface LessonCardData {
    type: CardType
    title?: string
    subtitle?: string
    description?: string
    content?: string
    question?: string
    options?: string[]
    correctAnswer?: number | string
    explanation?: string
    keyPoints?: string[]
    recap?: string[]
    nextSteps?: string
    badge?: string | {
        xp: number
        title: string
    }
    stats?: { value: string; label: string }[]
    infoBoxes?: { icon?: string, title: string, content: string, type?: 'warning' | 'info' }[]
    table?: { title?: string, headers: string[], rows: string[][] }
    warnings?: string[]
    example?: string
    actionSteps?: string[]
    icon?: string
    visual?: {
        type: 'image' | 'diagram'
        src: string
    }
    quiz?: {
        question: string
        options: string[]
        correct: number
        explanation: string
    }
    questions?: {
        question: string
        options: string[]
        correctAnswer: number
        explanation?: string
    }[]
    habits?: {
        text: string
        id: string
    }[]
    items?: { // For ChecklistCard
        id: string
        text: string
    }[]
    cards?: { // For FlashcardsCard
        front: string
        back: string
    }[]
    level?: string
    xp?: number
    // Lightbulb properties
    insight?: string
    accent_color?: string
    steps?: any[]
    // Story properties
    scenario?: { heading: string, text: string } | string
    consequences?: string[]
    lesson?: { heading: string, text: string }
    // Ending properties
    checklist?: { icon: string; text: string }[]
    tagline?: string
    next_steps?: { text: string; available: boolean }
    // Hero/Content specific
    sections?: any[]
    callout?: any
    remember?: any
    theme?: string
    // Quote specific
    text?: string
    author?: string
    role?: string
    // Data specific
    sources?: string[]

    // Math specific
    min?: number
    max?: number
    step?: number
    tolerance?: number
    initialValue?: number
    unit?: string
    hint?: string

    [key: string]: any
}

interface CardRendererProps {
    card: LessonCardData
    onAnswer?: (correct: boolean) => void
    onTestResult?: (score: number, passed: boolean) => void
    onReset?: () => void
    onNext?: () => void
}

export default function CardRenderer({ card, onAnswer, onTestResult, onReset, onNext }: CardRendererProps) {
    switch (card.type) {
        // ... previous cases ...
        case 'cover':
            return <CoverCard
                title={card.title || 'Lesson Title'}
                subtitle={card.subtitle}
                description={card.description}
                category={card.category}
                durationMinutes={card.durationMinutes}
                xpReward={card.xpReward}
                image={card.image}
                onStart={onNext}
            />
        // ... previous cases ...
        case 'test':
            return <TestCard
                title={card.title || 'Końcowy Test'}
                questions={card.questions || []}
                onTestResult={onTestResult || (() => { })}
                onReset={onReset}
            />
        case 'interactive':
            // Interactive contains a quiz
            return <QuestionCard
                question={card.quiz?.question || card.title || 'Pytanie'}
                options={card.quiz?.options || []}
                correctAnswer={card.quiz?.correct || 0}
                explanation={card.quiz?.explanation}
                onAnswer={onAnswer}
            />
        case 'intro':
            return <IntroCard
                title={card.title || 'Wstęp'}
                description={card.description || ''}
                subtitle={card.subtitle}
                icon={card.icon}
            />
        case 'concept':
            return <ConceptCard
                title={card.title || 'Koncepcja'}
                content={card.content || ''}
                keyPoints={card.keyPoints}
                visual={card.visual}
            />
        case 'question':
            return <QuestionCard
                question={card.question || 'Pytanie'}
                options={card.options || []}
                correctAnswer={(card.correctAnswer as number) || 0}
                explanation={card.explanation}
                onAnswer={onAnswer}
            />
        case 'summary':
            return <SummaryCard
                title={card.title}
                recap={card.recap || []}
                nextSteps={card.nextSteps}
                badge={typeof card.badge === 'string' ? { title: card.badge, xp: 0 } : card.badge}
            />
        case 'practice':
            return <PracticeCard
                title={card.title || 'Ćwiczenie'}
                content={card.content || card.description || ''}
                actionSteps={card.actionSteps}
                keyPoints={card.keyPoints}
                scenario={typeof card.scenario === 'string' ? card.scenario : undefined}
                instruction={card.instruction}
                inputs={card.inputs}
                sampleAnswers={card.sampleAnswers}
            />

        case 'timeline':
            return <TimelineCard
                title={card.title || 'Timeline'}
                data={card.data || { items: [] }}
            />
        case 'lightbulb':
            return <LightbulbCard
                title={card.title || 'Insight'}
                content={card.content || ''}
                insight={card.insight || ''}
                accent_color={card.accent_color}
                steps={card.steps}
            />
        case 'flashcards':
            return <FlashcardsCard
                title={card.title || 'Flashcards'}
                cards={card.cards || []}
            />
        case 'warning':
            return <WarningCard
                title={card.title || 'Uwaga'}
                content={card.content || card.description || ''}
                warnings={card.warnings || []}
                example={card.example}
            />
        case 'quiz':
            return <QuizCard
                title={card.title || 'Sprawdź Wiedzę'}
                questions={card.questions || []}
            />
        case 'achievement':
            return <AchievementCard
                title={card.title || 'Osiągnięcie'}
                description={card.content || card.description || ''}
                icon={card.icon as any || 'trophy'}
                level={card.level}
                xp={card.xp}
                stats={card.stats}
                badge={typeof card.badge === 'string' ? card.badge : undefined}
            />
        case 'habit':
            return <HabitBuilderCard
                title={card.title || 'Action Plan'}
                description={card.content || card.description || ''}
                habits={card.habits || []}
            />
        case 'data':
            return <DataCard
                icon={card.icon}
                title={card.title || 'Statystyki'}
                subtitle={card.subtitle}
                content={card.content}
                stats={card.stats || []}
                callout={card.callout}
                infoBoxes={card.infoBoxes}
                table={card.table}
                sources={card.sources?.join('; ')}
            />
        case 'story':
            return <StoryCard
                icon={card.icon}
                badge={typeof card.badge === 'object' ? card.badge?.title : card.badge}
                title={card.title || 'Przypadek z terenu'}
                scenario={typeof card.scenario === 'object' ? card.scenario : undefined}
                consequences={card.consequences || []}
                lesson={card.lesson}
                situation={card.situation}
                scenarios={card.scenarios}
                phases={card.phases}
                outcome={card.outcome}
            />
        case 'ending':
            return <EndingCard
                icon={card.icon}
                title={card.title || 'Podsumowanie'}
                subtitle={card.subtitle}
                checklist={card.checklist || []}
                tagline={card.tagline}
                next_steps={card.next_steps}
            />
        case 'hero':
            return <HeroCard
                title={card.title || 'Hero'}
                subtitle={card.subtitle}
                tagline={card.tagline}
                content={card.content}
                icon={card.icon}
                theme={card.theme}
                sections={card.sections}
                callout={card.callout}
            />
        case 'content':
            return <ConceptCard
                title={card.title || 'Content'}
                content={card.content}
                sections={card.sections}
                callout={card.callout}
                remember={card.remember}
                keyPoints={card.keyPoints}
                visual={card.visual}
            />
        case 'quote':
            return <QuoteCard
                text={card.content || card.text || ''}
                author={card.author || ''}
                role={card.role}
            />
        case 'checklist':
            return <ChecklistCard
                title={card.title || 'Lista Kontrolna'}
                description={card.description || ''}
                items={card.items || []}
            />
        case 'test':
            return <TestCard
                title={card.title || 'Końcowy Test'}
                questions={card.questions || []}
                onTestResult={onTestResult || (() => { })}
            />
        case 'input':
            return <InputCard
                question={card.question || 'Oblicz...'}
                correctAnswer={card.correctAnswer || ''}
                placeholder={card.placeholder}
                unit={card.unit}
                hint={card.hint}
                explanation={card.explanation}
            />
        case 'number-line':
            return <NumberLineCard
                question={card.question || 'Zaznacz na osi'}
                min={card.min || 0}
                max={card.max || 10}
                step={card.step || 1}
                correctValue={card.correctValue !== undefined ? Number(card.correctValue) : Number(card.correctAnswer) || 0}
                tolerance={card.tolerance}
                initialValue={card.initialValue}
                explanation={card.explanation}
            />
        case 'fraction-visual':
            return <FractionVisualCard
                title={card.title}
                question={card.question || 'Zaznacz odpowiednią część'}
                numerator={card.numerator || 1}
                denominator={card.denominator || 4}
                visualType={card.visualType || 'pie'}
                interactive={card.interactive !== false}
            />
        case 'number-sort':
            return <NumberSortCard
                title={card.title}
                question={card.question || 'Uporządkuj liczby'}
                numbers={card.numbers || [1, 2, 3]}
                order={card.order || 'asc'}
            />
        case 'cover':
            return <CoverCard
                title={card.title || 'Lesson Title'}
                subtitle={card.subtitle}
                description={card.description}
                category={card.category}
                durationMinutes={card.durationMinutes}
                xpReward={card.xpReward}
                image={card.image}
            />
        case 'learning-path':
            return <LearningPathCard
                title={card.title}
                description={card.description}
                levels={card.levels}
            />
        case 'cycle':
            return <CycleCard
                title={card.title}
                description={card.description}
                steps={card.steps}
                cycleType={card.cycleType}
            />
        case 'cycle-b':
            return <CycleCardVariantB
                title={card.title}
                description={card.description}
                steps={card.steps}
                cycleType={card.cycleType}
            />
        case 'dunning-kruger':
            return <DunningKrugerCard
                title={card.title}
                description={card.description}
                points={card.points}
            />
        case 'readiness':
            return <ReadinessCard
                title={card.title}
                description={card.description}
                imageSrc={card.image}
            />
        default:
            return (
                <div style={{
                    padding: '40px',
                    background: 'rgba(255, 68, 68, 0.1)',
                    border: '1px solid #ef4444',
                    borderRadius: '16px',
                    color: '#fca5a5',
                    textAlign: 'center'
                }}>
                    Unknown card type: {card.type}
                </div>
            )
    }
}
