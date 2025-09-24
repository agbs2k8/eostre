"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { apiClient } from "@utils/apiClient";
import { useAuth } from "@utils/authProvider";

export interface Grant {
  account_id: string;
  account_name: string;
  account_display_name: string;
  active: boolean;
  granted_date: string;
  id: string;
  revoked_date: string | null;
  role_id: number;
  role_name: string;
  user_id: number;
}

export interface Permissions {
  [accountId: string]: string[];
}

export interface Email {
  active: boolean,
  created_date: string,
  email: string,
  id: string,
  primary:boolean
}

export interface UserProfile {
  id: string;
  name: string;
  display_name: string;
  personal_name: string | null;
  family_names: string | null;
  emails: Email[];
  type: "service" | "person" | string;
  active: boolean;
  deleted: boolean;
  created_date: string;
  modified_date: string;
  grants: Grant[];
  permissions: Permissions;
}

interface UserContextValue {
  userProfile: UserProfile | null;
  loading: boolean;
  error: string | null;
  refreshUser: () => Promise<void>;
  updateUserProfile: (updates: Partial<UserProfile>) => Promise<UserProfile | null>;
}

const UserContext = createContext<UserContextValue | undefined>(undefined);

export function UserProvider({ children }: { children: React.ReactNode }) {
  const { accessToken } = useAuth();
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function fetchUser() {
    if (!accessToken) {
      setUserProfile(null);
      setLoading(false);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await apiClient<UserProfile>("/v1api/user/me", accessToken);
      setUserProfile(data);
    } catch (err) {
      setError("Failed to load user profile");
    } finally {
      setLoading(false);
    }
  }

  async function updateUserProfile(updates: Partial<UserProfile>) {
    if (!accessToken) return null;
    try {
      const updated = await apiClient<UserProfile>("/v1api/user/me", accessToken, {
        method: "POST",
        body: JSON.stringify(updates),
      });
      setUserProfile(updated);
      return updated;
    } catch (err) {
      setError("Failed to update profile");
      return null;
    }
  }

  useEffect(() => {
    fetchUser();
  }, [accessToken]);

  return (
    <UserContext.Provider
      value={{ userProfile, loading, error, refreshUser: fetchUser, updateUserProfile }}
    >
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const ctx = useContext(UserContext);
  if (!ctx) {
    throw new Error("useUser must be used inside a UserProvider");
  }
  return ctx;
}