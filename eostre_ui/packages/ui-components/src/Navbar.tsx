"use client";

import Link from "next/link";
import { Home, User, Menu } from "lucide-react"; // icons
import { useState } from "react";
import { Drawer } from "@ui-components/Drawer"

export function Navbar() {

  const [isNavOpen, setNavOpen] = useState(false);

  return (
    <>
      <nav className="fixed top-0 left-0 right-0 z-50 bg-brand-500 shadow-md">
        <div className="flex h-16 w-full items-center justify-between px-4 sm:px-6 lg:px-8">
          {/*Left side-icon and title */}
          <div className="flex item-center space-x-2">
            <button onClick={() => setNavOpen(prev => !prev)}
              className="p-1 rounded hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40"
              aria-label="Open navigation"
            >
              <Menu className="h-5 w-6 text-white hover:text-neutral-500" />
            </button>
            <Link className="text-xl font-bold text-neutral-50" href="/">
              Eostre
            </Link>
          </div>
          {/* Right side user/login info */}
          <div className="flex items-center space-x-4">
            <Link href="/login" className="text-neutral-50 hover:text-neutral-500">
              Login
            </Link>
            <User className="h-6 w-6 text-neutral-50 hover:text-neutral-500" />
          </div>
        </div>
      </nav>

      {/* Nav Drawer */}
      <Drawer
        isOpen={isNavOpen}
        onClose={() => setNavOpen(false)}
        //title="Navigation"
        side="left"
        variant="nav"
        offsetTop={64}
      >
        <nav className="flex flex-col space-y-4">
          <Link
            href="/"
            onClick={() => setNavOpen(false)}>
            <Home className="inline-block mr-2 h-4 w-4" /> Home
          </Link>
          <Link
            href="/location"
            onClick={() => setNavOpen(false)}>
            Locations
          </Link>
          <Link
            href="/login"
            onClick={() => setNavOpen(false)}>
            Login
          </Link>

        </nav>
      </Drawer>
    </>
  );
}
