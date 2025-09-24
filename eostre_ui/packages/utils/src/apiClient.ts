import { refreshRequest } from "./authClient";

// Always use relative URLs so Next.js rewrites/proxy can handle routing
const API_BASE_URL = "";

export const apiClient = async <T>(
  path: string,
  accessToken: string | null,
  options?: RequestInit
): Promise<T> => {
  let res = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
      ...(options?.headers || {}),
    },
    credentials: "include",
    ...options,
  });

  // Handle expired token → try refresh
  if (res.status === 401) {
    try {
      const newTokens = await refreshRequest();
      accessToken = newTokens.access_token;

      res = await fetch(`${API_BASE_URL}${path}`, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
          ...(options?.headers || {}),
        },
        credentials: "include",
        ...options,
      });
    } catch (err) {
      throw err; // bubble up if refresh fails
    }
  }

  if (!res.ok) {
    throw new Error(`Error ${res.status}: ${res.statusText}`);
  }

  return res.json();
};
