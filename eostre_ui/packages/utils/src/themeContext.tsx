"use client";
import { createContext, useContext, useState, ReactNode } from "react";

const ThemeContext = createContext({ isDark: false, setIsDark: (v: boolean) => {} });

export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const [isDark, setIsDark] = useState(() => localStorage.getItem("theme") === "dark");

  return (
    <ThemeContext.Provider value={{ isDark, setIsDark }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useThemeContext = () => useContext(ThemeContext);