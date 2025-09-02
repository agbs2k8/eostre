const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "";

export async function loginRequest(username: string, password: string) {
  const res = await fetch(`/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) throw new Error(`Login failed: ${res.status}`);
  return res.json();
}

export async function refreshRequest(refreshToken: string) {
  const res = await fetch(`/api/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });

  if (!res.ok) throw new Error(`Refresh failed: ${res.status}`);
  return res.json();
}
