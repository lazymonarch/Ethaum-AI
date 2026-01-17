// components/Navbar.tsx - Role-aware navigation

"use client";

import { UserButton, useUser } from "@clerk/nextjs";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const { user } = useUser();
  const pathname = usePathname();
  const role = user?.publicMetadata?.role as string;

  const isActive = (path: string) => pathname === path;

  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/dashboard" className="flex items-center">
              <span className="text-xl font-bold text-gray-900">
                EthAum.ai
              </span>
            </Link>

            <div className="hidden sm:ml-8 sm:flex sm:space-x-8">
              <Link
                href="/dashboard"
                className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${
                  isActive("/dashboard")
                    ? "text-blue-600 border-b-2 border-blue-600"
                    : "text-gray-500 hover:text-gray-700"
                }`}
              >
                Dashboard
              </Link>

              {role === "startup" && (
                <>
                  <Link
                    href="/launches"
                    className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${
                      isActive("/launches")
                        ? "text-blue-600 border-b-2 border-blue-600"
                        : "text-gray-500 hover:text-gray-700"
                    }`}
                  >
                    Launches
                  </Link>
                  <Link
                    href="/reviews"
                    className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${
                      isActive("/reviews")
                        ? "text-blue-600 border-b-2 border-blue-600"
                        : "text-gray-500 hover:text-gray-700"
                    }`}
                  >
                    Reviews
                  </Link>
                </>
              )}

              {role === "enterprise" && (
                <Link
                  href="/startups"
                  className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${
                    isActive("/startups")
                      ? "text-blue-600 border-b-2 border-blue-600"
                      : "text-gray-500 hover:text-gray-700"
                  }`}
                >
                  Discover Startups
                </Link>
              )}

              {role === "admin" && (
                <Link
                  href="/admin"
                  className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${
                    isActive("/admin")
                      ? "text-blue-600 border-b-2 border-blue-600"
                      : "text-gray-500 hover:text-gray-700"
                  }`}
                >
                  Admin
                </Link>
              )}
            </div>
          </div>

          <div className="flex items-center">
            <UserButton afterSignOutUrl="/" />
          </div>
        </div>
      </div>
    </nav>
  );
}