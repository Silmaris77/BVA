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

  return (
    <html lang="pl" suppressHydrationWarning>
      <body className={outfit.className} suppressHydrationWarning>
        <div className="orb orb-1"></div>
        <div className="orb orb-2"></div>
        <div className="orb orb-3"></div>

        <AuthProvider>
          {!isAuthPage && !isLessonPlayer && <Sidebar />}
          {/* Main content with responsive margins - skip for fullscreen pages */}
          <div className={!isAuthPage && !isLessonPlayer ? 'main-content' : ''}>
            {!isAuthPage && !isLessonPlayer && (
              <Suspense fallback={<div style={{ height: '65px' }} />}>
                <GlobalTopBar />
              </Suspense>
            )}
            {children}
          </div>
          {!isAuthPage && !isLessonPlayer && <BottomNav />}
        </AuthProvider>
      </body>
    </html>
  )
}
