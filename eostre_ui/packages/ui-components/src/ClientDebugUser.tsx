"use client";

import { useAuth } from "@utils/authProvider";

export function ClientDebugUser() {
  const { user, accessToken } = useAuth();

  if (!accessToken) return <div>No User Found</div>;

  return <pre>{JSON.stringify(user, null, 2)}</pre>;
}
