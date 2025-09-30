"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { useAuth } from "@utils/authProvider";
import { apiClient } from "@utils/apiClient";
import { useRouter } from "next/navigation";

interface ApiResponse {
  result: string;
}

export default function ValidatePage() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const router = useRouter();
  const { isAuthenticated, refresh } = useAuth();
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [message, setMessage] = useState<string>("");

  useEffect(() => {
    if (!token) {
      setStatus("error");
      setMessage("No token provided in the URL.");
      return;
    }

    const validateEmail = async () => {
      try {
        const response = await apiClient<ApiResponse>("/v1api/email/validate", null, {
          method: "POST",
          body: JSON.stringify({ token }),
        });

        setStatus("success");
        setMessage(response.result);
      } catch (err: any) {
        setStatus("error");
        setMessage(err.result || "Validation failed.");
      }
    };
    validateEmail();
  }, [token]);

  useEffect(() => {
    if (status === "success") {
      const timer = setTimeout(async () => {
        // Try refreshing in case they were logged in but token expired
        await refresh();
        if (isAuthenticated) {
          router.push("/user-profile");
        } else {
          router.push("/login");
        }
      }, 4000);

      return () => clearTimeout(timer);
    }
  }, [status, isAuthenticated, refresh, router]);

  return (
    <div className="font-sans flex min-h-screen items-center justify-center bg-brand-light text-brand-dark dark:bg-brand-dark dark:text-brand-light">
      <div className="flex flex-col items-center justify-center border border-brand-dark dark:border-brand-light rounded-lg p-6">
        <h1 className="text-xl font-bold mb-4">Email Validation</h1>

        {status === "loading" && (
          <p className="bg-brand-light text-brand-dark dark:bg-brand-dark dark:text-brand-light">
            Validating your email…
          </p>)}
        {status === "success" && (
          <p className="bg-brand-light text-brand-dark dark:bg-brand-dark dark:text-brand-light">
            {message} <br/> Redirecting shortly...
          </p>
        )}
        {status === "error" && (
          <p className="bg-brand-light text-brand-primary">
            {message}
          </p>
        )}
      </div>
    </div>
  );
}