"use client";

import Link from "next/link";
import { Home, User, Menu, ToggleLeft, ToggleRight } from "lucide-react";
import { useState, useEffect } from "react";
import { Drawer } from "@ui-components/Drawer";
import { useAuth } from "@utils/authProvider";
import { Tooltip } from "@ui-components/Tooltip"

export function Navbar() {
  const [isDark, setIsDark] = useState(false);
  const [isNavOpen, setNavOpen] = useState(false);
  const { accessToken, user, logout } = useAuth();

  const getInitials = (name: string | undefined) => {
    if (!name) return "~";
    return name[0].toUpperCase();
  };

  // Apply/remove 'dark' class on <html> element
  useEffect(() => {
    const root = window.document.documentElement;
    if (isDark) {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
  }, [isDark]);

  // Determine text color based on theme
  const textColor = isDark ? "text-brand-light" : "text-brand-dark";
  const hoverColor = isDark ? "hover:text-brand-muted" : "hover:text-brand-primary";

  return (
    <>
      <nav className={`fixed top-0 left-0 right-0 z-50 bg-brand-primary shadow-md`}>
        <div className="flex h-16 w-full items-center justify-between px-4 sm:px-6 lg:px-8">
          {/* Left: Menu + Title */}
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setNavOpen(prev => !prev)}
              className="p-1 rounded hover:bg-black/10 dark:hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-brand-primary"
              aria-label="Open navigation"
            >
              <Menu className={`h-5 w-6 text-white`} />
            </button>
            <Link href="/" className={`text-xl font-bold text-white`}>
              Eostre
            </Link>
          </div>

          {/* Right: User/Login + Dark Mode Toggle */}
          <div className="flex items-center space-x-4">
            {!accessToken ? (
              <>
                <Link href="/login" className="text-white flex items-center gap-1">
                  Login
                  <User className="h-6 w-6 text-white" />
                </Link>
              </>
            ) : (
              <div className="flex items-center gap-2">
                {/* Logout button */}
                <button
                  onClick={logout}
                  className="text-white hover:text-gray-200 flex items-center gap-1"
                >
                  Logout
                </button>

                {/* User initials circle */}
                <div
                  className="w-8 h-8 rounded-full bg-white text-brand-primary flex items-center justify-center font-bold text-sm">

                  {getInitials(user?.username)}
                </div>
              </div>
            )}
            <button
              onClick={() => setIsDark(!isDark)}
              className="p-1 rounded hover:bg-black/10 dark:hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-brand-primary"
              aria-label="Toggle dark mode"
            >
              {isDark ? (
                <Tooltip text="Enable light mode" position="left">
                  <ToggleLeft className="h-5 w-5 text-gray-700" />
                </Tooltip>
              ) : (
                <Tooltip text="Enable dark mode" position="left">
                  <ToggleRight className="h-5 w-5 text-gray-300" />
                </Tooltip>
              )}
            </button>
          </div>
        </div>
      </nav>

      {/* Navigation Drawer */}
      <Drawer
        isOpen={isNavOpen}
        onClose={() => setNavOpen(false)}
        side="left"
        variant="nav"
      >
        <nav className="flex flex-col space-y-4">
          <Link className="text-white" href="/" onClick={() => setNavOpen(false)}>
            <Home className="inline-block mr-2 h-4 w-4 text-white" /> Home
          </Link>
          <Link className="text-white" href="/location" onClick={() => setNavOpen(false)}>
            Locations
          </Link>
          <Link className="text-white" href="/user-profile" onClick={() => setNavOpen(false)}>
            User Profile
          </Link>
          {!accessToken ? (
            <Link className="text-white" href="/login" onClick={() => setNavOpen(false)}>
              Login
            </Link>
          ) : (
            <button
              className="text-white text-left"
              onClick={() => {
                logout();
                setNavOpen(false);
              }}
            >
              Logout
            </button>
          )}
        </nav>
      </Drawer>
    </>
  );
}
