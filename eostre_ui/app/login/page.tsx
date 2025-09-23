"use client";

import { useState } from "react";
import { useAuth } from "@utils/authProvider";
import { useRouter } from "next/navigation";
import { Button } from "@ui-components/Button";

export default function LoginPage() {
  const { login } = useAuth();
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(username, password);
      router.push("/");
    } catch (err) {
      console.error("Login error:", err);
      setError("Invalid username or password");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="w-80 rounded bg-brand-light text-brand-dark dark:bg-brand-dark dark:text-brand-light p-6 shadow space-y-4"
      >
        <h1 className="text-xl font-bold">Login</h1>
        {error && <p className="text-red-500">{error}</p>}
        <input
          className="w-full rounded border p-2 bg-brand-light dark:bg-brand-dark dark:text-brand-light"
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          className="w-full rounded border p-2 bg-brand-light dark:bg-brand-dark dark:text-brand-light"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button type="submit" aria-label="Login">
          Login
        </Button>
      </form>
    </div>
  );
}
