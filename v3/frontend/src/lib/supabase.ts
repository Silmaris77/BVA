import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

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
  cards: any[]
  created_at: string
  updated_at: string
}

export type UserProgress = {
  id: string
  user_id: string
  lesson_id: string
  started_at: string
  completed_at: string | null
  current_card_index: number
  cards_completed: number
  total_cards: number | null
}
