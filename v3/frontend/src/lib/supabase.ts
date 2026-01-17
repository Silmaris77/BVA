import { createClient } from './supabase/client'

// Use the cookie-based SSR client for browser authentication
// This ensures server-side API routes can access the user session
export const supabase = createClient()

// Types for our database
export type Profile = {
  id: string
  email: string | null
  full_name: string | null
  avatar_url: string | null
  organization_id: string | null
  role: string
  xp: number
  level: number
  theme_preference: string
  created_at: string
  updated_at: string
}

export type Lesson = {
  id: string
  title: string
  description: string | null
  category: string | null
  difficulty: string | null
  estimated_minutes: number | null
  xp_reward: number
  target_roles: string[]
  is_public: boolean
  content_json: {
    cards: any[]
  }
  created_at: string
  updated_at: string
}

export type UserProgress = {
  id: string
  user_id: string
  lesson_id: string
  started_at: string | null
  completed_at: string | null
  current_card_index: number
  updated_at: string
}

export type Engram = {
  id: string
  title: string
  category: string
  description: string | null
  content_json: {
    slides: any[]
    quiz: any[]
  }
  source_lesson_id: string | null
  xp_reward: number
  estimated_minutes: number
  created_at: string
}

export type UserEngram = {
  id: string
  user_id: string
  engram_id: string
  installed_at: string
  last_refreshed_at: string | null
  strength: number // 0-100
  times_refreshed: number
  status: 'active' | 'archived'
}

export type Resource = {
  id: string
  title: string
  type: 'article' | 'video' | 'template' | 'ebook'
  url: string | null
  description: string | null
  category: string
  image_url: string | null
  is_locked: boolean
  xp_cost: number
  created_at: string
}
