// components/startup/StartupDashboard.tsx

"use client";

import { useEffect, useState, useCallback } from "react";
import {
  setAuthToken,
  getMyCredibilityScore,
  getMyLaunches,
  getReviewsByStartup,
  getMyStartup,
} from "@/lib/api";

import CredibilityScoreCard from "./CredibilityScoreCard";
import LaunchListCard from "./LaunchListCard";
import ReviewListCard from "./ReviewListCard";
import QuickActionsCard from "./QuickActionsCard";
import CreateStartupCard from "./CreateStartupCard";

import type {
  CredibilityScoreResponse,
  Launch,
  Review,
  Startup,
} from "@/types";

interface StartupDashboardProps {
  token: string | null;
}

export default function StartupDashboard({ token }: StartupDashboardProps) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [startup, setStartup] = useState<Startup | null>(null);
  const [credibility, setCredibility] =
    useState<CredibilityScoreResponse | null>(null);
  const [launches, setLaunches] = useState<Launch[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);

  const fetchData = useCallback(async () => {
    if (!token) {
      setError("Authentication token not available");
      setLoading(false);
      return;
    }

    try {
      setAuthToken(token);
      console.log("🔐 Token set, fetching startup...");

      // 1️⃣ Try to fetch startup
      let startupData: Startup | null = null;

      try {
        startupData = await getMyStartup();
        console.log("✅ Startup fetched:", startupData);
        setStartup(startupData);
      } catch (err: any) {
        console.log("❌ Startup fetch error:", err.response?.status, err.message);
        // ✅ 404 = onboarding state, NOT an error
        if (err.response?.status === 404) {
          console.log("ℹ️ No startup found - showing onboarding");
          setStartup(null);
          setLoading(false);
          return;
        }
        throw err;
      }

      // 2️⃣ Fetch rest only if startup exists
      console.log("📊 Fetching credibility, launches, reviews...");
      const [credibilityData, launchesData, reviewsData] =
        await Promise.all([
          getMyCredibilityScore().catch(err => {
            console.log("❌ Credibility fetch error:", err.response?.status, err.message);
            throw err;
          }),
          getMyLaunches().catch(err => {
            console.log("❌ Launches fetch error:", err.response?.status, err.message);
            throw err;
          }),
          getReviewsByStartup(startupData.id).catch(err => {
            console.log("❌ Reviews fetch error:", err.response?.status, err.message);
            throw err;
          }),
        ]);

      console.log("✅ All data fetched successfully");
      setCredibility(credibilityData);
      setLaunches(launchesData);
      setReviews(reviewsData);
    } catch (err: any) {
      console.error("💥 Fatal error in fetchData:", err);
      setError(
        err.response?.data?.detail ||
        err.message ||
        "Failed to load dashboard data"
      );
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Refresh handler for after launch creation
  const handleRefresh = useCallback(async () => {
    setLoading(true);
    await fetchData();
  }, [fetchData]);

  // ---------------------------
  // RENDER STATES (ORDER MATTERS)
  // ---------------------------

  if (loading) {
    return <LoadingSkeleton />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  // ✅ Startup missing → onboarding UI
  if (!startup) {
    return <CreateStartupCard onCreated={() => window.location.reload()} />;
  }

  // Safety guard (should not normally hit)
  if (!credibility) {
    return <LoadingSkeleton />;
  }

  // ✅ Full dashboard
  return (
    <div className="space-y-6">
      <CredibilityScoreCard data={credibility} />

      <QuickActionsCard onLaunchCreated={handleRefresh} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <LaunchListCard launches={launches} />
        <ReviewListCard reviews={reviews} />
      </div>
    </div>
  );
}

/* -------------------- */
/* UI STATES            */
/* -------------------- */

function LoadingSkeleton() {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6 h-96 animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div className="h-32 bg-gray-200 rounded mb-4"></div>
        <div className="space-y-3">
          <div className="h-4 bg-gray-200 rounded"></div>
          <div className="h-4 bg-gray-200 rounded"></div>
          <div className="h-4 bg-gray-200 rounded"></div>
        </div>
      </div>
    </div>
  );
}

function ErrorState({ message }: { message: string }) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-6">
      <h3 className="text-red-900 font-semibold mb-2">
        Error Loading Dashboard
      </h3>
      <p className="text-red-700 text-sm mb-4">{message}</p>
    </div>
  );
}