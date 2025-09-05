"use client";

import Link from "next/link";

export function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-brand-500 shadow-md">
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="text-xl font-bold text-white">
          <Link href="/">Eostre</Link>
        </div>

        <div className="flex space-x-6">
          <Link href="/location" className="text-white hover:text-gray-200">
            Locations
          </Link>
          <Link href="/login" className="text-white hover:text-gray-200">
            Login
          </Link>
          <Link href="/register" className="text-white hover:text-gray-200">
            Register
          </Link>
        </div>
      </div>
    </nav>
  );
}
