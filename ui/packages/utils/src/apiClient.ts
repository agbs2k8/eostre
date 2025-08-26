import { refreshRequest } from "./authClient";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "";

export const apiClient = async <T>(
  path: string,
  options?: RequestInit
): Promise<T> => {
  const accessToken = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;

  let res = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
      ...(options?.headers || {}),
    },
    ...options,
  });

  if (res.status === 401) {
    const refreshToken = localStorage.getItem("refresh_token");
    if (refreshToken) {
      try {
        const newTokens = await refreshRequest(refreshToken);
        localStorage.setItem("access_token", newTokens.access_token);

        // retry the request with new access token
        res = await fetch(`${API_BASE_URL}${path}`, {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${newTokens.access_token}`,
            ...(options?.headers || {}),
          },
          ...options,
        });
      } catch (err) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        throw err;
      }
    }
  }

  if (!res.ok) throw new Error(`Error ${res.status}`);
  return res.json();
};
