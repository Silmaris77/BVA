'use client'

import { Outfit } from "next/font/google"
import { AuthProvider } from "@/contexts/AuthContext"
import { ThemeProvider } from "@/contexts/ThemeContext"
import { AIConversationProvider } from "@/contexts/AIConversationContext"
import AIConversationWidget from "@/components/ai/ConversationWidget"
import Sidebar from "@/components/Navigation"
import BottomNav from "@/components/BottomNav"
import GlobalTopBar from "@/components/layout/GlobalTopBar"
import EffectsOverlay from "@/components/layout/EffectsOverlay"
import { usePathname } from "next/navigation"
import { Suspense } from "react"
import "./globals.css"

const outfit = Outfit({ subsets: ["latin"] })

// Force rebuild for theme CSS

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  const pathname = usePathname()

  // Don't show sidebar on auth pages or lesson player
  const isAuthPage = pathname?.startsWith('/auth')
  const isLessonPlayer = pathname?.match(/^\/lessons\/[^\/]+$/) // matches /lessons/[id] but not /lessons
  const isLessonEditor = pathname?.startsWith('/admin/lessons/create')
  const isConsultingGame = pathname?.startsWith('/practice/games/consulting')
  const isBrainVenture = pathname?.startsWith('/brainventure')

  const isFullscreen = isAuthPage || isLessonPlayer || isLessonEditor || isConsultingGame || isBrainVenture

  return (
    <html lang="pl" suppressHydrationWarning>
      <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
        <link href="https://fonts.googleapis.com/css2?family=Rubik+Glitch&family=Rubik+Wet+Paint&display=swap&subset=latin,latin-ext" rel="stylesheet" />
      </head>
      <body className={outfit.className} suppressHydrationWarning>
        <div className="orb orb-1"></div>
        <div className="orb orb-2"></div>
        <div className="orb orb-3"></div>

        <AuthProvider>
          <ThemeProvider>
            <AIConversationProvider>
              <EffectsOverlay />
              {!isFullscreen && <Sidebar />}
              {/* Main content with responsive margins - skip for fullscreen pages */}
              <div className={!isFullscreen ? 'main-content' : ''}>
                {!isFullscreen && (
                  <Suspense fallback={<div style={{ height: '65px' }} />}>
                    <GlobalTopBar />
                  </Suspense>
                )}
                {children}
              </div>
              {!isFullscreen && <BottomNav />}
              <AIConversationWidget />
            </AIConversationProvider>
          </ThemeProvider>
        </AuthProvider>
      </body>
    </html>
  )
}
