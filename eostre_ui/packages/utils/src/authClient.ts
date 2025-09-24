const PUBLIC_ADMIN = process.env.NEXT_PUBLIC_ADMIN_API; // e.g. http://localhost:5000
// If PUBLIC_ADMIN defined, go direct (CORS must allow it); else use rewrite path.
const AUTH_BASE = PUBLIC_ADMIN ? `${PUBLIC_ADMIN.replace(/\/$/, "")}/auth` : "/auth";

export async function loginRequest(username: string, password: string) {
  const res = await fetch(`${AUTH_BASE}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
    credentials: "include",
  });

  if (!res.ok) throw new Error(`Login failed: ${res.status}`);
  return res.json();
}

export async function refreshRequest() {
  const res = await fetch(`${AUTH_BASE}/refresh`, {
    method: "POST",
    credentials: "include",
  });

  if (!res.ok) throw new Error(`Refresh failed: ${res.status}`);
  return res.json();
}

export async function logoutRequest() {
  const res = await fetch(`${AUTH_BASE}/logout`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
  });

  if (!res.ok) throw new Error(`Logout failed: ${res.status}`);
  return res.json();
}