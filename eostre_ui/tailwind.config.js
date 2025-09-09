/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./packages/ui-components/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class", // toggle with <html class="dark">
  theme: {
    extend: {
      colors: {
        brand: {
          primary: "#500000",          // main brand color for header/buttons
          "secondary": "#3E2C28",
          light: "#FEFEFE",            // light background variant
          dark: "#1F1F1F",             // dark background variant
          muted: "#A1A1A1",            // subtle text / border
          accent: "#9C9C9C",           // secondary accent for hover, highlights
          text: "#3E3E3E",             // default text in light mode
          "text-dark": "#FEFEFE",      // text in dark mode
          "bg-light": "#FEFEFE",       // page background in light mode
          "bg-dark": "#1F1F1F",        // page background in dark mode
        },
        neutral: {
          50: "#FEFEFE",
          100: "#F7F7F7",
          200: "#E5E5E5",
          300: "#D4D4D4",
          400: "#A1A1A1",
          500: "#9C9C9C",
          600: "#6B6B6B",
          700: "#3E3E3E",
          800: "#2C2C2C",
          900: "#1A1A1A",
        },
      },
      fontFamily: {
        sans: ["var(--font-geist-sans)", "ui-sans-serif", "system-ui"],
        mono: ["var(--font-geist-mono)", "ui-monospace", "SFMono-Regular"],
      },
    },
  },
  plugins: [],
};
