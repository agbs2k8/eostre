"use client";

import React, { createContext, useContext, useState, useCallback, useEffect } from "react";
import { jwtDecode } from "jwt-decode";
import { loginRequest, refreshRequest } from "./authClient";
import { useRouter } from "next/navigation";

interface TokenPayload {
  sub: string;
  username: string;
  type?: string;
  account_id?: string;
  permissions?: Record<string, unknown>;
  iat?: number;
  exp?: number;
}

interface AuthContextType {
  accessToken: string | null;
  user: TokenPayload | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  refresh: () => Promise<void>;
  isAuthenticated: boolean | false;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const ACCESS_TOKEN_KEY = "ACCESS_TOKEN";

function safeDecode(token: string): TokenPayload | null {
  try {
    return jwtDecode<TokenPayload>(token);
  } catch {
    return null;
  }
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [user, setUser] = useState<TokenPayload | null>(null);
  const router = useRouter();

  // Load from localStorage on mount (client side)
  useEffect(() => {
    const saved = typeof window !== "undefined" ? localStorage.getItem(ACCESS_TOKEN_KEY) : null;
    if (saved) {
      const payload = safeDecode(saved);
      if (payload?.username) {
        setAccessToken(saved);
        setUser(payload);
      } else {
        localStorage.removeItem(ACCESS_TOKEN_KEY);
      }
    }
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    const res = await loginRequest(username, password);
    // Expecting { access_token: "...", refresh_expires_in?, ... }
    const token = res.access_token;
    if (!token) throw new Error("Missing access_token in response");
    const payload = safeDecode(token);
    if (!payload?.username) throw new Error("Invalid token payload");
    setAccessToken(token);
    setUser(payload);
    localStorage.setItem(ACCESS_TOKEN_KEY, token);
  }, []);

  const refresh = useCallback(async () => {
    try {
      const res = await refreshRequest();
      const token = res.access_token;
      if (!token) return;
      const payload = safeDecode(token);
      if (!payload?.username) return;
      setAccessToken(token);
      setUser(payload);
      localStorage.setItem(ACCESS_TOKEN_KEY, token);
    } catch {
      // Silent fail; could auto-logout
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      // Call backend to clear refresh cookie
      await fetch("/api/auth/logout", {
        method: "POST",
        credentials: "include",
      });
    } catch (err) {
      console.error("Logout request failed:", err);
    }
    // Clear client state
    setAccessToken(null);
    setUser(null);
    localStorage.removeItem(ACCESS_TOKEN_KEY);

    router.push("/");
  }, [router]);

  // Optional: auto refresh shortly before expiry
  useEffect(() => {
    if (!accessToken || !user?.exp) return;
    const now = Math.floor(Date.now() / 1000);
    const secondsLeft = user.exp - now;
    if (secondsLeft <= 0) {
      logout();
      return;
    }
    // refresh 30s before expiry
    const timeout = setTimeout(() => {
      refresh();
    }, Math.max((secondsLeft - 30) * 1000, 5_000));
    return () => clearTimeout(timeout);
  }, [accessToken, user, refresh, logout]);

  const isAuthenticated = Boolean(accessToken);

  return (
    <AuthContext.Provider value={{ accessToken, user, login, logout, refresh, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider")
  const isAuthenticated = Boolean(ctx.accessToken);
  return { ...ctx, isAuthenticated };
}