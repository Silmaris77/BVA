'use client'

import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { CheckSquare } from 'lucide-react'
import { useState } from 'react'

interface ChecklistItem {
    id: string
    text: string
}

interface ChecklistSection {
    id: string
    title: string
    items: ChecklistItem[]
}

interface ChecklistCardProps {
    title: string
    description?: string
    items?: ChecklistItem[] // Flat items (old format)
    sections?: ChecklistSection[] // Grouped sections (new format)
}

export default function ChecklistCard({ title, description, items = [], sections }: ChecklistCardProps) {
    const [checkedState, setCheckedState] = useState<Record<string, boolean>>({})

    const toggleItem = (id: string) => {
        setCheckedState(prev => ({
            ...prev,
            [id]: !prev[id]
        }))
    }

    // Calculate total items from either flat items or sections
    const allItems = sections 
        ? sections.flatMap(section => section.items) 
        : items
    const totalItems = allItems.length
    const checkedCount = Object.values(checkedState).filter(Boolean).length
    const progress = totalItems > 0 ? Math.round((checkedCount / totalItems) * 100) : 0

    return (
        <div style={{
            maxWidth: '900px',
            width: '100%',
        }}>
            <div style={{
                background: 'rgba(20, 20, 35, 0.6)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(0, 212, 255, 0.2)',
                borderRadius: '24px',
                padding: '50px',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
                position: 'relative',
                display: 'flex',
                flexDirection: 'column',
                gap: '32px'
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
                    color: '#00d4ff',
                    fontWeight: 600,
                    padding: '6px 12px',
                    background: 'rgba(0, 212, 255, 0.1)',
                    border: '1px solid rgba(0, 212, 255, 0.2)',
                    borderRadius: '20px'
                }}>
                    CHECKLISTA
                </div>

                {/* Header */}
                <div style={{ textAlign: 'center', marginTop: '20px' }}>
                    <div style={{
                        width: '60px',
                        height: '60px',
                        margin: '0 auto 20px',
                        background: 'rgba(0, 212, 255, 0.1)',
                        borderRadius: '16px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: '#00d4ff'
                    }}>
                        <CheckSquare size={32} />
                    </div>
                    <h2 style={{
                        fontSize: '28px',
                        fontWeight: 700,
                        color: '#fff',
                        marginBottom: '12px'
                    }}>
                        {title}
                    </h2>
                    {description && (
                        <div style={{
                            fontSize: '16px',
                            color: 'rgba(255, 255, 255, 0.7)',
                            lineHeight: '1.6',
                            maxWidth: '700px',
                            margin: '0 auto'
                        }}>
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                {description}
                            </ReactMarkdown>
                        </div>
                    )}
                </div>

                {/* Progress Bar */}
                <div style={{
                    width: '100%',
                    height: '6px',
                    background: 'rgba(255, 255, 255, 0.1)',
                    borderRadius: '3px',
                    overflow: 'hidden'
                }}>
                    <div style={{
                        width: `${progress}%`,
                        height: '100%',
                        background: '#00d4ff',
                        transition: 'width 0.3s ease'
                    }} />
                </div>

                {/* Checklist Items */}
                {sections ? (
                    /* Sectioned format (new) */
                    <div style={{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '28px'
                    }}>
                        {sections.map((section) => {
                            const sectionCheckedCount = section.items.filter(item => checkedState[item.id]).length
                            const sectionProgress = section.items.length > 0 
                                ? Math.round((sectionCheckedCount / section.items.length) * 100) 
                                : 0

                            return (
                                <div key={section.id}>
                                    {/* Section Header */}
                                    <div style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '12px',
                                        marginBottom: '12px'
                                    }}>
                                        <h3 style={{
                                            fontSize: '18px',
                                            fontWeight: 700,
                                            color: '#00d4ff',
                                            margin: 0
                                        }}>
                                            {section.title}
                                        </h3>
                                        <span style={{
                                            fontSize: '13px',
                                            color: 'rgba(255, 255, 255, 0.5)',
                                            fontWeight: 600
                                        }}>
                                            {sectionCheckedCount}/{section.items.length}
                                        </span>
                                        {/* Mini progress bar */}
                                        <div style={{
                                            flex: 1,
                                            height: '4px',
                                            background: 'rgba(255, 255, 255, 0.1)',
                                            borderRadius: '2px',
                                            overflow: 'hidden'
                                        }}>
                                            <div style={{
                                                width: `${sectionProgress}%`,
                                                height: '100%',
                                                background: '#00d4ff',
                                                transition: 'width 0.3s ease'
                                            }} />
                                        </div>
                                    </div>

                                    {/* Section Items */}
                                    <div style={{
                                        display: 'flex',
                                        flexDirection: 'column',
                                        gap: '10px'
                                    }}>
                                        {section.items.map((item) => {
                                            const isChecked = checkedState[item.id] || false
                                            return (
                                                <div
                                                    key={item.id}
                                                    onClick={() => toggleItem(item.id)}
                                                    style={{
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        gap: '16px',
                                                        padding: '14px 18px',
                                                        background: isChecked ? 'rgba(0, 212, 255, 0.1)' : 'rgba(255, 255, 255, 0.05)',
                                                        border: isChecked ? '1px solid rgba(0, 212, 255, 0.3)' : '1px solid rgba(255, 255, 255, 0.1)',
                                                        borderRadius: '10px',
                                                        cursor: 'pointer',
                                                        transition: 'all 0.2s'
                                                    }}
                                                >
                                                    <div style={{
                                                        width: '22px',
                                                        height: '22px',
                                                        borderRadius: '6px',
                                                        border: isChecked ? 'none' : '2px solid rgba(255, 255, 255, 0.3)',
                                                        background: isChecked ? '#00d4ff' : 'transparent',
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        justifyContent: 'center',
                                                        flexShrink: 0
                                                    }}>
                                                        {isChecked && <CheckSquare size={14} color="#000" />}
                                                    </div>
                                                    <span style={{
                                                        fontSize: '15px',
                                                        color: isChecked ? '#fff' : 'rgba(255, 255, 255, 0.8)',
                                                        flex: 1,
                                                        textDecoration: isChecked ? 'line-through' : 'none',
                                                        opacity: isChecked ? 0.7 : 1
                                                    }}>
                                                        {item.text}
                                                    </span>
                                                </div>
                                            )
                                        })}
                                    </div>
                                </div>
                            )
                        })}
                    </div>
                ) : (
                    /* Flat format (old) */
                    <div style={{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '12px'
                    }}>
                        {items.map((item) => {
                            const isChecked = checkedState[item.id] || false
                            return (
                                <div
                                    key={item.id}
                                    onClick={() => toggleItem(item.id)}
                                    style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '16px',
                                        padding: '16px 20px',
                                        background: isChecked ? 'rgba(0, 212, 255, 0.1)' : 'rgba(255, 255, 255, 0.05)',
                                        border: isChecked ? '1px solid rgba(0, 212, 255, 0.3)' : '1px solid rgba(255, 255, 255, 0.1)',
                                        borderRadius: '12px',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s'
                                    }}
                                >
                                    <div style={{
                                        width: '24px',
                                        height: '24px',
                                        borderRadius: '6px',
                                        border: isChecked ? 'none' : '2px solid rgba(255, 255, 255, 0.3)',
                                        background: isChecked ? '#00d4ff' : 'transparent',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        flexShrink: 0
                                    }}>
                                        {isChecked && <CheckSquare size={16} color="#000" />}
                                    </div>
                                    <span style={{
                                        fontSize: '16px',
                                        color: isChecked ? '#fff' : 'rgba(255, 255, 255, 0.8)',
                                        flex: 1,
                                        textDecoration: isChecked ? 'line-through' : 'none',
                                        opacity: isChecked ? 0.7 : 1
                                    }}>
                                        {item.text}
                                    </span>
                                </div>
                            )
                        })}
                    </div>
                )}
            </div>
        </div>
    )
}
