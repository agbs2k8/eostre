"use client";

import { useEffect, useState } from "react";
import { Button } from "@ui-components/Button";
import { ProtectedRoute } from "@utils/ProtectedRoute";
import { useUser } from "@utils/userProvider";
import { useAuth } from "@utils/authProvider";

export default function ProfilePage() {
  return (
    <ProtectedRoute>
      <ProfileForm />
    </ProtectedRoute>
  );
}

function ProfileForm() {
  const { accessToken, user } = useAuth();
  const { userProfile, loading, error, updateUserProfile } = useUser();

  // Local state for editable fields
  const [name, setName] = useState("");
  const [personalName, setPersonalName] = useState("");
  const [familyNames, setFamilyNames] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [saving, setSaving] = useState(false);

useEffect(() => {
    if (userProfile) {
      setName(userProfile.name);
      setPersonalName(userProfile.personal_name ?? "");
      setFamilyNames(userProfile.family_names ?? "");
      setDisplayName(userProfile.display_name);
    }
  }, [userProfile]);

async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!userProfile) return;

    setSaving(true);
    await updateUserProfile({
      name,
      personal_name: personalName || null,
      family_names: familyNames || null,
      display_name: displayName,
    });
    setSaving(false);
  }

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="text-red-500">{error}</p>;
  if (!user) return <p>No profile data</p>;

  return (
    <>
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
              <p className="bg-brand-light dark:bg-brand-dark dark:text-brand-light">{userProfile.type}</p>
            </div>

            <div>
              <label className="block font-medium bg-brand-light dark:bg-brand-dark dark:text-brand-light">Email</label>
              <p className="bg-brand-light dark:bg-brand-dark dark:text-brand-light">{userProfile.email}</p>
            </div>

            <div>
              <label className="block font-medium bg-brand-light dark:bg-brand-dark dark:text-brand-light">Alternate Emails</label>
              <p className="bg-brand-light dark:bg-brand-dark dark:text-brand-light">{userProfile.alternate_emails.join(", ") || "—"}</p>
            </div>

            <div>
              <label className="block font-medium bg-brand-light dark:bg-brand-dark dark:text-brand-light">Created</label>
              <p className="bg-brand-light dark:bg-brand-dark dark:text-brand-light">{new Date(userProfile.created_date).toLocaleString()}</p>
            </div>

            {/* Submit */}
            <Button type="submit" aria-label="Submit">
              Submit
            </Button>
          </form>
        </div>
    </>
  );
}
