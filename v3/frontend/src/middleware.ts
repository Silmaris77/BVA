import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(req: NextRequest) {
    // Temporarily disabled - using client-side auth protection via AuthContext
    // TODO: Fix Supabase cookie detection for server-side protection
    return NextResponse.next()
}

export const config = {
    matcher: ['/', '/lessons/:path*', '/profile/:path*', '/auth/:path*']
}
