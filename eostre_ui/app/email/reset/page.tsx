"use client";

import { useSearchParams } from "next/navigation";

export default function ValidatePage() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");

  return <div>Validating token: {token}</div>;
}