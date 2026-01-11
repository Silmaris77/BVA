import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";
import { MobileNav } from "@/components/layout/MobileNav";
import { LayoutProvider } from "@/context/LayoutContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Brain Venture Academy v2",
  description: "Centrum dowodzenia Twoim rozwojem",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pl">
      <body className={inter.className}>
        <LayoutProvider>
          {/* Main App Wrapper - Controlled by Theme via CSS */}
          <div className="app-wrapper flex min-h-screen relative overflow-x-hidden transition-colors duration-500">
            {/* Background Gradients - Controlled by Theme via CSS */}
            <div className="bg-gradient-blobs fixed inset-0 z-0 pointer-events-none">
              <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] rounded-full bg-purple-900/20 blur-[100px]" />
              <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] rounded-full bg-blue-900/20 blur-[100px]" />
            </div>

            {/* Główny Sidebar (Desktop) */}
            <Sidebar />

            {/* Mobile Navigation */}
            <MobileNav />

            {/* Główna zawartość */}
            <main className="flex-1 relative z-10 w-full md:pl-20 lg:pl-64 transition-all duration-300">
              <div className="p-4 md:p-8 max-w-7xl mx-auto md:pb-8 pb-24">
                {/* pb-24 dodane, aby treść nie chowała się pod MobileNav na telefonach */}
                {children}
              </div>
            </main>
          </div>
        </LayoutProvider>
      </body>
    </html>
  );
}
