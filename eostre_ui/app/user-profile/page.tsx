"use client";

import { useAuth } from "@utils/authProvider";
import { useEffect, useState } from "react";
import { apiClient } from "@utils/apiClient";
import { ProtectedRoute } from "@utils/ProtectedRoute";


export interface Grant {
  account_id: number;
  account_name: string;
  active: boolean;
  granted_date: string;   // ISO datetime
  id: number;
  revoked_date: string | null;
  role_id: number;
  role_name: string;
  user_id: number;
}

export interface Permissions {
  [accountId: string]: string[]; // e.g. "1": ["account.read", "account.write"]
}

export interface User {
  id: number;
  name: string; // system username (e.g. "master_service_account")
  display_name: string;
  personal_name: string | null;
  family_names: string | null;
  email: string;
  alternate_emails: string[];
  type: "service" | "person" | string; // restrict or leave open
  active: boolean;
  deleted: boolean;
  created_date: string;   // ISO datetime
  modified_date: string;  // ISO datetime
  grants: Grant[];
  permissions: Permissions;
}


export default function ProfilePage() {
  const { accessToken } = useAuth();
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchProfile() {
      try {
        const data = await apiClient<User>("/api/v1/user/me", accessToken);
        setUser(data);
      } catch (err) {
        setError("Failed to load profile");
      } finally {
        setLoading(false);
      }
    }
    if (accessToken) {
      fetchProfile();
    } else {
      setLoading(false);
    }
  }, [accessToken]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="text-red-500">{error}</p>;
  if (!user) return <p>No profile data</p>;

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">My Profile</h1>

      <p><strong>Username:</strong> {user.name}</p>
      <p><strong>Personal Name:</strong> {user.personal_name ?? "—"}</p>
      <p><strong>Family Names:</strong> {user.family_names ?? "—"}</p>
      <p><strong>Display Name:</strong> {user.display_name}</p>
      <p><strong>Type:</strong> {user.type}</p>
      <p><strong>Email:</strong> {user.email}</p>
      <p><strong>Alternate Emails:</strong> {user.alternate_emails.join(", ")}</p>
      <p><strong>Created:</strong> {new Date(user.created_date).toLocaleString()}</p>
    </div>
  );
}