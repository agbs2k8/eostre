"use client";

import { useAuth } from "@utils/authProvider";
import { useEffect, useState } from "react";
import { apiClient } from "@utils/apiClient";
import { Button } from "@ui-components/Button";

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
  [accountId: string]: string[];
}

export interface User {
  id: number;
  name: string;
  display_name: string;
  personal_name: string | null;
  family_names: string | null;
  email: string;
  alternate_emails: string[];
  type: "service" | "person" | string;
  active: boolean;
  deleted: boolean;
  created_date: string;
  modified_date: string;
  grants: Grant[];
  permissions: Permissions;
}

export default function ProfilePage() {
  const { accessToken } = useAuth();
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  // Local state for editable fields
  const [name, setName] = useState("");
  const [personalName, setPersonalName] = useState("");
  const [familyNames, setFamilyNames] = useState("");
  const [displayName, setDisplayName] = useState("");

  useEffect(() => {
    async function fetchProfile() {
      try {
        const data = await apiClient<User>("/api/v1/user/me", accessToken);
        setUser(data);

        // Initialize form state
        setName(data.name);
        setPersonalName(data.personal_name ?? "");
        setFamilyNames(data.family_names ?? "");
        setDisplayName(data.display_name);
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

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!user) return;

    setSaving(true);
    setError(null);

    try {
      const updated = await apiClient<User>(
        "/api/v1/user/me",
        accessToken,
        {
          method: "POST",
          body: JSON.stringify({
            name,
            personal_name: personalName || null,
            family_names: familyNames || null,
            display_name: displayName,
          }),
        }
      );

      setUser(updated);
    } catch (err) {
      setError("Failed to save changes");
    } finally {
      setSaving(false);
    }
  }

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="text-red-500">{error}</p>;
  if (!user) return <p>No profile data</p>;

  return (
    <div className="flex min-h-screen justify-center">
      <form onSubmit={handleSubmit} className="w-80 rounded bg-brand-light text-brand-dark dark:bg-brand-dark dark:text-brand-light p-6 shadow space-y-4">
        <h1 className="text-2xl font-bold">User Profile</h1>
        {/* Editable fields */}
        <div>
          <label className="block font-medium bg-brand-light dark:bg-brand-dark dark:text-brand-light">Username</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="mt-1 block w-full border rounded p-2 dark:bg-brand-dark dark:text-brand-light"
          />
        </div>

        <div>
          <label className="block font-medium bg-brand-light dark:bg-brand-dark dark:text-brand-light">Personal Name</label>
          <input
            type="text"
            value={personalName}
            onChange={(e) => setPersonalName(e.target.value)}
            className="mt-1 block w-full border rounded p-2 dark:bg-brand-dark dark:text-brand-light"
          />
        </div>

        <div>
          <label className="block font-medium bg-brand-light dark:bg-brand-dark dark:text-brand-light">Family Names</label>
          <input
            type="text"
            value={familyNames}
            onChange={(e) => setFamilyNames(e.target.value)}
            className="mt-1 block w-full border rounded p-2 dark:bg-brand-dark dark:text-brand-light"
          />
        </div>

        <div>
          <label className="block font-medium bg-brand-light dark:bg-brand-dark dark:text-brand-light">Display Name</label>
          <input
            type="text"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            className="mt-1 block w-full border rounded p-2 dark:bg-brand-dark dark:text-brand-light"
          />
        </div>

        {/* Read-only fields */}
        <div>
          <label className="block font-medium bg-brand-light dark:bg-brand-dark dark:text-brand-light">Type</label>
          <p className="bg-brand-light dark:bg-brand-dark dark:text-brand-light">{user.type}</p>
        </div>

        <div>
          <label className="block font-medium bg-brand-light dark:bg-brand-dark dark:text-brand-light">Email</label>
          <p className="bg-brand-light dark:bg-brand-dark dark:text-brand-light">{user.email}</p>
        </div>

        <div>
          <label className="block font-medium bg-brand-light dark:bg-brand-dark dark:text-brand-light">Alternate Emails</label>
          <p className="bg-brand-light dark:bg-brand-dark dark:text-brand-light">{user.alternate_emails.join(", ") || "—"}</p>
        </div>

        <div>
          <label className="block font-medium bg-brand-light dark:bg-brand-dark dark:text-brand-light">Created</label>
          <p className="bg-brand-light dark:bg-brand-dark dark:text-brand-light">{new Date(user.created_date).toLocaleString()}</p>
        </div>

        {/* Submit */}
        <Button type="submit" aria-label="Submit">
          Submit
        </Button>
      </form>
    </div>
  );
}
