"use client";

import Link from "next/link";
import { Home, User, Menu } from "lucide-react"; // example icon

export function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-brand-500 shadow-md">
      <div className="flex h-16 w-full items-center justify-between px-4 sm:px-6 lg:px-8">
        {/*Left side-icon and title */}
        <div className="flex item-center space-x-2"> 
            <Menu className="h-7 w-6 text-white hover:text-neutral-500" />
            <Link  className="text-xl font-bold text-neutral-50" href="/">Eostre</Link>
            
        </div>

        <div className="flex items-center space-x-4">
          <Link href="/location" className="text-neutral-50 hover:text-neutral-500">
            Locations
          </Link>
          <Link href="/login" className="text-neutral-50 hover:text-neutral-500">
            Login
          </Link>
          <User className="h-6 w-6 text-neutral-50 hover:text-neutral-500" />
        </div>
      </div>
    </nav>
  );
}
