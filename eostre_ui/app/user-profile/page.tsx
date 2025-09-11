"use client";

import { useAuth } from "@utils/authProvider";
import { useEffect, useState } from "react";
import { apiClient } from "@utils/apiClient";

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
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">My Profile</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Editable fields */}
        <div>
          <label className="block font-medium">Username</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="mt-1 block w-full border rounded p-2"
          />
        </div>

        <div>
          <label className="block font-medium">Personal Name</label>
          <input
            type="text"
            value={personalName}
            onChange={(e) => setPersonalName(e.target.value)}
            className="mt-1 block w-full border rounded p-2"
          />
        </div>

        <div>
          <label className="block font-medium">Family Names</label>
          <input
            type="text"
            value={familyNames}
            onChange={(e) => setFamilyNames(e.target.value)}
            className="mt-1 block w-full border rounded p-2"
          />
        </div>

        <div>
          <label className="block font-medium">Display Name</label>
          <input
            type="text"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            className="mt-1 block w-full border rounded p-2"
          />
        </div>

        {/* Read-only fields */}
        <div>
          <label className="block font-medium">Type</label>
          <p>{user.type}</p>
        </div>

        <div>
          <label className="block font-medium">Email</label>
          <p>{user.email}</p>
        </div>

        <div>
          <label className="block font-medium">Alternate Emails</label>
          <p>{user.alternate_emails.join(", ") || "—"}</p>
        </div>

        <div>
          <label className="block font-medium">Created</label>
          <p>{new Date(user.created_date).toLocaleString()}</p>
        </div>

        {/* Submit */}
        <button
          type="submit"
          disabled={saving}
          className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
        >
          {saving ? "Saving..." : "Save Changes"}
        </button>
      </form>
    </div>
  );
}
