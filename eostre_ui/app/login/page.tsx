"use client";

import { useState } from "react";
import { useAuth, AuthProvider } from "@utils/authProvider"
import { useRouter } from "next/navigation";

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
      router.push("/location");
    } catch (err) {
      setError("Invalid username or password");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="w-80 rounded bg-white p-6 shadow space-y-4"
      >
        <h1 className="text-xl font-bold text-gray-700">Login</h1>
        {error && <p className="text-red-500">{error}</p>}
        <input
          className="w-full rounded border p-2 text-gray-700 placeholder-gray-400"
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          className="w-full rounded border p-2 text-gray-700 placeholder-gray-400"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          type="submit"
          className="w-full rounded bg-blue-500 p-2 text-white"
        >
          Login
        </button>
      </form>
    </div>
  );
}
