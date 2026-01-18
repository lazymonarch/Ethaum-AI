// app/dashboard/page.tsx

import { auth, currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import Navbar from "@/components/Navbar";
import StartupDashboard from "@/components/startup/StartupDashboard";

export default async function DashboardPage() {
  const { userId, getToken } = await auth();
  const user = await currentUser();

  if (!userId || !user) {
    redirect("/sign-in");
  }

  const token = await getToken({ template: "backend" });

  if (!token) {
    throw new Error("Failed to fetch Clerk JWT");
  }

  const role = user.unsafeMetadata?.role as string | undefined;

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">
          Welcome back, {user.emailAddresses[0].emailAddress}
        </p>

        {role === "startup" && <StartupDashboard token={token} />}

        {role === "enterprise" && (
          <div className="mt-8 bg-blue-50 p-6 rounded-lg">
            Enterprise dashboard coming next.
          </div>
        )}
      </div>
    </div>
  );
}
