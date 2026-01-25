'use client'

import { Outfit } from "next/font/google"
import { AuthProvider } from "@/contexts/AuthContext"
import Sidebar from "@/components/Navigation"
import BottomNav from "@/components/BottomNav"
import GlobalTopBar from "@/components/layout/GlobalTopBar"
import { usePathname } from "next/navigation"
import { Suspense } from "react"
import "./globals.css"

const outfit = Outfit({ subsets: ["latin"] })

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

  const isFullscreen = isAuthPage || isLessonPlayer || isLessonEditor

  return (
    <html lang="pl" suppressHydrationWarning>
      <body className={outfit.className} suppressHydrationWarning>
        <div className="orb orb-1"></div>
        <div className="orb orb-2"></div>
        <div className="orb orb-3"></div>

        <AuthProvider>
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
        </AuthProvider>
      </body>
    </html>
  )
}
