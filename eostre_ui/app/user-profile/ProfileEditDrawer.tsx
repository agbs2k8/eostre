"use client";

import { useState } from "react";
import { Button } from "@ui-components/Button";
import { useUser } from "@utils/userProvider";

export default function ProfileEditDrawer({ userProfile, onClose }: { userProfile: any, onClose: () => void }) {
  const { updateUserProfile } = useUser();

  const [displayName, setDisplayName] = useState(userProfile.display_name);
  const [personalName, setPersonalName] = useState(userProfile.personal_name ?? "");
  const [familyNames, setFamilyNames] = useState(userProfile.family_names ?? "");
  const [saving, setSaving] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    await updateUserProfile({
      ...userProfile,
      display_name: displayName,
      personal_name: personalName || null,
      family_names: familyNames || null,
    });
    setSaving(false);
    onClose();
  }

  return (
    <div className="fixed inset-0 z-50 flex">
      {/* Overlay */}
      <div
        className="flex-1 bg-black/50"
        onClick={onClose}
      />
      {/* Drawer */}
      <div className="w-full max-w-md bg-white dark:bg-gray-900 p-6 shadow-lg overflow-y-auto">
        <h2 className="text-xl font-bold mb-4">Edit Profile</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block font-medium">Display Name</label>
            <input
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              className="w-full border rounded p-2 text-black"
            />
          </div>
          <div>
            <label className="block font-medium">Personal Name</label>
            <input
              type="text"
              value={personalName}
              onChange={(e) => setPersonalName(e.target.value)}
              className="w-full border rounded p-2 text-black"
            />
          </div>
          <div>
            <label className="block font-medium">Family Names</label>
            <input
              type="text"
              value={familyNames}
              onChange={(e) => setFamilyNames(e.target.value)}
              className="w-full border rounded p-2 text-black"
            />
          </div>
          <div className="flex justify-end gap-2">
            <Button type="button" variant="secondary" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" disabled={saving}>
              {saving ? "Saving..." : "Save"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
