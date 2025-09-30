"use client";

import { useState } from "react";
import { useAuth } from "@utils/authProvider";
import { Button } from "@ui-components/Button";
import clsx from "clsx";

interface AddEmailDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: (email: string) => void; // callback if needed
  targetUserId?: string; // allow override, defaults to logged-in user
}

export function AddEmailDrawer({
  isOpen,
  onClose,
  onSuccess,
  targetUserId,
}: AddEmailDrawerProps) {
  const { user, accessToken } = useAuth();
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  if (!isOpen) return null;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!email) return;

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const res = await fetch("/v1api/email/send_validation", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          email,
          target_user: targetUserId ?? user?.sub,
        }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.message || `Request failed: ${res.status}`);
      }

      const data = await res.json();
      setSuccess(`Validation sent to ${email}`);
      setEmail("");

      if (onSuccess) onSuccess(email);
    } catch (err: any) {
      setError(err.message || "Failed to send validation.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      className={clsx(
        "fixed inset-0 z-50 flex justify-end bg-black bg-opacity-40",
        isOpen ? "visible" : "invisible"
      )}
      onClick={onClose}
    >
      <div
        className="w-96 bg-white dark:bg-brand-dark text-brand-dark dark:text-brand-light p-6 shadow-xl h-full overflow-y-auto"
        onClick={(e) => e.stopPropagation()} // prevent close on inner click
      >
        <h2 className="text-xl font-bold mb-4">Add New Email</h2>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="email"
            placeholder="Enter new email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 p-2 border rounded bg-brand-light dark:bg-brand-dark dark:text-brand-light"
            required
          />

          <Button type="submit" disabled={loading}>
            {loading ? "Sending..." : "Send Validation"}
          </Button>
          <Button
            type="button"
            variant="secondary"
            onClick={onClose}
            className="mt-2"
          >
            Cancel
          </Button>
        </form>

        {error && <p className="text-red-500 mt-3">{error}</p>}
        {success && <p className="text-green-500 mt-3">{success}</p>}
      </div>
    </div>
  );
}
