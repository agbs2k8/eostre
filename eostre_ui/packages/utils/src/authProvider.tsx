"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { loginRequest, refreshRequest } from "./authClient";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode";

interface AuthContextType {
  accessToken: string | null;
  user?: { [key: string]: any };
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const router = useRouter();
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [user, setUser] = useState<AuthContextType["user"]>();

  // Auto-refresh on mount
  useEffect(() => {
    (async () => {
      try {
        const res = await refreshRequest();
        setAccessToken(res.access_token);
        setUser(jwtDecode(res.access_token));
      } catch {
        setAccessToken(null);
        setUser(undefined);
      }
    })();
  }, []);

  const login = async (username: string, password: string) => {
    const res = await loginRequest(username, password);
    setAccessToken(res.access_token);
    setUser(jwtDecode(res.access_token));
  };

  const logout = () => {
    setAccessToken(null);
    setUser(undefined);
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/auth/logout`, {
      method: "POST",
      credentials: "include",
    }).finally(() => {
      router.push("/login");
    });
  };

  return (
    <AuthContext.Provider value={{ accessToken, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
