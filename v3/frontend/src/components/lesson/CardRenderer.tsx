import IntroCard from './IntroCard'
import ConceptCard from './ConceptCard'
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

interface CardRendererProps {
    card: {
        type: 'intro' | 'concept' | 'question' | 'summary' | 'practice' | 'warning' | 'hero' | 'content' | 'interactive' | 'timeline' | 'lightbulb' | 'flashcards' | 'quiz' | 'achievement' | 'habit' | 'quote'
        title?: string
        subtitle?: string
        description?: string
        content?: string
        question?: string
        options?: string[]
        correctAnswer?: number
        explanation?: string
        keyPoints?: string[]
        recap?: string[]
        nextSteps?: string
        badge?: {
            xp: number
            title: string
        }
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
        level?: string
        xp?: number
        [key: string]: any
    }
    onAnswer?: (correct: boolean) => void
}

export default function CardRenderer({ card, onAnswer }: CardRendererProps) {
    switch (card.type) {
        case 'hero':
            // Hero is like intro but more emphasis - now using Emotional Variant
            return <HeroCard
                title={card.title || 'Wstęp'}
                content={card.content || card.description || ''}
                subtitle={card.subtitle}
                icon={card.icon}
            />
        case 'content':
            // Content is like concept
            return <ConceptCard
                title={card.title || 'Koncepcja'}
                content={card.content || ''}
                keyPoints={card.keyPoints}
                visual={card.visual}
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
                correctAnswer={card.correctAnswer || 0}
                explanation={card.explanation}
                onAnswer={onAnswer}
            />
        case 'summary':
            return <SummaryCard
                title={card.title}
                recap={card.recap || []}
                nextSteps={card.nextSteps}
                badge={card.badge}
            />
        case 'practice':
            return <PracticeCard
                title={card.title || 'Ćwiczenie'}
                content={card.content || card.description || ''}
                actionSteps={card.actionSteps}
                keyPoints={card.keyPoints}
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
            />
        case 'habit':
            return <HabitBuilderCard
                title={card.title || 'Action Plan'}
                description={card.content || card.description || ''}
                habits={card.habits || []}
            />
        case 'quote':
            return <QuoteCard
                text={card.content || card.text || ''}
                author={card.author || ''}
                role={card.role}
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
