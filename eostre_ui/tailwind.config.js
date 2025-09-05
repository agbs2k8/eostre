/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./app/**/*.{js,ts,jsx,tsx}",    
        "./pages/**/*.{js,ts,jsx,tsx}",
        "./components/**/*.{js,ts,jsx,tsx}",
        "./packages/**/*.{js,ts,jsx,tsx}", 
    ],
    theme: {
        extend: {
            colors: {
                brand: {
                    50: "#fff5f5",
                    100: "#ffe3e3",
                    200: "#ffc9c9",
                    300: "#ffa8a8",
                    400: "#ff8787",
                    500: "#500000", // base maroon
                    600: "#400000",
                    700: "#2f0000",
                    800: "#1f0000",
                    900: "#0f0000",
                },
                accent: {
                    500: "#ab90c6", // secondary accent color
                },
                neutral: {
                    50: "#f9f9f9",
                    100: "#f2f2f2",
                    200: "#d9d9d9",
                    300: "#bfbfbf",
                    400: "#a6a6a6",
                    500: "#7d7d7d", // base
                    600: "#666666",
                    700: "#4d4d4d",
                    800: "#333333",
                    900: "#1a1a1a",
                }
            },
            fontFamily: {
                sans: ["var(--font-geist-sans)", "ui-sans-serif", "system-ui"],
                mono: ["var(--font-geist-mono)", "ui-monospace", "SFMono-Regular"],
            },
            spacing: {
                18: "4.5rem",
                22: "5.5rem",
                30: "7.5rem",
            },
            borderRadius: {
                xl: "1rem",
                "2xl": "1.5rem",
            },
        },
    },
    plugins: [],
};
