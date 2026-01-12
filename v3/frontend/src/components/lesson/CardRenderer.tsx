import IntroCard from './IntroCard'
import ConceptCard from './ConceptCard'
import QuestionCard from './QuestionCard'
import SummaryCard from './SummaryCard'
import PracticeCard from './PracticeCard'
import WarningCard from './WarningCard'

interface CardRendererProps {
    card: {
        type: 'intro' | 'concept' | 'question' | 'summary' | 'practice' | 'warning'
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
        [key: string]: any
    }
    onAnswer?: (correct: boolean) => void
}

export default function CardRenderer({ card, onAnswer }: CardRendererProps) {
    switch (card.type) {
        case 'intro':
            return <IntroCard {...card} />
        case 'concept':
            return <ConceptCard {...card} />
        case 'question':
            return <QuestionCard {...card} onAnswer={onAnswer} />
        case 'summary':
            return <SummaryCard {...card} />
        case 'practice':
            return <PracticeCard {...card} />
        case 'warning':
            return <WarningCard {...card} />
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
