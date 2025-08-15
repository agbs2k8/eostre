// ui/packages/utils/src/apiClient.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "";

export const apiClient = async <T>(path: string, options?: RequestInit): Promise<T> => {
  const url = `${API_BASE_URL}${path}`;
  const res = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
    ...options,
  });

  if (!res.ok) throw new Error(`Error ${res.status}`);
  return res.json();
};
