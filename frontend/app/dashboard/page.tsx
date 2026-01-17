// app/dashboard/page.tsx - Role-based dashboard with real data

import { auth, currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import Navbar from "@/components/Navbar";
import StartupDashboard from "@/components/startup/StartupDashboard";

export default async function DashboardPage() {
  const { userId, getToken } = await auth();
  const user = await currentUser();

  if (!userId) {
    redirect("/sign-in");
  }

  const role = user?.publicMetadata?.role as string;
  const token = await getToken({ template: "backend" });

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">
            Welcome back, {user?.firstName || user?.emailAddresses[0].emailAddress}
          </p>
        </div>

        {/* Role-specific dashboards */}
        {!role && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <h3 className="text-yellow-800 font-semibold mb-2">
              Role Not Configured
            </h3>
            <p className="text-yellow-700 text-sm">
              Your user role needs to be set in Clerk. Please add{" "}
              <code className="bg-yellow-100 px-2 py-1 rounded">role</code> to
              your user's public metadata with value: "startup", "enterprise", or
              "admin".
            </p>
          </div>
        )}

        {role === "startup" && <StartupDashboard token={token} />}

        {role === "enterprise" && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-6">
            <h3 className="text-green-900 font-semibold mb-2">
              Enterprise Dashboard Coming Soon
            </h3>
            <p className="text-green-700 text-sm">
              This will show startup discovery and evaluation tools.
            </p>
          </div>
        )}

        {role === "admin" && (
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
            <h3 className="text-purple-900 font-semibold mb-2">
              Admin Dashboard Coming Soon
            </h3>
            <p className="text-purple-700 text-sm">
              This will show verification and moderation tools.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}