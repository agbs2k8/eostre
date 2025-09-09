import { refreshRequest } from "./authClient";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "";

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
      throw err;
    }
  }

  if (!res.ok) throw new Error(`Error ${res.status}`);
  return res.json();
};