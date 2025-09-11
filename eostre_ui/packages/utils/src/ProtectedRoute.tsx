"use client";

import { useAuth } from "@utils/authProvider";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace("/login");
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    // Optional: show spinner while redirecting
    return <div className="flex justify-center items-center h-screen">Redirecting...</div>;
  }

  return <>{children}</>;
}
