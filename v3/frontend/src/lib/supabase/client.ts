import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
    // Prevent execution on server side to avoid "document is not defined" errors during build/SSR
    if (typeof window === 'undefined') {
        return null as any
    }

    return createBrowserClient(
        process.env.NEXT_PUBLIC_SUPABASE_URL!,
        process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
        {
            cookies: {
                get(name: string) {
                    if (typeof document === 'undefined') return undefined
                    // Get cookie using document.cookie
                    const value = `; ${document.cookie}`;
                    const parts = value.split(`; ${name}=`);
                    if (parts.length === 2) {
                        return parts.pop()?.split(';').shift();
                    }
                },
                set(name: string, value: string, options: any) {
                    if (typeof document === 'undefined') return
                    // Set cookie using document.cookie
                    let cookie = `${name}=${value}`;

                    if (options?.maxAge) {
                        cookie += `; max-age=${options.maxAge}`;
                    }
                    if (options?.path) {
                        cookie += `; path=${options.path}`;
                    }
                    if (options?.domain) {
                        cookie += `; domain=${options.domain}`;
                    }
                    if (options?.sameSite) {
                        cookie += `; samesite=${options.sameSite}`;
                    }
                    if (options?.secure) {
                        cookie += '; secure';
                    }

                    document.cookie = cookie;
                },
                remove(name: string, options: any) {
                    if (typeof document === 'undefined') return
                    // Remove cookie by setting it to expire
                    let cookie = `${name}=; max-age=0`;

                    if (options?.path) {
                        cookie += `; path=${options.path}`;
                    }
                    if (options?.domain) {
                        cookie += `; domain=${options.domain}`;
                    }

                    document.cookie = cookie;
                },
            },
        }
    )
}
