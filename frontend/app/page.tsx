// app/page.tsx - Landing page with role-based redirect

import { auth, currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import Link from "next/link";

export default async function HomePage() {
  const { userId } = await auth();

  // If authenticated, redirect to dashboard
  if (userId) {
    redirect("/dashboard");
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-white to-gray-100">
      <div className="max-w-4xl mx-auto px-6 text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          EthAum.ai
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          AI-powered credibility platform for Series A-D B2B startups
        </p>

        <div className="flex gap-4 justify-center mb-12">
          <Link
            href="/sign-up"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition"
          >
            Get Started
          </Link>
          <Link
            href="/sign-in"
            className="px-6 py-3 bg-white text-gray-700 border border-gray-300 rounded-lg font-medium hover:bg-gray-50 transition"
          >
            Sign In
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
          <div className="p-6 bg-white rounded-lg shadow-sm">
            <div className="text-3xl mb-3">🚀</div>
            <h3 className="font-semibold text-gray-900 mb-2">
              For Startups
            </h3>
            <p className="text-gray-600 text-sm">
              Build credibility through launches, reviews, and enterprise validation
            </p>
          </div>

          <div className="p-6 bg-white rounded-lg shadow-sm">
            <div className="text-3xl mb-3">🏢</div>
            <h3 className="font-semibold text-gray-900 mb-2">
              For Enterprises
            </h3>
            <p className="text-gray-600 text-sm">
              Discover trustworthy startups with transparent credibility signals
            </p>
          </div>

          <div className="p-6 bg-white rounded-lg shadow-sm">
            <div className="text-3xl mb-3">✅</div>
            <h3 className="font-semibold text-gray-900 mb-2">
              Transparent Scoring
            </h3>
            <p className="text-gray-600 text-sm">
              Every credibility score is explainable, verifiable, and earned
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}