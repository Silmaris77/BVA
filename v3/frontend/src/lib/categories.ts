// Shared content categories for lessons, engrams, and resources
// All content types should use these same categories for consistency

export interface Category {
    id: string
    name: string
    color: string
    icon?: string
}

export const CONTENT_CATEGORIES: Category[] = [
    { id: 'all', name: 'Wszystkie', color: '#00d4ff' },
    { id: 'Wiedza produktowa', name: 'Wiedza produktowa', color: '#00ff88' },
    { id: 'Sprzedaż', name: 'Sprzedaż', color: '#b000ff' },
    { id: 'Leadership', name: 'Leadership', color: '#ffd700' },
    { id: 'Negocjacje', name: 'Negocjacje', color: '#ff6b6b' },
    { id: 'Produktywność', name: 'Produktywność', color: '#4ecdc4' },
    { id: 'Komunikacja', name: 'Komunikacja', color: '#ff8800' }
]

// Get category color by id (for cards, badges, etc.)
export function getCategoryColor(categoryId: string | null | undefined): string {
    if (!categoryId) return '#00d4ff'
    const category = CONTENT_CATEGORIES.find(c => c.id === categoryId)
    return category?.color || '#00d4ff'
}

// Get categories for filter UI (includes "Wszystkie")
export function getFilterCategories(): Category[] {
    return CONTENT_CATEGORIES
}

// Get categories for forms/dropdowns (excludes "Wszystkie")
export function getContentCategories(): Category[] {
    return CONTENT_CATEGORIES.filter(c => c.id !== 'all')
}
