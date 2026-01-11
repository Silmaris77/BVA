import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "var(--background)",
                foreground: "var(--foreground)",
                glass: {
                    border: "rgba(255, 255, 255, 0.2)",
                    surface: "rgba(255, 255, 255, 0.05)",
                    highlight: "rgba(255, 255, 255, 0.1)",
                },
                neon: {
                    blue: "#00f3ff",
                    purple: "#bc13fe",
                    green: "#0aff68",
                }
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'glass-gradient': 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
                'main-bg': 'linear-gradient(135deg, #1a1c2e 0%, #0f1016 100%)',
            },
            backdropBlur: {
                xs: '2px',
            }
        },
    },
    plugins: [],
};
export default config;
