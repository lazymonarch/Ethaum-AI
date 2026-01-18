// components/Navbar.tsx

"use client";

import { UserButton, useUser } from "@clerk/nextjs";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const { user } = useUser();
  const pathname = usePathname();

  // ✅ Single source of truth (as YOU observed correctly)
  const role = user?.unsafeMetadata?.role as
    | "startup"
    | "enterprise"
    | "admin"
    | undefined;

  const isActive = (path: string) => pathname === path;

  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Left */}
          <div className="flex items-center">
            <Link href="/dashboard" className="text-xl font-bold text-gray-900">
              EthAum.ai
            </Link>

            <div className="hidden sm:ml-8 sm:flex sm:space-x-8">
              <NavLink href="/dashboard" active={isActive("/dashboard")}>
                Dashboard
              </NavLink>

              {role === "startup" && (
                <>
                  <NavLink href="/launches" active={isActive("/launches")}>
                    Launches
                  </NavLink>
                  <NavLink href="/reviews" active={isActive("/reviews")}>
                    Reviews
                  </NavLink>
                </>
              )}

              {role === "enterprise" && (
                <NavLink href="/startups" active={isActive("/startups")}>
                  Discover Startups
                </NavLink>
              )}

              {role === "admin" && (
                <NavLink href="/admin" active={isActive("/admin")}>
                  Admin
                </NavLink>
              )}
            </div>
          </div>

          {/* Right */}
          <div className="flex items-center">
            {/* ✅ NO props — this is correct */}
            <UserButton />
          </div>
        </div>
      </div>
    </nav>
  );
}

/* -------------------- */
/* NavLink helper      */
/* -------------------- */
function NavLink({
  href,
  active,
  children,
}: {
  href: string;
  active: boolean;
  children: React.ReactNode;
}) {
  return (
    <Link
      href={href}
      className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${active
          ? "text-blue-600 border-b-2 border-blue-600"
          : "text-gray-500 hover:text-gray-700"
        }`}
    >
      {children}
    </Link>
  );
}
